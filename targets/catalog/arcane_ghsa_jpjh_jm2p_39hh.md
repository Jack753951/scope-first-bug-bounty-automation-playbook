> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Target Catalog — Arcane <specific-ghsa-id>

Status: candidate / local bootstrap review
Date: 2026-05-23
Source: `handoff/vuln_intel/vuln_intel_candidates_20260523T130000Z.md`
Advisory: `https://github.com/advisories/<specific-ghsa-id>`
Repository metadata: `getarcaneapp/arcane`
Package: `github.com/getarcaneapp/arcane/backend`
Affected: `<= 1.19.1`
Patched: `1.19.2`

## Why tracked

This candidate is useful for Phase 5A because it maps recent vulnerability intelligence into a local-bootstrap planning exercise for a bug-bounty-relevant role-separation issue.

## Current route

```text
local_bootstrap_review
```

Current status: source/install feasibility reviewed in `handoff/phase5a_arcane_global_variables_feasibility_review_20260525.md`; fail-closed bootstrap precheck/run-card drafted in `scripts/labs/arcane_global_variables_bootstrap_precheck.sh` and `handoff/arcane_global_variables_bootstrap_precheck_run_card_20260525.md`; no target touched. Setup/proof must not run until disposable Docker daemon/socket posture is confirmed.

Do not run against live targets. If a live Arcane instance is ever selected, require Phase 5A legal scope package first.

## Required safe bootstrap posture

```text
disposable victim lab only
Docker-in-Docker or isolated disposable Docker daemon only
no host Docker socket
throwaway admin/member users
lab-owned marker variables only
no real compose projects
no real secrets
no command execution proof by default
```

## Planned proof primitive

```text
authenticated non-admin writes global variable marker to endpoint that should require admin
```

Minimum controls:

```text
unauth control denied
admin baseline succeeds
non-admin positive unexpectedly succeeds
non-admin separate admin-only control denied
post-health succeeds
cleanup succeeds
```

## Main handoff

```text
handoff/phase5a_arcane_global_variables_bootstrap_plan_20260523.md
```
