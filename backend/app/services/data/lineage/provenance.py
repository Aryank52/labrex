"""
LABREX Data Lineage & Provenance Tracker
Authority: Master Directive Section 13, 47 & 79
Standard: Append-only auditability, deterministic reproducibility, cryptographic traceability.
"""

from datetime import datetime, timezone
import hashlib
import json
import os
from typing import Any, Dict, Optional
from pydantic import BaseModel, Field


class IngestionLineage(BaseModel):
    """Lineage metadata packet attached to an ingestion run or canonical record."""
    source_id: str = Field(..., description="Unique source identifier from Registry")
    dataset_name: str = Field(..., description="Official dataset name")
    dataset_version: str = Field(..., description="Version release identifier")
    parser_name: str = Field(..., description="Python parser/adapter class")
    parser_version: str = Field(default="1.0.0")
    retrieved_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    file_path: Optional[str] = Field(default=None)
    file_sha256: Optional[str] = Field(default=None)
    batch_id: str = Field(...)
    lineage_signature: str = Field(...)


def compute_file_sha256(file_path: str) -> str:
    """Computes SHA-256 hex digest of a local file in streaming blocks."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Source file not found for checksumming: {file_path}")
    hasher = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(65536):
            hasher.update(chunk)
    return hasher.hexdigest()


def compute_record_hash(record_data: Dict[str, Any]) -> str:
    """Computes deterministic SHA-256 hash of a dictionary payload."""
    serialized = json.dumps(record_data, sort_keys=True, default=str).encode("utf-8")
    return hashlib.sha256(serialized).hexdigest()


def generate_lineage_signature(
    source_id: str,
    dataset_version: str,
    batch_id: str,
    file_sha256: Optional[str] = None
) -> str:
    """Generates an immutable signature for a batch lineage run."""
    raw = f"{source_id}::{dataset_version}::{batch_id}::{file_sha256 or 'IN_MEMORY'}"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def create_batch_lineage(
    source_id: str,
    dataset_name: str,
    dataset_version: str,
    parser_name: str,
    batch_id: str,
    file_path: Optional[str] = None,
    parser_version: str = "1.0.0"
) -> IngestionLineage:
    """Factory creating complete IngestionLineage object."""
    sha256 = compute_file_sha256(file_path) if file_path and os.path.exists(file_path) else None
    signature = generate_lineage_signature(source_id, dataset_version, batch_id, sha256)
    return IngestionLineage(
        source_id=source_id,
        dataset_name=dataset_name,
        dataset_version=dataset_version,
        parser_name=parser_name,
        parser_version=parser_version,
        retrieved_at=datetime.now(timezone.utc),
        file_path=file_path,
        file_sha256=sha256,
        batch_id=batch_id,
        lineage_signature=signature
    )
