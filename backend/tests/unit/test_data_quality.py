"""
Unit Tests for Data Quality Framework
Authority: Master Directive Section 13 & 93
"""

from datetime import date, timedelta
import pytest

from backend.app.schemas.staging import (
    CanonicalObservation,
    DatasetType,
    GeographyReference,
    OccupationReference,
    QualityScore,
    SkillReference
)
from backend.app.services.data.quality.data_quality_engine import (
    DataQualityEngine,
    QualityReportStatus,
    QualityRule,
    QualitySeverity
)


@pytest.fixture
def quality_engine():
    return DataQualityEngine(max_staleness_days=1500)


def create_sample_record(
    rec_id: str = "REC-001",
    obs_date: date = date(2025, 6, 1),
    state_code: str = "IN-MH",
    district_code: str = "IN-MH-PUN",
    nco_code: str = "7421.0300",
    value: float = 100.0,
    unit: str = "count"
) -> CanonicalObservation:
    return CanonicalObservation(
        source="SRC-TEST",
        source_record_id=rec_id,
        observation_date=obs_date,
        geography=GeographyReference(state_code=state_code, district_code=district_code),
        occupation=OccupationReference(nco_code=nco_code, title="Test Role"),
        skill=SkillReference(),
        metric="active_vacancies",
        value=value,
        unit=unit,
        dataset_version="TEST-v1",
        dataset_type=DatasetType.FIXTURE
    )


def test_clean_record_passes_quality_check(quality_engine):
    rec = create_sample_record()
    seen = set()
    violations = quality_engine.validate_record(rec, seen)
    assert len(violations) == 0


def test_duplicate_record_detection(quality_engine):
    rec1 = create_sample_record(rec_id="DUP-001")
    rec2 = create_sample_record(rec_id="DUP-001")
    seen = set()

    v1 = quality_engine.validate_record(rec1, seen)
    assert len(v1) == 0

    v2 = quality_engine.validate_record(rec2, seen)
    assert len(v2) == 1
    assert v2[0].rule == QualityRule.DUPLICATE_RECORD
    assert v2[0].severity == QualitySeverity.ERROR


def test_negative_count_rejected(quality_engine):
    rec = create_sample_record(value=-50.0, unit="count")
    seen = set()
    violations = quality_engine.validate_record(rec, seen)
    negative_rules = [v for v in violations if v.rule == QualityRule.NEGATIVE_COUNT]
    assert len(negative_rules) == 1
    assert negative_rules[0].severity == QualitySeverity.CRITICAL


def test_invalid_state_code(quality_engine):
    rec = create_sample_record(state_code="IN-XX")
    seen = set()
    violations = quality_engine.validate_record(rec, seen)
    geo_rules = [v for v in violations if v.rule == QualityRule.INVALID_GEOGRAPHY]
    assert len(geo_rules) == 1
    assert "Unrecognized Indian State" in geo_rules[0].message


def test_invalid_state_district_mismatch(quality_engine):
    # District prefix IN-KA does not match state IN-MH
    rec = create_sample_record(state_code="IN-MH", district_code="IN-KA-BLU")
    seen = set()
    violations = quality_engine.validate_record(rec, seen)
    mismatch_rules = [v for v in violations if v.rule == QualityRule.INVALID_STATE_DISTRICT_MAPPING]
    assert len(mismatch_rules) == 1


def test_invalid_nco_code_format(quality_engine):
    rec = create_sample_record(nco_code="INVALID_CODE_XYZ")
    seen = set()
    violations = quality_engine.validate_record(rec, seen)
    nco_rules = [v for v in violations if v.rule == QualityRule.INVALID_OCCUPATION_CODE]
    assert len(nco_rules) == 1
    assert nco_rules[0].severity == QualitySeverity.WARNING


def test_batch_evaluation_and_scoring(quality_engine):
    # Batch with 1 clean and 1 with negative count
    clean_rec = create_sample_record(rec_id="B-001")
    bad_rec = create_sample_record(rec_id="B-002", value=-25.0, unit="count")

    report = quality_engine.evaluate_batch(
        dataset_id="SRC-TEST-BATCH",
        batch_id="BAT-001",
        records=[clean_rec, bad_rec]
    )

    assert report.total_records == 2
    assert report.passed_records == 1
    assert report.failed_records == 1
    assert report.overall_quality_score < 100.0
    assert report.status in (QualityReportStatus.WARNING, QualityReportStatus.FAILED)
    assert report.summary["critical_violations"] == 1
