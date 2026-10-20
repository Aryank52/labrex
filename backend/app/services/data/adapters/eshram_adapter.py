"""
LABREX e-Shram Aggregate Ingestion Adapter
Authority: Master Directive Section 14 & Secondary Mandate Step 6
Source: Ministry of Labour & Employment (MoLE) e-Shram Public Dashboard

CRITICAL PRIVACY DIRECTIVE:
Under no circumstances may individual worker PII (Aadhaar, mobile number,
worker name, bank account, residential address) be ingested.
Only public district and occupation-sector aggregate counts are processed.
"""

import csv
import io
import json
from datetime import date
from typing import Any, Dict, List, Optional, Union

from backend.app.schemas.staging import (
    CanonicalWorkforceSignal,
    DatasetType,
    GeographyReference,
    OccupationReference,
    QualityScore,
    SkillReference
)
from backend.app.services.data.lineage.provenance import compute_record_hash


class PIISafetyViolationError(Exception):
    """Raised when incoming payload contains individual worker PII fields."""
    pass


FORBIDDEN_PII_COLUMNS = {
    "aadhaar", "uidai", "aadhaar_no", "mobile", "phone", "contact",
    "worker_name", "first_name", "last_name", "full_name",
    "bank_account", "account_no", "ifsc", "dob", "date_of_birth", "address"
}


class EShramAdapter:
    """
    Adapter for processing authorized public aggregate extracts from e-Shram portal.
    Enforces strict PII blocking, extracts district aggregates, occupation-sector counts,
    and monthly snapshot timestamps.
    """

    def __init__(self, source_version: str = "ESHRAM-AGG-2024"):
        self.source_id = "SRC-ESHRAM-AGG"
        self.source_version = source_version

    def verify_no_pii(self, field_names: List[str]) -> None:
        """Inspects column headers and raises PIISafetyViolationError if PII is detected."""
        for field in field_names:
            field_clean = field.strip().lower()
            if any(forbidden in field_clean for forbidden in FORBIDDEN_PII_COLUMNS):
                raise PIISafetyViolationError(
                    f"CRITICAL SECURITY GUARD: Ingestion rejected. Forbidden PII column detected: '{field}'"
                )

    def parse_record(self, raw_row: Dict[str, Any], default_snapshot_date: Optional[date] = None) -> CanonicalWorkforceSignal:
        """Parses a single public aggregate district/sector record."""
        self.verify_no_pii(list(raw_row.keys()))

        # Determine snapshot date
        snapshot_date = default_snapshot_date or date.today()
        if "snapshot_date" in raw_row or "date" in raw_row or "month" in raw_row:
            raw_d = str(raw_row.get("snapshot_date") or raw_row.get("date") or raw_row.get("month"))
            try:
                # Handle YYYY-MM or YYYY-MM-DD
                parts = raw_d.split("-")
                if len(parts) >= 2:
                    snapshot_date = date(int(parts[0]), int(parts[1]), int(parts[2]) if len(parts) >= 3 else 1)
            except Exception:
                pass

        state_code = raw_row.get("state_code") or raw_row.get("state_id")
        state_name = raw_row.get("state_name") or raw_row.get("state")
        district_code = raw_row.get("district_code") or raw_row.get("district_id")
        district_name = raw_row.get("district_name") or raw_row.get("district")
        sector_occ = str(raw_row.get("occupation_sector") or raw_row.get("sector") or raw_row.get("occupation") or "ALL_UNORGANIZED").strip()
        
        # Worker count
        count_val = raw_row.get("worker_count") or raw_row.get("registered_workers") or raw_row.get("count") or 0
        try:
            worker_count = int(float(count_val))
        except (ValueError, TypeError):
            worker_count = 0

        # Optional demographic ratios
        male_ratio = float(raw_row["male_ratio"]) if "male_ratio" in raw_row else None
        female_ratio = float(raw_row["female_ratio"]) if "female_ratio" in raw_row else None

        rec_id = f"ESHRAM-{district_code or state_code or 'NAT'}-{sector_occ}-{snapshot_date.isoformat()}"
        row_hash = compute_record_hash(raw_row)

        geo_ref = GeographyReference(
            country_code="IN",
            state_code=str(state_code) if state_code else None,
            state_name=str(state_name) if state_name else None,
            district_code=str(district_code) if district_code else None,
            district_name=str(district_name) if district_name else None
        )

        occ_ref = OccupationReference(
            title=sector_occ,
            sector_id=f"SEC-{sector_occ.upper()[:10]}"
        )

        return CanonicalWorkforceSignal(
            source=self.source_id,
            source_record_id=rec_id,
            observation_date=snapshot_date,
            geography=geo_ref,
            occupation=occ_ref,
            skill=SkillReference(),
            metric="unorganized_worker_registrations",
            value=float(worker_count),
            unit="count",
            quality=QualityScore(score=100.0, confidence=0.90),
            dataset_version=self.source_version,
            dataset_type=DatasetType.REAL if "FIXTURE" not in self.source_version else DatasetType.FIXTURE,
            raw_payload_hash=row_hash,
            workforce_sector=sector_occ,
            worker_count=worker_count,
            male_ratio=male_ratio,
            female_ratio=female_ratio
        )

    def parse_csv(self, csv_content: Union[str, bytes], default_snapshot_date: Optional[date] = None) -> List[CanonicalWorkforceSignal]:
        """Parses CSV content of aggregate public statistics."""
        if isinstance(csv_content, bytes):
            text = csv_content.decode("utf-8-sig", errors="replace")
        else:
            text = csv_content

        reader = csv.DictReader(io.StringIO(text))
        if reader.fieldnames:
            self.verify_no_pii(list(reader.fieldnames))

        signals = []
        for row in reader:
            if not any(row.values()):
                continue
            signals.append(self.parse_record(row, default_snapshot_date))
        return signals

    def parse_json(self, json_content: Union[str, bytes, list], default_snapshot_date: Optional[date] = None) -> List[CanonicalWorkforceSignal]:
        """Parses JSON content of aggregate public statistics."""
        if isinstance(json_content, (str, bytes)):
            data = json.loads(json_content)
        else:
            data = json_content

        if not isinstance(data, list):
            data = [data]

        signals = []
        for row in data:
            signals.append(self.parse_record(row, default_snapshot_date))
        return signals
