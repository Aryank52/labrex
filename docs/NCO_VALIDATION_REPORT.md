# LABREX NCO-2015 Parser Validation Report

**Document Version:** 1.0  
**Authority:** Master Directive Section 14, 93  
**Phase:** 4 (Data Ingestion) — Pre-Ingestion Validation  
**Status:** Template — Populate After Parser Execution

---

## 1. Executive Summary

| Metric | Target | Actual | Status |
|--------|--------|--------|--------|
| Total NCO Codes Parsed | ~3,500 (8-digit) | TBD | ⬜ |
| Hierarchy Levels Complete | 5 (Div → SubDiv → Group → Family → Occupation) | TBD | ⬜ |
| Division Coverage (1-digit) | 9 (0-9, excl. 0=Armed Forces) | TBD | ⬜ |
| Sub-Division Coverage (2-digit) | ~80 | TBD | ⬜ |
| Group Coverage (3-digit) | ~200 | TBD | ⬜ |
| Family Coverage (4-digit) | ~500 | TBD | ⬜ |
| Occupation Coverage (8-digit) | ~3,500 | TBD | ⬜ |
| Description Preservation | 100% non-empty | TBD | ⬜ |
| Sector Mapping Accuracy | ≥ 95% | TBD | ⬜ |
| Fixture Representativeness | ≥ 80% of sectors | TBD | ⬜ |
| Parser Determinism | 100% (re-run = identical) | TBD | ⬜ |

**Overall Validation Status:** ⬜ PENDING / ⬜ PASSED / ⬜ FAILED

---

## 2. Source Artifact Verification

| Artifact | File | SHA-256 | Rows (CSV) | Pages (PDF) | Verified |
|----------|------|---------|------------|-------------|----------|
| Vol I Code Structure | `nco_2015_vol_i_code_structure.csv` | | | N/A | ⬜ |
| Vol II Descriptions | `nco_2015_vol_ii_descriptions.csv` | | | N/A | ⬜ |
| Vol I Code Structure | `nco_2015_vol_i_code_structure.pdf` | | N/A | | ⬜ |
| Vol II Descriptions | `nco_2015_vol_ii_descriptions.pdf` | | N/A | | ⬜ |

**PDF-to-CSV Reconciliation:** ⬜ Row counts match / ⬜ Discrepancies documented

---

## 3. Hierarchy Integrity Checks

### 3.1 Division Level (1-digit)

| Division | Code | Title | Sub-Divisions Count | Status |
|----------|------|-------|---------------------|--------|
| 0 | Armed Forces | | | ⬜ |
| 1 | Legislators, Senior Officials & Managers | | | ⬜ |
| 2 | Professionals | | | ⬜ |
| 3 | Technicians & Associate Professionals | | | ⬜ |
| 4 | Clerks | | | ⬜ |
| 5 | Service Workers & Shop/Market Sales | | | ⬜ |
| 6 | Skilled Agricultural & Fishery Workers | | | ⬜ |
| 7 | Craft & Related Trades Workers | | | ⬜ |
| 8 | Plant & Machine Operators & Assemblers | | | ⬜ |
| 9 | Elementary Occupations | | | ⬜ |

**Validation Rules:**
- [ ] All 10 divisions present (0-9)
- [ ] No duplicate division codes
- [ ] Each division has ≥ 1 sub-division

### 3.2 Sub-Division Level (2-digit)

| Check | Expected | Actual | Status |
|-------|----------|--------|--------|
| Total sub-divisions | ~80 | | ⬜ |
| All parent divisions valid | 100% | | ⬜ |
| No orphan sub-divisions | 0 | | ⬜ |

### 3.3 Group Level (3-digit)

| Check | Expected | Actual | Status |
|-------|----------|--------|--------|
| Total groups | ~200 | | ⬜ |
| All parent sub-divisions valid | 100% | | ⬜ |

### 3.4 Family Level (4-digit)

| Check | Expected | Actual | Status |
|-------|----------|--------|--------|
| Total families | ~500 | | ⬜ |
| All parent groups valid | 100% | | ⬜ |

### 3.5 Occupation Level (8-digit)

| Check | Expected | Actual | Status |
|-------|----------|--------|--------|
| Total occupations | ~3,500 | | ⬜ |
| All parent families valid | 100% | | ⬜ |
| Code format: `DDDD.DDDD` | 100% | | ⬜ |
| No duplicate 8-digit codes | 0 | | ⬜ |

---

## 4. Description Preservation

| Metric | Vol I (Structure) | Vol II (Descriptions) | Combined |
|--------|-------------------|----------------------|----------|
| Records with title | | | |
| Records with description | | | |
| Empty descriptions | | | |
| Truncated descriptions | | | |
| Description length (avg chars) | | | |

**Requirement:** Every occupation must have non-empty `title` from Vol I and non-empty `description` from Vol II.

---

## 5. Sector Mapping Accuracy

| Sector | NCO Divisions Mapped | Occupations Mapped | Coverage % | Confidence |
|--------|---------------------|-------------------|------------|------------|
| SEC-AUTO (Automotive) | | | | |
| SEC-IT (IT-ITeS) | | | | |
| SEC-ELEC (Electronics) | | | | |
| SEC-HEALTH (Healthcare) | | | | |
| SEC-CONST (Construction) | | | | |
| SEC-TEXT (Textiles) | | | | |
| SEC-RENEW (Renewable Energy) | | | | |
| SEC-LOG (Logistics) | | | | |
| SEC-BFSI (Banking/Financial) | | | | |
| SEC-RETAIL (Retail) | | | | |
| SEC-TOUR (Tourism/Hospitality) | | | | |
| SEC-AGRI (Agriculture) | | | | |
| **TOTAL** | | | | |

**Mapping Method:** Automated keyword matching + manual review of top 200 occupations per sector.
**Unmapped Occupations:** Count = _____ ; Top 10 listed in Appendix.

---

## 6. Fixture Representativeness

The deterministic fixture set (`SRC-FIXTURE-IND`) must cover key sectors for development.

| Fixture Sector | NCO Divisions | Occupations in Fixture | Real Data Coverage % |
|----------------|---------------|------------------------|---------------------|
| Automotive & EV | 7, 8 | | |
| IT-ITeS & AI | 2, 3 | | |
| Renewable & Solar | 7, 8 | | |
| Healthcare | 2, 3, 5 | | |
| Construction | 6, 7 | | |
| **TOTAL** | | | |

**Requirement:** Fixture occupations must map to real NCO codes that exist in parsed data.

---

## 7. Parser Determinism Test

| Run | Total Codes | SHA-256 of Output JSON | Identical to Run 1? |
|-----|-------------|------------------------|---------------------|
| 1 | | | — |
| 2 | | | ⬜ YES / ⬜ NO |
| 3 | | | ⬜ YES / ⬜ NO |

**Requirement:** All runs produce identical output (deterministic parsing).

---

## 8. Edge Cases & Anomalies

| Issue ID | Code | Description | Resolution | Status |
|----------|------|-------------|------------|--------|
| | | | | |

---

## 9. ISCO-08 Concordance

| NCO Division | ISCO-08 Major Group | Mapping Confidence |
|--------------|---------------------|-------------------|
| 1 | 1 (Managers) | |
| 2 | 2 (Professionals) | |
| 3 | 3 (Technicians) | |
| 4 | 4 (Clerical) | |
| 5 | 5 (Service/Sales) | |
| 6 | 6 (Skilled Agri) | |
| 7 | 7 (Craft/Trades) | |
| 8 | 8 (Plant/Machine) | |
| 9 | 9 (Elementary) | |

**Note:** NCO-2015 is aligned to ISCO-08. Document any deviations.

---

## 10. Sign-Off

| Role | Name | Date | Signature |
|------|------|------|-----------|
| Data Engineer (Parser) | | | |
| Data Engineer (Reviewer) | | | |
| Domain Expert (SSC) | | | |
| Principal Engineering Agent | | | |

**Validation Complete:** ⬜ YES / ⬜ NO  
**Approved for Ingestion:** ⬜ YES / ⬜ NO

---

## Appendix A: Unmapped Occupations (Top 20 by Expected Demand)

| NCO Code | Title | Division | Reason Unmapped |
|----------|-------|----------|-----------------|
| | | | |

## Appendix B: Parser Configuration

```yaml
parser_version: "1.0"
vol_i_columns: [nco_code, title, division, sub_division, group_code, family_code]
vol_ii_columns: [nco_code, description]
code_format_regex: "^\\d{4}\\.\\d{4}$"
hierarchy_delimiter: "."
encoding: "utf-8"
```

## Appendix C: Reproduction Command

```bash
python -m labrex.data.adapters.nco_parser \
  --vol-i data/raw/nco/YYYYMMDD/nco_2015_vol_i_code_structure.csv \
  --vol-ii data/raw/nco/YYYYMMDD/nco_2015_vol_ii_descriptions.csv \
  --output data/staged/nco_parsed_YYYYMMDD.json \
  --report docs/NCO_VALIDATION_REPORT.md
```