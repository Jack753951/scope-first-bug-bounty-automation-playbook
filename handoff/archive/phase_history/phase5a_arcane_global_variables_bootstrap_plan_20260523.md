> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Phase 5A Candidate Bootstrap Plan — Arcane <specific-ghsa-id>

Status: selected candidate / bootstrap plan only / no target touched
Date: 2026-05-23
Source candidate list: `handoff/vuln_intel/vuln_intel_candidates_20260523T130000Z.md`
Selected candidate: `<specific-ghsa-id>` — Arcane missing admin authorization on global variables endpoint
Advisory: `https://github.com/advisories/<specific-ghsa-id>`
Package: `github.com/getarcaneapp/arcane/backend`
Affected range: `<= 1.19.1`
Patched version: `1.19.2`
Candidate routing: `local_bootstrap_review`

## Decision

Select Arcane <specific-ghsa-id> as the first Phase 5A vuln-intel-to-local-bootstrap planning candidate.

Why this candidate over the other local-bootstrap candidates:

- It is recent and source/package metadata is available through GitHub Advisory.
- It maps directly to the Phase 4 ability gap just completed: auth/session role separation.
- It has bug-bounty-relevant impact shape: authenticated non-admin user can reach an admin-only global variable endpoint.
- It is likely reproducible in a local self-hosted environment if the app can be run against a disposable Docker daemon.
- It trains the project on a high-risk but controllable class: admin authorization bypass in infrastructure-management UI.

## Critical safety note

Arcane is a Docker management application. A careless bootstrap could expose or modify the host Docker daemon.

Do not run Arcane against the host/control-plane Docker socket. Do not mount a production or user-owned Docker socket. Do not run against the Windows host Docker daemon.

Allowed bootstrap target only:

```text
<victim-vm> or an equivalent disposable VM/container sandbox
isolated Docker-in-Docker daemon or disposable Docker socket
host-only network by default
throwaway users and test project only
no real compose projects
no real secrets
no Internet during proof execution unless explicitly needed for install/pull and then closed
```

This plan is intentionally not an exploit run. It is a bounded local bootstrap feasibility plan.

## Vulnerability class

Primary:

```text
auth/access-control
role-separation bypass
admin-only configuration endpoint exposed to authenticated non-admin
```

Possible impact if proven in lab:

```text
non-admin user can overwrite global environment variables used by project compose deployments
```

Do not claim RCE unless a separate, explicitly authorized, marker-only deployment proof shows controlled execution in the disposable lab. Phase 5A first proof should stop at authorization-boundary and configuration-write marker if possible.

## Bootstrap objective

Create a local target plan that can answer:

```text
Can vulnerable Arcane <= 1.19.1 be launched in a disposable lab?
Can we create admin and non-admin throwaway users?
Can we observe the vulnerable endpoint and secure controls?
Can a non-admin write a lab-owned marker variable through the global variables endpoint?
Can an admin baseline do the same expected action?
Can a non-admin be denied on at least one separate admin-only control?
Can all evidence be collected without touching a real Docker socket or real compose project?
```

## Non-goals

Do not do these in the bootstrap phase:

```text
no public/live target testing
no exploit execution against third-party Arcane instances
no broad scanning
no host Docker socket mounting
no production Docker daemon access
no real project deployment
no secret/env dumping
no command execution proof
no reverse shell/callback/OAST
no persistence
no destructive cleanup outside disposable target
no report submission
```

## Proposed local architecture

Preferred architecture:

```text
Windows Hermes control plane
  -> <attacker-vm> as operator/attacker if target-touching becomes necessary
  -> <victim-vm> running disposable Arcane target
       -> Arcane vulnerable version <= 1.19.1
       -> Docker-in-Docker or disposable nested daemon
       -> throwaway project with inert compose service
       -> no host/user Docker socket
```

If Docker-in-Docker is impractical, stop and reassess. Do not substitute the host Docker socket just to make setup easier.

## Feasibility discovery steps

These are metadata/source review steps before any target launch:

1. Identify official install path for Arcane vulnerable `<= 1.19.1`.
2. Identify whether a tagged container image exists for `1.19.1`.
3. Identify required environment variables and database/storage paths.
4. Identify whether initial admin/user creation can be scripted with throwaway credentials.
5. Identify endpoint path and request schema for:
   - `PUT /api/environments/{id}/templates/variables`
   - login/session/token flow
   - one separate admin-only control endpoint for negative control
6. Identify whether Arcane can use a disposable Docker endpoint rather than `/var/run/docker.sock`.
7. Write a bootstrap script only after these are known.

## Minimum proof plan if bootstrap is feasible

Classification target:

```text
verified_role_separation_config_write_lab_only
```

Required evidence:

```text
pre-health 200
admin login/session works
non-admin login/session works
non-admin role confirmed as member/non-admin
unauthenticated request to global variables endpoint returns 401/403
admin baseline write of lab-owned marker succeeds or documented expected control succeeds
non-admin write to global variables endpoint succeeds unexpectedly
subsequent read/render/config observation shows lab-owned marker only
non-admin denied on separate admin-only control endpoint
post-health 200
cleanup removes disposable project/daemon/container
```

Safe marker example:

```text
HERMES_ARCANE_ROLE_SEPARATION_MARKER_<timestamp>
```

Allowed marker content only. Never write real secrets, cloud keys, tokens, or commands.

## Evidence artifact layout

If the bootstrap proceeds later, use:

```text
<artifact-output-dir>/arcane_global_variables_authz_<YYYYMMDDTHHMMSSZ>/
  summary.md
  summary_values.json
  pre_health.json
  admin_login.redacted.json
  member_login.redacted.json
  unauth_control.json
  admin_baseline.json
  member_positive_marker_write.json
  member_secure_control_403.json
  post_health.json
  cleanup.log
```

Redact tokens/cookies immediately. Store only status codes, endpoint labels, marker values, role labels, and minimal response excerpts.

## Stop conditions

Stop before target-touching if:

```text
only host Docker socket access is available
official vulnerable image cannot be pinned
account/role setup cannot be done with throwaway local users
proof requires real project/secrets/deployment
proof requires shell/RCE to show value
the app cannot run without broad network exposure
```

Stop during proof if:

```text
unexpected sensitive data appears
request leaves host-only lab unexpectedly
marker write affects non-disposable state
endpoint behavior differs from advisory and requires guessing
cleanup fails
```

## Next implementation slice

Recommended next slice:

```text
source/install feasibility review only
```

Expected output:

```text
handoff/phase5a_arcane_global_variables_feasibility_review_20260523.md
```

Only after that should a local bootstrap script be written.
