> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Phase 4 Closeout and Phase 5 Entry

Status: active transition recommendation
Date: 2026-05-23
Source: Hermes synthesis after Phase 4 ability-gap proof
Repo truth: `handoff/current_navigation.md`, `handoff/active_strategy_queue.md`, `handoff/proof_library_index_20260523.md`, `handoff/modern_api_auth_role_separation_wave1_20260523.md`, `handoff/accepted_changes.md`

## Decision

Phase 4 should close after this slice unless the operator identifies a specific missing ability gap.

Reason: Phase 4 now has the required local proof platform primitives:

- stable attacker/default route and recovery posture;
- true attacker callback proof pattern;
- file-read/path traversal/XXE safe-marker patterns;
- browser-runtime XSS proof packet;
- command injection marker/callback proof;
- deserialization bounded-marker proof;
- SQLi behavior/candidate proof;
- IDOR/object ownership proof;
- newly completed auth/session role-separation proof;
- evidence packets, proof library index, bundles, and current navigation.

## What changed in the final ability-gap slice

The final missing Phase 4 ability gap was role/account matrix proof for realistic bug-bounty authorization testing.

Completed artifact:

```text
handoff/modern_api_auth_role_separation_wave1_20260523.md
<artifact-output-dir>/modern_api_auth_role_separation_20260523T124050Z/
modules/bundles/verified_lab_flow_modern_api_auth_role_separation.md
```

Classification:

```text
verified_role_separation_bypass_lab_only
```

## Phase 4 exit criteria status

| Criterion | Status | Evidence |
| --- | --- | --- |
| Stable local lab route | met | `handoff/current_navigation.md` |
| Proof library index | met | `handoff/proof_library_index_20260523.md` |
| Callback proof | met | SSRF and DVWA callback packets |
| Safe file-read/path traversal/XXE proof | met | modern_vuln_api and WebGoat bundles |
| Browser-runtime XSS proof | met | WebGoat XSS evidence packet |
| Deserialization bounded marker | met | operator-verified deserialization handoff |
| Auth/session role-separation proof | met | `modern_api_auth_role_separation_wave1_20260523.md` |
| Evidence packet/report-readiness foundation | met enough for transition | existing packet template + packets |
| Periodic latest-vulnerability refresh automation | Phase 5 | intentionally not implemented in Phase 4 |

## Phase 5 name

Recommended:

```text
Phase 5: Authorized assessment readiness and vulnerability-intelligence intake
```

Avoid naming it simply `public bug bounty testing`, because public/live target work still needs a provided legal scope package.

## Phase 5 first slices

1. Phase 5A authorized live-target dry-run template
   - target scope package checklist;
   - role/account matrix template;
   - evidence redaction/minimization rules;
   - report-readiness submit/not-submit decision template.

2. Vulnerability-intelligence refresh MVP
   - one-shot source refresh first, not scheduler first;
   - classify candidates as:
     - `local_bootstrap_ready`;
     - `local_simulation_possible_but_not_faithful`;
     - `needs_authorized_live_target`;
     - `reference_only`.

3. Local/live target routing
   - if faithful local target is possible, bootstrap it in recoverable lab;
   - if live target is genuinely required, ask the operator for the legal scope package;
   - do not silently drop live-target-dependent candidates;
   - do not automatically touch live targets.

4. Optional weekly schedule only after MVP output stays compact
   - top 5 candidates maximum;
   - one selected proof lane at a time;
   - no automated target-touching cron against live targets.

## Phase 5 entry gate for live targets

Before any live/real target proof wave, collect:

```text
target URL/app/API/product/version
authorization or program/scope link
in-scope and out-of-scope assets/actions
allowed vulnerability classes and payload boundaries
rate limits / time windows / notification rules
test accounts / roles / test data availability
destructive/state-changing permission
redaction/evidence handling rules
external callback / OAST / tunnel allowance
```

Until supplied, keep candidates as:

```text
needs_authorized_live_target / blocked-awaiting-scope
```

## Boundary

This closeout is a transition/navigation record. It does not authorize public target testing, broad scanning, live-target exploitation, scope/config authorization changes, credential theft, exfiltration, destructive live testing, automatic finding confirmation, or report submission.
