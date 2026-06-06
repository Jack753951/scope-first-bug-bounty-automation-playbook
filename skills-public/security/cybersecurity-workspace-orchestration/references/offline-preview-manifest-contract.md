> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Offline Preview Manifest Contract

Use this reference when adding a versioned manifest/validator for already-persisted dry-run preview bundles in a cybersecurity lab or bug bounty automation platform.

## When to use

After an offline preview bundle persistence layer exists and writes fixed JSON artifacts under `runs/<run_id>/preview/`, add a separate contract phase before any ledger, archive, agent-triage consumer, or executor work depends on those artifacts.

This is a contract/platform-boundary change. Treat it as T3: direction review with OSS Recon Gate, implementation by Codex or equivalent, Hermes/local validation, and independent implementation/safety review.

## Contract shape

Prefer a closed, strict-version manifest such as `preview_manifest/1.0` that:

- uses `additionalProperties: false` for every object;
- requires an exact `schema_version` match; no silent additive drift in 1.0;
- binds only a fixed allowlist of expected dry-run preview artifacts, for example:
  - `run.json`
  - `module_inputs.json`
  - `module_results.json`
  - `bundle_consistency.json`
- explicitly excludes `preview_manifest.json` from the artifact list;
- records safe POSIX relative paths, lowercase SHA-256, byte size, and content type for each artifact;
- records producer metadata and preview-mode booleans only as data, not as authorization to execute anything;
- binds bundle consistency status/verdict and hash so downstream consumers can fail closed on drift.

## Validator requirements

Keep the validator standalone, standard-library-only, and read-only. It should accept a `runs/<run_id>/preview` directory and emit one machine-readable validation JSON object. Nonzero exit on deny.

Reject at minimum:

- malformed JSON, duplicate JSON keys, trailing data, and non-UTF-8 manifest bodies;
- unknown top-level or nested fields;
- bad schema versions;
- unsafe `run_id` values;
- absolute paths, drive prefixes, backslashes, `..`, raw `./`, duplicate slashes, and artifact paths not matching the expected `runs/<run_id>/preview/<artifact>` tuple;
- symlinks anywhere in the manifest/preview/artifact path chain;
- missing, extra, duplicate, or self-listed artifacts;
- SHA-256 mismatch or size drift;
- `bundle_consistency.json` that is not allow/ok or whose hash differs from the manifest binding;
- invalid/future/ordering-broken timestamps when cross-checking `run.json`.

The validator must not write, repair, move, delete, import module code, spawn subprocesses, open network clients, invoke scanners, touch targets, emit findings/evidence/reports, or add generic output hooks.

## Tests to include

Use TDD/focused tests for:

- valid persisted preview bundle passes;
- missing required fields and unknown fields deny;
- bad `schema_version` denies;
- unsafe run IDs and relative paths deny;
- missing/extra/duplicate/self-listed artifacts deny;
- hash and size mismatch deny;
- malformed JSON, duplicate keys, trailing data, and non-UTF-8 bodies deny;
- non-UTC/non-RFC3339 timestamp plus future/order violations deny;
- non-allow/non-ok bundle consistency denies;
- symlinked artifact, preview directory, or run directory denies where OS privileges allow;
- CLI JSON success/failure shape and nonzero failure exit;
- read-only behavior: file bytes and mtimes unchanged after validation;
- static import guard: no `socket`, `urllib`, `http`, `subprocess`, or equivalent network/process launch modules.

## Review and documentation notes

Compare relevant open formats conceptually, but adapt rather than copy unsafe runtime defaults. Useful references: SARIF run metadata, DefectDojo import metadata, CycloneDX/OSV metadata, and Nuclei result/template metadata.

Document compatibility near the schema: consumers accept only the exact current version; additive optional fields or semantic changes require a separately reviewed future schema version.

Independent review should check both code and contract semantics: closed schema, validator/schema parity, fail-closed errors, no hidden executor/network surface, no generic file index behavior, and no premature transition from dry-run preview artifacts to findings/evidence/reports.
