"""
LABREX NCO-2015 Preprocessor & Taxonomy Parser
Authority: Master Directive Section 14 & Secondary Mandate Step 4
Source: Official National Classification of Occupations 2015 (Vol I & II)
"""

import csv
import io
import json
import os
import re
from datetime import date
from typing import Any, Dict, List, Optional, Union

from backend.app.schemas.staging import (
    CanonicalOccupation,
    DatasetType,
    GeographyReference,
    OccupationReference,
    QualityScore,
    SkillReference
)
from backend.app.services.data.lineage.provenance import compute_record_hash

# Official NCO-2015 Division mapping
NCO_DIVISIONS = {
    "0": "Armed Forces Occupations",
    "1": "Managers",
    "2": "Professionals",
    "3": "Technicians and Associate Professionals",
    "4": "Clerical Support Workers",
    "5": "Service and Sales Workers",
    "6": "Skilled Agricultural, Forestry and Fishery Workers",
    "7": "Craft and Related Trades Workers",
    "8": "Plant and Machine Operators and Assemblers",
    "9": "Elementary Occupations"
}


class NCOParser:
    """
    Parser for official NCO-2015 datasets.
    Extracts 8-digit occupation codes, hierarchy (division, sub-division, group, family),
    canonical job titles, descriptions, and verified sector associations.
    """

    def __init__(self, source_version: str = "NCO-2015-v1.0"):
        self.source_version = source_version
        self.source_id = "SRC-NCO-2015"

    def parse_hierarchy_from_code(self, raw_code: str) -> Dict[str, Optional[str]]:
        """
        Decomposes an NCO code into its constituent levels:
        Example: '7421.0300' or '7421.03'
        - Division: 7
        - Sub-division: 74
        - Group: 742
        - Family: 7421
        - Occupation Code: 7421.0300
        """
        cleaned = re.sub(r"[^\d.]", "", raw_code.strip())
        parts = cleaned.split(".")
        family_part = parts[0]
        
        division = family_part[0] if len(family_part) >= 1 else None
        sub_div = family_part[:2] if len(family_part) >= 2 else None
        group = family_part[:3] if len(family_part) >= 3 else None
        family = family_part[:4] if len(family_part) >= 4 else None

        return {
            "division": division,
            "sub_division": sub_div,
            "group": group,
            "family": family,
            "nco_code": cleaned
        }

    def parse_record(self, raw_row: Dict[str, Any], observation_date: Optional[date] = None) -> CanonicalOccupation:
        """Parses a single dictionary record into a CanonicalOccupation staging model."""
        obs_date = observation_date or date(2015, 1, 1)

        raw_code = str(raw_row.get("nco_code") or raw_row.get("code") or raw_row.get("occupation_code") or "").strip()
        title = str(raw_row.get("title") or raw_row.get("occupation") or raw_row.get("occupation_title") or "").strip()
        description = raw_row.get("description") or raw_row.get("task_description")
        sector = raw_row.get("sector") or raw_row.get("sector_id") or raw_row.get("ssc")
        isco = raw_row.get("isco_08") or raw_row.get("isco_mapping")

        hierarchy = self.parse_hierarchy_from_code(raw_code)
        rec_id = f"NCO-{hierarchy['nco_code'] or hash(title)}"
        row_hash = compute_record_hash(raw_row)

        occ_ref = OccupationReference(
            nco_code=hierarchy["nco_code"],
            title=title,
            division=hierarchy["division"],
            sub_division=hierarchy["sub_division"],
            group_code=hierarchy["group"],
            family_code=hierarchy["family"],
            sector_id=str(sector) if sector else None
        )

        return CanonicalOccupation(
            source=self.source_id,
            source_record_id=rec_id,
            observation_date=obs_date,
            geography=GeographyReference(country_code="IN"),
            occupation=occ_ref,
            skill=SkillReference(),
            metric="occupational_definition",
            value=1.0,
            unit="taxonomy_entity",
            quality=QualityScore(score=100.0, confidence=1.0),
            dataset_version=self.source_version,
            dataset_type=DatasetType.REAL if "FIXTURE" not in self.source_version else DatasetType.FIXTURE,
            raw_payload_hash=row_hash,
            is_authoritative=True,
            isco_08_mapping=str(isco) if isco else None,
            task_description=str(description) if description else None
        )

    def parse_csv(self, csv_content: Union[str, bytes], observation_date: Optional[date] = None) -> List[CanonicalOccupation]:
        """Parses CSV string/bytes of NCO taxonomy table."""
        if isinstance(csv_content, bytes):
            text = csv_content.decode("utf-8-sig", errors="replace")
        else:
            text = csv_content

        reader = csv.DictReader(io.StringIO(text))
        canonical_records = []
        for row in reader:
            if not any(row.values()):
                continue
            canonical_records.append(self.parse_record(row, observation_date))
        return canonical_records

    def parse_json(self, json_content: Union[str, bytes, list], observation_date: Optional[date] = None) -> List[CanonicalOccupation]:
        """Parses JSON array of NCO taxonomy records."""
        if isinstance(json_content, (str, bytes)):
            data = json.loads(json_content)
        else:
            data = json_content

        if not isinstance(data, list):
            data = [data]

        return [self.parse_record(row, observation_date) for row in data]
