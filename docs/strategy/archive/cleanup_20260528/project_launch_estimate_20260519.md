> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Project Launch Estimate — Cybersec Lab

Date: 2026-05-19
Prepared by: Hermes
Basis inspected:

- `handoff/active_strategy_queue.md`
- `handoff/third_party_p3_7_implementation_review.md`
- `handoff/accepted_changes.md`
- `handoff/systematization_extension_plan.md`
- `handoff/extensible_architecture_direction.md`
- `handoff/periodic_reviews/2026-05-18/hermes_synthesis.md`
- current PR #1 / branch `feat/p1-4-program-policy-boundary`

## Current state

The project is not yet production/live bug-bounty automation. It is, however, well past a toy scaffold:

- Phase 1 scope and program-policy gates exist and have dry-run/runtime integration hardening.
- Phase 2 offline contracts, dry-run runner previews, module manifest/profile checks, candidate review workflow, verification planning, and report-readiness gating exist.
- Phase 3 built strong offline regression / review artifacts and P3.7 returned the project to the program-policy mainline.
- P3.7 independent implementation/safety review returned `PASS_WITH_RECOMMENDATIONS`.

Current safe acceptance state: P3.7 can be accepted as committed at `c7dfe2c`.

## Definition-dependent launch estimate

"正式上線" can mean several different gates. The estimates below use current velocity but assume the project continues to preserve the existing safety/review discipline.

| Launch level | Meaning | Remaining work | Estimate |
|---|---|---:|---:|
| Dry-run/local MVP | Local platform demo: deterministic scope/policy/module/report-readiness pipeline; no live target touching | 6–10 small slices | 3–10 workdays (~1–2 weeks) |
| Controlled lab beta | Can run only against local lab / intentionally vulnerable app with explicit operator approval; no public bug bounty targets | 12–20 slices | 9–30 workdays (~2–6 weeks) |
| Authorized bug-bounty private beta | One or a few explicitly scoped programs, manual activation, strict review gate, report drafts only after human verification | 24–40 slices | 24–80 workdays (~5–16 weeks) |
| Production-like multi-program platform | Repeatable multi-program onboarding, durable run/evidence store, report/export adapters, monitoring, operational docs, rollback, stronger CI | 45–70 slices | 45–175 workdays (~9–35 weeks) |

Hermes recommendation: treat "正式上線" as **authorized bug-bounty private beta**, not production-like multi-program operation. That puts the realistic target at **about 2–4 months** if work continues steadily and no major safety redesign is discovered.

## Why not sooner

The remaining risk is not basic coding speed; it is safety-boundary correctness. The following are still deferred or blocked:

- real program scope/rule onboarding;
- any live target execution;
- scanner/module execution;
- schema promotion for current `*/0.1-trial` artifacts;
- scanner-output importer/exporter boundaries;
- recon-to-runner policy-artifact bridge;
- real evidence locator and redaction gate;
- report drafting/submission adapters;
- scheduler/CI automation that could touch targets;
- credentials/OAuth/deployment/billing/production settings.

These cannot be compressed safely by just writing more code, because each crosses a review tier or operator-approval boundary.

## Recommended path to private beta

### Gate A — Close P3.7 cleanly

Status: almost done.

- Accept `handoff/third_party_p3_7_implementation_review.md`.
- Update `handoff/active_strategy_queue.md` to mark P3.7 complete.
- Record the review in `handoff/accepted_changes.md`.
- Push PR update.

### Gate B — Program-policy mainline hardening (offline/tests first)

Estimated 3–6 slices.

Candidate slices:

1. `_examples/` documentation or fixture clarification for `automation_permitted: true`.
2. Fresh micro-direction review for malformed-scope exit-code semantics.
3. Fresh micro-direction review for literal CIDR-deny end-to-end coverage.
4. Stale artifact / target / mode / technique mismatch E2E harness if it can be done without runtime scope weakening.
5. A small closeout review for program-policy dry-run confidence.

### Gate C — Recon-to-runner bridge, still dry-run only

Estimated 4–8 slices.

Needed before meaningful automation:

- direction review + OSS Recon Gate;
- dry-run-only policy artifact bridge;
- no module execution at first;
- preview ledger / run manifest consistency;
- independent safety review.

### Gate D — Evidence and finding flow toward report drafts

Estimated 5–8 slices.

Needed before any useful bug-bounty private beta:

- evidence locator and redaction gate;
- scanner-output remains triage-only;
- finding/evidence lifecycle review;
- candidate-to-report-draft boundary without `confirmed` auto-promotion;
- human verification checklist remains mandatory.

### Gate E — Lab-only controlled live activation

Estimated 4–8 slices.

Only after explicit operator approval:

- local lab / intentionally vulnerable app scope file;
- live-mode activation design review;
- deny-by-default runtime tests;
- rate limits / blackout windows / kill switch;
- proof no public target can be touched accidentally.

### Gate F — One-program private beta

Estimated 8–12 slices.

Only after explicit scope and rules:

- one real program scope/rules file, reviewed manually;
- operator approval record;
- private beta runbook;
- manual preflight checklist;
- post-run evidence review;
- report-draft quality gate;
- rollback and incident stop procedure.

## Concrete forecast

If continuing at the current slice quality:

- Best-case private beta: about **5–8 weeks**.
- Realistic private beta: about **8–16 weeks**.
- Conservative production-like operation: **4–8+ months**.

The best next move is not to add live behavior yet. Finish Gate A, then run Gate B hardening while keeping everything offline. After that, decide whether to enter Gate C (dry-run recon-to-runner bridge) or Gate E (lab-only live activation) depending on operator appetite.

## Process-quality note

The process is strong but becoming expensive:

- P3.7 direction/implementation consumed high Claude Code turn count for a small test slice.
- Review artifacts are high quality but long.
- Future slices should be smaller and have stricter prompt budgets, especially for T1/T2 work.

Suggested workflow adjustment:

- keep T3+ full reviews;
- use shorter T1/T2 review prompts;
- separate "direction", "implementation", and "expectation alignment" passes;
- preserve named artifacts, but avoid re-reading the entire history for every small slice.
