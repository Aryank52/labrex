# LABREX Scenario Engine Specification

**Document Version:** 1.0  
**Authority:** Master Directive Section 17, 40, 92  
**Phase:** 11 (Scenario Engine Implementation)  
**Status:** Specification — Ready for Implementation

---

## 1. Purpose & Scope

The Scenario Engine enables policy planners to simulate counterfactual "what-if" interventions on the labour market and immediately observe projected impacts on skill gaps, budget requirements, and placement outcomes. It is the bridge between diagnostic intelligence (Phases 8-10) and prescriptive optimization (Phase 12).

**Core Principle:** Every scenario is a deterministic, reproducible transformation of the canonical data state. No hidden state, no side effects, full audit trail.

---

## 2. Scenario State Machine

```
┌─────────────┐
│   DRAFT     │  ← User creates scenario, edits parameters
└──────┬──────┘
       │ validate()
       ▼
┌─────────────┐
│  VALIDATED  │  ← Parameters pass schema + business rule checks
└──────┬──────┘
       │ simulate()
       ▼
┌─────────────┐
│  SIMULATING │  ← Async execution (background job)
└──────┬──────┘
       │ complete / fail
       ▼
┌─────────────┐     ┌─────────────┐
│  COMPLETED  │     │   FAILED    │  ← Terminal states
└─────────────┘     └─────────────┘
       │                    │
       │ export()           │ retry()
       ▼                    ▼
┌─────────────┐     ┌─────────────┐
│  EXPORTED   │     │  SIMULATING │
└─────────────┘     └─────────────┘
```

**Transitions:**
- `DRAFT → VALIDATED`: Automatic on parameter save if `validate()` passes
- `VALIDATED → SIMULATING`: User clicks "Run Simulation" or API `POST /scenarios/{id}/run`
- `SIMULATING → COMPLETED`: Simulation finishes successfully, results persisted
- `SIMULATING → FAILED`: Simulation throws error; error logged, scenario marked failed
- `FAILED → SIMULATING`: User clicks "Retry" after fixing parameters
- `COMPLETED → EXPORTED`: User downloads PDF/CSV report

---

## 3. Parameter Schema (Pydantic)

```python
# backend/app/schemas/scenario.py

from pydantic import BaseModel, Field, field_validator
from typing import Dict, List, Optional, Literal
from uuid import UUID
from datetime import date

class InterventionBase(BaseModel):
    """Base intervention — all specific types inherit."""
    intervention_id: str = Field(..., description="Client-generated UUID for idempotency")
    type: Literal["SEAT_EXPANSION", "NEW_PROGRAM", "CENTRE_UPGRADE", "CURRICULUM_UPDATE", "MOBILE_LAB", "SUBSIDY", "TARGETED_RESKILLING"]
    target_district_id: str = Field(..., description="District code (e.g., IN-MH-PUN)")
    target_occupation_id: Optional[str] = None  # Required for occupation-specific interventions
    target_qualification_id: Optional[str] = None  # Required for program-specific interventions

class SeatExpansion(InterventionBase):
    type: Literal["SEAT_EXPANSION"] = "SEAT_EXPANSION"
    seat_delta: int = Field(..., ge=1, le=10000, description="Additional seats per intake cycle")
    cost_per_seat_inr: float = Field(..., gt=0, description="Marginal cost per additional seat")
    intake_cycles_per_year: int = Field(default=2, ge=1, le=4)
    start_date: date
    end_date: Optional[date] = None

class NewProgram(InterventionBase):
    type: Literal["NEW_PROGRAM"] = "NEW_PROGRAM"
    qualification_id: str
    centre_id: str
    annual_intake: int = Field(..., ge=10, le=500)
    setup_cost_inr: float = Field(..., gt=0)
    recurring_cost_inr: float = Field(..., gt=0)
    start_date: date

class CentreUpgrade(InterventionBase):
    type: Literal["CENTRE_UPGRADE"] = "CENTRE_UPGRADE"
    centre_id: str
    new_capacity_multiplier: float = Field(..., gt=1.0, le=3.0)
    upgrade_cost_inr: float = Field(..., gt=0)
    downtime_months: int = Field(default=0, ge=0, le=12)
    start_date: date

class MobileLab(InterventionBase):
    type: Literal["MOBILE_LAB"] = "MOBILE_LAB"
    districts_covered: List[str]  # Multiple districts
    skills_targeted: List[str]    # Skill IDs
    annual_operating_cost_inr: float
    trainees_per_year: int
    start_date: date

class TargetedReskilling(InterventionBase):
    type: Literal["TARGETED_RESKILLING"] = "TARGETED_RESKILLING"
    source_occupation_id: str  # Workers transitioning FROM this occupation
    target_occupation_id: str  # Workers transitioning TO this occupation
    workers_per_batch: int
    training_duration_months: int
    cost_per_worker_inr: float
    placement_rate_pct: float = Field(..., ge=0.0, le=100.0)
    start_date: date

class ScenarioParameters(BaseModel):
    """Complete scenario definition."""
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    horizon_months: int = Field(default=12, ge=3, le=24)
    budget_inr: float = Field(..., gt=0, description="Total budget ceiling for this scenario")
    interventions: List[InterventionBase] = Field(..., min_length=1, max_length=50)
    assumptions: Dict[str, float] = Field(default_factory=dict, description="Override default assumptions")

    @field_validator("interventions")
    @classmethod
    def validate_interventions(cls, v):
        # Check budget feasibility (rough estimate)
        total_estimated = sum(
            i.seat_delta * i.cost_per_seat_inr * i.intake_cycles_per_year
            if hasattr(i, 'seat_delta') else
            i.setup_cost_inr + i.recurring_cost_inr
            if hasattr(i, 'setup_cost_inr') else
            i.upgrade_cost_inr
            if hasattr(i, 'upgrade_cost_inr') else
            i.annual_operating_cost_inr
            if hasattr(i, 'annual_operating_cost_inr') else
            i.workers_per_batch * i.cost_per_worker_inr
            for i in v
        )
        if total_estimated > 1.5 * cls.model_fields['budget_inr'].default:
            # Warning only — not a hard error
            pass
        return v
```

---

## 4. Simulation Engine Algorithm

### 4.1 Inputs

| Source | Table | Key Fields |
|--------|-------|------------|
| Baseline Demand Forecast | `forecast_demand` | `district_id`, `occupation_id`, `horizon_months`, `point_estimate` (champion) |
| Baseline Supply Forecast | `forecast_supply` | Same keys |
| Current Skill Gap | `skill_gap` | `demand_index`, `supply_index`, `projected_gap` |
| Training Capacity | `fact_training_capacity` | `center_id`, `qualification_id`, `sanctioned_seats` |
| Training Outcomes | `fact_training_outcomes` | `certified_trainees`, `placed_trainees` |
| Centre Info | `dim_training_center` | `center_id`, `district_id`, `center_type`, `is_accredited` |
| Occupation ↔ Skill Map | `map_occupation_skill` | `occupation_id`, `skill_id`, `importance_weight` |
| Skill ↔ Qualification Map | `map_skill_qualification` | `skill_id`, `qualification_id`, `coverage_weight` |

### 4.2 Simulation Steps

```
FOR each intervention IN scenario.interventions (ordered by user priority):
    
    1. RESOLVE TARGET SET
       - Identify affected (district, occupation) tuples
       - For SEAT_EXPANSION: all occupations mapped to the qualification at that centre
       - For NEW_PROGRAM: single (centre, qualification) → mapped occupations
       - For MOBILE_LAB: cross-product of districts × skills → mapped occupations
       - For TARGETED_RESKILLING: source occupation workers → target occupation
    
    2. COMPUTE SUPPLY DELTA
       - Annual new certified supply = seats × intake_cycles × certification_rate
       - certification_rate = historical certified_trainees / enrolled_trainees (per centre/qualification)
       - Apply placement_rate discount for effective supply
       - Distribute across horizon_months (linear ramp-up unless specified)
    
    3. COMPUTE COST
       - Capital cost (setup, upgrade) incurred at start_date
       - Recurring cost prorated monthly
       - Track cumulative spend vs budget_inr
    
    4. UPDATE SUPPLY FORECAST
       - For each affected (district, occupation, month):
           new_supply = baseline_supply + supply_delta
       - Recompute supply_index (0-100) using SI-1.0 formula
       - Recompute skill_gap = demand_index - supply_index
    
    5. TRACK METRICS
       - Net gap reduction per occupation/district
       - Budget utilization %
       - Cost per gap unit reduced (INR/gap)
       - Placement outcomes projected

AGGREGATE:
    - Total gap reduction across all interventions
    - Budget utilization
    - Pareto efficiency: interventions sorted by cost-effectiveness
    - Sensitivity: ±10% budget → gap reduction delta
```

### 4.3 Output Schema (ScenarioResult)

```python
class ScenarioResult(BaseModel):
    scenario_id: UUID
    baseline_gap: float  # Sum of projected_gap across all affected tuples
    simulated_gap: float  # After interventions
    net_reduction: float  # baseline - simulated
    reduction_pct: float  # net_reduction / baseline * 100
    estimated_cost_inr: float
    budget_utilization_pct: float  # estimated_cost / budget_inr * 100
    confidence_score: float = Field(..., ge=0.0, le=1.0)
    
    # Per-intervention breakdown
    intervention_results: List[InterventionResult]
    
    # Sensitivity
    sensitivity: Dict[str, float]  # e.g., {"budget_+10%": -5.2, "budget_-10%": +6.1}
    
    # Assumptions used
    assumptions_applied: Dict[str, float]
    
    # Metadata
    simulated_at: datetime
    simulation_duration_ms: int
    simulator_version: str = "1.0"
```

---

## 5. Business Rules & Constraints

| Rule | Enforcement |
|------|-------------|
| Budget cannot be exceeded | Hard constraint: simulation fails if cumulative cost > budget_inr |
| Centre capacity physical limit | `sanctioned_seats + seat_delta ≤ max_physical_capacity` (from `dim_training_center`) |
| Minimum cohort size | `seat_delta ≥ 10` (configurable per centre type) |
| Regional equity | No single district > 40% of total budget (configurable) |
| Certification rate bounded | Use historical 5th percentile, not mean |
| Placement rate bounded | Use historical 5th percentile, not mean |
| Intervention ordering matters | User-specified priority order; later interventions see supply from earlier ones |
| No double-counting | If two interventions target same (centre, qualification), seats are additive but certification rate applies once |

---

## 6. API Contract

### `POST /api/v1/scenarios`
```json
{
  "title": "EV Technician Expansion - Pune",
  "description": "Add 500 seats across 4 ITIs for EV Assembly",
  "horizon_months": 12,
  "budget_inr": 25000000,
  "interventions": [
    {
      "intervention_id": "int-001",
      "type": "SEAT_EXPANSION",
      "target_district_id": "IN-MH-PUN",
      "target_qualification_id": "QP-ASC-Q1402",
      "seat_delta": 150,
      "cost_per_seat_inr": 45000,
      "intake_cycles_per_year": 2,
      "start_date": "2026-04-01"
    }
  ],
  "assumptions": {
    "certification_rate": 0.78,
    "placement_rate": 0.72
  }
}
```
**Response (201):** `{ "scenario_id": "uuid", "status": "DRAFT", "validation": { "valid": true, "warnings": [] } }`

### `POST /api/v1/scenarios/{scenario_id}/run`
**Response (202):** `{ "status": "SIMULATING", "job_id": "uuid" }` — async job

### `GET /api/v1/scenarios/{scenario_id}/result`
**Response (200):** `ScenarioResult` (if COMPLETED)

### `GET /api/v1/scenarios`
Query: `status`, `user_id`, `limit`, `offset`
**Response (200):** Paginated list of scenarios

---

## 7. Reproducibility Guarantees

1. **Deterministic Inputs:** All inputs read from canonical tables at simulation start (snapshot isolation via `SELECT ... FOR SHARE` or MVCC)
2. **Versioned Assumptions:** Default assumptions (certification rates, placement rates) stored in `dim_source` or config; overrideable per scenario
3. **Simulator Versioning:** `simulator_version` in result; breaking changes increment major version
4. **Audit Trail:** Every simulation writes to `scenario_result` + `audit_log` with full parameter JSON
5. **Idempotent Re-run:** Same `scenario_id` + same inputs → identical `ScenarioResult` (within floating-point tolerance)

---

## 8. Testing Requirements

| Test | Description |
|------|-------------|
| Unit: Parameter Validation | Invalid interventions rejected; budget checks work |
| Unit: Supply Delta Calculation | Seat expansion → correct annual certified supply |
| Unit: Cost Computation | Capital + recurring correctly prorated |
| Integration: Full Simulation | End-to-end with seeded DB; compare to golden master |
| Integration: Budget Enforcement | Simulation fails when cost > budget |
| Integration: Concurrent Runs | Two scenarios for same district don't interfere |
| Property: Monotonicity | Adding interventions never increases gap |
| Property: Budget Monotonicity | Higher budget → ≥ gap reduction |
| Regression: Golden Master | Stored fixture scenario produces identical results |

---

## 9. Performance Targets

| Metric | Target |
|--------|--------|
| Simulation latency (50 interventions) | < 2.5s |
| Simulation latency (10 interventions) | < 500ms |
| API response (create scenario) | < 200ms |
| API response (get result) | < 100ms |
| Concurrent simulations | 10 per API instance |

---

## 10. Future Extensions (Post-MVP)

- **Monte Carlo Simulation:** Run N times with sampled assumption distributions
- **Multi-Objective Optimization:** Pareto front (gap reduction vs budget vs equity)
- **Dynamic Assumptions:** Time-varying certification/placement rates
- **Spatial Spillover:** Adjacent district effects
- **Labour Mobility:** Worker migration between districts in response to gaps