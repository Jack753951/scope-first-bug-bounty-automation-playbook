> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Claude Code Implementation Task — P3.7 Program-Policy Dry-Run Regression Slice

Date: 2026-05-19
Requested by: Hermes / Operator
Route: Claude Code MAX/OAuth via `hermes claude-impl`
Source direction review: `handoff/cowork_p3_7_direction_review.md`
Expected rolling output: `handoff/claude_code_result.md`
Expected named output: `handoff/claude_code_result_p3_7.md`

## Goal

Implement the narrow P3.7 slice approved by `handoff/cowork_p3_7_direction_review.md`:

- Close the P3.1-P3.6 offline candidate/reviewer line as coherent enough to pause.
- Return to the program-policy mainline with an offline-only regression exercise for existing `recon.sh --dry-run --program <slug> --policy-mode planned|live` behavior.
- Add only synthetic/local fixture/test/docs material. Do not modify runtime code or scope gates.

## Binding decision summary

Decision: APPROVE_WITH_CHANGES / PASS_WITH_CONDITIONS.
Implementation tier: T2.
Hermes authority: conditional.
Operator approval required: no, because the slice is offline/local tests/docs/fixture only and does not touch target automation.

Preferred option: Option 1 bundled with scoped Option 3.
Rejected/deferred for this slice: Option 2 fixture-only with no consumer, Option 4 recon-to-runner bridge, Option 5 continued Phase 3 review line, Option 6 block/defer.

## Allowed changes

You may change only these paths unless you stop and write a blocking note:

1. `programs/_examples/sample-lab/scope.json`
   - New synthetic program scope fixture only.
   - Must not contain real domains, real public IPs, customer/program names, credentials, tokens, callbacks, or production language.
   - Prefer synthetic domains already used by tests, such as `lab.local`, `authorized.test`, or clearly reserved test names.

2. `scripts/test_recon_program_policy_dry_run.py`
   - New offline-only test file.
   - It may invoke `recon.sh` using `subprocess.run` in the same style as existing test files.
   - It must not execute scanners, modules, target probes, DNS/network requests, fuzzing, brute force, callbacks, OAST, proxy/pivot/tunnel, or exploit tooling.

3. `docs/recon_policy_dry_run.md` (optional)
   - New short docs page describing synthetic dry-run regression workflow only.
   - No real targets, no live activation instructions, no production or platform submission wording.

4. `handoff/accepted_changes.md`
   - Append-only entry for this implementation slice.
   - Do not rewrite or reorder old entries.

5. `handoff/claude_code_result_p3_7.md`
   - New named implementation summary.
   - Include route/tool, visible model/runtime if exposed, changed files, validations run, safety boundary, and next recommended review.

The wrapper will also update `handoff/claude_code_result.md` and usage JSON automatically.

## Forbidden changes

Do not modify:

- `recon.sh`
- `scripts/program_policy_boundary.py`
- `scripts/program_policy_check.py`
- `scripts/module_runner.py`
- any `scripts/build_*` or `scripts/review_*` production/consumer file
- any file under `scripts/core/**`
- any file under `modules/**`
- any schema under `modules/_schema/**` or any `*/0.1-trial` schema
- `config/scope.txt`
- `config/recon.conf`
- `bin/hermes`
- `run_hermes_worker.ps1`
- `programs/**` except the single new `programs/_examples/sample-lab/scope.json`
- `tests/fixtures/**`, `templates/**`, `evidence/**`, `runs/**`, `loot/**`, `scans/**`, `reports/**`
- scheduler, CI, deployment, billing, OAuth, credential, secret, or repo-setting files

Do not introduce:

- new live-target CLI affordances such as `--target`, `--url`, `--host`, `--scope`, or `--live`
- scanner-output importers/exporters
- platform adapters
- report drafting/submission behavior or vocabulary such as confirmed, verified, valid, reportable, accepted, resolved, submitted, published, bounty
- recon-to-runner coupling; do not invoke `module_runner.py` from the new test
- any runtime hardening change, even if tiny; if a runtime issue is found, stop and document it as a separate required micro-review

## Required implementation behavior

Before writing the new test, inspect the existing tests for patterns, especially:

- `scripts/test_recon_program_cli.py`
- `scripts/test_program_policy_check.py`
- `scripts/test_program_policy_boundary.py`

The new test should exercise the existing program-policy dry-run behavior with synthetic/local fixtures. It should include as many of the following assertions as are practical without modifying runtime code:

1. `recon.sh --dry-run --program sample-lab --policy-mode planned` succeeds or fails closed exactly as expected for synthetic in-scope target(s).
2. `--policy-mode live` is treated only as an offline regression path and must not cause target-touching behavior.
3. Program-policy allow and deny audit events are present where expected.
4. Missing or malformed program scope fails closed.
5. CIDR remains forced-deny under program policy, even if `--allow-cidr` is supplied.
6. Stale or mismatched policy artifacts are rejected if this can be asserted through existing behavior.
7. Target/mode/technique mismatch is rejected if this can be asserted through existing behavior.
8. Dry-run output does not indicate scanner execution.
9. No subprocess names associated with scanners/modules are invoked by the test except `recon.sh` itself and standard shell/python test helpers.
10. The test uses temporary directories/environment isolation where needed and does not write persistent runtime evidence except normal test temp files.

If an assertion cannot be implemented cleanly without runtime edits, document it in `handoff/claude_code_result_p3_7.md` as a deferred assertion rather than changing runtime code.

## Required validations

Run focused tests first, then broader checks:

- `python -m unittest scripts/test_recon_program_policy_dry_run.py`
- relevant existing program-policy/recon tests discovered during inspection
- `python -m unittest discover scripts`
- `HACKLAB=<private-workspace> ./bin/hermes review`
- `git diff --check`

Also run a staged or working-tree added-line safety scan before reporting done. The scan must look for accidental live-target/scanner/exploit/callback/OAST/proxy/pivot/tunnel/credential/secret/submission vocabulary in added lines, allowing only clearly synthetic/test/documentation matches.

## Output requirements

Write `handoff/claude_code_result_p3_7.md` with:

```text
Decision implemented:
Changed files:
Tests/validation run:
Safety boundary confirmation:
Forbidden files untouched:
Deferred assertions or blockers:
Reviewer route/tool and visible model/runtime:
Next recommended review:
```

Append a concise entry to `handoff/accepted_changes.md` that records:

- P3.7 program-policy dry-run regression slice
- changed files
- validation summary
- explicit no-live-target/no-runtime-code/no-scope-file boundary
- next review recommendation

Do not commit or push. Hermes will verify, commit, push, and update the PR.
