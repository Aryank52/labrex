# LABREX Product Requirements Document (PRD)

**Document Version:** 1.0  
**Status:** Approved  
**Classification:** Evidence-Backed Decision Support Platform  

---

## 1. Executive Summary & Problem Definition

Labour market and workforce skilling in India spans 1.4 billion people, 36 States/UTs, 700+ districts, 50+ Sector Skill Councils, and tens of thousands of vocational training providers. Despite significant national initiatives (Skill India Mission, PMKVY, National Career Service, e-Shram, DGT ITIs), the ecosystem suffers from four critical structural disconnects:

1. **Temporal Disconnect**: Traditional government surveys (e.g. Periodic Labour Force Survey - PLFS) provide retrospective snapshots with multi-month reporting lags, while emerging industrial sectors require forward-looking demand signals.
2. **Taxonomic Disconnect**: Employer job descriptions, industry postings, educational curricula, and vocational trades use divergent naming conventions that fail to map to the National Classification of Occupations (NCO-2015) or National Skills Qualification Framework (NSQF).
3. **Spatial Disconnect**: Aggregated state or national metrics hide acute district-level skill shortages and localized training capacity gluts.
4. **Action Disconnect**: Planners have access to descriptive charts, but lack prescriptive, constraint-aware optimization tools to calculate where to allocate limited annual skilling budgets.

**LABREX** solves these challenges by transforming heterogeneous market and training signals into a unified, explainable, and evidence-backed intelligence and policy optimization platform.

---

## 2. Core Value Proposition: The Four Analytical Dimensions

LABREX explicitly segregates its analytical capabilities into four distinct tiers:

```
+--------------------------------------------------------------------------------------------------+
|                                    LABREX ANALYTICAL TIERS                                       |
+-------------------+------------------------------------------------------------------------------+
| TIER              | CAPABILITY & OBJECTIVE                                                       |
+-------------------+------------------------------------------------------------------------------+
| 1. DESCRIPTIVE    | What is happening right now? Realized demand index, certified supply stock,  |
|                   | active training capacity, and geographical distributions across districts.   |
+-------------------+------------------------------------------------------------------------------+
| 2. DIAGNOSTIC     | Why is it happening? Root-cause decomposition of skill gaps: wage divergence,|
|                   | low pass rates, high attrition, employer concentration, or curriculum decay. |
+-------------------+------------------------------------------------------------------------------+
| 3. PREDICTIVE     | What will happen next? 3- to 24-month walk-forward forecasts of demand and   |
|                   | supply with explicit prediction intervals, confidence scores, and shock radar|
+-------------------+------------------------------------------------------------------------------+
| 4. PRESCRIPTIVE   | What should we do? Constrained budget optimization (MILP) calculating the    |
|                   | optimal distribution of new training seats and programs across trades.       |
+-------------------+------------------------------------------------------------------------------+
```

---

## 3. Target User Personas & Core User Journeys

### Persona 1: National Workforce & Skilling Planner
- **Organization**: Ministry of Skill Development & Entrepreneurship (MSDE) / NSDC.
- **Core Need**: Macro-level visibility across sectors, identifying national critical shortages, allocating central scheme funds across states, and evaluating national training outcomes.
- **Primary Feature Usage**: Executive Overview, National Radar, Policy Optimizer, Export Reports.

### Persona 2: State Skilling Mission Director
- **Organization**: State Skill Development Missions (SSDMs) / State Planning Boards.
- **Core Need**: District-level allocation of training targets, matching localized industrial corridor requirements with ITI/polytechnic capacity.
- **Primary Feature Usage**: India Skill Map (State & District Drilldown), Scenario Studio (seat reallocations), Radar.

### Persona 3: Sector Skill Council (SSC) Analyst
- **Organization**: Industry Sector Councils (e.g. Automotive, IT-ITeS, Electronics, Healthcare).
- **Core Need**: Granular occupation-to-skill demand trajectories, emerging technology skill shocks, and qualification pack (QP) refresh priorities.
- **Primary Feature Usage**: Skill Intelligence Page, Forecast Studio, Skill Knowledge Graph.

### Persona 4: Vocational Training Capacity Planner
- **Organization**: Directorate General of Training (DGT), Vocational Training Providers (VTPs).
- **Core Need**: Optimizing classroom and lab seat utilization, identifying under-subscribed trades, and launching certified courses in high-demand clusters.
- **Primary Feature Usage**: Training Capacity vs. Demand analytics, Supply Pipeline view.

### Persona 5: Senior Data Analyst & Policy Researcher
- **Organization**: NITI Aayog, Research Institutes, Multilateral Development Banks.
- **Core Need**: Complete methodological transparency, access to historical panels, model performance comparisons (MAE/RMSE), and data lineage verification.
- **Primary Feature Usage**: Model Governance, Forecast Studio (Champion vs Challenger), Data Lineage.

---

## 4. Key Functional Requirements

1. **National Skill Knowledge Graph (SKG)**: Relational network connecting NCO codes, canonical skills, NSQF qualifications, training courses, accredited centres, and districts.
2. **Transparent Indices**:
   - **Demand Index (0–100)**: Normalized synthesis of job postings, hiring growth, vacancy persistence, and employer diversity.
   - **Supply Index (0–100)**: Normalized synthesis of certified workforce stock, training pipeline, and centre intake capacity.
3. **Hierarchical Forecasting Engine**:
   - Multi-horizon forecasts (3, 6, 12, 18, 24 months).
   - Champion-vs-challenger evaluation: Seasonal Naive baseline benchmarked against LightGBM/XGBoost and deep foundation candidates (TimesFM-3).
   - Prediction intervals (80% and 95%) and model disagreement score.
4. **LABREX RADAR (Early Warning Engine)**:
   - Automated classification into CRITICAL, HIGH, EMERGING, WATCH, NORMAL, and OVERSUPPLY.
   - Anomaly detection for sudden demand surges (Skill Shocks).
5. **Counterfactual Scenario Studio**:
   - What-if simulation of policy adjustments (e.g., adding 5,000 ITI seats in Pune for Electric Vehicle Assembly).
   - Instant delta analysis showing projected impact on net skill gap and local placement rates.
6. **Constrained Policy Optimizer**:
   - Mathematical solver minimizing weighted future shortages subject to fiscal budget, centre capacity, and minimum cohort sizes.
   - Multi-option output with cost-benefit Pareto trade-offs and natural language justifications.
7. **AI Policy Copilot**:
   - Conversational assistant powered by Gemini 3.8.
   - Strict tool execution: all numerical outputs, forecasts, and allocations are retrieved from validated platform APIs, preventing hallucinations.

---

## 5. Non-Functional Requirements

- **Reliability & Availability**: 99.9% uptime target for API and dashboard services.
- **Performance**:
  - API P95 latency < 350ms for analytical queries.
  - Interactive map render < 1.2s for district-level GeoJSON overlays.
  - Scenario simulation execution < 2.5s.
  - MILP optimization solve < 5.0s for national/state candidate sets.
- **Security & Privacy**:
  - Role-Based Access Control (RBAC) with row-level data scoping by state/jurisdiction.
  - Zero PII exposure; full compliance with India's Digital Personal Data Protection (DPDP) Act.
  - Pre-commit secret scanning preventing credential leakage.
- **Accessibility & Internationalization**:
  - WCAG 2.1 AA compliance (high contrast, keyboard navigation, screen-reader semantics).
  - Localization-ready architecture supporting English and Hindi.
