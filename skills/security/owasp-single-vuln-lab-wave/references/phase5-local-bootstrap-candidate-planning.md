> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Phase 5 local-bootstrap candidate planning

Use after a one-shot vulnerability-intelligence refresh has produced candidates and the operator agrees to move one `local_bootstrap_review` lane forward without touching live targets or immediately running an exploit.

## Core lesson

The next step after vuln-intel intake is not automatic exploitation. Pick at most one candidate and write a bounded local-bootstrap plan that answers whether the advisory can be reproduced safely in a disposable lab.

Prefer candidates that:

- map to an explicit capability gap or recently stabilized proof primitive, such as auth/session role separation;
- have clear advisory metadata, affected/patched versions, and source/package links;
- are likely to run locally in a recoverable target;
- train bug-bounty-relevant judgment such as role/account boundaries, admin authorization, tenant separation, or reportable impact framing.

## Required planning artifacts

Create or update:

- a dated handoff plan under `handoff/phase5a_<product_or_class>_bootstrap_plan_<date>.md`;
- a target catalog entry under `targets/catalog/<candidate>.md` when the repo uses a target catalog;
- current navigation / active queue / accepted changes / Obsidian project note.

The plan should include:

- advisory ID/title/source and affected/patched versions;
- why this candidate was selected over other candidates;
- candidate routing and current status (`selected / plan-only / no target touched`);
- safety boundary and non-goals;
- proposed local architecture;
- feasibility-discovery steps before target launch;
- minimum proof shape if bootstrap is feasible;
- artifact layout;
- stop conditions;
- next implementation slice.

## Docker-management and infrastructure apps

For products that manage Docker, orchestration, CI/CD, secrets, cloud, identity, or infrastructure, add an explicit socket/credential boundary before any bootstrap work.

For Docker-management apps in particular:

- do not mount the host/user Docker socket just to make setup easy;
- do not connect to the Windows host Docker daemon or production/user-owned Docker daemon;
- use only Docker-in-Docker or an isolated disposable victim-lab daemon;
- use throwaway projects/users and marker-only config changes;
- do not claim RCE or host impact unless a separate explicitly approved disposable-lab proof demonstrates it;
- stop if safe bootstrap requires real projects, real secrets, a host socket, or production-like daemon access.

## Minimum proof design for authz/config-write candidates

For admin authorization or role-separation advisories, require at least:

- pre-health;
- unauthenticated control denied;
- admin login/session baseline;
- non-admin/member login/session and role label;
- admin baseline action or expected admin control;
- non-admin positive action that should be denied;
- one separate admin-only secure-control endpoint denied to non-admin;
- marker-only readback/observation when safe;
- post-health and cleanup.

Keep tokens/cookies redacted; store status codes, endpoint labels, role labels, marker values, and minimal response excerpts only.

## Pitfalls

- Do not let `local_bootstrap_review` mean `ready to exploit`; it means `ready for feasibility planning`.
- Do not select high-impact infrastructure candidates without writing explicit daemon/socket/credential safety rules.
- Do not substitute a convenient host socket or real account when a disposable equivalent is not yet available; stop and record the blocker.
- Do not promote the candidate to report-ready because the advisory exists. Local bootstrap planning is still pre-proof.