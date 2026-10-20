# LABREX Technical Requirements Document (TRD)

**Document Version:** 1.0  
**Status:** Approved  
**Classification:** Technical Architecture & Specifications  

---

## 1. System Architecture Overview

LABREX is architected as a **High-Performance Modular Monolith** coupled with asynchronous analytical/ML batch workers. This design eliminates microservice overhead, distributed network latency, and transactional fragmentation while enforcing clean domain separation.

```
+--------------------------------------------------------------------------------------------------+
|                                  LABREX TECHNICAL TOPOLOGY                                       |
+--------------------------------------------------------------------------------------------------+
| FRONTEND WORKSPACE (Next.js 15 App Router, React 19, TypeScript, Tailwind, ECharts, MapLibre)    |
|   └── Client-side state (TanStack Query, Zustand)                                                |
|   └── Server-side rendering (SSR) for initial data-dense executive views                         |
+--------------------------------------------------------------------------------------------------+
                                        │ (HTTPS / JSON REST / WSS)
                                        ▼
+--------------------------------------------------------------------------------------------------+
| BACKEND MODULAR MONOLITH (Python 3.12, FastAPI, Pydantic v2, SQLAlchemy 2 Async)                 |
|   ├── /api/v1/ Route Controllers (Auth, Geography, Forecasts, Gaps, Scenarios, Optimizer, Copilot)|
|   ├── Domain Services Layer (Stateless analytical & policy business logic)                       |
|   ├── Repository Layer (Async PostgreSQL & BigQuery data abstractions)                           |
|   └── Core Security (RBAC, Rate Limiting, Audit Logger, Input Sanitizers)                        |
+--------------------------------------------------------------------------------------------------+
           │                                 │                                 │
           ▼                                 ▼                                 ▼
+----------------------+         +-----------------------+         +-----------------------+
| RELATIONAL & SPATIAL |         | ANALYTICAL WAREHOUSE  |         | AI & ML ENGINES       |
| PostgreSQL 16.15     |         | BigQuery (or local    |         | Scikit-learn, XGBoost |
| + PostGIS (GeoJSON)  |         | Parquet/Polars)       |         | TimesFM-3, OR-Tools   |
| + pgvector           |         | Historical Panels     |         | Gemini 3.8 Tool Calls |
+----------------------+         +-----------------------+         +-----------------------+
```

---

## 2. Component Specifications

### 2.1 Backend Platform (FastAPI + Python 3.12)
- **ASGI Server**: Uvicorn running with uvloop and httptools.
- **Data Validation & Serialization**: Pydantic v2 with strict type coercion.
- **Database Driver**: `asyncpg` with SQLAlchemy 2.0 async engine and session factory. Connection pooling tuned for max 20 concurrent connections with automatic pre-ping.
- **Synchronous ML & Numerical Stack**: NumPy 2.0, SciPy 1.18, Pandas 3.0, Scikit-learn 1.9, XGBoost 3.4, Google OR-Tools.

### 2.2 Relational & Spatial Database (PostgreSQL 16 + PostGIS)
- **Engine**: PostgreSQL 16.15 with spatial extensions (`postgis`, `postgis_topology`).
- **Spatial Reference System**: EPSG:4326 (WGS 84) storage, EPSG:3857 for web tile calculations.
- **Vector Search**: `pgvector` extension for semantic embedding lookups of occupation descriptions and qualification text.
- **Migration Framework**: Alembic with versioned, reversible migration scripts.

### 2.3 Optimization Solver (Google OR-Tools)
- **Engine**: Google OR-Tools Linear Solver (`CBC_MIXED_INTEGER_PROGRAMMING`) and Constraint Programming Solver (`CP-SAT`).
- **Execution Budget**: Maximum solve timeout set to 5.0 seconds. If optimal is not reached, the solver returns the best feasible bound with an optimality gap metric.

### 2.4 Frontend Application (Next.js 15)
- **Runtime**: Node.js v24.16.0 with TypeScript strict mode enabled.
- **Framework**: Next.js 15 (App Router) with React 19.
- **Styling**: Tailwind CSS with custom CSS variables for light/dark themes, strict data density, and WCAG AA contrast.
- **Visualization**: Apache ECharts for time-series charts, radar charts, and confidence bands; MapLibre GL for high-performance vector/GeoJSON district map interactions.

---

## 3. Communication Protocols & Contracts

1. **REST API**:
   - URL Namespace: `/api/v1/`
   - Content Type: `application/json; charset=utf-8`
   - Error Handling: Standard RFC 7807 problem details schema as defined in `ERROR_CATALOG.md`.
2. **Authentication & Authorization**:
   - Bearer Token: Signed JWT (JSON Web Token) with RS256 / HS256 algorithm.
   - Claims: `sub` (User UUID), `role` (Role Enum), `jurisdiction` (State/District scope), `exp` (Expiry).
3. **Audit Trail**:
   - Every mutating request logs `timestamp`, `user_id`, `action`, `resource`, `ip_address`, and `change_summary` to table `audit_logs`.

---

## 4. Hardware & Scaling Profiles

| Environment | CPU Allocation | Memory Allocation | Database Tier | Target Concurrency |
| :--- | :---: | :---: | :---: | :---: |
| **Local Development** | Host Native | Host RAM | Local PostgreSQL 16 | 1–5 developers |
| **Staging (Cloud Run)** | 2 vCPU | 4 GB RAM | Cloud SQL (db-custom-2-7680) | 50 concurrent planners |
| **Production (Cloud Run)** | 4 vCPU (Autoscale 2–20) | 8 GB RAM | Cloud SQL (db-custom-4-15360) + Read Replica | 500+ concurrent users |
