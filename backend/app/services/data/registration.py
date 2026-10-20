"""
LABREX Raw Dataset Registration Tool
Authority: Master Directive Section 14 & Secondary Ingestion Mandate Step 6
Scope: Safe, entirely local offline registration of raw source files placed in data/raw/.
Safety: Does NOT upload, transmit, or alter source files.
"""

from datetime import datetime, timezone
import fnmatch
import hashlib
import json
import mimetypes
import os
from typing import Any, Dict, List, Optional, Tuple
from pydantic import BaseModel, Field
import yaml


class FileMetadata(BaseModel):
    file_path: str
    filename: str
    file_size_bytes: int
    sha256_hash: str
    detected_type: str
    matched_manifest: Optional[str] = None
    matched_source_id: Optional[str] = None
    matched_target: Optional[str] = None
    missing_metadata: List[str] = Field(default_factory=list)
    is_unexpected: bool = False
    registered_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class RegistrationSummary(BaseModel):
    total_files_scanned: int
    matched_files: int
    unexpected_files: int
    files_with_missing_metadata: int
    records: List[FileMetadata] = Field(default_factory=list)
    unexpected_file_paths: List[str] = Field(default_factory=list)


def compute_sha256(file_path: str) -> str:
    """Computes SHA-256 checksum in 64KB chunks."""
    hasher = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(65536):
            hasher.update(chunk)
    return hasher.hexdigest()


def detect_file_type(file_path: str) -> str:
    """Detects broad file category from extension and content headers."""
    _, ext = os.path.splitext(file_path.lower())
    if ext in {".csv", ".tsv"}:
        return "TABULAR_DELIMITED"
    elif ext in {".xlsx", ".xls"}:
        return "SPREADSHEET_EXCEL"
    elif ext == ".geojson":
        return "GEOSPATIAL_GEOJSON"
    elif ext == ".json":
        return "STRUCTURED_JSON"
    elif ext in {".shp", ".shx", ".dbf", ".prj"}:
        return "GEOSPATIAL_SHAPEFILE"
    elif ext == ".txt":
        return "TEXT_OR_FIXED_WIDTH"
    elif ext == ".pdf":
        return "DOCUMENT_PDF"
    elif ext in {".zip", ".tar", ".gz"}:
        return "ARCHIVE_COMPRESSED"
    
    mime, _ = mimetypes.guess_type(file_path)
    return mime or "UNKNOWN_BINARY"


def load_all_manifests(manifests_dir: str = "data/manifests") -> Dict[str, Dict[str, Any]]:
    """Loads all YAML manifests in the manifests directory."""
    manifests: Dict[str, Dict[str, Any]] = {}
    if not os.path.isdir(manifests_dir):
        return manifests

    for file in os.listdir(manifests_dir):
        if file.endswith((".yaml", ".yml")):
            full_path = os.path.join(manifests_dir, file)
            try:
                with open(full_path, "r", encoding="utf-8") as f:
                    manifests[file] = yaml.safe_load(f) or {}
            except Exception:
                pass
    return manifests


def match_file_to_manifest(
    file_path: str,
    manifests: Dict[str, Dict[str, Any]]
) -> Tuple[Optional[str], Optional[str], Optional[str], List[str]]:
    """
    Matches a given raw file against manifests based on folder and filename pattern.
    Returns: (manifest_filename, source_id, target_key, missing_metadata)
    """
    filename = os.path.basename(file_path)
    source_dir = None
    try:
        rel_path = os.path.relpath(file_path).replace("\\", "/")
        parts = rel_path.split("/")
        source_dir = parts[2] if len(parts) >= 3 and parts[0] == "data" and parts[1] == "raw" else None
    except ValueError:
        # Cross-drive path on Windows (e.g. C: temp file when running on E: project drive)
        norm_path = os.path.abspath(file_path).replace("\\", "/")
        parts = norm_path.split("/")
        if "raw" in parts:
            idx = parts.index("raw")
            if len(parts) > idx + 1:
                source_dir = parts[idx + 1]

    missing: List[str] = []

    for m_filename, m_data in manifests.items():
        source_id = m_data.get("source_id")
        
        # Check folder affiliation
        m_base = os.path.splitext(m_filename)[0].lower()
        if source_dir and m_base != source_dir:
            continue

        # Check acquisition targets if structured
        targets = m_data.get("acquisition_targets", {})
        if isinstance(targets, dict):
            for t_key, t_data in targets.items():
                patterns = t_data.get("filename_patterns", [])
                for pat in patterns:
                    if fnmatch.fnmatch(filename.lower(), pat.lower()):
                        return (m_filename, source_id, t_key, missing)

        # Check PLFS required artifacts
        artifacts = m_data.get("required_artifacts_per_round", {})
        if isinstance(artifacts, dict):
            for a_key, a_data in artifacts.items():
                patterns = a_data.get("filename_patterns", [])
                for pat in patterns:
                    if fnmatch.fnmatch(filename.lower(), pat.lower()):
                        return (m_filename, source_id, a_key, missing)

        # Check file_spec filename_pattern
        f_spec = m_data.get("file_spec", {})
        pattern = f_spec.get("filename_pattern")
        if pattern and fnmatch.fnmatch(filename.lower(), pattern.lower()):
            if "expected_checksum" not in f_spec or not f_spec["expected_checksum"]:
                missing.append("expected_checksum")
            return (m_filename, source_id, "default_file_spec", missing)

        # Fallback loose match by folder
        if source_dir and m_base == source_dir:
            missing.append("filename_pattern_unmatched")
            return (m_filename, source_id, "folder_fallback", missing)

    return (None, None, None, ["no_manifest_matched"])


def register_file(
    file_path: str,
    manifests_dir: str = "data/manifests"
) -> FileMetadata:
    """Processes a single file and extracts registration metadata."""
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    filename = os.path.basename(file_path)
    size = os.path.getsize(file_path)
    sha256 = compute_sha256(file_path)
    file_type = detect_file_type(file_path)

    manifests = load_all_manifests(manifests_dir)
    m_name, s_id, t_key, missing = match_file_to_manifest(file_path, manifests)

    is_unexpected = (m_name is None)

    return FileMetadata(
        file_path=os.path.abspath(file_path),
        filename=filename,
        file_size_bytes=size,
        sha256_hash=sha256,
        detected_type=file_type,
        matched_manifest=m_name,
        matched_source_id=s_id,
        matched_target=t_key,
        missing_metadata=missing,
        is_unexpected=is_unexpected
    )


def scan_and_register_all(
    raw_dir: str = "data/raw",
    manifests_dir: str = "data/manifests",
    registry_output_file: Optional[str] = "data/raw_registry.json"
) -> RegistrationSummary:
    """Scans data/raw/ recursively, registers all files (excluding README and .gitkeep)."""
    manifests = load_all_manifests(manifests_dir)
    records: List[FileMetadata] = []
    unexpected_paths: List[str] = []

    matched_count = 0
    missing_meta_count = 0

    if os.path.isdir(raw_dir):
        for root, _, files in os.walk(raw_dir):
            for file in files:
                if file.lower() in {"readme.md", ".gitkeep", ".ds_store"}:
                    continue
                full_path = os.path.join(root, file)
                rec = register_file(full_path, manifests_dir)
                records.append(rec)
                if rec.is_unexpected:
                    unexpected_paths.append(full_path)
                else:
                    matched_count += 1
                if rec.missing_metadata:
                    missing_meta_count += 1

    summary = RegistrationSummary(
        total_files_scanned=len(records),
        matched_files=matched_count,
        unexpected_files=len(unexpected_paths),
        files_with_missing_metadata=missing_meta_count,
        records=records,
        unexpected_file_paths=unexpected_paths
    )

    if registry_output_file:
        os.makedirs(os.path.dirname(os.path.abspath(registry_output_file)), exist_ok=True)
        with open(registry_output_file, "w", encoding="utf-8") as f:
            f.write(summary.model_dump_json(indent=2))

    return summary
