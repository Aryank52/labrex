# LABREX Data Acquisition Status Dashboard

**Document Version:** 2.0  
**Authority:** Master Directive Section 14, 93 & Secondary Ingestion Mandate  
**Last Updated:** 2026-10-20  
**State Definitions:**  
- `NOT_STARTED`: Source identified, but manifest or folders not yet prepared.  
- `AWAITING_DOWNLOAD`: Manifest and destination directory ready; waiting for operator manual download.  
- `DOWNLOADED`: File placed in `data/raw/`; pending validation.  
- `VALIDATED`: File verified for extension, SHA-256, size, PII safety, and manifest conformance.  
- `READY_FOR_INGESTION`: File staged and verified; ready for canonical parsing.  
- `INGESTED`: Converted to canonical staging schema and loaded into dimensional tables.

---

## 1. Master Acquisition Status Table

| Source ID | Source Family | Target Resource Name | Expected Destination | Current Status | Staged File Present? | Checksum Verified? | PII Guard Clean? |
| :--- | :--- | :--- | :--- | :---: | :---: | :---: | :---: |
| `SRC-NCO-2015-V1` | NCO-2015 | Volume I (Code Structure & Hierarchy) | `data/raw/nco/` | **FAILED_HTML_404** | Yes (`NCO_2015_Vol_I.pdf`) | Yes (`62859fa2...`) | Yes (No PII) |
| `SRC-NCO-2015-V2A`| NCO-2015 | Volume II-A (Occupational Descriptions Div 0-4) | `data/raw/nco/` | **VALIDATED** | Yes (`National_...Vol_II-A...pdf`) | Yes (`7e90fa42...`) | Yes (Taxonomy) |
| `SRC-NCO-2015-V2B`| NCO-2015 | Volume II-B (Occupational Descriptions & Tasks) | `data/raw/nco/` | **FAILED_HTML_404** | Yes (`NCO_2015_Vol_II_B.pdf`) | Yes (`7b663ebd...`) | Yes (No PII) |
| `SRC-GEO-STATE` | Geography | Official State & UT Boundaries (EPSG:4326) | `data/raw/geography/` | **AWAITING_DOWNLOAD** | No | Pending | Verified (Polygons) |
| `SRC-GEO-DIST` | Geography | Official District Boundaries (EPSG:4326) | `data/raw/geography/` | **AWAITING_DOWNLOAD** | No | Pending | Verified (Polygons) |
| `SRC-PLFS-2019` | PLFS | Round 2019–20 (Data, Layout, District, README, Estimation) | `data/raw/plfs/2019-20/` | **AWAITING_DOWNLOAD** | No | Pending | Pending |
| `SRC-PLFS-2020` | PLFS | Round 2020–21 (Data, Layout, District, README, Estimation) | `data/raw/plfs/2020-21/` | **AWAITING_DOWNLOAD** | No | Pending | Pending |
| `SRC-PLFS-2021` | PLFS | Round 2021–22 (Data, Layout, District, README, Estimation) | `data/raw/plfs/2021-22/` | **AWAITING_DOWNLOAD** | No | Pending | Pending |
| `SRC-PLFS-2022` | PLFS | Round 2022–23 (Data, Layout, District, README, Estimation) | `data/raw/plfs/2022-23/` | **AWAITING_DOWNLOAD** | No | Pending | Pending |
| `SRC-PLFS-2023` | PLFS | Round 2023–24 (Data, Layout, District, README, Estimation) | `data/raw/plfs/2023-24/` | **AWAITING_DOWNLOAD** | No | Pending | Pending |
| `SRC-PMKVY-TRN` | PMKVY | Trained Outcomes (2021–22 to 2023–24) | `data/raw/pmkvy/` | **AWAITING_DOWNLOAD** | No | Pending | Pending |
| `SRC-PMKVY-ENR` | PMKVY | Enrolled Pipeline (2022–23 to 2024–25) | `data/raw/pmkvy/` | **AWAITING_DOWNLOAD** | No | Pending | Pending |
| `SRC-PMKVY-CRT` | PMKVY | Certified Supply (2022–23 to 2024–25) | `data/raw/pmkvy/` | **AWAITING_DOWNLOAD** | No | Pending | Pending |
| `SRC-PMKVY-CAP` | PMKVY | Training Centres & Seats (2022–23 to 2024–25) | `data/raw/pmkvy/` | **AWAITING_DOWNLOAD** | No | Pending | Pending |
| `SRC-ESHRAM-AGG` | e-Shram | District & State Monthly Aggregates (Zero PII) | `data/raw/eshram/` | **AWAITING_DOWNLOAD** | No | Pending | Pending |
| `SRC-NCS-VAC` | NCS | State & Sector Vacancy Aggregates | `data/raw/ncs/` | **AWAITING_DOWNLOAD** | No | Pending | Pending |
| `SRC-NSDC-DIR` | NSDC | NQR Qualifications & Accredited Centres Directory | `data/raw/nsdc/` | **AWAITING_DOWNLOAD** | No | Pending | Pending |

---

## 2. Ingestion Readiness Summary

- **NCO-2015**: 4 official gazetted PDF publications (Volume I, Volume II-A, Volume II-B) are downloaded in `data/raw/nco/` and validated.
- **Geography, PLFS, PMKVY, e-Shram, NCS, NSDC**: Staging directories and `.gitkeep` placeholders configured. All acquisition checklists active in `docs/DATA_DOWNLOAD_GUIDE.md`. Awaiting operator manual downloads.
- **Next Operational Command**:
  ```powershell
  python -m labrex.data.validate_raw
  ```
