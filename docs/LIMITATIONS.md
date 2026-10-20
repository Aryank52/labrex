# LABREX Limitations & Known Operational Boundaries

**Document Version:** 1.0  
**Authority:** Master Directive Section 96  
**Guiding Principle:** Be completely transparent about capabilities and constraints.  

---

## 1. Data Availability & Geographic Coverage

1. **Informal Sector Representation**:
   - While official surveys (PLFS) and e-Shram provide aggregate signals for informal employment, high-frequency online job postings heavily skew toward formal, organized industrial and service sectors.
   - For rural and informal trades, LABREX relies on survey panels and administrative training registries with lower reporting frequency.
2. **District-Level Granularity**:
   - In newly formed districts or remote tribal regions (e.g. Gadchiroli), administrative reporting may have lower sample sizes. LABREX explicitly flags these regions with a `LOW DATA CONFIDENCE` badge.

---

## 2. Modeling & Forecasting Limitations

1. **Long-Horizon Uncertainty**:
   - Forecasts for 3- and 6-month horizons demonstrate high empirical reliability (WAPE < 10%).
   - Forecasts for 18- and 24-month horizons carry wider prediction intervals due to macroeconomic shifts, global trade policies, and unexpected supply chain disruptions.
2. **Policy Recommendation Disclaimers**:
   - The Policy Optimizer produces **Model Recommendations** based on mathematical optimization under defined constraints. It does not replace constitutional administrative approvals or local community consultations.
3. **Synthetic Data Boundaries**:
   - During local and staging operation prior to live government API integration, data is provided via verified deterministic fixtures tagged `DEMO_FIXTURE`. These values are illustrative and must not be cited as official census or ministry publications.
