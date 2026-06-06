> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Growth-First Review Policy

Status: active simplified policy
Owner: Hermes / Operator
Safety posture: preserve hard authorization gates; remove review bureaucracy that slows capability growth

## Purpose

This file replaces the old T0-T5 review-tier machinery. The project should grow as a Hermes/agent capability library: reusable scripts, machine-readable contracts, validation, proof bundles, handoff, and worker collaboration. Review exists to catch concrete blockers, not to become an approval maze.

## Default Rule

Hermes may proceed without extra reviewer approval when the work is:

- repo-local or offline;
- local-lab only against disposable/recoverable targets;
- passive/read-only public research;
- in-scope owned-account browser/manual work that stays within documented stop-before boundaries;
- cleanup, indexing, handoff, Obsidian routing, schemas, tests, scripts, proof-pattern drafts, bundle retention, or validation helpers.

For these cases, use focused validation and compact handoff. Do not require a tier label, milestone ceremony, multi-party review, or separate approval just because a file is non-trivial.

## Hard Stops That Still Require Operator Approval

Stop and ask before any of these:

- adding or broadening live target authorization in `config/scope.txt` or `programs/<slug>/scope.json`;
- active scans, fuzzing, DAST, exploit attempts, callbacks, OAST, tunnels, proxies/pivots, or high-volume automation against live targets;
- OAuth, integration, webhook, channel/mailbox connection, API-token creation, billing/payment/KYC, scheduler/deployment/publishing, or persistent external automation;
- invite/team/role/account mutation unless the current lane explicitly authorizes an owned-account proof boundary;
- credentials, cookies, tokens, OTPs, passwords, phone numbers, verification links, loot, or customer/non-owned data;
- destructive actions, stealth, persistence, malware, evasion, brute-force/password guessing, resource exhaustion, or uncontrolled state change;
- report-ready promotion, public disclosure, or report submission.

These are safety/authorization boundaries, not review-process preferences.

## Review Is Advisory Unless It Names a Concrete Blocker

Reviewer output from Claude/Cowork/Codex is useful for tactical coverage, architecture, evidence quality, and dissent. It does not block growth by itself.

A finding blocks execution only when it names a concrete issue such as:

- missing or ambiguous authorization/scope;
- live target contact beyond the current lane;
- secret/token/cookie/OTP/phone/customer-data risk;
- unsafe external side effect;
- missing stop-before boundary for a state-changing proof;
- failing validation introduced by the change;
- malformed machine-readable contract that a runner consumes;
- deletion/overwrite risk to useful project capability or evidence.

Everything else is advisory. Record useful dissent, then continue or defer it.

## Validation Expectations

Prefer the smallest validation that proves the slice is safe and useful:

- JSON/schema parse for machine-readable state;
- `bash -n` / Python compile for changed scripts;
- focused regression tests for changed behavior;
- redaction check for evidence artifacts;
- `bash ./bin/hermes review` when broad repo state or shared worker contracts changed;
- pre/post health, cleanup, and network-closure checks for local-lab execution.

Do not run unrelated full reviews just to satisfy ceremony.

## Capability-Growth Bias

When deciding between more process and more capability, choose capability unless a hard stop applies.

Prefer:

- runnable scripts over prose;
- compact indexes over long narratives;
- verified proof bundles over discussion;
- preserving realistic hypotheses over prematurely pruning them;
- checkpointing useful blocked/deferred lanes over turning them into global bans;
- fast local-lab learning over publication-grade review.

## Binding Safety Preservation

This policy does not authorize live target work, secret handling, report submission, or external side effects. It removes unnecessary review/tier ceremony while preserving `.hermes.md`, scope files, program rules, and the hard stops above.
