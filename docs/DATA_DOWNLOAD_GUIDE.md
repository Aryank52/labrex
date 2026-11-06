# LABREX Data Download Guide

**Document Version:** 2.0  
**Authority:** Master Directive Section 14, 93  
**Audience:** Data Engineers, Operators, Analysts  
**Compliance:** MoSPI NDSAP, MeitY Open Government Data Guidelines

---

## 1. Overview

This guide provides step-by-step procedures for acquiring all official datasets required by LABREX. Each source has unique access requirements, authentication methods, and file formats. **Never assume a filename represents actual contents — always inspect every artifact.**

---

## 2. Source-Specific Download Procedures

### 2.1 NCO-2015 (National Classification of Occupations)

| Field | Value |
|-------|-------|
| **Source ID** | `SRC-NCO-2015` |
| **Authority** | Ministry of Labour & Employment (MoLE), Directorate General of Employment |
| **Official URL** | `https://labour.gov.in/national-classification-occupations-nco` |
| **Access Method** | Public document download (no auth) |
| **Required Files** | Vol I (Code Structure), Vol II (Occupational Descriptions) |
| **Format** | PDF (official), CSV/XLSX (machine-readable tables from OGD) |
| **Validation** | SHA-256 checksums in `data/manifests/nco.yaml` |

**Procedure:**
1. Navigate to `https://labour.gov.in/national-classification-occupations-nco`
2. Download **Volume I** (NCO 2015 Code Structure) — PDF
3. Download **Volume II** (Occupational Descriptions) — PDF
4. Check OGD portal (`https://data.gov.in/`) for machine-readable CSV/XLSX versions
5. Save to `data/raw/nco/YYYYMMDD/` with original filenames
6. Run `python -m labrex.data.register_file --source SRC-NCO-2015 --dir data/raw/nco/YYYYMMDD/`
7. Run `python -m labrex.data.validate_raw --source SRC-NCO-2015 --dir data/raw/nco/YYYYMMDD/`

**Expected Files:**
```
data/raw/nco/20261104/
├── nco_2015_vol_i_code_structure.pdf
├── nco_2015_vol_i_code_structure.csv
├── nco_2015_vol_ii_descriptions.pdf
└── nco_2015_vol_ii_descriptions.csv
```

---

### 2.2 PLFS (Periodic Labour Force Survey)

| Field | Value |
|-------|-------|
| **Source ID** | `SRC-PLFS-ANN` |
| **Authority** | MoSPI / NSSO |
| **Official URL** | `https://microdata.gov.in/`, `https://www.mospi.gov.in/` |
| **Access Method** | Microdata portal (registration required) + public annual reports |
| **Required Rounds** | 2019-20, 2020-21, 2021-22, 2022-23, 2023-24, 2024 (redesigned), 2025 (quarterly) |
| **Format** | Fixed-width .TXT + layout dictionary (.do/.sps) for microdata; XLSX/CSV for reports |
| **Validation** | Row counts, survey weights, geographic coverage per round |

**Procedure:**
1. **Microdata (restricted):**
   - Register at `https://microdata.gov.in/`
   - Request access to PLFS unit-level data
   - Download fixed-width .TXT files + layout dictionaries for each round
   - Save to `data/raw/plfs/microdata/ROUND/`

2. **Annual Reports (public):**
   - Download from `https://www.mospi.gov.in/plfs-annual-report`
   - Files: `plfs_annual_report_YYYY-YY.pdf`, `plfs_key_indicators_YYYY-YY.xlsx`
   - Save to `data/raw/plfs/reports/YYYY/`

3. **Quarterly Bulletins (public, urban only):**
   - Download from MoSPI website
   - Save to `data/raw/plfs/quarterly/YYYYQN/`

4. Run validation for each round:
   ```bash
   python -m labrex.data.register_file --source SRC-PLFS-ANN --dir data/raw/plfs/reports/2023-24/
   python -m labrex.data.validate_raw --source SRC-PLFS-ANN --dir data/raw/plfs/reports/2023-24/
   ```

**Critical Notes:**
- **2025 PLFS is redesigned** — different sampling frame, different variable names. Treat separately from historical July-June rounds.
- **Row count ≠ workforce population** — always apply survey weights (`multiplier` / `weight` columns).
- Preserve original survey methodology documentation (PDF reports) for lineage.

---

### 2.3 PMKVY (Pradhan Mantri Kaushal Vikas Yojana)

| Field | Value |
|-------|-------|
| **Source ID** | `SRC-PMKVY-OUT` |
| **Authority** | MSDE / NSDC |
| **Official URL** | `https://www.pmkvyofficial.org/`, `https://www.skillindiadigital.gov.in/` |
| **Access Method** | MSDE Open Data, SIDH Portal, Parliamentary disclosures |
| **Required Series** | PMKVY 1.0, 2.0, 3.0, 4.0 |
| **Format** | CSV/XLSX |
| **Key Separation** | **Enrolled** (training pipeline) ≠ **Certified** (effective supply) ≠ **Placed** |

**Procedure:**
1. Download PMKVY 4.0 dashboard data from Skill India Digital Hub
2. Download historical PMKVY 1.0-3.0 from MSDE annual reports / Lok Sabha Q&A
3. **Critical:** Separate files by stream:
   - `pmkvy4_enrolled_YYYY.csv` — currently in training
   - `pmkvy4_certified_YYYY.csv` — assessed & certified
   - `pmkvy4_placed_YYYY.csv` — placement tracked
   - `pmkvy4_centres_YYYY.csv` — infrastructure capacity
3. Save to `data/raw/pmkvy/YYYY/STREAM/`
4. Run validation per stream

**Expected Structure:**
```
data/raw/pmkvy/
├── 2023-24/
│   ├── enrolled/
│   │   └── pmkvy4_enrolled_2023-24.csv
│   ├── certified/
│   │   └── pmkvy4_certified_2023-24.csv
│   ├── placed/
│   │   └── pmkvy4_placed_2023-24.csv
│   └── centres/
│       └── pmkvy4_centres_2023-24.csv
└── historical/
    ├── pmkvy1/, pmkvy2/, pmkvy3/ (same structure)
```

---

### 2.4 e-Shram (Unorganised Worker Registry)

| Field | Value |
|-------|-------|
| **Source ID** | `SRC-ESHRAM-AGG` |
| **Authority** | MoLE |
| **Official URL** | `https://eshram.gov.in/eshramportal/publicDashboard` |
| **Access Method** | Public dashboard export / Parliamentary answers |
| **Format** | CSV/XLSX/JSON (dashboard summary cards) |
| **Frequency** | Monthly cumulative snapshots |
| **PII Guard** | **CRITICAL** — Never ingest microdata. Only district-level aggregates. |

**Procedure:**
1. Navigate to e-Shram public dashboard
2. Export **district-level aggregates only** (state, district, occupation sector, worker count, gender ratio)
3. **Verify no PII columns:** Aadhaar, mobile, name, bank account, DOB, address
4. Save to `data/raw/eshram/YYYYMM/`
5. Run PII guard validation:
   ```bash
   python -m labrex.data.validate_raw --source SRC-ESHRAM-AGG --dir data/raw/eshram/202610/
   ```

**Mandatory Checklist:**
- [ ] File contains only aggregate counts (no individual records)
- [ ] Columns: `state_code`, `district_code`, `occupation_sector`, `worker_count`, `male_ratio`, `female_ratio`, `snapshot_date`
- [ ] No columns matching: `aadhaar`, `mobile`, `phone`, `name`, `account`, `dob`, `address`
- [ ] SHA-256 recorded in lineage

---

### 2.5 NCS (National Career Service)

| Field | Value |
|-------|-------|
| **Source ID** | `SRC-NCS-FEED` |
| **Authority** | MoLE / NCS |
| **Official URL** | `https://www.ncs.gov.in/`, `https://api.ncs.gov.in/` |
| **Access Method** | Gated API (credentials required) + OGD monthly releases |
| **Connection States** | `NOT_CONFIGURED` (default), `AVAILABLE`, `RATE_LIMITED`, `UNAVAILABLE` |
| **Format** | JSON (API), CSV/ZIP (batch) |
| **Key Distinction** | Cumulative vacancy snapshots ≠ time-period vacancy flows |

**Procedure:**
1. **If API credentials available:**
   - Configure `NCS_API_KEY`, `NCS_API_ENDPOINT` in `.env`
   - Run `python -m labrex.data.adapters.ncs_adapter --mode api --since 2026-01-01`
   - Handle rate limiting with exponential backoff
2. **If no credentials (default):**
   - Download monthly batch releases from `https://data.gov.in/`
   - Save to `data/raw/ncs/YYYYMM/`
   - Mark source status as `NOT_CONFIGURED` in `dim_source`

**Validation:**
- Distinguish `active_postings` (snapshot) from `new_postings` (flow)
- Verify NCO code format (8-digit)
- Check geographic coverage (state/district codes valid)

---

### 2.6 NQR / NSDC (National Qualification Register / Training Directory)

| Field | Value |
|-------|-------|
| **Source ID** | `SRC-NSDC-DIR` |
| **Authority** | NSDC / NCVET |
| **Official URL** | `https://nsdcindia.org/`, `https://nqr.gov.in/` |
| **Access Method** | Public web directory / NQR open register exports |
| **Datasets** | Primary ~14k catalogue + Secondary ~2.8k reference dataset |
| **Format** | CSV/JSON/XLSX |

**Procedure:**
1. Download NQR primary catalogue (`nqr_primary_YYYYMMDD.csv`)
2. Download NQR secondary reference (`nqr_secondary_YYYYMMDD.csv`)
3. Download NSDC training partner directory
4. **Do not silently deduplicate** — document why records are merged/dropped
5. Save to `data/raw/nsdc/YYYYMMDD/`
6. Run validation

**Deduplication Rules (Document in Lineage):**
- Primary key: `qualification_id` (QP code)
- If duplicate QP: keep most recent `curriculum_version`
- Log all dropped records with reason

---

### 2.7 Administrative Boundaries (Geography)

| Field | Value |
|-------|-------|
| **Source ID** | `SRC-GEO-ADMIN` |
| **Authority** | Survey of India / MoPR (LGD) |
| **Official URL** | `https://lgdirectory.gov.in/`, `https://onlinemaps.surveyofindia.gov.in/` |
| **Access Method** | Survey of India Open Data / Bharat Maps / LGD API |
| **Required Files** | `state_nwic_shp.zip`, `district_nwic_shp.zip` |
| **Format** | Shapefile (.shp) / GeoJSON |
| **CRS** | EPSG:4326 (WGS84) mandatory |
| **Hierarchy** | State → District (strict parent-child via LGD codes) |

**Procedure:**
1. Download `state_nwic_shp.zip` from Survey of India / LGD
2. Download `district_nwic_shp.zip` from Survey of India / LGD
3. Extract and convert to GeoJSON:
   ```bash
   ogr2ogr -f GeoJSON -t_srs EPSG:4326 states.geojson state_nwic_shp.shp
   ogr2ogr -f GeoJSON -t_srs EPSG:4326 districts.geojson district_nwic_shp.shp
   ```
4. Validate with geography parser:
   ```bash
   python -m labrex.data.validate_raw --source SRC-GEO-ADMIN --dir data/raw/geography/20261104/
   ```
5. **Validation Checks:**
   - Geometry validity (`is_valid`, non-empty, exterior ring closed)
   - CRS = EPSG:4326
   - Parent-child: `district.state_id == state.state_id` (LGD codes)
   - India bounding envelope: [6°N, 38°N] × [68°E, 98°E]

---

## 3. Universal Post-Download Checklist

For **every** downloaded artifact:

```bash
# 1. Register file (computes SHA-256, matches manifest)
python -m labrex.data.register_file --source SRC-XXX --dir data/raw/xxx/YYYYMMDD/

# 2. Validate raw (schema, PII, format, geography)
python -m labrex.data.validate_raw --source SRC-XXX --dir data/raw/xxx/YYYYMMDD/

# 3. Inspect output — verify:
#    - File count matches manifest
#    - SHA-256 matches expected (if in manifest)
#    - No PII detected
#    - Geometry valid (for geo sources)
#    - NCO codes valid format (for occupation sources)
#    - Row counts reasonable (not 0, not implausibly high)

# 4. If validation passes → move to staging
#    python -m labrex.data.ingest --source SRC-XXX --batch-id YYYYMMDD-HHMMSS
```

---

## 4. Manifest Files

Manifests in `data/manifests/*.yaml` define expected files per source. **Update manifests when new rounds/releases arrive.**

Example `data/manifests/nco.yaml`:
```yaml
source_id: SRC-NCO-2015
version: "2.0.0"
files:
  - pattern: "nco_2015_vol_i_code_structure.*"
    required: true
    format: [pdf, csv]
    description: "NCO 2015 Volume I - Code Structure"
  - pattern: "nco_2015_vol_ii_descriptions.*"
    required: true
    format: [pdf, csv]
    description: "NCO 2015 Volume II - Occupational Descriptions"
checksums:
  nco_2015_vol_i_code_structure.pdf: "sha256:abc123..."
  nco_2015_vol_i_code_structure.csv: "sha256:def456..."
  nco_2015_vol_ii_descriptions.pdf: "sha256:ghi789..."
  nco_2015_vol_ii_descriptions.csv: "sha256:jkl012..."
```

---

## 5. Troubleshooting

| Issue | Resolution |
|-------|------------|
| File not in manifest | Add to manifest with `required: false` if experimental; investigate source |
| SHA-256 mismatch | Re-download; verify source hasn't updated file; update manifest if legitimate |
| PII detected in e-Shram | **Abort ingestion.** Log security event. Notify data owner. |
| Geometry invalid | Try `ST_MakeValid` in PostGIS; if fails, quarantine and request corrected file |
| NCO code format invalid | Check parser regex; some codes may have trailing spaces or dots |
| PLFS weights missing | Download layout dictionary; apply weight column per round specification |

---

## 6. Security & Compliance

- **Never commit raw data** to git (`.gitignore` enforces `data/raw/**`)
- **Never share API credentials** — use `.env` (gitignored)
- **PII guard is mandatory** for e-Shram — hard reject on any PII column
- **Audit trail:** Every download logged in `dataset_registry` with SHA-256, timestamp, operator
- **Retention:** Raw files retained 90 days post-ingestion; lineage permanent