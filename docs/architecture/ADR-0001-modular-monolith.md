# ADR-0001: Modular Monolith Architecture

**Status:** APPROVED  
**Date:** 2026-10-20  
**Deciders:** Principal Engineering Agent  

---

## Context
Labour market intelligence involves tightly coupled domain logic: occupation taxonomies, skill mappings, spatial geometries, time-series feature engineering, and optimization models. Implementing this system as distributed microservices would introduce substantial operational overhead, distributed transactional complexity, network serialization latency, and development friction without providing immediate organizational scaling benefits.

## Decision
We adopt a **High-Performance Modular Monolith** architecture for LABREX using Python 3.12, FastAPI, and Pydantic v2 in `backend/app/`. Subsystems are strictly isolated into decoupled domain service modules (`services/demand`, `services/supply`, `services/forecasting`, `services/optimization`, etc.) that interact through typed internal interfaces and database repositories rather than HTTP network hops.

## Consequences
### Positive
- Zero network serialization overhead between domain services.
- Atomic ACID transactions supported across dimensional updates.
- Simplified local development and unified CI/CD testing.
- Single deployment artifact on Cloud Run.

### Negative / Trade-offs
- Requires strict enforcement of package boundary rules to prevent domain logic leaking into API route controllers.
- Compute-intensive ML workloads must be managed via background workers or asynchronous threads.
