# LABREX — Labour Market Intelligence & Policy Optimization Platform

[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.141+-009688.svg)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-336791.svg)](https://www.postgresql.org/)
[![Next.js](https://img.shields.io/badge/Next.js-15-black.svg)](https://nextjs.org/)
[![License](https://img.shields.io/badge/license-Proprietary-red.svg)]()

> **"From labour-market signals to optimized skilling action."**

LABREX is an enterprise-grade, evidence-backed labour-market intelligence, workforce forecasting, skill-gap analysis, and policy optimization platform. It bridges the critical divide between raw market signals and national/state-level skilling decisions.

---

## 1. What LABREX Solves

Governments, sector skill councils, and educational authorities routinely face fragmented datasets: job posting frequencies, survey samples (e.g. PLFS), training completions (e.g. PMKVY), and informal sector registries (e.g. e-Shram). Traditional dashboards merely plot historical counts with no predictive capability, no causal explanation, and no actionable optimization.

LABREX connects the complete intelligence chain:

```
[RAW DATA SIGNALS]
       │
       ▼
[STANDARDIZED ONTOLOGY] (NCO-2015, NSQF, Canonical Skills)
       │
       ▼
[INTELLIGENCE & INDICES] (Demand Index, Supply Index 0–100)
       │
       ▼
[CHAMPION FORECASTING] (Walk-Forward ML, Uncertainty Bands)
       │
       ▼
[SKILL-GAP & RADAR] (Critical Shortages, Oversupply, Shocks)
       │
       ▼
[CONSTRAINED OPTIMIZER] (Google OR-Tools MILP Budget Allocation)
       │
       ▼
[GROUNDED AI COPILOT] (Strict Tool-Gated Evidence Synthesis)
```

---

## 2. Core Pillars & Capabilities

1. **National Skill Knowledge Graph**: Authoritative mapping connecting Occupations (NCO), Skills, Qualifications, NSQF levels, Training Programs, Centres, and Districts.
2. **Standardized Indices**: Methodologically transparent **Demand Index (0–100)** and **Supply Index (0–100)** with versioned formulas.
3. **Champion-vs-Challenger Forecasting**: Rigorous walk-forward validation comparing Seasonal Naive baselines, LightGBM/XGBoost, and candidate deep models (e.g. TimesFM). No guessing, no temporal leakage.
4. **LABREX RADAR**: Early warning detection for emerging shortages, sudden demand shocks, and persistent supply bottlenecks.
5. **Constrained Policy Optimizer**: Solves mixed-integer linear programming (MILP) models using Google OR-Tools to maximize skill deficit reduction under budgetary and training-capacity constraints.
6. **Strictly Grounded Copilot**: AI copilot using the Gemini API strictly bounded by typed tools. The LLM summarizes and explains verified results; it cannot fabricate statistics.
7. **End-to-End Auditability**: Complete data lineage and model provenance recorded from raw ingestion to policy recommendation.

---

## 3. Technology Stack

- **Backend**: Python 3.12, FastAPI, Pydantic v2, SQLAlchemy 2, Alembic, Polars/Pandas.
- **Database**: PostgreSQL 16 + PostGIS for spatial queries and PostGIS geometry.
- **Machine Learning & Optimization**: Scikit-Learn, XGBoost, SHAP, Google OR-Tools.
- **Frontend**: Next.js (App Router), React 19, TypeScript, Tailwind CSS, shadcn/ui, Apache ECharts, MapLibre GL.
- **Security & Quality**: Pytest, secret guard scanner, role-based access control (RBAC), and Chrome DevTools verification.

---

## 4. Repository Structure

```
├── .labrex/                  # Persistent loop state, task queue & memory
│   ├── LOOP_SPEC.md          # Autonomous loop specification
│   ├── LOOP_STATE.md         # Current state of the development loop
│   ├── TASK_QUEUE.md         # Granular tasks and completion criteria
│   ├── ITERATION_LOG.md      # Chronological engineering log
│   └── MEMORY.md             # Persistent engineering learnings
├── backend/                  # FastAPI modular monolith backend
│   ├── app/
│   │   ├── api/v1/           # Versioned API routes
│   │   ├── core/             # Database, security, and logging config
│   │   ├── models/           # SQLAlchemy ORM models
│   │   ├── schemas/          # Pydantic v2 validation contracts
│   │   ├── services/         # Domain services (demand, supply, ML, etc.)
│   │   └── repositories/     # Data access layer
│   ├── tests/                # Pytest unit and integration test suite
│   ├── requirements.txt      # Pinned Python dependencies
│   └── pyproject.toml        # Backend configuration
├── frontend/                 # Next.js TypeScript frontend workspace
│   ├── src/
│   │   ├── app/              # Next.js App Router pages
│   │   ├── components/       # UI components & charts
│   │   └── lib/              # API clients & utilities
│   ├── package.json          # Frontend dependencies
│   └── tsconfig.json         # TypeScript configuration
├── docs/                     # Authoritative engineering documentation
│   ├── PRD.md                # Product Requirements Document
│   ├── TRD.md                # Technical Requirements Document
│   ├── ARCHITECTURE.md       # System Architecture
│   ├── API_SPEC.md           # API Specifications
│   ├── THREAT_MODEL.md       # Security & Threat Model
│   └── ...                   # Complete documentation suite
├── scripts/                  # Utility and security automation
│   └── secret_guard.py       # Pre-commit secret scanning engine
├── Dockerfile.backend        # Multi-stage production container for API
├── Dockerfile.frontend       # Production container for Next.js web
├── docker-compose.yml        # Local orchestration manifest
└── .env.example              # Centralized environment template
```

---

## 5. Getting Started (Local Development)

### Prerequisites
- Python 3.12+
- Node.js v20+ / v24+
- PostgreSQL 16+ running locally or via container

### Backend Setup
```bash
# 1. Create and activate virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1

# 2. Install dependencies
pip install -r backend/requirements.txt

# 3. Configure environment
cp .env.example .env
# Edit .env with your local PostgreSQL credentials

# 4. Run tests
pytest backend/tests/
```

### Frontend Setup
```bash
cd frontend
npm.cmd install
npm.cmd run build
```

---

## 6. Development Philosophy & Governance

LABREX adheres to strict engineering rules:
- **No-Pretending**: Never display fake confidence scores, fabricated numbers, or imaginary API integrations.
- **Maker-Checker Separation**: Implementation is independently reviewed and verified with machine-checkable tests.
- **Traceable Lineage**: Every insight must cite its underlying dataset version and methodology.
