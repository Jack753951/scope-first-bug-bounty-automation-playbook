> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Direction Review — P3.8 Malformed-Scope Exit-Code Semantics

Date: 2026-05-19
Reviewer route/tool: Claude Code CLI direct direction-review pass using the local `claude` command after the project `hermes cowork` wrapper hit its default max-turn limit. Visible model/runtime reported by the Claude Code session: `claude-opus-4-7`; exact backing runner beyond the tool output surface is not exposed.
Posture: design-only direction review; no code implementation in this artifact.

## Verdict

`APPROVE_WITH_CHANGES`.

P3.8 may proceed as a narrow program-policy boundary hardening slice. The approved direction is to separate malformed/boundary-error policy outcomes from valid policy denies at the `recon.sh` process-exit surface.

## Review Tier

Review tier: T4 process-wise.

Rationale:

- The slice touches `recon.sh` and program-policy runtime semantics.
- `handoff/review_tiering_policy.md` escalates changes to scope enforcement, policy decisions, dry-run/live-mode decisions, and `recon.sh` to T4.
- The substantive change is narrow and hardening-only: it changes exit-code signaling after policy evaluation; it must not activate scanners, target touching, callbacks, modules, live behavior, or scope changes.

Milestone: Program-Policy Boundary Hardening / P3.x return-to-mainline.

Hermes authority: conditional.

Operator approval is not required if the implementation remains inside the approved boundary and independent implementation/safety review passes, because the slice does not change `config/scope.txt`, authorize targets, enable scanner/module execution, add callbacks, or touch production/scheduler/credential settings. Escalate to the operator only if reviewers materially disagree or if an operator-visible consumer of the current exit-code behavior is identified.

## OSS Recon Gate

OSS Recon Gate is not strictly required as a full gate because this slice does not introduce a new schema, module, runner, reporting boundary, external-tool integration, or finding/evidence lifecycle. A lightweight design comparison is still useful:

- Unix CLI conventions: distinguish "evaluated but found no matches" from "tool/config/runtime error." Adopt the pattern by keeping valid policy denies as non-error while making malformed policy state non-zero.
- ProjectDiscovery-style tools such as nuclei/httpx/subfinder: empty result sets are generally not fatal, but invalid configuration or runtime errors are fatal. Adapt the pattern without copying any scanner/network behavior.
- Semgrep/ShellCheck-style tools: rule/config load failures are non-zero even if no findings are produced. Adopt the analogy for malformed `scope.json` / validator failure.
- CI conventions: CI gates on exit codes, so malformed policy configuration must not look like a successful no-result run. Adopt the philosophy, but do not wire CI/scheduler behavior in this slice.

Conclusion: lightweight OSS comparison supports the proposed split; no target-touching OSS behavior is adopted.

## Recommended Exit-Code Semantics

Use a four-part taxonomy:

1. Invalid operator/config/runtime state
   - Examples: malformed program `scope.json`, `VALIDATOR_DENY`, boundary script missing, policy Python unavailable, invalid policy timeout, missing/unreadable policy artifact, artifact validation failure.
   - Expected policy surface: `POLICY_VERDICT=error` or equivalent `PROGRAM_POLICY_BOUNDARY_ERROR` class.
   - Recommended exit: non-zero; reserve exit code `3` as `POLICY_BOUNDARY_ERROR`.

2. Valid policy deny
   - Examples: out-of-scope, technique not allowed, automation not permitted, CIDR requires `--allow-cidr`, mode/window deny.
   - Expected policy surface: structured deny with `POLICY_VERDICT=deny` and deny reason codes.
   - Recommended exit: zero in dry-run/planned preflight when the CLI evaluated successfully and simply had no authorized work to do.

3. No live hosts after safe filtering
   - Examples: all candidates dropped by `safe_target` or global scope filtering.
   - Recommended exit: preserve current zero/no-work semantics unless a separate reviewed slice changes global safe-target exit semantics.

4. No live hosts because every candidate was policy-error denied
   - This is a subset of category 1.
   - Recommended exit: non-zero, preferably exit `3`.

Mode invariance:

- Malformed policy state should be non-zero in `dry-run`, `planned`, and `live` modes.
- `dry-run` should catch malformed scope before any future live execution.

Recommended mechanism:

- Add a `POLICY_ERROR_COUNT` accumulator in `recon.sh`.
- Increment it when `policy_decide` resolves to the error class, not for ordinary valid denies.
- After the existing summary is printed, exit `3` if `POLICY_ERROR_COUNT > 0`.
- Do not short-circuit on the first policy error; continue dropping candidates so audit/drop artifacts remain complete.

A narrower alternative — exit non-zero only when all entry-stage candidates are policy-error denied — is defensible but less informative. The recommended implementation is the counter approach.

## Approved Implementation Scope

Allowed files:

1. `recon.sh`
   - Initialize `POLICY_ERROR_COUNT=0` at run start.
   - Increment it only for policy-boundary error outcomes.
   - At final exit, after existing summary output, exit `3` if `POLICY_ERROR_COUNT > 0`.
   - Add a short inline comment reserving exit `3` as `POLICY_BOUNDARY_ERROR`.

2. `scripts/test_recon_program_policy_dry_run.py`
   - Strengthen malformed-scope regression to assert non-zero, preferably exact return code `3`.
   - Preserve existing fail-closed assertions: `policy DENY`, `VALIDATOR_DENY`, no PASS, no scanner/module execution markers.
   - Add or strengthen allowed dry-run tests confirming expected successful dry-run still exits `0`.
   - Add a valid policy-deny regression confirming ordinary deny remains exit `0`.

3. Handoff files
   - `handoff/cowork_p3_8_direction_review.md`
   - `handoff/claude_code_task_p3_8.md`
   - `handoff/claude_code_result_p3_8.md`
   - `handoff/active_strategy_queue.md`
   - `handoff/accepted_changes.md`
   - standard rolling worker outputs/archives if a worker wrapper is used.

Forbidden files/surfaces:

- `scripts/program_policy_boundary.py`
- `scripts/program_policy_check.py`
- `scripts/module_runner.py`
- `scripts/core/**`
- `modules/**`
- `config/scope.txt`
- `config/recon.conf`
- `programs/_examples/sample-lab/scope.json`
- scanner/module/runtime activation surfaces
- reports, loot, scans, runs, evidence
- scheduler, CI, OAuth, credentials, billing, deployment, production settings

## Required Tests

Focused tests:

- `test_malformed_program_scope_fails_closed_at_policy_gate` must assert exit code `3` or at least non-zero, plus the existing fail-closed markers.
- Existing allow-path dry-run tests must continue to assert `returncode == 0`.
- Add a valid policy-deny test, preferably an out-of-scope program-policy denial, asserting:
  - policy DENY marker appears;
  - deny reason is policy-valid, not boundary-error;
  - return code remains `0`;
  - no scanner/module execution leakage.

Validation gates:

- `python -m unittest scripts/test_recon_program_policy_dry_run.py`
- `python -m unittest discover scripts`
- `git diff --check`
- `HACKLAB=<private-workspace> ./bin/hermes review`

Safety assertions:

- Real `config/scope.txt` unchanged.
- Synthetic fixture unchanged.
- No scanner/module invocation added.
- No target-touching behavior introduced.
- No `module_runner.py` import/coupling.

## Out of Scope

- Live target execution.
- Scanner execution.
- Module execution.
- Callback/OAST behavior.
- Fuzzing, brute force, exploit attempts.
- Changes to `config/scope.txt` or real program scopes.
- Recon-to-runner bridge.
- Report drafting/submission adapters.
- Scheduler/CI activation consuming exit code `3`.
- Schema promotion or new platform contracts.
- Credentials/OAuth/billing/deployment/production settings.

## Blocking Issues

None for the direction review.

## Non-Blocking Recommendations

1. Reserve exit code `3` explicitly as `POLICY_BOUNDARY_ERROR` in `recon.sh` comments.
2. If cheap, emit a final summary line such as `policy_error_count=<N>`; do not let this become a new broad contract.
3. Do not document new public CLI contract outside `recon.sh` unless reviewers decide the documentation surface is worth it.
4. Keep stale-artifact and target/mode/technique mismatch follow-ups separate; P3.8 only handles malformed/boundary-error exit semantics.

## Final Multi-Party Review Decision Block

- Implementation review: required after implementation.
- Safety review: required after implementation; must confirm no scope/config/scanner/callback/module-runner surface was added.
- Architecture/direction review: this artifact returns `APPROVE_WITH_CHANGES`.
- Hermes synthesis authority: conditional T4 authority; operator approval not required if implementation stays within the allowed boundary and independent reviews align.
- Final disposition: proceed to a narrow implementation task for P3.8.
- Next action: create `handoff/claude_code_task_p3_8.md` with the allowed-file list and required tests, then implement via the offline worker route or a tightly scoped local patch, followed by independent implementation/safety review and Hermes verification.
