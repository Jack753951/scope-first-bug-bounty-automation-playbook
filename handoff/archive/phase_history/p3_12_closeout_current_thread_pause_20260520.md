> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# P3.12 Closeout / SOC Calibration Thread Pause

Status: accepted checkpoint
Source: Hermes synthesis of P3.12 direction review, implementation result, independent implementation/safety review, and local validation
Date: 2026-05-20
Repo truth: `handoff/accepted_changes.md`, `handoff/active_strategy_queue.md`, `handoff/cowork_soc_reviewer_gap_catalog_direction_review.md`, `handoff/claude_code_result_p3_12.md`, `handoff/third_party_p3_12_implementation_review.md`, `fixtures/soc_evidence_bucket/reviewer_gap_catalog.{md,json}`, `scripts/test_soc_reviewer_gap_catalog.py`

## Reviewer identity

- Reviewer route/tool: Hermes local synthesis + repository validation
- Visible runtime model: gpt-5.5 / openai-codex
- Provider / CLI version if visible: provider visible as openai-codex from session metadata; lower-level deployment details not exposed
- Review focus: milestone closeout, safety boundary, current-priority routing
- Limitation: this checkpoint did not request a new independent subagent review because P3.12 already has a fresh implementation/safety review at `handoff/third_party_p3_12_implementation_review.md`

## Purpose

This checkpoint closes the immediate SOC calibration mini-thread created by P3.11 and P3.12, then routes the project back toward the main authorized bug-bounty platform track.

It is a planning/handoff artifact only. It does not approve a SOC trial consumer, runtime consumer, schema promotion, SIEM integration, report gate, scanner/module execution, target-touching automation, scope/config change, credentials, scheduler/CI, deployment, billing, OAuth, or production setting change.

## Inputs inspected

- `handoff/active_strategy_queue.md`
- `handoff/accepted_changes.md`
- `handoff/cowork_soc_reviewer_gap_catalog_direction_review.md`
- `handoff/claude_code_result_p3_12.md`
- `handoff/third_party_p3_12_implementation_review.md`
- `fixtures/soc_evidence_bucket/reviewer_gap_catalog.md`
- `fixtures/soc_evidence_bucket/reviewer_gap_catalog.json`
- `scripts/test_soc_reviewer_gap_catalog.py`
- `scripts/test_soc_evidence_bucket_fixture.py`
- Current git status and Hermes local review output

## Current P3.11/P3.12 state

P3.11 and P3.12 form a coherent offline calibration pair:

1. P3.11 added a synthetic SOC evidence-bucket fixture and local test coverage for reviewer-aligned evidence completeness.
2. P3.12 added a static companion reviewer-gap catalog and local test coverage tying its vocabulary/status posture exactly to the P3.11 fixture source.
3. Independent review initially found a real P3.12 blocker: asymmetric drift-lock coverage. Hermes fixed it with AST-based exact set equality against the P3.11 source constants, then follow-up review passed.

The accepted boundary remains narrow: static fixture/catalog/docs/tests/handoff only. The catalog is synthetic, trial, non-contractual, non-promotional, and unwired from runtime/schema/report paths.

## Tier classification

- This closeout checkpoint tier: T1 planning/handoff only.
- P3.11 accepted implementation tier: T2 offline fixture/docs/test only.
- P3.12 accepted implementation tier: T2 offline static catalog/docs/test only.
- Future SOC trial-consumer design tier: T3 minimum because it would introduce a new consumer/boundary around reviewer feedback normalization.
- Future SOC runtime/report/SIEM/platform activation tier: T4/T5 depending on target interaction, report/submission, credentials, scheduler, deployment, or production persistence.

## Safety boundary

In scope for this checkpoint:

- close the P3.11/P3.12 SOC calibration mini-thread;
- preserve the accepted safety boundary;
- route next work back to platform mainline;
- update handoff/navigation artifacts.

Out of scope / still blocked:

- SOC trial consumer implementation;
- reviewer-answer capture artifact;
- schema promotion for `soc_reviewer_gap_catalog_v0_trial` or any current trial document;
- SIEM, Elastic, Kibana, Splunk, scanner, module, recon runtime, report-readiness gate, report generator, or platform adapter integration;
- live target behavior, scanner/module execution, fuzzing, brute force, exploit attempts, callbacks/OAST, proxy/pivot/tunnel/beacon/relay behavior;
- `config/scope.txt` changes or real program scope/rule activation;
- credentials/OAuth/tokens/private keys, loot-class data, scheduler/CI, deployment, billing, or production settings.

## OSS Recon Gate posture

Not applicable for this checkpoint because it introduces no platform contract, schema, importer/exporter, runtime boundary, scanner integration, or report adapter.

Required before future SOC trial-consumer or report/runtime integration: yes. Any new consumer or promoted contract must run a fresh T3+ direction review and compare mature patterns for feedback normalization, auditability, evidence provenance, and non-promotional report readiness without copying unsafe target-touching defaults.

## Decision

Decision: PASS_WITH_CONDITIONS.

P3.11/P3.12 are accepted and the SOC calibration thread should pause here. The next default lane should return to mainline platform governance: module risk-tier / active-testing policy follow-up as policy/docs-only work.

Rationale:

- P3.11/P3.12 now capture the useful SOC lesson without creating runtime obligations.
- Extending SOC work into a trial consumer would cross a new consumer/contract boundary and should not be the default without a fresh T3 direction review.
- Module risk-tier / active-testing policy is closer to the long-term authorized bug-bounty platform path and can be advanced safely as docs/policy only before any manifest/runner implementation.

## Candidate next lane: P3.13 module risk-tier / active-testing policy follow-up

Goal: refine how modules, techniques, execution modes, and review tiers should be described before future module manifests or runner validators add explicit risk-tier fields.

Allowed output for the next slice:

- direction/checkpoint prompt or policy-doc update under `handoff/`;
- no code/runtime behavior changes unless a later reviewed T3/T4 slice explicitly authorizes manifest/validator implementation;
- no scanner/module execution;
- no live target behavior;
- no `config/scope.txt` or real program scope/rule changes.

Minimum questions for the next policy follow-up:

1. What module risk-tier vocabulary should the platform use for passive, active-safe, active-intrusive, exploit-adjacent, DoS-risk, credential-sensitive, callback/OAST, and authenticated techniques?
2. How should risk tier map to review depth, required authorization evidence, program-rule compatibility, execution mode, and human-in-loop gates?
3. Which fields belong in a future module manifest/profile contract, and which should remain policy prose for now?
4. Which future implementation steps are T3, T4, or T5 and therefore blocked until fresh review and/or explicit operator approval?
5. How should the policy avoid banning legitimate authorized testing while still failing closed for ambiguous scope/rules?

## Final Decision Block

Decision: PASS_WITH_CONDITIONS
Tier: T1 for this checkpoint; future SOC consumer is T3 minimum; future live/report/runtime activation is T4/T5
Milestone: P3.12 closeout / SOC calibration thread pause
Hermes authority: direct for this planning artifact; conditional/escalation-only for future runtime or activation work according to tier
Reviewers consulted:
- Hermes local synthesis; visible model/runtime: gpt-5.5 / openai-codex; limitation: lower-level runtime details not exposed
- P3.12 Cowork direction review: `handoff/cowork_soc_reviewer_gap_catalog_direction_review.md`
- P3.12 independent implementation/safety review: `handoff/third_party_p3_12_implementation_review.md`; reviewer route/tool: Hermes `delegate_task` subagent; visible model/runtime reported there as `gpt-5.5 / openai-codex` with lower-level runtime not exposed
Validation performed:
- inspected current queue, P3.12 artifacts, review records, and git status;
- relied on completed P3.12 validation recorded in `handoff/claude_code_result_p3_12.md` and `handoff/third_party_p3_12_implementation_review.md`;
- `HACKLAB=$(pwd) ./bin/hermes review` passed before this checkpoint with Python compile OK for 78 files, shell scripts OK, lock clear, and 12 scope entries;
- this checkpoint itself changes handoff/planning only
Blocking findings: none for planning/handoff closeout
Non-blocking recommendations:
- leave SOC trial-consumer design deferred behind fresh T3 review;
- proceed next with P3.13 module risk-tier / active-testing policy follow-up as docs/policy only;
- split future Claude Code tasks more narrowly when they include fixture + test + handoff + review obligations
Safety boundary:
- no runtime consumer, schema promotion, SIEM/report/platform integration, live target, scanner/module execution, scope/config, credentials/loot, scheduler/CI, deployment, billing, OAuth, or production surface approved
OSS Recon Gate: not applicable for this checkpoint; required before future consumer/contract/runtime/report integration
User approval required: no for this planning artifact; yes before any T4/T5 activation or scope/config/target-touching behavior
