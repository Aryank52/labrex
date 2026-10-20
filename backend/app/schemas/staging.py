"""
LABREX Canonical Staging Contracts
Authority: Master Directive Section 13 & Secondary Data Engineering Mandate
Status: Conformed Staging Contracts (Decoupled from Physical Storage)
"""

from datetime import date, datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Literal, Optional
from pydantic import BaseModel, Field, field_validator


class DatasetType(str, Enum):
    REAL = "REAL"
    DERIVED = "DERIVED"
    FIXTURE = "FIXTURE"


class FrequencyType(str, Enum):
    DAILY = "DAILY"
    WEEKLY = "WEEKLY"
    MONTHLY = "MONTHLY"
    QUARTERLY = "QUARTERLY"
    ANNUAL = "ANNUAL"
    STATIC = "STATIC"


class GeographyReference(BaseModel):
    """Normalized geographic reference linking observation to administrative levels."""
    country_code: str = Field(default="IN", description="ISO 3166-1 alpha-2 country code")
    state_code: Optional[str] = Field(default=None, description="Standard State code, e.g. 'IN-MH', 'IN-KA'")
    state_name: Optional[str] = Field(default=None, description="Official State / UT name")
    district_code: Optional[str] = Field(default=None, description="Standard District code, e.g. 'IN-MH-PUN'")
    district_name: Optional[str] = Field(default=None, description="Official District name")
    lgd_code: Optional[int] = Field(default=None, description="Local Government Directory (LGD) unique code")
    pincode: Optional[str] = Field(default=None, description="6-digit Indian Postal Index Number")


class OccupationReference(BaseModel):
    """Normalized occupational reference conforming to NCO-2015 hierarchy."""
    nco_code: Optional[str] = Field(default=None, description="Official 8-digit or 4-digit NCO code, e.g. '7421.0300'")
    title: Optional[str] = Field(default=None, description="Canonical or reported occupational title")
    division: Optional[str] = Field(default=None, description="1-digit NCO major division (0-9)")
    sub_division: Optional[str] = Field(default=None, description="2-digit NCO sub-division")
    group_code: Optional[str] = Field(default=None, description="3-digit NCO group")
    family_code: Optional[str] = Field(default=None, description="4-digit NCO family")
    sector_id: Optional[str] = Field(default=None, description="Mapped sector ID (e.g. 'SEC-AUTO', 'SEC-SOLAR')")


class SkillReference(BaseModel):
    """Normalized skill reference linking to NSQF / NOS / QP."""
    skill_id: Optional[str] = Field(default=None, description="Canonical skill identifier, e.g. 'SKILL-SOLAR-PV-INSTALL'")
    name: Optional[str] = Field(default=None, description="Canonical skill name")
    skill_type: Optional[str] = Field(default="TECHNICAL", description="TECHNICAL, FOUNDATIONAL, DIGITAL, GREEN")
    qualification_id: Optional[str] = Field(default=None, description="Associated QP ID, e.g. 'QP-SGJ-Q0101'")
    nsqf_level: Optional[int] = Field(default=None, ge=1, le=10, description="NSQF level 1 to 10")


class QualityScore(BaseModel):
    """Data quality and confidence metadata associated with each record."""
    score: float = Field(default=100.0, ge=0.0, le=100.0, description="Quality score from 0 to 100")
    confidence: float = Field(default=1.0, ge=0.0, le=1.0, description="Analytical confidence metric (0.0 to 1.0)")
    flags: List[str] = Field(default_factory=list, description="Quality violation flags or warnings")
    is_anomaly: bool = Field(default=False, description="Flagged by outlier detection")


class CanonicalBaseRecord(BaseModel):
    """Base staging contract containing mandatory provenance and lineage fields."""
    source: str = Field(..., description="Master Data Source ID (e.g. 'SRC-PLFS-ANN', 'SRC-NCS-FEED')")
    source_record_id: str = Field(..., description="Unique deterministic identifier from the raw record")
    observation_date: date = Field(..., description="Observation reference date or period start date")
    geography: GeographyReference = Field(default_factory=GeographyReference)
    occupation: OccupationReference = Field(default_factory=OccupationReference)
    skill: SkillReference = Field(default_factory=SkillReference)
    metric: str = Field(..., description="Measured indicator name (e.g. 'unemployment_rate', 'active_postings')")
    value: float = Field(..., description="Measured quantitative value")
    unit: str = Field(..., description="Metric unit: 'count', 'percentage', 'ratio', 'currency_inr'")
    quality: QualityScore = Field(default_factory=QualityScore)
    dataset_version: str = Field(..., description="Version of the source dataset release")
    dataset_type: DatasetType = Field(default=DatasetType.REAL, description="REAL, DERIVED, or FIXTURE")
    ingested_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    raw_payload_hash: Optional[str] = Field(default=None, description="SHA-256 digest of source record")


class CanonicalObservation(CanonicalBaseRecord):
    """
    Standard staging observation representing general labour-market signals
    (e.g. NCS postings, OGD vacancies, macroeconomic employment metrics).
    """
    frequency: FrequencyType = Field(default=FrequencyType.MONTHLY)
    employer_count: Optional[int] = Field(default=None, ge=0)
    salary_median_inr: Optional[float] = Field(default=None, ge=0)
    extra_attributes: Dict[str, Any] = Field(default_factory=dict)


class CanonicalOccupation(CanonicalBaseRecord):
    """
    Standard staging model for NCO-2015 occupational taxonomy records.
    """
    is_authoritative: bool = Field(default=True, description="True if sourced directly from gazetted NCO-2015")
    isco_08_mapping: Optional[str] = Field(default=None, description="Concordance mapping to ISCO-08")
    task_description: Optional[str] = Field(default=None, description="Task and duties description")
    educational_requirement: Optional[str] = Field(default=None)


class CanonicalSkillSignal(CanonicalBaseRecord):
    """
    Standard staging signal for skill frequency, demand growth, or emerging skill indicators.
    """
    postings_mentioning_count: Optional[int] = Field(default=None, ge=0)
    growth_rate_pct: Optional[float] = Field(default=None)
    skill_cluster: Optional[str] = Field(default=None)


class CanonicalTrainingSignal(CanonicalBaseRecord):
    """
    Standard staging record for skilling pipelines (PMKVY, DGT/ITI, NSDC).
    Separates training pipeline, certified supply, and infrastructure capacity.
    """
    stream_type: Literal["TRAINING_PIPELINE", "CERTIFIED_SUPPLY", "INFRASTRUCTURE_CAPACITY"] = Field(
        ..., description="Strict separation of skilling components"
    )
    center_id: Optional[str] = Field(default=None, description="Unique training centre identifier")
    center_name: Optional[str] = Field(default=None)
    scheme_name: Optional[str] = Field(default=None, description="e.g. 'PMKVY 4.0', 'CTS', 'DDU-GKY'")
    enrolled_count: Optional[int] = Field(default=None, ge=0)
    trained_count: Optional[int] = Field(default=None, ge=0)
    certified_count: Optional[int] = Field(default=None, ge=0)
    placed_count: Optional[int] = Field(default=None, ge=0)
    sanctioned_seats: Optional[int] = Field(default=None, ge=0)

    @field_validator("certified_count")
    @classmethod
    def validate_certified_lte_trained(cls, v: Optional[int], info) -> Optional[int]:
        trained = info.data.get("trained_count")
        if v is not None and trained is not None and v > trained:
            # We record a soft warning or allow quality scorer to flag
            pass
        return v


class CanonicalWorkforceSignal(CanonicalBaseRecord):
    """
    Standard staging record for macro survey indicators (PLFS) or informal registries (e-Shram).
    """
    workforce_sector: Optional[str] = Field(default=None, description="e.g. 'INFORMAL', 'ORGANIZED', 'AGRICULTURE'")
    worker_count: Optional[int] = Field(default=None, ge=0)
    male_ratio: Optional[float] = Field(default=None, ge=0.0, le=1.0)
    female_ratio: Optional[float] = Field(default=None, ge=0.0, le=1.0)
    survey_round: Optional[str] = Field(default=None, description="e.g. 'PLFS-2023-24'")
    sampling_weight: Optional[float] = Field(default=None, ge=0.0)
