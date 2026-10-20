# LABREX Security Architecture & Access Control

**Document Version:** 1.0  
**Authority:** Master Directive Section 43, 44 & 45  
**Compliance Standard:** ISO/IEC 27001 & India Digital Personal Data Protection (DPDP) Act  

---

## 1. Authentication & Identity Management

- **Protocol**: OpenID Connect (OIDC) / OAuth 2.0 with JSON Web Tokens (JWT).
- **Token Signing**: RS256 (Asymmetric key pair) in production; HS256 for local development.
- **Token Expiry**:
  - Access Token: 60 minutes.
  - Refresh Token: 7 days with rotation and single-use revocation.
- **Password Security**: Passwords hashed using `bcrypt` (work factor 12) or Argon2id.

---

## 2. Role-Based & Attribute-Based Access Control (RBAC / ABAC)

LABREX enforces hierarchical roles combined with spatial jurisdictional boundaries:

```
+--------------------------------------------------------------------------------------------------+
|                                    LABREX RBAC / ABAC MATRIX                                     |
+---------------------+-------------------------------+--------------------------------------------+
| ROLE                | GEOGRAPHIC SCOPE              | PERMITTED CAPABILITIES                     |
+---------------------+-------------------------------+--------------------------------------------+
| `NATIONAL_PLANNER`  | National (All States & Dist)  | Full Read, Scenario Sim, Policy Optimizer, |
|                     |                               | Copilot, PDF/CSV Reports, Model View       |
+---------------------+-------------------------------+--------------------------------------------+
| `STATE_PLANNER`     | Assigned State(s) Only        | Read assigned state & constituent districts|
|                     |                               | Scenario Sim & Optimization within state   |
+---------------------+-------------------------------+--------------------------------------------+
| `SECTOR_ANALYST`    | Assigned Sector(s) National   | Deep dive in sector occupations & skills   |
|                     |                               | Scenario simulation for target sector      |
+---------------------+-------------------------------+--------------------------------------------+
| `DATA_ANALYST`      | Assigned Datasets             | Data Lineage, Model Evaluation, Quality    |
+---------------------+-------------------------------+--------------------------------------------+
| `ADMIN`             | System-wide                   | User management, role assignment, audit    |
+---------------------+-------------------------------+--------------------------------------------+
```

---

## 3. Secret Management & Ingestion Security

1. **Zero Secret Storage in Code**:
   - All credentials, DB URLs, JWT secrets, and API keys are loaded via environment variables (`.env` locally, Google Cloud Secret Manager in production).
   - `scripts/secret_guard.py` enforces pre-commit scanning across the repository.
2. **Database Encryption**:
   - Encryption at Rest via Cloud SQL AES-256.
   - Encryption in Transit via TLS 1.3 enforced for all client-to-API and API-to-database connections.
3. **Data Protection & Privacy**:
   - No Personally Identifiable Information (PII) of individual job applicants or trainees is stored in the core analytics facts. All trainee figures are aggregated at the qualification and training centre level.
