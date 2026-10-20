# LABREX Deterministic Demo Scenarios

**Document Version:** 1.0  
**Authority:** Master Directive Section 94 & 95  
**Data Integrity:** Driven by verified deterministic fixtures with stable random seeds.  

---

## 1. Scenario Master Index

The platform includes 7 deterministic scenarios designed to demonstrate every core capability without relying on unpredictable external feeds:

```
+--------------------------------------------------------------------------------------------------+
|                                    DEMO SCENARIOS OVERVIEW                                       |
+-----+-------------------------------+-------------------+----------------------------------------+
| ID  | SCENARIO NAME                 | REGION & SECTOR   | KEY CAPABILITY DEMONSTRATED            |
+-----+-------------------------------+-------------------+----------------------------------------+
| SC1 | Emerging Critical Shortage    | Pune (Automotive) | RADAR detection, Demand Index surge    |
| SC2 | Structural Oversupply         | Bengaluru (IT/CSE)| Supply pipeline surplus vs absorption  |
| SC3 | Sudden Skill Shock            | Ahmedabad (Chem)  | Non-linear demand spike, anomaly score |
| SC4 | Training Capacity Simulation  | Nashik (Renewable)| What-if simulation, net gap reduction  |
| SC5 | Constrained Policy Optimizer  | Maharashtra (All) | Google OR-Tools MILP budget allocation |
| SC6 | Model Disagreement Caution    | Surat (Textiles)  | High dispersion between GBDT & TimesFM |
| SC7 | Low Data Confidence Area      | Gadchiroli (Tribal| Data quality discount & wide bounds    |
+-----+-------------------------------+-------------------+----------------------------------------+
```

---

## 2. Detailed Scenario Specifications

### Scenario 1: Emerging Critical Shortage (Solar PV Technicians in Pune)
- **District**: Pune, Maharashtra (`IN-MH-PUN`).
- **Occupation**: Solar PV Installation Technician (NCO: `7421.0300`).
- **Observed Metrics**:
  - Current Demand Index: 89.2 (Rapid growth: +38% QoQ).
  - Current Supply Index: 45.1 (Fixed ITI training capacity of 120 seats/year).
  - 12-Month Projected Gap: **1,450 workers**.
  - RADAR Status: **CRITICAL** (Confidence: 88%, Agreement: HIGH).
- **Expected Outcome**: Appears as #1 priority alert on executive overview and radar ticker.

### Scenario 2: Structural Oversupply (Entry-Level Web Developers in Bengaluru)
- **District**: Bengaluru Urban, Karnataka (`IN-KA-BLR`).
- **Occupation**: Web Developer / Frontend Trainee (NCO: `2513.0100`).
- **Observed Metrics**:
  - Current Demand Index: 52.0 (Moderating hiring).
  - Current Supply Index: 91.5 (High private polytechnic and bootcamp enrollment: 12,000 trainees/yr).
  - 12-Month Projected Gap: **-4,200 workers (Surplus)**.
  - RADAR Status: **OVERSUPPLY**.
- **Expected Outcome**: Prompts recommendation to reallocate seats toward Cloud Systems and Cybersecurity.

### Scenario 3: Sudden Skill Shock (Battery Chemical Processors in Ahmedabad)
- **District**: Ahmedabad, Gujarat (`IN-GJ-AHM`).
- **Occupation**: Chemical Plant Operator - EV Battery Cell (NCO: `3133.0200`).
- **Observed Metrics**:
  - Demand index accelerates from 30 to 85 within 2 consecutive quarters following a mega-factory announcement.
  - Residual Z-score: 3.8 (Statistical outlier / Skill Shock detected).
  - RADAR Status: **EMERGING SHOCK**.

### Scenario 4: Training Capacity Intervention Simulation (Nashik)
- **Baseline**: Projected shortage of 600 Electric Vehicle Technicians in Nashik.
- **Intervention Input**: Planner adds 200 seats at Government ITI Nashik and 150 seats at a private polytechnic.
- **Simulated Output**:
  - Net projected gap drops from 600 to 250 (-58.3% deficit reduction).
  - Estimated capital/operational cost: ₹45.0 Lakhs.

### Scenario 5: Constrained Budget Optimization (Maharashtra State Skilling)
- **Inputs**: Total Skilling Fund Budget = **₹2.5 Crore (₹25,000,000)**; Allowed interventions = Seat expansion in accredited centres; Minimum cohort = 30 trainees.
- **Optimizer Output**:
  - Solver Status: **OPTIMAL** (Execution time: < 350ms).
  - Recommended actions: 6 specific centre/trade additions across Pune, Nashik, and Nagpur.
  - Total Budget Allocated: ₹2.12 Crore.
  - Net Deficit Reduction: 1,820 skilled workers.

### Scenario 6: Model Disagreement Caution (Textile Machinery in Surat)
- **District**: Surat, Gujarat (`IN-GJ-SUR`).
- **Occupation**: Automated Loom Technician (NCO: `7223.0100`).
- **Forecast Outputs**:
  - Seasonal Naive: 1,200.
  - LightGBM: 1,450.
  - TimesFM-3: 2,100.
  - Relative Dispersion: 0.42 (High).
- **Expected Outcome**: RADAR marks **MODEL AGREEMENT: LOW**. Confidence score is discounted from 0.85 to 0.55. System warns against irreversible infrastructure investments without additional surveys.

### Scenario 7: Low Data Confidence Area (Gadchiroli Tribal District)
- **District**: Gadchiroli, Maharashtra (`IN-MH-GAD`).
- **Observed Metrics**:
  - Sparse online job postings; infrequent training centre reporting.
  - Data Quality Score: 38 / 100.
- **Expected Outcome**: System renders wide 95% uncertainty intervals and displays explicit badge: `LOW DATA CONFIDENCE — SURVEY SUPPLEMENT RECOMMENDED`.
