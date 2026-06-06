> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# lab_source_map_disclosure_triage

Status: draft-active bundle / local-learning-lab / candidate-only
Date: 2026-05-21
Adapter: `scripts/lab_modules/lab_source_map_disclosure_triage.py`
Generated runner: `setting/local/lab_source_map_disclosure_triage_run.sh`
Latest artifacts: `<artifact-output-dir>/phase4b_three_exposure_bundles_20260521T143412Z/lab_source_map_disclosure_triage/`

## Use when

Use this bundle when a JavaScript-heavy app may expose `.js.map` source maps, client build artifacts, endpoint hints, dependency clues, or source-level metadata.

## OWASP / CVE mapping

- OWASP A05:2021 Security Misconfiguration
- OWASP A06:2021 Vulnerable and Outdated Components, only when source maps support client dependency/version triage
- 2025 migration track: client artifact / information exposure leads
- CVE: none claimed by default; source maps are usually information exposure/context leads, not a CVE by themselves.

## Mature OSS/tooling recon

Decision: first probe for source-map exposure; reference mature tools for later offline/redacted review.

- Retire.js (`RetireJS/retire.js`, Apache-2.0): client-side dependency/CVE hint review after asset inventory.
- SecretFinder (`m4ll0k/SecretFinder`, GPL-3.0): reference-only unless redaction/loot hygiene is explicit.
- trufflehog (`trufflesecurity/trufflehog`, AGPL-3.0): offline redacted secret-pattern review only, not raw loot retention.
- LinkFinder (`GerbenJavado/LinkFinder`, license to verify before vendoring): reference-only endpoint extraction from JS assets.

## What it runs

- Fetch `/` and extract linked `.js` assets.
- Probe inferred `.js.map` paths.
- Probe common source-map paths:

```text
/main.js.map
/runtime.js.map
/vendor.js.map
/polyfills.js.map
```

The runner records status, content type, SHA-256, and candidate/control observations. It does not commit raw JS/source-map bodies.

## Inputs

```bash
MSYS2_ARG_CONV_EXCL='*' python scripts/lab_modules/lab_source_map_disclosure_triage.py \
  --target http://<lab-ip>:3000/ \
  --lab-approved \
  --out-script setting/local/lab_source_map_disclosure_triage_run.sh \
  --output-dir /tmp/lab_source_map_disclosure_triage
bash setting/local/lab_source_map_disclosure_triage_run.sh
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

- HTTP 200/redirect with source-map-like keywords such as `sources`, `sourcesContent`, `webpack`, `mappings`, or `file`.
- Body hash differs from `/` root.

Controls:

- 404/401/403/timeout.
- HTTP 200 with same body hash as `/` root.
- Non-JSON or non-source-map content.

## Latest local-lab result

No source-map candidate remained after root-fallback filtering.

Several inferred `.js.map` paths returned HTTP 200, but the body hash matched `/`, so they were classified as generic SPA/router fallback controls.

## Missing evidence before finding language

- Manually verify any future source map is real JSON source-map content.
- Confirm whether it includes original source, comments, endpoints, dependency versions, or secrets.
- Redact before recording evidence.
- Use Retire.js/trufflehog/SecretFinder only in offline redacted mode unless separately approved.
