# Raw Data Source: National Classification of Occupations (NCO-2015)

## 1. What Belongs in this Folder
- Official NCO-2015 Volume I (Structure and Code List) in CSV, XLSX, or machine-readable format.
- Official NCO-2015 Volume II (Occupational Descriptions & Task Definitions).
- Concordance tables between NCO-2004, NCO-2015, and ISCO-08.
- Typical filenames: `nco_2015_volume1_codes.csv`, `nco_2015_volume2_descriptions.csv`.

## 2. Where to Download It
- **Ministry of Labour & Employment (MoLE)**:
  `https://labour.gov.in/national-classification-occupations-nco`
- **Directorate General of Employment (DGE)**:
  `https://dge.gov.in/dge/nco`
- **National Career Service (NCS)**:
  `https://www.ncs.gov.in/` (NCO Occupational Search section)
- **Open Government Data (OGD) Platform India**:
  `https://data.gov.in/`

## 3. Version Being Used
- **Version**: NCO-2015 (Standard Gazetted Edition, 2015).
- Aligned to International Standard Classification of Occupations (ISCO-08).
- Structure:
  - 1-Digit: Major Division (0–9)
  - 2-Digit: Sub-Division
  - 3-Digit: Group
  - 4-Digit: Family
  - 8-Digit: Detailed Occupation Code (e.g. `7421.0300` - Solar PV Installation Technician)

## 4. How It Is Processed
- Processed by: `backend.app.services.data.parsers.nco_parser.NCOParser`
- Pipeline:
  1. Checks file integrity and SHA-256 digest.
  2. Parses hierarchy levels: Division -> Sub-Division -> Group -> Family -> Occupation Code.
  3. Validates regex syntax: `^\d{4}\.\d{2,4}$`.
  4. Standardizes canonical occupational titles and maps available sector linkages.
  5. Outputs canonical staging schema: `CanonicalOccupation` -> Gold table `dim_occupation`.
