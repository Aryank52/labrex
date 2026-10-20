"""
LABREX Raw Dataset Pre-Ingestion Validator
Authority: Master Directive Section 14 & Secondary Ingestion Mandate Step 7
Scope: Verifies file existence, allowed extensions, size, PII safety, and schema validity before any ingestion.
Rule: Do NOT transform or ingest source files here. Pure validation only.
"""

import csv
from datetime import datetime, timezone
from enum import Enum
import json
import os
from typing import Any, Dict, List, Optional, Tuple
from pydantic import BaseModel, Field

from backend.app.services.data.registration import (
    compute_sha256,
    load_all_manifests,
    match_file_to_manifest
)

ALLOWED_EXTENSIONS = {
    ".csv", ".tsv", ".xlsx", ".xls", ".json", ".geojson",
    ".txt", ".pdf", ".zip", ".gz", ".tar",
    ".shp", ".dbf", ".shx", ".prj"
}

FORBIDDEN_PII_KEYWORDS = [
    "aadhaar", "uidai", "aadhaar_no", "mobile", "phone", "contact",
    "worker_name", "first_name", "last_name", "full_name",
    "bank_account", "account_no", "ifsc", "dob", "date_of_birth"
]


class RawValidationStatus(str, Enum):
    VALIDATED = "VALIDATED"
    WARNING = "WARNING"
    FAILED = "FAILED"


class RawFileCheckResult(BaseModel):
    file_path: str
    filename: str
    exists: bool = True
    extension_allowed: bool = True
    size_reasonable: bool = True
    size_bytes: int = 0
    manifest_match: bool = True
    matched_manifest: Optional[str] = None
    matched_source_id: Optional[str] = None
    hash_verified: Optional[bool] = None
    pii_guard_passed: bool = True
    schema_valid: bool = True
    overall_status: RawValidationStatus = RawValidationStatus.VALIDATED
    violations: List[str] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)


class RawValidationBatchReport(BaseModel):
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    total_files_inspected: int
    passed_count: int
    warning_count: int
    failed_count: int
    results: List[RawFileCheckResult] = Field(default_factory=list)


class RawDataValidator:
    """
    Validates staged raw files in data/raw/ before any ingestion takes place.
    """

    def __init__(self, manifests_dir: str = "data/manifests"):
        self.manifests_dir = manifests_dir
        self.manifests = load_all_manifests(manifests_dir)

    def check_pii_in_file(self, file_path: str) -> Tuple[bool, List[str]]:
        """Scans headers of tabular/json files for PII keywords."""
        violations = []
        _, ext = os.path.splitext(file_path.lower())

        if ext in {".csv", ".tsv"}:
            try:
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    header_line = f.readline()
                    for keyword in FORBIDDEN_PII_KEYWORDS:
                        if keyword in header_line.lower():
                            violations.append(f"Forbidden PII keyword '{keyword}' found in CSV header")
            except Exception as e:
                violations.append(f"Could not inspect CSV header: {e}")

        elif ext == ".json":
            try:
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    data = json.load(f)
                    sample = data[0] if isinstance(data, list) and data else (data if isinstance(data, dict) else {})
                    if isinstance(sample, dict):
                        for k in sample.keys():
                            for keyword in FORBIDDEN_PII_KEYWORDS:
                                if keyword in k.lower():
                                    violations.append(f"Forbidden PII keyword '{keyword}' found in JSON key: '{k}'")
            except Exception as e:
                violations.append(f"Could not inspect JSON keys: {e}")

        return len(violations) == 0, violations

    def check_schema_readability(self, file_path: str) -> Tuple[bool, List[str]]:
        """Verifies that machine-readable files (CSV, JSON, GeoJSON) are parseable."""
        violations = []
        _, ext = os.path.splitext(file_path.lower())

        if ext in {".csv", ".tsv"}:
            try:
                delimiter = "\t" if ext == ".tsv" else ","
                with open(file_path, "r", encoding="utf-8", errors="replace") as f:
                    reader = csv.reader(f, delimiter=delimiter)
                    first_row = next(reader, None)
                    if not first_row or len(first_row) == 0:
                        violations.append("CSV file appears completely empty or unparseable")
            except Exception as e:
                violations.append(f"Failed to read CSV structure: {e}")

        elif ext in {".json", ".geojson"}:
            try:
                with open(file_path, "r", encoding="utf-8", errors="replace") as f:
                    parsed = json.load(f)
                    if ext == ".geojson":
                        if not isinstance(parsed, dict) or "type" not in parsed:
                            violations.append("GeoJSON missing mandatory root 'type' attribute")
            except Exception as e:
                violations.append(f"Invalid JSON/GeoJSON syntax: {e}")

        return len(violations) == 0, violations

    def validate_file(self, file_path: str) -> RawFileCheckResult:
        """Runs full validation battery on a single raw file."""
        filename = os.path.basename(file_path)
        violations: List[str] = []
        warnings: List[str] = []

        # 1. Existence Check
        if not os.path.isfile(file_path):
            return RawFileCheckResult(
                file_path=file_path,
                filename=filename,
                exists=False,
                overall_status=RawValidationStatus.FAILED,
                violations=["File does not exist on disk"]
            )

        # 2. Extension Check
        _, ext = os.path.splitext(file_path.lower())
        extension_allowed = ext in ALLOWED_EXTENSIONS
        if not extension_allowed:
            violations.append(f"Extension '{ext}' is not permitted for raw datasets")

        # 3. Size Check
        size_bytes = os.path.getsize(file_path)
        size_reasonable = True
        if size_bytes == 0:
            violations.append("File is 0 bytes (empty file)")
            size_reasonable = False
        elif size_bytes > 1073741824:  # 1 GB hard cap
            violations.append(f"File size {size_bytes} exceeds maximum platform cap of 1GB")
            size_reasonable = False

        # 4. Manifest Match
        m_name, s_id, t_key, missing = match_file_to_manifest(file_path, self.manifests)
        manifest_match = (m_name is not None)
        if not manifest_match:
            warnings.append("File does not match any official manifest pattern; considered unexpected")

        # Check manifest size bounds if specified
        if m_name and m_name in self.manifests:
            max_size = self.manifests[m_name].get("max_file_size_bytes")
            if max_size and size_bytes > max_size:
                violations.append(f"File size {size_bytes} exceeds manifest limit {max_size}")
                size_reasonable = False

        # 5. Hash Check
        hash_verified = None
        if m_name and m_name in self.manifests:
            f_spec = self.manifests[m_name].get("file_spec", {})
            expected_hash = f_spec.get("expected_checksum")
            if expected_hash and not expected_hash.startswith("e3b0c442"):
                actual_hash = compute_sha256(file_path)
                hash_verified = (actual_hash.lower() == expected_hash.lower())
                if not hash_verified:
                    violations.append(f"SHA-256 mismatch: expected {expected_hash}, got {actual_hash}")

        # 6. PII Policy Check
        pii_passed, pii_violations = self.check_pii_in_file(file_path)
        if not pii_passed:
            violations.extend(pii_violations)

        # 7. Schema / Readability Check
        schema_valid, schema_violations = self.check_schema_readability(file_path)
        if not schema_valid:
            violations.extend(schema_violations)

        # Overall Status Determination
        if violations:
            overall_status = RawValidationStatus.FAILED
        elif warnings:
            overall_status = RawValidationStatus.WARNING
        else:
            overall_status = RawValidationStatus.VALIDATED

        return RawFileCheckResult(
            file_path=os.path.abspath(file_path),
            filename=filename,
            exists=True,
            extension_allowed=extension_allowed,
            size_reasonable=size_reasonable,
            size_bytes=size_bytes,
            manifest_match=manifest_match,
            matched_manifest=m_name,
            matched_source_id=s_id,
            hash_verified=hash_verified,
            pii_guard_passed=pii_passed,
            schema_valid=schema_valid,
            overall_status=overall_status,
            violations=violations,
            warnings=warnings
        )

    def validate_raw_directory(self, raw_dir: str = "data/raw") -> RawValidationBatchReport:
        """Inspects all files in data/raw/ (excluding README and .gitkeep)."""
        results: List[RawFileCheckResult] = []
        passed = 0
        warns = 0
        fails = 0

        if os.path.isdir(raw_dir):
            for root, _, files in os.walk(raw_dir):
                for file in files:
                    if file.lower() in {"readme.md", ".gitkeep", ".ds_store"}:
                        continue
                    full_path = os.path.join(root, file)
                    res = self.validate_file(full_path)
                    results.append(res)
                    if res.overall_status == RawValidationStatus.VALIDATED:
                        passed += 1
                    elif res.overall_status == RawValidationStatus.WARNING:
                        warns += 1
                    else:
                        fails += 1

        return RawValidationBatchReport(
            timestamp=datetime.now(timezone.utc),
            total_files_inspected=len(results),
            passed_count=passed,
            warning_count=warns,
            failed_count=fails,
            results=results
        )
