> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Independent Implementation/Safety Review — P3.7 Program-Policy Dry-Run Regression

Date: 2026-05-19
Reviewer route/tool: Claude Code CLI (Anthropic API), invoked as an independent implementation/safety review pass. The visible model/runtime is `claude-opus-4-7` as identified by the session model id. Exact backing Anthropic runner beyond the tool output surface is not exposed; this is the strongest model identification available without crossing a tool-output boundary.
Reviewed commit: `c7dfe2c` on branch `feat/p1-4-program-policy-boundary`.
Source direction review: `handoff/cowork_p3_7_direction_review.md`.
Source implementation result: `handoff/claude_code_result_p3_7.md` (and rolling `handoff/claude_code_result.md`).

## Verdict

**PASS_WITH_RECOMMENDATIONS.**

The P3.7 implementation stayed strictly inside the approved tests/fixture/handoff-only boundary. No forbidden files were changed. The synthetic fixture and offline test contain no live-target affordance, no credentials/tokens/OAuth/secrets, no scanner/module execution path, no report/platform/submission surface, and no recon-to-runner coupling. Validation evidence is credible and reproducible. The Hermes fixup after the Claude Code worker hit max-turn is documented, contained to test expectations, and stayed inside the same approved boundary.

The recommendations below do not block acceptance; they queue specific items for a separate fresh micro-direction review and should not be smuggled into P3.7.

## Scope Reviewed

- Direction review: `handoff/cowork_p3_7_direction_review.md`.
- Implementation task: `handoff/claude_code_task_p3_7.md`.
- Implementation result: `handoff/claude_code_result_p3_7.md`.
- Active strategy queue: `handoff/active_strategy_queue.md`.
- Append-only log: `handoff/accepted_changes.md` (head entry).
- Commit `c7dfe2c` full file list:
  - `programs/_examples/sample-lab/scope.json` (new, 55 lines)
  - `scripts/test_recon_program_policy_dry_run.py` (new, 495 lines)
  - `handoff/cowork_p3_7_direction_review.md` (new, 793 lines)
  - `handoff/claude_code_task_p3_7.md` (new, 143 lines)
  - `handoff/claude_code_result_p3_7.md` (new, 101 lines)
  - `handoff/claude_code_task.md` (rolling pointer update)
  - `handoff/claude_code_result.md` (rolling pointer update)
  - `handoff/active_strategy_queue.md` (queue update)
  - `handoff/accepted_changes.md` (append-only entry, 2 lines added at head)
  - `handoff/claude_code_impl_run_20260519_163456.json` (worker usage JSON)
  - `handoff/archive/rolling/claude_code_result_20260519_163456.md` (rolling archive)
  - `handoff/archive/rolling/cowork_result_20260519_162311.md` (rolling archive)
- Tooling surface scanned: every changed file inspected; forbidden-path negative diff confirmed.

## Boundary Compliance

### Allowed surface — all matches against the direction review's five-file maximum

| Approved path | Status | Notes |
|---|---|---|
| `programs/_examples/sample-lab/scope.json` | Present, new | Lives under `_examples/`; `recon.sh` line 319 already forbids resolving this as a real `--program` slug. |
| `scripts/test_recon_program_policy_dry_run.py` | Present, new | Subprocess-driven offline unittest only. |
| `docs/recon_policy_dry_run.md` | Not added | Optional; result file justifies omission. Acceptable. |
| `handoff/accepted_changes.md` | Appended at head | Single new entry, no truncation or reorder of older entries (`git diff` confirms head-append only). |
| `handoff/claude_code_result_p3_7.md` | Present, new | Named implementation summary. |
| Rolling `handoff/claude_code_task.md`, `handoff/claude_code_result.md`, `handoff/active_strategy_queue.md`, `handoff/claude_code_impl_run_*.json`, `handoff/archive/rolling/*.md` | Present, updated by wrapper | Allowed by the `claude-impl` worker contract. |

### Forbidden surface — explicit negative confirmation

The following negative `git diff c7dfe2c~1 c7dfe2c -- <paths>` was empty:

- `recon.sh`
- `scripts/program_policy_boundary.py`
- `scripts/program_policy_check.py`
- `scripts/module_runner.py`
- `scripts/core/**`
- `modules/**`
- `modules/_schema/**`
- `config/scope.txt`
- `config/recon.conf`
- `bin/hermes`
- `run_hermes_worker.ps1`
- `reports/**`, `loot/**`, `scans/**`, `runs/**`, `evidence/**`

The new `scope.json` is the only entry under `programs/` and is correctly placed under `programs/_examples/` (not `programs/<real-slug>/`). No new files under `tests/fixtures/`, `templates/`, `scheduler/`, CI, OAuth, billing, or deployment paths.

### Forbidden behaviors — surveyed in added lines

- No new live-target CLI affordance (`--target`, `--url`, `--host`, `--scope`, `--live`) introduced anywhere. The test re-uses existing `recon.sh` flags only.
- No scanner-output importer/exporter.
- No platform adapter.
- No report drafting/submission vocabulary. Token grep on `submitted|published|bounty|confirmed|verified|reportable|customer|production` against the fixture returned no matches. Same grep against the test file returned only docstring negatives ("the test asserts these are not invoked", etc.) — i.e., the test names forbidden activity only to assert its *absence*, not to perform it.
- No recon-to-runner coupling. `module_runner.py` is not imported, not invoked, and not referenced from the test or fixture.
- No runtime hardening sneaked in. The malformed-scope deferred assertion is documented in `claude_code_result_p3_7.md` rather than smuggled into a `recon.sh` patch.

Boundary compliance: **CLEAN**.

## Safety / Security Findings

### Fixture — `programs/_examples/sample-lab/scope.json`

- Lives under `_examples/`, which `recon.sh` excludes from real-program resolution. The test installs a copy into a temporary `HACKLAB/programs/sample-lab/` directory only.
- `program.url` is a synthetic `file:///` placeholder, not a real URL.
- `program.authorization_reference` is explicit prose stating: synthetic, offline, no real targets.
- `scope.in_scope` uses RFC 6761 `.test` and RFC 6762 `.local` reserved/non-routable TLDs already used by `scripts/test_recon_program_cli.py`.
- `techniques.allowed = ["http_probe"]` only. `techniques.forbidden` correctly enumerates `dos`, `credential_brute_force`, `social_engineering`, `physical`, `malware`, `callback_payloads`.
- `techniques.automation_permitted: true` — flagged as non-blocking observation (see recommendation 1 below). The accompanying `automation_notes` field explicitly disclaims live activation: "Synthetic fixture only. Automation flag is present so the offline dry-run regression test exercises the allow path; no live target activation is implied." Combined with the `_examples/` exclusion at `recon.sh` line 319 and the test's `--dry-run`-only invocation pattern, the field is safely fenced.
- No credentials, tokens, API keys, OAuth references, callbacks, webhook URLs, OAST endpoints, proxy/pivot endpoints, real platform names, or customer/program identifiers.

### Test — `scripts/test_recon_program_policy_dry_run.py`

- Every `recon.sh` invocation uses `--dry-run`. No live mode is executed against any target.
- `--policy-mode live` is exercised only under `--dry-run`, as offline regression of the gate's allow/deny path.
- Test uses a per-test `tempfile.TemporaryDirectory` under repo root as `HACKLAB`. The real `config/scope.txt` is never written; a `tearDownClass` assertion verifies its sha256 is unchanged across the entire run. The committed fixture sha256 is also re-verified in `tearDownClass`.
- The test does not import `module_runner`, does not import any scanner library, does not open sockets, does not spawn DNS queries, and does not perform raw subprocess execution against scanner binaries.
- The test's `where.exe bash` discovery and `bash --version` probe are read-only and standard.
- The CIDR case uses RFC 5737 documentation range `192.0.2.0/24`.
- Scanner-execution leakage assertions (`[critical]`, `[high]`, `Found `, `Open: `, `Nmap scan report`, etc.) and denied-technique dry-run markers (`DRY: nuclei`, `DRY: nmap`, `DRY: subfinder`, `DRY: naabu`, `DRY: feroxbuster`, `DRY: curl -s https://crt.sh`) are asserted as *absent*. The test names these strings only to enforce their non-appearance.

### No new attack-surface vocabulary introduced

- No mention of `interactsh`, `requestbin`, `burpcollab`, `webhook`, listener, beacon, relay, reverse-shell, exploit/fuzz/brute-force tooling, or callback infrastructure outside the negative-assertion list.
- No credential/token/secret strings introduced.
- No scheduler, CI auto-execution, deployment, billing, or production-setting affordance.

Safety findings: **CLEAN**.

## Test / Validation Assessment

Reproduced independently on the working tree at `c7dfe2c`:

| Check | Command | Result |
|---|---|---|
| Focused P3.7 test | `python -m unittest scripts/test_recon_program_policy_dry_run.py` | PASS — 12 tests, 0 failures, 0 errors, 36.5s. |
| Full scripts discovery | `python -m unittest discover scripts` | PASS — 387 tests, 0 failures, 0 errors, 8 skipped, 104.8s. |
| Whitespace / diff hygiene | `git diff --check c7dfe2c~1 c7dfe2c` | exit 0; no errors. |
| Hermes review | `HACKLAB=<private-workspace> ./bin/hermes review` | PASS — Python compile OK across 75 files, all shell scripts `bash -n` OK, runtime lock clear, working tree clean, `config/scope.txt` 12 entries unchanged. |
| Working tree state | `git status` | Clean; branch up to date with origin. |

The result file's claim of "12 tests OK, 62 tests OK (skipped=2) on adjacent suite, 387 tests OK (skipped=8) on full discovery" is consistent with the independent re-run. The implementation result's record of `hermes review` PASS is consistent with this reviewer's re-run.

Coverage versus the direction review's checklist:

| Required behavior (per task) | Status in test |
|---|---|
| planned-mode allow path succeeds for in-scope synthetic target | Covered (`test_synthetic_program_dry_run_planned_mode_allows_and_emits_artifact`). |
| live-mode treated as offline regression only | Covered (`test_synthetic_program_dry_run_live_mode_remains_offline_regression_only`). |
| Program-policy allow audit events present | Covered (`test_audit_log_records_program_policy_allow_event` asserts `PROGRAM_POLICY_ALLOW`, `target=`, `mode=planned`). |
| Missing program scope fails closed | Covered (`test_missing_program_scope_file_fails_closed`). |
| Malformed program scope fails closed | Covered with deferred-exit-code caveat (`test_malformed_program_scope_fails_closed_at_policy_gate`) — see recommendation 2. |
| CIDR + `--allow-cidr` remains policy-limited | Covered (`test_cidr_target_with_allow_cidr_stays_dry_run_and_policy_limited`) — see recommendation 3 on semantics. |
| Stale artifact rejection | Deferred (documented in result file). |
| Target/mode/technique mismatch rejection | Deferred (documented in result file). |
| Dry-run output does not indicate scanner execution | Covered (`test_dry_run_output_does_not_indicate_scanner_execution` plus inline `assert_no_*` helpers across all positive-path tests). |
| No scanner subprocess invocation by the test | Reviewer-verified by source inspection: only `recon.sh` and `bash --version`/`where.exe bash` discovery are invoked. |
| Tests use temporary directories / env isolation | Verified — per-test `TemporaryDirectory` under repo root, scope sha256 fences. |
| Reserved `_examples` slug is rejected at the CLI layer | Covered (`test_reserved_examples_slug_is_rejected_by_recon`). |
| `--program` requires `--policy-mode` | Covered (`test_program_requires_policy_mode_for_synthetic_slug`). |
| Real `config/scope.txt` untouched | Covered (`test_global_scope_file_in_real_repo_is_unchanged_by_dry_run` plus `tearDownClass` sha256 fence). |
| Synthetic fixture file untouched | Covered (`test_synthetic_fixture_file_is_unchanged_by_dry_run` plus `tearDownClass` sha256 fence). |

Validation assessment: **CREDIBLE AND REPRODUCIBLE.**

## Max-Turn Worker / Hermes Fixup Assessment

Worker run metadata (`handoff/claude_code_impl_run_20260519_163456.json`):

- `subtype: error_max_turns`, `terminal_reason: max_turns`, `num_turns: 36`, `total_cost_usd: 3.2401427500000004`, `duration_ms: 457209`.
- Model usage: `claude-opus-4-7` (dominant: 27,771 output tokens, ~$3.234) and `claude-haiku-4-5-20251001` (minor: 18 output tokens, ~$0.006).
- `permission_denials: []`, no errors other than the max-turn hit.
- The 1-hour ephemeral cache creation (~133k tokens) and large cache-read (~3.42M tokens) profile is consistent with a sustained workspace-edit session.

Hermes fixup, per `handoff/claude_code_result_p3_7.md` and `handoff/claude_code_result.md`:

- The worker produced the fixture, the test file, and the named result before reaching max turns. Hermes completed test-expectation alignment to actual fail-closed semantics (the malformed-scope path: assert `policy DENY` + `VALIDATOR_DENY` + no PASS, rather than non-zero exit code) and wrote the rolling result.
- The fixup stayed inside the same approved tests/fixture/handoff-only boundary. No runtime code path was modified.
- The fixup is explicitly disclosed in the rolling result ("Status: implemented with Hermes verification/fixup after Claude Code worker reached max turns") and in the `accepted_changes.md` head entry ("Hermes fixed test expectations to match existing fail-closed runtime semantics and completed local verification").
- The deferred exit-code-semantics observation is recorded under "Deferred assertions or blockers" in the named result rather than addressed by a runtime patch.

The Hermes fixup is **acceptable** for this slice because:

1. It modified only test expectations, not runtime code.
2. It stayed inside the same approved tests/fixture/handoff boundary.
3. It is disclosed in both the rolling result and the append-only log.
4. The semantic the fixup encodes (fail-closed observed via `policy DENY` + `VALIDATOR_DENY` + absence of PASS, regardless of process exit code) matches actual `recon.sh` behavior and is the conservative reading.
5. No runtime defect was masked: the deferred observation is recorded as a candidate for a fresh micro-direction review.

The independent implementation/safety review the direction review asked for is this artifact, which the result file specifically anticipates.

## Required Fixes

None. The slice is acceptable as committed.

## Non-Blocking Recommendations

These should be queued for separate handling and explicitly **must not** be folded into P3.7:

1. **`automation_permitted: true` in the synthetic fixture.** The flag is correctly fenced by `_examples/` exclusion, the explicit `authorization_reference` prose, and the test's `--dry-run`-only invocation pattern, but it is the only "automation_permitted: true" entry that has ever lived inside `programs/` in the repo. Consider one of: (a) adding a top-level repo comment or `programs/_examples/README.md` note clarifying that `_examples/` fixtures are *never* resolvable as real program slugs and that any `automation_permitted` flag inside `_examples/` is test-only, or (b) inverting the fixture to `automation_permitted: false` plus a parallel test variant that flips it to true only on a per-test temp copy. Either approach removes the surface a future operator typo could exploit. This is a docs/test-only follow-up and does not require runtime change.

2. **Malformed-scope fail-closed exit-code semantics.** The current test asserts `policy DENY stage=find_live_hosts.input` + `VALIDATOR_DENY` + absence of any PASS marker, but does *not* assert a non-zero process exit code. `recon.sh` may currently exit 0 with a "zero live hosts" summary after the policy gate denies all stage inputs. Operators or future CI consumers may reasonably expect a non-zero exit code in this state. The fix is a runtime change (and therefore out of scope for P3.7) and should route through a fresh micro-direction review with its own tiering and OSS Recon Gate consideration.

3. **CIDR test verifies `TECHNIQUE_NOT_ALLOWED`, not literal `CIDR_REQUIRES_ALLOW_CIDR`.** The direction review at Question 6 item 4 anticipated asserting `CIDR_REQUIRES_ALLOW_CIDR` exactly. The committed test instead exercises the synthetic program's `techniques.allowed = ["http_probe"]` path and asserts the port-scan stage is denied with `TECHNIQUE_NOT_ALLOWED`. Both are valid fail-closed observations, but they are not the same observation. The literal `CIDR_REQUIRES_ALLOW_CIDR` path remains uncovered by recon-side end-to-end tests (it may be covered by lower-level policy unit tests). A separate micro-direction review could add an explicit CIDR-no-`--allow-cidr` regression, or a `--allow-cidr` regression against a fixture whose `techniques.allowed` includes a normally CIDR-blocked technique.

4. **Worker turn budget.** The Claude Code worker spent 36 turns and $3.24 on a slice with two committed source files plus handoff prose. The per-turn yield is consistent with a max-turn fight against the deferred-assertion question rather than implementation complexity. For future similarly-scoped T2 slices, consider either (a) a lower `CLAUDE_IMPL_MAX_TURNS` ceiling, or (b) decomposing the slice into "scaffold tests" then "align expectations" passes. Non-blocking.

5. **Stale artifact and target/mode/technique mismatch deferrals.** Documented in the result file. These remain reasonable deferrals; flag here so the next periodic review notices they have aged and decides whether to commission a separate micro-direction review.

## Final Multi-Party Review Decision Block

Per `handoff/multi_party_review_decision_policy.md`:

- **Implementation review (this artifact):** PASS_WITH_RECOMMENDATIONS. The committed code is acceptable; recommendations are non-blocking and must not be folded back into P3.7.
- **Safety review (this artifact, combined):** PASS. No live-target affordance, no scope/runtime weakening, no credential/secret/submission/platform surface, no recon-to-runner coupling. The synthetic fixture and the test are offline-only by construction.
- **Architecture / direction review (`handoff/cowork_p3_7_direction_review.md`, prior):** APPROVE_WITH_CHANGES; the changes were honored.
- **Hermes synthesis authority:** This slice is T2 with conditional Hermes authority per the direction review. Operator approval is **not** required for acceptance because the slice did not cross any T4/T5 boundary, did not touch `config/scope.txt`, did not modify runtime code, and did not introduce live-target automation.
- **Final disposition:** ACCEPT P3.7 as committed at `c7dfe2c`. Update `handoff/active_strategy_queue.md` to move P3.7 from "current lane" to "completed", and to record the recommendations above as candidate fresh micro-direction reviews (not as P3.7 follow-on patches).
- **Next slice gate:** Before opening any of the recommendation follow-ups, route them through a fresh direction review (with appropriate tiering and OSS Recon Gate consideration where applicable). Do not smuggle runtime hardening (recommendation 2) or new CIDR coverage that asserts internal deny codes (recommendation 3) into a P3.7 amendment.
- **Frozen evidence:** This review file, the direction review, the implementation task, the named implementation result, the worker JSON, and the commit `c7dfe2c` together form the audit trail for P3.7.
