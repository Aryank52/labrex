# LABREX Data Source Registry

**Document Version:** 1.0  
**Authority:** Master Directive Section 14 & 93  
**Integrity Rule:** Synthetic and demo datasets are explicitly tagged. Never fabricate government data.  

---

## 1. Registry Master Table

| Source ID | Source Family | Authority / Organization | Coverage | Freshness | Retrieval Method | Real/Synthetic Status | Schema Mapping Status | Quality Score (0–100) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :---: |
| `SRC-NCO-2015` | NCO Taxonomy | Ministry of Labour & Employment (MoLE) | All India (All Occupations) | Static (2015 Edition) | Official Gazetted PDF / CSV Import | **REAL** | Fully Mapped (Canonical) | 100 |
| `SRC-NSQF-QP` | Qualifications | NCVET / NSDC | National (Level 1–10) | Quarterly | National Qualification Register (NQR) | **REAL** | Fully Mapped (Canonical) | 98 |
| `SRC-PLFS-ANN` | Labour Force Survey | MoSPI / NSSO | National & State Panels | Annual | MoSPI Public Data Portal / Microdata | **REAL** | Mapped to NCO 2-digit | 92 |
| `SRC-NCS-FEED` | Job Vacancies | National Career Service (NCS) | Multi-State / Multi-District | Monthly / Bi-weekly | NCS API / Batch CSV Upload | **DATA_PENDING** (Config Required) | Schema Defined | 85 |
| `SRC-ESHRAM-AGG` | Informal Workforce | MoLE (e-Shram Portal) | District Aggregates | Monthly | Public Dashboard Extracts | **DATA_PENDING** | Schema Defined | 80 |
| `SRC-PMKVY-OUT` | Training Outcomes | MSDE / NSDC | District Training Centres | Quarterly | Skill India Digital Hub Data Dumps | **DATA_PENDING** | Schema Defined | 88 |
| `SRC-DGT-ITI` | ITI Capacity & Seats | Directorate General of Training | All Accredited ITIs | Annual | NCVT MIS Public Portal | **REAL** (Public Snapshot) | Fully Mapped | 94 |
| `SRC-FIXTURE-IND` | National Demo Fixtures | LABREX Engineering Team | 3 States (MH, KA, GJ), 18 Districts | 2024–2026 Monthly Panels | Deterministic Seed Generator | **DEMO_FIXTURE** | 100% Star Schema Aligned | 100 (Synthetic) |

---

## 2. Ingestion & Fallback Policy

1. **Active Local Development & Testing**:
   - The platform boots using `SRC-FIXTURE-IND` (Deterministic fixtures with seeded time-series and district geometries).
   - In the UI and API responses, all data points sourced from fixtures carry:
     ```json
     "data_provenance": {
       "source_id": "SRC-FIXTURE-IND",
       "dataset_type": "DEMO_FIXTURE",
       "is_synthetic": true
     }
     ```
2. **Production Onboarding of Real Feeds**:
   - When an external API credential is not configured, the ingestion adapter returns status `NOT_CONFIGURED` without crashing.
   - External data feeds pass through the **Data Quality Engine** before landing in Bronze/Silver layers. If schema validation fails, the ingestion job marks the batch `DATA_SCHEMA_INVALID` and sends an alert.
