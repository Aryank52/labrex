#!/usr/bin/env python3
"""
LABREX Secret Guard Scanner
Authority: Master Directive Section 43 & 67

Scans repository files for hardcoded secrets, API tokens, database connection
passwords, and private credentials before commit.
"""

import os
import re
import sys
from typing import List, Tuple

# Suspicious patterns to detect
SECRET_PATTERNS = [
    (r"(?i)(password|passwd|pwd|secret|token|api_key|apikey)\s*[:=]\s*['\"][A-Za-z0-9_\-\.\$]{8,}['\"]", "Hardcoded credential assignment"),
    (r"AIzaSy[A-Za-z0-9_-]{33}", "Google API Key"),
    (r"sk-[A-Za-z0-9]{20,}", "OpenAI API Key / Token"),
    (r"(?i)postgres(?:ql)?://[a-zA-Z0-9_\-]+:[^@\s/]+@[a-zA-Z0-9_\-\.]+:\d+/[a-zA-Z0-9_\-]+", "PostgreSQL connection string with plaintext password"),
    (r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----", "Private cryptographic key"),
    (r"ghp_[A-Za-z0-9]{36}", "GitHub Personal Access Token"),
    (r"xox[baprs]-[0-9a-zA-Z]{10,}", "Slack Token"),
    (r"eyJ[A-Za-z0-9_-]{10,}\.eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}", "Raw JWT Bearer Token"),
]

# File extensions and paths to inspect
VALID_EXTENSIONS = {".py", ".ts", ".tsx", ".js", ".jsx", ".json", ".yaml", ".yml", ".env", ".toml", ".sh", ".md"}

# Directories to skip
IGNORED_DIRS = {
    ".git",
    "node_modules",
    ".next",
    "__pycache__",
    ".pytest_cache",
    "venv",
    ".venv",
    "dist",
    "build",
    ".labrex"
}

# Explicitly allowed fixture exceptions (e.g. test patterns or template placeholders)
ALLOWED_EXCEPTIONS = [
    "local_dev_secret_key_change_in_production_min_32_chars_long",
    "postgresql+asyncpg://postgres:postgres@localhost:5432/labrex_db",
    "postgresql://postgres:postgres@localhost:5432/labrex_db",
    "YOUR_GITHUB_EMAIL",
    "SecurePassword123!"
]


def is_exception(line: str) -> bool:
    for allowed in ALLOWED_EXCEPTIONS:
        if allowed in line:
            return True
    return False


def scan_file(file_path: str) -> List[Tuple[int, str, str]]:
    findings = []
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            for line_no, line in enumerate(f, start=1):
                if is_exception(line):
                    continue
                for pattern, desc in SECRET_PATTERNS:
                    if re.search(pattern, line):
                        # Mask the finding
                        masked = line.strip()[:60] + "..." if len(line.strip()) > 60 else line.strip()
                        findings.append((line_no, desc, masked))
    except Exception as e:
        print(f"Warning: Could not read {file_path}: {e}", file=sys.stderr)
    return findings


def scan_repository(root_dir: str = ".") -> int:
    print(f"[*] Running LABREX Secret Guard across: {os.path.abspath(root_dir)}")
    total_files_scanned = 0
    total_violations = 0

    for root, dirs, files in os.walk(root_dir):
        dirs[:] = [d for d in dirs if d not in IGNORED_DIRS]
        for file in files:
            _, ext = os.path.splitext(file)
            if ext in VALID_EXTENSIONS or file.startswith(".env"):
                file_path = os.path.join(root, file)
                total_files_scanned += 1
                violations = scan_file(file_path)
                if violations:
                    total_violations += len(violations)
                    print(f"\n[!] VIOLATION DETECTED in {file_path}:")
                    for line_no, desc, snippet in violations:
                        print(f"    Line {line_no} [{desc}]: {snippet}")

    print(f"\n[*] Scan complete: {total_files_scanned} files inspected.")
    if total_violations > 0:
        print(f"[FAIL] {total_violations} potential secret leak(s) detected. Fix before committing.")
        return 1
    else:
        print("[PASS] Zero secret leaks detected. Repository is clean.")
        return 0


if __name__ == "__main__":
    exit_code = scan_repository(".")
    sys.exit(exit_code)
