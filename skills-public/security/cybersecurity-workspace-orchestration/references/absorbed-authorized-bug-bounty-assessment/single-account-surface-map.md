> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Live Bounty Single-Account Surface Mapping Pattern

Session-derived pattern from a <program-redacted> Taiwan HackerOne first-lane run. Use this as a compact reference when an operator has only one owned account and cross-account IDOR is not yet possible.

## When This Applies

- Public bug bounty or client-authorized live target.
- Exact scope/rules are recorded and minimal hosts have been added to the project scope whitelist.
- Operator has one owned normal account, but not a second account/phone/role for negative controls.
- Goal is post-login surface mapping, not exploitation.

## Safe Objective

Produce a `surface_only` map:

- account/member/my-page paths;
- cart/review/settings/customer-service paths;
- visible object types;
- whether object IDs appear through normal UI/API provenance;
- read vs write/state-changing operations;
- which checks need a second owned account.

Do not try to prove IDOR with one account. Label it `needs_second_account`.

## Low-Risk Observation Steps

1. Re-confirm the browser is logged in without recording identity details.
2. Capture only redacted screenshots or sanitized observations.
3. For each page, record:
   - URL/path and host;
   - visible page type/state;
   - owned object/ID hints, if any;
   - whether PII is visible, without transcribing it;
   - whether the action is read-only or state-changing;
   - classification.
4. Prefer empty-state and history/list pages before any create/edit flow.
5. Stop on CAPTCHA, OTP, account warning, rate limit, third-party data, payment/KYC prompt, policy uncertainty, or any non-owned data exposure.

## Useful Classifications

```text
surface_only
no_finding
candidate
needs_second_account
blocked_state_change_without_plan
blocked_sensitive_auth_flow
blocked_operator_action
```

## Common Empty-State Findings

These are not vulnerabilities by themselves:

- empty order history;
- empty cart;
- empty return/refund history;
- zero coupon count;
- empty customer-service inquiry history;
- disabled pagination with no records.

They are useful because they identify future object classes, but they are `surface_only` unless an owned object/ID and a safe control exist.

## State-Changing / Sensitive Surfaces to Block by Default

Block until there is a separate plan, program-rule support, and operator approval:

- coupon redemption or promo-code guessing;
- customer-service chat or support ticket creation/editing;
- ID/password recovery or account-auth flows;
- checkout/payment/order/cash/points/KYC;
- upload flows;
- seller/partner/admin/developer portals without a legitimate account;
- any action that might touch non-owned data.

## Evidence/Handoff Shape

Use a concise table:

```text
| Step | Surface | URL/Path | Visible status | Owned object / ID notes | Classification | Evidence |
```

Then add:

- current blocker;
- candidate queue;
- needs-second-account queue;
- next preview seed.

For a single-account empty-state run, the synthesis should say clearly: no reportable vulnerability found; current constraint is proof quality, not tooling.

## Project Benefit

A single-account map is still valuable because it:

- prevents overclaiming;
- shows where real object IDs may appear later;
- defines which negative controls need Account B;
- keeps high-risk flows out of the first lane;
- seeds a future bundle or report-readiness path only if actual owned objects appear.
