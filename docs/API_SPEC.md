# LABREX REST API Specifications (v1)

**Base URL:** `/api/v1`  
**Protocol:** HTTPS / JSON  
**Auth:** Bearer JWT Token  
**Document Version:** 1.0  

---

## 1. Authentication & System Health

### `POST /auth/login`
- **Description**: Authenticate user credentials and return signed JWT with role and geographic scope.
- **Request Body**:
  ```json
  {
    "email": "planner@msde.gov.in",
    "password": "SecurePassword123!"
  }
  ```
- **Response (200 OK)**:
  ```json
  {
    "access_token": "eyJhbGciOiJIUzI1Ni...",
    "token_type": "bearer",
    "expires_in": 3600,
    "user": {
      "user_id": "8f8b8e0b-...",
      "name": "Arun Sharma",
      "email": "planner@msde.gov.in",
      "role": "NATIONAL_PLANNER",
      "jurisdiction": "ALL"
    }
  }
  ```

### `GET /health` & `GET /health/ready`
- **Description**: Liveness and readiness probes checking PostgreSQL, PostGIS, and model registry availability.
- **Response (200 OK)**:
  ```json
  {
    "status": "HEALTHY",
    "version": "1.0.0",
    "database": "CONNECTED",
    "postgis": "AVAILABLE",
    "models_loaded": 3
  }
  ```

---

## 2. Spatial & Geographic Intelligence

### `GET /geographies/states`
- **Query Params**: `limit` (int, default 50)
- **Response (200 OK)**: Array of states with centroid and summary demand/supply metrics.

### `GET /geographies/districts`
- **Query Params**: `state_id` (string, optional), `include_geojson` (boolean, default false)
- **Response (200 OK)**:
  ```json
  [
    {
      "district_id": "IN-MH-PUN",
      "state_id": "IN-MH",
      "name": "Pune",
      "demand_index": 78.4,
      "supply_index": 62.1,
      "net_skill_gap": 14200,
      "risk_status": "HIGH"
    }
  ]
  ```

---

## 3. Demand, Supply & Skill Gap Intelligence

### `GET /demand/index`
- **Query Params**: `district_id` (string), `sector_id` (string), `horizon` (string, default "12m")
- **Response (200 OK)**:
  ```json
  {
    "scope": "DISTRICT",
    "district_id": "IN-MH-PUN",
    "demand_index": 78.4,
    "index_version": "DI-1.0",
    "components": {
      "active_postings_score": 82.5,
      "growth_rate_score": 75.0,
      "vacancy_persistence_score": 71.2,
      "employer_diversity_score": 84.9
    },
    "historical_trend": [
      { "period": "2025-Q1", "index": 64.2 },
      { "period": "2025-Q2", "index": 69.8 },
      { "period": "2025-Q3", "index": 74.5 },
      { "period": "2025-Q4", "index": 78.4 }
    ]
  }
  ```

### `GET /gaps/radar`
- **Description**: Returns all flagged early-warning items filtered by risk level.
- **Query Params**: `risk_class` (`CRITICAL`, `HIGH`, `EMERGING`), `state_id`, `limit` (default 50)
- **Response (200 OK)**:
  ```json
  [
    {
      "alert_id": "ALT-9042",
      "district_id": "IN-MH-PUN",
      "district_name": "Pune",
      "occupation_title": "Solar PV Installation Technician",
      "nco_code": "7421.0300",
      "risk_class": "CRITICAL",
      "projected_gap": 1450,
      "demand_index": 89.2,
      "supply_index": 45.1,
      "forecast_confidence": 0.88,
      "model_agreement": "HIGH",
      "drivers": [
        "Demand surge of +38% QoQ due to green industrial corridor",
        "Local ITI training capacity stagnant at 120 seats/yr"
      ]
    }
  ]
  ```

---

## 4. Forecasting & Model Comparison

### `GET /forecasts/occupation/{occupation_id}`
- **Query Params**: `district_id` (string), `horizon_months` (int, default 12)
- **Response (200 OK)**:
  ```json
  {
    "occupation_id": "OCC-7421-0300",
    "district_id": "IN-MH-PUN",
    "champion_model": "LIGHTGBM_V1",
    "forecast": {
      "horizon_months": 12,
      "target_date": "2026-12-31",
      "point_estimate": 2650,
      "interval_80": { "lower": 2420, "upper": 2880 },
      "interval_95": { "lower": 2180, "upper": 3120 }
    },
    "challenger_comparisons": [
      { "model": "SEASONAL_NAIVE", "point_estimate": 2100, "validation_wape": 0.184 },
      { "model": "LIGHTGBM_V1", "point_estimate": 2650, "validation_wape": 0.089 },
      { "model": "TIMESFM_3", "point_estimate": 2720, "validation_wape": 0.094 }
    ],
    "model_agreement": "HIGH"
  }
  ```

---

## 5. Counterfactual Scenarios & Policy Optimization

### `POST /scenarios/simulate`
- **Request Body**:
  ```json
  {
    "title": "Pune Solar Training Expansion",
    "district_id": "IN-MH-PUN",
    "occupation_id": "OCC-7421-0300",
    "interventions": [
      { "type": "ADD_SEATS", "center_id": "TC-MH-PUN-01", "additional_seats": 250 },
      { "type": "ADD_SEATS", "center_id": "TC-MH-PUN-04", "additional_seats": 250 }
    ]
  }
  ```
- **Response (200 OK)**:
  ```json
  {
    "scenario_id": "scen-4b2a9...",
    "baseline_12m_gap": 1450,
    "simulated_12m_gap": 950,
    "net_gap_reduction": 500,
    "reduction_percentage": 34.48,
    "estimated_cost_inr": 7500000,
    "confidence_score": 0.88
  }
  ```

### `POST /optimization/solve`
- **Request Body**:
  ```json
  {
    "state_id": "IN-MH",
    "budget_inr": 25000000,
    "target_horizon_months": 12,
    "allowed_intervention_types": ["EXPAND_SEATS", "LAUNCH_PROGRAM"],
    "min_cohort_size": 30
  }
  ```
- **Response (200 OK)**:
  ```json
  {
    "run_id": "opt-9f3a1...",
    "solver_status": "OPTIMAL",
    "total_budget_allocated_inr": 21250000,
    "expected_deficit_reduction": 1820,
    "solve_time_ms": 284,
    "recommended_interventions": [
      {
        "rank": 1,
        "center_id": "TC-MH-PUN-01",
        "center_name": "Government ITI Aundh",
        "qualification_id": "QP-ASC-Q1402",
        "action": "EXPAND_SEATS",
        "seat_delta": 240,
        "cost_inr": 3600000,
        "targeted_skill": "Solar PV Installation",
        "expected_gap_reduction": 240
      }
    ],
    "explanation": "Intervention Option A yields highest deficit reduction per rupee by expanding existing accredited ITI facilities with pre-existing electrical lab infrastructure."
  }
  ```

---

## 6. AI Policy Copilot Endpoint

### `POST /copilot/query`
- **Request Body**:
  ```json
  {
    "query": "Where is the largest skill deficit in Maharashtra and what will it cost to reduce it by 30%?",
    "conversation_id": "conv-3a1..."
  }
  ```
- **Response (200 OK)**:
  ```json
  {
    "answer": "In Maharashtra, the largest 12-month projected deficit is in Pune for **Solar PV Installation Technicians** (Net gap: 1,450 workers). According to the LABREX Optimizer, reducing this deficit by 34% requires adding 500 training seats across accredited centres at an estimated cost of ₹75.0 Lakhs.",
    "tools_executed": [
      { "tool": "get_risk_alerts", "params": { "state_id": "IN-MH" }, "status": "SUCCESS" },
      { "tool": "run_scenario", "params": { "district_id": "IN-MH-PUN" }, "status": "SUCCESS" }
    ],
    "supporting_evidence": [
      { "source": "LABREX RADAR", "metric": "Gap = 1,450", "confidence": "0.88" },
      { "source": "LABREX Optimizer", "cost": "₹75,00,000" }
    ]
  }
  ```
