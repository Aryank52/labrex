# LABREX Machine-Readable Task Queue

**Authority:** Master Directive Section 90  
**States:** `TODO` | `READY` | `IN_PROGRESS` | `BLOCKED` | `REVIEW` | `FAILED` | `VERIFIED` | `DONE`  

---

### TASK-001
- **TASK-ID**: TASK-001
- **TITLE**: Discover Host Environment & Tooling
- **DOMAIN**: Architecture / Discovery
- **DEPENDENCIES**: None
- **DESCRIPTION**: Run host discovery commands to determine Python, Node, Git, PostgreSQL, Docker, and MCP capabilities.
- **FILES**: `docs/ENVIRONMENT_INVENTORY.md`
- **ACCEPTANCE**: All runtimes, services, and paths discovered and documented without exposed credentials.
- **TEST COMMANDS**: Direct environment inspection via PowerShell.
- **RISK**: Low
- **ESTIMATED COMPLEXITY**: Small
- **STATUS**: DONE

---

### TASK-002
- **TASK-ID**: TASK-002
- **TITLE**: Construct Antigravity Capability Matrix
- **DOMAIN**: Architecture / Tooling
- **DEPENDENCIES**: TASK-001
- **DESCRIPTION**: Classify all discovered capabilities into ESSENTIAL, RECOMMENDED, OPTIONAL, IRRELEVANT, and UNAVAILABLE.
- **FILES**: `docs/ANTIGRAVITY_CAPABILITY_MATRIX.md`
- **ACCEPTANCE**: Clear boundaries set; zero duplicate or conflicting plugins.
- **TEST COMMANDS**: Inspection of matrix document against directive rules.
- **RISK**: Low
- **ESTIMATED COMPLEXITY**: Small
- **STATUS**: DONE

---

### TASK-003
- **TASK-ID**: TASK-003
- **TITLE**: Establish Root Constitution & Governance
- **DOMAIN**: Governance / Standards
- **DEPENDENCIES**: TASK-002
- **DESCRIPTION**: Create authoritative root constitution documents defining project identity, rules, brain, memory, tasks, error codes, and agent hierarchy.
- **FILES**: `README.md`, `AGENTS.md`, `BRAIN.md`, `MEMORY.md`, `TASKS.md`, `RULES.md`, `ERROR_CATALOG.md`
- **ACCEPTANCE**: All 7 root documents present, cohesive, and aligned with master directive.
- **TEST COMMANDS**: Verification of files in root directory.
- **RISK**: Low
- **ESTIMATED COMPLEXITY**: Medium
- **STATUS**: DONE

---

### TASK-004
- **TASK-ID**: TASK-004
- **TITLE**: Author Full System Architecture & Engineering Specifications
- **DOMAIN**: Architecture / Documentation
- **DEPENDENCIES**: TASK-003
- **DESCRIPTION**: Write the complete 23-document architectural suite across product, data, ML, optimization, security, UI/UX, and testing.
- **FILES**: `docs/*.md` (PRD, TRD, ARCHITECTURE, BACKEND_SCHEMA, API_SPEC, ML_ARCHITECTURE, THREAT_MODEL, etc.)
- **ACCEPTANCE**: All documents written with technical depth, math formulas, schemas, and zero placeholders.
- **TEST COMMANDS**: Verification of 23 markdown documents in `docs/`.
- **RISK**: Medium
- **ESTIMATED COMPLEXITY**: High
- **STATUS**: DONE

---

### TASK-005
- **TASK-ID**: TASK-005
- **TITLE**: Create Loop Specification & Persistent State
- **DOMAIN**: Loop Engineering
- **DEPENDENCIES**: TASK-004
- **DESCRIPTION**: Set up `.labrex/` state files (`LOOP_SPEC.md`, `LOOP_STATE.md`, `TASK_QUEUE.md`, `ITERATION_LOG.md`, `BLOCKERS.md`, `DECISIONS.md`, `MEMORY.md`).
- **FILES**: `.labrex/*`
- **ACCEPTANCE**: State files initialized and ready to track iterations across sessions.
- **TEST COMMANDS**: Inspection of `.labrex/` directory.
- **RISK**: Low
- **ESTIMATED COMPLEXITY**: Small
- **STATUS**: DONE

---

### TASK-006
- **TASK-ID**: TASK-006
- **TITLE**: Author Initial Architecture Decision Records (ADRs)
- **DOMAIN**: Architecture / Decision Log
- **DEPENDENCIES**: TASK-005
- **DESCRIPTION**: Record foundational architecture decisions ADR-0001 through ADR-0007 in `docs/architecture/`.
- **FILES**: `docs/architecture/ADR-0001-modular-monolith.md` through `ADR-0007-cloud-run-container-deployment.md`
- **ACCEPTANCE**: 7 ADRs documented following standard context, decision, consequences structure.
- **TEST COMMANDS**: Inspection of `docs/architecture/`.
- **RISK**: Low
- **ESTIMATED COMPLEXITY**: Medium
- **STATUS**: READY

---

### TASK-007
- **TASK-ID**: TASK-007
- **TITLE**: Scaffold Repository Structure
- **DOMAIN**: Platform / DevOps
- **DEPENDENCIES**: TASK-006
- **DESCRIPTION**: Create the monorepo directory tree for `backend/`, `frontend/`, `scripts/`, Dockerfiles, docker-compose, and `.env.example`.
- **FILES**: `backend/`, `frontend/`, `scripts/secret_guard.py`, `Dockerfile.backend`, `Dockerfile.frontend`, `docker-compose.yml`, `.env.example`, `.gitignore`
- **ACCEPTANCE**: Complete directory tree scaffolded with valid syntax and configuration.
- **TEST COMMANDS**: File tree inspection and Python syntax check.
- **RISK**: Low
- **ESTIMATED COMPLEXITY**: Medium
- **STATUS**: READY

---

### TASK-008
- **TASK-ID**: TASK-008
- **TITLE**: Implement and Validate Secret Guard Scanner
- **DOMAIN**: Security / Pre-Commit
- **DEPENDENCIES**: TASK-007
- **DESCRIPTION**: Write `scripts/secret_guard.py` with regex patterns for API keys, DB passwords, JWT secrets, and private keys.
- **FILES**: `scripts/secret_guard.py`
- **ACCEPTANCE**: Scanner executes, exits 0 on clean code, and detects intentionally injected secret patterns in test mode.
- **TEST COMMANDS**: `python scripts/secret_guard.py`
- **RISK**: Low
- **ESTIMATED COMPLEXITY**: Small
- **STATUS**: READY

---

### TASK-009
- **TASK-ID**: TASK-009
- **TITLE**: Validate Scaffold & Initialize Git Repository
- **DOMAIN**: Platform / SCM
- **DEPENDENCIES**: TASK-008
- **DESCRIPTION**: Initialize git in project root, verify `.gitignore`, run secret guard scanner, run basic pytest check on backend scaffold, and commit Phase 0/1 milestone.
- **FILES**: `.git/`, `.gitignore`
- **ACCEPTANCE**: Clean git status, zero secret leaks, tests pass.
- **TEST COMMANDS**: `git status`, `python scripts/secret_guard.py`, `pytest backend/tests/`
- **RISK**: Low
- **ESTIMATED COMPLEXITY**: Small
- **STATUS**: READY

---

### TASK-010
- **TASK-ID**: TASK-010
- **TITLE**: Generate Phase 0 Initialization Report
- **DOMAIN**: Governance / Reporting
- **DEPENDENCIES**: TASK-009
- **DESCRIPTION**: Produce the authoritative final initialization artifact `docs/PHASE0_INITIALIZATION_REPORT.md` and complete the initial turn.
- **FILES**: `docs/PHASE0_INITIALIZATION_REPORT.md`
- **ACCEPTANCE**: Comprehensive summary of environment, tools, files created, risks, blockers, and exact next prompt.
- **TEST COMMANDS**: Inspection of report.
- **RISK**: Low
- **ESTIMATED COMPLEXITY**: Small
- **STATUS**: READY

---

### TASK-DATA-001
- **TASK-ID**: TASK-DATA-001
- **TITLE**: Data Source Registry & Download Manifests
- **DOMAIN**: Data Engineering / Governance
- **DEPENDENCIES**: None
- **DESCRIPTION**: Author docs/DATA_SOURCE_REGISTRY.md with 14 fields per source and create 7 YAML manifests in data/manifests/.
- **FILES**: `docs/DATA_SOURCE_REGISTRY.md`, `data/manifests/*.yaml`
- **ACCEPTANCE**: All 7 core sources (NCO, PLFS, NCS, e-Shram, PMKVY, NSDC, Geography) cataloged with verified access modes.
- **TEST COMMANDS**: YAML schema load check.
- **RISK**: Low
- **ESTIMATED COMPLEXITY**: Medium
- **STATUS**: DONE

---

### TASK-DATA-002
- **TASK-ID**: TASK-DATA-002
- **TITLE**: Canonical Staging Contracts & Medallion Ingestion Architecture
- **DOMAIN**: Data Engineering / Schemas
- **DEPENDENCIES**: TASK-DATA-001
- **DESCRIPTION**: Implement decoupled Pydantic v2 staging models in backend/app/schemas/staging.py and document pipeline in docs/DATA_PIPELINE.md.
- **FILES**: `backend/app/schemas/staging.py`, `docs/DATA_PIPELINE.md`
- **ACCEPTANCE**: All canonical signals (Observation, Occupation, Skill, Training, Workforce) defined with strict typing.
- **TEST COMMANDS**: `pytest backend/tests/unit/test_canonical_staging.py`
- **RISK**: Low
- **ESTIMATED COMPLEXITY**: Medium
- **STATUS**: DONE

---

### TASK-DATA-003
- **TASK-ID**: TASK-DATA-003
- **TITLE**: Automated Data Quality Framework & Cryptographic Lineage Engine
- **DOMAIN**: Data Governance & Quality
- **DEPENDENCIES**: TASK-DATA-002
- **DESCRIPTION**: Implement DataQualityEngine with 8 validation rules, penalty scoring (0-100), and IngestionLineage SHA-256 tracker.
- **FILES**: `backend/app/services/data/quality/`, `backend/app/services/data/lineage/`, `docs/DATA_QUALITY.md`, `docs/DATA_LINEAGE.md`
- **ACCEPTANCE**: Automated validation of missing dates, invalid geo, duplicates, negative counts, NCO regex, PII leakage, staleness.
- **TEST COMMANDS**: `pytest backend/tests/unit/test_data_quality.py`, `pytest backend/tests/unit/test_data_lineage.py`
- **RISK**: Low
- **ESTIMATED COMPLEXITY**: High
- **STATUS**: DONE

---

### TASK-DATA-004
- **TASK-ID**: TASK-DATA-004
- **TITLE**: Ingestion Parsers & Adapters for Official Datasets
- **DOMAIN**: Data Engineering / Adapters
- **DEPENDENCIES**: TASK-DATA-003
- **DESCRIPTION**: Build adapters for NCO, PLFS, e-Shram (PII guarded), PMKVY (stream split), NSDC, NCS (4 connection states), and Geography (Shapely + EPSG:4326).
- **FILES**: `backend/app/services/data/parsers/`, `backend/app/services/data/adapters/`
- **ACCEPTANCE**: All parsers normalize raw inputs into canonical contracts without data loss or unauthorized scraping.
- **TEST COMMANDS**: `pytest backend/tests/unit/test_data_adapters.py`
- **RISK**: Medium
- **ESTIMATED COMPLEXITY**: High
- **STATUS**: DONE

---

### TASK-DATA-005
- **TASK-ID**: TASK-DATA-005
- **TITLE**: Deterministic Test Fixtures & Unit Test Verification Suite
- **DOMAIN**: QA / Automation
- **DEPENDENCIES**: TASK-DATA-004
- **DESCRIPTION**: Create deterministic test fixtures in data/fixtures/ tagged with dataset_type=FIXTURE and verify with 27 unit tests.
- **FILES**: `data/fixtures/*.json`, `data/fixtures/*.geojson`, `backend/tests/unit/test_*.py`
- **ACCEPTANCE**: 100% test pass rate with zero secret leaks.
- **TEST COMMANDS**: `pytest backend/tests/`, `python scripts/secret_guard.py`
- **RISK**: Low
- **ESTIMATED COMPLEXITY**: Medium
- **STATUS**: DONE

---

### TASK-DATA-006
- **TASK-ID**: TASK-DATA-006
- **TITLE**: Ingestion Implementation Roadmap & Operator Download Guide
- **DOMAIN**: Documentation / Operations
- **DEPENDENCIES**: TASK-DATA-005
- **DESCRIPTION**: Author docs/DATA_DOWNLOAD_GUIDE.md and docs/INGESTION_ROADMAP.md covering pre-ingestion checks and post-Phase 3 migration.
- **FILES**: `docs/DATA_DOWNLOAD_GUIDE.md`, `docs/INGESTION_ROADMAP.md`
- **ACCEPTANCE**: Clear, auditable operator manual for downloading and staging official datasets.
- **TEST COMMANDS**: Markdown inspection.
- **RISK**: Low
- **ESTIMATED COMPLEXITY**: Small
- **STATUS**: DONE

---

### TASK-DATA-007
- **TASK-ID**: TASK-DATA-007
- **TITLE**: Manifest Target Harmonization & Download Checklist Expansion
- **DOMAIN**: Data Acquisition / Specification
- **DEPENDENCIES**: TASK-DATA-006
- **DESCRIPTION**: Update data/manifests/*.yaml to version 2.0.0 with exact acquisition targets (NCO Vol I/II-B, Geo boundaries, PLFS 5 rounds, PMKVY 4 series, e-Shram aggregates, NCS vacancies, NSDC directory) and expand docs/DATA_DOWNLOAD_GUIDE.md and docs/DATA_ACQUISITION_STATUS.md.
- **FILES**: `data/manifests/*.yaml`, `docs/DATA_DOWNLOAD_GUIDE.md`, `docs/DATA_ACQUISITION_STATUS.md`
- **ACCEPTANCE**: All manifests and checklists explicitly enumerate exact target files, formats, login requirements, and URLs.
- **TEST COMMANDS**: Manifest load inspection.
- **RISK**: Low
- **ESTIMATED COMPLEXITY**: Medium
- **STATUS**: DONE

---

### TASK-DATA-008
- **TASK-ID**: TASK-DATA-008
- **TITLE**: Raw File Registration Tool & Pre-Ingestion Validator CLI
- **DOMAIN**: Data Tooling / Quality Gate
- **DEPENDENCIES**: TASK-DATA-007
- **DESCRIPTION**: Implement python -m labrex.data.register_file and python -m labrex.data.validate_raw for offline file identification, SHA-256 calculation, manifest matching, PII safety checks, and schema validation.
- **FILES**: `labrex/data/register_file.py`, `labrex/data/validate_raw.py`, `backend/app/services/data/registration.py`, `backend/app/services/data/raw_validator.py`, `backend/tests/unit/test_raw_validation.py`
- **ACCEPTANCE**: Automated CLI tools operate locally without network transmission, correctly detect unexpected files and PII leaks, 35 tests passing.
- **TEST COMMANDS**: `pytest backend/tests/`, `python -m labrex.data.validate_raw`
- **RISK**: Low
- **ESTIMATED COMPLEXITY**: Medium
- **STATUS**: DONE

---

### TASK-011
- **TASK-ID**: TASK-011
- **TITLE**: Phase 3 Database Foundation & Migration Architecture
- **DOMAIN**: Database & Platform Engineering
- **DEPENDENCIES**: TASK-010, TASK-DATA-008
- **DESCRIPTION**: Set up root Alembic migration environment, configure async env.py, create initial schema migration for 36 tables with PostGIS extensions, SRID 4326 geometries, constraints, indexes, idempotent seed framework, and automated PowerShell db_ops CLI.
- **FILES**: `alembic.ini`, `alembic/env.py`, `alembic/versions/20261020_0001_initial_schema.py`, `backend/app/models/*.py`, `backend/app/services/data/seed_framework.py`, `scripts/db_ops.ps1`, `docs/DATABASE_OPERATIONS.md`, `docs/PHASE3_DATABASE_VERIFICATION.md`
- **ACCEPTANCE**: Alembic environment functional, 36 normalized tables defined in Base.metadata, idempotent seed with zero row duplication, 35/35 pytest tests pass, secret guard clean.
- **TEST COMMANDS**: `pytest backend/tests/ -v`, `python scripts/secret_guard.py`
- **RISK**: Medium
- **ESTIMATED COMPLEXITY**: High
- **STATUS**: DONE
