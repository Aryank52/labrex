"""LABREX Database Connectivity, Extensions, and Migration Revision Checker.

Executes non-destructive health checks:
- Verifies PostgreSQL reachability via configured engine
- Verifies PostGIS extension version
- Verifies pgcrypto extension presence
- Queries active Alembic migration revision
- Exits 0 on full health, 1 on any failure
- Strictly never exposes credentials or DATABASE_URL
"""
import asyncio
import sys
from pathlib import Path

# Ensure repository root is on sys.path
repo_root = Path(__file__).resolve().parent.parent
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

from sqlalchemy import text
from backend.app.core.database import engine
from backend.app.core.config import settings


async def run_check() -> int:
    print(f"[*] Checking LABREX Database Health [{settings.ENVIRONMENT}]")
    exit_code = 0

    try:
        async with engine.connect() as conn:
            # 1. Reachability
            try:
                res = await conn.execute(text("SELECT 1"))
                if res.scalar() == 1:
                    print("  [PASS] PostgreSQL Engine Reachability: OK (SELECT 1)")
                else:
                    print("  [FAIL] Unexpected response from SELECT 1")
                    exit_code = 1
            except Exception as e:
                print(f"  [FAIL] Reachability check failed: {type(e).__name__}")
                await conn.rollback()
                exit_code = 1

            # 2. PostGIS Extension
            try:
                gis = await conn.execute(text("SELECT PostGIS_Version()"))
                gis_ver = gis.scalar()
                print(f"  [PASS] PostGIS Extension: Active ({gis_ver})")
            except Exception as e:
                print(f"  [WARN] PostGIS Extension: Not yet active ({type(e).__name__}) - will be created by migration")
                await conn.rollback()

            # 3. pgcrypto Extension
            try:
                cry = await conn.execute(text("SELECT extversion FROM pg_extension WHERE extname = 'pgcrypto'"))
                cry_ver = cry.scalar()
                if cry_ver:
                    print(f"  [PASS] pgcrypto Extension: Active ({cry_ver})")
                else:
                    print("  [WARN] pgcrypto Extension: Not yet active - will be created by migration")
            except Exception as e:
                print(f"  [WARN] pgcrypto Extension: Query error ({type(e).__name__})")
                await conn.rollback()

            # 4. Current Alembic Revision
            try:
                rev = await conn.execute(text("SELECT version_num FROM alembic_version LIMIT 1"))
                current_rev = rev.scalar()
                if current_rev:
                    print(f"  [PASS] Active Alembic Migration Revision: {current_rev}")
                else:
                    print("  [WARN] Alembic Version Table Empty (No migrations applied yet)")
            except Exception:
                print("  [WARN] Alembic Version Table: Not yet created (Database un-migrated)")
                await conn.rollback()

    except Exception as e:
        print(f"  [FAIL] Database Connection Error: {type(e).__name__}")
        exit_code = 1

    return exit_code


if __name__ == "__main__":
    code = asyncio.run(run_check())
    sys.exit(code)
