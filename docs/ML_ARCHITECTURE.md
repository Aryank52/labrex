# LABREX Machine Learning & Forecasting Architecture

**Document Version:** 1.0  
**Design Standard:** Champion-vs-Challenger Walk-Forward Validation  
**Core Rule:** Never use random train/test splits on temporal series. Baseline comparison is mandatory.  

---

## 1. Forecasting Problem Formulation

For every tuple of $(\text{Occupation } i, \text{District } j)$ at time $t$, we forecast:
1. **Demand** $\hat{Y}_{ij, t+h}^{D}$ for horizons $h \in \{3, 6, 12, 18, 24\}$ months.
2. **Supply** $\hat{Y}_{ij, t+h}^{S}$ for horizons $h \in \{3, 6, 12, 18, 24\}$ months.
3. **Skill Gap**:
   $$\widehat{\text{Gap}}_{ij, t+h} = \hat{Y}_{ij, t+h}^{D} - \hat{Y}_{ij, t+h}^{S}$$

---

## 2. Model Candidates & Champion-vs-Challenger Strategy

We maintain a strict competition between three model tiers:

```
+--------------------------------------------------------------------------------------------------+
|                                    LABREX MODEL SPECTRUM                                         |
+-------------------+-------------------------------------+----------------------------------------+
| TIER              | ALGORITHM / SPECIFICATION           | ROLE & CRITERIA                        |
+-------------------+-------------------------------------+----------------------------------------+
| 1. BASELINE       | Seasonal Naive ($t - 12$) + Drift   | Mandatory benchmark. Any model failing |
|                   |                                     | to beat Seasonal Naive is REJECTED.    |
+-------------------+-------------------------------------+----------------------------------------+
| 2. GBDT ENSEMBLE  | LightGBM & XGBoost Regressors with  | Primary production champion candidate. |
|                   | lag, rolling, and spatial features  | Fast inference, tabular excellence.    |
+-------------------+-------------------------------------+----------------------------------------+
| 3. FOUNDATION TS  | TimesFM-3 (Zero-shot / fine-tuned)  | Advanced challenger candidate.         |
|                   | Temporal patch transformer          | Captures complex multi-series regimes. |
+-------------------+-------------------------------------+----------------------------------------+
```

---

## 3. Walk-Forward Temporal Validation

```
Fold 1: [--- Train: 2022-2023 ---] -> [Val: 2024 Q1-Q2]
Fold 2: [--- Train: 2022-2024 Q2 ---] -> [Val: 2024 Q3-Q4]
Fold 3: [--- Train: 2022-2024 Q4 ---] -> [Val: 2025 Q1-Q2]
```

### Evaluation Metrics
- **Weighted Absolute Percentage Error (WAPE)**:
  $$\text{WAPE} = \frac{\sum |y_t - \hat{y}_t|}{\sum y_t}$$
- **Mean Absolute Error (MAE)** & **Root Mean Squared Error (RMSE)**.
- **Prediction Interval Coverage Probability (PICP)**: Percentage of actual values falling within the 80% and 95% forecast bands.
- **Mean Scaled Interval Score (MSIS)**: Evaluates sharpness and width of uncertainty bands.

---

## 4. Uncertainty Estimation & Model Disagreement

Every forecast produces:
- Point estimate: $\hat{y}_t$
- 80% Prediction Interval: $[L_{80}, U_{80}]$ (via quantile loss or conformal prediction)
- 95% Prediction Interval: $[L_{95}, U_{95}]$

### Model Agreement Indicator
When multiple models generate predictions ($\hat{y}_{\text{naive}}$, $\hat{y}_{\text{lgbm}}$, $\hat{y}_{\text{timesfm}}$), we calculate **Relative Dispersion**:
$$\text{Dispersion} = \frac{\max(\hat{y}) - \min(\hat{y})}{\text{median}(\hat{y})}$$
- $\text{Dispersion} \le 0.10 \implies$ **HIGH AGREEMENT**
- $0.10 < \text{Dispersion} \le 0.25 \implies$ **MEDIUM AGREEMENT**
- $\text{Dispersion} > 0.25 \implies$ **LOW AGREEMENT** (Flags caution on policy decisions)

---

## 5. Hierarchical Reconciliation (National -> State -> District)

Forecasts are generated bottom-up at the district level and reconciled using **MinT (Minimum Trace)** or **Optimal Bottom-Up Coherence** so that:
$$\sum_{j \in \text{State}} \hat{Y}_{ij, t+h} \equiv \hat{Y}_{i, \text{State}, t+h}$$
Dashboard totals will never contradict their constituent district records.
