#!/usr/bin/env python3
"""
LABREX Raw Dataset Pre-Ingestion Validator CLI
Usage:
    python -m labrex.data.validate_raw
    python -m labrex.data.validate_raw --file <path_to_file>
    python -m labrex.data.validate_raw --source <source_subfolder>
"""

import argparse
import json
import os
import sys

from backend.app.services.data.raw_validator import (
    RawDataValidator,
    RawValidationStatus
)


def main() -> int:
    parser = argparse.ArgumentParser(description="LABREX Raw Dataset Pre-Ingestion Validator")
    parser.add_argument("--file", default=None, help="Validate a specific file in data/raw/")
    parser.add_argument("--source", default=None, help="Filter validation to specific source directory (e.g. nco, plfs)")
    parser.add_argument("--raw-dir", default="data/raw", help="Directory of raw datasets")
    parser.add_argument("--manifests-dir", default="data/manifests", help="Directory of manifests")
    parser.add_argument("--json", action="store_true", help="Output machine-readable JSON report")

    args = parser.parse_args()

    validator = RawDataValidator(manifests_dir=args.manifests_dir)

    target_dir = args.raw_dir
    if args.source:
        target_dir = os.path.join(args.raw_dir, args.source)
        if not os.path.isdir(target_dir):
            print(f"Error: Source directory not found: {target_dir}", file=sys.stderr)
            return 1

    if args.file:
        res = validator.validate_file(args.file)
        if args.json:
            print(res.model_dump_json(indent=2))
        else:
            print("============================================================")
            print("LABREX RAW FILE VALIDATION RESULT")
            print("============================================================")
            print(f"File:         {res.filename}")
            print(f"Status:       {res.overall_status.value}")
            print(f"Size:         {res.size_bytes} bytes (Reasonable: {res.size_reasonable})")
            print(f"Extension:    Permitted: {res.extension_allowed}")
            print(f"Manifest:     {res.matched_manifest or 'NO_MATCH'}")
            print(f"PII Guard:    Passed: {res.pii_guard_passed}")
            print(f"Schema Check: Valid: {res.schema_valid}")
            if res.hash_verified is not None:
                print(f"Hash Check:   Verified: {res.hash_verified}")
            if res.violations:
                print("\n[!] VIOLATIONS:")
                for v in res.violations:
                    print(f"    - {v}")
            if res.warnings:
                print("\n[*] WARNINGS:")
                for w in res.warnings:
                    print(f"    - {w}")
            print("============================================================")
        return 0 if res.overall_status != RawValidationStatus.FAILED else 1

    # Batch validation across raw_dir
    report = validator.validate_raw_directory(raw_dir=target_dir)

    if args.json:
        print(report.model_dump_json(indent=2))
    else:
        print("============================================================")
        print("LABREX RAW DATASET VALIDATION REPORT")
        print("============================================================")
        print(f"Total files inspected: {report.total_files_inspected}")
        print(f"Passed validation:     {report.passed_count}")
        print(f"Warnings:              {report.warning_count}")
        print(f"Failed validation:     {report.failed_count}")
        print("------------------------------------------------------------")
        if report.total_files_inspected == 0:
            print("Status: AWAITING_DOWNLOAD (No raw source data files staged yet).")
            print("Staging directories and manifests are prepared and ready.")
        else:
            for r in report.results:
                badge = f"[{r.overall_status.value}]"
                print(f"{badge:<12} {r.filename} ({r.size_bytes} bytes)")
                if r.violations:
                    for v in r.violations:
                        print(f"    [VIOLATION] {v}")
                if r.warnings:
                    for w in r.warnings:
                        print(f"    [WARNING]   {w}")
        print("============================================================")

    return 0 if report.failed_count == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
