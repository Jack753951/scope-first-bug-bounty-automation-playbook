> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# P3.1 Direction Review Prompt — Curated Near-Real Offline Fixture Set

Date: 2026-05-19
Owner: Hermes
Requested reviewer: Claude/Cowork via Claude Code MAX/OAuth
Review tier: T3 direction review + OSS Recon Gate, design-only
Milestone: Phase 3 start after Phase 2 closeout

## Context

P2.25 closed Phase 2 with verdict `CLOSE_PHASE_2` and recommended first Phase 3 slice:

```text
P3.1 Curated near-real offline fixture set
```

Relevant closeout files:

```text
handoff/cowork_p2_25_closeout_review.md
handoff/cowork_p2_24_direction_review.md
```

Phase 2 candidate chain is trial-only and offline/local:

```text
P2.19 scripts/build_candidate_review_packet.py
  -> candidate_review_packet/0.1-trial
P2.20 scripts/review_candidate_packet_gaps.py
  -> candidate_review_gap_report/0.1-trial
P2.21 scripts/build_candidate_verification_plan.py
  -> candidate_verification_plan/0.1-trial
P2.22 scripts/build_report_readiness_gate.py
  -> report_readiness_gate/0.1-trial
P2.23 scripts/build_candidate_workflow_fixture.py
  -> candidate_workflow_fixture/0.1-trial
```

## Requested review

Before implementation, perform a third-party design review and OSS Recon Gate for P3.1.

Decide whether the proposed P3.1 slice should proceed, and if so define a narrow implementation boundary that Hermes can hand to Claude Code Impl / Codex.

## Proposed P3.1 goal

Add a small curated set of fully offline, synthetic/redacted, near-real bug-bounty-shaped finding fixtures that stress the existing P2.19-P2.23 chain without changing chain behavior.

Target fixture count: 4-8 cases.

Suggested fixture root:

```text
tests/fixtures/candidate_review_packet/p3_1_curated_<case_slug>/expected_findings.json
```

Candidate stress cases:

1. partial / messy evidence;
2. ambiguous scope signal in text fields only, without invoking scope runtime;
3. chained-precondition finding;
4. low-severity / informational signal that should remain not-ready / blocked;
5. duplicate / near-duplicate candidates from synthetic sources;
6. conflicting source records;
7. non-finding / control case that should stay below reportability.

## Required review questions

1. Should P3.1 proceed as the first Phase 3 slice?
2. Are 4-8 committed fixture cases the right boundary, or should the slice be smaller?
3. Which fixture case types are most useful now?
4. Should P3.1 be allowed to modify implementation scripts, or should it be fixture/tests/docs only?
5. How should deterministic output and non-promotional vocabulary be asserted?
6. What should count as a blocker during implementation review?
7. Which OSS patterns should be adapted or rejected?

## OSS Recon Gate

Compare against public/mature finding-shape patterns without copying target-touching defaults. Include adopt/adapt/ignore decisions for at least:

- <bug-bounty-platform> / Bugcrowd public report shape concepts: title, impact, steps, affected asset, evidence, remediation, duplicate state;
- DefectDojo finding lifecycle / dedupe concepts;
- SARIF result shape / levels;
- Nuclei template findings or scanner JSON conventions;
- OWASP ZAP alert fields.

Important: reject anything that implies live scanning, scanner importers, report drafting/submission, confirmed status, platform adapter, or real external-source ingest.

## Safety boundary

This is design-only. Do not run live scans, probes, scanners, fuzzers, exploit tooling, callbacks, OAST infrastructure, proxy/pivot tooling, or target-touching automation.

Do not modify code in this review step. Do not modify:

```text
config/scope.txt
recon.sh
scripts/*.py
modules/**
tests/**
loot/**
scans/**
reports/**
.env
credentials/OAuth/scheduler/deployment/billing/production settings
```

## Expected output

Write review to:

```text
handoff/cowork_p3_1_direction_review.md
```

Required sections:

```text
# P3.1 Direction Review

## Verdict
PROCEED_WITH_FIXTURE_ONLY_P3_1 | PROCEED_WITH_CHANGES | DO_NOT_PROCEED

## Rationale

## Approved Fixture Scope

## OSS Recon Gate Notes

## Implementation Boundary

## Required TDD / Validation Gates

## Safety Boundary Confirmation

## Blocking Issues

## Non-Blocking Recommendations
```

If proceeding, provide a concrete worker-ready implementation boundary and acceptance criteria.
