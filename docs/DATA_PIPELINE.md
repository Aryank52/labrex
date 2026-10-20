# LABREX Data Ingestion & Pipeline Architecture

**Document Version:** 1.0  
**Authority:** Master Directive Section 13, 14 & Secondary Ingestion Mandate  
**Engineering Standard:** Medallion Staging Architecture (Raw -> Bronze -> Silver -> Gold)  
**Strict Rule:** No bypass of data quality verification or lineage tracking.

---

## 1. End-to-End Pipeline Architecture

```mermaid
flowchart TD
    subgraph S["Source Acquisition Gate (Layer 0)"]
        S1["SRC-NCO-2015<br/>Gazetted Standards"]
        S2["SRC-PLFS-ANN<br/>MoSPI Survey Microdata"]
        S3["SRC-NCS-FEED<br/>MoLE Vacancy Feed"]
        S4["SRC-ESHRAM-AGG<br/>Unorganized Aggregates"]
        S5["SRC-PMKVY-OUT<br/>MSDE/NSDC Outcomes"]
        S6["SRC-NSDC-DIR<br/>Accredited Centres"]
        S7["SRC-GEO-ADMIN<br/>Survey of India Polygons"]
    end

    subgraph A["Parser & Adapter Layer"]
        P1["NCOParser<br/>8-digit Hierarchy"]
        P2["PLFSAdapter<br/>LFPR, WPR, UR Rates"]
        P3["NCSAdapter<br/>ConnectionState Gated"]
        P4["EShramAdapter<br/>PII Guard Enforced"]
        P5["PMKVYAdapter<br/>Pipeline/Supply Split"]
        P6["NSDCAdapter<br/>Capacity Directory"]
        P7["GeographyParser<br/>Shapely & SRID:4326"]
    end

    subgraph C["Canonical Staging Tier (Decoupled Contracts)"]
        CS1["CanonicalOccupation"]
        CS2["CanonicalWorkforceSignal"]
        CS3["CanonicalObservation"]
        CS4["CanonicalTrainingSignal"]
        CS5["GeographyValidationResult"]
    end

    subgraph Q["Data Quality & Governance Gate"]
        DQ["DataQualityEngine<br/>- Duplicate check<br/>- Date validation<br/>- Negative count guard<br/>- NCO syntax regex<br/>- Geo parent-child check"]
        REP["DataQualityReport<br/>(Score 0-100)"]
        LIN["LineageTracker<br/>(SHA-256 Digest & Audit)"]
    end

    subgraph M["Target Medallion Stores"]
        BRONZE["Bronze Layer<br/>Raw JSONB Staging"]
        SILVER["Silver Layer<br/>Deduplicated, NCO-Mapped"]
        GOLD["Gold Layer<br/>Star Schema Dimensions & Facts"]
    end

    S1 --> P1 --> CS1 --> DQ
    S2 --> P2 --> CS2 --> DQ
    S3 --> P3 --> CS3 --> DQ
    S4 --> P4 --> CS2 --> DQ
    S5 --> P5 --> CS4 --> DQ
    S6 --> P6 --> CS4 --> DQ
    S7 --> P7 --> CS5 --> DQ

    DQ --> REP
    DQ --> LIN
    DQ -->|Score >= 70| BRONZE
    DQ -->|< 70 (Fails)| QUAR["Quarantine Store"]
    BRONZE --> SILVER --> GOLD
```

---

## 2. Ingestion Lifecycles & Adapter Contracts

### 2.1 The Connection State Machine (NCS Adapter)
External demand signals via NCS support four explicit, typed states:
1. `NOT_CONFIGURED`: Default local developer state when credentials/endpoints are absent in `.env`. Does not crash; serves verified fallback fixtures or staged offline extracts.
2. `AVAILABLE`: Verified HTTP 200 connection to authorized endpoint.
3. `RATE_LIMITED`: HTTP 429 response detected. Implements exponential backoff with random jitter.
4. `UNAVAILABLE`: HTTP 5xx or connection timeout. Triggers circuit breaker and logs alert.

### 2.2 PII Security Guard (e-Shram Adapter)
Before parsing incoming rows:
- `verify_no_pii(field_names)` examines all column keys against the blacklist: `aadhaar`, `uidai`, `mobile`, `phone`, `worker_name`, `bank_account`, `dob`.
- If any forbidden identifier is found, `PIISafetyViolationError` is raised immediately, halting ingestion and generating a critical security audit record.

### 2.3 Skilling Stream Separation (PMKVY Adapter)
To prevent conflating trainees currently in classes with fully qualified workers, the adapter emits 3 mutually exclusive signal streams:
1. `TRAINING_PIPELINE`: Enrolled and ongoing trainees (`candidates_enrolled_pipeline`).
2. `CERTIFIED_SUPPLY`: Assessed, passed, and certified graduates (`candidates_certified_supply`).
3. `INFRASTRUCTURE_CAPACITY`: Training centre count and sanctioned seats (`training_centre_capacity`).

---

## 3. Canonical Staging Contract Specifications

All ingestion adapters produce typed Pydantic v2 schemas defined in `backend/app/schemas/staging.py`:
- `CanonicalObservation`: General demand, posting, and macroeconomic observations.
- `CanonicalOccupation`: NCO-2015 8-digit taxonomic hierarchy.
- `CanonicalSkillSignal`: Emerging skills, qualification packs, and NSQF levels.
- `CanonicalTrainingSignal`: Pipeline, supply, and institutional seating capacities.
- `CanonicalWorkforceSignal`: PLFS rates (LFPR, WPR, UR) and e-Shram unorganized registration counts.

---

## 4. Error Handling, Retry Policies, and Circuit Breakers

| Exception / Event | Handling Policy | Retry Strategy | Target Severity |
| :--- | :--- | :--- | :--- |
| `PIISafetyViolationError` | Abort batch immediately, purge memory buffer | Zero retry (Security Lock) | `CRITICAL` |
| `FileNotFoundError` | Log missing file alert, fallback to test fixture | No retry | `ERROR` |
| `ChecksumMismatchError` | Reject corrupted file | Operator intervention required | `CRITICAL` |
| `HTTP 429 Rate Limited` | Throttle request pipeline | Exponential backoff (1s, 2s, 4s, 8s max 30s) | `WARNING` |
| `HTTP 503 Unavailable` | Trip circuit breaker, switch to offline cache | 3 retries over 5 minutes | `ERROR` |
| `QualityScore < 70` | Divert batch to quarantine table | Manual review flag | `ERROR` |
