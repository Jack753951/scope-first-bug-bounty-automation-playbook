> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# lab_nikto_server_misconfig

Status: active bundle / local-lab tool wrapper / candidate-only
Date: 2026-05-21
Adapter: `scripts/lab_modules/lab_nikto_server_misconfig.py`
Shared helper: `scripts/lab_modules/tool_wrapper_common.py`
Generated runner: `setting/local/lab_nikto_server_misconfig_run.sh`
Final artifacts: `<artifact-output-dir>/phase4b_tool_wrapper_three_20260521T085200Z/lab_nikto_server_misconfig/`

## Scope

One vulnerability behavior/capability:

```text
A05:2021 Security Misconfiguration — web server/header/default-file misconfiguration leads
```

This wraps mature scanner `nikto` for the authorized disposable local lab. It is allowed under the lab tooling authorization update, but output is parsed as candidate-only and does not become a confirmed finding.

## OSS/tooling decision

Decision: `wrap`

Considered:

- Nikto
- OWASP ZAP baseline
- nuclei HTTP exposure templates

Reason:

`nikto` is installed on the Kali attacker VM and is useful for server/default-file misconfiguration leads when scoped to the disposable lab and parsed as candidate-only output.

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

Candidate leads from Nikto output:

```text
Access-Control-Allow-Origin: *
Uncommon x-recruiting header pointing to /#/jobs
robots.txt should be manually viewed
Missing permissions-policy
Missing content-security-policy
Missing strict-transport-security
Missing referrer-policy
```

Controls / informational output was separated from candidates.

## Output files

```text
observations.jsonl
possible_vulnerabilities.md
health.txt
summary.txt
tool_stdout.txt
tool_stderr.txt
tool_raw.txt
tool_raw.json.json
artifact_manifest.txt
```

Note: this distro's Nikto appends `.json` to the requested JSON output path, so the raw JSON artifact appears as `tool_raw.json.json`; parser uses safe text fallback for this run.

## Safety semantics

This is not a confirmed finding. Scanner wording is treated as:

```text
candidate-only / needs_manual_review
```

Missing evidence before finding language:

- manual validation of each Nikto message;
- redacted reproduction for header/file issues;
- impact analysis independent of scanner wording;
- report-readiness gate.
