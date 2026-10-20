# ADR-0003: BigQuery as Analytical Data Warehouse Layer

**Status:** APPROVED  
**Date:** 2026-10-20  
**Deciders:** Principal Engineering Agent  

---

## Context
Aggregating years of high-frequency job postings and national census records across hundreds of districts can saturate an operational OLTP database during large-scale feature extraction, time-series training set assembly, and national backtesting jobs.

## Decision
We designate **Google BigQuery** as the analytical warehouse tier for large-scale analytical transformations, multi-year historical panel queries, and feature engineering. For local execution and environments without active cloud credentials, LABREX implements an abstraction layer with local Parquet / Polars fallback so the application runs completely offline without failures.

## Consequences
### Positive
- High-concurrency SQL analytics across billion-row national datasets without impacting OLTP performance.
- Serverless scaling with zero database administration.
- Parquet/Polars local abstraction allows complete local offline development.

### Negative / Trade-offs
- Requires data movement pipelines from operational PostgreSQL or Cloud Storage into BigQuery.
- Cloud costs must be monitored with query byte limits.
