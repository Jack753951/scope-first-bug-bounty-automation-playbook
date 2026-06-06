> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Verified Lab Flow — @hapi/content <specific-cve-id> parameter smuggling

Status: `verified_hapi_content_cve_2026_44974_parameter_smuggling_local_lab`
Last verified: 2026-05-28
Source advisory: `<specific-ghsa-id>`
CVE: `<specific-cve-id>`
Package under test: `@hapi/content@6.0.1` (`< 6.0.2` vulnerable; `6.0.2` patched control)
OWASP mapping: A01 Broken Access Control / upload validation bypass; A06 Vulnerable and Outdated Components
Target lane: `local-learning-lab`

## When to use

Use this bundle when a target uses Hapi upload/content parsing or equivalent duplicated-parameter parser chains and the attacker can influence `Content-Disposition` or `Content-Type` parameters.

## Latest verified artifacts

```text
<artifact-output-dir>/three_latest_npm_vulns_20260528T110251Z/evidence/
```

Key evidence:

- `hapi_content_smuggling_proof.json`
- `summary.json`
- `posture.txt`

Latest values:

```text
status: verified
vulnerable duplicate filename selected: shell.php
patched duplicate parameter handling: rejected
```

## Success criteria

- Vulnerable control accepts duplicate parameter input and resolves a dangerous attacker-controlled value.
- Patched control rejects the duplicate parameter input.
- No live upload, web shell, malware, customer data, or third-party system is touched.

## Live-target prerequisite mapping

This is not live authorization. For bounty use, require exact scope, program rules permitting upload/parser proof, a demonstrated in-scope parser mismatch, owned harmless files only, no executable payloads, and manual redaction/review before report-ready promotion.
