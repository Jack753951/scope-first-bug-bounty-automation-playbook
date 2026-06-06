> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Phase 3 Remaining Work and Plain-Language Review Meaning

Status: planning/explanation checkpoint
Date: 2026-05-20
Prepared by: Hermes

## Plain-language answer: what the multi-party reviews mean

The reviews are not saying "the platform is ready to attack targets." They are saying something narrower and more useful:

1. The offline/dry-run architecture is coherent enough to keep building.
2. The safety boundaries are being preserved: no silent live scans, no scope bypass, no automatic confirmed findings, no report submission, no callbacks/proxy/pivot behavior.
3. Reviewers have found real issues when present, such as the P3.12 asymmetric drift-lock bug, and those issues were fixed before acceptance.
4. The current policy language is good enough to support the next design step, but future module manifest/profile fields still require a fresh T3+ direction review and OSS Recon Gate before becoming a contract.
5. Hermes may directly accept low-risk offline/docs/tests slices after validation, but target-touching, live activation, scanner/module execution, credentials, scheduler, deployment, or report submission remain escalation-only and require explicit operator approval.

In short: multi-party review currently evaluates the project as **safe and disciplined for offline platform hardening**, not as **ready for autonomous live bug-bounty testing**.

## What "APPROVE_WITH_CHANGES" means here

`APPROVE_WITH_CHANGES` means:

- the reviewer agrees with the direction;
- implementation is allowed only after applying the narrowing conditions;
- anything outside those conditions remains blocked.

For P3.13, the conditions were: keep it docs-only, add a risk-tier cross-map, add fail-closed clauses, add ambiguous-scope handling, and keep future fields non-contractual.

## What "PASS_WITH_RECOMMENDATIONS" means here

`PASS_WITH_RECOMMENDATIONS` means:

- no blocker was found for the reviewed slice;
- the work can be accepted inside the approved boundary;
- recommendations are future hardening items, not permission to expand scope.

For bridge-related work, this usually means the test/dry-run slice is OK, while runtime bridge or live behavior remains deferred.

## What "REQUEST_CHANGES" meant in P3.12

`REQUEST_CHANGES` meant the reviewer found a real blocker. In P3.12, the catalog test could miss reverse drift from P3.11 fixture vocabulary/status changes. Hermes fixed that with AST-based exact set equality, then follow-up review returned `PASS`.

That is evidence the review loop is catching practical correctness issues, not just rubber-stamping.

## Current capability level

The platform can currently support:

- offline/dry-run policy and contract validation;
- local module runner previews;
- policy artifact and profile hash binding;
- synthetic evidence and reviewer-readiness calibration;
- candidate-only workflow and report-readiness analysis;
- strict handoff/review governance.

The platform cannot yet safely support without more phases:

- public or private bug-bounty target scanning;
- live scanner/module execution;
- exploit/fuzz/brute-force/callback workflows;
- automatic recon-to-runner execution;
- automatic finding confirmation;
- report submission or platform adapters.

## Phase 3 remaining rough estimate

Phase 3 is now in its late offline-hardening segment, but not complete. A realistic remaining breakdown is:

1. P3.14 — module manifest/profile field promotion direction review, design-only T3+.
2. P3.15 — first-bounty readiness checkpoint / dry-run-local MVP gap list.
3. P3.16 — if approved, implement a small contract/schema/test slice for only the safest subset of module risk fields, or explicitly defer field promotion.
4. P3.17 — offline dry-run MVP closeout review: confirm whether Gate B/C/D readiness is enough to move toward controlled lab beta.
5. P3.18 optional — cleanup/commit hygiene: resolve untracked artifacts, archive rolling handoffs, and create a clean acceptance bundle.

Estimated remaining Phase 3: about **3-5 small stages** if we keep it offline and do not introduce live behavior.

If we choose to fold controlled lab activation into Phase 3, then Phase 3 would expand significantly, likely **6-10 more stages**, because lab live activation is T4/T5-style safety work. Hermes recommendation: keep live/lab activation as Phase 4, not Phase 3.

The accepted roadmap insertion is now **Phase 4A — Controlled Lab Semi-Automated Calibration** (`handoff/phase4a_controlled_lab_calibration_plan_20260520.md`): use a local lab/intentionally vulnerable app/explicit CTF-training target to calibrate workflow and scripts after Phase 3 closeout, before any real bug-bounty private beta.

## Recommended phase boundary

Recommended Phase 3 exit criteria:

- risk-tier policy accepted;
- future manifest/profile field direction decided;
- dry-run/local MVP readiness gaps listed;
- no live activation hidden inside Phase 3;
- next phase explicitly named before any lab/live work begins.

Recommended Phase 4 start criteria:

- operator selects local lab / intentionally vulnerable app scope;
- explicit authorization exists;
- live-mode activation is reviewed as T4/T5;
- kill switch, rate limits, deny-by-default tests, and audit logging are ready.

Recommended Phase 4 sub-phases:

1. Phase 4A — authorized lab semi-automated workflow/script calibration.
2. Phase 4B — lab-to-report workflow trial with manual verification and report-readiness artifacts.
3. Phase 4C — one-program authorized bug-bounty private-beta planning.
