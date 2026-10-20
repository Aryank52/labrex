# Raw Data Source: Pradhan Mantri Kaushal Vikas Yojana (PMKVY)

## 1. What Belongs in this Folder
- PMKVY district outcome datasets (`pmkvy_state_district_outcomes_*.csv`).
- Scheme phase tables for PMKVY 1.0, 2.0, 3.0, and PMKVY 4.0.
- State Skill Development Mission (SSDM) and Centrally Sponsored Centrally Managed (CSCM) reports.
- Training Centre accredited lists with allocated target numbers.

## 2. Where to Download It
- **PMKVY Official Portal**:
  `https://www.pmkvyofficial.org/`
- **Ministry of Skill Development and Entrepreneurship (MSDE)**:
  `https://www.msde.gov.in/` (Open Data & Statistics)
- **Skill India Digital Hub (SIDH)**:
  `https://www.skillindiadigital.gov.in/` (Analytics Dashboard)
- **Open Government Data (OGD) Portal**:
  `https://data.gov.in/` (Keyword: "PMKVY candidates trained certified")

## 3. Version Being Used
- Cumulative reports through PMKVY 3.0 and active PMKVY 4.0 (2023–2026).
- Aggregations by State, District, Sector Skill Council (SSC), and Qualification Pack (QP).

## 4. How It Is Processed
- Processed by: `backend.app.services.data.adapters.pmkvy_adapter.PMKVYAdapter`
- Core Invariant: Strict separation of 3 supply components:
  1. **Training Pipeline**: Enrolled and ongoing candidates in training.
  2. **Certified Supply**: Successfully certified candidates assessed by NCVET/SSC.
  3. **Infrastructure Capacity**: Accredited training centres, sanctioned batches, and seat allocations.
- Validation Checks:
  - $\text{Certified} \le \text{Trained} \le \text{Enrolled}$
  - $\text{Counts} \ge 0$
  - Referential integrity to canonical `district_id` and `qualification_id`
- Emits `CanonicalTrainingSignal` -> Gold `fact_training_capacity` & `fact_training_outcomes`.
