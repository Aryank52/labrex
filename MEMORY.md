# LABREX Persistent Memory & Operational Learnings

**Maintained By:** Principal Engineering Agent  
**Last Updated:** 2026-10-20  

---

## 1. Host Environment Nuances

1. **PowerShell Script Execution**:
   - The default Execution Policy on the Windows host is `Undefined` (effectively `Restricted`), blocking `.ps1` execution.
   - **Operational Rule**: Always invoke Node CLI commands using `.cmd` extensions (e.g. `npm.cmd`, `npx.cmd`) or via `cmd /c`. For Python virtual environments, use `python -m venv` and invoke `python` directly or run commands in subshells.
2. **PostgreSQL Installation**:
   - Service name: `postgresql-x64-16`. Status: **RUNNING**.
   - Binary location: `E:\postsql database\bin\` (includes `psql.exe`, `pg_ctl.exe`).
   - Default port: 5432.
   - For database management and migrations, connect directly to `localhost:5432`.
3. **Python Environment**:
   - Python 3.12.10 is installed at `C:\Users\HP\AppData\Local\Programs\Python\Python312\python.exe`.
   - Core libraries already installed: FastAPI 0.141+, SQLAlchemy 2.1+, Alembic 1.20+, Scikit-Learn 1.9+, XGBoost 3.4+, SHAP 0.52+, GeoAlchemy2, Shapely, Pytest 9.1+, ReportLab 5.0+.
4. **Antigravity Tooling**:
   - `chrome-devtools-mcp` and `browser_subagent` are fully functional and must be used for browser validation of frontend components.
   - System protection boundaries exist on `C:\Users\HP\.gemini\config`; access capabilities via published schemas and MCP tools.

---

## 2. Architectural Guidelines & Decisions

1. **Monorepo Structure**: Keep backend and frontend co-located in `backend/` and `frontend/` to allow unified CI/CD, shared contract synchronization, and end-to-end integration tests.
2. **No-Pretending Ingestion**: When external public APIs (such as NCS or e-Shram) lack live authorization tokens during local runs, mark datasets as `DEMO_FIXTURE` or `NOT_CONFIGURED`. Never fabricate data points to mimic live feeds.
3. **Walk-Forward Validation**: Never use random `train_test_split` on temporal labour-market series. Always use chronological walk-forward splits with a baseline Seasonal Naive benchmark.
4. **Tool-Gated AI**: Gemini interactions must always pass through Pydantic-validated tool schemas. The LLM produces explanations, recommendations, and summaries, but numerical indicators must originate from database queries or analytical calculations.

---

## 3. Recurring Patterns & Solutions

- **Pattern: Type Safety between FastAPI and Next.js**:
  All API schemas must be defined in Pydantic v2 in `backend/app/schemas/`. Use OpenAPI export (`openapi.json`) to keep frontend TypeScript interfaces aligned.
- **Pattern: Geographic Boundaries**:
  Store boundaries as GeoJSON in PostGIS. For map tiles, serve pre-simplified GeoJSON or vector tiles to prevent frontend rendering lag.
- **Pattern: Secret Management**:
  Use `scripts/secret_guard.py` before git commits to prevent accidental leakage of database credentials or API keys.
