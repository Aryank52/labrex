import os
import subprocess
import sys


def test_secret_guard_clean_repo():
    """Validates that the repository passes the secret guard scan cleanly."""
    cmd = [sys.executable, "scripts/secret_guard.py"]
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=os.getcwd())
    assert result.returncode == 0, f"Secret guard failed:\n{result.stdout}\n{result.stderr}"
    assert "Zero secret leaks detected" in result.stdout
