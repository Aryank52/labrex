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
