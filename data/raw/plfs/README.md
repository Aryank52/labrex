# Raw Data Source: Periodic Labour Force Survey (PLFS)

## 1. What Belongs in this Folder
- Tabular annual report extracts (e.g. `plfs_annual_2022_23_statement_*.csv`, `plfs_annual_2023_24_indicators.xlsx`).
- Quarterly urban bulletin summary tables (`plfs_quarterly_urban_2024_q1.csv`).
- Selected microdata extract files with data dictionary layouts (`plfs_person_level_sample.csv`).
- Do NOT download all 574+ catalog datasets. Keep to minimal high-value indicator files.

## 2. Where to Download It
- **Ministry of Statistics and Programme Implementation (MoSPI)**:
  `https://www.mospi.gov.in/` (Reports & Publications -> Employment and Unemployment)
- **MoSPI Microdata Portal**:
  `https://microdata.gov.in/mop/` (Survey Category: Labour Force -> Periodic Labour Force Survey)
- **Open Government Data (OGD) Portal**:
  `https://data.gov.in/` (Keyword: "PLFS Annual Report")

## 3. Version Being Used
- **Primary Annual Baseline**: PLFS 2022–23 and 2023–24 Annual Surveys (covering July to June survey periods).
- **Secondary Urban Baseline**: PLFS Quarterly Bulletins (Calendar Years 2023–2024).
- Temporal Frequency:
  - Annual: Rural + Urban nationwide panel.
  - Quarterly: Urban high-frequency rotation panel.

## 4. How It Is Processed
- Processed by: `backend.app.services.data.adapters.plfs_adapter.PLFSAdapter`
- Pipeline:
  1. Identifies minimal high-value metrics:
     - LFPR (Labour Force Participation Rate in %)
     - WPR (Worker Population Ratio in %)
     - UR (Unemployment Rate in %)
     - Broad industry distributions (Agriculture, Industry/Manufacturing, Services)
  2. Maps state names/codes to canonical `dim_state` codes (e.g. `'IN-MH'`, `'IN-KA'`).
  3. Validates boundary values ($0.0 \le \text{rate} \le 100.0\%$).
  4. Preserves temporal frequency flag (`ANNUAL` vs `QUARTERLY`).
  5. Emits `CanonicalWorkforceSignal` and `CanonicalObservation` records.
