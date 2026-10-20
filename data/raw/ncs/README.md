# Raw Data Source: National Career Service (NCS)

## 1. What Belongs in this Folder
- Public vacancy batch extracts (`ncs_vacancies_batch_YYYY_MM.csv` or `.json`).
- Open vacancy summary datasets from OGD India.
- Authenticated export payloads received from MoLE data exchange agreements.
- Do NOT run aggressive or unauthorized scrapers against `ncs.gov.in`.

## 2. Where to Download It
- **National Career Service Portal**:
  `https://www.ncs.gov.in/` (Open data & reports section)
- **Open Government Data (OGD) Portal**:
  `https://data.gov.in/` (Ministry of Labour & Employment -> NCS Vacancies)
- **Ministry API Integration**:
  Configured via environment variables (`NCS_API_ENDPOINT`, `NCS_API_KEY`).

## 3. Version Being Used
- Monthly and bi-weekly vacancy aggregations (2024–2026).
- Industry sector classifications mapped to NIC-2008 / SSC sectors.
- Occupational demand codes mapped to NCO-2015.

## 4. How It Is Processed
- Processed by: `backend.app.services.data.adapters.ncs_adapter.NCSAdapter`
- Pluggable connection handling:
  - `NOT_CONFIGURED`: Returns safe empty/fixture mode without crashing.
  - `AVAILABLE`: Fetches from verified endpoint or reads staged files.
  - `RATE_LIMITED`: Exponential backoff with jitter.
  - `UNAVAILABLE`: Circuit breaker fallback.
- Security Guard:
  - Phone numbers, applicant names, and private employer emails are stripped.
  - Postings aggregated by `(district_id, occupation_id, month)`.
- Emits `CanonicalObservation` (`metric='active_postings'`) -> Gold `fact_job_demand`.
