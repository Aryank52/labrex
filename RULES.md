# LABREX Engineering & Architectural Rules

**Authoritative Standard:** Master Project Directive  
**Compliance Level:** MANDATORY — Zero Exceptions  
**Enforced By:** Principal Engineering Agent & Automated Verification Suites  

---

## 1. Core Engineering Discipline

1. **Understand Before Changing**: Always inspect existing schemas, code, and dependencies before modifying or generating code.
2. **Persistent Loop Engineering**: Follow the continuous cycle: `DISCOVER -> PLAN -> IMPLEMENT -> RUN -> TEST -> OBSERVE -> DIAGNOSE -> FIX -> RETEST -> VERIFY -> REVIEW -> DOCUMENT -> COMMIT`.
3. **No-Pretending Rule**:
   - Never claim a component is "implemented", "real-time", or "verified" without automated proof.
   - Never display hardcoded statistics or fake confidence percentages.
   - Every metric must be computable from data fixtures or active models.
4. **Maker/Checker Separation**: Code written by the Maker role must be reviewed and validated against acceptance tests by independent checker roles before completion.

---

## 2. Data & Model Governance

1. **Layer Separation**: Strictly isolate `RAW -> BRONZE -> SILVER -> GOLD -> FEATURE -> MODEL -> SERVING`. Never bypass layers.
2. **Synthetic Data Tagging**: Any fixture or mock data must be explicitly flagged with `dataset_type = 'SYNTHETIC'` or `'DEMO_FIXTURE'`.
3. **Time-Series Integrity**:
   - Never use random train/test splits for temporal forecasting.
   - Always apply chronological walk-forward splits.
   - Every model must be evaluated against a Seasonal Naive baseline.
4. **Uncertainty & Disagreement**:
   - Forecasts must output lower and upper prediction intervals (e.g. 80% and 95%).
   - Model dispersion (disagreement between baseline, GBDT, and deep models) must be explicitly quantified.

---

## 3. Security & Operational Boundaries

1. **Zero Secret Leakage**:
   - No passwords, connection strings, API keys, or JWT secrets may be committed to version control.
   - The pre-commit scanner `scripts/secret_guard.py` must run and pass cleanly.
2. **AI Copilot Sandboxing**:
   - The Copilot is an explainer and router, not the analytical source of truth.
   - All Copilot actions must execute through strictly typed Pydantic tools.
   - Absolutely no dynamic or raw SQL generation from LLM inputs.
   - User inputs and retrieved text must be sanitized against prompt injection.
3. **Destructive Action Gates**:
   - No automatic dropping of databases, force-pushing, or mass deletion of resources.
   - Explicit confirmation is mandatory for destructive commands.

---

## 4. Code Quality & Standards

1. **Backend**:
   - Python 3.12 with strict type hints (`typing`, `Pydantic v2`).
   - Domain logic must reside in `services/`, never in route controllers (`api/`).
   - All database access must use SQLAlchemy 2.0 async sessions and repository patterns.
2. **Frontend**:
   - Next.js 15 App Router with TypeScript.
   - Styling via Tailwind CSS following high data density and clean policy-intelligence aesthetics.
   - Zero console errors; full WCAG-oriented keyboard and screen-reader accessibility.
3. **Documentation**:
   - Any architectural deviation must be recorded in an Architecture Decision Record (`docs/architecture/ADR-*.md`).
