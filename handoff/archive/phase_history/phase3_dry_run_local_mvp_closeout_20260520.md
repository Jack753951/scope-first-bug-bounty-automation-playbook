> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Phase 3 Dry-Run/Local MVP Closeout Checkpoint

Status: accepted closeout checkpoint
Date: 2026-05-20
Prepared by: Hermes
Tier: T1 documentation / milestone closeout synthesis
Hermes authority: direct for offline documentation closeout; escalation-only for any lab/live activation
Scope: planning and handoff only; no code, schema, validator, runner, scanner, profile, manifest, scope, target, report, scheduler, credential, deployment, or production behavior changed

## Decision

Phase 3 can close as an offline/dry-run local MVP milestone, with conditions.

Decision: PASS_WITH_CONDITIONS / CLOSE_PHASE_3_OFFLINE_MVP

The project is coherent enough to stop adding Phase 3 micro-slices by default and move the next default lane to Phase 4A Controlled Lab Semi-Automated Calibration planning/entry preparation.

This is not approval to touch a lab or real target. Phase 4A activation still requires explicit operator target selection, narrow lab scope documentation, T4/T5 review, deny-by-default runtime tests, rate/timeout/kill controls, audit logging, and explicit activation approval.

## What Phase 3 achieved

Phase 3 established the offline governance and dry-run backbone for the long-term authorized bug-bounty platform:

1. Curated synthetic candidate-review fixtures exist for near-real bug-bounty-shaped cases.
2. Candidate packet, gap review, verification plan, and report-readiness gate workflow can be exercised offline using committed fixtures.
3. Module runner discovery and preview behavior is covered for the two committed Level 1 modules under the conservative `audit-baseline` profile.
4. Program-policy dry-run behavior has synthetic sample-lab coverage, including allow/deny semantics and fail-closed malformed-scope behavior.
5. Recon-to-runner policy artifact flow is covered as dry-run/direct-read/test-harness-only behavior, with no auto-discovery, no auto-copy runtime bridge, no scanner/module execution, and no live target path.
6. SOC/evidence-bucket and reviewer-gap artifacts exist as static calibration companions, not runtime consumers or schemas.
7. Multi-party review, review tiering, OSS Recon Gate, memory/strategy routing, and active strategy queue governance are in place.
8. P3.13/P3.14/P3.15 clarified active-testing risk tiers and module manifest/profile mapping while deferring formal field promotion.
9. Phase 4A has been inserted as a controlled lab calibration phase before any real bug-bounty private beta.

## Current capability statement

The platform can currently support:

- deterministic offline/dry-run policy and contract validation;
- local module-runner previews that do not execute modules;
- profile and policy-artifact binding for preview planning;
- synthetic candidate triage workflow exercises;
- report-readiness review logic below confirmed-finding/report-submission status;
- documentation-backed safety and review governance.

The platform still cannot safely support, without later phases and explicit approval:

- public or private bug-bounty target scanning;
- lab or live scanner/module execution;
- exploit, fuzz, brute-force, callback/OAST, proxy, pivot, tunnel, or transport workflows;
- automatic recon-to-runner execution;
- automatic finding confirmation;
- report submission or platform adapters;
- scheduler/CI target-touching automation;
- credentials, loot handling, OAuth, deployment, billing, or production-like operation.

## Phase 3 exit conditions

Phase 3 exit condition | Status | Evidence / note
---|---|---
Risk-tier / active-testing policy accepted | Met | `handoff/active_testing_policy.md`, `handoff/p3_13_module_risk_tier_policy_result.md`
Future manifest/profile field direction decided | Met | P3.14 deferred formal promotion; P3.15 documented crosswalk only
Dry-run/local MVP gaps listed | Met | `handoff/first_bounty_readiness_checkpoint_20260520.md`
Phase 4A inserted before real bug bounty | Met | `handoff/phase4a_controlled_lab_calibration_plan_20260520.md`
No live activation hidden inside Phase 3 | Met | P3.15 and this closeout keep activation deferred
Operator-facing demo shape identified | Met as plan/checklist | See the dry-run demo checklist below; execution remains local/offline only
Worktree clean-enough acceptance bundle | Conditional | Requires final local validation and any operator-chosen cleanup of unrelated untracked artifacts before a formal commit/release bundle

## Local dry-run demo checklist

Purpose: demonstrate the Phase 3 offline MVP without touching any real target.

This checklist is allowed only as local/offline dry-run validation. It must not be modified to use a real target, real program scope, scanner execution, module execution, external network, callbacks, report submission, or scheduler automation.

Suggested operator-facing sequence:

1. Confirm repository status and no lock:

```bash
git status --short
USER=${USER:-Owner} HACKLAB=<private-workspace> ./bin/hermes review
```

2. Run the focused synthetic recon-to-runner dry-run bridge tests:

```bash
python -m unittest scripts.test_recon_runner_bridge_dry_run -v
```

Expected posture:

- test harness may create temporary directories only;
- `recon.sh` remains dry-run in the test;
- module runner emits preview-only output;
- no scanner/module execution leakage markers appear;
- no real target is touched.

3. Run the local candidate workflow fixture smoke:

```bash
python scripts/build_candidate_workflow_fixture.py --repo-root . --json \
  | python -c 'import json,sys; d=json.load(sys.stdin); print(d["schema_version"], d["status"], d["summary"])'
```

Expected posture:

- schema version remains `candidate_workflow_fixture/0.1-trial`;
- output remains candidate/review workflow data;
- no report draft, submission, platform adapter, target interaction, or confirmed-finding promotion occurs.

4. If needed, run a broader offline scripts suite:

```bash
python -m unittest discover scripts
```

5. Re-run final review:

```bash
USER=${USER:-Owner} HACKLAB=<private-workspace> ./bin/hermes review
```

## Remaining gaps carried into Phase 4A+

These are not blockers to closing Phase 3 as an offline MVP, but they block lab/live/private-beta activation:

1. Lab target selection and narrow lab scope artifact do not exist yet.
2. No T4/T5 direction review has approved a live-ish lab boundary.
3. No lab activation command sequence is approved.
4. Runtime deny-by-default tests for non-lab/public targets must be written before activation.
5. Rate limits, timeouts, kill switch, stop conditions, rollback/cleanup, and audit trail must be documented and tested for the selected lab boundary.
6. Evidence redaction/minimization for real tool output is not ready.
7. Candidate findings cannot become confirmed findings without human verification.
8. Report drafting/submission remains deferred.
9. Real bug-bounty program scope/rules and platform adapters remain out of scope.
10. Scheduler/CI target-touching automation remains blocked.

## Phase 4A entry criteria reaffirmed

Before Phase 4A can do anything live-ish:

1. Operator selects the exact lab target class and scope: local lab, intentionally vulnerable app, explicit CTF/training target, or user-owned test asset.
2. Lab scope/rules are documented separately from real bug-bounty program scope.
3. Review tier is assigned; default T4 for live-ish lab activation, escalating to T5 if credentials, persistence, callbacks, destructive behavior, external services, production assets, or scheduler/CI are involved.
4. Deny-by-default tests prove non-lab/public targets cannot be touched.
5. Audit logging, timeout/rate limits, stop conditions, kill switch, and rollback/cleanup are documented.
6. Automation output is candidate-only and cannot auto-confirm findings.
7. Operator explicitly approves the exact activation command/scope.

## Phase 4A default first slice

Recommended next slice after this closeout:

Phase 4A.1 — Lab target selection and activation-boundary direction prompt.

Boundary for Phase 4A.1:

- planning/direction only;
- operator chooses a target class or asks Hermes to present options;
- no lab is touched;
- no `config/scope.txt` or real program scope is changed;
- no scanner/module execution;
- no target interaction.

Possible target classes to choose later:

- OWASP Juice Shop local instance;
- DVWA local instance;
- WebGoat local instance;
- PortSwigger Web Security Academy lab;
- HackTheBox / TryHackMe box with explicit scope;
- another user-owned intentionally vulnerable app.

## Final decision block

Decision: PASS_WITH_CONDITIONS / CLOSE_PHASE_3_OFFLINE_MVP
Tier: T1 milestone closeout documentation; future activation defaults T4/T5
Milestone: Phase 3 dry-run/local MVP
Hermes authority: direct for this documentation closeout; escalation-only for lab/live activation
Reviewers consulted:
- Hermes local synthesis from accepted P3.13, P3.14, P3.15, first-bounty readiness, Phase 4A plan, review-tiering policy, and multi-party review policy; visible model/runtime: gpt-5.5 / openai-codex
Validation performed:
- Documentation synthesis only in this closeout artifact. Final command validation should run `git diff --check` and `USER=${USER:-Owner} HACKLAB=<private-workspace> ./bin/hermes review` before commit/release bundling.
Blocking findings:
- None for closing Phase 3 as an offline/dry-run MVP checkpoint.
Non-blocking recommendations:
- Execute the local dry-run demo checklist and record results before any formal release bundle.
- Clean or intentionally preserve unrelated untracked artifacts before committing.
Safety boundary:
- No live scans, probes, scanner/module execution, target interaction, fuzzing, brute force, exploit attempts, callbacks/OAST, proxy/pivot/tunnel/transport behavior, external service calls, SIEM integration, report drafting/submission, platform adapter, credentials, loot-class data, scheduler/CI, deployment, billing, OAuth, production settings, `config/scope.txt` changes, lab target selection, or real program scope/rule activation were introduced.
OSS Recon Gate: not applicable for this docs-only closeout; required again for any future schema/contract/module/runner/reporting/external-tool boundary promotion.
User approval required: yes for any Phase 4A activation or target-touching step; no for this docs-only closeout.
