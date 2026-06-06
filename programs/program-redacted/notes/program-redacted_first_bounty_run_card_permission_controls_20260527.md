> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# <program-name> first-bounty run card — owned permission controls — 2026-05-27

Status: READY_FOR_PRECONDITION_CHECK, not report-ready
Generated: 2026-05-27T10:05:54Z
Program: <program-name> / `<program-redacted>`
Platform: <bug-bounty-platform>
Authorization basis: `programs/<program-redacted>/scope.json`; in-scope web/API assets include `<in-scope-host>` and `<in-scope-host>`.

## External tactical review synthesis

Two advisory agents reviewed the current queue/artifacts without touching live targets.

Consensus:

- Rank #1 target: <program-name> / `<program-redacted>`.
- Recommended lane: owned-account permission controls, not Account C same-domain signup.
- Best bundle: `removed-downgraded-stale-access`.
- Secondary bundle: `auth-role-separation`.
- Later-only bundle: `api-ui-permission-mismatch` after a separate token/API redaction plan and operator action.
- Parked/avoid: Account C same-company/same-domain signup line; current evidence is better explained by verified-domain workspace grouping and requires email verification before login.
- Concrete blocker for reportability: no clean admin-vs-low-priv or removed/downgraded negative control yet.

## Target score

```text
self_signup: 2/2
free_plan: 2/2
low_priv_control: 1/3  # Account B exists but is currently active/admin-like; clean low-priv split not established
owned_object: 2/3      # owned workspace/account/resource surfaces exist; exact resource for proof still to choose
scope_clarity: 2/2
operator_cost_low: 2/3 # user is logged into H1; target app auth/control changes may still need operator gates
access_control_surface: 3/3
api_or_direct_url_surface: 2/2
Total: 16/20
Decision: strong target, proceed only to precondition/control check.
```

## Selected bundle

Primary bundle: `removed-downgraded-stale-access`

Report title if true:

```text
Downgraded or removed <program-name> teammate retains access to admin/resource settings via direct URL.
```

Secondary bundle: `auth-role-separation`

Report title if true:

```text
Low-privilege <program-name> teammate can access admin-only settings or resource controls via direct URL.
```

Do not use this run card to claim a finding unless low-priv / removed / downgraded negative control is clean.

## Hypothesis

If Account A/admin removes, excludes, or downgrades Account B from a workspace group/resource/permission set, Account B might retain access to admin-only or resource-specific pages/actions through existing session state, direct URLs, stale membership, or UI/API mismatch.

## Lab-derived bundle transfer

Lab-derived bundle: WebGoat-style access-control / IDOR lessons + verified local proof discipline for safe-marker evidence.

Transferred controls:

- Positive control: Account A/admin can access the selected settings/resource page.
- Negative control: Account B after low-priv/downgrade/remove should be denied.
- Owned-data-only: use operator-owned workspace/account/resource labels only.

Transferred evidence pattern:

- role/control matrix;
- expected-vs-observed table;
- redacted screenshots;
- URL path class only, not secrets/tokens/cookies/full private identifiers.

Live restrictions applied:

- manual low-speed browser/noVNC only;
- no scanner/fuzzer/DAST;
- no broad API probing;
- no token creation/storage;
- no customer/non-owned data;
- no outbound messages/channel/integration/OAuth/callback/webhook;
- stop before report submission.

## Preconditions before live proof

Required:

1. Confirm current <bug-bounty-platform> policy/scope still lists <program-name> web app/API assets as in scope.
2. Confirm target interaction is limited to `<in-scope-host>` first.
3. Confirm Account A/admin positive control is visible.
4. Establish one clean negative control:
   - Account B intentionally downgraded to low-privilege; or
   - Account B removed/excluded from selected group/resource; or
   - fresh operator-owned Account C invited/accepted as low-privilege only if operator chooses that cost.
5. Choose one owned resource/page family for the proof:
   - admin settings;
   - teammate/permission settings;
   - shared inbox/resource settings;
   - teammate group/resource membership page.

Current blocker:

```text
Account B is currently an active teammate with admin-like group/permissions; that state cannot prove unauthorized low-privilege access.
```

## Allowed actions

- Browser/noVNC manual navigation at low speed.
- Read H1 policy/scope and target docs/UI.
- Use Account A/admin and operator-owned Account B/C only.
- Change Account B role/group/resource membership only when doing the selected owned-control proof.
- Capture redacted screenshots/notes of role labels, expected deny/allow state, and URL path class.

## Blocked actions

- Scanner/fuzzer/DAST/exploit automation.
- DoS/rate-limit stress.
- Customer/non-owned data access or interaction.
- Outbound customer messages/comments.
- Third-party integrations, OAuth, external channel/mailbox connection.
- API token creation/storage unless a separate operator-approved API redaction plan exists.
- Callbacks/OAST/tunnels/webhooks.
- Billing/payment/support/KYC.
- Password, OTP, cookie, bearer token, API key, verification-link, phone, or raw private email storage.
- Report submission without operator final approval.

## Minimal execution plan

Phase 0 — H1/scope precondition check:

1. Open logged-in <bug-bounty-platform> <program-name> program page.
2. Confirm scope/rules relevant to `<in-scope-host>`; if policy changed or scope is unclear, stop.
3. Do not download/store secrets or private H1 content beyond non-sensitive scope/status notes.

Phase 1 — live app control check:

1. Open Account A/admin <program-name> settings.
2. Identify one specific owned page/resource where A has access.
3. Determine if B can be made a clean negative control without high operator cost:
   - downgrade B;
   - remove B from resource/group;
   - or stop and ask operator only if a secret/auth/role-change decision is required.

Phase 2 — proof attempt, only if clean negative control exists:

1. Record expected matrix:
   - A/admin: allow.
   - B low-priv/removed/excluded: deny.
2. In B session, use normal UI first; if UI denies, test only the already-owned direct URL path for the same page/resource.
3. Stop immediately if non-owned/customer data, token/cookie, external integration, or destructive action appears.

Phase 3 — decision:

- EXECUTE: clean negative control exists and direct URL/action mismatch appears.
- PARK: no clean low-priv/remove/downgrade control, or role change needs operator cost above current signal.
- KILL: behavior matches documented/expected permissions.

## Evidence required if candidate appears

- Scope reference path/date, not raw private H1 exports.
- Account labels only: A/admin, B/low-priv-or-removed; no raw emails.
- Role/control matrix.
- Owned resource/page label, redacted.
- Expected vs observed behavior.
- Redacted screenshots or request snippets without cookies/tokens/PII/customer data.
- Stop-before confirmation.
- Cleanup/no-customer-data statement.

## Current decision

```text
Decision: EXECUTE_PRECONDITION_CHECK_ONLY
Next action: open H1 <program-name> program page and target app/noVNC state to confirm scope + whether clean A/B permission control can be established. If only Account B active/admin-like remains, PARK rather than forcing Account C signup.
```
