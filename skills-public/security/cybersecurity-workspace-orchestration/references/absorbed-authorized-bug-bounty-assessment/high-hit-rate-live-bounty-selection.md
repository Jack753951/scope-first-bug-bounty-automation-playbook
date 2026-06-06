> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# High-hit-rate live bounty selection

Use this pattern after an initial live/VDP flow has proven process familiarity but produced no vulnerability. The goal is to improve finding probability without weakening authorization or evidence gates.

## Diagnosis pattern

A no-finding result is often not a technical failure. Common causes:

- target state is empty or low-surface;
- only one account is available;
- no safe owned object ID exists;
- policy blocks the features most likely to contain impact;
- the run optimized for workflow validation, not vulnerability yield.

Treat this as target-selection learning, not as a reason to increase intensity.

## Default high-hit-rate loop

```text
A0 passive OSINT / program scoring
-> choose one bug class before choosing the target
-> confirm prerequisites: Account A/B, tenant/workspace, roles, API, safe owned objects
-> timebox A2 viability check to 15-30 minutes
-> run A3 bounded proof only with exact policy/scope and owned controls
-> if prerequisites are absent, park quickly and move to a better-fit target
```

## Target scoring dimensions

Score each candidate 0-2 for:

1. self-service signup;
2. two owned accounts feasible;
3. two workspaces/tenants feasible;
4. team/org/role model;
5. free safe owned objects;
6. official API/docs;
7. policy allows access-control/authz testing;
8. no payment/KYC/order/support dependency for first proof;
9. public/private/share/invite boundary;
10. disclosed reports or product shape suggesting relevant bug classes.

Suggested routing:

- 16+: high-fit candidate; worth policy intake and first lane.
- 12-15: possible; verify prerequisites before touching target.
- 8-11: short viability check only.
- <8: park unless operator has a specific reason.

## Bug-class-first priority

Prefer classes with strong controlled evidence:

1. IDOR/BOLA/object ownership;
2. tenant/workspace isolation;
3. role/permission confusion;
4. API authorization mismatch;
5. share/public-private boundary.

Do not start with broad surface mapping as the main effort. Use surface mapping only to answer: “Can this target support one of the prioritized bug classes with owned controls?”

## No-finding closeout requirement

Every no-finding live lane should produce a hypothesis backlog:

```text
missing prerequisite:
target deepen or park:
next bug class:
next required account/object/role/tenant:
what target-selection rule changes next time:
```

If the first answer is `needs_second_account`, `blocked_no_owned_object`, or `blocked_sensitive_flow`, do not keep browsing indefinitely. Park or switch target.

## Safety stays tiered, not heavy everywhere

- A0 passive/docs/OSINT/shortlist: default and fast; no target asset requests.
- A1 scope-gated dry-run: semi-automatic, exact policy facts only.
- A2 low-rate owned-account viability: browser/manual, narrow, timeboxed.
- A3 bounded proof: requires A/B or equivalent controls and redacted evidence.
- A4 sensitive/high-risk flows: separate plan and explicit policy/operator allowance.

The improvement is to lighten low-risk selection and viability, not to weaken A3/A4 gates.
