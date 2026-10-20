# LABREX Production Deployment & Cloud Architecture

**Document Version:** 1.0  
**Authority:** Master Directive Section 81, 82 & 83  
**Target Infrastructure:** Google Cloud Platform (Cloud Run, Cloud SQL, BigQuery, Cloud Storage)  

---

## 1. Cloud Infrastructure Topology

```
+--------------------------------------------------------------------------------------------------+
|                                    GOOGLE CLOUD ARCHITECTURE                                     |
+--------------------------------------------------------------------------------------------------+
| CLOUD LOAD BALANCING (HTTPS / Managed SSL / Cloud Armor WAF / DDoS Protection)                  |
+--------------------------------------------------------------------------------------------------+
                                        │
                    ┌───────────────────┴───────────────────┐
                    ▼                                       ▼
+---------------------------------------+   +---------------------------------------+
| FRONTEND: Cloud Run Service           |   | BACKEND API: Cloud Run Service        |
| - Container: Next.js 15 SSR Node.js   |   | - Container: Python 3.12 FastAPI/Uvicorn
| - Autoscaling: 1 to 10 instances      |   | - Autoscaling: 1 to 20 instances      |
| - Min Instances: 1 (zero cold start)  |   | - Concurrency: 80 requests/instance   |
+---------------------------------------+   +---------------------------------------+
                                                            │
                                                            ▼ (Serverless VPC Access)
                                            +---------------------------------------+
                                            | MANAGED STORAGE & COMPUTE             |
                                            | - Cloud SQL PostgreSQL 16 + PostGIS   |
                                            | - BigQuery Analytical Data Warehouse  |
                                            | - Cloud Storage (Model & PDF artifacts)|
                                            | - Secret Manager (API Keys & JWT)     |
                                            | - Cloud Scheduler (Nightly jobs)      |
                                            +---------------------------------------+
```

---

## 2. Environment Management Matrix

| Setting / Resource | LOCAL (Host Dev) | STAGING (GCP) | PRODUCTION (GCP) |
| :--- | :--- | :--- | :--- |
| **API Host** | `http://localhost:8000` | `https://api.staging.labrex.in` | `https://api.labrex.in` |
| **Web Host** | `http://localhost:3000` | `https://staging.labrex.in` | `https://labrex.in` |
| **Database** | Native PostgreSQL 16.15 | Cloud SQL (db-custom-2-7680) | Cloud SQL (db-custom-4-15360) + Replica |
| **Secrets Engine**| `.env` file (Git-ignored) | Google Secret Manager | Google Secret Manager |
| **Data Engine** | Local PostgreSQL + Parquet | BigQuery Staging Dataset | BigQuery Production Dataset |

---

## 3. CI/CD GitHub Actions Pipeline

1. **Pull Request Workflow (`pr.yml`)**:
   - Python code format & linting (`ruff`, `mypy`).
   - Secret scan via `scripts/secret_guard.py`.
   - Unit and integration tests (`pytest`).
   - Frontend TypeScript typecheck (`tsc --noEmit`) and production build.
2. **Main Branch Promotion Workflow (`deploy.yml`)**:
   - Build multi-stage Docker images (`Dockerfile.backend`, `Dockerfile.frontend`).
   - Push to Google Artifact Registry.
   - Run database migrations via Cloud Run job (`alembic upgrade head`).
   - Deploy backend and frontend containers to Cloud Run with zero-downtime traffic migration.
   - Run post-deploy smoke health checks (`/health/ready`).
