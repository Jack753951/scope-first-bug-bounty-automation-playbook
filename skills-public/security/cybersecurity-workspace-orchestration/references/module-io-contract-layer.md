> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Offline Module I/O Contract Layer

Use this reference when a cybersecurity platform has already introduced validated module manifests, a dry-run runner, safe fixtures, discovery/profile selection, and data-driven module profiles, and the next phase is to define how future modules will receive invocation data and return results.

## Goal

Add a small, versioned, offline-only contract layer for future module execution without turning the runner into an executor. The contract should make future module boundaries explicit while preserving the current dry-run/non-target-touching safety posture.

## Recommended Contract Shape

- `modules/_schema/module_input.schema.json`
  - versioned envelope such as `schema_version: module_input/1.0`
  - stable identifiers: `run_id`, `module_id`, target, target type, mode/profile references
  - policy/provenance binding to the already-validated allow artifact and scope/profile hashes
  - runner-provided execution context only; no secrets, credentials, callback URLs, or arbitrary environment dumps
- `modules/_schema/module_result.schema.json`
  - versioned envelope such as `schema_version: module_result/1.0`
  - constrained statuses; while still offline-only, use preview statuses such as `not_executed`
  - `dry_run: true`, `target_touching: false`, and empty `findings` / `evidence` for previews
  - future candidate findings/evidence must remain triage-only and link back to run/module IDs
- A strict stdlib validator such as `scripts/validate_module_io_contract.py`
  - JSON Schema-style structural checks plus semantic checks JSON Schema cannot express
  - fail closed on unknown versions, identity mismatches, unsafe status/dry-run/target-touching combinations, unexpected findings/evidence in preview mode, duplicate IDs, path traversal, or untrusted paths
- Runner integration as a preview-only flag, for example `--include-module-io-preview`
  - emit `module_input_previews` and `module_result_previews` only after manifest/profile/policy/run-plan gates have all passed
  - never import module code, spawn module subprocesses, open network clients, generate real findings/evidence, or touch targets

## Sequencing

1. Run an independent strategy/direction review before implementation if there is any ambiguity between a new I/O contract, capability registry, or runner-execution layer.
2. Prefer the smallest contract that removes future ambiguity. Do not duplicate manifest/profile capability fields unless the runner truly needs runtime invocation data.
3. Write failing tests first for schema acceptance/rejection and runner preview output.
4. Implement schemas and semantic validation with the Python standard library where feasible.
5. Wire the runner behind an explicit preview flag only after existing gates pass.
6. Run focused tests, full script tests, project review/preflight, diff whitespace checks, and independent implementation/safety review.
7. Record safety boundaries in handoff/PR text and create the next phase issue instead of silently continuing into execution.

## Review Checklist

- Direction review considered whether the phase should be I/O contract, capability registry, or executor work.
- Preview output appears only after policy allow, manifest validation, profile gate, and run-plan validation.
- Result previews cannot imply confirmed findings or executed checks.
- Input envelopes do not expose secrets, raw environment values, credentials, tokens, cookies, or callback endpoints.
- Path fields are canonicalized and reject `..`, raw `/./`, raw `//`, absolute escapes, symlink escapes when applicable, and backslash variants on Windows-sensitive paths.
- Runner source contains no hidden execution primitives: subprocess/process launch, dynamic imports of module code, `eval`/`exec`, sockets/HTTP clients, callback/OAST logic, scanner invocation, or target-touching helpers.
- Tests include both happy-path previews and unsafe fixtures for mismatched IDs, unsupported schema versions, unsafe status/dry-run/target-touching combinations, unexpected findings/evidence, and path-canonicalization bypasses.

## Pitfalls

- Do not add a broad capability registry before the invocation/result boundary is clear; it often overlaps with manifests and profiles.
- Do not treat a result schema as permission to produce findings. Until execution gates exist, result objects should be previews only.
- Do not emit previews before all existing authorization and profile gates pass.
- Do not let a convenience flag become implicit execution. Preview flags must remain inert and visibly dry-run-only.
