> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# P3.5 Direction Review Prompt — Report-Readiness Reviewer Prompts Without Drafting

Date: 2026-05-19
Requester: Hermes
Reviewer route requested: Claude/Cowork via local `hermes cowork` or Claude Code MAX/OAuth-compatible route. Record the route/tool used and any visible runtime/model information; if exact model is not exposed, state that limitation.
Review tier: T3 direction review + OSS Recon Gate, design-only
Milestone: Phase 3 candidate next slice after P3.1 curated fixtures, P3.2 terminal-state matrix, P3.3 two-module runner discovery coverage, and P3.4-alt runner-indifference coverage.

## Goal

Decide whether the next Phase 3 slice should add a strictly offline, data-only reviewer-prompt artifact for `report_readiness_gate/0.1-trial` outputs, without report drafting, submission adapters, platform adapters, runtime wiring, schema promotion, network access, or target-touching behavior.

This prompt intentionally reopens the Phase 3 priority recommendation from `handoff/cowork_p2_25_closeout_review.md` lines 309-329, but with updated context: the module-count / manifest-only concerns were resolved as P3.3 and P3.4-alt tests/docs-only slices, not by adding a new module.

## Current State Summary

Completed Phase 3 slices:

- P3.1: curated near-real offline fixture set, fully synthetic/redacted, stressing candidate -> gap -> verification -> readiness states.
- P3.2: curated fixture terminal-state expectation matrix.
- P3.3: tests proving two committed Level 1 modules are selected by the runner under `audit-baseline` without changing modules/profile/schema/runtime.
- P3.4-alt: tests proving `module_runner.py` is indifferent to `check.py` presence/absence and does not import or condition on evaluator files.

Relevant existing workflow scripts:

- `scripts/build_candidate_review_packet.py`
- `scripts/review_candidate_packet_gaps.py`
- `scripts/build_candidate_verification_plan.py`
- `scripts/build_report_readiness_gate.py`
- `scripts/build_candidate_workflow_fixture.py`

Relevant current trial document shapes:

- `candidate_review_packet/0.1-trial`
- `candidate_review_gap_report/0.1-trial`
- `candidate_verification_plan/0.1-trial`
- `report_readiness_gate/0.1-trial`
- `candidate_workflow_fixture/0.1-trial`

The current chain remains non-promotional. It may emit states such as `blocked`, `not_ready`, `reviewer_decision_required`, and `needs_manual_review`, but must not emit `confirmed`, `verified`, `ready_for_submission`, or report-submission language.

## Proposed Slice

Working name: P3.5 report-readiness reviewer prompts without drafting.

Potential implementation shape for reviewer to evaluate:

1. Add a static data catalog of reviewer prompt templates keyed only by existing report-readiness gate action / gap codes.
   - Suggested path if approved: `templates/report_readiness_reviewer_prompts.json` or `templates/report_readiness_reviewer_prompts.yaml`.
   - Data-only; no executable code; no network references; no platform/vendor API fields.
   - Prompts should ask a reviewer to check evidence sufficiency, manual verification needs, scope ambiguity, duplicate/chain relationship, remediation clarity, and whether the candidate should stay blocked/not-ready/needs-review.
   - Prompts must not draft vulnerability report prose, titles, summaries, impact narratives, reproduction steps, or submission text.

2. Add a trial-only structured reviewer-notes artifact shape, if and only if the review concludes it is justified.
   - Suggested schema label: `reviewer_notes/0.1-trial` or `report_readiness_reviewer_notes/0.1-trial`.
   - Keep it local/trial-only; do not promote under `modules/_schema/**` unless the review explicitly says a schema file is necessary, which is not preferred for this slice.
   - It should attach reviewer answers to stable finding IDs and gate-action codes.
   - Allowed states must stay non-promotional; e.g. `blocked`, `not_ready`, `needs_manual_review`, `defer`, `needs_more_evidence` if such new vocabulary is explicitly approved.
   - It must not include `confirmed`, `verified`, `valid`, `ready_for_submission`, `accepted`, `duplicate_confirmed`, or platform lifecycle vocabulary.

3. Prefer a tests/docs/data-only implementation if approved.
   - No new stdin-only consumer unless the reviewer decides the benefit outweighs triggering the P2.24 duplication/revisit concern.
   - No fifth `_compact_emit` clone should be added casually.
   - If any code is proposed, explain why a data-only catalog plus tests is insufficient and whether P2.24 refactor revisit is triggered.

## Review Questions

Please answer these explicitly:

1. Should P3.5 proceed now, defer, or be replaced by a smaller slice?
2. Is a static prompt catalog enough, or is a trial reviewer-notes artifact justified in this slice?
3. If a reviewer-notes artifact is justified, should it remain fixture-only/data-only or does it need a validator/consumer? What is the minimum safe boundary?
4. Does adding reviewer prompts or reviewer notes trigger P2.24 core-helper extraction revisit? Why or why not?
5. What exact files may be written in the implementation slice?
6. What exact files are forbidden?
7. What tests / static checks are required?
8. What non-promotional vocabulary is allowed, and what vocabulary must be explicitly rejected?
9. What should be deferred to a later slice?
10. What independent implementation review is required before acceptance?

## OSS Recon Gate Required

Run a design-only OSS / ecosystem comparison before approving any shape. Compare at least:

- <bug-bounty-platform> public report / disclosure structures
- Bugcrowd disclosure / VRT-style triage language
- DefectDojo finding lifecycle and importer states
- SARIF result / suppression / baseline / review concepts
- OWASP ASVS / WSTG reviewer checklist style

For each reference, record adopt / adapt / ignore decisions. Explicitly reject:

- platform submission workflows
- target-touching defaults
- scanner importers
- confirmed/verified status promotion
- report drafting prose generation
- DefectDojo lifecycle vocabulary unless explicitly mapped to a non-promotional local term
- SARIF result levels if they would be confused with finding validation

## Safety Boundary

This direction review is design-only. It must not:

- run live scans, probes, fuzzers, exploit tooling, callbacks, OAST, proxy/pivot/transport, or target-touching automation
- import, vendor, or invoke third-party scanner/platform code
- modify `config/scope.txt`, `config/recon.conf`, `recon.sh`, scope logic, program policy boundary, module runner runtime, schemas, manifests, profiles, loot, scans, reports, credentials, OAuth, scheduler, deployment, billing, or production settings
- promote any `*/0.1-trial` schema
- draft or submit reports
- add network clients, subprocess invocation, scanner importers, platform adapters, webhooks, notifications, or persistent automation

## Candidate Allowed Implementation Files if Approved

The reviewer may adjust this list:

- `templates/report_readiness_reviewer_prompts.json` or `.yaml`
- `tests/fixtures/report_readiness_reviewer_prompts/**` if fixtures are needed
- `scripts/test_report_readiness_gate.py` or a new test file that validates prompt coverage as data only
- `scripts/README.md` with a short note only
- `handoff/accepted_changes.md` append-only summary
- `handoff/third_party_p3_5_implementation_review.md` after implementation review

## Candidate Forbidden Implementation Files

Unless the reviewer explicitly routes back with a higher-tier design:

- `config/scope.txt`
- `config/recon.conf`
- `recon.sh`
- `scripts/module_runner.py`
- `scripts/program_policy_boundary.py`
- all `scripts/build_*` and `scripts/review_*` workflow consumers listed above
- `modules/_schema/**`
- `modules/checks/**`
- `modules/profiles/**`
- `loot/**`, `scans/**`, `reports/**`, `runs/**`
- `.env`, credentials, OAuth, scheduler, deployment, billing, production settings

## Expected Review Output Template

Use this structure:

```text
# P3.5 Direction Review — Report-Readiness Reviewer Prompts

Date:
Reviewer route/tool:
Visible model/runtime model:
Review tier:
Milestone:
Decision: APPROVE / APPROVE_WITH_CHANGES / DEFER / BLOCK

## Executive Summary

## OSS Recon Gate Notes
- <bug-bounty-platform>:
- Bugcrowd:
- DefectDojo:
- SARIF:
- OWASP ASVS/WSTG:
- Net decision:

## Approved / Deferred Scope

## Allowed Files

## Forbidden Files

## Required Tests / Validation

## P2.24 Refactor Revisit Assessment

## Non-Promotional Vocabulary Rules

## Blocking Issues

## Non-Blocking Recommendations

## Safety Boundary Confirmation
```
