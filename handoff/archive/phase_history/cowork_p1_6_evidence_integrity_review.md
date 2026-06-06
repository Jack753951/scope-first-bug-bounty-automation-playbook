> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Cowork Review — P1-6 Evidence Integrity Hardening

Date: 2026-05-16
Scope: `recon.sh` program policy allow-artifact validation and regression tests.

## Verdict

PASS. No blocking defects found after the second review/fix cycle.

## Review notes

### First independent review

The first independent review found one important gap: the proposed validation compared artifact `decision.*` hashes against the flat `POLICY_BOUNDARY_*` output, but did not prove those flat hashes matched the actual program scope and global scope files currently being used by `recon.sh`.

### Fix applied

`policy_validate_artifact()` now receives the current `PROGRAM_SCOPE_FILE` and `SCOPE_FILE`, resolves them in isolated Python, computes SHA-256 for both files, and requires:

- `POLICY_BOUNDARY_PROGRAM_HASH == sha256(PROGRAM_SCOPE_FILE)`
- `POLICY_BOUNDARY_GLOBAL_HASH == sha256(SCOPE_FILE)`
- artifact `decision.program_file_sha256` matches the flat boundary output
- artifact `decision.global_scope_sha256` matches the flat boundary output

The test fake boundary was also tightened so negative tests use actual source hashes except where the tested condition intentionally mutates a value.

## Blocking defects

None after fix.

## Non-blocking suggestions

- Consider parsing `decided_at_utc` semantically with `datetime.strptime` in a later cleanup instead of regex-only syntax validation.
- If evidence validation continues growing, move the inline Python validator from `recon.sh` into a small reusable Python module under `scripts/core/`.
- If future local-tamper threat modeling is needed, document that validation binds evidence to source files as they exist at validation time immediately after the boundary run.

## Architecture / roadmap fit

Good fit:

- Global `safe_target` remains the first authorization gate.
- Program policy remains a second fail-closed gate.
- Evidence validation is stricter without adding live scan behavior.
- The change supports the long-term goal of a structured bug bounty platform with auditable, agent-reviewable evidence and policy decisions.

## Test adequacy

Adequate for merge:

- Forged allow artifact with missing `decision` is denied.
- Forged allow artifact with mismatched `decision.target` is denied.
- Forged allow artifact with mismatched `boundary.audit_event` is denied.
- Forged allow artifact with source-hash mismatch is denied.
- Valid program dry-run path still passes.
- All denial cases assert scanner/probe dry-run command is not consumed.

## Validation observed

- `bash -n recon.sh bin/hermes` passed.
- Python compile checks passed.
- Target pytest suite passed: `47 passed, 2 skipped, 21 subtests passed`.
- `HACKLAB="$PWD" ./bin/hermes review` passed.
- `git diff --check` passed.
- Static added-line scans found no hardcoded secrets, shell execution anti-patterns, `eval`/`exec`, or pickle patterns.

## Safety boundary

No live scans were run. `config/scope.txt` was not modified. Changes are local policy/evidence hardening only.
