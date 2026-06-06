> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Tactical risk rebalance — 2026-05-26

Status: proposed adjustment / no target touched
Source: operator feedback that current tactics are too conservative compared with productive bug bounty practice.
Boundary: This does not authorize out-of-scope testing, destructive actions, credential theft, malware, stealth, persistence, uncontrolled scanning, non-owned data access, or report submission. It proposes a richer tactic taxonomy so useful but stronger techniques are considered instead of silently excluded.

## Problem

Current live-bounty workflow correctly preserves safety, but it can under-select realistic bug-hunting tactics by treating many stronger techniques as simply blocked. Productive researchers often consider higher-risk tools and bundles when they are policy-allowed, rate-limited, non-destructive, owned-resource-only, and evidence-bounded.

The gap is not that the project lacks safety. The gap is that the tactic planner needs a middle layer between `safe_now` and `blocked_high_risk`.

## New tactical posture

Replace binary thinking:

```text
safe_now vs blocked
```

with a ladder:

```text
Tactic L0 — passive only
Tactic L1 — manual browser/UI observation
Tactic L2 — authenticated owned-object request replay
Tactic L3 — bounded active validation within owned resources
Tactic L4 — policy-allowed tool-assisted validation with strict budgets
Tactic L5 — high-risk/sensitive; explicit operator + policy + separate plan
Tactic X — prohibited regardless of authorization
```

## Tactic levels

### Tactic L0 — passive only

Examples:
- public policy/docs/release notes
- disclosed reports
- JS/static artifact reading without probing target beyond normal page load
- CVE/vendor advisory mapping

Default autonomy: Hermes may do autonomously.

### Tactic L1 — normal manual observation

Examples:
- normal logged-in UI browsing
- profile/workspace/object inventory
- identifying object IDs through normal provenance

Default autonomy: allowed after A2 scope/auth gates.

### Tactic L2 — request replay for owned objects

Examples:
- replay a normal UI request with Account A and Account B sessions
- compare status/body excerpts for one object family
- test direct API fetch of a normally observed owned object

Default autonomy: allowed only after A3 lane preview, exact scope, Account A/B controls, request budget, and redaction plan.

### Tactic L3 — bounded active validation

Examples:
- harmless marker update
- role downgrade/revoke/share/unshare checks
- low-volume parameter tampering on known owned object IDs
- UI/API parity checks for documented endpoints
- GraphQL single-object authorization check when endpoint and object are known

Default autonomy: checkpoint before execution; may proceed only with explicit lane approval and policy allowance.

### Tactic L4 — policy-allowed tool-assisted validation

Examples:
- Burp Repeater/Intruder with tiny fixed payload set and request budget
- nuclei single-template metadata-informed check against exact in-scope host when program permits
- ZAP/Burp passive scan of owned session traffic
- content discovery with tiny allowlisted wordlist against explicit asset when permitted
- OAST/DNS callback only if program explicitly allows and no internal scanning is involved

Default autonomy: not default; requires separate plan, policy evidence, request budget, stop conditions, and operator approval.

### Tactic L5 — high-risk/sensitive

Examples:
- broad scanner/fuzzer/DAST
- upload/parser exploitation
- workflow/run-script/integration execution
- payment/order/KYC/support/recovery
- mobile MITM/rooted devices
- callbacks/tunnels beyond explicitly allowed minimal OAST
- admin/seller/partner surfaces

Default autonomy: escalation-only. Requires explicit operator approval and often should be avoided for first lanes.

### Tactic X — prohibited

Never create or run:
- credential theft
- malware
- stealth/persistence/evasion
- destructive actions on non-disposable targets
- unauthorized access
- non-owned data collection
- broad exfiltration
- bypassing legitimate controls outside authorized test scope

## Engineering impact

Update preview/synthesis artifacts to preserve stronger tactics instead of discarding them:

- `safe_now_l0_l1`
- `owned_bounded_l2_candidate`
- `active_l3_requires_lane_approval`
- `tool_assisted_l4_requires_policy_and_operator_approval`
- `sensitive_l5_escalation_only`
- `prohibited_x`

A preview should include at least one higher-powered tactic candidate when product shape supports it, even if it is deferred. The final selected lane can still be conservative, but the tactical option must not disappear.

## Practical change for next live lanes

For each target preview:

1. Generate default safe A/B hypotheses.
2. Generate stronger L3/L4 hypotheses separately.
3. For each stronger tactic, list:
   - exact policy text needed;
   - exact asset/object prerequisite;
   - request budget;
   - non-destructive evidence standard;
   - stop condition;
   - why it is worth the risk.
4. Hermes chooses one safe executable lane now and preserves stronger candidates as approval-ready packets.

## Acceptance rule

The project should be less tactically timid but not less disciplined. Stronger tactics are allowed into consideration and planning. Execution still requires scope, policy, owned controls, request budgets, and operator approval at the relevant gate.
