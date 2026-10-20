# LABREX System Brain (Architecture & Product Knowledge)

**Last Updated:** 2026-10-20  
**Status:** Living Knowledge Repository  
**Maintained By:** LABREX Principal Engineering Agent  

---

## 1. Domain Foundations & Philosophy

### 1.1 The Core Problem
Labour-market decision-making in developing and emerging economies is structurally impaired by data fragmentation:
- **Demand Signals**: Job postings, employer surveys, investment announcements, and industrial corridor data arrive at differing frequencies with inconsistent occupation titles.
- **Supply Signals**: Educational enrollments, technical skilling certifications (PMKVY/DGT), university graduations, and informal sector registrations (e-Shram) use different taxonomies.
- **The Decision Disconnect**: Even when governments possess historical tables, planners lack forward-looking estimates, uncertainty metrics, and mathematical tools to allocate limited skilling budgets effectively across thousands of districts and trades.

### 1.2 The LABREX Intelligence Value Chain
```
Data -> Signal -> Intelligence -> Forecast -> Gap -> Risk -> Scenario -> Optimization -> Action
```
LABREX is not an exploratory playground or a passive dashboard. It is an end-to-end **decision-support platform** providing mathematically sound, auditable recommendations.

---

## 2. Core Ontologies & Standard Classifications

### 2.1 Geographic Hierarchy
India -> State / Union Territory (36) -> District (700+) -> Training Center / Industrial Cluster.
- Spatial Representation: PostGIS geometries (EPSG:4326 WGS84 for storage, EPSG:3857 for web tile projection).
- Strict Standard: Coordinates stored as `(longitude, latitude)`. District geometries matched to Survey of India official boundary references.

### 2.2 National Classification of Occupations (NCO-2015)
- Divisions (1-digit) -> Sub-Divisions (2-digit) -> Group (3-digit) -> Family (4-digit) -> Occupation Code (8-digit).
- Authoritative NCO codes are deterministic. Free-text job descriptions are mapped to canonical NCO codes via NLP/embeddings with an audit confidence score (0.00–1.00).

### 2.3 National Skills Qualification Framework (NSQF)
- Levels 1 through 10, defining competence, knowledge, autonomy, and skill complexity.
- Qualifications and Qualification Packs (QPs) align to National Occupational Standards (NOS).

---

## 3. Analytical & Forecasting Foundations

### 3.1 Demand Index (0–100)
Calculated via normalized weighted components:
- $D_{post}$: Normalized volume of active postings/vacancies.
- $D_{growth}$: Quarter-over-quarter posting growth rate.
- $D_{persist}$: Vacancy persistence (mean days active on market).
- $D_{div}$: Employer diversity index (Herfindahl-Hirschman Index of hiring companies).
- Formally versioned: `DI-1.0`. All weights and normalization bounds are auditable.

### 3.2 Supply Index (0–100)
- $S_{stock}$: Current employed/certified workforce stock.
- $S_{pipeline}$: Trainees enrolled in relevant NSQF programs nearing completion.
- $S_{capacity}$: Available intake capacity across accredited training centres.
- $S_{place}$: Historical placement and certification rate (quality discount).
- Formally versioned: `SI-1.0`.

### 3.3 Skill Gap & Risk Classification
$$\text{Skill Gap} = \text{Forecasted Demand} - \text{Forecasted Effective Supply}$$
Risk Categories (LABREX RADAR):
- **CRITICAL**: Rapid demand surge + severe supply stagnation + high forecast confidence.
- **HIGH**: Substantial gap, negative supply growth trend.
- **EMERGING**: Early acceleration in demand residual before training response forms.
- **WATCH**: Moderate shortage with potential self-correction.
- **NORMAL**: Balanced labour market (within equilibrium bounds).
- **OVERSUPPLY**: Persistent training excess exceeding absorbed market demand.

---

## 4. Optimization Theory (Constrained Intervention)

We formulate the intervention problem as a Mixed-Integer Linear Program (MILP):
$$\min_{x} \sum_{i \in \text{Occupations}} \sum_{j \in \text{Districts}} w_{ij} \cdot \max(0, \text{Gap}_{ij} - \Delta \text{Supply}_{ij}(x))$$
Subject to:
1. $\sum_{k} \text{Cost}_k \cdot x_k \le \text{Total Budget}$ (Fiscal Constraint)
2. $\sum_{k \in \text{Center}_c} \text{Seats}_k \cdot x_k \le \text{Max Center Capacity}_c$ (Physical Infrastructure Constraint)
3. $x_k \in \{0, 1\}$ or bounded integer seat increments (Program Launch / Capacity Expansion)
4. Minimum viable cohort sizes and regional equity quotas.

Solved via Google OR-Tools (CBC/CP-SAT engine).

---

## 5. System Boundary Rules

1. **No Hallucinated Data**: Synthetic fixtures are strictly segregated from real source tables and flagged `data_type = 'SYNTHETIC'`.
2. **AI Copilot Restraints**: Gemini models are interfaced via typed schema tools only. No raw SQL execution, no arbitrary file system access, no fabricated numerical statistics.
3. **Immutability of Historical Snapshots**: Ingestion is append-only. Run records and evaluation metrics cannot be altered retroactively.
