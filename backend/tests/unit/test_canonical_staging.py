"""
Unit Tests for Canonical Staging Contracts
"""

from datetime import date
import pytest
from pydantic import ValidationError

from backend.app.schemas.staging import (
    CanonicalObservation,
    CanonicalOccupation,
    CanonicalSkillSignal,
    CanonicalTrainingSignal,
    CanonicalWorkforceSignal,
    DatasetType,
    FrequencyType,
    GeographyReference,
    OccupationReference,
    QualityScore,
    SkillReference
)


def test_canonical_observation_creation():
    obs = CanonicalObservation(
        source="SRC-NCS-FEED",
        source_record_id="NCS-PUN-001",
        observation_date=date(2024, 10, 1),
        geography=GeographyReference(state_code="IN-MH", district_code="IN-MH-PUN"),
        occupation=OccupationReference(nco_code="7421.0300", title="Solar PV Technician"),
        metric="active_job_vacancies",
        value=150.0,
        unit="count",
        dataset_version="2024-M10",
        dataset_type=DatasetType.REAL,
        employer_count=12,
        salary_median_inr=28500.0
    )
    assert obs.source == "SRC-NCS-FEED"
    assert obs.value == 150.0
    assert obs.geography.state_code == "IN-MH"
    assert obs.employer_count == 12


def test_canonical_occupation_hierarchy():
    occ = CanonicalOccupation(
        source="SRC-NCO-2015",
        source_record_id="NCO-7421.0300",
        observation_date=date(2015, 1, 1),
        occupation=OccupationReference(
            nco_code="7421.0300",
            title="Solar PV Installation Technician",
            division="7",
            sub_division="74",
            group_code="742",
            family_code="7421"
        ),
        metric="occupational_definition",
        value=1.0,
        unit="taxonomy_entity",
        dataset_version="NCO-2015-v1.0"
    )
    assert occ.occupation.division == "7"
    assert occ.occupation.family_code == "7421"
    assert occ.is_authoritative is True


def test_canonical_training_signal_stream_separation():
    # Training pipeline stream
    pipe_sig = CanonicalTrainingSignal(
        source="SRC-PMKVY-OUT",
        source_record_id="PMKVY-PUN-001",
        observation_date=date(2024, 3, 31),
        metric="candidates_enrolled_pipeline",
        value=350.0,
        unit="count",
        dataset_version="PMKVY-4.0",
        stream_type="TRAINING_PIPELINE",
        enrolled_count=350,
        trained_count=300
    )
    assert pipe_sig.stream_type == "TRAINING_PIPELINE"
    assert pipe_sig.enrolled_count == 350

    # Certified supply stream
    cert_sig = CanonicalTrainingSignal(
        source="SRC-PMKVY-OUT",
        source_record_id="PMKVY-PUN-002",
        observation_date=date(2024, 3, 31),
        metric="candidates_certified_supply",
        value=280.0,
        unit="count",
        dataset_version="PMKVY-4.0",
        stream_type="CERTIFIED_SUPPLY",
        certified_count=280,
        placed_count=220
    )
    assert cert_sig.stream_type == "CERTIFIED_SUPPLY"
    assert cert_sig.certified_count == 280


def test_canonical_workforce_signal():
    wf_sig = CanonicalWorkforceSignal(
        source="SRC-PLFS-ANN",
        source_record_id="PLFS-MH-LFPR",
        observation_date=date(2024, 6, 30),
        geography=GeographyReference(state_code="IN-MH"),
        metric="labour_force_participation_rate",
        value=56.4,
        unit="percentage",
        dataset_version="PLFS-2023-24",
        survey_round="PLFS-2023-24",
        workforce_sector="RURAL+URBAN"
    )
    assert wf_sig.metric == "labour_force_participation_rate"
    assert wf_sig.value == 56.4
    assert wf_sig.unit == "percentage"
