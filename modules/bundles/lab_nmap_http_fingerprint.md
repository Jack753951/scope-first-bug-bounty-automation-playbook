> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# lab_nmap_http_fingerprint

Status: active bundle / local-lab tool wrapper / candidate-only
Date: 2026-05-21
Adapter: `scripts/lab_modules/lab_nmap_http_fingerprint.py`
Shared helper: `scripts/lab_modules/tool_wrapper_common.py`
Generated runner: `setting/local/lab_nmap_http_fingerprint_run.sh`
Final artifacts: `<artifact-output-dir>/phase4b_tool_wrapper_three_20260521T085200Z/lab_nmap_http_fingerprint/`

## Scope

One vulnerability behavior/capability:

```text
A05:2021 Security Misconfiguration — bounded single-port HTTP service/header fingerprinting
```

This wraps mature tool `nmap` with only the target's known HTTP port and selected HTTP NSE scripts. It is not a broad network scan: host/port are fixed from the approved local lab target.

## OSS/tooling decision

Decision: `wrap`

Considered:

- nmap `http-title` / `http-headers` NSE scripts
- httpx
- OWASP ZAP passive scan

Reason:

`nmap` is installed on the Kali attacker VM and can provide bounded single-port HTTP fingerprint/header leads without crawling or credential use.

## Final local-lab result

Run id:

```text
phase4b_tool_wrapper_three_20260521T085200Z
```

Health:

```text
pre_health=200
post_health=200
```

Candidate leads:

```text
None from this run.
```

Controls:

```text
:3000 open service fingerprint observed
```

The local lab target did not expose additional parsed HTTP script output through this nmap run.

## Output files

```text
observations.jsonl
possible_vulnerabilities.md
health.txt
summary.txt
tool_stdout.txt
tool_stderr.txt
tool_raw.xml
artifact_manifest.txt
```

## Safety semantics

This is not a confirmed finding. Output remains:

```text
candidate-only / metadata/control
```

Missing evidence before finding language:

- determine whether disclosed service/header details are sensitive;
- version/outdatedness confirmation from primary sources;
- redacted evidence packet and report-readiness gate.
