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
