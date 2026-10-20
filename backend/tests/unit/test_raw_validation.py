"""
Unit Tests for Raw Dataset Registration and Validation
Authority: Master Directive Section 14 & Secondary Ingestion Mandate Step 11
"""

import os
import tempfile
import pytest

from backend.app.services.data.raw_validator import (
    RawDataValidator,
    RawValidationStatus
)
from backend.app.services.data.registration import (
    compute_sha256,
    detect_file_type,
    load_all_manifests,
    match_file_to_manifest,
    register_file,
    scan_and_register_all
)


@pytest.fixture
def validator():
    return RawDataValidator(manifests_dir="data/manifests")


def test_file_type_detection():
    assert detect_file_type("test.csv") == "TABULAR_DELIMITED"
    assert detect_file_type("test.xlsx") == "SPREADSHEET_EXCEL"
    assert detect_file_type("test.geojson") == "GEOSPATIAL_GEOJSON"
    assert detect_file_type("test.pdf") == "DOCUMENT_PDF"
    assert detect_file_type("test.unknown_ext") == "UNKNOWN_BINARY"


def test_manifest_loader():
    manifests = load_all_manifests("data/manifests")
    assert len(manifests) >= 7
    assert "nco.yaml" in manifests
    assert "plfs.yaml" in manifests
    assert "geography.yaml" in manifests


def test_raw_validator_valid_file(validator):
    # Test with one of the downloaded official NCO PDFs
    pdf_path = "data/raw/nco/NCO_2015_Vol_I.pdf"
    if os.path.exists(pdf_path):
        res = validator.validate_file(pdf_path)
        assert res.exists is True
        assert res.extension_allowed is True
        assert res.size_reasonable is True
        assert res.overall_status in (RawValidationStatus.VALIDATED, RawValidationStatus.WARNING)
        assert len(res.violations) == 0


def test_raw_validator_disallowed_extension(validator):
    with tempfile.NamedTemporaryFile(suffix=".exe", delete=False) as tmp:
        tmp.write(b"MOCK_BINARY_DATA")
        tmp_path = tmp.name

    try:
        res = validator.validate_file(tmp_path)
        assert res.extension_allowed is False
        assert res.overall_status == RawValidationStatus.FAILED
        assert any("not permitted" in v for v in res.violations)
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)


def test_raw_validator_empty_file_rejected(validator):
    with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as tmp:
        tmp_path = tmp.name  # 0 bytes

    try:
        res = validator.validate_file(tmp_path)
        assert res.size_reasonable is False
        assert res.overall_status == RawValidationStatus.FAILED
        assert any("0 bytes" in v for v in res.violations)
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)


def test_raw_validator_pii_column_rejected(validator):
    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as tmp:
        tmp.write("state,district,worker_name,aadhaar_no,count\n")
        tmp.write("IN-MH,IN-MH-PUN,Ramesh,123456789012,1\n")
        tmp_path = tmp.name

    try:
        res = validator.validate_file(tmp_path)
        assert res.pii_guard_passed is False
        assert res.overall_status == RawValidationStatus.FAILED
        assert any("PII" in v for v in res.violations)
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)


def test_raw_validator_invalid_json(validator):
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as tmp:
        tmp.write("{ invalid json string")
        tmp_path = tmp.name

    try:
        res = validator.validate_file(tmp_path)
        assert res.schema_valid is False
        assert res.overall_status == RawValidationStatus.FAILED
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)


def test_registration_tool_scan_all():
    summary = scan_and_register_all(raw_dir="data/raw", manifests_dir="data/manifests", registry_output_file=None)
    assert summary.total_files_scanned >= 3
    assert summary.matched_files >= 3
