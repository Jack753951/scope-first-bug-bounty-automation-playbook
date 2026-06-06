> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# lab_headers_cors_baseline

Status: active learning-stage bundle
Created: 2026-05-21
Semantics: candidate-only / hardening metadata

## Purpose

Run a quick HTTP security-header and inert CORS baseline against the authorized local learning靶機.

This bundle is intentionally lightweight under the learning-stage safety-control pause: it uses existing practical scripts instead of adding a new profile/tier/contract first.

## Scripts

1. `scripts/headers_audit.sh`
2. `scripts/cors_audit.sh`

## Current local-lab run

Artifact directory:

```text
<artifact-output-dir>/phase4b_headers_cors_learning_20260521T100814Z/
```

Target:

```text
http://<lab-ip>:3000
```

Execution note:

```text
Windows Git-Bash local execution was used because the Kali SSH wrapper could connect but the shared repo path `/home/kali/projects/cybersec` / `/mnt/hacking` was permission-denied during this run. The target was reachable from the Windows host and health stayed 200/200.
```

## Current observations

Candidate-only hardening leads:

```text
security headers baseline score: 2/9
missing HSTS
missing CSP
missing Referrer-Policy
missing Permissions-Policy
missing COOP
missing COEP
```

Controls / non-findings:

```text
X-Content-Type-Options present
X-Frame-Options or frame-ancestors present
no Set-Cookie observed on root endpoint
CORS audit: 0 misconfiguration hits
pre_health=200
post_health=200
```

## Manual review notes

Do not submit missing headers alone as a finding unless the target program explicitly accepts hardening-only reports.

Promotion requirements:

- Missing CSP needs an actual XSS/script-injection chain to become impactful.
- Missing HSTS is mostly relevant to HTTPS/public/on-path downgrade scenarios, not this local HTTP-only lab observation.
- CORS needs credentialed cross-origin read impact; this run found no CORS candidate.
- Findings remain candidate-only until manual verification, evidence, impact, remediation, and retest notes exist.

## Learning-stage next improvements

- Add a small normalized JSONL importer for `headers_audit/report.md` and `cors_audit/hits.txt` if this bundle becomes a routine baseline.
- Optionally wrap these shell scripts in a Python lab module like the ffuf/Nikto/nmap wrappers, but do not block learning-stage execution on that refactor.
