> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Cowork Direction Prompt — P3.8 Malformed-Scope Exit-Code Semantics

Date: 2026-05-19
Requested route/tool: Claude/Cowork direction review via Claude Code MAX/OAuth when available. If exact runtime model is not exposed, state that limitation.
Task type: micro-direction review before implementation

## Context

P3.7 added an offline dry-run regression fixture and tests for program-policy runtime behavior. Independent implementation/safety review returned `PASS_WITH_RECOMMENDATIONS` and accepted P3.7, but recommendation 2 identified an unresolved runtime-semantics question:

> Malformed program scope currently fails closed at the policy gate (`policy DENY stage=find_live_hosts.input` with `VALIDATOR_DENY` and no PASS/scanner markers), but `recon.sh` may still exit 0 after the policy gate drops all stage inputs and the pipeline reaches a zero-host summary. Operators or future CI consumers may reasonably expect non-zero exit when all candidate inputs were dropped due to a malformed program policy.

This prompt asks for a direction review only. Do not implement yet.

## Files / Evidence To Inspect

- `.hermes.md`
- `handoff/review_tiering_policy.md`
- `handoff/oss_recon_gate.md`
- `handoff/multi_party_review_decision_policy.md`
- `handoff/third_party_p3_7_implementation_review.md`, especially recommendation 2
- `handoff/active_strategy_queue.md`
- `handoff/active_testing_policy.md`
- `recon.sh`, especially `policy_decide` and `filter_safe_and_policy_targets`
- `scripts/test_recon_program_policy_dry_run.py`, especially `test_malformed_program_scope_fails_closed_at_policy_gate`
- `scripts/program_policy_boundary.py`
- `scripts/program_policy_check.py`

## Current Observed Boundary

Current P3.7 test intentionally does not assert non-zero exit for malformed program scope. It asserts:

- `policy DENY stage=find_live_hosts.input`
- `VALIDATOR_DENY`
- no `policy PASS stage=find_live_hosts.input`
- no denied-technique dry-run scanner markers
- no scanner-execution leakage

This is fail-closed from a target-touching perspective, but ambiguous from an operator/CI exit-code perspective.

## Direction Questions

Please answer:

1. Review tier and authority:
   - Is this T2, T3, or T4?
   - Does changing exit-code behavior for program-policy denial count as safety/runtime boundary work because it touches `recon.sh` and program-policy semantics?
   - What review/implementation route is required?

2. Desired semantics:
   - Should malformed program scope produce non-zero process exit in `recon.sh`, even under `--dry-run`?
   - Should all policy-boundary `status=error` denials produce non-zero exit, or only validator/malformed-policy errors?
   - Should ordinary policy denials such as out-of-scope/technique-not-allowed remain zero in dry-run, or become non-zero when they drop all candidate inputs?
   - Should the behavior differ between `dry-run`, `planned`, and `live` policy modes?

3. Failure taxonomy:
   - Recommend a minimal taxonomy separating:
     - invalid operator/config/runtime state;
     - valid policy deny;
     - no live hosts after safe filtering;
     - no live hosts because every candidate was policy-error denied.
   - Which category should map to non-zero exit?

4. Implementation boundary:
   - If approved, what exact files may Codex/Claude Code edit?
   - Should this be a test-first slice limited to `recon.sh` and `scripts/test_recon_program_policy_dry_run.py`, plus handoff updates?
   - Should `scripts/program_policy_boundary.py` or `scripts/program_policy_check.py` remain untouched?

5. Required tests:
   - What focused tests are required before acceptance?
   - At minimum, should P3.8 add/adjust a test asserting malformed `scope.json` exits non-zero while preserving no scanner/module execution?
   - What adjacent regression should prove normal allowed dry-run remains zero?
   - Should out-of-scope or technique-not-allowed dry-run denials remain zero or non-zero?

6. OSS Recon Gate:
   - Is OSS Recon Gate required for this micro-slice?
   - If required or useful, compare briefly with 2-5 relevant patterns, e.g. Unix CLI exit-code conventions, ProjectDiscovery-style tool failures, Nuclei/httpx structured failures, CI gating conventions.
   - Do not run scanners or contact targets; this is design-only.

7. Safety boundary:
   - Confirm that the proposed implementation must not run live scans, alter `config/scope.txt`, change program scope examples, add scanner/module execution, wire recon-to-runner coupling, or authorize target-touching behavior.

## Requested Output Format

Return a direction review with:

```text
Review tier:
Milestone:
Decision: APPROVE / APPROVE_WITH_CHANGES / DEFER / BLOCK
Hermes authority:
OSS Recon Gate:
Recommended exit-code semantics:
Implementation scope:
Required tests:
Out of scope:
Blocking issues:
Non-blocking recommendations:
Final Multi-Party Review Decision Block:
```

## Safety Footer

No live scans. No target interaction. No scanner/module execution. No callbacks/OAST. No changes to `config/scope.txt`. No report drafting/submission. No production, scheduler, OAuth, credential, billing, or deployment changes. This is a design-only direction review.
