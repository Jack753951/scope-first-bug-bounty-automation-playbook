> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# <program-redacted> campaign run card — 2026-05-27

Program: <program-redacted>
H1 URL: https://<bug-bounty-platform>.com/<program-redacted>
Freshness signal: Active campaign, ends in 30 days, double payouts for Core services.

## Score

```text
freshness: 3/3
self_signup: 0/2
free_plan: 0/2
low_priv_control: 0/3
owned_object: 0/3
scope_clarity: 2/2
operator_cost_low: 0/3
access_control_surface: 2/3
api_or_direct_url_surface: 2/2
Total: 9/23
```

## Bundle fit

Potential bundles if official/owned access exists:

- auth-role-separation
- invite-membership-lifecycle
- object-ownership-idor
- api-ui-permission-mismatch

No bundle executed.

## Candidate asset

`teammate.indriver.io` is visible as Core / in-scope / bounty-eligible / Critical / 0 resolved reports in the H1 scope table.

Minimal public check found a SPA login page:

```text
Teammate
Build Collaborative Teams
Sign in with Google
```

The public client bundle contains internal-looking route/API path strings. Raw bundle content and third-party links are not preserved here to avoid turning recon into unnecessary data exposure. No external docs/links were opened.

## Controls

Positive control: missing.
Negative control: missing.
Owned object/resource: missing.

## Operator cost

Current cost: 4

Reason: Google/company-style OAuth or official test credentials appear necessary before any owned teammate/admin/team object controls can be created.

## Allowed actions for this parked lane

- H1 program/scope review.
- Low-speed public landing-page checks already completed.
- Passive client-resource review only if needed, without opening external docs or collecting non-owned data.

## Blocked actions

- Google/company OAuth attempt without explicit operator approval.
- Contacting support/employees.
- Opening embedded third-party docs/Atlassian/Drive/etc. links from the bundle.
- Accessing arbitrary user/company data.
- Scanning/fuzzing without explicit approval and request caps.
- Report submission without operator final approval.

## Decision

PARK.

Reason: good fresh/campaign signal, but no clean self-serve owned controls and high OAuth/operator cost. This is not execution-ready for a first-bounty access-control bundle.

## Resume criteria

Resume only if one of these appears:

1. official test credentials or self-serve owned account path;
2. operator explicitly approves OAuth/company-identity setup;
3. another in-scope Core asset exposes a low-friction owned-object/control surface;
4. a bounded, policy-allowed proof can be done without non-owned data or high auth cost.
