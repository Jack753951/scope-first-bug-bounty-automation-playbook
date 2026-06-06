> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Claude Code Result — P3.8 Malformed-Scope Exit-Code Semantics

Date: 2026-05-19
Route/tool: Hermes local implementation and verification after Claude/Cowork direction review. The earlier `./bin/hermes cowork` wrapper hit its default max-turn limit, so Hermes captured the direction review from a direct Claude Code CLI pass and saved it to `handoff/cowork_p3_8_direction_review.md`.

## Summary

Implemented the P3.8 exit-code hardening slice.

Changed `recon.sh` so program-policy boundary/config errors are counted and surfaced as process exit code `3` after the normal summary/audit output. Valid policy denies remain successful no-work decisions with exit code `0`.

The implementation preserves dry-run/non-target-touching behavior and does not change program-policy helper contracts, scope files, scanner/module execution, or runtime activation gates.

## Files Changed

- `recon.sh`
- `scripts/test_recon_program_policy_dry_run.py`
- `scripts/test_recon_program_cli.py`
- `handoff/cowork_p3_8_direction_prompt.md`
- `handoff/cowork_task.md`
- `handoff/cowork_p3_8_direction_review.md`
- `handoff/claude_code_task_p3_8.md`
- `handoff/claude_code_result_p3_8.md`
- `handoff/active_strategy_queue.md`
- `handoff/accepted_changes.md`

## Runtime Semantics

- Exit `0`: allow-path dry-run and valid policy denies.
- Exit `3`: policy-boundary/config error class, including malformed program scope surfaced as `VALIDATOR_DENY`.

Implementation detail:

- Added `POLICY_ERROR_COUNT` and `POLICY_BOUNDARY_ERROR_EXIT=3`.
- Added `policy_is_boundary_error` to classify `POLICY_VERDICT=error` and existing validator/boundary-error deny codes such as `VALIDATOR_DENY`, `ARTIFACT_VALIDATION_FAILED`, and `INVALID_POLICY_TIMEOUT` as boundary errors.
- `run_pipeline` returns exit `3` if a policy-boundary error was observed during that pipeline.
- Top-level multi-target status aggregation preserves exit `3` priority over generic exit `1`.

## Tests / Validation

Focused P3.8 / adjacent recon-program regressions:

```text
python -m unittest scripts/test_recon_program_cli.py scripts/test_recon_program_policy_dry_run.py
36 OK, 2 skipped
```

Full validation:

```text
python -m unittest discover -s scripts -p 'test_*.py'
388 OK, 8 skipped

git diff --check
PASS with CRLF warnings only

HACKLAB=<private-workspace> ./bin/hermes review
PASS: Python compile OK, shell scripts bash -n OK, lock clear, 12 scope entries
```

## Safety Boundary

No live scans, no target interaction, no scanner/module execution, no callbacks/OAST, no fuzzing/brute force/exploit attempts, no `config/scope.txt` changes, no program scope fixture changes, no helper contract changes, no module-runner coupling, no report drafting/submission, no credentials/OAuth/billing/deployment/production changes.
