> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Claude Code / Hermes Result — P3.9 Offline Dry-Run Recon-to-Runner Bridge

Decision implemented: `APPROVE_WITH_CHANGES` from `handoff/cowork_p3_9_direction_review.md` as a T2 tests-only implementation slice.

Changed files:

- `scripts/test_recon_runner_bridge_dry_run.py` — new offline unittest bridge harness, 593 lines after Hermes cleanup to satisfy the direction review cap.
- `handoff/claude_code_task.md` — rolling pointer updated to the P3.9 implementation task.
- `handoff/claude_code_task_p3_9_impl.md` — named implementation task.
- `handoff/cowork_p3_9_direction_review.md` — T3 direction review from Claude Code route.
- `handoff/claude_code_result_p3_9.md` / `handoff/claude_code_result.md` — implementation result summary.
- wrapper artifacts: `handoff/claude_code_impl_run_20260519_182706.json`, `handoff/claude_code_impl_run_20260519_183403.json.tmp`, and rolling result archives.

RED evidence:

- Claude Code implementation worker for P3.9 timed out at the parent Hermes tool timeout after creating the test file, so a clean captured RED transcript was not preserved in the wrapper result.
- Hermes did not accept the worker self-report blindly. Hermes inspected the partial workspace, compacted the test file without changing behavior, then ran focused and broad validation locally.
- Process caveat: RED evidence is incomplete for this slice. Risk is limited because no production/runtime code was changed; the new artifact is tests-only and all safety assertions pass.

GREEN validation:

- `python -m unittest scripts.test_recon_runner_bridge_dry_run` — 10 tests OK in 33.845s after Hermes cleanup.
- `python -m unittest scripts.test_recon_program_policy_dry_run scripts.test_module_runner` — 53 tests OK, skipped=1.
- `python -m unittest discover scripts` — 399 tests OK, skipped=8.
- `git diff --check` — OK.
- `USER=${USER:-Owner} HACKLAB=<private-workspace> ./bin/hermes review` — PASS; Python compile OK for 76 files, shell scripts OK, lock clear.
- added-line secret/target-touching scan — OK; one expected safety-text match for `OAuth` in handoff route text only.

Safety boundary confirmation:

- No live targets, scans, probes, scanner execution, module execution, fuzzing, brute force, callbacks, OAST, proxy/pivot/tunnel, or target-touching automation.
- `recon.sh` is invoked only with `--dry-run` against a temporary HACKLAB using the synthetic `sample-lab` program fixture.
- `module_runner.py` is invoked only with `--mode dry-run` and only as the existing preview planner.
- Bridge path translation happens only inside the test harness: recon-emitted `policy_boundary_*.json` is copied into temp `runs/<run_id>/policy/decision.json` before invoking the runner.
- Real `config/scope.txt` is sha256 fenced.
- Real repo `runs/`, `loot/`, `scans/`, `evidence/`, and `reports/` are snapshot fenced.
- No findings/evidence/report/submission promotion occurs.

Forbidden files untouched:

- `recon.sh`
- `scripts/module_runner.py`
- `scripts/program_policy_boundary.py`
- `scripts/program_policy_check.py`
- policy/core validators
- modules/profiles/checks/schema files
- `config/scope.txt`, `config/recon.conf`
- runtime/report/loot/evidence/scans surfaces

Implemented assertions:

- positive recon artifact -> runner allow verdict bridge;
- policy hash/path consistency;
- optional module I/O preview remains dry-run and emits no findings/evidence;
- target mismatch denied;
- artifact path outside `runs/<run_id>/policy/` denied;
- helper returncode mismatch denied;
- audit event mismatch denied;
- planned-vs-dry-run mode mismatch denied;
- no bridge-specific CLI flag in `recon.sh --help` or `module_runner.py --help`;
- no scanner/module execution leakage markers;
- real repo scope and output directories unchanged.

Deferred assertions/blockers:

- Standalone stale-artifact / target / mode / technique mismatch E2E harness remains deferred as recommended by P3.9.
- Runtime bridge, auto-copy wrapper, CLI bridge flags, artifact layout changes, module execution, finding/evidence flow, live lab activation, real-program onboarding, report submission, scheduler, credentials/OAuth, deployment, billing, and production settings remain deferred and require fresh T3/T4 review and operator approval where applicable.
- RED evidence was not cleanly captured because the Claude Code worker exceeded the parent Hermes tool timeout; this should be treated as a process caveat, not a runtime blocker.

Reviewer route/tool and visible model/runtime:

- P3.9 direction review route/tool: Claude Code Impl via `bin/hermes claude-impl`; visible model/runtime: `claude-opus-4-7` as reported in the direction review, underlying Anthropic serving runtime not exposed.
- P3.9 implementation route/tool: Claude Code Impl started via `bin/hermes claude-impl`; parent Hermes terminal timed out before wrapper completion, so final usage JSON is `.tmp` and exact terminal reason is incomplete. Hermes completed verification directly on Windows Git-Bash.

Next recommended review:

- Treat P3.9 implementation as ready for local acceptance after Hermes verification, but because the worker timed out and RED evidence was incomplete, prefer a lightweight independent implementation/safety review before any future runtime bridge discussion.
