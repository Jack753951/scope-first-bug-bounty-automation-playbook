> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Phase 5A authorized assessment and vulnerability-intelligence routing

Use this reference when coordinating a cybersecurity workspace that is moving from local proof-library work into authorized live-target readiness.

## Transition rule

When the local lab has stable proof primitives, stop expanding the lab just to increase vulnerability count. Continue local testing only for explicit ability gaps. Move recurring/latest vulnerability intake into a Phase 5-style lane with metadata-only intake, scope-package requirements, and report-readiness decisions.

## Required Phase 5A artifacts

- `phase5a_authorized_live_target_dry_run_template.md` — legal scope package, target map, role/account matrix, candidate lane, proof plan, evidence packet, and report decision structure.
- `phase5a_report_readiness_checklist.md` — submit/not-submit checklist by vulnerability class.
- one-shot `vuln_intel_refresh` style script — advisory metadata only; no target touch.
- compact candidate artifacts in markdown/JSON/CSV.
- navigation updates in current queue, accepted changes, and long-term project notes.

## Candidate routing

Use routing states that preserve breadth while keeping legal boundaries:

- `local_bootstrap_review`: likely worth reviewing for a local fixture/target.
- `local_or_live_review_high_impact`: high-impact class; attempt local reproduction first, otherwise ask for legal scope.
- `needs_authorized_live_target`: keep the candidate and ask the operator for legal target/scope/rules. Do not silently reject it.
- `reference_only_review`: hold as intelligence until it maps to an authorized target or local lab.

## Scope package request

Before any real/live target touch, collect:

- target URL/app/API/product/version;
- authorization/program scope link;
- in-scope and out-of-scope assets/actions;
- allowed and forbidden test classes;
- rate limits/time windows/notification rules;
- throwaway accounts/roles/test data;
- destructive/state-changing permission;
- evidence redaction/minimization rules;
- callback/OAST/tunnel allowance.

Until provided, label the lane `blocked-awaiting-scope`.

## Coordination pitfalls

- Do not create a recurring scheduler first. Prove the one-shot intake is compact and useful before scheduling.
- Do not let Hermes self-authorize live testing from public advisory data.
- Do not convert candidates directly into findings. Require report-readiness checks and program rules.
- Keep raw targets, credentials, tokens, private scope details, and sensitive evidence out of global memory and broad notes; route them to the approved repo/private handoff layer with redaction.
