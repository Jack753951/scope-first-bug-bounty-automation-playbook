> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# lab_ffuf_sensitive_path_discovery

Status: active bundle / local-lab tool wrapper / candidate-only
Date: 2026-05-21
Adapter: `scripts/lab_modules/lab_ffuf_sensitive_path_discovery.py`
Shared helper: `scripts/lab_modules/tool_wrapper_common.py`
Generated runner: `setting/local/lab_ffuf_sensitive_path_discovery_run.sh`
Final artifacts: `<artifact-output-dir>/phase4b_tool_wrapper_three_20260521T085200Z/lab_ffuf_sensitive_path_discovery/`

## Scope

One vulnerability behavior/capability:

```text
A05:2021 Security Misconfiguration — exposed sensitive/admin/metadata path discovery
```

This wraps mature tool `ffuf` instead of rejecting it as too broad. The wrapper constrains it to the authorized disposable local lab, a tiny static wordlist, rate/thread caps, timeout, pre/post health, no credentials, no callbacks, no public target, and candidate-only parsing.

## OSS/tooling decision

Decision: `wrap`

Considered:

- ffuf
- gobuster
- wfuzz
- OWASP ZAP spider

Reason:

`ffuf` is installed on the Kali attacker VM and provides useful bounded path-discovery coverage when constrained to a tiny lab wordlist, rate cap, and candidate-only parser.

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
/rest/admin/application-configuration
/metrics
/api-docs
/ftp
/robots.txt
```

Suppressed controls / likely SPA fallback:

```text
/admin
/administration
/backup
/server-status
/debug
/.git/HEAD
/swagger.json
```

## Output files

```text
observations.jsonl
possible_vulnerabilities.md
health.txt
summary.txt
tool_raw.json
tool_stderr.txt
wordlist.txt
artifact_manifest.txt
```

## Safety semantics

This is not a confirmed finding. Output remains:

```text
candidate-only / needs_manual_review
```

Missing evidence before finding language:

- manual publicness/intent check;
- authenticated versus unauthenticated comparison where relevant;
- redacted evidence packet;
- impact analysis;
- report-readiness gate.
