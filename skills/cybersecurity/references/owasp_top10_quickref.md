> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# OWASP Top 10 (2021) — Quick Reference

Each entry: definition → minimal example → root-cause fix → recommended lab.

---

## A01:2021 — Broken Access Control
- **What**: Server fails to enforce that the user is allowed to perform the action.
- **Examples**: IDOR (`/api/users/123` → change to `124`); forced browsing to admin panels; missing `@PreAuthorize`.
- **Fix**: Centralized authorization layer; deny-by-default; check on the server, never trust the client.
- **CWE**: 285, 639, 200.
- **Lab**: PortSwigger Academy → "Access control vulnerabilities" track.

## A02:2021 — Cryptographic Failures
- **What**: Sensitive data exposed via weak crypto, plaintext storage, missing TLS.
- **Examples**: MD5 password hashes; hard-coded keys; HTTP for login; no HSTS.
- **Fix**: Argon2id / bcrypt for passwords; TLS 1.2+ everywhere; secrets in KMS/Vault, not config.
- **CWE**: 327, 326, 798.
- **Lab**: Cryptopals Set 1–3.

## A03:2021 — Injection
- **What**: Untrusted input concatenated into a parser (SQL, OS shell, LDAP, NoSQL, OS command).
- **Example payload (SQLi)**: `1' OR '1'='1` ; `'; DROP TABLE users;--`
- **Fix**: Parameterized queries / prepared statements; ORM with bound parameters; safe APIs (`exec` argv list, never string concat).
- **CWE**: 89, 78, 90.
- **Lab**: PortSwigger SQLi labs (free); DVWA SQLi.

## A04:2021 — Insecure Design
- **What**: Architectural flaws — missing rate limits, no threat model, business-logic abuse paths.
- **Example**: Password reset that emails the new password; gift-card endpoint without quota.
- **Fix**: Threat modelling (STRIDE) before code; misuse cases in user stories; security requirements in DoD.
- **CWE**: 209, 256, 501.

## A05:2021 — Security Misconfiguration
- **What**: Defaults left on, debug pages exposed, verbose errors, headers missing.
- **Examples**: `actuator/env` exposed; `X-Frame-Options` missing; default Tomcat creds.
- **Fix**: Hardening baselines (CIS); minimal images; CI-time config scanning (tfsec, Checkov, Trivy).
- **CWE**: 16, 209.

## A06:2021 — Vulnerable & Outdated Components
- **What**: Using libraries with known CVEs.
- **Example**: log4j 2.14 → Log4Shell.
- **Fix**: SBOM (CycloneDX/SPDX); Dependabot/Renovate; SCA in CI (Snyk, Trivy, OSV-Scanner).
- **CWE**: 1104.

## A07:2021 — Identification & Authentication Failures
- **What**: Weak login flow — credential stuffing, no MFA, predictable session IDs, weak password reset.
- **Fix**: Rate limiting + account lockout with CAPTCHA; MFA (TOTP/WebAuthn); session IDs with ≥128 bits entropy; rotate on auth.
- **CWE**: 287, 384, 521.

## A08:2021 — Software & Data Integrity Failures
- **What**: Insecure deserialization; unsigned updates; CI/CD pipeline trust gaps.
- **Examples**: Java `ObjectInputStream`; Python `pickle.load`; package typosquatting.
- **Fix**: Sign artefacts (cosign / Sigstore); pin dependencies by hash; allowlist deserialization classes; SLSA framework.
- **CWE**: 502, 829.

## A09:2021 — Security Logging & Monitoring Failures
- **What**: No audit trail → can't detect or respond.
- **Fix**: Centralised logs (SIEM); log auth events, admin changes, access denied; retention ≥90 days; alerts on anomalies.
- **CWE**: 778, 117.

## A10:2021 — Server-Side Request Forgery (SSRF)
- **What**: Server fetches a URL the attacker controls.
- **Common targets**: `http://169.254.169.254/` (cloud metadata), internal services, file://.
- **Fix**: Egress allowlist; deny RFC1918 + link-local + metadata IP; protocol allowlist (https only); IMDSv2 on AWS.
- **CWE**: 918.
- **Lab**: PortSwigger SSRF labs.

---

## API-specific (OWASP API Top 10 – 2023)

| Code | Title | Quick Detection Signal |
|------|-------|-------------------------|
| API1 | Broken Object Level Authorization (BOLA / IDOR) | Same endpoint behaves identically for any object ID |
| API2 | Broken Authentication | JWT alg=none accepted, refresh token reuse |
| API3 | Broken Object Property Level Authorization | PATCH writes a server-only field (mass assignment) |
| API4 | Unrestricted Resource Consumption | No rate limits, no pagination cap |
| API5 | Broken Function Level Authorization | Hidden admin endpoints reachable by user role |
| API6 | Unrestricted Access to Sensitive Business Flow | Bot signs up 10 000 accounts/day |
| API7 | SSRF | Same as A10 |
| API8 | Security Misconfiguration | CORS `*` with credentials, debug enabled |
| API9 | Improper Inventory Management | `/api/v1/` deprecated and vulnerable still live |
| API10 | Unsafe Consumption of APIs | Trusting partner API responses without validation |
