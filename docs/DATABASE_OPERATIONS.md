# LABREX Database Operations Guide

**System:** LABREX Primary Decision-Support & Policy Optimization Platform  
**Target:** Local PostgreSQL 16.15 + PostGIS 3.4.2  
**Driver & ORM:** `asyncpg` 0.31.0 + SQLAlchemy 2.1.1 (AsyncIO)  
**Migration Tool:** Alembic 1.13.0  
**Effective Date:** 2026-10-21  

---

## 1. Architecture Overview

LABREX leverages a high-performance, asynchronous relational and geospatial data layer:
- **Engine:** PostgreSQL 16 (Service `postgresql-x64-16`) on `127.0.0.1:5432`, database `labrex`.
- **Spatial Extensions:** PostGIS 3.4.2 enabled with SRID 4326 for administrative state and district boundaries, centroids, and training institution coordinates.
- **Cryptographic Extensions:** `pgcrypto` 1.3 for deterministic hashing and cryptographic operations.
- **Connection Pooling:** SQLAlchemy `AsyncEngine` with `pool_size=10`, `max_overflow=20`, `pool_pre_ping=True`.
- **Driver:** High-throughput binary protocol async driver `asyncpg`.

---

## 2. Environment Configuration

The local application connects via the git-ignored `.env` file at the repository root.

### URL Format & Special Character Encoding
```env
DATABASE_URL=postgresql+asyncpg://postgres:<ENCODED_PASSWORD>@127.0.0.1:5432/labrex
ENVIRONMENT=development
DEBUG=true
```

> [!IMPORTANT]
> If your database password contains special characters (such as `@`, `:`, or `/`), they **must** be percent-encoded in connection strings to prevent URL parsing errors (e.g. `@` must be written as `%40`). The LABREX `Settings` model automatically validates and sanitizes credentials, but adhering to RFC 3986 in `.env` is recommended.

---

## 3. PowerShell Operations CLI (`scripts/db_ops.ps1`)

LABREX provides a unified, cross-platform PowerShell automation script for common operational routines:

### Applying Migrations
Applies all pending migration revisions up to `head`:
```powershell
.\scripts\db_ops.ps1 -Action migrate
```
*Equivalent raw command:*
```powershell
$env:PYTHONPATH="."; alembic upgrade head
```

### Checking Active Migration Status
Inspects the current migration revision recorded in `alembic_version`:
```powershell
.\scripts\db_ops.ps1 -Action current
```
*Equivalent raw command:*
```powershell
$env:PYTHONPATH="."; alembic current
```

### Seeding Reference Data and Deterministic Benchmark Fixtures
Executes the idempotent seed framework:
```powershell
.\scripts\db_ops.ps1 -Action seed
```
*Equivalent raw command:*
```powershell
$env:PYTHONPATH="."; python -m backend.app.services.data.seed_runner
```

### Running Test Verification Suites
Executes the full test suite (unit, integration, database, and security):
```powershell
.\scripts\db_ops.ps1 -Action test
```
*Equivalent raw command:*
```powershell
pytest backend/tests -v
```

### Checking Engine & Extension Health
Verifies database connectivity, PostGIS 3.4, pgcrypto 1.3, and active Alembic migration revision without exposing credentials:
```powershell
.\scripts\db_ops.ps1 -Action check
```
*Equivalent raw command:*
```powershell
python scripts/db_check.py
```

### Fail-Fast CLI Execution Guarantee
All operations in `scripts/db_ops.ps1` enforce strict error handling (`Assert-LastExitCode`):
- Non-zero exit codes from underlying tools (`alembic`, `python`, `pytest`) immediately abort the pipeline.
- If a migration fails, subsequent seed and test actions are prevented from executing.
- If seed fails, subsequent tests are prevented from executing.
- Success messages are never printed upon error.

---

## 4. Disposable Database Reset & Recovery Procedure

In local development before external production datasets are ingested, the `labrex` database can be safely reset and reconstructed cleanly:

```powershell
# 1. Terminate any active connections and drop the database
psql -U postgres -h 127.0.0.1 -c "SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = 'labrex' AND pid <> pg_backend_pid();"
psql -U postgres -h 127.0.0.1 -c "DROP DATABASE IF EXISTS labrex;"

# 2. Recreate the empty labrex database
psql -U postgres -h 127.0.0.1 -c "CREATE DATABASE labrex;"

# 3. Apply the initial schema migration (extensions & tables created by Alembic)
.\scripts\db_ops.ps1 -Action migrate

# 4. Verify current active revision
.\scripts\db_ops.ps1 -Action current

# 5. Populate reference data and benchmark fixtures
.\scripts\db_ops.ps1 -Action seed

# 6. Execute full verification test suite
.\scripts\db_ops.ps1 -Action test
```

---

## 5. Migration Architecture

The root migration environment is organized as:
```text
/alembic.ini             # Root configuration pointing to script_location = alembic
/alembic/
    env.py               # Async Alembic execution environment connecting via Settings.DATABASE_URL
    script.py.mako       # Migration template with GeoAlchemy2 and PostgreSQL dialect imports
    versions/
        20261020_0001_initial_schema.py  # Initial foundation schema (extensions, dimensions, facts)
```

### Creating New Migrations
When ORM models in `backend/app/models/` are added or updated:
```powershell
$env:PYTHONPATH="."; alembic revision --autogenerate -m "describe_migration"
```

---

## 5. Seed Framework & Data Governance

### Provenance Labeling
All demo data generated by the seed framework adheres strictly to the LABREX Data Governance Constitution:
- **Authority:** `LABREX Methodology & Synthesis Engine`
- **Source ID:** `LABREX_DEMO`
- **Dataset Type:** `FIXTURE`
- **License:** `LABREX_INTERNAL_BENCHMARK`

> [!WARNING]
> No fabricated government statistics are ever stored under official source designations (`SRC-NCS`, `SRC-PLFS`, `SRC-PMKVY`). All synthetic fixtures are unambiguously quarantined via `dataset_type='FIXTURE'`.

### Idempotency Guarantee
The seed routines use PostgreSQL `INSERT ... ON CONFLICT DO NOTHING` indexed on natural business keys (`state_id`, `district_id`, `sector_id`, `nco_code`, `occupation_id`, `skill_id`, `qualification_id`, `center_id`, and `[district_id, occupation_id, date_key]`). Re-running the seed runner multiple times produces **zero** duplicate records and preserves existing state.

---

## 6. Probes & Health API

FastAPI exposes two HTTP probes configured for container orchestrators and monitoring:

1. **Liveness Probe (`GET /api/v1/health` or `GET /health`):**
   - Returns HTTP 200 `{"status": "HEALTHY", "components": {"api": "OPERATIONAL"}}`.
2. **Readiness Probe (`GET /api/v1/health/ready` or `GET /ready`):**
   - Tests active PostgreSQL connection via `SELECT 1`.
   - Inspects `alembic_version` to verify schema compatibility.
   - Returns HTTP 200 `{"status": "READY", "components": {"database": "CONNECTED", "migration": "APPLIED:0001_initial_schema"}}` or HTTP 503 if unreachable.
