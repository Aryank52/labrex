# LABREX Raw Data Staging Directory (`data/raw/`)

**Standard:** Layer 0 (Raw Storage)  
**Security Level:** Read-Only, Local Cache, Uncommitted  
**Compliance Directive:** NEVER commit large datasets, binary dumps, or private personal data to git.

---

## 1. Directory Structure

```
data/raw/
├── nco/            # National Classification of Occupations (NCO-2015 Vol I/II)
├── plfs/           # Periodic Labour Force Survey reports & microdata
├── ncs/            # National Career Service vacancy and posting exports
├── eshram/         # e-Shram unorganized worker public district aggregates
├── pmkvy/          # PMKVY 1.0 - 4.0 training, certification & placement metrics
├── nsdc/           # NSDC Skill Directory & Training Center rosters
└── geography/      # Survey of India / LGD administrative boundary GeoJSONs
```

---

## 2. Ingestion Rules for Operators

1. **Format Preservation**: Retain files exactly as downloaded from the official ministry portal. Do not rename or edit lines manually.
2. **Checksum Verification**: Always calculate SHA-256 before running the ingestion pipeline:
   ```powershell
   Get-FileHash -Algorithm SHA256 <filename>
   ```
   Compare against the hash defined in `data/manifests/<source>.yaml`.
3. **No PII Policy**:
   - Only authorized aggregates belong in `eshram/` and `ncs/`.
   - Never place raw worker records with Aadhaar numbers, voter IDs, bank accounts, or telephone numbers here.
4. **Git Policy**:
   - All data files (*.csv, *.xlsx, *.zip, *.pdf, *.json, *.txt, *.geojson) in this directory tree are Git-ignored.
   - Only structural documentation files (`README.md`, `.gitkeep`) are tracked.
