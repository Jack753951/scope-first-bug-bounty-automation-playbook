> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# lab_auth_surface_no_bruteforce

Status: draft-active bundle / local-learning-lab / candidate-only
Date: 2026-05-22
Adapter: `scripts/lab_modules/lab_auth_surface_no_bruteforce.py`
Generated runner: `setting/local/lab_auth_surface_no_bruteforce_run.sh`
Latest artifacts: `<artifact-output-dir>/phase4b_owasp_cve_continuation_20260521T232928Z/lab_auth_surface_no_bruteforce/`

## Use when

Use this bundle when preview/recon shows login, account, user, security-question, or session endpoints and the goal is authentication-surface mapping without credential attempts.

## OWASP / CVE mapping

- OWASP A07:2021 Identification and Authentication Failures.
- OWASP A01:2021 Broken Access Control, limited to unauthenticated metadata/access-gate observations.
- CVE: none claimed by default; auth-surface exposure is context dependent.

## Mature OSS/tooling recon

Decision: reference mature tools but exclude brute force from this bundle.

- OWASP ZAP: passive auth/session observation after scope gate.
- Burp Suite Community: manual proxy verification only; no Intruder/brute-force default.
- ffuf: tiny fixed auth path discovery only.
- hydra: explicitly excluded here; no username/password fuzzing.

## What it runs

Fixed GET-only probes:

```text
/login
/#/login
/rest/user/login
/rest/user/whoami
/api/Users
/api/SecurityQuestions
/rest/admin/application-configuration
```

## Controls

- No usernames, passwords, token replay, credential stuffing, lockout testing, brute force, or session theft.
- 401/403 are treated as access-control observations, not bypasses.
- 200 + root-body hash is treated as SPA/router fallback.

## Missing evidence before finding language

- Manual verification of unauthenticated reachability and endpoint purpose.
- Demonstrable impact beyond route existence.
- Redacted evidence packet and report-readiness review.
