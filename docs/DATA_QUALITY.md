# LABREX Data Quality Framework & Evaluation Specification

**Document Version:** 1.0  
**Authority:** Master Directive Section 13, 93 & Secondary Mandate Step 12  
**Standard:** Automated verification, continuous monitoring, and auditable scoring (0–100).  
**Compliance Standard:** ISO/IEC 25012 Data Quality Model.

---

## 1. Core Data Quality Dimensions

The LABREX Data Quality Engine evaluates every ingestion batch across 6 foundational quality dimensions:
1. **Completeness**: Absence of nulls in primary keys, dates, and essential metrics.
2. **Validity**: Strict conformance to regular expressions, ranges, and enum domains (e.g. NCO regex, state codes).
3. **Accuracy / Plausibility**: Physical bounds checking (e.g. rates between 0–100%, non-negative counts).
4. **Consistency**: Relational parent-child integrity (e.g. district mapped to correct state, certified $\le$ trained).
5. **Uniqueness**: Prevention of duplicate records sharing identical natural keys.
6. **Freshness & Timeliness**: Tracking observation latency against statutory publication cadences.

---

## 2. Mathematical Scoring Formulation

For a given batch $B$ containing $N$ records, the overall Data Quality Score $Q(B) \in [0, 100]$ is computed as:

$$Q(B) = \max\left(0.0, 100.0 - \frac{1}{N} \sum_{i=1}^{N} \sum_{v \in V(r_i)} W(v)\right)$$

Where:
- $V(r_i)$ is the set of quality violations detected on record $r_i$.
- $W(v)$ is the penalty weight associated with the violation severity:

| Severity Level | Penalty Weight $W(v)$ | Example Violations |
| :--- | :---: | :--- |
| `CRITICAL` | **20.0** | PII leakage detected, negative count for postings/seats, unparseable date |
| `ERROR` | **5.0** | Unrecognized state code, duplicate natural key, date outside 1990–2035 |
| `WARNING` | **1.0** | NCO non-standard code regex, data staleness exceeding threshold |
| `INFO` | **0.0** | Minor formatting anomalies, soft whitespace trims |

### Batch Quality Status Gates
- **`PASSED`** ($Q(B) \ge 85.0$ and zero critical/error violations): Batch advances automatically to Silver/Gold layers.
- **`WARNING`** ($70.0 \le Q(B) < 85.0$): Batch lands in staging with flagged warning alerts; discounted in analytical confidence calculations.
- **`FAILED`** ($Q(B) < 70.0$ or any `CRITICAL` violation): Batch is rejected from landing in dimensional facts and diverted to the Quarantine Store (`stg_quarantined_records`).

---

## 3. Implemented Validation Rules

### 3.1 Rule: `MISSING_DATE`
- **Assertion**: `observation_date IS NOT NULL AND 1990 <= observation_date.year <= 2035`.
- **Severity**: `CRITICAL` if null; `ERROR` if out of bounds.

### 3.2 Rule: `INVALID_GEOGRAPHY`
- **Assertion**: `geography.state_code IN VALID_INDIAN_STATES` (36 official States and UTs).
- **Severity**: `ERROR`.

### 3.3 Rule: `INVALID_STATE_DISTRICT_MAPPING`
- **Assertion**: For district code `IN-XX-YYY`, the prefix `IN-XX` must equal `geography.state_code`.
- **Severity**: `ERROR`.

### 3.4 Rule: `DUPLICATE_RECORD`
- **Assertion**: Each `source_record_id` must be unique within an ingestion batch.
- **Severity**: `ERROR`.

### 3.5 Rule: `NEGATIVE_COUNT`
- **Assertion**: For metrics with units in `{"count", "vacancies", "candidates", "seats"}`, `value >= 0`.
- **Severity**: `CRITICAL`.

### 3.6 Rule: `INVALID_OCCUPATION_CODE`
- **Assertion**: `occupation.nco_code` must match regex `^([0-9]{1,4}|[0-9]{4}\.[0-9]{2,4})$`.
- **Severity**: `WARNING`.

### 3.7 Rule: `SOURCE_STALENESS`
- **Assertion**: `(today - observation_date).days <= max_staleness_days`.
- **Severity**: `WARNING`.

### 3.8 Rule: `PII_LEAKAGE`
- **Assertion**: Attribute names and values must not contain tokens matching Aadhaar, phone, name, or bank account.
- **Severity**: `CRITICAL`.

---

## 4. `DataQualityReport` Schema

```json
{
  "dataset_id": "SRC-PMKVY-OUT",
  "batch_id": "BAT-20261020-001",
  "timestamp": "2026-10-20T10:00:00Z",
  "total_records": 1000,
  "passed_records": 998,
  "failed_records": 2,
  "overall_quality_score": 98.5,
  "status": "PASSED",
  "execution_time_ms": 12.4,
  "violations": [],
  "summary": {
    "violation_count": 0,
    "critical_violations": 0,
    "error_violations": 0,
    "warning_violations": 0
  }
}
```
