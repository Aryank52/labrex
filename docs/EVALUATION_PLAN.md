# LABREX Model Evaluation & Benchmarking Plan

**Document Version:** 1.0  
**Authority:** Master Directive Section 24, 77 & 89  

---

## 1. Benchmarking Protocol

Every forecasting candidate must be evaluated against a **Seasonal Naive Baseline** across at least 3 historical walk-forward folds.

### Baseline Definition: Seasonal Naive with Drift
$$\hat{Y}_{t+h} = Y_{t+h-12} + \frac{h}{12} \left( Y_t - Y_{t-12} \right)$$
For monthly series, this takes the value from the same month last year and adds the annual drift observed in the most recent period.

---

## 2. Evaluation Criteria Matrix

| Criterion | Target Metric Threshold | Action if Failed |
| :--- | :--- | :--- |
| **Accuracy vs Baseline** | $\text{WAPE}_{\text{model}} < 0.85 \times \text{WAPE}_{\text{baseline}}$ | Model rejected; cannot become Champion. |
| **Uncertainty Calibration** | $75\% \le \text{Empirical Coverage of 80\% Band} \le 85\%$ | Uncertainty estimation retuned or widened. |
| **Leakage Audit** | Zero future features present at inference time | Build failure; immediate disqualification. |
| **Inference Latency** | P95 inference latency < 150ms per series | Model optimized or pre-computed. |

---

## 3. Challenger Model Evaluation (TimesFM-3 vs LightGBM)

- **LightGBM**: Evaluated on engineered lag, rolling statistics, and district-level economic covariates.
- **TimesFM-3**: Evaluated zero-shot on normalized raw series to assess deep foundation model transfer capabilities on Indian labour panels.
- The model with the lower average WAPE and well-calibrated prediction intervals is designated `CHAMPION` in `model_registry`.
