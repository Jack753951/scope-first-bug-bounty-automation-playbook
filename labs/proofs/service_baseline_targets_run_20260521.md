> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Service baseline targets lab run

Status: completed local-learning-lab run / candidate-only
Date: 2026-05-21
Target: `http://<lab-ip>:3000/`
Bundle: `lab_service_baseline_targets`
Adapter: `scripts/lab_modules/lab_service_baseline_targets.py`
Generated runner: `setting/local/lab_service_baseline_targets_run.sh`
Artifacts: `<artifact-output-dir>/phase4b_service_baseline_targets_20260521T135015Z/`

## Scope/safety

- Target is inside `<lab-ip>/16` from `config/scope.txt`.
- Output remains `candidate-only / needs_manual_review`.
- No credential attempts, brute force, config exfiltration, confirmed-finding promotion, or report submission.

## Execution notes

First actual execution found two implementation bugs:

1. `/;csv` was emitted unquoted and shell interpreted `;csv` as a command.
2. Generated runner used `python3`, which resolves to the WindowsApps shim in this Git-Bash environment and exits with code 49 for heredoc execution.

Fixes applied:

- Quote service paths in generated runner, including `'/;csv'`.
- Use `python - "$outdir" <<'PY'` in the generated runner.
- Switch generated runner template to raw f-string so embedded Python `\n` stays valid.
- Add `root_body.sha256` comparison to detect generic SPA/router fallback.
- Treat OpenSSL `no peer certificate available` / `Cipher is (NONE)` as TLS control, not TLS candidate.

## Final run result

Final runner exit code: `0`.

Health:

```text
pre_health=200
post_health=200
```

Artifacts created:

```text
artifact_manifest.txt
health.txt
http_probe_results.tsv
observations.jsonl
openssl_s_client.txt
possible_vulnerabilities.md
root_body.sha256
summary.txt
tool_raw.xml
tool_stderr.txt
tool_stdout.txt
```

## Candidate-only summary

One candidate remained after generic root-fallback filtering:

```text
traefik /metrics status=200 signal `traefik_service_baseline_candidate`
content_type=text/plain; version=0.0.4; charset=utf-8
```

Interpretation: candidate-only metadata exposure lead. Needs manual verification before any finding language.

## Controls / false-positive suppression

Most Apache/Tomcat/HAProxy/Envoy/Traefik service paths returned HTTP 200, but their body hash matched the application root. The scanner now classifies these as generic root fallback controls rather than service-specific candidates.

Examples:

```text
apache /server-status -> apache_generic_root_fallback_control
tomcat /manager/html -> tomcat_generic_root_fallback_control
haproxy /haproxy?stats -> haproxy_generic_root_fallback_control
envoy /stats/prometheus -> envoy_generic_root_fallback_control
traefik /dashboard/ -> traefik_generic_root_fallback_control
```

Envoy `:9901/*` probes timed out and were classified as controls. Traefik API paths returned 500 and were classified as controls.

OpenSSL/TLS against the HTTP port produced no peer certificate and `Cipher is (NONE)`, so it is now classified as `openssl_tls_metadata_control`.

## Tool/environment notes

- `nmap` was not available in this Windows Git-Bash runtime, so the nmap XML artifact is empty and stderr records `missing tool: nmap`.
- For fuller service baseline coverage, run the same generated script in Kali where `nmap` is installed, or install/route nmap in this environment.

## Missing evidence before finding language

- Manually verify `/metrics` content and whether it is service-specific or app-level metrics.
- Confirm whether it belongs to Traefik, another component, or Juice Shop/application instrumentation.
- Add redacted evidence and impact analysis only if manual verification supports it.
- Keep this out of report/submission language until report-readiness gates pass.
