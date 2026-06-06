> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Claude/Cowork Independent Review — Phase 1 P1-5 Policy Artifact Validation

Generated: 2026-05-16 12:46:49

## Verdict

ACCEPT / PASS after one blocking timeout-hardening fix.

## Scope Reviewed

- `recon.sh` program policy artifact validation before accepting `allow`.
- `recon.sh` `PROGRAM_POLICY_TIMEOUT_SECS` validation and canonicalization.
- `scripts/test_recon_program_cli.py` regressions for forged artifacts and timeout edge cases.

## Blocking Issues Found And Resolved During Review

1. Timeout arithmetic parsing bypass
   - Finding: initial timeout validation used Bash arithmetic after a permissive `[0-9]+` regex. Leading-zero values such as `099` and huge integers could trigger octal/overflow behavior while the raw value was forwarded to the Python boundary.
   - Resolution: `normalize_policy_timeout()` now only accepts `^[1-9][0-9]?$`, rejects leading-zero and huge numeric strings before arithmetic, checks `10#$raw > 60`, and emits canonical decimal.
   - Regression: timeout subtests now cover `0`, `61`, `099`, `000`, `18446744073709551617`, and `not-int`.

## Safety / Security Observations

- Artifact path validation uses `Path(...).resolve(strict=True)` for both artifact and artifact directory, then requires `os.path.commonpath([artifact, artifact_dir]) == artifact_dir`.
- This blocks outside-directory artifacts, traversal, symlink escape, and different drive/tree allow-forgery attempts.
- Allow artifacts must have:
  - `schema_version == policy_boundary/1.0`
  - `boundary.status == allow`
  - `request.target/stage/technique/mode` matching the current `policy_decide()` request
- Validation failure becomes `PROGRAM_POLICY_BOUNDARY_ERROR` with `ARTIFACT_VALIDATION_FAILED` and fails closed before stage consumption.
- No new target-touching behavior was added; tests confirm forged artifacts are denied before `httpx` dry-run command construction.

## Validation Evidence

- PASS: `bash -n recon.sh bin/hermes`
- PASS: Python compile checks for policy/test files
- PASS: `env -u PYTHONIOENCODING -u PYTHONUTF8 python -m pytest scripts/test_program_policy_boundary.py scripts/test_recon_program_cli.py scripts/test_program_policy_check.py -q`
  - Result after timeout fix: `43 passed, 2 skipped, 21 subtests passed`
- PASS: `HACKLAB="$PWD" ./bin/hermes review`
  - Python Compile OK
  - Shell scripts bash-n OK
  - Lock clear
- PASS: `git diff --check`
- PASS: static added-line scans found no hardcoded secrets, shell=True/os.system, or eval/exec patterns.
- PASS: independent re-review found no remaining blocking defect.

## Non-Blocking Recommendations

- Future evidence-integrity hardening can also compare embedded `decision` fields, `boundary.audit_event`, program/global scope paths, and provenance hashes.
- Consider capping/sanitizing validation error message length if future validation includes artifact-derived strings.
- Longer term, canonicalize the Python interpreter path if the threat model expands to hostile local PATH manipulation.

## Final Reviewer Verdict

PASS. The previous timeout parsing blocker has been resolved. Artifact path/request validation is sufficient for the P1-5 safety goal, and no target-touching safety defect remains in the reviewed diff.
