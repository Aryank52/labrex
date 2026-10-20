# Raw Data Source: NSDC Skill Directory & Training Centers

## 1. What Belongs in this Folder
- Training Centre directory exports (`nsdc_training_centre_directory_*.csv`).
- National Qualification Register (NQR) course files (`nqr_qualifications_catalog_*.csv`).
- Accredited PMKK (Pradhan Mantri Kaushal Kendra) directory tables.
- Sector Skill Council (SSC) affiliated partner catalogs.

## 2. Where to Download It
- **National Skill Development Corporation (NSDC)**:
  `https://nsdcindia.org/`
- **National Qualification Register (NQR)**:
  `https://nqr.gov.in/`
- **Skill India Digital Hub (SIDH)**:
  `https://www.skillindiadigital.gov.in/` (Training Centers directory)
- **NCVET (National Council for Vocational Education and Training)**:
  `https://ncvet.gov.in/`

## 3. Version Being Used
- Active roster for Calendar Years 2024–2026.
- Attributes:
  - Centre Unique Identifier (`center_id`)
  - Center Name & Institutional Sponsor
  - State, District, Postal PIN Code
  - Centre Type (`PMKK`, `GOVT_ITI`, `POLYTECHNIC`, `PRIVATE_VTP`)
  - Approved Qualification Packs (QPs) & NSQF Levels (1 to 10)
  - Sanctioned Capacity & Shift Capacity

## 4. How It Is Processed
- Processed by: `backend.app.services.data.adapters.nsdc_adapter.NSDCAdapter`
- Ingestion logic:
  - Standardizes center identifiers and trims postal codes.
  - Matches district name to canonical `dim_district`.
  - Normalizes GPS coordinates when provided (verifies valid India bounds).
  - Emits `CanonicalTrainingSignal` (capacity) -> Gold `dim_training_center` & `dim_qualification`.
