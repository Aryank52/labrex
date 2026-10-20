# LABREX Engineering Decisions Log

**Maintained By:** Principal Engineering Agent  

---

| Decision ID | Date | Topic | Summary of Decision | Primary Rationale | Reference |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `DEC-001` | 2026-10-20 | Runtime Invocations | Use `.cmd` wrappers for Node/npm in PowerShell | Host execution policy restricts `.ps1` execution | `MEMORY.md` |
| `DEC-002` | 2026-10-20 | Monorepo Structure | Colocate `backend/` and `frontend/` in single repo | Eliminates contract drift; single source of truth | `ARCHITECTURE.md` |
| `DEC-003` | 2026-10-20 | Database Target | Use local PostgreSQL 16.15 service directly | Service is already running locally on host at port 5432 | `ENVIRONMENT_INVENTORY.md` |
| `DEC-004` | 2026-10-20 | Fixture Policy | Deterministic seed generator for demo data | Ensures test reproducibility without fabricating data | `DATA_SOURCE_REGISTRY.md` |
