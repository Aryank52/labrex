"""
LABREX Data Quality Engine
Authority: Master Directive Section 13 & 93
Standard: Automated validation, anomaly detection, data health scoring (0-100).
"""

from datetime import date, datetime, timedelta, timezone
from enum import Enum
import re
from typing import Any, Dict, List, Optional, Set
from pydantic import BaseModel, Field

from backend.app.schemas.staging import CanonicalBaseRecord, QualityScore


class QualitySeverity(str, Enum):
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class QualityRule(str, Enum):
    MISSING_DATE = "MISSING_DATE"
    INVALID_GEOGRAPHY = "INVALID_GEOGRAPHY"
    DUPLICATE_RECORD = "DUPLICATE_RECORD"
    NEGATIVE_COUNT = "NEGATIVE_COUNT"
    INVALID_OCCUPATION_CODE = "INVALID_OCCUPATION_CODE"
    INVALID_STATE_DISTRICT_MAPPING = "INVALID_STATE_DISTRICT_MAPPING"
    SCHEMA_DRIFT = "SCHEMA_DRIFT"
    SOURCE_STALENESS = "SOURCE_STALENESS"
    PII_LEAKAGE = "PII_LEAKAGE"


class QualityViolation(BaseModel):
    rule: QualityRule
    severity: QualitySeverity
    record_id: str
    field_name: Optional[str] = None
    message: str
    observed_value: Optional[Any] = None


class QualityReportStatus(str, Enum):
    PASSED = "PASSED"
    WARNING = "WARNING"
    FAILED = "FAILED"


class DataQualityReport(BaseModel):
    dataset_id: str
    batch_id: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    total_records: int
    passed_records: int
    failed_records: int
    overall_quality_score: float = Field(ge=0.0, le=100.0)
    status: QualityReportStatus
    violations: List[QualityViolation] = Field(default_factory=list)
    execution_time_ms: float = 0.0
    summary: Dict[str, Any] = Field(default_factory=dict)


# Authoritative 36 Indian State / UT codes
VALID_INDIAN_STATES = {
    "IN-AN", "IN-AP", "IN-AR", "IN-AS", "IN-BR", "IN-CH", "IN-CT", "IN-DL",
    "IN-DN", "IN-GA", "IN-GJ", "IN-HP", "IN-HR", "IN-JH", "IN-JK", "IN-KA",
    "IN-KL", "IN-LA", "IN-LD", "IN-MH", "IN-ML", "IN-MN", "IN-MP", "IN-MZ",
    "IN-NL", "IN-OD", "IN-PB", "IN-PY", "IN-RJ", "IN-SK", "IN-TG", "IN-TN",
    "IN-TR", "IN-UP", "IN-UT", "IN-WB"
}

NCO_REGEX = re.compile(r"^([0-9]{1,4}|[0-9]{4}\.[0-9]{2,4})$")
PII_INDICATORS = {"aadhaar", "uidai", "mobile", "phone", "password", "bank_account", "ifsc"}


class DataQualityEngine:
    """
    Automated verification engine validating canonical records against
    completeness, consistency, validity, freshness, and privacy invariants.
    """

    def __init__(
        self,
        max_staleness_days: int = 730,  # 2 years for periodic census/survey baselines
        known_valid_states: Optional[Set[str]] = None
    ):
        self.max_staleness_days = max_staleness_days
        self.valid_states = known_valid_states or VALID_INDIAN_STATES

    def validate_record(
        self,
        record: CanonicalBaseRecord,
        seen_record_ids: Set[str]
    ) -> List[QualityViolation]:
        """Runs individual record-level quality assertions."""
        violations: List[QualityViolation] = []
        rec_id = record.source_record_id

        # 1. Duplicate Check
        if rec_id in seen_record_ids:
            violations.append(QualityViolation(
                rule=QualityRule.DUPLICATE_RECORD,
                severity=QualitySeverity.ERROR,
                record_id=rec_id,
                message=f"Duplicate natural key detected: {rec_id}"
            ))
        seen_record_ids.add(rec_id)

        # 2. Date Validation
        if not record.observation_date:
            violations.append(QualityViolation(
                rule=QualityRule.MISSING_DATE,
                severity=QualitySeverity.CRITICAL,
                record_id=rec_id,
                field_name="observation_date",
                message="Observation date is null or unparseable"
            ))
        else:
            if record.observation_date.year < 1990 or record.observation_date.year > 2035:
                violations.append(QualityViolation(
                    rule=QualityRule.MISSING_DATE,
                    severity=QualitySeverity.ERROR,
                    record_id=rec_id,
                    field_name="observation_date",
                    observed_value=str(record.observation_date),
                    message=f"Observation date {record.observation_date} is outside reasonable bounds (1990-2035)"
                ))

            # Freshness check
            age = (date.today() - record.observation_date).days
            if age > self.max_staleness_days:
                violations.append(QualityViolation(
                    rule=QualityRule.SOURCE_STALENESS,
                    severity=QualitySeverity.WARNING,
                    record_id=rec_id,
                    field_name="observation_date",
                    observed_value=age,
                    message=f"Data is stale: age {age} days exceeds threshold {self.max_staleness_days} days"
                ))

        # 3. Geography & State-District Mapping
        st_code = record.geography.state_code
        dt_code = record.geography.district_code

        if st_code:
            st_norm = st_code.upper()
            if st_norm not in self.valid_states:
                violations.append(QualityViolation(
                    rule=QualityRule.INVALID_GEOGRAPHY,
                    severity=QualitySeverity.ERROR,
                    record_id=rec_id,
                    field_name="geography.state_code",
                    observed_value=st_code,
                    message=f"Unrecognized Indian State/UT code: {st_code}"
                ))

        if dt_code and st_code:
            # Check state-district parent link
            if dt_code.startswith("IN-"):
                dt_prefix = "-".join(dt_code.split("-")[:2])
                if dt_prefix != st_code.upper():
                    violations.append(QualityViolation(
                        rule=QualityRule.INVALID_STATE_DISTRICT_MAPPING,
                        severity=QualitySeverity.ERROR,
                        record_id=rec_id,
                        field_name="geography.district_code",
                        observed_value=f"district={dt_code}, state={st_code}",
                        message=f"District prefix '{dt_prefix}' does not match parent state '{st_code}'"
                    ))

        # 4. Negative Counts Check
        count_units = {"count", "number", "vacancies", "candidates", "seats"}
        if record.unit.lower() in count_units and record.value < 0:
            violations.append(QualityViolation(
                rule=QualityRule.NEGATIVE_COUNT,
                severity=QualitySeverity.CRITICAL,
                record_id=rec_id,
                field_name="value",
                observed_value=record.value,
                message=f"Count metric '{record.metric}' cannot be negative: {record.value}"
            ))

        # 5. Occupation Code Check (if provided)
        nco = record.occupation.nco_code
        if nco:
            if not NCO_REGEX.match(nco.strip()):
                violations.append(QualityViolation(
                    rule=QualityRule.INVALID_OCCUPATION_CODE,
                    severity=QualitySeverity.WARNING,
                    record_id=rec_id,
                    field_name="occupation.nco_code",
                    observed_value=nco,
                    message=f"NCO code '{nco}' does not conform to NCO-2015 format"
                ))

        # 6. PII Leakage Check
        for attr_name in dir(record):
            if any(pii in attr_name.lower() for pii in PII_INDICATORS):
                violations.append(QualityViolation(
                    rule=QualityRule.PII_LEAKAGE,
                    severity=QualitySeverity.CRITICAL,
                    record_id=rec_id,
                    field_name=attr_name,
                    message=f"Potential PII field detected in canonical record: {attr_name}"
                ))

        return violations

    def evaluate_batch(
        self,
        dataset_id: str,
        batch_id: str,
        records: List[CanonicalBaseRecord]
    ) -> DataQualityReport:
        """Evaluates an entire batch of canonical records and generates DataQualityReport."""
        import time
        start_time = time.perf_counter()

        all_violations: List[QualityViolation] = []
        seen_ids: Set[str] = set()
        failed_count = 0

        # Penalty weights
        penalty_map = {
            QualitySeverity.CRITICAL: 20.0,
            QualitySeverity.ERROR: 5.0,
            QualitySeverity.WARNING: 1.0,
            QualitySeverity.INFO: 0.0
        }

        total_penalty = 0.0

        for rec in records:
            rec_violations = self.validate_record(rec, seen_ids)
            if rec_violations:
                all_violations.extend(rec_violations)
                # Assign to record quality object
                has_critical_or_error = any(v.severity in {QualitySeverity.CRITICAL, QualitySeverity.ERROR} for v in rec_violations)
                if has_critical_or_error:
                    failed_count += 1
                rec_penalty = sum(penalty_map.get(v.severity, 0.0) for v in rec_violations)
                rec.quality.score = max(0.0, 100.0 - rec_penalty)
                rec.quality.confidence = max(0.0, 1.0 - (rec_penalty / 100.0))
                rec.quality.flags = [f"{v.rule.value}:{v.message}" for v in rec_violations]
                total_penalty += rec_penalty
            else:
                rec.quality.score = 100.0
                rec.quality.confidence = 1.0
                rec.quality.flags = []

        total_records = len(records)
        passed_records = total_records - failed_count

        # Overall batch score
        if total_records > 0:
            avg_penalty = total_penalty / total_records
            overall_score = max(0.0, min(100.0, 100.0 - avg_penalty))
        else:
            overall_score = 0.0

        if overall_score >= 85.0 and failed_count == 0:
            status = QualityReportStatus.PASSED
        elif overall_score >= 70.0:
            status = QualityReportStatus.WARNING
        else:
            status = QualityReportStatus.FAILED

        elapsed_ms = (time.perf_counter() - start_time) * 1000.0

        return DataQualityReport(
            dataset_id=dataset_id,
            batch_id=batch_id,
            timestamp=datetime.now(timezone.utc),
            total_records=total_records,
            passed_records=passed_records,
            failed_records=failed_count,
            overall_quality_score=round(overall_score, 2),
            status=status,
            violations=all_violations,
            execution_time_ms=round(elapsed_ms, 2),
            summary={
                "violation_count": len(all_violations),
                "critical_violations": sum(1 for v in all_violations if v.severity == QualitySeverity.CRITICAL),
                "error_violations": sum(1 for v in all_violations if v.severity == QualitySeverity.ERROR),
                "warning_violations": sum(1 for v in all_violations if v.severity == QualitySeverity.WARNING)
            }
        )
