# Raw Data Source: e-Shram Portal Aggregates

## 1. What Belongs in this Folder
- Public e-Shram Dashboard aggregate reports (`eshram_district_registrations_YYYY_MM.csv`).
- Parliamentary session statistical annexures (Lok Sabha / Rajya Sabha unstarred questions).
- MoLE annual review unorganized workforce statistical summaries.
- **CRITICAL RESTRICTION**:
  - ONLY aggregate counts (district-level, sector-level, state-level).
  - NEVER download, extract, or place individual worker records, Aadhaar numbers, or personal identifying information (PII) in this repository.

## 2. Where to Download It
- **e-Shram Public Dashboard**:
  `https://eshram.gov.in/eshramportal/publicDashboard`
- **Ministry of Labour & Employment (MoLE)**:
  `https://labour.gov.in/` (Reports and dashboard statistics)
- **Parliament of India Question Search**:
  `https://loksabha.nic.in/` / `https://rajyasabha.nic.in/` (Search keyword: "e-Shram registrations district-wise")

## 3. Version Being Used
- Monthly snapshot series (2023–2024 cumulative registers).
- Categorized by:
  - State & District
  - Broad Occupations (Agriculture, Construction, Apparel, Transport, Domestic Worker)
  - Gender & Age demographics (aggregate percentages)

## 4. How It Is Processed
- Processed by: `backend.app.services.data.adapters.eshram_adapter.EShramAdapter`
- Verification Steps:
  1. Runs `PIIGuard`: fails immediately if columns matching Aadhaar, phone, name, or account are present.
  2. Parses `snapshot_date`, `geography` (State/District), `occupation_sector`, `worker_count`.
  3. Verifies counts are non-negative integers.
  4. Maps sector to canonical `dim_sector` and broad NCO division.
  5. Emits `CanonicalWorkforceSignal` -> Gold `fact_workforce_stock`.
