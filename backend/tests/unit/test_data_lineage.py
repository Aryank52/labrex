"""
Unit Tests for Data Lineage & Provenance Tracker
Authority: Master Directive Section 13, 47 & 79
"""

import os
import tempfile
import pytest

from backend.app.services.data.lineage.provenance import (
    compute_file_sha256,
    compute_record_hash,
    create_batch_lineage,
    generate_lineage_signature
)


def test_record_hash_deterministic():
    payload1 = {"source": "NCO", "code": "7421.0300", "title": "Solar PV"}
    payload2 = {"title": "Solar PV", "code": "7421.0300", "source": "NCO"}  # Different key order

    hash1 = compute_record_hash(payload1)
    hash2 = compute_record_hash(payload2)

    assert hash1 == hash2
    assert len(hash1) == 64


def test_file_sha256_computation():
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt") as tmp:
        tmp.write("LABREX_LINEAGE_TEST_CONTENT")
        tmp_path = tmp.name

    try:
        digest = compute_file_sha256(tmp_path)
        assert len(digest) == 64
        # Verify idempotency
        assert digest == compute_file_sha256(tmp_path)
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)


def test_create_batch_lineage():
    lineage = create_batch_lineage(
        source_id="SRC-NCO-2015",
        dataset_name="NCO 2015",
        dataset_version="v1.0",
        parser_name="NCOParser",
        batch_id="BAT-001"
    )

    assert lineage.source_id == "SRC-NCO-2015"
    assert lineage.batch_id == "BAT-001"
    assert lineage.parser_name == "NCOParser"
    assert len(lineage.lineage_signature) == 64
