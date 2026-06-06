> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# lab_sqli_acquisition_triage

Status: active learning-stage bundle
Created: 2026-05-21
Semantics: candidate-only / needs_manual_review
OWASP mapping: A03:2021 Injection / SQL injection learning track

## Purpose

Use the newly acquired mature SQLi tooling and wordlists against the authorized disposable local靶機, then preserve the result as a reusable learning-stage bundle.

## Acquisition inputs

Acquisition summary:

```text
handoff/tool_acquisition_wave1_20260521.md
```

Tool/source:

```text
setting/local/tool_acquisition/wave1_20260521/tools/sqlmap
```

Useful wordlists for follow-up:

```text
setting/local/tool_acquisition/wave1_20260521/wordlists/sqli_quick.txt
setting/local/tool_acquisition/wave1_20260521/wordlists/sqli_generic.txt
setting/local/tool_acquisition/wave1_20260521/wordlists/sqli_low_risk_boolean_blind.txt
```

## Current local-lab run

Artifact directory:

```text
<artifact-output-dir>/phase4b_sqli_acquisition_learning_20260521T105021Z/
```

Target tested:

```text
http://<lab-ip>:3000/rest/products/search?q=test
```

Command shape:

```text
python setting/local/tool_acquisition/wave1_20260521/tools/sqlmap/sqlmap.py \
  -u 'http://<lab-ip>:3000/rest/products/search?q=test' \
  --batch --level 1 --risk 1 --time-sec 2 --timeout 8 --retries 0 --threads 1 \
  --output-dir=<artifact>/sqlmap-output --flush-session
```

Health:

```text
pre_health=200
post_health=200
```

## Current observations

```text
GET parameter q appeared dynamic
sqlmap did not identify q as injectable at bounded level/risk
sqlmap observed HTTP 500 responses during probes: 32 times
```

## Candidate-only interpretation

This run did not produce a confirmed SQLi candidate. The repeated HTTP 500 responses are worth manual review as robustness/error-handling leads, but they are not proof of SQL injection.

## Suggested next SQLi learning steps

1. Find a known intentionally vulnerable Juice Shop SQLi flow or endpoint, likely login/auth-related, instead of blindly escalating this search endpoint.
2. If using sqlmap again, keep local-lab target only and preserve pre/post health.
3. Build a small project-owned parser/importer for sqlmap stdout/session output only after one or two useful local-lab runs show the output shape we need.
4. Keep sqlmap output as candidate-only; no automatic finding promotion.
