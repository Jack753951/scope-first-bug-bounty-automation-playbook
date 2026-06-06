> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# lab_metrics_exposure_triage

Status: draft-active bundle / local-learning-lab / candidate-only
Date: 2026-05-21
Adapter: `scripts/lab_modules/lab_metrics_exposure_triage.py`
Generated runner: `setting/local/lab_metrics_exposure_triage_run.sh`
Latest artifacts: `<artifact-output-dir>/phase4b_three_exposure_bundles_20260521T143412Z/lab_metrics_exposure_triage/`

## Use when

Use this bundle when preview/recon or a service baseline suggests `/metrics`, Prometheus, Actuator, or observability endpoint exposure.

## OWASP / CVE mapping

- OWASP A05:2021 Security Misconfiguration
- OWASP A09:2021 Security Logging and Monitoring Failures, only when exposed telemetry creates monitoring/operational risk
- 2025 migration track: exposed observability / misconfiguration leads
- CVE: none claimed by default; metrics exposure is usually configuration/context dependent.

## Mature OSS/tooling recon

Decision: wrap/reference mature tools; keep first pass GET-only and redacted.

- promtool from Prometheus (`prometheus/prometheus`, Apache-2.0): offline format sanity for Prometheus text metrics.
- nuclei (`projectdiscovery/nuclei`, MIT): allowlisted exposed metrics templates after scope gate.
- ffuf (`ffuf/ffuf`, MIT): bounded metrics path discovery.
- OWASP ZAP (`zaproxy/zaproxy`, Apache-2.0): passive metadata review.

## What it runs

Fixed GET-only probes:

```text
/metrics
/prometheus
/stats/prometheus
/actuator/prometheus
/actuator/metrics
```

## Inputs

```bash
MSYS2_ARG_CONV_EXCL='*' python scripts/lab_modules/lab_metrics_exposure_triage.py \
  --target http://<lab-ip>:3000/ \
  --lab-approved \
  --out-script setting/local/lab_metrics_exposure_triage_run.sh \
  --output-dir /tmp/lab_metrics_exposure_triage
bash setting/local/lab_metrics_exposure_triage_run.sh
```

## Outputs

```text
observations.jsonl
http_probe_results.jsonl
possible_vulnerabilities.md
summary.txt
tool_stdout.txt
tool_stderr.txt
artifact_manifest.txt
```

## Candidate / control logic

Candidate:

- HTTP 200/redirect with metrics keywords such as `# HELP`, `# TYPE`, `process_`, `nodejs_`, `http_`, or `metrics`.
- Body hash differs from `/` root.

Controls:

- 404/401/403/timeout.
- HTTP 200 with same body hash as `/` root.
- Metrics path exists but content lacks metrics-like markers.

## Latest local-lab result

Candidate-only lead:

```text
/metrics status=200 content_type=text/plain; version=0.0.4; charset=utf-8 bytes=25971
keywords=['# help', '# type', 'process_', 'nodejs_', 'http_']
```

Controls:

- `/prometheus`, `/stats/prometheus`, `/actuator/prometheus`, and `/actuator/metrics` were generic SPA/root fallback controls.

## Missing evidence before finding language

- Manually inspect/redact metrics names and labels.
- Determine if exposed data is app-level, infrastructure-level, or sensitive operational telemetry.
- Confirm impact before report language.
- Do not retain secrets or raw sensitive metric labels in committed docs.
