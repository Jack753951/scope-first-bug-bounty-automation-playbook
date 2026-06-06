> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# First-Bounty Readiness Checkpoint — Dry-Run/Local MVP Gap List

Status: planning checkpoint
Date: 2026-05-20
Prepared by: Hermes
Scope: planning only; no target-touching, no scope activation, no live execution

## Purpose

The operator asked to pursue both next paths:

1. a T3+ direction review for possible module manifest/profile field promotion; and
2. a first-bounty readiness checkpoint.

This checkpoint answers what the project can do now, what still blocks a controlled lab beta and a first authorized bug-bounty private beta, and what should stay out of Phase 3.

## Current capability summary

The platform is strong in offline/dry-run governance:

- Global scope whitelist exists at `config/scope.txt`.
- Program policy/rule concepts exist and have dry-run tests around allow/deny behavior.
- Module manifest/profile schemas and conservative validators exist.
- Module runner can perform dry-run planning/previews without module execution.
- Run, finding, evidence, module I/O, preview manifest, and preview ledger contracts exist for offline validation.
- Recon-to-runner policy artifact bridge has explicit direct-read/dry-run coverage, but no auto-discovery or live coupling.
- Evidence/reviewer-readiness calibration exists through candidate packets, report-readiness prompts, SOC evidence-bucket fixtures, and reviewer-gap catalog.
- Multi-party review policies and active-testing risk tiers exist.

This is enough for a local dry-run demo and further contract hardening. It is not enough for autonomous live bug-bounty testing.

## Current launch-readiness level

| Launch level | Current status | Meaning |
|---|---|---|
| Dry-run/local MVP | Near, but still needs closeout/gap review | Can demonstrate deterministic local policy/module/report-readiness flow without target-touching |
| Phase 4A controlled lab semi-automated calibration | Not started; now explicitly inserted after Phase 3 closeout | Needs explicit local lab/intentionally vulnerable app/CTF-training scope, T4/T5 direction review, deny-by-default runtime tests, rate/kill controls, audit logs, candidate-only outputs |
| Controlled lab beta / lab-to-report trial | Not ready | Follows Phase 4A; needs manual verification loop, evidence packet, false-positive review, report-readiness gate, and no external submission |
| Authorized bug-bounty private beta | Not ready | Needs real program scope/rules, manual activation workflow, evidence redaction/report draft gates, operator approval record |
| Production-like multi-program platform | Not ready | Needs durable store, onboarding, monitoring, adapters, CI/ops controls, rollback, stronger docs |

## Remaining gates to first private beta

### Gate B/C closeout — Dry-run/local MVP confidence

Status: partially complete.

Remaining work:

1. Decide P3.14 field-promotion direction: promote narrow manifest/profile fields, defer, or docs-only mapping.
2. Close Phase 3 with a dry-run/local MVP review packet.
3. Clean or intentionally preserve untracked test/temp artifacts.
4. Produce one operator-facing dry-run demo command sequence showing policy artifact → module runner preview → validation → reviewer-readiness artifact, using only synthetic/local data.

Success condition:

- Hermes can run a deterministic local demo that never touches a target and produces only candidate/preview artifacts.

### Gate D — Evidence and report-draft readiness

Status: partially designed, not private-beta ready.

Remaining work:

1. Real evidence locator/redaction gate design.
2. Candidate finding to report-draft boundary, without auto-`confirmed` promotion.
3. Human verification checklist tied to evidence artifacts.
4. Report-draft quality gate that requires manual/agent verification before any submission wording.

Success condition:

- Scanner/module output, when eventually imported, remains triage-only and cannot become confirmed/report-ready without verification.

### Gate E — Phase 4A controlled lab semi-automated calibration

Status: not started; explicitly inserted after Phase 3 closeout and before any real bug-bounty private beta. See `handoff/phase4a_controlled_lab_calibration_plan_20260520.md`.

Required before any lab live execution:

1. Operator selects local lab, intentionally vulnerable app, or explicit CTF/training target.
2. Scope/rules are recorded narrowly for that lab.
3. T4/T5 direction review approves a live-mode lab boundary.
4. Runtime tests prove public targets cannot be touched accidentally.
5. Rate limits, kill switch, audit logging, stop conditions, and candidate-only output rules exist.
6. Operator explicitly approves the exact activation.

Success condition:

- The platform can touch only the named lab target, with deny-by-default controls, audit evidence, candidate-only findings, human verification checkpoints, and report-readiness observations.

### Gate E2 — Phase 4B lab-to-report workflow trial

Status: not started; should follow Phase 4A calibration.

Required before any real program private beta:

1. Select 1-2 lab candidate findings produced under Phase 4A controls.
2. Manually verify or reject them.
3. Build evidence packets with redaction and integrity checks.
4. Draft impact/remediation/retest notes as lab-only report-readiness artifacts.
5. Confirm no report submission path or automatic confirmed-finding promotion exists.

Success condition:

- The lab workflow can move from candidate signal to human-reviewed evidence/report readiness without touching a real bug-bounty target or submitting anything externally.

### Gate F — Phase 4C one-program bug-bounty private-beta planning

Status: not started.

Required before any real program run:

1. Operator selects a real program and provides explicit scope/rules.
2. Program scope file and rule interpretation are reviewed manually.
3. Live-capable technique set is constrained to low-risk/passive or explicitly allowed methods.
4. Manual activation checklist exists.
5. Evidence redaction and report-draft review gate exists.
6. Rollback/stop/incident procedure exists.
7. No scheduler/CI target-touching automation at first.

Success condition:

- One manually activated, explicitly scoped, low-risk private beta workflow can produce candidate findings and report drafts only after human verification.

## Recommended Phase 3 exit line and Phase 4A insertion

Keep Phase 3 offline. Do not make controlled lab activation part of Phase 3.

Phase 3 should end after:

1. P3.14 direction review decides future field promotion / deferral.
2. Dry-run/local MVP gap list is accepted.
3. Active strategy queue names Phase 4A as controlled lab semi-automated calibration preparation, not real bug-bounty activation by default.
4. The repo has a clean-enough acceptance bundle or at least a documented dirty-worktree inventory.

After Phase 3 closeout, Phase 4A should calibrate semi-automated workflow and scripts on an explicit authorized lab before Phase 4B lab-to-report trial and Phase 4C real-program private-beta planning.

## Approximate remaining phase count

If Phase 3 remains offline:

- P3.14: field-promotion direction review.
- P3.15: dry-run/local MVP demo/readiness checkpoint.
- P3.16: optional narrow implementation or explicit deferral based on P3.14.
- P3.17: Phase 3 closeout and Phase 4 entry criteria.

Estimated remaining Phase 3: **3-5 stages**.

If lab live activation is included in Phase 3, add at least **3-5 more stages**, and the phase becomes much riskier. Recommendation: do not do that.

## Next actions created by this checkpoint

1. Run Cowork direction review using `handoff/cowork_p3_14_module_field_promotion_direction_prompt.md`.
2. After P3.14 review, create either:
   - a narrow implementation task for approved field/schema/doc changes, or
   - a deferral/closeout checkpoint if field promotion is not yet worth it.
3. Prepare a dry-run/local MVP demo plan using only synthetic/local data.

## Safety boundary

This checkpoint is planning only.

No live scans, probes, scanner/module execution, target interaction, fuzzing, brute force, exploit attempts, callbacks/OAST, proxy/pivot/tunnel/transport behavior, external service calls, SIEM integration, report drafting/submission, platform adapter, credentials, loot-class data, scheduler/CI, deployment, billing, OAuth, production settings, `config/scope.txt` changes, or real program scope/rule activation were introduced.
