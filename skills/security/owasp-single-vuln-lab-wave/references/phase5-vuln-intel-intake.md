> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Phase 5 vulnerability-intelligence intake pattern

Use when the local proof platform has stable primitives and the operator wants to start absorbing current CVE/advisory intelligence without turning the system into automatic public-target exploitation.

## Core lesson

Closeout-stage local labs should not keep adding similar vulnerability waves for quantity. After proof primitives are stable, new vulnerability testing should fill explicit ability gaps only. Recurring/latest-vulnerability intake belongs in the next phase as metadata-first candidate routing.

## Minimum Phase 5A shape

Create these artifacts before any live target work:

- authorized live-target dry-run / scope package template;
- report-readiness checklist;
- one-shot vulnerability-intelligence refresh script;
- compact candidate output in markdown/JSON/CSV;
- current navigation / active queue / accepted changes / Obsidian updates.

The one-shot intake should fetch advisory metadata from allowlisted sources such as CISA KEV, NVD recent CVEs, and GitHub Security Advisories. It should not scan, exploit, bootstrap containers, probe live targets, use callback/OAST, submit reports, or schedule recurring jobs.

## Routing labels

Use explicit routing labels so valuable lanes are not silently dropped:

- `local_bootstrap_review` — likely worth reviewing for a faithful local target or fixture.
- `local_or_live_review_high_impact` — high-impact class; try local reproduction first, otherwise ask for legal scope.
- `needs_authorized_live_target` — do not filter out; ask the operator for a legal target/scope/rules package before target-touching work.
- `reference_only_review` — keep as reference until it maps to a current authorized scope or clear local target.

Earlier wording may use `local_bootstrap_ready` / `local_simulation_possible_but_not_faithful` / `needs_authorized_live_target` / `reference_only`; keep the same semantics but prefer `*_review` when no bootstrap has been validated yet.

## Scope package before live target

Before any live/real target proof wave, ask the operator for:

- target URL/app/API/product/version;
- authorization or program/scope link;
- in-scope and out-of-scope assets/actions;
- allowed vulnerability classes and payload boundaries;
- rate limits, testing windows, and notification rules;
- throwaway test accounts/roles/data availability;
- destructive/state-changing permission;
- evidence redaction/minimization rules;
- external callback/OAST/tunnel allowance.

Until supplied, keep the candidate `blocked-awaiting-scope`.

## Report-readiness checklist

Convert evidence into submit/not-submit decisions only after checking:

- in-scope asset/action and allowed method;
- positive evidence and negative controls;
- meaningful security boundary/impact;
- bounded reproducible steps;
- no prohibited automation, payload class, sensitive data retention, or forbidden state change;
- duplicate/known-issue review where possible;
- redacted/minimized evidence and honest limitations.

## Pitfalls

- Do not let `local_bootstrap_review` mean `ready to exploit`; it means ready for feasibility planning. Select one lane, write a bounded local-bootstrap plan/target catalog entry, document non-goals and stop conditions, and only then decide whether a target can be safely launched.
- For Docker-management, CI/CD, secrets, cloud, identity, or infrastructure-management apps, do not trade safety for convenience: never mount a host/user Docker socket or use real daemons/secrets/projects just to reproduce a finding. Require Docker-in-Docker or an isolated disposable victim-lab daemon and marker-only actions.
- Do not implement weekly/cron scheduling first. Run a one-shot MVP, inspect compactness and usefulness, then schedule only if the output stays actionable.
- Do not treat `needs_authorized_live_target` as rejection. It is a request for operator-provided legal scope.
- Do not claim local lab proof equals a bounty report. Use report-readiness conversion and program policy checks.
- Do not let vulnerability-intel intake become a CVE warehouse. Output top candidates and pick at most one lane at a time.
