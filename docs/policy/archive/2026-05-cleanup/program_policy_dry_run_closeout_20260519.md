> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Program-Policy Dry-Run Closeout — Gate B

Status: historical closeout; active implementation-blocking language superseded by growth-first policy on 2026-05-27
Supersession note: keep dry-run/live separation and hard stops. Do not treat old T3/OSS-gate direction-review wording as a current blocker when focused validation and hard-stop checks are enough.

Date: 2026-05-19
Prepared by: Hermes
Route/tool: Hermes direct synthesis on Windows Git-Bash; no fresh Claude/Cowork direction review was run for this closeout artifact.
Visible model/runtime: Hermes Agent current session; exact backing model is not recorded in repo-local worker usage artifacts for this direct synthesis.

## Purpose

Close the current program-policy dry-run hardening lane after P3.7, P3.8, and the lightweight literal CIDR forced-deny follow-up, then prepare the next mainline direction-review prompt without changing runtime behavior.

This is a planning/handoff artifact only. It does not authorize target-touching behavior, live scans, module execution, recon-to-runner coupling, scope/config changes, report drafting/submission, scheduler, credentials/OAuth, deployment, billing, or production settings.

## Inputs inspected

- `.hermes.md`
- `handoff/active_strategy_queue.md`
- `docs/policy/review_tiering_policy.md`
- `docs/policy/multi_party_review_decision_policy.md`
- `docs/policy/oss_recon_gate.md`
- `handoff/cowork_p3_7_direction_review.md`
- `handoff/third_party_p3_7_implementation_review.md`
- `handoff/project_launch_estimate_20260519.md`
- Current code/test surfaces around `recon.sh`, `scripts/module_runner.py`, and `scripts/test_recon_program_policy_dry_run.py`

## Gate B closeout status

Decision: PASS_WITH_CONDITIONS / CLOSE_GATE_B_FOR_NOW.

Gate B has enough offline confidence to stop adding small program-policy dry-run hardening slices by default.

Completed Gate B items:

1. `_examples/` safety clarification
   - `programs/_examples/README.md` clarifies `_examples/` fixtures are never real program slugs.
   - `automation_permitted: true` in synthetic examples is test-only and not live authorization.

2. P3.7 dry-run program-policy end-to-end regression
   - Synthetic fixture under `programs/_examples/sample-lab/scope.json`.
   - `scripts/test_recon_program_policy_dry_run.py` exercises `recon.sh --dry-run --program <slug> --policy-mode planned|live` through temporary HACKLAB state.
   - No real target, scanner execution, module execution, or recon-to-runner coupling.

3. P3.8 malformed-scope exit-code semantics
   - `recon.sh` now reserves exit code `3` for policy boundary/config errors.
   - Valid policy denies still exit `0` as no-work dry-run outcomes.

4. Literal CIDR forced-deny coverage
   - `192.0.2.0/24` without `--allow-cidr` is accepted by synthetic global scope but policy-denied at `find_live_hosts.input` with `CIDR_REQUIRES_ALLOW_CIDR`.
   - The test asserts no `policy PASS`, no `DRY: httpx`, emitted deny artifact, and no scanner-execution leakage markers.

## Remaining Gate B recommendations

These do not block closeout, but they define future re-open triggers:

- Stale artifact / target / mode / technique mismatch end-to-end harness remains deferred because lower-level runner/policy artifact tests already cover important mismatch behavior and an E2E harness may require a broader fixture design.
- If future work changes `recon.sh`, `scripts/program_policy_boundary.py`, `scripts/program_policy_check.py`, policy artifact schemas, or module runner policy-artifact consumption, re-open Gate B-style regression review.
- If future work introduces lab/live activation, require T4 review and operator approval before target-touching execution.

## Next recommended lane

Prepare a T3 design-only direction review for Gate C:

`handoff/cowork_p3_9_direction_prompt.md` — P3.9 dry-run recon-to-runner bridge direction review.

Why this lane:

- It is the next mainline step named in `handoff/project_launch_estimate_20260519.md` Gate C.
- `scripts/module_runner.py` already validates `policy_boundary/1.0` allow artifacts and remains dry-run-only.
- P3.7/P3.8 proved recon-side dry-run policy artifacts and error semantics are stable enough to ask whether a narrow offline bridge exercise is useful.
- The bridge is a platform/runner boundary, so implementation should use a bounded scope, focused validation, and current hard-stop checks. Lightweight source/OSS comparison is useful when it improves the design, but it is not a blocking ceremony.

## Explicit non-goals for the next prompt

The P3.9 direction prompt should not authorize target-touching or live behavior by itself. It can recommend proceed/change/defer/block, but current authority comes from hard stops, focused validation, and explicit operator approval for live/activation boundaries.

Forbidden until a later approved implementation slice:

- no `recon.sh` runtime edits;
- no `module_runner.py` runtime edits;
- no target-touching execution;
- no scanner/module execution;
- no live/lab activation;
- no real program scope/rules;
- no `config/scope.txt` change;
- no schema promotion;
- no report drafting/submission;
- no scheduler/CI target automation;
- no credentials/OAuth/deployment/billing/production changes.

## Final Decision Block

Decision: PASS_WITH_CONDITIONS
Tier: T1/T2 closeout artifact; next proposed prompt is T3 design-only
Milestone: Gate B program-policy dry-run hardening closeout -> Gate C dry-run recon-to-runner bridge direction
Hermes authority: direct for this closeout; conditional/escalation-only for future T3/T4 slices depending on review outcome
Reviewers consulted:
- Hermes direct synthesis; visible model/runtime: not exposed in repo-local artifact beyond current Hermes session
Validation performed:
- Read current handoff/review policies and relevant strategy/review artifacts
- Inspected repo status and relevant code/test search results
Blocking findings:
- None for closeout
Non-blocking recommendations:
- Keep stale/mismatch E2E harness deferred unless future runtime/bridge work needs it
- Use focused validation and source/OSS comparison if it materially improves any recon-to-runner bridge implementation
Safety boundary:
- Handoff/planning only; no target interaction, no runtime change, no live implementation authorization
Source/OSS pattern check: useful if bridge implementation proceeds; not a gate by itself
User approval required: no for this closeout; yes before any target-touching/lab/live activation
