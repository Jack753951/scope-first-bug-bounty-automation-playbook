> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Claude/Cowork Independent Review — Phase 1 P1-4 Task B

Generated: 2026-05-15

## Verdict

ACCEPT

## Scope Reviewed

- `recon.sh` P1-4 Task A program CLI validation follow-up
- `scripts/program_policy_boundary.py`
- `scripts/test_program_policy_boundary.py`
- `scripts/test_recon_program_cli.py`
- Staged handoff updates

## Blocking Issues

None found.

## Safety / Security Observations

- `recon.sh` program CLI validation remains fail-closed for malformed slugs, missing policy mode, invalid policy mode, missing/unreadable scope file, resolved-path escape, and `--program` plus `--skip-scope-check` incompatibility.
- Existing global `safe_target` remains the active runtime gate; `--program` does not bypass it.
- `--policy-mode dry-run` requires recon `--dry-run`.
- `scripts/program_policy_boundary.py` uses `subprocess.run([...], shell=False)`, timeout, captured output, strict JSON parsing, versioned contract validation, verdict/exit-code contradiction checks, and fail-closed behavior.
- Boundary artifacts are written atomically with temp file plus `os.replace`.
- Helper timeout, invalid JSON, and contradiction cases are covered by tests.

## Hermes Follow-Up Applied

After this review, Hermes applied one non-blocking hardening recommendation:

- `recon.sh` now requires the resolved program scope path to be exactly `programs/<slug>/scope.json`, preventing same-tree symlink aliasing to another program's scope file.
- Added `test_program_scope_symlink_to_other_program_is_rejected` to cover that behavior when symlink creation is available.

## Non-Blocking Carry-Forward

- Deduplicate schema/version/enums between boundary and policy core in a future cleanup.
- Consider tests for helper-start failure and artifact-write failure.
- Consider bounding `--timeout-seconds` with a sane maximum.
- Consider restrictive permissions for future policy artifacts if they include sensitive program metadata.
- Document current fail-closed handling if the helper returns missing/unreadable-file denials with null hashes.

## Validation Suggestions

Keep running:

- `bash -n recon.sh`
- `python -m py_compile scripts/program_policy_boundary.py scripts/test_program_policy_boundary.py`
- `python -m unittest scripts/test_program_policy_boundary.py`
- `python -m unittest scripts/test_recon_program_cli.py`
- `python -m unittest scripts/test_program_policy_check.py`
- `./bin/hermes review`
