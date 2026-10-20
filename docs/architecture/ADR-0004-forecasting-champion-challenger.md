# ADR-0004: Champion-vs-Challenger Walk-Forward Forecasting Strategy

**Status:** APPROVED  
**Date:** 2026-10-20  
**Deciders:** Principal Engineering Agent  

---

## Context
Labour market forecasting requires strict statistical rigor. Models must not suffer from temporal data leakage. Deep learning foundation models (such as TimesFM-3) sound attractive but may overfit or perform worse than well-tuned gradient-boosted trees (LightGBM/XGBoost) or even simple Seasonal Naive baselines on sparse, noisy regional series.

## Decision
We enforce a **Champion-vs-Challenger** architecture evaluated exclusively via **Walk-Forward Validation**. 
1. Every series must be benchmarked against a **Seasonal Naive with Drift** baseline.
2. Candidate models (LightGBM, XGBoost, TimesFM-3) compete on out-of-time evaluation metrics (WAPE, RMSE, Coverage).
3. A model can only be designated `CHAMPION` if it demonstrates a statistically significant reduction in WAPE over the baseline with well-calibrated prediction intervals.
4. Model disagreement between baseline, GBDT, and deep models is explicitly calculated and presented to users as a confidence indicator.

## Consequences
### Positive
- Prevents unvalidated ML models from reaching production.
- Guarantees complete protection against temporal data leakage.
- Surfaces honest uncertainty and model disagreement to policy planners.

### Negative / Trade-offs
- Requires maintaining multiple model training pipelines and a model registry.
- Walk-forward evaluation increases training compute time.
