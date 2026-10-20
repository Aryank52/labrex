# LABREX Antigravity Capability Matrix

**Classification Standard:** Directive Section 2  
**Updated:** 2026-10-20  
**Authority:** Principal Engineering Agent  

---

## 1. Capability Classification Summary

| Capability / Toolset | Discovery Status | LABREX Tier | Justification & Architectural Role |
| :--- | :--- | :--- | :--- |
| **Python 3.12 + Scientific Stack** | Installed & Verified | **ESSENTIAL** | Core runtime for FastAPI backend, ML models (Scikit-Learn, XGBoost), feature engineering, and optimization solvers. |
| **PostgreSQL 16.15 (Local Service)** | Running on Host | **ESSENTIAL** | Primary transactional and analytical relational store with PostGIS geometry support and pgvector embeddings. |
| **Node.js v24 + npm.cmd** | Installed & Verified | **ESSENTIAL** | Modern frontend execution runtime for Next.js, React 19, TypeScript, Tailwind CSS, and ECharts dashboards. |
| **Chrome DevTools & Browser Subagent** | Installed & Available | **ESSENTIAL** | Real-world E2E verification of frontend rendering, map interactions, data density, console errors, and WCAG accessibility. |
| **Git SCM** | Installed & Verified | **ESSENTIAL** | Version control, atomic commits, branch protection, reproducible history, and change tracking. |
| **Security & Secret Scanning** | Custom Script (`secret_guard`) | **ESSENTIAL** | Mandatory pre-commit verification ensuring zero secrets or API tokens leak into Git or logs. |
| **Gemini API & Structured Outputs** | Global Plugin Available | **ESSENTIAL** | LABREX Copilot natural language interface, tool routing, structured decision synthesis, and grounded explanation generation. |
| **Modern Web Guidance Plugin** | Global Plugin Available | **ESSENTIAL** | Enforces rich UI aesthetics, modern typography, high data density, zero-generic design, and WCAG accessibility. |
| **Data Agent Kit (BigQuery, GCS)** | Global Plugin Available | **RECOMMENDED** | Cloud analytical warehouse layer for historical national data panels and large-scale model evaluation. |
| **Google Maps Platform** | Global Plugin Available | **RECOMMENDED** | Geocoding and geographic boundary mapping across India's states and districts. |
| **Gemini API Docs MCP** | MCP Server Active | **RECOMMENDED** | Real-time upstream SDK schema validation and type-safe tool declaration. |
| **Firebase Plugin** | Global Plugin Available | **OPTIONAL** | Scoped strictly to optional hosting or push notifications if explicitly required. Not used in core data loops. |
| **Science & Biomedical Plugins** | Global Plugin Available | **IRRELEVANT** | Biomolecular and genomic skills (AlphaFold, ChEMBL, PDB) are irrelevant to labour-market and workforce intelligence. |
| **Docker Engine (Local Host)** | Not in Host PATH | **UNAVAILABLE** (Locally) | Container manifests (`Dockerfile.*`, `docker-compose.yml`) will be provided and validated for Cloud Run / remote CI without blocking local execution. |
| **Cloud CLIs (`gcloud`, `gh`)** | Not in Host PATH | **UNAVAILABLE** (Locally) | Local development relies on environment variables (`.env`) and local DB; cloud deployment uses GitHub Actions and Terraform templates. |

---

## 2. Architectural Boundaries & Domain Authority

To prevent redundant tools and overlapping logic, LABREX enforces a single authoritative capability per domain:

```
+----------------------------------------------------------------------------------+
|                               LABREX DOMAIN MATRIX                               |
+----------------------------------------------------------------------------------+
| DOMAIN               | AUTHORITATIVE TOOLSET            | STRICT EXCLUSION       |
+----------------------+----------------------------------+------------------------+
| Frontend Web UI      | Next.js, React, Tailwind, ECharts| Static HTML / Streamlit|
| Backend API          | Python 3.12, FastAPI, Pydantic v2| Express / Django / Flask|
| Relational Storage   | PostgreSQL 16 + PostGIS          | SQLite / Mongo / Prisma|
| Time-Series Forecast | Walk-forward ML (LGBM/XGB/TimesFM)| Arbitrary LLM guessing |
| Policy Optimization  | Google OR-Tools (MILP/CP-SAT)    | Heuristic unconstrained|
| Copilot Reasoning    | Gemini API with Strict Tool Gates| Unbounded chat / no-SQL|
| Browser Verification | Chrome DevTools Subagent         | Mock-only unit tests   |
+----------------------+----------------------------------+------------------------+
```

---

## 3. Implementation Policy for Optional / Unavailable Tools

1. **Docker**: While Docker daemon is absent on this local Windows machine, production Dockerfiles and a `docker-compose.yml` defining `web`, `api`, and `db` will be maintained in the repo root and verified for syntactic and build correctness.
2. **Cloud Services (BigQuery, Cloud Storage)**: Development mode operates fully on PostgreSQL 16. A clean storage abstraction layer (`app/services/data/storage_adapter.py`) allows seamless switching between local file storage and Cloud Storage / BigQuery.
3. **No Redundant Plugins**: We explicitly reject introducing experimental or unverified plugins that do not have a defined role in the LABREX PRD.
