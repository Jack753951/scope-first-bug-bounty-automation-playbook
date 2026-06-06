> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Phase 4B SQLi acquisition-backed learning run

Status: completed / candidate-only
Date: 2026-05-21
Run ID: phase4b_sqli_acquisition_learning_20260521T105021Z
Target: http://<lab-ip>:3000/rest/products/search?q=test
Tool: sqlmap from `setting/local/tool_acquisition/wave1_20260521/tools/sqlmap`
OWASP mapping: A03:2021 Injection / SQL injection learning track

## Why this run

The operator asked to download/organize the first batch of new scripts and wordlists while continuing OWASP vulnerability implementation modularization.

Hermes acquired mature sources locally under git-ignored `setting/local/tool_acquisition/wave1_20260521/`, then used sqlmap in a bounded local-lab run against the authorized learning靶機.

## Command shape

```text
python setting/local/tool_acquisition/wave1_20260521/tools/sqlmap/sqlmap.py \
  -u 'http://<lab-ip>:3000/rest/products/search?q=test' \
  --batch --level 1 --risk 1 --time-sec 2 --timeout 8 --retries 0 --threads 1 \
  --output-dir=<artifact-output-dir>/phase4b_sqli_acquisition_learning_20260521T105021Z/sqlmap-output \
  --flush-session
```

## Artifacts

```text
<artifact-output-dir>/phase4b_sqli_acquisition_learning_20260521T105021Z/
<artifact-output-dir>/phase4b_sqli_acquisition_learning_20260521T105021Z/sqlmap_stdout.txt
<artifact-output-dir>/phase4b_sqli_acquisition_learning_20260521T105021Z/sqlmap_exit.txt
<artifact-output-dir>/phase4b_sqli_acquisition_learning_20260521T105021Z/health.txt
<artifact-output-dir>/phase4b_sqli_acquisition_learning_20260521T105021Z/possible_vulnerabilities.md
```

## Health

```text
pre_health=200
post_health=200
```

## Result summary

```text
GET parameter q appeared dynamic
heuristic basic test suggested q might not be injectable
bounded sqlmap run did not identify q as injectable
sqlmap observed HTTP 500 responses during testing: 32 times
sqlmap_exit=0
```

## Candidate-only interpretation

No confirmed SQL injection from this route.

The repeated HTTP 500 responses are a candidate error-handling/robustness lead, not proof of SQL injection. Manual review is needed before any finding language.

## Modularization output

Added bundle:

```text
modules/bundles/lab_sqli_acquisition_triage.md
```

Acquisition summary:

```text
handoff/tool_acquisition_wave1_20260521.md
```

## Next suggested SQLi step

Use the acquired sqlmap + SQLi wordlists to test a known intentionally vulnerable Juice Shop flow, likely an auth/login-related path, rather than escalating blindly on `/rest/products/search?q=`.
