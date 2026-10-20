# LABREX Security Threat Model & Risk Matrix

**Document Version:** 1.0  
**Authority:** Master Directive Section 67  
**Methodology:** STRIDE (Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, Elevation of Privilege)  

---

## 1. Threat Identification & Mitigation Matrix

| Threat Category | Specific Threat | Attack Surface | Severity | Architecture Mitigation | Verification Test | Status |
| :--- | :--- | :--- | :---: | :--- | :--- | :---: |
| **AI / Copilot** | Prompt Injection / System Jailbreak | User query input in `/copilot/query` | **HIGH** | Strict role delimitation, Pydantic tool schemas, zero direct DB/eval access, regex sanitization. | `test_copilot_injection_rejection` | **MITIGATED** |
| **AI / Copilot** | Hallucinated Policy Allocations | LLM response generation | **HIGH** | Output verification engine checks that every number in response text matches tool payload. | `test_copilot_hallucination_check` | **MITIGATED** |
| **Data / Storage** | SQL Injection | API query parameters & filters | **CRITICAL** | Parameterized queries exclusively via SQLAlchemy 2.0 ORM; zero raw string SQL concatenation. | `test_sql_injection_safety` | **MITIGATED** |
| **Web Security** | Cross-Site Scripting (XSS) | Frontend render of occupation / skill text | **HIGH** | React 19 JSX automatic escaping, strict Content Security Policy (CSP) headers. | DevTools XSS payload audit | **MITIGATED** |
| **Web Security** | Cross-Site Request Forgery (CSRF)| State-modifying API endpoints | **MEDIUM** | SameSite=Lax/Strict cookies, Authorization Bearer token header architecture. | CSRF origin check suite | **MITIGATED** |
| **System** | Server-Side Request Forgery (SSRF) | Ingestion webhook / URL fetchers | **HIGH** | Hardcoded internal IP denylists (`10.0.0.0/8`, `169.254.169.254`), outbound domain allowlists. | `test_ssrf_internal_ip_block` | **MITIGATED** |
| **System** | Path Traversal / Arbitrary Read | Report download endpoints (`/reports/*`)| **HIGH** | Filenames validated against strict UUID regex; absolute paths constructed from safe base directory. | `test_report_path_traversal` | **MITIGATED** |
| **Access Control**| Broken Object-Level Auth (BOLA) | District & state analytical queries | **CRITICAL** | Authorization middleware enforces user jurisdiction scope on every SQL query `WHERE state_id = :scope`. | `test_state_planner_scope_isolation` | **MITIGATED** |
| **Availability** | Denial of Service / Optimization Exhaustion | Complex MILP optimization queries | **MEDIUM** | Hard timeout of 5.0 seconds on OR-Tools solver; IP and role-based rate limiting (FastAPI limiter). | `test_rate_limiting_optimization` | **MITIGATED** |
| **Supply Chain** | Vulnerable Third-Party Dependencies | Python `pip` / Node `npm` packages | **HIGH** | Pinned dependency versions in `requirements.txt` and `package.json`; automated dependency scans. | `pip audit` / `npm audit` | **MITIGATED** |
| **Data Integrity**| Data Poisoning in Ingestion | Untrusted external CSV uploads | **HIGH** | Data Quality Engine checks distributions, schema types, and outlier z-scores before Silver promotion. | `test_data_poisoning_rejection` | **MITIGATED** |
| **Confidentiality**| Credential Leakage in Version Control| Git commits | **CRITICAL** | Automated pre-commit hook running `scripts/secret_guard.py` detecting API keys, passwords, and tokens. | `python scripts/secret_guard.py` | **MITIGATED** |

---

## 2. Security Testing & Verification Protocol

- **Automated Pre-Commit**: `python scripts/secret_guard.py` runs before any commit.
- **Continuous Integration (CI)**: GitHub Actions executes `pytest backend/tests/security/` testing prompt injection, SQL parameterization, and authorization boundaries on every Pull Request.
- **Audit Logging**: All security-relevant actions (authentication failure, permission rejection, optimization execution) are logged to `audit_logs` with client IP and user identity.
