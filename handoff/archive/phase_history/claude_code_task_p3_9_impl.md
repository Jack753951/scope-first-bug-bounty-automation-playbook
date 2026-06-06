> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Claude Code Implementation Task — P3.9 Offline Dry-Run Recon-to-Runner Bridge

Status: READY_FOR_CLAUDE_IMPL
Date: 2026-05-19
Prepared by: Hermes
Route: Claude Code MAX/OAuth via `hermes claude-impl`
Source direction review: `handoff/cowork_p3_9_direction_review.md`
Expected named result: `handoff/claude_code_result_p3_9.md`
Expected rolling result: `handoff/claude_code_result.md`

## Goal

Implement the P3.9 slice approved by `handoff/cowork_p3_9_direction_review.md`:

- Demonstrate offline interoperability between recon's existing program-policy allow artifact and the existing dry-run-only `scripts/module_runner.py` preview path.
- Keep bridge path translation inside the test harness only.
- Do not modify runtime code.
- Do not touch targets, scanners, modules, scope/config, schemas, reports, scheduler, credentials, deployment, billing, or production settings.

## Binding decision summary

Decision: `APPROVE_WITH_CHANGES`.
Implementation tier: T2 tests/fixtures/docs only, inheriting P3.9 T3 OSS Recon Gate.
Hermes authority: conditional.
Operator approval required: no, because this is offline/local dry-run tests/docs only.

## Strict TDD requirement

Follow RED-GREEN-REFACTOR:

1. First add a focused failing test in `scripts/test_recon_runner_bridge_dry_run.py`.
2. Run that focused test and record the expected RED failure in `handoff/claude_code_result_p3_9.md`.
3. Then implement only the test harness/helpers needed to make it pass. Do not edit runtime code.
4. Run focused tests until GREEN.
5. Run relevant adjacent suites and Hermes review.

Because this slice is expected to need no production-code changes, the RED failure may be the initial absence/incomplete behavior of the new test file or missing harness helper. The important invariant: do not change runtime code to satisfy the test.

## Allowed files only

You may touch only:

1. `scripts/test_recon_runner_bridge_dry_run.py` — new unittest file, maximum ~600 lines.
2. `scripts/README.md` — append a concise P3.9 bridge note only if needed; prefer this over a new docs file.
3. `handoff/claude_code_result_p3_9.md` — named implementation result.
4. `handoff/claude_code_result.md` — rolling result.
5. `handoff/accepted_changes.md` — append/prepend concise accepted entry.
6. `handoff/active_strategy_queue.md` — update current lane after implementation.
7. Normal wrapper artifacts under `handoff/claude_code_impl_run_*.json` and `handoff/archive/rolling/*`.

Do not exceed this file list. If you think another file is needed, stop and write a blocker in the result file instead.

## Files that must remain byte-identical

Do not modify:

- `recon.sh`
- `scripts/program_policy_boundary.py`
- `scripts/program_policy_check.py`
- `scripts/core/policy.py`
- `scripts/module_runner.py`
- `scripts/validate_module_io_bundle.py`
- `scripts/validate_module_io_contract.py`
- `scripts/validate_preview_manifest.py`
- `scripts/validate_preview_ledger.py`
- `scripts/validate_run_manifest.py`
- `scripts/profile_issues.py`
- anything under `modules/checks/**`, `modules/profiles/**`, `modules/_schema/**`
- `config/scope.txt`, `config/recon.conf`
- `programs/_examples/sample-lab/scope.json`
- `programs/_examples/README.md`
- `bin/hermes`, `run_hermes_worker.ps1`
- `reports/**`, `loot/**`, `scans/**`, `evidence/**`, real repo `runs/**`

## Required test shape

Create `scripts/test_recon_runner_bridge_dry_run.py` using `unittest` and patterns from `scripts/test_recon_program_policy_dry_run.py` and `scripts/test_module_runner.py`.

The test file should:

- Use `tempfile.TemporaryDirectory` for a per-test HACKLAB.
- Install synthetic program scope into temp `HACKLAB/programs/sample-lab/scope.json` by copying/reusing committed `_examples/sample-lab` data.
- Install/copy committed module profile and level1 module manifests into temp HACKLAB so runner discovery uses only temp files.
- Invoke `recon.sh --dry-run --program sample-lab --policy-mode planned <synthetic in-scope target>` against the temp HACKLAB.
- Locate one emitted `policy_boundary_*.json` allow artifact.
- Copy that artifact to temp `HACKLAB/runs/<run_id>/policy/decision.json` inside the test harness only.
- Invoke `scripts/module_runner.py --policy-artifact <copied-path> --run-id <id> --target <same-target> --target-type <type> --mode dry-run --discover-root <HACKLAB> --json`.
- Assert allow/planned/dry-run/no-target-touching/no-module-execution semantics.

Use a synthetic target already covered by the sample-lab fixture. If exact target/mode mismatch appears because recon emits `planned` while runner supports `dry-run`, do not edit runtime code. Instead, either select an existing recon invocation mode that emits a runner-compatible dry-run decision if available, or document a blocker/defer if the contracts are not actually compatible without runtime change.

## Required assertions

Cover as many of the P3.9 direction review §6 items as possible without runtime edits, especially:

- positive bridge allow path;
- optional module I/O preview no-execution path if easy;
- policy artifact hash/path consistency;
- target mismatch deny;
- path outside `runs/<run_id>/policy/` deny;
- helper failure deny;
- audit event mismatch deny;
- no scanner execution leakage markers;
- no module execution leakage markers;
- real `config/scope.txt` sha256 unchanged;
- real repo `runs/`, `loot/`, `scans/`, `evidence/`, `reports/` unchanged;
- reserved `_examples` remains installed only into temp HACKLAB, not used as a real slug;
- no new bridge CLI flag in `recon.sh --help` or runner `--help`.

If a specific recommended assertion cannot be implemented cleanly, document it as deferred in the result file rather than changing runtime code.

## Required validation commands

Run and record results:

- RED focused test command and expected failure.
- `python -m unittest scripts.test_recon_runner_bridge_dry_run`
- `python -m unittest scripts.test_recon_program_policy_dry_run scripts.test_module_runner`
- `python -m unittest discover scripts` if feasible within time; if not, run the adjacent suites and explain why.
- `git diff --check`
- `USER=${USER:-Owner} HACKLAB=<private-workspace> ./bin/hermes review`

Also run a staged/working-tree added-line secret and target-touching vocabulary scan before reporting done.

## Safety statements to include in result

`handoff/claude_code_result_p3_9.md` must include:

```text
Decision implemented:
Changed files:
RED evidence:
GREEN validation:
Safety boundary confirmation:
Forbidden files untouched:
Deferred assertions/blockers:
Reviewer route/tool and visible model/runtime:
Next recommended review:
```

Do not commit or push. Hermes will verify, commit, push, and update PR after local review.
