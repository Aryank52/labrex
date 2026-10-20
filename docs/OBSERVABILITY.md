# LABREX Observability & Telemetry Architecture

**Document Version:** 1.0  
**Authority:** Master Directive Section 69 & 70  

---

## 1. Structured Logging Standard

All backend logs are emitted to standard output (`stdout`) in JSON format. Every log record contains standard context fields:

```json
{
  "timestamp": "2026-10-20T10:15:30.124Z",
  "level": "INFO",
  "service": "labrex-api",
  "request_id": "c1f7a4e2-63b1-4f12-9c10-8b1e4c7d9a12",
  "user_id": "8f8b8e0b-d249-47bb-8c38-8e6f1a7d4e32",
  "operation": "RUN_OPTIMIZATION",
  "endpoint": "/api/v1/optimization/solve",
  "status_code": 200,
  "latency_ms": 284.5,
  "model_version": "OR_TOOLS_MILP_V1",
  "dataset_version": "GOLD_2026_Q1",
  "message": "Optimization solved to optimality in 284ms. 5 interventions recommended."
}
```

---

## 2. Key Metrics & Service Level Objectives (SLOs)

| Metric Name | Type | Description | Target SLO |
| :--- | :--- | :--- | :--- |
| `labrex_http_request_duration_seconds` | Histogram | Latency distribution by endpoint and method | P95 < 350ms |
| `labrex_http_requests_total` | Counter | Total requests partitioned by status code | Error Rate < 0.1% |
| `labrex_optimization_solve_duration_seconds` | Histogram | Time spent in Google OR-Tools solver | P95 < 4.0s |
| `labrex_copilot_tool_invocations_total` | Counter | Counts of tool calls triggered by Gemini | Success > 99.0% |
| `labrex_forecast_wape_gauge` | Gauge | Active Champion WAPE per occupation series | WAPE < 0.15 |

---

## 3. Health & Diagnostic Probes

- `/health`: Lightweight HTTP 200 check for container orchestration liveness.
- `/health/ready`: Validates active database connection pool, PostGIS extensions, and model registry artifacts.
- `/health/version`: Returns git commit hash, build timestamp, and active environment (`LOCAL`, `STAGING`, `PRODUCTION`).
