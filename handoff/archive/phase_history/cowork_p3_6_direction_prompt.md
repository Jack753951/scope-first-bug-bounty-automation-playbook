> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# P3.6 Direction Review Prompt — Reviewer Notes Artifact / Multi-Party Review Output Boundary

Date: 2026-05-19
Requested by: Hermes / Operator
Reviewer route requested: Claude Code MAX/OAuth / Cowork direction review
Review type: design-only direction review
Expected output: `handoff/cowork_p3_6_direction_review.md`

## Context

This cybersec lab is building an authorized bug-bounty automation platform with strict offline-first, scope-gated, triage-only workflow boundaries. The current Phase 3 line has been intentionally validating the candidate-finding -> review -> verification -> report-readiness workflow without adding live target behavior, scanner/runtime wiring, report drafting, or schema promotion.

Relevant predecessor decisions:

- `handoff/review_tiering_policy.md` defines T0-T5 review tiers and escalation triggers.
- `handoff/multi_party_review_decision_policy.md` defines role-separated implementation, safety/security, architecture/roadmap review, and Hermes final synthesis.
- `handoff/oss_recon_gate.md` is required for T3+ platform/contract/reporting/tool boundaries.
- `handoff/cowork_p2_24_direction_review.md` deferred shared offline-consumer helper extraction until a real trigger appears, such as:
  - a fifth stdin/stdout consumer joining the chain,
  - a second file-reading consumer,
  - schema promotion to `modules/_schema/**`,
  - observable drift requiring centralization.
- `handoff/cowork_p3_5_direction_review.md` approved only a static reviewer-prompt catalog and explicitly deferred any reviewer-notes artifact or consumer to a future direction review, provisionally P3.6.
- `handoff/third_party_p3_5_implementation_review.md` repeated that a reviewer-notes consumer would fire the P2.24 fifth-consumer trigger and must be reviewed before implementation.
- Current catalog: `templates/report_readiness_reviewer_prompts.json`, data-only, flat marker, not a `*/0.1-trial` schema, not read by chain consumers.

## Question for P3.6

Should the project now introduce any reviewer-notes artifact / reviewer-answer capture boundary, or should it defer that and instead consolidate periodic multi-party review artifacts first?

Evaluate at least these options:

1. **DEFER reviewer-notes artifact** and instead tighten periodic multi-party review/status artifacts under `handoff/periodic_reviews/YYYY-MM-DD/` so scheduled reviews follow `multi_party_review_decision_policy.md` without adding a new chain consumer or schema.
2. **Data-only reviewer-notes fixture/artifact sketch** with no consumer, no schema under `modules/_schema/**`, and no runtime wiring. If you approve this, explain what makes it testable and worthwhile despite having no consumer.
3. **Consumer-backed reviewer-notes artifact** that reads existing `report_readiness_gate/0.1-trial` output and/or the P3.5 prompt catalog and emits reviewer notes. If you approve this, explicitly decide whether it triggers P2.24 helper extraction first or in the same slice.
4. **Core offline-consumer helper extraction first** before any reviewer-notes consumer, following the minimal surface described in `handoff/cowork_p2_24_direction_review.md` lines 178-220.
5. **Schema/contract promotion** for reviewer notes. This should be assumed high-friction and likely premature unless you identify a clear need.

## Required Review Dimensions

Please structure the review as a multi-party-compatible direction review:

1. Review tier and milestone boundary.
2. Decision: APPROVE / APPROVE_WITH_CHANGES / DEFER / BLOCK.
3. Safety boundary: what must remain offline/local and what is forbidden.
4. OSS Recon Gate notes:
   - Compare a small set of mature formats/workflows such as SARIF suppressions/reviews, DefectDojo notes/lifecycle, <bug-bounty-platform>/Bugcrowd triage comments, OWASP checklist evidence notes, and project-internal periodic review artifacts.
   - For each, state adopt / adapt / ignore.
   - Do not copy platform lifecycle, submission, severity, bounty, confirmed/verified, or importer/exporter vocabulary into this project unless explicitly justified and still below confirmation semantics.
5. P2.24 trigger assessment:
   - Does each option trigger fifth stdin consumer, second file-reading consumer, schema promotion, helper extraction, or centralization risk?
   - If a trigger fires, name the required prerequisite review/implementation boundary.
6. Multi-party review fit:
   - How should future scheduled review artifacts show implementation/safety/architecture reviewer status without exaggerating evidence?
   - Should P3.6 prioritize improving `handoff/periodic_reviews/YYYY-MM-DD/` output templates instead of adding reviewer notes to the candidate chain?
7. Approved / deferred / forbidden scope.
8. Required tests/validation if implementation proceeds.
9. Final recommendation for next implementation slice, if any.

## Hard Safety Constraints

The review is design-only. Do not implement code. Do not modify runtime scripts. Do not run scanners. Do not touch targets. Do not modify `config/scope.txt`, `recon.sh`, `modules/_schema/**`, `modules/checks/**`, `modules/profiles/**`, `runs/**`, `loot/**`, `scans/**`, `reports/**`, credentials, OAuth, scheduler, deployment, billing, repo settings, or production settings.

The reviewed implementation scope, if any, must remain offline/local and must not add:

- active scan / exploit / fuzz / brute force / callback / proxy / pivot / transport behavior,
- target-touching automation,
- scanner/module execution,
- report drafting or submission,
- platform adapter/importer/exporter,
- lifecycle promotion to confirmed/verified/valid/reportable/accepted/resolved,
- any live-target CLI affordance such as `--target`, `--url`, `--host`, `--scope`, or `--live`.

## Output Requirements

Write the review to `handoff/cowork_p3_6_direction_review.md`.

The review must include:

```text
Review tier: T0/T1/T2/T3/T4/T5
Milestone:
Decision: APPROVE / APPROVE_WITH_CHANGES / DEFER / BLOCK
Safety boundary:
OSS Recon Gate: not applicable / attached / required before implementation
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
