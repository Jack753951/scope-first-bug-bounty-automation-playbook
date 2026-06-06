> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Lab service baseline bundle adapter

Use this pattern when the operator wants practical service-specific coverage for an authorized local/intentionally vulnerable lab, but the main recon/scope framework is too sensitive to modify directly.

## Class pattern

- Prefer `script/tool -> bundle -> module` for early service coverage.
- Add a bounded adapter under a lab-module/script location first, document it as a bundle, and only later promote stable pieces into module manifests or runner integration.
- Keep the main recon scope/policy path unchanged unless the task explicitly requires a reviewed runtime boundary change.
- Treat outputs as `candidate-only` / `needs_manual_review`; never promote service banners, public endpoints, or scanner hints into confirmed findings.

## Safe default shape

For service-baseline adapters covering Apache, Tomcat, TLS/OpenSSL, HAProxy, Envoy, Traefik, or similar infrastructure services:

- Default to plan-only output.
- Require an explicit lab/authorization flag before writing or running a runnable script.
- Fail closed on public-looking targets unless the repo's normal scope/program gate explicitly allows them.
- Use fixed low-risk probe paths and metadata commands; avoid recursive crawling, brute force, credential attempts, config dumping beyond metadata, file downloads, or secret capture.
- Include request caps/timeouts, pre/post health where execution is added, and redacted local artifacts.
- Label every observation as candidate/triage-only and add manual verification notes.

## Recommended artifacts

A generated runner or adapter should produce predictable local artifacts such as:

- `observations.jsonl`
- `possible_vulnerabilities.md`
- `summary.txt`
- `health.txt`
- `http_probe_results.tsv`
- tool stdout/stderr/raw output files where applicable
- `artifact_manifest.txt`

## Validation checklist

- TDD first: test plan-only behavior, explicit lab-approval requirement, public target denial, service coverage, and candidate-only wording.
- Compile touched Python files.
- `bash -n` any generated shell runner.
- Run focused tests plus adjacent wrapper/module tests.
- Run the project review wrapper when available.
- Update `SCRIPT_INVENTORY.md`, bundle documentation, and `handoff/accepted_changes.md`.
- If the generated runner lives under git-ignored local runtime directories such as `setting/local/`, state that it exists but is intentionally not tracked.

## Pitfalls

- Do not wire a new service scanner directly into `recon.sh` just to make it visible; that crosses the scope/policy runtime boundary and may require heavier review.
- Do not treat Tomcat manager, Envoy admin, Traefik API, HAProxy stats, `/server-status`, or TLS metadata as vulnerabilities by themselves. They are triage signals until manually verified for exposure, access control, sensitive content, and impact.
- Do not brute-force Tomcat manager or fetch/dump full admin/config bodies as a baseline step.
- Do not let service-specific convenience bypass the user's script-first direction: produce a practical reusable bundle now, then modularize only what proves useful.