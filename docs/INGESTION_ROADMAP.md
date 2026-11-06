# LABREX Ingestion Roadmap

**Document Version:** 2.0  
**Authority:** Master Directive Section 14, 93, 94  
**Phase:** 4 (Data Ingestion Pipelines & Harmonization)  
**Status:** Execution Plan — Ready for Implementation

---

## 1. Phased Ingestion Strategy

The roadmap is organized into **waves** with explicit gate criteria. Each wave can be parallelized within its stage but waves are sequential due to foreign key dependencies.

```
WAVE 1: Reference Dimensions (No FK dependencies)
    ├── dim_date (calendar)
    ├── dim_nsqf_level (1-10)
    └── dim_sector (economic sectors)
           │
           ▼
WAVE 2: Geography (Depends on dim_date for versioning)
    ├── dim_state (PostGIS boundaries)
    └── dim_district (PostGIS boundaries, FK → dim_state)
           │
           ▼
WAVE 3: Core Taxonomy (Depends on Wave 1 + 2)
    ├── dim_nco (NCO-2015 hierarchy)
    ├── dim_skill (canonical skills)
    ├── dim_qualification (QPs, FK → dim_nsqf_level, dim_sector)
    ├── dim_training_program (FK → dim_qualification)
    └── dim_training_center (FK → dim_district)
           │
           ▼
WAVE 4: Mapping Tables (Depends on Wave 3)
    ├── map_occupation_skill
    └── map_skill_qualification
           │
           ▼
WAVE 5: Fact Tables (Depends on Waves 2, 3, 4)
    ├── fact_job_demand (NCS, job portals)
    ├── fact_workforce_supply (PLFS, census)
    ├── fact_training_capacity (PMKVY, DGT, NSDC)
    ├── fact_training_outcomes (PMKVY, DGT)
    ├── fact_skill_signal (NCS, job portals, scraping)
    └── fact_employer_signal (MCA, EPFO, surveys)
           │
           ▼
WAVE 6: Analytics & Intelligence (Depends on Wave 5)
    ├── forecast_demand / forecast_supply (ML pipeline)
    ├── skill_gap (computed)
    ├── risk_alert (computed)
    └── model_registry / model_run / model_metric
           │
           ▼
WAVE 7: Governance (Continuous)
    ├── dataset_registry
    ├── data_quality
    ├── data_lineage
    └── audit_log
```

---

## 2. Wave Details & Gate Criteria

### Wave 1: Reference Dimensions (Week 1)

| Task | Source | Estimated Rows | Gate Criteria |
|------|--------|----------------|---------------|
| `dim_date` | Generated | 50 years × 365 = ~18k | All dates 2020-2070 present; FY/FQ correct |
| `dim_nsqf_level` | NSQF Gazette | 10 | Levels 1-10; descriptors non-empty |
| `dim_sector` | NSDC/SSC list | 30-50 | All major SSCs represented; unique names |

**Parallelizable:** Yes (all independent)
**Rollback:** `TRUNCATE dim_date, dim_nsqf_level, dim_sector RESTART IDENTITY CASCADE`

---

### Wave 2: Geography (Week 1-2)

| Task | Source | Estimated Rows | Gate Criteria |
|------|--------|----------------|---------------|
| `dim_state` | LGD/Survey of India | 36 | All 36 States/UTs; geom valid MultiPolygon SRID 4326; centroid present |
| `dim_district` | LGD/Survey of India | 780+ | All districts; parent state_id valid; geom valid; centroid present |

**Dependencies:** Wave 1 complete
**Parallelizable:** State → District (sequential within wave)
**Validation:** `python -m labrex.data.validate_raw --source SRC-GEO-ADMIN`
**Rollback:** `TRUNCATE dim_district, dim_state RESTART IDENTITY CASCADE`

---

### Wave 3: Core Taxonomy (Week 2-3)

| Task | Source | Estimated Rows | Gate Criteria |
|------|--------|----------------|---------------|
| `dim_nco` | NCO-2015 Vol I | ~3,500 (8-digit) | All 5 hierarchy levels populated; no duplicate nco_code |
| `dim_skill` | NSQF/NOS/QP analysis | 500-2,000 | All 4 types (TECHNICAL, FOUNDATIONAL, DIGITAL, GREEN) represented |
| `dim_qualification` | NQR | ~14,000 | All linked to valid nsqf_level + sector_id |
| `dim_training_program` | NQR + NSDC | ~14,000 | All linked to valid qualification_id |
| `dim_training_center` | NSDC/DGT | 15,000-25,000 | All linked to valid district_id; geom valid Point SRID 4326 |

**Dependencies:** Waves 1, 2 complete
**Parallelizable:** NCO, Skill, Qualification can run in parallel; Program, Center after Qualification
**Validation:** NCO parser unit tests; geography validator for centers
**Rollback:** Truncate in reverse FK order

---

### Wave 4: Mapping Tables (Week 3)

| Task | Source | Estimated Rows | Gate Criteria |
|------|--------|----------------|---------------|
| `map_occupation_skill` | NCO-NOS-QP mapping | 10,000-50,000 | All occupation_id valid; all skill_id valid; weight 0-1 |
| `map_skill_qualification` | QP-NOS mapping | 20,000-100,000 | All skill_id valid; all qualification_id valid; weight 0-1 |

**Dependencies:** Wave 3 complete
**Parallelizable:** Yes (independent)
**Validation:** FK checks; uniqueness on (occupation_id, skill_id) and (skill_id, qualification_id)

---

### Wave 5: Fact Tables (Week 3-6) — **Core Ingestion**

| Fact Table | Source(s) | Frequency | Key Challenges |
|------------|-----------|-----------|----------------|
| `fact_job_demand` | NCS, job portals | Monthly | NCO mapping; employer dedup; cumulative vs flow |
| `fact_workforce_supply` | PLFS, Census | Annual/Quarterly | Survey weights; small-area estimation for districts |
| `fact_training_capacity` | PMKVY, DGT, NSDC | Quarterly | Stream separation (enrolled/certified/capacity) |
| `fact_training_outcomes` | PMKVY, DGT | Quarterly | Certification rate; placement tracking lag |
| `fact_skill_signal` | NCS, job portals | Monthly | Skill extraction from text; frequency normalization |
| `fact_employer_signal` | MCA, EPFO, surveys | Quarterly | Enterprise mapping to sector; sentiment scoring |

**Dependencies:** Waves 1-4 complete
**Parallelizable:** Each fact table independent (but share dim lookups)
**Critical Gates per Fact Table:**
1. Row count > 0 for expected geography × occupation × period
2. No FK violations (all district_id, occupation_id, etc. exist)
3. Check constraints pass (non-negative counts)
4. Data quality score ≥ 70 (else → quarantine)
5. Lineage recorded for every batch

**Rollback per Fact Table:** `TRUNCATE fact_xxx RESTART IDENTITY` + delete `dataset_registry` entries for batch

---

### Wave 6: Analytics & Intelligence (Week 6-8)

| Component | Input | Output | Gate |
|-----------|-------|--------|------|
| Demand Index Engine | `fact_job_demand` | `demand_index` (0-100) components | DI-1.0 formula matches BRAIN.md |
| Supply Index Engine | `fact_workforce_supply`, `fact_training_capacity` | `supply_index` (0-100) | SI-1.0 formula matches BRAIN.md |
| Forecasting | Historical indices | `forecast_demand`, `forecast_supply` | Walk-forward WAPE < Seasonal Naive |
| Skill Gap | Demand + Supply indices | `skill_gap` + `risk_alert` | RADAR classifications match BRAIN.md §3.3 |
| Model Registry | Training runs | `model_registry`, `model_run`, `model_metric` | All metrics recorded; champion flagged |

**Dependencies:** Wave 5 complete
**Parallelizable:** Demand/Supply indices parallel; Forecasting after indices; Gap after forecasts

---

### Wave 7: Governance (Continuous)

| Table | Trigger | Content |
|-------|---------|---------|
| `dataset_registry` | Every ingestion batch | source_id, version, row_count, quality_score, data_type, status |
| `data_quality` | Every validation run | completeness_pct, valid_geometry_pct, unmapped_nco_pct, duplicate_count, passed |
| `data_lineage` | Every transformation | target_entity, source_dataset, transformation_pipeline, model_run_id |
| `audit_log` | Every mutating API call | user_id, action, resource, details, ip_address |

---

## 3. Parallelization Map

```
W1: [dim_date] [dim_nsqf_level] [dim_sector]              → 3 parallel
W2: [dim_state] → [dim_district]                           → sequential
W3: [dim_nco] [dim_skill] [dim_qualification]              → 3 parallel
    → [dim_training_program] [dim_training_center]         → 2 parallel (after qualification)
W4: [map_occupation_skill] [map_skill_qualification]       → 2 parallel
W5: [fact_job_demand] [fact_workforce_supply] [fact_training_capacity] [fact_training_outcomes] [fact_skill_signal] [fact_employer_signal]  → 6 parallel
W6: [demand_index] [supply_index] → [forecasting] → [gap/radar] → [model_registry]
W7: Continuous (hooks in each wave)
```

**Estimated Total Duration:** 8 weeks (with 2 engineers parallelizing within waves)

---

## 4. Rollback Procedures

### Per-Batch Rollback (Single Ingestion Run)

```sql
-- 1. Identify batch
SELECT * FROM dataset_registry WHERE dataset_id = 'DS-NCS-2026-10';

-- 2. Delete fact rows for this batch
DELETE FROM fact_job_demand WHERE source_id = 'SRC-NCS-FEED' AND dataset_type = 'REAL' AND date_key >= '2026-10-01';

-- 3. Delete lineage
DELETE FROM data_lineage WHERE source_dataset_id = 'DS-NCS-2026-10';

-- 4. Delete quality records
DELETE FROM data_quality WHERE dataset_id = 'DS-NCS-2026-10';

-- 5. Mark registry as ROLLED_BACK
UPDATE dataset_registry SET status = 'ROLLED_BACK' WHERE dataset_id = 'DS-NCS-2026-10';

-- 6. Audit log
INSERT INTO audit_log (user_id, action, resource, details, ip_address)
VALUES (current_user, 'ROLLBACK_INGESTION', 'fact_job_demand', '{"dataset_id": "DS-NCS-2026-10"}', inet_client_addr());
```

### Per-Wave Rollback (Catastrophic Failure)

```bash
# Run wave-specific rollback script
python scripts/rollback_wave.py --wave 5 --confirm

# Script executes TRUNCATE in reverse FK order
# Requires explicit --confirm flag
```

### Full Database Reset (Nuclear Option)

```bash
# Only in development — never production
alembic downgrade base
alembic upgrade head
python -m backend.app.services.data.seed_runner --fixtures-only
```

---

## 5. Idempotency Verification

**Requirement:** Every ingestion run must be re-runnable with identical results.

**Test Protocol:**
1. Run ingestion for batch `B1` → record row counts per table
2. Re-run ingestion for batch `B1` → record row counts
3. Assert: all counts identical (zero duplicates)
4. Assert: `dataset_registry` has single entry for `B1` (status = ACTIVE)
5. Assert: `data_lineage` entries unchanged

**Implementation:** All fact tables use `INSERT ... ON CONFLICT (unique_key) DO UPDATE SET ...` or `DO NOTHING` depending on update policy.

**Unique Keys (Business Keys):**
- `fact_job_demand`: (district_id, occupation_id, date_key)
- `fact_workforce_supply`: (district_id, occupation_id, date_key)
- `fact_training_capacity`: (center_id, qualification_id, date_key)
- `fact_training_outcomes`: (center_id, qualification_id, date_key)
- `fact_skill_signal`: (district_id, skill_id, date_key)
- `fact_employer_signal`: (district_id, sector_id, date_key)

---

## 6. Monitoring & Alerting

| Metric | Threshold | Action |
|--------|-----------|--------|
| Ingestion duration | > 30 min (per fact table) | Alert on-call; check for stuck transaction |
| Data quality score | < 70 | Quarantine batch; manual review required |
| FK violation count | > 0 | Hard fail; rollback batch |
| Duplicate row count | > 0 | Alert; investigate idempotency bug |
| PII detection | Any | **Critical alert**; security team; hard reject |
| Disk usage (raw) | > 50 GB | Cleanup old raw files (>90 days post-ingestion) |

---

## 7. Milestone Gates

| Milestone | Criteria | Verification |
|-----------|----------|--------------|
| **M1: Dimensions Ready** | Waves 1-4 complete; all FKs valid; 100% FK coverage | `pytest backend/tests/integration/test_dimensions.py` |
| **M2: Facts Loaded** | Wave 5 complete; all 6 fact tables have data for ≥3 states, ≥10 occupations, ≥12 months | Row count queries; data quality reports |
| **M3: Indices Computed** | Demand/Supply indices (0-100) for all district-occupation-period tuples | Spot-check against manual calculation |
| **M4: Forecasts Generated** | Champion model forecasts for all 5 horizons (3,6,12,18,24) | WAPE < Seasonal Naive on validation folds |
| **M5: Gap + RADAR Live** | skill_gap + risk_alert populated; classifications match BRAIN.md | `pytest backend/tests/integration/test_gap_radar.py` |
| **M6: System Ready for Phase 7** | All APIs return data; frontend can query; copilot tools work | E2E test suite passes |

---

## 8. Resource Requirements

| Resource | Specification |
|----------|---------------|
| **Compute** | 8 vCPU, 32 GB RAM for ingestion workers (parallel fact loads) |
| **Database** | PostgreSQL 16 + PostGIS; 500 GB SSD; connection pool 20 |
| **Storage (Raw)** | 100 GB for raw artifacts (90-day retention) |
| **Storage (Staging)** | 50 GB for intermediate Parquet/JSON |
| **Network** | 1 Gbps for downloads; API rate limits respected |
| **Personnel** | 2 Data Engineers (parallel waves); 1 QA for validation |

---

## 9. Risk Register

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| NCS API credentials delayed | High | Blocks `fact_job_demand` real data | Develop with `SRC-FIXTURE-IND`; switch when creds arrive |
| PLFS microdata access denied | Medium | Forces use of aggregated reports only | Document limitation; use small-area estimation models |
| e-Shram PII in aggregates | Low | Security incident | Automated PII guard (already implemented); manual spot-check |
| District boundary changes | Medium | FK violations in fact tables | Versioned geography; `dim_district` effective_from/effective_to |
| NCO mapping coverage < 80% | Medium | Gaps in demand/supply by occupation | Manual mapping sprint; track `unmapped_nco_pct` in quality |
| PMKVY stream confusion | High | Enrolled ≠ certified conflated | Strict adapter separation (already coded); unit tests enforce |

---

## 10. Next Actions

1. **Immediate:** Confirm raw data acquisition status (`docs/DATA_ACQUISITION_STATUS.md`)
2. **Week 1:** Execute Waves 1-2 (Dimensions + Geography)
3. **Week 2:** Execute Wave 3 (Core Taxonomy) — NCO parser critical path
4. **Week 3:** Execute Waves 4-5 (Mappings + Facts) — parallel fact loads
5. **Week 4:** Execute Wave 6 (Analytics) — Demand/Supply indices first
6. **Week 5:** Forecasting pipeline + Skill Gap + RADAR
7. **Week 6:** Model Registry + Governance hooks
8. **Week 7:** Reconciliation Gate (Phase 6) — produce `PHASE4_REAL_DATA_MIGRATION_REPORT.md`
9. **Week 8:** Phase 7 API Read Model implementation