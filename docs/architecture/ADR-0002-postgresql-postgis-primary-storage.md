# ADR-0002: PostgreSQL 16 + PostGIS as Primary Relational & Spatial Store

**Status:** APPROVED  
**Date:** 2026-10-20  
**Deciders:** Principal Engineering Agent  

---

## Context
LABREX requires robust relational integrity for users, roles, NCO codes, NSQF levels, training centres, and fact records, combined with native spatial querying capabilities for India's 36 States and 700+ districts (boundary polygons, containment checks, distance calculations, and GeoJSON serialization).

## Decision
We select **PostgreSQL 16** with the **PostGIS** extension as the primary operational and analytical relational database. Spatial coordinates and district boundaries are stored in PostGIS geometry columns (`EPSG:4326`). Text embeddings for semantic search are stored using `pgvector`. All schema changes are governed through Alembic migrations.

## Consequences
### Positive
- Single robust database engine handling relational, spatial, and vector capabilities.
- Native PostGIS functions (`ST_Contains`, `ST_Intersects`, `ST_AsGeoJSON`) provide sub-millisecond geographic spatial lookups.
- Mature async ecosystem via Python `asyncpg` and SQLAlchemy 2.0.
- Seamless compatibility with Google Cloud SQL for PostgreSQL.

### Negative / Trade-offs
- PostGIS spatial indexing requires disciplined memory allocation (work_mem, maintenance_work_mem).
- Massive multi-year historical log queries (>100M rows) should be offloaded to BigQuery rather than overloading transactional tables.
