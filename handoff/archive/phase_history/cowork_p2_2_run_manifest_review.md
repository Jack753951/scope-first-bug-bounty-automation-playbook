> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Cowork Review — P2-2 Run Manifest / Execution Ledger

Date: 2026-05-16
Verdict: PASS after one route-back fix cycle

## Scope reviewed

- `modules/_schema/run.schema.json`
- `modules/_schema/README.md`
- `scripts/validate_run_manifest.py`
- `scripts/test_run_manifest_schema.py`
- Existing P2-1 interaction with:
  - `modules/_schema/finding.schema.json`
  - `modules/_schema/evidence.schema.json`
  - `scripts/validate_finding_evidence.py`

## Initial review verdict

Initial independent review returned BLOCKED.

Blocking issues found:

1. `validate_run_bundle()` only cross-checked `findings[0]` with evidence. Later findings could reference missing evidence, mismatched hashes, wrong kind, or wrong `finding_id` and still pass.
2. Duplicate IDs were not rejected. Duplicate `modules[].module_id`, `artifacts.findings[].id`, or `artifacts.evidence[].id` could create ambiguous ledger state because dictionary mapping collapsed later entries.

## Fixes applied

- Added regression coverage:
  - `test_run_bundle_cross_checks_every_finding_not_only_first`
  - `test_run_manifest_rejects_duplicate_module_and_artifact_ids`
- Updated `validate_run_bundle()` so every supplied finding is passed through `validate_finding_evidence.validate_bundle(finding, evidence_items)`.
- Updated `_validate_modules()` to reject duplicate `module_id` values.
- Updated `_validate_artifacts()` to reject duplicate finding/evidence artifact IDs.

## Final re-review verdict

Final independent re-review returned PASS.

Confirmed:

- The previous multi-finding evidence bypass is closed.
- Duplicate module/artifact IDs are denied.
- Run manifest remains offline-only and standard-library only.
- Triage-only semantics are enforced by `scanner_output_only=true` and `manual_verification_required=true`.
- Dry-run runs cannot be marked target-touching.
- No live scans, target interaction, scheduler/report/loot behavior, or `config/scope.txt` changes were introduced.

## Validation evidence

Hermes local validation after fixes:

- PASS: `env -u PYTHONIOENCODING -u PYTHONUTF8 python -m pytest scripts/test_run_manifest_schema.py -q`
  - `10 passed, 14 subtests passed`
- PASS: `python -m py_compile scripts/validate_run_manifest.py scripts/test_run_manifest_schema.py scripts/validate_finding_evidence.py scripts/test_finding_evidence_schema.py`
- PASS: JSON parse for:
  - `modules/_schema/run.schema.json`
  - `modules/_schema/finding.schema.json`
  - `modules/_schema/evidence.schema.json`
- PASS: full relevant pytest suite:
  - `75 passed, 2 skipped, 65 subtests passed`
- PASS: `USER=${USER:-Owner} HACKLAB=<private-workspace> ./bin/hermes review`
- PASS: `git diff --check`

## Non-blocking recommendations

- Consider adding explicit tests for second/later finding evidence sha256/kind/finding_id mismatches, although the per-finding bundle validation now covers these through the existing P2-1 validator.
- Document that duplicate ID uniqueness is enforced by the Python semantic validator; JSON Schema does not enforce uniqueness by object ID.
- In a future phase, decide whether run artifact hashes bind metadata JSON files, redacted payload files, or both before the module runner starts writing real run directories.

## Safety boundary

This phase is schema/validator/test work only. It does not execute modules, scan targets, touch external hosts, alter `config/scope.txt`, commit secrets/loot, publish reports, or change production/scheduler settings.
