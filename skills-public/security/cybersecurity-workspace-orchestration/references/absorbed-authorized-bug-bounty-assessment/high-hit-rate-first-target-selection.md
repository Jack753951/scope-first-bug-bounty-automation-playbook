> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# High-hit-rate first target selection after no-finding live runs

Use this reference when one or more authorized live-bounty/VDP runs produced `no_finding`, `surface_only`, or `needs_second_account`, and the operator asks whether the learning mechanism is working or wants Hermes to pick the next target from the Kali/noVNC lane.

## Core lesson

A no-finding run is not a signal to increase intensity. It is a target-selection signal. Convert it into a new, higher-fit candidate choice using passive program/policy intake first, then exact scope confirmation, then a narrow A2 viability lane.

The operator expects Hermes to act as the project owner here: diagnose why prior runs failed, update the no-finding feedback log, and proactively select a better target/lane instead of waiting for step-by-step instructions.

## Safe sequence

```text
read current repo navigation + no-finding log
-> inspect existing shortlist/filter artifacts
-> use Kali VM/control-plane route for passive public program metadata/policy only
-> compare 3-5 candidates against high-hit-rate criteria
-> choose one recommended candidate
-> write a target-selection preview artifact
-> update accepted_changes/current_navigation/active_queue/Obsidian
-> stop at exact asset-table / account / alias / scope gate
```

Do not navigate target app assets, create accounts, log in, add scope, run scanners, or touch candidate application hosts during this selection step.

## Candidate scoring lens

Prefer a target with:

- open submissions and real program history;
- clear researcher signup or test-instance route;
- exact account/email/header requirements;
- workspace/org/team/tenant model;
- role/member/invite boundaries;
- safe owned object creation;
- official API docs or SDKs;
- explicit interest in cross-tenant, AuthZ, access control, API/UI mismatch, or role-permission issues;
- no immediate payment/KYC/order/support/customer-data dependency.

Downgrade candidates when:

- the useful test requires emailing for a special instance before any action;
- bounties are paused or unavailable for the current goal;
- the platform is identity/security-sensitive and would be better as a second run;
- first proof depends on enterprise/account-request, customer messaging, outbound sends, integrations, callbacks, uploads, or secrets;
- public metadata does not expose exact in-scope assets and the operator has not confirmed them from the logged-in program view.

## Artifact shape

Create a concise artifact under `handoff/<program>_target_selection_preview_<date>.md` with:

```text
Status / route / boundary
Decision
Passive facts observed
Relevant policy facts
Unresolved exact-scope facts
Candidate comparison
Tactical preview: expanded options before narrowing
Selected first lane if scope/account gates pass
Operator-safe confirmation phrases
Next safe action
```

Use safe reply phrases for the operator, for example:

```text
<Program> assets confirmed
<Program> assets not visible
<Program> signup in scope
<Program> signup not in scope
<Program> alias ready
blocked_auth
blocked_email_verification
blocked_policy
stop
```

## Stop conditions

Stop before target-touching if:

- structured asset table is not visible from public metadata;
- exact signup/app host scope is not confirmed;
- account alias/header requirement is unresolved;
- the first viable lane needs customer data, real messages, outbound sends, integrations, callbacks, API-key/secret retention, or third-party data;
- the next step would create `programs/<slug>/scope.json` or `config/scope.txt` without explicit operator-confirmed scope facts.

## Session-derived example

After <program-redacted> (`needs_second_account` / consumer/payment-heavy/no safe object) and <program-redacted> (`surface_only` / empty workspace / needs second tenant/API plan), Front (`<program-redacted>`) was selected as a better first new-process candidate because public policy metadata showed open bounty, explicit researcher signup, HackerOne alias requirement, API docs, customer-ops/team/workspace shape, and interest in cross-company/cross-tenant/admin/API permission boundaries. The run still stopped before target-touching because the full structured asset table required logged-in HackerOne confirmation.
