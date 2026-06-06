> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Phase 4B headers/CORS learning run

Status: completed / candidate-only
Date: 2026-05-21
Run ID: phase4b_headers_cors_learning_20260521T100814Z
Target: http://<lab-ip>:3000

## Why this run

After the operator paused over-broad internal safety/tier/profile controls for the learning stage, Hermes continued with a script-first local-lab loop: choose useful existing scripts, execute against the authorized local靶機, keep artifacts local, preserve candidate-only semantics, and modularize the useful combination.

## Execution

Initial attempt used the Kali SSH wrapper, but the remote shared repo path was permission-denied:

```text
cd: /home/kali/projects/cybersec: Permission denied
cd: /mnt/hacking: Permission denied
```

Because the target was reachable from the Windows host, the run continued from Windows Git-Bash local execution.

Commands executed conceptually:

```text
bash scripts/headers_audit.sh --yes -o <artifact-output-dir>/phase4b_headers_cors_learning_20260521T100814Z/headers_audit http://<lab-ip>:3000
bash scripts/cors_audit.sh --yes -o <artifact-output-dir>/phase4b_headers_cors_learning_20260521T100814Z/cors_audit http://<lab-ip>:3000
```

## Artifacts

```text
<artifact-output-dir>/phase4b_headers_cors_learning_20260521T100814Z/
<artifact-output-dir>/phase4b_headers_cors_learning_20260521T100814Z/headers_audit/report.md
<artifact-output-dir>/phase4b_headers_cors_learning_20260521T100814Z/headers_audit/scores.csv
<artifact-output-dir>/phase4b_headers_cors_learning_20260521T100814Z/cors_audit/report.md
<artifact-output-dir>/phase4b_headers_cors_learning_20260521T100814Z/cors_audit/hits.txt
<artifact-output-dir>/phase4b_headers_cors_learning_20260521T100814Z/possible_vulnerabilities.md
modules/bundles/lab_headers_cors_baseline.md
```

## Health

```text
pre_health=200
post_health=200
```

## Candidate-only observations

Security headers audit:

```text
score: 2/9
present: X-Content-Type-Options, X-Frame-Options/frame-ancestors
missing: Strict-Transport-Security, Content-Security-Policy, Referrer-Policy, Permissions-Policy, Cross-Origin-Opener-Policy, Cross-Origin-Embedder-Policy
Set-Cookie: none on tested root endpoint
```

CORS audit:

```text
URLs tested: 1
Misconfig hits: 0
```

## Interpretation

These are hardening / metadata observations, not confirmed vulnerabilities.

Missing headers should not become a reportable finding unless chained with concrete impact or accepted by the target program rules. CORS produced no candidate in this run.

## Next suggested script-first step

Now that headers/CORS baseline is captured, the next learning-stage run can move to one higher-signal class:

```text
SQLi triage or LFI/path traversal triage against the disposable local lab
```

Because the learning-stage pause is active, do not block that on a new safety profile; keep it local, cap obvious runaway behavior, save artifacts, recover if needed, and keep outputs candidate-only.
