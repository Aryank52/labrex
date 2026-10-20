# LABREX Standard Error Catalog

**Authoritative Standard:** Directive Section 40  
**Version:** 1.0  
**Format:** All API error responses adhere to RFC 7807 (Problem Details for HTTP APIs).  

---

## 1. Error Response Contract

Every error returned by the LABREX API has the following standardized JSON schema:

```json
{
  "error_code": "STRING_ENUM",
  "message": "Human-readable description of what failed",
  "details": {},
  "timestamp": "2026-10-20T10:00:00Z",
  "request_id": "req-uuid-v4",
  "status_code": 400
}
```

---

## 2. Standardized Error Catalog

| Error Code | HTTP Status | Domain | Description & Remedy |
| :--- | :---: | :--- | :--- |
| `DATA_SOURCE_UNAVAILABLE` | 503 | Data Ingestion | External data source connection failed or upstream provider returned error. Check source health and fallback to cached snapshot. |
| `DATA_SCHEMA_INVALID` | 422 | Data Quality | Ingested or submitted dataset failed schema or type validation. Inspect schema mismatch report in details. |
| `DATA_MAPPING_FAILURE` | 422 | Ontology | Occupation title or skill text could not be resolved to canonical NCO/NSQF codes above confidence threshold. |
| `INSUFFICIENT_HISTORY` | 400 | Forecasting | Time series lacks minimum required historical points (minimum 12 months) for walk-forward forecasting. |
| `FORECAST_UNAVAILABLE` | 503 | Forecasting | Selected model champion has not been trained or inference failed. Check model registry state. |
| `MODEL_NOT_READY` | 503 | Modeling | Requested model is currently undergoing training or evaluation. Status is `CANDIDATE`, not `CHAMPION`. |
| `OPTIMIZATION_INFEASIBLE` | 422 | Policy Optimization | The optimization problem has no feasible solution under the specified budget, capacity, or equity constraints. Details contain constraint conflict report. |
| `SCENARIO_INVALID` | 400 | Simulation | The scenario parameters (e.g. negative seat shifts or out-of-range percentage shocks) are mathematically invalid. |
| `UNAUTHORIZED` | 401 | Security / Auth | Authentication credentials missing, expired, or malformed. Re-authenticate via OIDC/OAuth bearer token. |
| `FORBIDDEN` | 403 | Security / RBAC | Authenticated user lacks required permission or is attempting to access state/district data outside assigned jurisdiction. |
| `RATE_LIMITED` | 429 | Traffic Control | Request rate exceeded tier threshold. Header `Retry-After` specifies cooldown duration in seconds. |
| `VALIDATION_FAILED` | 422 | Input Guard | Request body, query parameter, or file upload violated Pydantic validation rules. |
| `UPSTREAM_TIMEOUT` | 504 | System | Internal worker or external API failed to respond within service timeout budget. |
| `DATABASE_UNAVAILABLE` | 503 | Infrastructure | PostgreSQL database connection pool exhausted or database unreachable. |
| `LLM_UNAVAILABLE` | 503 | AI Copilot | Gemini API unreachable, quota exhausted, or response timeout. Copilot enters graceful degraded mode. |
| `RAG_UNAVAILABLE` | 503 | AI Copilot | Vector search / pgvector document retrieval index unavailable. Copilot falls back to deterministic rule lookup. |
| `EXPORT_FAILED` | 500 | Reporting | Report generation engine (PDF/CSV/JSON) encountered an error during serialization or rendering. |

---

## 3. Production Error Handling Rules

1. **No Stack Traces in Production**: Internal exceptions, tracebacks, and database connection strings are logged internally to structured logs with `request_id` but never exposed to the client.
2. **Deterministic Error Codes**: Frontends and automated agents must key logic off `error_code`, never parsing the English text of `message`.
3. **Safe Failure Modes**: When forecasting or optimization fails due to data or constraint limits, the API returns a structured explanation with actionable remediation steps.
