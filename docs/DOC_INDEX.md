# LABREX Documentation Index

**Document Version:** 1.0  
**Authority:** Master Directive Section 0, 5  
**Precedence Hierarchy:** See Section 2  
**Last Updated:** 2026-11-04  
**Maintained By:** Principal Engineering Agent

---

## 1. Document Precedence Hierarchy (Conflict Resolution)

Per `AGENTS.md` Section 4 and `RULES.md`, when requirements or implementation choices conflict, the order of precedence is strictly:

| Priority | Document | Description | Immutable Without |
|----------|----------|-------------|-------------------|
| **1** | `docs/PRD.md` | Product Scope & Value | ADR |
| **2** | `docs/TRD.md` | Technical Requirements | ADR |
| **3** | `docs/ARCHITECTURE.md` | System Design | ADR |
| **4** | `docs/architecture/ADR-*.md` | Recorded Architecture Decisions | New ADR |
| **5** | `.labrex/TASK_QUEUE.md` | Current Active Task | Loop Iteration |
| **6** | `docs/*.md` (other) | Detailed Specifications | ADR if architectural |
| **7** | `README.md` | Project Overview | Never (root) |
| **8** | `AGENTS.md` | Agent Constitution | Never (root) |
| **9** | `BRAIN.md` | Domain Knowledge | Never (root) |
| **10** | `RULES.md` | Engineering Rules | Never (root) |
| **11** | `.labrex/LOOP_SPEC.md` | Loop Contract | Never (root) |
| **12** | `.labrex/LOOP_STATE.md` | Current State | Loop Iteration (append-only) |
| **13** | `.labrex/MEMORY.md` | Runtime Learnings | Loop Iteration (append-only) |

**Rule:** Lower-numbered documents override higher-numbered. Never modify precedence documents without an approved ADR.

---

## 2. Root Constitutional Documents (Repository Root)

| Document | Purpose | Last Updated | Version |
|----------|---------|--------------|---------|
| [`README.md`](../README.md) | Project overview, stack, quickstart | 2026-10-20 | 1.0 |
| [`AGENTS.md`](../AGENTS.md) | Principal agent governance, Maker/Checker/Validator | 2026-10-20 | 1.0 |
| [`BRAIN.md`](../BRAIN.md) | Domain foundations, mathematical formulations | 2026-10-20 | 1.0 |
| [`RULES.md`](../RULES.md) | Mandatory engineering, security, architectural rules | 2026-10-20 | 1.0 |
| [`MEMORY.md`](../MEMORY.md) | Persistent operational learnings | 2026-11-04 | 1.0 |
| [`TASKS.md`](../TASKS.md) | Human-readable master task roadmap | 2026-10-20 | 1.0 |
| [`ERROR_CATALOG.md`](../ERROR_CATALOG.md) | RFC 7807 error codes (see `docs/ERROR_CATALOG.md`) | 2026-11-04 | 1.0 |

---

## 3. Authoritative Architecture Suite (`docs/`)

### 3.1 Core Specifications (Precedence Tier 1-3)

| Document | Purpose | Precedence | Status |
|----------|---------|------------|--------|
| [`PRD.md`](PRD.md) | Product Requirements — 4 analytical tiers, 5 personas, 7 FRs | **1** | ✅ Approved |
| [`TRD.md`](TRD.md) | Technical Requirements — stack, protocols, scaling profiles | **2** | ✅ Approved |
| [`ARCHITECTURE.md`](ARCHITECTURE.md) | System architecture — domain decomposition, data flows | **3** | ✅ Approved |

### 3.2 Domain Specifications

| Document | Purpose | Related To |
|----------|---------|------------|
| [`APP_FLOW.md`](APP_FLOW.md) | User workflows, state transitions | ARCHITECTURE, PRD |
| [`UI_UX_BRIEF.md`](UI_UX_BRIEF.md) | Design system — colors, typography, layout, responsiveness | ARCHITECTURE, PRD |
| [`BACKEND_SCHEMA.md`](BACKEND_SCHEMA.md) | Relational & dimensional schema (PostGIS) | ARCHITECTURE, TRD |
| [`API_SPEC.md`](API_SPEC.md) | REST API v1 contracts — 8 endpoint groups | ARCHITECTURE, TRD |
| [`DATA_ARCHITECTURE.md`](DATA_ARCHITECTURE.md) | Medallion pipeline (Raw→Bronze→Silver→Gold→Feature→Model→Serving) | ARCHITECTURE, TRD |
| [`DATA_SOURCE_REGISTRY.md`](DATA_SOURCE_REGISTRY.md) | 7 core sources, access methods, PII guards | DATA_ARCHITECTURE |
| [`ML_ARCHITECTURE.md`](ML_ARCHITECTURE.md) | Champion-vs-Challenger forecasting, walk-forward validation | ARCHITECTURE, TRD |
| [`MODEL_GOVERNANCE.md`](MODEL_GOVERNANCE.md) | Model registry, validation, retirement policy | ML_ARCHITECTURE |
| [`AI_ARCHITECTURE.md`](AI_ARCHITECTURE.md) | Copilot topology, tool registry, injection defense | ARCHITECTURE, TRD |
| [`SECURITY.md`](SECURITY.md) | Security architecture, RBAC, encryption | ARCHITECTURE, TRD |
| [`THREAT_MODEL.md`](THREAT_MODEL.md) | STRIDE threat model, mitigations | SECURITY |
| [`OBSERVABILITY.md`](OBSERVABILITY.md) | Logging, metrics, tracing, dashboards | ARCHITECTURE |
| [`TEST_STRATEGY.md`](TEST_STRATEGY.md) | 10-tier test strategy (unit → E2E → visual → perf → security) | ARCHITECTURE |
| [`EVALUATION_PLAN.md`](EVALUATION_PLAN.md) | Model evaluation metrics, benchmarks, acceptance criteria | ML_ARCHITECTURE |
| [`DEPLOYMENT.md`](DEPLOYMENT.md) | Cloud Run, Cloud SQL, Terraform, CI/CD | ARCHITECTURE, TRD |
| [`IMPLEMENTATION_PLAN.md`](IMPLEMENTATION_PLAN.md) | 19-phase master schedule with gantt | ARCHITECTURE |
| [`UX_ACCEPTANCE_CRITERIA.md`](UX_ACCEPTANCE_CRITERIA.md) | Page-level acceptance gates, accessibility | UI_UX_BRIEF |
| [`DEMO_SCENARIOS.md`](DEMO_SCENARIOS.md) | 7 deterministic demo scenarios for validation | PRD, APP_FLOW |
| [`DATA_LINEAGE.md`](DATA_LINEAGE.md) | Cryptographic provenance, HMAC batch signatures | DATA_ARCHITECTURE |
| [`LIMITATIONS.md`](LIMITATIONS.md) | Operational boundaries, transparency disclaimers | PRD |
| [`SCENARIO_ENGINE.md`](SCENARIO_ENGINE.md) | Scenario simulation engine specification | ARCHITECTURE, APP_FLOW |
| [`ERROR_CATALOG.md`](ERROR_CATALOG.md) | RFC 7807 error codes (machine-readable) | API_SPEC, SECURITY |
| [`DATA_DOWNLOAD_GUIDE.md`](DATA_DOWNLOAD_GUIDE.md) | Operator manual for 7 source downloads | DATA_SOURCE_REGISTRY |
| [`INGESTION_ROADMAP.md`](INGESTION_ROADMAP.md) | Phased ingestion plan with gates & rollback | DATA_ARCHITECTURE |
| [`DATA_ACQUISITION_STATUS.md`](DATA_ACQUISITION_STATUS.md) | Live tracker: 53 artifacts, status, checksums | DATA_DOWNLOAD_GUIDE |
| [`NCO_VALIDATION_REPORT.md`](NCO_VALIDATION_REPORT.md) | NCO-2015 parser validation evidence | DATA_SOURCE_REGISTRY |
| [`PHASE0_INITIALIZATION_REPORT.md`](PHASE0_INITIALIZATION_REPORT.md) | Phase 0/1 completion evidence | IMPLEMENTATION_PLAN |
| [`PHASE3_DATABASE_VERIFICATION.md`](PHASE3_DATABASE_VERIFICATION.md) | Phase 3 DB verification (42 tests, schema, seed) | IMPLEMENTATION_PLAN |
| [`DATABASE_OPERATIONS.md`](DATABASE_OPERATIONS.md) | Migration, seed, test CLI procedures | IMPLEMENTATION_PLAN |

---

## 4. Architecture Decision Records (`docs/architecture/`)

| ADR | Title | Status | Date |
|-----|-------|--------|------|
| [`ADR-0001`](architecture/ADR-0001-modular-monolith.md) | Modular Monolith Architecture | ✅ Accepted | 2026-10-20 |
| [`ADR-0002`](architecture/ADR-0002-postgresql-postgis-primary-storage.md) | PostgreSQL 16 + PostGIS Primary Storage | ✅ Accepted | 2026-10-20 |
| [`ADR-0003`](architecture/ADR-0003-bigquery-analytical-layer.md) | BigQuery Analytical Layer | ✅ Accepted | 2026-10-20 |
| [`ADR-0004`](architecture/ADR-0004-forecasting-champion-challenger.md) | Champion-vs-Challenger Forecasting | ✅ Accepted | 2026-10-20 |
| [`ADR-0005`](architecture/ADR-0005-tool-grounded-ai-copilot.md) | Tool-Grounded AI Copilot | ✅ Accepted | 2026-10-20 |
| [`ADR-0006`](architecture/ADR-0006-or-tools-policy-optimizer.md) | Google OR-Tools Policy Optimizer | ✅ Accepted | 2026-10-20 |
| [`ADR-0007`](architecture/ADR-0007-cloud-run-container-deployment.md) | Cloud Run Container Deployment | ✅ Accepted | 2026-10-20 |

**ADR Template:** Context → Decision → Consequences → Alternatives Considered → Links

---

## 5. Persistent Loop State (`.labrex/`)

| File | Purpose | Update Frequency |
|------|---------|------------------|
| [`LOOP_SPEC.md`](../.labrex/LOOP_SPEC.md) | Loop contract (Discover→Plan→Implement→...→Commit) | Never (immutable) |
| [`LOOP_STATE.md`](../.labrex/LOOP_STATE.md) | Active phase, task, iteration count | Every iteration |
| [`TASK_QUEUE.md`](../.labrex/TASK_QUEUE.md) | Machine-readable task queue with status | Every task transition |
| [`ITERATION_LOG.md`](../.labrex/ITERATION_LOG.md) | Chronological audit log | Every iteration |
| [`MEMORY.md`](../.labrex/MEMORY.md) | Runtime learnings, gotchas | As discovered |
| [`DECISIONS.md`](../.labrex/DECISIONS.md) | Technical trade-offs log | As decided |
| [`BLOCKERS.md`](../.labrex/BLOCKERS.md) | Active blockers with reproduction steps | As blocked/resolved |

---

## 6. Implementation Artifacts (Not Documentation — For Reference)

| Artifact | Location | Purpose |
|----------|----------|---------|
| Alembic Migrations | `alembic/versions/` | Schema evolution (never edit applied) |
| ORM Models | `backend/app/models/` | SQLAlchemy 2.0 table definitions |
| Pydantic Schemas | `backend/app/schemas/` | API contracts, staging contracts |
| Domain Services | `backend/app/services/` | Pure business logic |
| API Routes | `backend/app/api/v1/` | HTTP controllers (no logic) |
| Frontend Pages | `frontend/src/app/` | Next.js App Router pages |
| UI Components | `frontend/src/components/` | Reusable React components |
| Test Suites | `backend/tests/`, `frontend/` | Pytest + Vitest/Playwright |
| Scripts | `scripts/` | Automation, validation, ops |

---

## 7. Navigation Quick Links

### By Role

| Role | Start Here |
|------|------------|
| **Product Owner** | `PRD.md` → `DEMO_SCENARIOS.md` → `UX_ACCEPTANCE_CRITERIA.md` |
| **Backend Engineer** | `ARCHITECTURE.md` → `BACKEND_SCHEMA.md` → `API_SPEC.md` → `BACKEND_SCHEMA.md` |
| **Frontend Engineer** | `UI_UX_BRIEF.md` → `API_SPEC.md` → `APP_FLOW.md` → `UX_ACCEPTANCE_CRITERIA.md` |
| **Data Engineer** | `DATA_ARCHITECTURE.md` → `DATA_SOURCE_REGISTRY.md` → `INGESTION_ROADMAP.md` |
| **ML Engineer** | `ML_ARCHITECTURE.md` → `MODEL_GOVERNANCE.md` → `EVALUATION_PLAN.md` |
| **Security Engineer** | `SECURITY.md` → `THREAT_MODEL.md` → `ERROR_CATALOG.md` |
| **QA Engineer** | `TEST_STRATEGY.md` → `UX_ACCEPTANCE_CRITERIA.md` → `EVALUATION_PLAN.md` |
| **DevOps Engineer** | `DEPLOYMENT.md` → `DATABASE_OPERATIONS.md` → `OBSERVABILITY.md` |
| **New Team Member** | `README.md` → `AGENTS.md` → `BRAIN.md` → `RULES.md` → `DOC_INDEX.md` |

### By Phase

| Phase | Key Documents |
|-------|---------------|
| **Phase 0-1 (Constitution)** | `README.md`, `AGENTS.md`, `BRAIN.md`, `RULES.md`, `DOC_INDEX.md`, `PHASE0_INITIALIZATION_REPORT.md` |
| **Phase 2 (Scaffold)** | `IMPLEMENTATION_PLAN.md`, `DATABASE_OPERATIONS.md` |
| **Phase 3 (Database)** | `BACKEND_SCHEMA.md`, `PHASE3_DATABASE_VERIFICATION.md`, `alembic/versions/0001_initial_schema.py` |
| **Phase 4 (Ingestion)** | `DATA_SOURCE_REGISTRY.md`, `DATA_DOWNLOAD_GUIDE.md`, `INGESTION_ROADMAP.md`, `DATA_ACQUISITION_STATUS.md`, `NCO_VALIDATION_REPORT.md` |
| **Phase 5-6 (Canonical + Reconciliation)** | `BACKEND_SCHEMA.md`, `DATA_ARCHITECTURE.md`, `DATA_LINEAGE.md` |
| **Phase 7 (API Read Model)** | `API_SPEC.md`, `ERROR_CATALOG.md` |
| **Phase 8-10 (Intelligence)** | `ML_ARCHITECTURE.md`, `BRAIN.md` (indices), `SCENARIO_ENGINE.md` |
| **Phase 11-13 (Scenario/Optimize/Recommend)** | `SCENARIO_ENGINE.md`, `ARCHITECTURE.md` §3.2 |
| **Phase 14 (Copilot)** | `AI_ARCHITECTURE.md`, `API_SPEC.md` (copilot endpoints) |
| **Phase 15 (UI)** | `UI_UX_BRIEF.md`, `UX_ACCEPTANCE_CRITERIA.md`, `DEMO_SCENARIOS.md` |
| **Phase 16-19 (Perf/Obs/Test/Deploy)** | `OBSERVABILITY.md`, `TEST_STRATEGY.md`, `DEPLOYMENT.md` |

---

## 8. Document Maintenance Rules

1. **Every architectural change** → New ADR in `docs/architecture/`
2. **Every phase completion** → Verification report in `docs/PHASE{X}_VERIFICATION.md`
3. **Every loop iteration** → Entry in `.labrex/ITERATION_LOG.md`
4. **Every task transition** → Update `.labrex/TASK_QUEUE.md`
5. **Every blocker** → Entry in `.labrex/BLOCKERS.md`
6. **Every learning** → Entry in `.labrex/MEMORY.md`
7. **Every decision** → Entry in `.labrex/DECISIONS.md`
8. **Root documents** (README, AGENTS, BRAIN, RULES, LOOP_SPEC) → **Never rewrite**; only append or ADR
9. **Precedence documents** (PRD, TRD, ARCHITECTURE) → **Only via ADR**

---

## 9. Search Index (Keywords → Documents)

| Keyword | Primary Document | Secondary |
|---------|------------------|-----------|
| "Demand Index" | `BRAIN.md` §3.1, `ML_ARCHITECTURE.md` | `BACKEND_SCHEMA.md` |
| "Supply Index" | `BRAIN.md` §3.2 | |
| "Forecast" | `ML_ARCHITECTURE.md`, `AI_ARCHITECTURE.md` | `API_SPEC.md` |
| "Skill Gap" | `BRAIN.md` §3.3, `SCENARIO_ENGINE.md` | |
| "RADAR" | `BRAIN.md` §3.3, `APP_FLOW.md` | |
| "Optimization" | `ARCHITECTURE.md` §3.2, `ADR-0006` | `SCENARIO_ENGINE.md` |
| "Copilot" | `AI_ARCHITECTURE.md`, `ADR-0005` | `API_SPEC.md` |
| "NCO-2015" | `BRAIN.md` §2.2, `DATA_SOURCE_REGISTRY.md` | `NCO_VALIDATION_REPORT.md` |
| "PLFS" | `DATA_SOURCE_REGISTRY.md`, `DATA_DOWNLOAD_GUIDE.md` | |
| "PMKVY" | `DATA_SOURCE_REGISTRY.md`, `BRAIN.md` §2.3 | |
| "e-Shram" | `DATA_SOURCE_REGISTRY.md` (PII guard), `DATA_DOWNLOAD_GUIDE.md` | |
| "PostGIS" | `ADR-0002`, `BACKEND_SCHEMA.md`, `DATABASE_OPERATIONS.md` | |
| "Alembic" | `DATABASE_OPERATIONS.md`, `PHASE3_DATABASE_VERIFICATION.md` | |
| "Walk-forward" | `ML_ARCHITECTURE.md` §3, `RULES.md` §2.3 | |
| "Seasonal Naive" | `ML_ARCHITECTURE.md` §2, `RULES.md` §2.3 | |
| "OR-Tools" | `ADR-0006`, `ARCHITECTURE.md` §3.2 | `SCENARIO_ENGINE.md` |
| "JWT" | `SECURITY.md`, `API_SPEC.md`, `ERROR_CATALOG.md` | |
| "RBAC" | `SECURITY.md`, `THREAT_MODEL.md`, `API_SPEC.md` | |
| "TanStack Query" | `UI_UX_BRIEF.md`, `APP_FLOW.md` | |
| "MapLibre" | `UI_UX_BRIEF.md`, `ARCHITECTURE.md` | |
| "ECharts" | `UI_UX_BRIEF.md`, `APP_FLOW.md` | |
| "Secret Guard" | `RULES.md` §3.1, `scripts/secret_guard.py` | |
| "Maker/Checker" | `AGENTS.md` §2, `RULES.md` §1.4 | |

---

## 10. Changelog

| Date | Version | Changes | Author |
|------|---------|---------|--------|
| 2026-11-04 | 1.0 | Initial creation; all 31 docs indexed; precedence hierarchy defined | Principal Engineering Agent |

---

**End of Document Index**