#!/usr/bin/env python3
"""
LABREX File Registration CLI
Usage:
    python -m labrex.data.register_file <path_to_file>
    python -m labrex.data.register_file --scan-all
"""

import argparse
import json
import os
import sys

from backend.app.services.data.registration import (
    register_file,
    scan_and_register_all
)


def main() -> int:
    parser = argparse.ArgumentParser(description="LABREX Raw Dataset Registration Tool")
    parser.add_argument("file", nargs="?", default=None, help="Path to raw file to register")
    parser.add_argument("--scan-all", action="store_true", help="Scan and register all files in data/raw/")
    parser.add_argument("--raw-dir", default="data/raw", help="Directory of raw datasets")
    parser.add_argument("--manifests-dir", default="data/manifests", help="Directory of manifests")
    parser.add_argument("--json", action="store_true", help="Output raw JSON summary")

    args = parser.parse_args()

    if args.scan_all or (not args.file and os.path.isdir(args.raw_dir)):
        summary = scan_and_register_all(raw_dir=args.raw_dir, manifests_dir=args.manifests_dir)
        if args.json:
            print(summary.model_dump_json(indent=2))
        else:
            print("============================================================")
            print("LABREX RAW DATASET REGISTRATION SUMMARY")
            print("============================================================")
            print(f"Total files scanned:         {summary.total_files_scanned}")
            print(f"Manifest matched files:      {summary.matched_files}")
            print(f"Unexpected files:            {summary.unexpected_files}")
            print(f"Files with missing metadata: {summary.files_with_missing_metadata}")
            print("------------------------------------------------------------")
            for r in summary.records:
                status = "MATCHED" if not r.is_unexpected else "UNEXPECTED"
                print(f"[{status}] {r.filename} ({r.file_size_bytes} bytes)")
                print(f"    SHA-256: {r.sha256_hash}")
                print(f"    Type:    {r.detected_type}")
                if r.matched_manifest:
                    print(f"    Target:  {r.matched_manifest} -> {r.matched_target}")
                if r.missing_metadata:
                    print(f"    Missing: {', '.join(r.missing_metadata)}")
            if summary.unexpected_file_paths:
                print("\n[!] UNEXPECTED FILES:")
                for p in summary.unexpected_file_paths:
                    print(f"    - {p}")
            print("============================================================")
        return 0

    if args.file:
        if not os.path.isfile(args.file):
            print(f"Error: File not found: {args.file}", file=sys.stderr)
            return 1
        meta = register_file(args.file, manifests_dir=args.manifests_dir)
        if args.json:
            print(meta.model_dump_json(indent=2))
        else:
            print("============================================================")
            print("LABREX FILE REGISTRATION RECORD")
            print("============================================================")
            print(f"Filename:     {meta.filename}")
            print(f"Path:         {meta.file_path}")
            print(f"Size:         {meta.file_size_bytes} bytes")
            print(f"SHA-256:      {meta.sha256_hash}")
            print(f"Type:         {meta.detected_type}")
            print(f"Manifest:     {meta.matched_manifest or 'NO_MATCH'}")
            print(f"Source ID:    {meta.matched_source_id or 'UNKNOWN'}")
            print(f"Target:       {meta.matched_target or 'NONE'}")
            print(f"Unexpected:   {meta.is_unexpected}")
            if meta.missing_metadata:
                print(f"Missing Meta: {', '.join(meta.missing_metadata)}")
            print("============================================================")
        return 0

    parser.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
