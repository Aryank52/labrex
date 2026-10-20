# Raw Data Source: Indian Administrative Boundaries

## 1. What Belongs in this Folder
- Official State and Union Territory boundary vector files (`india_states.geojson` or `.shp`).
- Official District boundary vector files (`india_districts.geojson` or `.shp`).
- LGD (Local Government Directory) hierarchy code mapping tables (`lgd_state_district_master.csv`).
- Do NOT use unverified third-party boundary sketches that misrepresent the official Survey of India external boundary.

## 2. Where to Download It
- **Survey of India (SOI)**:
  `https://onlinemaps.surveyofindia.gov.in/` (Open Map Series / Administrative Boundary vector data)
- **Local Government Directory (LGD)**:
  `https://lgdirectory.gov.in/` (Ministry of Panchayati Raj)
- **Bharat Maps (NIC - National Informatics Centre)**:
  `https://bharatmaps.gov.in/`
- **Open Government Data (OGD) Portal**:
  `https://data.gov.in/` (Keywords: "District Boundary Shapefiles", "State Boundary GeoJSON")

## 3. Version Being Used
- Baseline: Survey of India National Map 2021/2024 specifications.
- 36 States and Union Territories.
- 780+ Districts reflecting recent state delimitation / administrative bifurcations.
- Coordinate Reference System (CRS): Standard EPSG:4326 (WGS 84, degrees lon/lat).

## 4. How It Is Processed
- Processed by: `backend.app.services.data.parsers.geography_parser.GeographyParser`
- Quality Validation:
  1. Validates topological geometry with Shapely (`geom.is_valid`, non-empty Polygon/MultiPolygon).
  2. Confirms SRID is EPSG:4326.
  3. Verifies India geographic bounding box ($6.0 \le \text{lat} \le 38.0$, $68.0 \le \text{lon} \le 98.0$).
  4. Validates referential state-district relationships (no orphan districts).
  5. Computes official polygon centroid for geospatial indexation.
  6. Emits conformed records for Gold dimensions `dim_state` and `dim_district`.
