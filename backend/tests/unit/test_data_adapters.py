"""
Unit Tests for LABREX Data Parsers & Adapters
Authority: Master Directive Section 14 & Secondary Mandate Steps 4-10
"""

import json
import os
import pytest

from backend.app.services.data.adapters.eshram_adapter import (
    EShramAdapter,
    PIISafetyViolationError
)
from backend.app.services.data.adapters.ncs_adapter import (
    ConnectionState,
    NCSAdapter
)
from backend.app.services.data.adapters.nsdc_adapter import NSDCAdapter
from backend.app.services.data.adapters.plfs_adapter import PLFSAdapter
from backend.app.services.data.adapters.pmkvy_adapter import PMKVYAdapter
from backend.app.services.data.parsers.geography_parser import GeographyParser
from backend.app.services.data.parsers.nco_parser import NCOParser

FIXTURES_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../data/fixtures"))


def test_nco_parser_hierarchy_and_fixture():
    parser = NCOParser(source_version="NCO-2015-FIXTURE")
    fixture_path = os.path.join(FIXTURES_DIR, "nco_fixture.json")
    with open(fixture_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    records = parser.parse_json(data)
    assert len(records) == 5

    # Check Solar PV technician
    solar_rec = next(r for r in records if r.occupation.nco_code == "7421.0300")
    assert solar_rec.occupation.division == "7"
    assert solar_rec.occupation.sub_division == "74"
    assert solar_rec.occupation.group_code == "742"
    assert solar_rec.occupation.family_code == "7421"
    assert solar_rec.occupation.sector_id == "SEC-RENEWABLE-ENERGY"
    assert solar_rec.is_authoritative is True


def test_plfs_adapter_minimal_indicators():
    adapter = PLFSAdapter(source_version="PLFS-2023-24-FIXTURE")
    fixture_path = os.path.join(FIXTURES_DIR, "plfs_fixture.json")
    with open(fixture_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    signals = []
    for row in data:
        signals.extend(adapter.parse_record(row))

    # Should contain LFPR, WPR, UR, plus 3 industry share metrics per state
    assert len(signals) > 10

    mh_lfpr = next(s for s in signals if s.geography.state_code == "IN-MH" and s.metric == "labour_force_participation_rate")
    assert mh_lfpr.value == 56.4
    assert mh_lfpr.unit == "percentage"

    ka_ur = next(s for s in signals if s.geography.state_code == "IN-KA" and s.metric == "unemployment_rate")
    assert ka_ur.value == 2.8


def test_eshram_adapter_clean_aggregates():
    adapter = EShramAdapter(source_version="ESHRAM-AGG-FIXTURE")
    fixture_path = os.path.join(FIXTURES_DIR, "eshram_fixture.json")
    with open(fixture_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    signals = adapter.parse_json(data)
    assert len(signals) == 4

    pune_auto = next(s for s in signals if s.geography.district_code == "IN-MH-PUN" and "Automotive" in s.workforce_sector)
    assert pune_auto.worker_count == 84250
    assert pune_auto.male_ratio == 0.78
    assert pune_auto.female_ratio == 0.22


def test_eshram_adapter_pii_guard_violation():
    adapter = EShramAdapter()
    polluted_record = {
        "snapshot_date": "2024-09-30",
        "state_code": "IN-MH",
        "district_code": "IN-MH-PUN",
        "worker_name": "Ramesh Kumar",  # FORBIDDEN PII
        "aadhaar_no": "XXXX-XXXX-1234",  # FORBIDDEN PII
        "worker_count": 1
    }
    with pytest.raises(PIISafetyViolationError) as exc_info:
        adapter.parse_record(polluted_record)
    assert "CRITICAL SECURITY GUARD" in str(exc_info.value)


def test_pmkvy_adapter_stream_separation():
    adapter = PMKVYAdapter(source_version="PMKVY-4.0-FIXTURE")
    fixture_path = os.path.join(FIXTURES_DIR, "pmkvy_fixture.json")
    with open(fixture_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    all_signals = []
    for row in data:
        all_signals.extend(adapter.parse_record(row))

    # Must contain separated streams
    pipeline_signals = [s for s in all_signals if s.stream_type == "TRAINING_PIPELINE"]
    certified_signals = [s for s in all_signals if s.stream_type == "CERTIFIED_SUPPLY"]
    capacity_signals = [s for s in all_signals if s.stream_type == "INFRASTRUCTURE_CAPACITY"]

    assert len(pipeline_signals) > 0
    assert len(certified_signals) > 0
    assert len(capacity_signals) > 0

    solar_cert = next(s for s in certified_signals if s.skill.qualification_id == "QP-SGJ-Q0101")
    assert solar_cert.certified_count == 395
    assert solar_cert.placed_count == 310


def test_nsdc_adapter_directory_parsing():
    adapter = NSDCAdapter(source_version="NSDC-DIR-FIXTURE")
    sample_centre = {
        "center_id": "TC-MH-042",
        "center_name": "Pune Advanced Solar Skill Academy",
        "state_code": "IN-MH",
        "district_code": "IN-MH-PUN",
        "pincode": "411001",
        "qualification_id": "QP-SGJ-Q0101",
        "course_name": "Solar PV Installation",
        "nsqf_level": 4,
        "sanctioned_seats": 120,
        "scheme": "PMKVY 4.0"
    }
    signal = adapter.parse_record(sample_centre)
    assert signal.center_id == "TC-MH-042"
    assert signal.sanctioned_seats == 120
    assert signal.skill.nsqf_level == 4
    assert signal.geography.pincode == "411001"


def test_ncs_adapter_connection_states():
    # 1. Unconfigured default state
    adapter_unconfigured = NCSAdapter(api_endpoint=None, api_key=None)
    assert adapter_unconfigured.connection_state == ConnectionState.NOT_CONFIGURED
    state, res = adapter_unconfigured.fetch_live_vacancies()
    assert state == ConnectionState.NOT_CONFIGURED
    assert len(res) == 0

    # 2. Configured state
    adapter_configured = NCSAdapter(api_endpoint="https://api.ncs.gov.in/vacancies", api_key="mock")
    assert adapter_configured.connection_state == ConnectionState.AVAILABLE

    # 3. State transitions
    adapter_configured.set_connection_state(ConnectionState.RATE_LIMITED)
    assert adapter_configured.connection_state == ConnectionState.RATE_LIMITED

    adapter_configured.set_connection_state(ConnectionState.UNAVAILABLE)
    assert adapter_configured.connection_state == ConnectionState.UNAVAILABLE


def test_geography_parser_and_validation():
    parser = GeographyParser(srid=4326)
    fixture_path = os.path.join(FIXTURES_DIR, "geography_fixture.geojson")
    with open(fixture_path, "r", encoding="utf-8") as f:
        geo_data = json.load(f)

    state_features = [feat for feat in geo_data["features"] if "state_code" in feat["properties"] and "district_code" not in feat["properties"]]
    district_features = [feat for feat in geo_data["features"] if "district_code" in feat["properties"]]

    # Validate States
    state_results = [parser.parse_state_feature(feat) for feat in state_features]
    assert len(state_results) == 2
    for s_res in state_results:
        assert s_res.is_valid is True
        assert s_res.geometry_valid is True
        assert s_res.bounding_box_valid is True
        assert s_res.srid_valid is True
        assert len(s_res.violations) == 0

    known_states = {s_res.code for s_res in state_results}

    # Validate Districts
    district_results = [parser.parse_district_feature(feat, known_states) for feat in district_features]
    assert len(district_results) == 2
    for d_res in district_results:
        assert d_res.is_valid is True
        assert d_res.geometry_valid is True
        assert d_res.bounding_box_valid is True
        assert d_res.parent_state_code in known_states
        assert len(d_res.violations) == 0
