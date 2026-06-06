> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# P3.7 Direction Review Prompt — Return-to-Mainline / Program-Policy Dry-Run Boundary

Date: 2026-05-19
Requested by: Hermes / Operator
Reviewer route requested: Claude Code MAX/OAuth / Cowork direction review
Review type: design-only direction review
Expected output: `handoff/cowork_p3_7_direction_review.md`

## Context

This repository is an authorized cybersecurity lab building a bug-bounty automation platform with strict scope gates, default-deny program rules, and triage-only output. Phase 3 has intentionally stayed offline/local: it improved candidate-review fixture quality, module-runner observation tests, reviewer prompt catalogs, and periodic multi-party review artifacts without adding live target behavior, scanner execution, report drafting, schema promotion, or platform adapters.

Relevant predecessor decisions and artifacts:

- `.hermes.md` defines the binding security gate: active scan/exploit/brute force/callback/target-touching automation requires explicit authorization; `config/scope.txt` is operator-controlled; bug-bounty automation must eventually require both global scope and active program rules.
- `handoff/review_tiering_policy.md` defines T0-T5 review depth and escalation.
- `handoff/multi_party_review_decision_policy.md` defines role-separated implementation, safety/security, architecture/roadmap review, and Hermes synthesis.
- `handoff/oss_recon_gate.md` applies whenever a slice introduces or changes platform contracts, schemas, module/runner/reporting boundaries, or external-tool integrations.
- `handoff/cowork_p1_4_proposal.md` designed `recon.sh` consumption of `policy_decision/1.0` through a thin default-deny per-stage program policy wrapper.
- Phase 1 P1-4 through P1-6 were later implemented and accepted:
  - `recon.sh` applies global `safe_target` plus per-stage program policy gates before target-touching stages.
  - Policy evidence artifacts are recorded under `evidence/policy/`.
  - Allow artifacts are validated for path, request match, schema/status, source hashes, boundary audit event, decision target/technique/mode, and staleness before consumption.
  - `--allow-cidr` remains forced-deny for program policy runtime.
  - The policy boundary uses fixed repo paths and Python isolated mode to avoid helper/path/env forgery.
- Phase 2 then built a dry-run-only module runner and offline candidate-review chain. `scripts/module_runner.py` can build dry-run preview manifests and bind to policy artifacts, but it does not execute modules, import module code, or touch targets.
- P2.25 closed Phase 2 and named several future Phase 3 candidates, including per-program policy binding inside the candidate chain, but also locked `recon.sh` semantics and program policy boundary semantics behind explicit direction review.
- P3.6 deferred reviewer-notes artifacts and prioritized periodic multi-party review templates instead of adding a fifth consumer or new reviewer-notes schema.

## Current Decision Point

The candidate-review UX/fixture line has reached a reasonable pause point. The operator asked to continue the next reasonable slice after P3.6. Hermes' provisional recommendation is not to add another reviewer-note/schema/consumer artifact by default; instead, ask whether the project should return to the main platform line around program-policy dry-run / stage integration.

This P3.7 prompt is deliberately design-only. The reviewer should decide whether the next implementation slice should be a narrow offline/local planning or test slice around program-policy dry-run integration, or whether that would prematurely cross a runtime boundary.

## Question for P3.7

Should the project now return from Phase 3 candidate-chain UX work to a program-policy dry-run / mainline integration slice, and if so, what is the smallest safe implementation boundary?

Evaluate at least these options:

1. **CLOSE_PHASE_3_AND_RETURN_TO_PROGRAM_POLICY_MAINLINE**
   - Declare the P3.1-P3.6 candidate-chain / review-artifact line coherent enough to pause.
   - Recommend the next slice as a design-only or test-only mainline continuation around program-policy dry-run behavior.
   - Do not modify runtime code in this review.

2. **ADD_OFFLINE_POLICY_BINDING_FIXTURE_ONLY**
   - Add only offline fixture/test material proving that candidate/review artifacts can carry a program slug and policy artifact hash consistently.
   - No `recon.sh` changes, no scanner/module execution, no live target flags, no new stable schema, no external ingest.
   - If approved, state whether this is still Phase 3 or a bridge slice back to the Phase 1/2 platform line.

3. **PLAN_RECON_DRY_RUN_POLICY_STAGE_EXERCISE**
   - Prepare a future implementation task that exercises existing `recon.sh --dry-run --program <slug> --policy-mode planned|live` behavior against synthetic/local fixtures only.
   - Scope should be limited to tests/docs/handoff unless the reviewer explicitly justifies a tiny hardening change.
   - Must not change `config/scope.txt`, weaken `safe_target`, relax policy artifact validation, or add target-touching automation.

4. **PLAN_MODULE_RUNNER_POLICY_ARTIFACT_BRIDGE**
   - Prepare a future dry-run-only bridge where `module_runner.py` consumes already-validated policy artifacts produced by the existing policy boundary or committed fixtures.
   - No module execution, no scanner output ingest, no recon-to-runner automation, no new subprocess/network behavior.
   - If approved, identify exact artifact contracts and tests needed to prevent stale/forged policy decisions.

5. **CONTINUE_PHASE_3_OFFLINE_REVIEW_LINE**
   - Reject return-to-mainline for now and recommend another offline candidate-chain/review slice instead.
   - If chosen, explain why P3.6's re-trigger conditions do or do not apply, and avoid adding a fifth consumer or reviewer-notes schema unless explicitly justified.

6. **BLOCK_OR_DEFER**
   - Use this if the current state is too ambiguous or if any option would silently cross T4/T5 safety boundaries without operator activation approval.

## Required Review Dimensions

Please structure the review as a multi-party-compatible direction review:

1. Review tier and milestone boundary.
2. Decision: APPROVE / APPROVE_WITH_CHANGES / DEFER / BLOCK.
3. Preferred option from the list above, with rationale.
4. Safety boundary:
   - What remains offline/local.
   - What is forbidden without fresh operator approval.
   - Whether the next implementation slice is T3, T4, or T5.
5. OSS Recon Gate notes:
   - Compare a small set of mature references relevant to policy/stage/runner gating, such as Nuclei workflow/template gating, OWASP ZAP context/policy concepts, DefectDojo engagement/test scoping, SARIF run/result provenance, and CI security-scan dry-run patterns.
   - For each, state adopt / adapt / ignore.
   - Do not copy target-touching defaults, importer/exporter behavior, confirmed/verified lifecycle vocabulary, submission workflows, or platform adapter semantics.
6. Existing Phase 1/P1-6 status check:
   - Is the current `recon.sh` policy gate mature enough to build tests/docs around, or should a hardening review happen first?
   - Are there known unresolved risks around stale allow artifacts, program/global hash validation, target/mode/technique mismatch, CIDR denial, or Python boundary execution?
7. Phase 2/3 boundary check:
   - Does the proposed next slice touch the P2.24 helper-extraction triggers?
   - Does it add a fifth stdin consumer, third file-reading consumer, schema promotion, shared helper extraction, scanner-output ingest, or report/submission surface?
8. Minimal implementation boundary if proceeding:
   - Exact files/directories allowed to change.
   - Exact files/directories forbidden to change.
   - Required tests/safety assertions.
   - Whether a named artifact and rolling handoff file are both required.
9. Multi-party review fit:
   - Which roles must review implementation vs safety vs architecture before Hermes accepts?
   - Is Hermes direct-authority, conditional-authority, or escalation-only under `handoff/multi_party_review_decision_policy.md`?
10. Final recommendation for the next worker task, if any.

## Hard Safety Constraints

The review is design-only. Do not implement code. Do not run scanners. Do not touch targets. Do not invoke recon stages against real hosts. Do not modify runtime scripts, schemas, configs, scope files, modules, runners, reports, credentials, scheduler, deployment, billing, repo settings, or production settings.

The reviewed implementation scope, if any, must remain offline/local unless the operator later gives explicit written approval for a narrower T4/T5 activation. This review must not authorize:

- active scan, exploit, fuzz, brute force, callback, OAST, proxy, pivot, tunnel, beacon, relay, reverse listener, or target-touching behavior;
- weakening or bypassing `safe_target`, `config/scope.txt`, `--skip-scope-check` confirmation, program policy gates, or policy artifact validation;
- changing `config/scope.txt` or real program scope/rules;
- accepting stale/forged policy decisions or cached allows;
- module execution, scanner execution, external-source/scanner-output ingest, or report drafting/submission;
- platform adapters/importers/exporters;
- lifecycle promotion to `confirmed`, `verified`, `valid`, `reportable`, `accepted`, `resolved`, or bounty/submission vocabulary;
- new live-target CLI affordances such as `--target`, `--url`, `--host`, `--scope`, or `--live` in any offline consumer;
- scheduler, CI auto-execution against targets, deployment, billing, OAuth, credentials, secrets, or repo-setting changes.

## Output Requirements

Write the review to `handoff/cowork_p3_7_direction_review.md`.

The review must include:

```text
Review tier: T0/T1/T2/T3/T4/T5
Milestone:
Decision: APPROVE / APPROVE_WITH_CHANGES / DEFER / BLOCK
Preferred option:
Safety boundary:
OSS Recon Gate: not applicable / attached / required before implementation
Existing P1/P1-6 status assessment:
Phase 2/3 boundary assessment:
Blocking issues:
Non-blocking improvements:
Codex/Claude implementation scope:
Required tests/safety assertions:
Out-of-scope/deferred items:
P2.24 trigger assessment:
Reviewer route/tool and visible model/runtime:
```

Also include a final decision block compatible with `handoff/multi_party_review_decision_policy.md`:

```text
Decision: PASS / PASS_WITH_CONDITIONS / REQUEST_CHANGES / DEFER / ESCALATE_TO_OPERATOR
Tier: T0/T1/T2/T3/T4/T5
Milestone:
Hermes authority: direct / conditional / escalation-only
Reviewers consulted:
- <route/tool>; visible model/runtime: <model if exposed, otherwise limitation>
Validation performed:
Blocking findings:
Non-blocking recommendations:
Safety boundary:
OSS Recon Gate: not applicable / attached / required before implementation
User approval required: yes/no; reason:
Accepted changes updated: yes/no/not applicable
Next action:
```
