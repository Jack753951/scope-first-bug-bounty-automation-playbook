> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Local Proof Packet — @hapi/content <specific-cve-id> parameter smuggling

Status: verified local-lab proof / sanitized summary
Date: 2026-05-28
Verified at: 2026-05-28T11:00:42.460Z
Verdict: `verified_hapi_content_cve_2026_44974_parameter_smuggling_local_lab`

## Selected candidate

- Source: GitHub Advisory
- ID: `<specific-ghsa-id>`
- CVE: `<specific-cve-id>`
- Title: `@hapi/content header parser has a parameter smuggling issue that allows upload-filter bypass via duplicate parameters`
- Vulnerable package/range: npm `@hapi/content < 6.0.2`
- Tested vulnerable version: `@hapi/content@6.0.1`
- Patched control version: `@hapi/content@6.0.2`
- Advisory published: `2026-05-27T00:37:20Z`

## Boundary

Local Kali victim-lab only. No live target, public IP/domain, scanner/fuzzer/DAST, callback/OAST, credential/token handling, secret/system file access, persistence, or report submission.

## Execution

- Victim-side artifact: `/home/kali/codex-output/<artifact-output-dir>/three_latest_npm_vulns_20260528T110251Z/`
- Pulled sanitized evidence: `<artifact-output-dir>/three_latest_npm_vulns_20260528T110251Z/evidence/`
- Package environment was built on the Windows control plane and transferred to the isolated victim.

## Sanitized evidence

Key observed values from `hapi_content_smuggling_proof.json`:

```text
status: verified
vulnerable_version: 6.0.1
patched_control_version: 6.0.2
vulnerable duplicate filename result: shell.php
patched duplicate filename result: rejected
patched duplicate boundary result: rejected
```

Evidence files:

- `<artifact-output-dir>/three_latest_npm_vulns_20260528T110251Z/evidence/summary.json`
- `<artifact-output-dir>/three_latest_npm_vulns_20260528T110251Z/evidence/hapi_content_smuggling_proof.json`
- `<artifact-output-dir>/three_latest_npm_vulns_20260528T110251Z/evidence/posture.txt`

## Verified proof pattern

The vulnerable parser accepted a duplicate `Content-Disposition` filename parameter and resolved the dangerous attacker-controlled filename `shell.php`. The patched parser rejected duplicate parameters. This gives a local proof of an upload-filter-bypass primitive where parser disagreement can turn a safe-looking filename into a dangerous one downstream.

## Stop-before rules

- Do not test against live upload endpoints without exact scope/rules and explicit operator approval.
- Do not upload web shells, scripts, malware, or active payloads.
- Do not contact third-party systems or customer data.
- Do not promote to report-ready without an authorized app data-flow showing duplicate-parameter parser disagreement affects a real in-scope upload control.
