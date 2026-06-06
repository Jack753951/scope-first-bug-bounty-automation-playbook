> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# OWASP 2017/2021/2025 single-vulnerability modularization tracker

Status: active tracking matrix / runtime requires per-wave gate
Date: 2026-05-21
Skill: `owasp-single-vuln-lab-wave`

## Purpose

Track every OWASP Top 10 category in 2017, 2021, and 2025/migration-track so each vulnerability class can be tested one-by-one against the local靶機 and retained as a reusable module: adapter -> lab run -> importer -> candidate-review bridge -> bundle docs.

## Recovery/destructive gate

- Local lab target observed: `http://<lab-ip>:3000/`.
- Attacker VM: `<attacker-vm>` / `<lab-ip>`, host-only route only.
- Victim VM: `<victim-vm>` / `<lab-ip>`.
- Victim snapshots found: `setup-complete-with-tools`, `pre-aggressive-current-running-recovery-20260521-093252`.
- Attacker snapshot found: `clean-before-aggressive-tests-20260521-093233`.
- Destructive waves are allowed only after the wave plan includes automatic snapshot restore and post-restore health verification. If restore is not verified immediately before the wave, downgrade to bounded non-destructive mode.

## Current reusable coverage

| Bundle/adapter | Status | Use when |
|---|---|---|
| `lab_directory_listing_triage` | active | `/ftp/` or directory-listing/security-misconfiguration candidate |
| `benign_reflection_redirect_triage` | active | query reflection/open-redirect candidate; inert canaries only |
| `lab_access_control_unauth_route_metadata` | active | A01 broken access-control fixed unauthenticated route metadata with controls |
| `lab_crypto_transport_metadata` | active | A02 crypto/transport HTTP/cookie metadata controls |
| `lab_exceptional_condition_metadata` | active | A10:2025 exceptional-condition/error-handling metadata |
| `lab_ffuf_sensitive_path_discovery` | active | A05 ffuf wrapped sensitive/admin/metadata path discovery on disposable lab |
| `lab_nikto_server_misconfig` | active | A05 Nikto wrapped server/header/default-file misconfiguration leads |
| `lab_nmap_http_fingerprint` | active | A05 nmap wrapped single-port HTTP fingerprint/header controls |
| `wave1a_metadata.py` + importer + bridge | partial active baseline | low-risk metadata, `/api-docs/`, `/robots.txt`, CORS, known paths |
| `lab_auth_surface_no_bruteforce` | draft-active | A07 auth-surface metadata without brute force or credential attempts |
| `lab_component_metadata_triage` | draft-active | A06 vulnerable/outdated component metadata and Retire.js/npm/OSV follow-up clues |
| `lab_integrity_metadata_triage` | draft-active | A08 software/data integrity/security metadata, no tampering tests |
| `lab_api_docs_metrics_manual_verification` | mini-bundle | API docs + metrics manual verification and A09 logging/monitoring checklist |
| `verified_lab_flow_sqli_auth_bypass_admin_users_read` | verified-lab-flow | Kali-side SQLi auth bypass -> admin lab token -> protected `/api/Users` read |
| `verified_lab_flow_unauth_admin_config_read` | verified-lab-flow | unauthenticated admin configuration read with JSON evidence |
| `verified_lab_flow_directory_listing_file_read` | verified-lab-flow | `/ftp/` listing plus bounded file reads; Kali wave 2 also observed `incident-support.kdbx` status/metadata |
| `verified_lab_flow_api_docs_metrics_exposure` | verified-lab-flow | unauthenticated Swagger/OpenAPI and Prometheus metrics exposure |
| `verified_lab_flow_file_upload_marker_pdf` | verified-lab-flow | Kali-side SQLi-derived admin session accepted marker PDF upload with HTTP 204; not RCE/arbitrary write |

## Release/category tracker

| Release | Category | Name | 2021 mapping | Current reusable module state | Runtime tier note |
|---:|---|---|---|---|---|
| 2017 | `A01:2017` | Injection | A03:2021 | benign_reflection_redirect_triage (partial active for inert reflection/redirect only; injection-specific exploit modules pending) | T3/T4 benign-marker local-lab only; no exploit chains |
| 2017 | `A02:2017` | Broken Authentication | A07:2021 | `lab_auth_surface_no_bruteforce` draft-active: auth surface/checklist, no brute force or credential attempts | T1/T2 metadata/manual; no brute force |
| 2017 | `A03:2017` | Sensitive Data Exposure | A02:2021 | `lab_crypto_transport_metadata` active: bounded HTTP/cookie/API transport metadata only; TLS scanner wrapper deferred | T1/T2 passive metadata local-lab only |
| 2017 | `A04:2017` | XML External Entities (XXE) | A05:2021 | not yet modularized; destructive/parser-risk lab wave requires recovery gate | T1/T2 bounded metadata local-lab only |
| 2017 | `A05:2017` | Broken Access Control | A01:2021 | `lab_access_control_unauth_route_metadata` active: unauthenticated fixed-route metadata with auth-gate and SPA-fallback controls; credential/session matrix still deferred | T0/T3 planned; T4 only for approved local-lab workflow |
| 2017 | `A06:2017` | Security Misconfiguration | A05:2021 | active: `lab_directory_listing_triage`, `wave1a_metadata_baseline`, `lab_ffuf_sensitive_path_discovery`, `lab_nikto_server_misconfig`, `lab_nmap_http_fingerprint`; mature-tool wrappers are lab-only/candidate-only | T1/T3 local-lab tool wrappers; public targets require program scope/rules |
| 2017 | `A07:2017` | Cross-Site Scripting (XSS) | A03:2021 | benign_reflection_redirect_triage (partial active for inert reflection/redirect only; injection-specific exploit modules pending) | T3/T4 benign-marker local-lab only; no exploit chains |
| 2017 | `A08:2017` | Insecure Deserialization | A08:2021 | not yet modularized; destructive/parser-risk lab wave requires recovery gate | T1/T2 metadata/checklist only |
| 2017 | `A09:2017` | Using Components with Known Vulnerabilities | A06:2021 | `lab_component_metadata_triage` draft-active: static package/version clues; Retire.js/npm/OSV correlation deferred/manual | T1/T2 metadata-only |
| 2017 | `A10:2017` | Insufficient Logging & Monitoring | A09:2021 | `lab_api_docs_metrics_manual_verification` mini-bundle active as log/alert observability checklist and lab evidence workflow | T0/T1 evidence/logging checklist |
| 2021 | `A01:2021` | Broken Access Control | A01:2021 | `lab_access_control_unauth_route_metadata` active: unauthenticated fixed-route metadata with auth-gate and SPA-fallback controls; credential/session matrix still deferred | T0/T3 planned; T4 only for approved local-lab workflow |
| 2021 | `A02:2021` | Cryptographic Failures | A02:2021 | `lab_crypto_transport_metadata` active: bounded HTTP/cookie/API transport metadata only; TLS scanner wrapper deferred | T1/T2 passive metadata local-lab only |
| 2021 | `A03:2021` | Injection | A03:2021 | benign_reflection_redirect_triage (partial active for inert reflection/redirect only; injection-specific exploit modules pending) | T3/T4 benign-marker local-lab only; no exploit chains |
| 2021 | `A04:2021` | Insecure Design | A04:2021 | not yet modularized; checklist/threat-model module first | T0/T1 checklist/reporting |
| 2021 | `A05:2021` | Security Misconfiguration | A05:2021 | active: `lab_directory_listing_triage`, `wave1a_metadata_baseline`, `lab_ffuf_sensitive_path_discovery`, `lab_nikto_server_misconfig`, `lab_nmap_http_fingerprint`; candidate-only mature-tool wrappers now allowed for disposable lab | T1/T3 local-lab tool wrappers; public targets require program scope/rules |
| 2021 | `A06:2021` | Vulnerable and Outdated Components | A06:2021 | `lab_component_metadata_triage` draft-active: static package/version clues; vulnerable-component scanner/importer still deferred/manual | T1/T2 metadata-only |
| 2021 | `A07:2021` | Identification and Authentication Failures | A07:2021 | `lab_auth_surface_no_bruteforce` draft-active: auth surface/checklist, no brute force or credential attempts | T1/T2 metadata/manual; no brute force |
| 2021 | `A08:2021` | Software and Data Integrity Failures | A08:2021 | `lab_integrity_metadata_triage` draft-active plus component metadata clues; no tampering/destructive integrity tests | T1/T2 metadata/checklist only |
| 2021 | `A09:2021` | Security Logging and Monitoring Failures | A09:2021 | `lab_api_docs_metrics_manual_verification` mini-bundle active as log/alert observability checklist and lab evidence workflow | T0/T1 evidence/logging checklist |
| 2021 | `A10:2021` | Server-Side Request Forgery (SSRF) | A10:2021 | not yet modularized; callbacks/OAST blocked unless isolated callback lab is built | T3 planned only; T4/T5 for callbacks/pivots if ever proposed |
| 2025 | `A01:2025` | Broken Access Control | A01:2021 | `lab_access_control_unauth_route_metadata` active: unauthenticated fixed-route metadata with auth-gate and SPA-fallback controls; credential/session matrix still deferred | T0/T3 planned; T4 only for approved local-lab workflow |
| 2025 | `A02:2025` | Security Misconfiguration | A05:2021 | lab_directory_listing_triage + wave1a_metadata_baseline (partial active for directory listing/API-docs/metadata only) | T1/T2 bounded metadata local-lab only |
| 2025 | `A03:2025` | Software Supply Chain Failures | A06:2021, A08:2021 | `lab_component_metadata_triage` + `lab_integrity_metadata_triage` draft-active metadata/checklist coverage; scanner/importer/manual CVE correlation deferred | T1/T2 metadata-only; T1/T2 metadata/checklist only |
| 2025 | `A04:2025` | Cryptographic Failures | A02:2021 | `lab_crypto_transport_metadata` active: bounded HTTP/cookie/API transport metadata only; TLS scanner wrapper deferred | T1/T2 passive metadata local-lab only |
| 2025 | `A05:2025` | Injection | A03:2021 | benign_reflection_redirect_triage (partial active for inert reflection/redirect only; injection-specific exploit modules pending) | T3/T4 benign-marker local-lab only; no exploit chains |
| 2025 | `A06:2025` | Insecure Design | A04:2021 | not yet modularized; checklist/threat-model module first | T0/T1 checklist/reporting |
| 2025 | `A07:2025` | Authentication Failures | A07:2021 | `lab_auth_surface_no_bruteforce` draft-active: auth surface/checklist, no brute force or credential attempts | T1/T2 metadata/manual; no brute force |
| 2025 | `A08:2025` | Software or Data Integrity Failures | A08:2021 | `lab_integrity_metadata_triage` draft-active plus component metadata clues; no tampering/destructive integrity tests | T1/T2 metadata/checklist only |
| 2025 | `A09:2025` | Security Logging and Alerting Failures | A09:2021 | `lab_api_docs_metrics_manual_verification` mini-bundle active as log/alert observability checklist and lab evidence workflow | T0/T1 evidence/logging checklist |
| 2025 | `A10:2025` | Mishandling of Exceptional Conditions | A05:2021, A09:2021, A04:2021 | `lab_exceptional_condition_metadata` active: fixed benign exceptional-condition probes; `/rest/does-not-exist` server-error candidate; destructive-lab error-handling still deferred | T1/T2 bounded metadata local-lab only; T0/T1 evidence/logging checklist; T0/T1 checklist/reporting |


## Verified exploit-flow wave 1 update — 2026-05-21 UTC

Artifact: `<artifact-output-dir>/verified_flow_wave1_20260521T235533Z/`.

Promoted lab-only verified flows:

- A03/A07 chain: SQLi authentication bypass to admin lab JWT, then authenticated `/api/Users` read (`verified_lab_flow_sqli_auth_bypass_admin_users_read`).
- A01: unauthenticated admin application configuration read (`verified_lab_flow_unauth_admin_config_read`).
- A05/A02: exposed `/ftp/` directory listing with bounded file reads (`verified_lab_flow_directory_listing_file_read`).
- A05/A09: unauthenticated Swagger UI/API docs and Prometheus metrics with operational counters (`verified_lab_flow_api_docs_metrics_exposure`).

Not promoted: JWT alg-none probe, coupon/business logic probe, XSS execution marker, source-map disclosure, CORS/header metadata, component/integrity metadata, service default paths, and missing-tool ffuf/nikto/nmap/sqlmap reruns. See `attempted_not_verified_flows_wave1.md`.

## Operating rule

Run one row/class at a time. A row is not complete until it has: tests, bounded/destructive-gated adapter, local lab artifact, importer or explicit deferral, candidate-review bridge or explicit deferral, bundle docs, accepted-change entry, and validation evidence. Outputs remain candidate-only unless a later manual verification/report gate authorizes stronger language.

## Accuracy note

The `Current reusable module state` column is capability-specific, not taxonomy-equivalence-specific. A category mapping to `A05:2021` does not mean the existing directory-listing bundle covers XXE, exception handling, or every misconfiguration subclass. Each class still needs its own single-vulnerability wave before it is considered modularized.
