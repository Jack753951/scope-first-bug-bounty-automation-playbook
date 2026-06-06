> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Offline Module I/O Bundle Diagnostics Hardening

Use this reference when a cybersecurity workspace already has offline `run/1.0`, `module_input/1.0`, and `module_result/1.0` preview bundle validation and the next task is to harden diagnostic quality without enabling execution.

## Durable pattern

- Preserve legacy human-readable fields (`errors`, `warnings`) and stable code arrays (`error_codes`, `warning_codes`) for compatibility.
- Add an additive structured details array such as `error_details`; do not replace existing fields in the same phase.
- Each detail should include, at minimum:
  - `code`
  - `message`
  - `path` to the diverging document/key when applicable
  - `expected`
  - `observed`
  - `module_id` where applicable
- Include `expected` and `observed` keys even when the value is `null`; missing/null observations are diagnostically meaningful.
- Route JSON load failures and all validator errors through one `add_error(...)` helper so every error code has a corresponding detail object.

## Checks worth adding

- Timestamp drift: `run.created_at_utc` must match `module_input.run.created_at_utc`; use a stable code such as `BUNDLE_CREATED_AT_UTC_MISMATCH`.
- Explicit tests for existing bundle codes, not only broad deny behavior:
  - mode mismatch
  - runner mismatch
  - dry-run mismatch
  - unsupported result status
  - target-touching drift
  - constraint drift
  - module ID mismatch
  - duplicate run module IDs
- Missing/extra previews must produce structured paths and module IDs.
- Multi-module module-ID mismatches need coverage. Avoid single-module-only heuristics; if there is exactly one missing planned ID and one extra input/result ID, emit a module-ID mismatch detail with expected/observed values.
- Non-empty findings/evidence in previews should remain deny-by-default and report the exact path (`module_input[...].output.findings`, `module_result[...].evidence`, etc.).

## Review loop

1. Run an OSS Recon Gate / design-only review if the diagnostic shape changes a versioned contract.
2. Implement with TDD: add failing tests for the explicit code and detail shape first.
3. Run focused tests, relevant adjacent tests, full safe offline tests, Python compile, diff check, project review wrapper, and independent implementation/safety review.
4. If independent review finds incomplete structured details, patch immediately before recording completion.

## Safety boundary

This task class is offline helper/test/documentation work only. It must not import module implementations, spawn module/scanner subprocesses, open network clients, touch targets, emit real findings/evidence, write loot/reports, modify scope allowlists, or add persisted execution ledgers unless that is a separate reviewed phase.
