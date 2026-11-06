# LABREX Error Catalog (RFC 7807 Compliant)

**Document Version:** 1.0  
**Authority:** Master Directive Section 12, 38, 82  
**Standard:** RFC 7807 Problem Details for HTTP APIs  
**Machine-Readable:** Yes (YAML front-matter + Markdown table)

---

## 1. Error Code Registry

Each error is uniquely identified by a machine-readable `error_code` (SCREAMING_SNAKE_CASE), mapped to HTTP status, category, and default message. Frontend and backend must use these exact codes.

```yaml
errors:
  # Authentication & Authorization (4xx)
  - error_code: "AUTH_INVALID_CREDENTIALS"
    http_status: 401
    category: "AUTHENTICATION"
    default_message: "Invalid email or password."
    retryable: false

  - error_code: "AUTH_TOKEN_EXPIRED"
    http_status: 401
    category: "AUTHENTICATION"
    default_message: "Access token has expired. Please refresh or re-authenticate."
    retryable: true

  - error_code: "AUTH_TOKEN_INVALID"
    http_status: 401
    category: "AUTHENTICATION"
    default_message: "Access token is malformed, tampered, or issued by unknown authority."
    retryable: false

  - error_code: "AUTH_REFRESH_TOKEN_EXPIRED"
    http_status: 401
    category: "AUTHENTICATION"
    default_message: "Refresh token has expired. Full re-authentication required."
    retryable: false

  - error_code: "AUTH_INSUFFICIENT_ROLE"
    http_status: 403
    category: "AUTHORIZATION"
    default_message: "Your role does not permit this action."
    retryable: false

  - error_code: "AUTH_JURISDICTION_DENIED"
    http_status: 403
    category: "AUTHORIZATION"
    default_message: "You do not have jurisdiction over the requested geography."
    retryable: false

  - error_code: "AUTH_RATE_LIMITED"
    http_status: 429
    category: "RATE_LIMIT"
    default_message: "Too many requests. Please slow down."
    retryable: true
    retry_after_header: true

  # Validation Errors (422)
  - error_code: "VALIDATION_FAILED"
    http_status: 422
    category: "VALIDATION"
    default_message: "Request payload or parameters violated validation constraints."
    retryable: false

  - error_code: "VALIDATION_GEOGRAPHY_INVALID"
    http_status: 422
    category: "VALIDATION"
    default_message: "Invalid state_id or district_id. Must match registered geography codes."
    retryable: false

  - error_code: "VALIDATION_OCCUPATION_INVALID"
    http_status: 422
    category: "VALIDATION"
    default_message: "Invalid occupation_id or nco_code. Must exist in dim_occupation."
    retryable: false

  - error_code: "VALIDATION_HORIZON_INVALID"
    http_status: 422
    category: "VALIDATION"
    default_message: "Invalid forecast horizon. Must be one of: 3, 6, 12, 18, 24 months."
    retryable: false

  - error_code: "VALIDATION_BUDGET_INVALID"
    http_status: 422
    category: "VALIDATION"
    default_message: "Budget must be a positive number in INR."
    retryable: false

  - error_code: "VALIDATION_SCENARIO_PARAMETERS_INVALID"
    http_status: 422
    category: "VALIDATION"
    default_message: "Scenario parameters malformed or violate domain constraints."
    retryable: false

  # Resource Not Found (404)
  - error_code: "RESOURCE_NOT_FOUND"
    http_status: 404
    category: "NOT_FOUND"
    default_message: "The requested resource does not exist."
    retryable: false

  - error_code: "DISTRICT_NOT_FOUND"
    http_status: 404
    category: "NOT_FOUND"
    default_message: "District not found for the given state_id."
    retryable: false

  - error_code: "OCCUPATION_NOT_FOUND"
    http_status: 404
    category: "NOT_FOUND"
    default_message: "Occupation not found for the given occupation_id."
    retryable: false

  - error_code: "FORECAST_NOT_FOUND"
    http_status: 404
    category: "NOT_FOUND"
    default_message: "No forecast available for the requested occupation, district, and horizon."
    retryable: false

  - error_code: "SCENARIO_NOT_FOUND"
    http_status: 404
    category: "NOT_FOUND"
    default_message: "Scenario not found for the given scenario_id."
    retryable: false

  - error_code: "OPTIMIZATION_RUN_NOT_FOUND"
    http_status: 404
    category: "NOT_FOUND"
    default_message: "Optimization run not found for the given run_id."
    retryable: false

  # Conflict / State Errors (409)
  - error_code: "RESOURCE_CONFLICT"
    http_status: 409
    category: "CONFLICT"
    default_message: "Resource conflict: the operation would violate a uniqueness constraint."
    retryable: false

  - error_code: "SCENARIO_ALREADY_EXISTS"
    http_status: 409
    category: "CONFLICT"
    default_message: "A scenario with the same parameters already exists."
    retryable: false

  - error_code: "OPTIMIZATION_ALREADY_RUNNING"
    http_status: 409
    category: "CONFLICT"
    default_message: "An optimization is already running for this jurisdiction. Wait for completion."
    retryable: true

  # Server Errors (5xx)
  - error_code: "INTERNAL_SERVER_ERROR"
    http_status: 500
    category: "SERVER_ERROR"
    default_message: "An unexpected server error occurred. Please contact the administrator with the request ID."
    retryable: false

  - error_code: "DATABASE_UNAVAILABLE"
    http_status: 503
    category: "SERVER_ERROR"
    default_message: "Database is temporarily unavailable. Please retry shortly."
    retryable: true

  - error_code: "MIGRATION_MISMATCH"
    http_status: 503
    category: "SERVER_ERROR"
    default_message: "Database schema migration mismatch. Contact administrator."
    retryable: false

  - error_code: "FORECAST_ENGINE_UNAVAILABLE"
    http_status: 503
    category: "SERVER_ERROR"
    default_message: "Forecasting engine is unavailable. Model artifacts may be missing."
    retryable: true

  - error_code: "OPTIMIZATION_SOLVER_FAILED"
    http_status: 500
    category: "SERVER_ERROR"
    default_message: "Optimization solver failed to find a feasible solution within timeout."
    retryable: false

  - error_code: "OPTIMIZATION_INFEASIBLE"
    http_status: 422
    category: "BUSINESS_LOGIC"
    default_message: "Optimization problem is infeasible with given constraints. Relax budget or capacity limits."
    retryable: false

  - error_code: "COPILOT_TOOL_EXECUTION_FAILED"
    http_status: 500
    category: "SERVER_ERROR"
    default_message: "Copilot tool execution failed. See tool trace for details."
    retryable: false

  - error_code: "COPILOT_PROMPT_INJECTION_DETECTED"
    http_status: 400
    category: "SECURITY"
    default_message: "Prompt injection attempt detected. Request rejected."
    retryable: false

  - error_code: "COPILOT_GEMINI_API_ERROR"
    http_status: 502
    category: "EXTERNAL_DEPENDENCY"
    default_message: "Gemini API returned an error. Please retry later."
    retryable: true

  - error_code: "INGESTION_VALIDATION_FAILED"
    http_status: 422
    category: "DATA_QUALITY"
    default_message: "Ingested data failed quality validation. See quarantine for details."
    retryable: false

  - error_code: "INGESTION_PII_DETECTED"
    http_status: 400
    category: "SECURITY"
    default_message: "PII detected in ingestion payload. Ingestion aborted and logged."
    retryable: false

  - error_code: "EXPORT_GENERATION_FAILED"
    http_status: 500
    category: "SERVER_ERROR"
    default_message: "Failed to generate export report (PDF/CSV)."
    retryable: true

  # Business Logic Errors (422)
  - error_code: "INSUFFICIENT_DATA_FOR_FORECAST"
    http_status: 422
    category: "BUSINESS_LOGIC"
    default_message: "Insufficient historical data points to generate a reliable forecast."
    retryable: false

  - error_code: "INSUFFICIENT_DATA_FOR_GAP"
    http_status: 422
    category: "BUSINESS_LOGIC"
    default_message: "Insufficient demand or supply data to compute skill gap."
    retryable: false

  - error_code: "NO_CHAMPION_MODEL"
    http_status: 422
    category: "BUSINESS_LOGIC"
    default_message: "No champion model is currently registered for the requested forecast type."
    retryable: false

  - error_code: "SCENARIO_SIMULATION_FAILED"
    http_status: 500
    category: "SERVER_ERROR"
    default_message: "Scenario simulation failed due to internal computation error."
    retryable: false
```

---

## 2. Error Response Format (RFC 7807)

All error responses MUST conform to this schema:

```json
{
  "error_code": "VALIDATION_FAILED",
  "message": "Request payload or parameters violated validation constraints.",
  "details": {
    "errors": [
      {
        "loc": ["body", "district_id"],
        "msg": "Invalid district code",
        "type": "value_error"
      }
    ]
  },
  "timestamp": "2026-11-04T12:34:56.789Z",
  "request_id": "550e8400-e29b-41d4-a716-446655440000",
  "status_code": 422
}
```

### Field Definitions

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `error_code` | string | Yes | Machine-readable code from this catalog |
| `message` | string | Yes | Human-readable explanation (localizable) |
| `details` | object | No | Additional diagnostic context (validation errors, stack traces in dev) |
| `timestamp` | string (ISO 8601) | Yes | UTC timestamp of error generation |
| `request_id` | string (UUID) | Yes | Unique request trace ID for log correlation |
| `status_code` | integer | Yes | HTTP status code |

---

## 3. Frontend Error Handling Contract

The frontend MUST:

1. **Display `message` to user** — never show raw `error_code` or `details` to end users
2. **Log `error_code` + `request_id`** — for support ticket correlation
3. **Handle `retryable: true`** — show retry button with exponential backoff
4. **Redirect on 401** — clear auth store, redirect to `/login` with `next` param
5. **Show jurisdiction denial** — explain geographic scope mismatch, link to admin if elevated access needed

---

## 4. Backend Error Generation Rules

1. **Always use `ErrorResponse` model** from `backend/app/schemas/common.py`
2. **Set `request_id`** from `request.state.request_id` (injected by middleware)
3. **Never expose internal stack traces** in production (`details` only in DEBUG mode)
4. **Map exceptions to catalog codes** — never raise raw HTTPException with arbitrary detail
5. **Validation errors** → `VALIDATION_FAILED` with Pydantic `exc.errors()` in `details.errors`
6. **Database integrity errors** → map to `RESOURCE_CONFLICT` or `DATABASE_UNAVAILABLE`
7. **External API errors** → `COPILOT_GEMINI_API_ERROR`, `FORECAST_ENGINE_UNAVAILABLE`, etc.

---

## 5. Error Code Lookup (Auto-Generated)

> This section is auto-generated from the YAML above. Do not edit manually.

| Error Code | HTTP | Category | Retryable |
|------------|------|----------|-----------|
| AUTH_INVALID_CREDENTIALS | 401 | AUTHENTICATION | No |
| AUTH_TOKEN_EXPIRED | 401 | AUTHENTICATION | Yes |
| AUTH_TOKEN_INVALID | 401 | AUTHENTICATION | No |
| AUTH_REFRESH_TOKEN_EXPIRED | 401 | AUTHENTICATION | No |
| AUTH_INSUFFICIENT_ROLE | 403 | AUTHORIZATION | No |
| AUTH_JURISDICTION_DENIED | 403 | AUTHORIZATION | No |
| AUTH_RATE_LIMITED | 429 | RATE_LIMIT | Yes |
| VALIDATION_FAILED | 422 | VALIDATION | No |
| VALIDATION_GEOGRAPHY_INVALID | 422 | VALIDATION | No |
| VALIDATION_OCCUPATION_INVALID | 422 | VALIDATION | No |
| VALIDATION_HORIZON_INVALID | 422 | VALIDATION | No |
| VALIDATION_BUDGET_INVALID | 422 | VALIDATION | No |
| VALIDATION_SCENARIO_PARAMETERS_INVALID | 422 | VALIDATION | No |
| RESOURCE_NOT_FOUND | 404 | NOT_FOUND | No |
| DISTRICT_NOT_FOUND | 404 | NOT_FOUND | No |
| OCCUPATION_NOT_FOUND | 404 | NOT_FOUND | No |
| FORECAST_NOT_FOUND | 404 | NOT_FOUND | No |
| SCENARIO_NOT_FOUND | 404 | NOT_FOUND | No |
| OPTIMIZATION_RUN_NOT_FOUND | 404 | NOT_FOUND | No |
| RESOURCE_CONFLICT | 409 | CONFLICT | No |
| SCENARIO_ALREADY_EXISTS | 409 | CONFLICT | No |
| OPTIMIZATION_ALREADY_RUNNING | 409 | CONFLICT | Yes |
| INTERNAL_SERVER_ERROR | 500 | SERVER_ERROR | No |
| DATABASE_UNAVAILABLE | 503 | SERVER_ERROR | Yes |
| MIGRATION_MISMATCH | 503 | SERVER_ERROR | No |
| FORECAST_ENGINE_UNAVAILABLE | 503 | SERVER_ERROR | Yes |
| OPTIMIZATION_SOLVER_FAILED | 500 | SERVER_ERROR | No |
| OPTIMIZATION_INFEASIBLE | 422 | BUSINESS_LOGIC | No |
| COPILOT_TOOL_EXECUTION_FAILED | 500 | SERVER_ERROR | No |
| COPILOT_PROMPT_INJECTION_DETECTED | 400 | SECURITY | No |
| COPILOT_GEMINI_API_ERROR | 502 | EXTERNAL_DEPENDENCY | Yes |
| INGESTION_VALIDATION_FAILED | 422 | DATA_QUALITY | No |
| INGESTION_PII_DETECTED | 400 | SECURITY | No |
| EXPORT_GENERATION_FAILED | 500 | SERVER_ERROR | Yes |
| INSUFFICIENT_DATA_FOR_FORECAST | 422 | BUSINESS_LOGIC | No |
| INSUFFICIENT_DATA_FOR_GAP | 422 | BUSINESS_LOGIC | No |
| NO_CHAMPION_MODEL | 422 | BUSINESS_LOGIC | No |
| SCENARIO_SIMULATION_FAILED | 500 | SERVER_ERROR | No |

---

## 6. Adding New Error Codes

**Process:**
1. Add entry to YAML front-matter in this file
2. Run doc generation script (updates lookup table)
3. Add unit test in `backend/tests/unit/test_error_catalog.py`
4. Update frontend error handling if new category or retry behavior

**Naming Convention:** `{DOMAIN}_{SPECIFIC_ERROR}` in SCREAMING_SNAKE_CASE
- Domains: AUTH, VALIDATION, RESOURCE, SCENARIO, OPTIMIZATION, COPILOT, INGESTION, EXPORT, BUSINESS_LOGIC, SERVER, SECURITY, EXTERNAL

**Prohibited:**
- Generic codes like `ERROR`, `FAILED`, `INVALID`
- Codes without category mapping
- Codes without explicit retryable boolean