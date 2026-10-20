# LABREX Loop-Specific Runtime Memory

**Maintained By:** Principal Engineering Agent  
**Last Updated:** 2026-10-20  

---

## 1. Active Environment State
- **PostgreSQL 16**: Located at `E:\postsql database\bin\`, service `postgresql-x64-16` is RUNNING. Port: 5432.
- **Node.js**: v24.16.0 with `npm.cmd` and `npx.cmd`.
- **Python**: 3.12.10 with pre-installed FastAPI, SQLAlchemy, Alembic, Scikit-learn, XGBoost, SHAP, and GeoAlchemy2.
- **PowerShell Invocation**: Do not call raw `.ps1` script files directly due to restricted execution policy; use `.cmd` wrappers.

## 2. Invariant Reminders
- Never use random train/test splits for time series data. Always use walk-forward validation with Seasonal Naive baseline.
- Never output raw SQL from Copilot. All LLM operations must route through Pydantic tools.
- Keep domain services decoupled from API route handlers in `backend/app/services/`.

---

## 3. Data Ingestion & Engineering Learnings (Secondary Loop)
- **PII Guard for e-Shram**: Unorganized worker registries must never ingest microdata. Pre-ingestion `verify_no_pii()` strictly checks headers and aborts on Aadhaar, mobile, name, or account tokens.
- **Canonical Staging Decoupling**: Data engineering proceeds on `backend/app/schemas/staging.py` without requiring physical database migration locks from Phase 3.
- **NCS Demand Signal State Machine**: Real-time vacancy ingestion gracefully operates in 4 states: `NOT_CONFIGURED` (default offline), `AVAILABLE`, `RATE_LIMITED` (exponential backoff), and `UNAVAILABLE`.
- **PMKVY Skilling Separation**: Never conflate trainees in classroom batches with qualified graduates. Ingestion strictly divides signals into `TRAINING_PIPELINE` vs `CERTIFIED_SUPPLY` vs `INFRASTRUCTURE_CAPACITY`.
- **Topological Geography Validation**: Administrative boundary vector files must be validated using Shapely (`is_valid`, non-empty Polygon/MultiPolygon) within the India bounding envelope $[6^\circ\text{N}, 38^\circ\text{N}] \times [68^\circ\text{E}, 98^\circ\text{E}]$ under SRID 4326.
- **Deterministic Fixtures**: All development fixtures in `data/fixtures/` carry explicit `"dataset_type": "FIXTURE"` tags and provenance disclaimers to prevent conflation with official census or statistical publications.

---

## 4. Pre-Ingestion Data Arrival Learnings
- **Cross-Mount Paths on Windows**: When temporary files reside on `C:` while repo is on `E:`, `os.path.relpath()` raises `ValueError`. Always wrap `relpath()` in a try/except fallback that normalizes absolute paths.
- **Browser Download Artifacts**: Saving web pages via browser can create companion `*_files/` directories filled with `.png`, `.css`, and `.js`. The raw data validator correctly detects and rejects these non-permitted file extensions.
- **Manifest Pattern Specificity**: Roman numerals in filename patterns (e.g., `vol_i` vs `vol_ii`) require strict ordering or word boundaries so wildcard `*vol_i*` does not shadow `vol_ii_a` or `vol_ii_b`.

---

## 5. Database Foundation & Migration Learnings (Phase 3)
- **Special Character URL Encoding in Database Connection Strings**: Passwords containing `@` or `%` cause standard URL parsers to misidentify the hostname or break ConfigParser interpolation. Passwords must be percent-encoded (`%40`), and `alembic/env.py` must escape `%` as `%%` when setting `sqlalchemy.url` via `config.set_main_option()`.
- **Topological ForeignKey Migration Ordering**: SQLAlchemy's `Base.metadata.sorted_tables` provides deterministic, topological dependency ordering, ensuring parent dimensions (e.g., `dim_state`, `dim_sector`, `dim_nco`) are created prior to referencing tables (`dim_district`, `dim_occupation`, facts).
- **PostGIS System Table Exclusions**: Alembic autogenerate compares database metadata against target metadata; PostGIS system tables (`spatial_ref_sys`, `topology`, `layer`) must be filtered out in `alembic/env.py:include_object` to prevent spurious drop/create operations.
- **Idempotent Fixture Seeding**: Deterministic benchmark fixtures must always be seeded using PostgreSQL `INSERT ... ON CONFLICT DO NOTHING` on explicit business keys to ensure clean zero-duplication re-runs across local development and CI/CD pipelines.

---

## 6. Database Hardening & Operational Resilience (Phase 3 Recovery)
- **GeoAlchemy2 Duplicate Indexing**: Declaring `Geometry(..., spatial_index=True)` causes GeoAlchemy2's DDL event listeners to create a spatial index automatically. If Alembic also generates `op.create_index(..., postgresql_using='gist')`, migration fails with `relation "idx_..." already exists`. Solution: set `spatial_index=False` on `Geometry` columns and let Alembic explicitly manage `op.create_index`.
- **PowerShell External Process Exit Codes**: PowerShell does NOT halt on non-zero exit codes from native Windows CLI processes (like `python.exe` or `alembic.exe`) even with `$ErrorActionPreference = "Stop"`. Explicit exit-code assertions (`if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }`) are required to prevent silent failure propagation.
- **Async Event Loop Lifecycle in pytest-asyncio**: Under `pytest-asyncio` on Windows, creating pooled connections with a singleton `engine` causes `AttributeError: 'NoneType' object has no attribute 'send'` when subsequent tests run on a new event loop. An autouse fixture yielding and awaiting `engine.dispose()` cleanly recycles connection pools across async test executions.
- **PostgreSQL Transaction Abort on Missing Objects**: When probing for extensions or tables that might not exist in a transaction, catching the exception is not enough; PostgreSQL marks the transaction aborted. The connection must execute `await conn.rollback()` before issuing any subsequent query.
