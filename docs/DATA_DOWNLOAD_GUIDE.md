# LABREX Operator Data Acquisition & Download Checklist

**Document Version:** 2.0  
**Authority:** Master Directive Section 14, 93 & Secondary Ingestion Mandate  
**Target Audience:** Human Data Operations Engineers, System Administrators  
**Strict Safety Rule:** NEVER commit downloaded raw source files to git. NEVER download individual worker PII.

---

## 1. Master Acquisition Checklist

| Source Code | Source Name | Official Portal | Login Required? | Exact Target Resources | Destination Folder | Committable to Git? | Status |
| :--- | :--- | :--- | :---: | :--- | :--- | :---: | :--- |
| `SRC-NCO-2015` | National Classification of Occupations | `labour.gov.in` / `dge.gov.in` | **No** | Volume I (Code Structure) & Volume II-B (Descriptions) | `data/raw/nco/` | **NO** (Git-ignored) | `AWAITING_DOWNLOAD` |
| `SRC-GEO-ADMIN` | Administrative Boundaries | `onlinemaps.surveyofindia.gov.in` | **No** | India State Boundaries & India District Boundaries (EPSG:4326) | `data/raw/geography/` | **NO** (Git-ignored) | `AWAITING_DOWNLOAD` |
| `SRC-PLFS-ANN` | Periodic Labour Force Survey | `microdata.gov.in` | **Yes** (Free) | 5 Rounds (2019-20 to 2023-24): Main Data, Layout, District Code, README, Estimation | `data/raw/plfs/<round>/` | **NO** (Git-ignored) | `AWAITING_DOWNLOAD` |
| `SRC-PMKVY-OUT` | PMKVY Skilling Outcomes | `pmkvyofficial.org` / `msde.gov.in` | **No** | Trained (2021-24), Enrolled (2022-25), Certified (2022-25), Centres (2022-25) | `data/raw/pmkvy/` | **NO** (Git-ignored) | `AWAITING_DOWNLOAD` |
| `SRC-ESHRAM-AGG` | e-Shram Unorganized Registry | `eshram.gov.in` | **No** | District & State Aggregate Reports Only | `data/raw/eshram/` | **NO** (Git-ignored) | `AWAITING_DOWNLOAD` |
| `SRC-NCS-FEED` | National Career Service | `ncs.gov.in` / `data.gov.in` | **No** (Batch) | State & Sector Vacancy Aggregates Batch | `data/raw/ncs/` | **NO** (Git-ignored) | `AWAITING_DOWNLOAD` |
| `SRC-NSDC-DIR` | NSDC Skill Directory | `nsdcindia.org` / `nqr.gov.in` | **No** | NQR Qualifications Catalog & Accredited Centres Directory | `data/raw/nsdc/` | **NO** (Git-ignored) | `AWAITING_DOWNLOAD` |

---

## 2. Detailed Step-by-Step Acquisition Procedures

### 2.1 Source 1: NCO-2015 (National Classification of Occupations)
- **Official Portal & Direct Download URLs**:
  - **Volume I (Structure and Code List)**:
    - *Direct URL*: `https://www.ncs.gov.in/Documents/National%20Classification%20of%20Occupations%20_Vol%20I-%202015.pdf`
    - *Portal Mirror*: `https://dge.gov.in/dge/nco`
    - *(CAUTION: Do NOT download from `labour.gov.in/sites/default/files/...` as MoLE migrated file paths, which returns an HTML 404 page)*.
  - **Volume II-A (Occupational Descriptions Div 0 to 4)**:
    - *Direct URL*: `https://www.ncs.gov.in/Documents/National_Classification_of_Occupations_Vol_II-A-2015.pdf`
    - *(CAUTION: Do NOT save `https://ncs.gov.in/` without the `/Documents/` path, as that downloads the HTML website homepage)*.
  - **Volume II-B (Occupational Descriptions & Tasks Div 5 to 9)**:
    - *Direct URL*: `https://www.ncs.gov.in/Documents/National%20Classification%20of%20Occupations_Vol%20II-B-%202015.pdf`
    - *(CAUTION: Verify that the downloaded file starts with `%PDF-` and is ~7-10 MB, not ~470 KB HTML text)*.
- **What to Click**:
  1. Use the direct URLs above or navigate on the National Career Service (NCS) portal to **Reports & Documents** -> **Documents**.
  2. Save each link directly as a binary PDF.
- **Whether Login is Required**: **NO**. Public unrestricted government publications.
- **What Exact Resources to Download**:
  - `NCO_2015_Vol_I.pdf` (~2-5 MB, binary PDF)
  - `National_Classification_of_Occupations_Vol_II-A-2015.pdf` (~7.0 MB, binary PDF - already verified in `data/raw/nco/`)
  - `NCO_2015_Vol_II_B.pdf` (~7-10 MB, binary PDF)
- **What NOT to Download**:
  - HTML error pages or landing pages masquerading as `.pdf`.
  - Outdated NCO-1968 or NCO-2004 volumes (unless strictly for historical concordance).
- **Expected Format**: Official binary PDF (`%PDF-1.6`), or exported CSV/XLSX.
- **Destination Folder**: `data/raw/nco/`
- **Whether Committable to Git**: **NO** (enforced by `.gitignore`).
- **How to Verify Download**:
  ```powershell
  python -m labrex.data.validate_raw --source nco
  ```

---

### 2.2 Source 2: Administrative Boundaries (Survey of India & LGD)
- **Official URL**: `https://onlinemaps.surveyofindia.gov.in/` and `https://lgdirectory.gov.in/`
- **What to Click**:
  1. Navigate to the Survey of India Open Map Series or Bharat Maps (`https://bharatmaps.gov.in/`).
  2. Select **Administrative Boundary Maps** (State and District levels).
  3. For Local Government Directory (LGD), download the latest gazetted State-District hierarchy master.
- **Whether Login is Required**: **NO** for public administrative boundaries.
- **What Exact Resources to Download**:
  - `india_states.geojson` (36 States & UTs, EPSG:4326)
  - `india_districts.geojson` (780+ Districts, EPSG:4326)
  - `lgd_state_district_master.csv` (Optional concordance table)
- **What NOT to Download**:
  - Third-party, unverified boundary sketches that misrepresent the official Survey of India external border.
  - High-resolution raster imagery (.tif) over 500 MB.
- **Expected Format**: GeoJSON, Shapefile (.shp/.shx/.dbf/.prj), or TopoJSON.
- **Destination Folder**: `data/raw/geography/`
- **Whether Committable to Git**: **NO** (enforced by `.gitignore`).
- **How to Verify Download**:
  ```powershell
  python -m labrex.data.validate_raw --source geography
  ```

---

### 2.3 Source 3: PLFS (Periodic Labour Force Survey)
- **Official URL**: `https://microdata.gov.in/mop/` and `https://www.mospi.gov.in/`
- **What to Click**:
  1. Open MoSPI Microdata Portal -> Click **Microdata Catalog**.
  2. Filter by **Labour Force** -> **Periodic Labour Force Survey**.
  3. Select each of the 5 target rounds:
     - PLFS 2019–20 (July 2019 – June 2020)
     - PLFS 2020–21 (July 2020 – June 2021)
     - PLFS 2021–22 (July 2021 – June 2022)
     - PLFS 2022–23 (July 2022 – June 2023)
     - PLFS 2023–24 (July 2023 – June 2024)
  4. In the survey page, navigate to **Study Description** and **Data Files**.
- **Whether Login is Required**: **YES**. Requires a free user account on `microdata.gov.in`. Registration is instant with an email verification.
- **What Exact Resources to Download** (For EACH of the 5 rounds):
  1. `Main Data`: Raw unit-level microdata or indicator statement tables (`*data*.*` / `*statement*.*`).
  2. `Data Layout`: Record layout file specifying column positions and widths (`*layout*.*` / `*codebook*.*`).
  3. `District Code Reference`: State and District code concordance document (`*district*.*`).
  4. `README`: Official release notes and survey overview (`*readme*.*` / `*note*.*`).
  5. `Estimation Procedure`: Official sampling weights, multipliers, and estimation procedure document (`*estimation*.*` / `*multiplier*.*`).
- **What NOT to Download**:
  - Do NOT download all 574+ MoSPI datasets. Restrict downloads strictly to the 5 annual rounds.
- **Expected Format**: CSV, XLSX, TXT (fixed-width), and PDF documentation.
- **Destination Folders**:
  - `data/raw/plfs/2019-20/`
  - `data/raw/plfs/2020-21/`
  - `data/raw/plfs/2021-22/`
  - `data/raw/plfs/2022-23/`
  - `data/raw/plfs/2023-24/`
- **Whether Committable to Git**: **NO** (enforced by `.gitignore`).
- **How to Verify Download**:
  ```powershell
  python -m labrex.data.validate_raw --source plfs
  ```

---

### 2.4 Source 4: PMKVY (Pradhan Mantri Kaushal Vikas Yojana)
- **Official URL**: `https://www.pmkvyofficial.org/` and `https://www.skillindiadigital.gov.in/`
- **What to Click**:
  1. Open PMKVY portal or Skill India Digital Hub (SIDH) analytics section.
  2. Navigate to **Reports & Open Data** -> **Scheme Performance**.
  3. Download annual/phase outcome tables for:
     - `Trained Candidates`: Financial Years 2021–22, 2022–23, 2023–24.
     - `Enrolled Candidates`: Financial Years 2022–23, 2023–24, 2024–25.
     - `Certified Candidates`: Financial Years 2022–23, 2023–24, 2024–25.
     - `Training Centres & Capacity`: Financial Years 2022–23, 2023–24, 2024–25.
- **Whether Login is Required**: **NO**. Data is available through open public reports and parliamentary releases.
- **What Exact Resources to Download**:
  - State and district outcome breakdown tables (e.g. `pmkvy_trained_2021_2024.csv`, `pmkvy_enrolled_2022_2025.csv`, `pmkvy_certified_2022_2025.csv`, `pmkvy_centres_2022_2025.csv`).
- **What NOT to Download**:
  - Candidate identity cards or personal assessment scorecards.
- **Expected Format**: CSV, XLSX, or PDF.
- **Destination Folder**: `data/raw/pmkvy/`
- **Whether Committable to Git**: **NO** (enforced by `.gitignore`).
- **How to Verify Download**:
  ```powershell
  python -m labrex.data.validate_raw --source pmkvy
  ```

---

### 2.5 Source 5: e-Shram Portal District Aggregates
- **Official URL**: `https://eshram.gov.in/eshramportal/publicDashboard`
- **What to Click**:
  1. Open the e-Shram Public Dashboard.
  2. Navigate to **State / District Statistics** and **Occupation Overview**.
  3. Export public monthly snapshot summaries or aggregate district reports.
  4. Alternatively, obtain Lok Sabha / Rajya Sabha unstarred question annexures containing official district totals.
- **Whether Login is Required**: **NO**.
- **What Exact Resources to Download**:
  - District and State cumulative worker registration aggregates (`eshram_district_aggregates_*.csv`).
- **CRITICAL RESTRICTION (What NOT to Download)**:
  - **ABSOLUTELY NO INDIVIDUAL WORKER RECORDS**.
  - Never download or place files containing Aadhaar numbers, worker names, phone numbers, or bank details.
  - The validation tool will immediately fail and reject any file containing PII.
- **Expected Format**: CSV or XLSX.
- **Destination Folder**: `data/raw/eshram/`
- **Whether Committable to Git**: **NO** (enforced by `.gitignore`).
- **How to Verify Download**:
  ```powershell
  python -m labrex.data.validate_raw --source eshram
  ```

---

### 2.6 Source 6: NCS (National Career Service Vacancies)
- **Official URL**: `https://www.ncs.gov.in/` and `https://data.gov.in/`
- **What to Click**:
  1. Open Open Government Data (OGD) Portal (`data.gov.in`) -> Search "National Career Service".
  2. Download monthly or quarterly vacancy aggregate batch files.
  3. Filter for state, district, and industry sector summaries.
- **Whether Login is Required**: **NO** for public batch downloads.
- **What Exact Resources to Download**:
  - State and sector vacancy aggregate releases (`ncs_vacancies_*.csv`).
- **CRITICAL RESTRICTION (What NOT to Download)**:
  - **DO NOT RUN SCRAPERS AGAINST LIVE JOB POSTINGS**.
  - Do not download individual applicant profiles or recruiter personal credentials.
- **Expected Format**: CSV or JSON.
- **Destination Folder**: `data/raw/ncs/`
- **Whether Committable to Git**: **NO** (enforced by `.gitignore`).
- **How to Verify Download**:
  ```powershell
  python -m labrex.data.validate_raw --source ncs
  ```

---

### 2.7 Source 7: NSDC Skill Directory & Training Centers
- **Official URL**: `https://nsdcindia.org/` and `https://nqr.gov.in/`
- **What to Click**:
  1. Open the National Qualification Register (NQR) at `https://nqr.gov.in/`.
  2. Download the public qualification catalog (QP codes, NSQF levels, Sector Skill Councils).
  3. Open NSDC or Skill India Digital Hub directory section to download the accredited training centre roster.
- **Whether Login is Required**: **NO**.
- **What Exact Resources to Download**:
  - `nqr_qualifications_catalog.csv` (or `.xlsx`)
  - `nsdc_training_centres_directory.csv` (or `.xlsx`)
- **What NOT to Download**:
  - Do not scrape partner portals aggressively.
  - No trainer personal CVs or bank accounts.
- **Expected Format**: CSV, XLSX, or JSON.
- **Destination Folder**: `data/raw/nsdc/`
- **Whether Committable to Git**: **NO** (enforced by `.gitignore`).
- **How to Verify Download**:
  ```powershell
  python -m labrex.data.validate_raw --source nsdc
  ```

---

## 3. Post-Download Validation Command

Once files are placed into `data/raw/`, run the automated validation and registration tools:

```powershell
# 1. Register newly placed files (computes SHA-256 and checks manifest match)
python -m labrex.data.register_file data/raw/nco/nco_2015_volume_1.csv

# 2. Run comprehensive raw data validation across all staged files
python -m labrex.data.validate_raw

# 3. View updated acquisition status
Get-Content docs/DATA_ACQUISITION_STATUS.md
```
