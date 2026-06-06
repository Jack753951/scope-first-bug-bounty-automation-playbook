> Public filtered Obsidian memory export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Phase 4B Three Exposure Bundles 2026-05-21

Status: completed local-learning-lab run / candidate-only
Repo truth: <user-home>
Artifacts: <user-home>

## Decision

Added three lightweight bundle-first OWASP exposure triage workflows rather than formal `module.json` capabilities:

1. `lab_api_docs_exposure_triage`
2. `lab_metrics_exposure_triage`
3. `lab_source_map_disclosure_triage`

They follow the accepted path:

```text
script/tool -> bundle -> module
```

## Mature OSS/tooling references

Recorded mature tools to adopt/wrap/reference later:

- OWASP ZAP
- nuclei
- ffuf
- dirsearch
- Prometheus/promtool
- Retire.js
- SecretFinder
- trufflehog
- LinkFinder

Decision: start with fixed GET-only lab probes and mature-tool references; do not vendor or run broad templates yet.

## Local-lab results

Target: `http://<lab-ip>:3000/`

Candidate-only leads:

- `/api-docs` and `/api-docs/` exposed Swagger UI markers.
- `/metrics` exposed Prometheus-style metrics markers.

No source-map disclosure candidate remained after root-body fallback filtering.

Controls:

- Many 200 responses were correctly downgraded to generic SPA/router fallback controls using body-hash comparison.

## Safety boundary

- Candidate-only / needs manual review.
- No credential attempts, brute force, callbacks, exploit PoCs, raw secret retention, report submission, or confirmed-finding promotion.
- Raw response bodies are not committed.

## Next useful action

Manual review/redacted evidence for:

1. `/api-docs`
2. `/metrics`

Only after manual verification should either become a report candidate.
