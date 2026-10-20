"""
LABREX PMKVY Ingestion Adapter
Authority: Master Directive Section 14 & Secondary Mandate Step 7
Source: Ministry of Skill Development and Entrepreneurship (MSDE) & NSDC
"""

import csv
import io
import json
from datetime import date
from typing import Any, Dict, List, Optional, Union

from backend.app.schemas.staging import (
    CanonicalTrainingSignal,
    DatasetType,
    GeographyReference,
    OccupationReference,
    QualityScore,
    SkillReference
)
from backend.app.services.data.lineage.provenance import compute_record_hash


class PMKVYAdapter:
    """
    Adapter for processing PMKVY outcome datasets (PMKVY 1.0, 2.0, 3.0, 4.0).
    Strictly separates:
    - Training Pipeline: Enrolled candidates
    - Certified Supply: Assessed and certified candidates
    - Infrastructure Capacity: Active centres and seat allotments
    """

    def __init__(self, source_version: str = "PMKVY-4.0-2024"):
        self.source_id = "SRC-PMKVY-OUT"
        self.source_version = source_version

    def parse_record(
        self,
        raw_row: Dict[str, Any],
        default_period: Optional[date] = None
    ) -> List[CanonicalTrainingSignal]:
        """
        Parses a single row and generates separated CanonicalTrainingSignal records
        for Pipeline, Certified Supply, and Infrastructure Capacity.
        """
        signals: List[CanonicalTrainingSignal] = []

        obs_date = default_period or date(2024, 3, 31)
        if "period" in raw_row or "year" in raw_row or "financial_year" in raw_row:
            raw_yr = str(raw_row.get("financial_year") or raw_row.get("year") or raw_row.get("period"))
            try:
                yr = int(raw_yr[:4])
                obs_date = date(yr, 3, 31)
            except Exception:
                pass

        state_code = raw_row.get("state_code") or raw_row.get("state_id")
        state_name = raw_row.get("state_name") or raw_row.get("state")
        district_code = raw_row.get("district_code") or raw_row.get("district_id")
        district_name = raw_row.get("district_name") or raw_row.get("district")
        
        qp_id = raw_row.get("job_role_code") or raw_row.get("qp_code") or raw_row.get("qualification_id")
        job_role = raw_row.get("job_role") or raw_row.get("course_name") or raw_row.get("trade")
        scheme_name = str(raw_row.get("scheme") or raw_row.get("component") or "PMKVY-STT")

        # Counts
        enrolled = int(float(raw_row.get("enrolled") or raw_row.get("enrolled_count") or 0))
        trained = int(float(raw_row.get("trained") or raw_row.get("trained_count") or 0))
        certified = int(float(raw_row.get("certified") or raw_row.get("certified_count") or 0))
        placed = int(float(raw_row.get("placed") or raw_row.get("placed_count") or 0))
        centres = int(float(raw_row.get("centres") or raw_row.get("training_centres_count") or 0))
        seats = int(float(raw_row.get("seats") or raw_row.get("sanctioned_seats") or 0))

        row_hash = compute_record_hash(raw_row)

        geo_ref = GeographyReference(
            country_code="IN",
            state_code=str(state_code) if state_code else None,
            state_name=str(state_name) if state_name else None,
            district_code=str(district_code) if district_code else None,
            district_name=str(district_name) if district_name else None
        )

        skill_ref = SkillReference(
            qualification_id=str(qp_id) if qp_id else None,
            name=str(job_role) if job_role else None
        )

        # 1. Training Pipeline Signal (Enrolled / Ongoing)
        if enrolled > 0 or trained > 0:
            rec_id = f"PMKVY-PIPE-{district_code or state_code or 'NAT'}-{qp_id or 'GEN'}-{obs_date.isoformat()}"
            signals.append(CanonicalTrainingSignal(
                source=self.source_id,
                source_record_id=rec_id,
                observation_date=obs_date,
                geography=geo_ref,
                skill=skill_ref,
                metric="candidates_enrolled_pipeline",
                value=float(enrolled),
                unit="count",
                quality=QualityScore(score=100.0, confidence=0.95),
                dataset_version=self.source_version,
                dataset_type=DatasetType.REAL if "FIXTURE" not in self.source_version else DatasetType.FIXTURE,
                raw_payload_hash=row_hash,
                stream_type="TRAINING_PIPELINE",
                scheme_name=scheme_name,
                enrolled_count=enrolled,
                trained_count=trained
            ))

        # 2. Certified Supply Signal (Certified & Placed)
        if certified > 0 or placed > 0:
            rec_id = f"PMKVY-CERT-{district_code or state_code or 'NAT'}-{qp_id or 'GEN'}-{obs_date.isoformat()}"
            signals.append(CanonicalTrainingSignal(
                source=self.source_id,
                source_record_id=rec_id,
                observation_date=obs_date,
                geography=geo_ref,
                skill=skill_ref,
                metric="candidates_certified_supply",
                value=float(certified),
                unit="count",
                quality=QualityScore(score=100.0, confidence=0.98),
                dataset_version=self.source_version,
                dataset_type=DatasetType.REAL if "FIXTURE" not in self.source_version else DatasetType.FIXTURE,
                raw_payload_hash=row_hash,
                stream_type="CERTIFIED_SUPPLY",
                scheme_name=scheme_name,
                trained_count=trained,
                certified_count=certified,
                placed_count=placed
            ))

        # 3. Infrastructure Capacity Signal (Centres & Allocated Seats)
        if centres > 0 or seats > 0:
            rec_id = f"PMKVY-CAP-{district_code or state_code or 'NAT'}-{obs_date.isoformat()}"
            signals.append(CanonicalTrainingSignal(
                source=self.source_id,
                source_record_id=rec_id,
                observation_date=obs_date,
                geography=geo_ref,
                skill=skill_ref,
                metric="training_centre_capacity",
                value=float(seats if seats > 0 else centres),
                unit="count",
                quality=QualityScore(score=100.0, confidence=0.95),
                dataset_version=self.source_version,
                dataset_type=DatasetType.REAL if "FIXTURE" not in self.source_version else DatasetType.FIXTURE,
                raw_payload_hash=row_hash,
                stream_type="INFRASTRUCTURE_CAPACITY",
                scheme_name=scheme_name,
                sanctioned_seats=seats
            ))

        return signals

    def parse_csv(
        self,
        csv_content: Union[str, bytes],
        default_period: Optional[date] = None
    ) -> List[CanonicalTrainingSignal]:
        """Parses CSV content of PMKVY reports."""
        if isinstance(csv_content, bytes):
            text = csv_content.decode("utf-8-sig", errors="replace")
        else:
            text = csv_content

        reader = csv.DictReader(io.StringIO(text))
        all_signals = []
        for row in reader:
            if not any(row.values()):
                continue
            all_signals.extend(self.parse_record(row, default_period))
        return all_signals

    def parse_json(
        self,
        json_content: Union[str, bytes, list],
        default_period: Optional[date] = None
    ) -> List[CanonicalTrainingSignal]:
        """Parses JSON content of PMKVY reports."""
        if isinstance(json_content, (str, bytes)):
            data = json.loads(json_content)
        else:
            data = json_content

        if not isinstance(data, list):
            data = [data]

        all_signals = []
        for row in data:
            all_signals.extend(self.parse_record(row, default_period))
        return all_signals
