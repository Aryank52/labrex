# LABREX Master Task Roadmap

**Status:** Initialized (Phase 0 Complete)  
**Governing Document:** Master Directive Section 89 & 90  
**Machine-Readable Queue:** `.labrex/TASK_QUEUE.md`  

---

## Phase Overview & Progress Summary

| Phase | Title | Scope & Key Deliverables | Status |
| :---: | :--- | :--- | :---: |
| **0** | **Environment Discovery** | Environment inventory, capability matrix, tooling constraints | **DONE** |
| **1** | **Project Constitution & Architecture** | PRD, TRD, ARCHITECTURE, Data/ML specs, ADRs, Loop spec | **IN_PROGRESS** (Active) |
| **2** | **Repository Foundation & Scaffold** | Backend/frontend scaffold, Docker, CI, secret guard, environment setup | **READY** |
| **3** | **Database Foundation** | PostgreSQL + PostGIS migrations, core dimensional models, seeders | TODO |
| **4** | **Data Foundation & Pipelines** | Ingestion framework, Bronze/Silver/Gold layers, data quality engine | TODO |
| **5** | **Ontology & Knowledge Graph** | NCO-2015, NSQF, Skill taxonomy, embeddings, relational graph | TODO |
| **6** | **Demand & Supply Engines** | Feature pipelines, Demand Index (0–100), Supply Index (0–100) | TODO |
| **7** | **Forecasting Engine** | Walk-forward validation, Seasonal Naive, XGBoost/LGBM, TimesFM-3, uncertainty | TODO |
| **8** | **Skill-Gap Intelligence & Radar** | Gap computation, LABREX RADAR early warnings, skill shock detection | TODO |
| **9** | **Scenario Simulation Engine** | Counterfactual simulator, capacity shifts, macro demand/supply shocks | TODO |
| **10** | **Policy Optimization Engine** | Google OR-Tools MILP budget allocation, explainable recommendations | TODO |
| **11** | **Backend API & Security** | FastAPI endpoints, RBAC, rate limiting, audit logging, error catalog | TODO |
| **12** | **Frontend Intelligence Platform** | Next.js 15, India Skill Map, Forecast Studio, Radar, Scenario Studio | TODO |
| **13** | **AI Policy Copilot** | Gemini 3.8 tool calling, RAG knowledge retrieval, injection defense | TODO |
| **14** | **Security Hardening** | Threat model mitigations, secret scanner, vulnerability audit, fuzzing | TODO |
| **15** | **Performance & Scalability** | Query optimization, caching, frontend bundle size, P95 latency | TODO |
| **16** | **Production Deployment** | Multi-stage Docker, Cloud Run manifests, Cloud SQL, Cloud Scheduler | TODO |
| **17** | **System Acceptance** | Full regression, browser E2E verification, model validation suite | TODO |
| **18** | **Product Polish** | WCAG accessibility, micro-interactions, dark/light theme, demo scenarios | TODO |
| **19** | **Final Hardening & Release** | Final audit, release checklist, documentation signoff | TODO |

---

## Active Phase Details: Phase 0 & 1

### Phase 0: Environment Discovery
- [x] **TASK-001**: Inspect host environment (Python, Node, PostgreSQL, Git, tools)
- [x] **TASK-002**: Generate `docs/ENVIRONMENT_INVENTORY.md`
- [x] **TASK-003**: Generate `docs/ANTIGRAVITY_CAPABILITY_MATRIX.md`

### Phase 1: Project Constitution & Architecture
- [x] **TASK-004**: Author root governance documents (`README.md`, `AGENTS.md`, `BRAIN.md`, `MEMORY.md`, `TASKS.md`, `RULES.md`, `ERROR_CATALOG.md`)
- [ ] **TASK-005**: Author comprehensive product & technical documentation in `docs/` (`PRD.md`, `TRD.md`, `ARCHITECTURE.md`, `API_SPEC.md`, etc.)
- [ ] **TASK-006**: Create loop specification and state files in `.labrex/` (`LOOP_SPEC.md`, `LOOP_STATE.md`, `TASK_QUEUE.md`, etc.)
- [ ] **TASK-007**: Record initial Architecture Decision Records (ADRs 0001 through 0007)
- [ ] **TASK-008**: Scaffold repository structure (`backend/`, `frontend/`, `scripts/`, `Dockerfile.*`, `docker-compose.yml`, `.env.example`)
- [ ] **TASK-009**: Validate scaffold (Python syntax, secret guard, git initialization, tests)
- [ ] **TASK-010**: Generate `docs/PHASE0_INITIALIZATION_REPORT.md` and complete loop initialization
