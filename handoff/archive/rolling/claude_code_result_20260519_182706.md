> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Claude Code Implementation Result — P3.7 Program-Policy Dry-Run Regression

Status: implemented with Hermes verification/fixup after Claude Code worker reached max turns.

- Worker JSON: `handoff/claude_code_impl_run_20260519_163456.json`
- Worker subtype: `error_max_turns`
- Worker turns/cost: `num_turns=36`, `total_cost_usd=3.2401427500000004`
- Visible model usage: `claude-opus-4-7` and `claude-haiku-4-5-20251001` per JSON metadata
- Named result: `handoff/claude_code_result_p3_7.md`

Implemented files:

- `programs/_examples/sample-lab/scope.json`
- `scripts/test_recon_program_policy_dry_run.py`
- `handoff/cowork_p3_7_direction_review.md`
- `handoff/claude_code_task_p3_7.md`
- `handoff/claude_code_result_p3_7.md`
- `handoff/active_strategy_queue.md`
- `handoff/accepted_changes.md`

Validation completed before this rolling result was written:

- `python -m unittest scripts/test_recon_program_policy_dry_run.py` — PASS, 12 tests.
- `python -m unittest scripts/test_recon_program_cli.py scripts/test_program_policy_check.py scripts/test_program_policy_boundary.py scripts/test_recon_program_policy_dry_run.py` — PASS, 62 tests, 2 skipped.
- `python -m unittest discover scripts` — PASS, 387 tests, 8 skipped.
- `git diff --check` — PASS, line-ending warnings only.
- `HACKLAB=<private-workspace> ./bin/hermes review` — PASS, Python compile OK for 75 files, shell scripts OK, lock clear.

Boundary:

- Tests/fixture/handoff only.
- No `recon.sh`, program policy helper, module runner, schema, module, config, `config/scope.txt`, scope gate, runtime behavior, scanner/module execution, target-touching automation, report drafting/submission, platform adapter, credentials/OAuth, scheduler, deployment, billing, or production setting changes.

Next recommended step:

- Independent implementation/safety review for P3.7, likely `handoff/third_party_p3_7_implementation_review.md`.
