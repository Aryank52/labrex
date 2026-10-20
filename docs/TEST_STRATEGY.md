# LABREX Master Test Strategy

**Document Version:** 1.0  
**Authority:** Master Directive Section 76  
**Quality Rule:** No feature is complete without the corresponding automated tests.  

---

## 1. The 10 Test Levels

```
+--------------------------------------------------------------------------------------------------+
|                                      LABREX TEST PYRAMID                                         |
+-----+----------------------+------------------------------+--------------------------------------+
| LVL | TEST TYPE            | FRAMEWORK / RUNTIME          | TARGET SCOPE & OBJECTIVE             |
+-----+----------------------+------------------------------+--------------------------------------+
| 1   | Unit Tests           | pytest (Python), Vitest (TS) | Domain logic, index math, schemas    |
| 2   | Integration Tests    | pytest-asyncio, httpx        | API endpoints with real database     |
| 3   | Data Quality Tests   | Custom Ingestion Validators  | Completeness, schema types, z-scores |
| 4   | ML Evaluation Tests  | Scikit-learn, Walk-forward   | Baseline benchmark, leakage check    |
| 5   | API Contract Tests   | Pydantic v2 & OpenAPI check  | Request/response schema alignment    |
| 6   | Security Tests       | pytest-security, secret_guard| RBAC, prompt injection, SQLi, SSRF   |
| 7   | Browser E2E Tests    | Chrome DevTools Subagent     | Real browser render, map, UX states  |
| 8   | Performance Tests    | Locust / Python httpx bench  | P95 latency budgets (< 350ms)        |
| 9   | Regression Tests     | Full Pytest Suite            | Pre-merge regression across phases   |
| 10  | Acceptance Tests     | Scenario verification suite  | 7 Deterministic Demo Scenarios       |
+-----+----------------------+------------------------------+--------------------------------------+
```

---

## 2. Test Execution Commands & Automation

- **Fast Unit & Security Tests**:
  ```bash
  pytest backend/tests/unit/ backend/tests/security/ -v
  ```
- **Integration Tests (Database Required)**:
  ```bash
  pytest backend/tests/integration/ -v
  ```
- **ML Benchmark Suite**:
  ```bash
  python -m backend.app.services.forecasting.benchmark_runner
  ```
- **Secret Guard Scanner**:
  ```bash
  python scripts/secret_guard.py
  ```
- **Browser E2E Verification**:
  Invoked via `browser_subagent` using Chrome DevTools MCP tools inspecting DOM, network requests, and console errors.
