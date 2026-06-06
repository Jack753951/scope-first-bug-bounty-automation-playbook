> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Claude Code Task — P3.8 Malformed-Scope Exit-Code Semantics

Date: 2026-05-19
Route: Hermes local implementation after Claude/Cowork direction review
Review tier: T4 process-wise / hardening-only

## Source Direction

Read:

- `.hermes.md`
- `handoff/cowork_p3_8_direction_prompt.md`
- `handoff/cowork_p3_8_direction_review.md`

Direction verdict: `APPROVE_WITH_CHANGES`.

## Objective

Harden `recon.sh` exit-code semantics so malformed or boundary-error program-policy outcomes no longer look like successful no-work dry runs.

Approved behavior:

- valid allow dry-run remains exit `0`;
- valid policy deny, such as out-of-program-scope, remains exit `0`;
- malformed/validator/boundary-error policy outcomes exit `3`;
- no scanner/module/target-touching behavior is introduced.

## Allowed Files

- `recon.sh`
- `scripts/test_recon_program_policy_dry_run.py`
- handoff files for task/result/queue/accepted-changes

## Forbidden Surfaces

Do not edit:

- `scripts/program_policy_boundary.py`
- `scripts/program_policy_check.py`
- `scripts/module_runner.py`
- `scripts/core/**`
- `modules/**`
- `config/scope.txt`
- `config/recon.conf`
- `programs/_examples/sample-lab/scope.json`
- scanner/module/runtime activation surfaces
- scheduler, CI, OAuth, credentials, billing, deployment, production settings

Do not run live scans, target-touching automation, scanners, modules, callbacks/OAST, fuzzing, brute force, exploit attempts, or report submission.

## Required Tests

- `python -m unittest scripts/test_recon_program_policy_dry_run.py`
- `python -m unittest scripts/test_recon_program_cli.py`
- `python -m unittest discover -s scripts -p 'test_*.py'`
- `git diff --check`
- `HACKLAB=<private-workspace> ./bin/hermes review`

## Implementation Notes

- Reserve exit code `3` as policy-boundary/config error.
- Count boundary-error policy outcomes without changing ordinary policy-deny semantics.
- Include `VALIDATOR_DENY` in boundary-error handling because the existing boundary wrapper surfaces malformed program scope as a deny with a validator-deny code rather than as `status=error`.
