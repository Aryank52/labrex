"""
LABREX PLFS Ingestion Adapter
Authority: Master Directive Section 14 & Secondary Mandate Step 5
Source: Ministry of Statistics and Programme Implementation (MoSPI) / NSSO
"""

import csv
import io
import json
from datetime import date
from typing import Any, Dict, List, Optional, Union
import pandas as pd

from backend.app.schemas.staging import (
    CanonicalWorkforceSignal,
    DatasetType,
    FrequencyType,
    GeographyReference,
    OccupationReference,
    QualityScore,
    SkillReference
)
from backend.app.services.data.lineage.provenance import compute_record_hash

# Standard mapping for Indian State names to canonical State codes
STATE_NAME_TO_CODE = {
    "ANDAMAN & NICOBAR ISLANDS": "IN-AN", "ANDHRA PRADESH": "IN-AP", "ARUNACHAL PRADESH": "IN-AR",
    "ASSAM": "IN-AS", "BIHAR": "IN-BR", "CHANDIGARH": "IN-CH", "CHHATTISGARH": "IN-CT",
    "DELHI": "IN-DL", "GOA": "IN-GA", "GUJARAT": "IN-GJ", "HARYANA": "IN-HR",
    "HIMACHAL PRADESH": "IN-HP", "JAMMU & KASHMIR": "IN-JK", "JHARKHAND": "IN-JH",
    "KARNATAKA": "IN-KA", "KERALA": "IN-KL", "LADAKH": "IN-LA", "LAKSHADWEEP": "IN-LD",
    "MADHYA PRADESH": "IN-MP", "MAHARASHTRA": "IN-MH", "MANIPUR": "IN-MN", "MEGHALAYA": "IN-ML",
    "MIZORAM": "IN-MZ", "NAGALAND": "IN-NL", "ODISHA": "IN-OD", "PUDUCHERRY": "IN-PY",
    "PUNJAB": "IN-PB", "RAJASTHAN": "IN-RJ", "SIKKIM": "IN-SK", "TAMIL NADU": "IN-TN",
    "TELANGANA": "IN-TG", "TRIPURA": "IN-TR", "UTTAR PRADESH": "IN-UP", "UTTARAKHAND": "IN-UT",
    "WEST BENGAL": "IN-WB", "ALL INDIA": "IN"
}


class PLFSAdapter:
    """
    Adapter for processing Periodic Labour Force Survey (PLFS) releases.
    Extracts minimal high-value metrics (LFPR, WPR, UR, Industry distributions)
    from CSV, XLSX, or Fixed-Width Microdata with explicit frequency tagging.
    """

    def __init__(self, source_version: str = "PLFS-2023-24"):
        self.source_id = "SRC-PLFS-ANN"
        self.source_version = source_version

    def resolve_state_code(self, raw_state: Optional[str]) -> Optional[str]:
        if not raw_state:
            return None
        st_clean = str(raw_state).strip().upper()
        if st_clean.startswith("IN-"):
            return st_clean
        return STATE_NAME_TO_CODE.get(st_clean)

    def parse_record(
        self,
        raw_row: Dict[str, Any],
        default_period: Optional[date] = None,
        frequency: FrequencyType = FrequencyType.ANNUAL
    ) -> List[CanonicalWorkforceSignal]:
        """
        Transforms a PLFS row containing indicators (LFPR, WPR, UR)
        into normalized CanonicalWorkforceSignal instances.
        """
        signals: List[CanonicalWorkforceSignal] = []

        raw_state = raw_row.get("state") or raw_row.get("state_name") or raw_row.get("state_code")
        state_code = self.resolve_state_code(str(raw_state)) if raw_state else None
        
        # Determine observation date
        obs_date = default_period or date(2024, 6, 30)
        if "year" in raw_row or "survey_year" in raw_row:
            try:
                yr = int(str(raw_row.get("year") or raw_row.get("survey_year"))[:4])
                obs_date = date(yr, 6, 30)
            except (ValueError, TypeError):
                pass

        row_hash = compute_record_hash(raw_row)
        round_name = str(raw_row.get("round") or raw_row.get("survey_round") or self.source_version)
        sector_area = str(raw_row.get("sector") or raw_row.get("area") or "RURAL+URBAN").upper()

        geo_ref = GeographyReference(
            country_code="IN",
            state_code=state_code,
            state_name=str(raw_state) if raw_state else None
        )

        # 1. LFPR
        if "lfpr" in raw_row or "LFPR" in raw_row:
            val = float(raw_row.get("lfpr") or raw_row.get("LFPR"))
            rec_id = f"PLFS-{round_name}-{state_code or 'NAT'}-LFPR-{sector_area}"
            signals.append(CanonicalWorkforceSignal(
                source=self.source_id,
                source_record_id=rec_id,
                observation_date=obs_date,
                geography=geo_ref,
                metric="labour_force_participation_rate",
                value=val,
                unit="percentage",
                quality=QualityScore(score=100.0, confidence=0.95),
                dataset_version=self.source_version,
                dataset_type=DatasetType.REAL if "FIXTURE" not in self.source_version else DatasetType.FIXTURE,
                survey_round=round_name,
                workforce_sector=sector_area,
                raw_payload_hash=row_hash
            ))

        # 2. WPR
        if "wpr" in raw_row or "WPR" in raw_row:
            val = float(raw_row.get("wpr") or raw_row.get("WPR"))
            rec_id = f"PLFS-{round_name}-{state_code or 'NAT'}-WPR-{sector_area}"
            signals.append(CanonicalWorkforceSignal(
                source=self.source_id,
                source_record_id=rec_id,
                observation_date=obs_date,
                geography=geo_ref,
                metric="worker_population_ratio",
                value=val,
                unit="percentage",
                quality=QualityScore(score=100.0, confidence=0.95),
                dataset_version=self.source_version,
                dataset_type=DatasetType.REAL if "FIXTURE" not in self.source_version else DatasetType.FIXTURE,
                survey_round=round_name,
                workforce_sector=sector_area,
                raw_payload_hash=row_hash
            ))

        # 3. Unemployment Rate
        if "unemployment_rate" in raw_row or "UR" in raw_row or "ur" in raw_row:
            val = float(raw_row.get("unemployment_rate") or raw_row.get("UR") or raw_row.get("ur"))
            rec_id = f"PLFS-{round_name}-{state_code or 'NAT'}-UR-{sector_area}"
            signals.append(CanonicalWorkforceSignal(
                source=self.source_id,
                source_record_id=rec_id,
                observation_date=obs_date,
                geography=geo_ref,
                metric="unemployment_rate",
                value=val,
                unit="percentage",
                quality=QualityScore(score=100.0, confidence=0.95),
                dataset_version=self.source_version,
                dataset_type=DatasetType.REAL if "FIXTURE" not in self.source_version else DatasetType.FIXTURE,
                survey_round=round_name,
                workforce_sector=sector_area,
                raw_payload_hash=row_hash
            ))

        # 4. Broad Industry Distributions
        for ind_key, metric_name in [
            ("share_agriculture", "worker_share_agriculture"),
            ("share_industry", "worker_share_secondary_industry"),
            ("share_services", "worker_share_tertiary_services")
        ]:
            if ind_key in raw_row:
                val = float(raw_row[ind_key])
                rec_id = f"PLFS-{round_name}-{state_code or 'NAT'}-{ind_key.upper()}"
                signals.append(CanonicalWorkforceSignal(
                    source=self.source_id,
                    source_record_id=rec_id,
                    observation_date=obs_date,
                    geography=geo_ref,
                    metric=metric_name,
                    value=val,
                    unit="percentage",
                    quality=QualityScore(score=100.0, confidence=0.90),
                    dataset_version=self.source_version,
                    dataset_type=DatasetType.REAL if "FIXTURE" not in self.source_version else DatasetType.FIXTURE,
                    survey_round=round_name,
                    workforce_sector=sector_area,
                    raw_payload_hash=row_hash
                ))

        return signals

    def parse_csv(
        self,
        csv_content: Union[str, bytes],
        default_period: Optional[date] = None,
        frequency: FrequencyType = FrequencyType.ANNUAL
    ) -> List[CanonicalWorkforceSignal]:
        """Parses CSV string/bytes of PLFS statement extracts."""
        if isinstance(csv_content, bytes):
            text = csv_content.decode("utf-8-sig", errors="replace")
        else:
            text = csv_content

        reader = csv.DictReader(io.StringIO(text))
        all_signals = []
        for row in reader:
            if not any(row.values()):
                continue
            all_signals.extend(self.parse_record(row, default_period, frequency))
        return all_signals

    def parse_dataframe(
        self,
        df: pd.DataFrame,
        default_period: Optional[date] = None,
        frequency: FrequencyType = FrequencyType.ANNUAL
    ) -> List[CanonicalWorkforceSignal]:
        """Parses pandas DataFrame (from CSV or XLSX)."""
        records = df.to_dict(orient="records")
        all_signals = []
        for r in records:
            all_signals.extend(self.parse_record(r, default_period, frequency))
        return all_signals

    def parse_fixed_width_txt(
        self,
        txt_content: str,
        layout: List[Dict[str, Any]],
        default_period: Optional[date] = None,
        frequency: FrequencyType = FrequencyType.ANNUAL
    ) -> List[CanonicalWorkforceSignal]:
        """
        Parses microdata layout where each field is defined by start_col, end_col, and name.
        """
        all_signals = []
        for line in txt_content.splitlines():
            if not line.strip():
                continue
            row: Dict[str, Any] = {}
            for col_def in layout:
                start = col_def["start"] - 1
                end = col_def["end"]
                name = col_def["name"]
                row[name] = line[start:end].strip()
            all_signals.extend(self.parse_record(row, default_period, frequency))
        return all_signals
