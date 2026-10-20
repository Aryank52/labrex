# ADR-0007: Containerized Deployment via Google Cloud Run

**Status:** APPROVED  
**Date:** 2026-10-20  
**Deciders:** Principal Engineering Agent  

---

## Context
Deploying full Kubernetes (GKE) clusters for LABREX introduces unnecessary operational overhead, node pool management, and fixed infrastructure expenses. A serverless, auto-scaling container platform is ideal for handling fluctuating policy research and planner workloads while minimizing idle hosting costs.

## Decision
We select **Google Cloud Run** as the production runtime environment for both:
1. `labrex-api`: Python 3.12 FastAPI backend container.
2. `labrex-web`: Next.js 15 Node.js frontend container.
Both services scale automatically based on request concurrency. Cloud Run services connect to managed Cloud SQL (PostgreSQL 16) via Serverless VPC Access and retrieve secrets securely from Google Secret Manager.

## Consequences
### Positive
- Serverless scaling from 1 (warm standby) to 20 instances based on traffic.
- Zero Kubernetes cluster maintenance.
- Predictable cost profile with per-millisecond billing.
- Simplified CI/CD pipeline using standard container images.

### Negative / Trade-offs
- Maximum request timeout capped at 60 minutes (well beyond the 5-second API budget).
- Very long-running batch training jobs should run via Cloud Run Jobs or Vertex AI instead of HTTP web requests.
