"""
LABREX NSDC Skill Directory & Training Center Adapter
Authority: Master Directive Section 14 & Secondary Mandate Step 8
Source: National Skill Development Corporation (NSDC) & NCVET
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


class NSDCAdapter:
    """
    Adapter for processing NSDC Skill Directory and Accredited Training Centre listings.
    Supports non-aggressive, respectful loading of official registry exports,
    capturing center locations, courses, NSQF levels, and operational schemes.
    """

    def __init__(self, source_version: str = "NSDC-DIRECTORY-2024"):
        self.source_id = "SRC-NSDC-DIR"
        self.source_version = source_version

    def parse_record(
        self,
        raw_row: Dict[str, Any],
        default_period: Optional[date] = None
    ) -> CanonicalTrainingSignal:
        """Parses a single training centre registry entry."""
        obs_date = default_period or date.today()

        center_id = str(raw_row.get("center_id") or raw_row.get("tc_id") or raw_row.get("id") or "TC-UNKNOWN").strip()
        center_name = str(raw_row.get("center_name") or raw_row.get("name") or "Training Centre").strip()
        state_code = raw_row.get("state_code") or raw_row.get("state_id")
        state_name = raw_row.get("state_name") or raw_row.get("state")
        district_code = raw_row.get("district_code") or raw_row.get("district_id")
        district_name = raw_row.get("district_name") or raw_row.get("district")
        pincode = str(raw_row.get("pincode") or raw_row.get("pin") or "")[:6]

        qp_id = raw_row.get("qualification_id") or raw_row.get("qp_code") or raw_row.get("course_id")
        course_name = raw_row.get("course_name") or raw_row.get("job_role")
        nsqf_level = int(raw_row["nsqf_level"]) if "nsqf_level" in raw_row and raw_row["nsqf_level"] else None
        scheme = str(raw_row.get("scheme") or raw_row.get("scheme_name") or "PMKVY/NSDC")
        center_type = str(raw_row.get("center_type") or "TRAINING_CENTRE").upper()

        seats_val = raw_row.get("sanctioned_seats") or raw_row.get("capacity") or 30
        try:
            sanctioned_seats = int(float(seats_val))
        except (ValueError, TypeError):
            sanctioned_seats = 30

        row_hash = compute_record_hash(raw_row)

        geo_ref = GeographyReference(
            country_code="IN",
            state_code=str(state_code) if state_code else None,
            state_name=str(state_name) if state_name else None,
            district_code=str(district_code) if district_code else None,
            district_name=str(district_name) if district_name else None,
            pincode=pincode if pincode else None
        )

        skill_ref = SkillReference(
            qualification_id=str(qp_id) if qp_id else None,
            name=str(course_name) if course_name else None,
            nsqf_level=nsqf_level
        )

        rec_id = f"NSDC-TC-{center_id}-{qp_id or 'ALL'}"

        return CanonicalTrainingSignal(
            source=self.source_id,
            source_record_id=rec_id,
            observation_date=obs_date,
            geography=geo_ref,
            skill=skill_ref,
            metric="training_centre_sanctioned_capacity",
            value=float(sanctioned_seats),
            unit="seats",
            quality=QualityScore(score=100.0, confidence=0.95),
            dataset_version=self.source_version,
            dataset_type=DatasetType.REAL if "FIXTURE" not in self.source_version else DatasetType.FIXTURE,
            raw_payload_hash=row_hash,
            stream_type="INFRASTRUCTURE_CAPACITY",
            center_id=center_id,
            center_name=center_name,
            scheme_name=scheme,
            sanctioned_seats=sanctioned_seats
        )

    def parse_csv(
        self,
        csv_content: Union[str, bytes],
        default_period: Optional[date] = None
    ) -> List[CanonicalTrainingSignal]:
        """Parses CSV directory export."""
        if isinstance(csv_content, bytes):
            text = csv_content.decode("utf-8-sig", errors="replace")
        else:
            text = csv_content

        reader = csv.DictReader(io.StringIO(text))
        signals = []
        for row in reader:
            if not any(row.values()):
                continue
            signals.append(self.parse_record(row, default_period))
        return signals

    def parse_json(
        self,
        json_content: Union[str, bytes, list],
        default_period: Optional[date] = None
    ) -> List[CanonicalTrainingSignal]:
        """Parses JSON directory export."""
        if isinstance(json_content, (str, bytes)):
            data = json.loads(json_content)
        else:
            data = json_content

        if not isinstance(data, list):
            data = [data]

        return [self.parse_record(row, default_period) for row in data]
