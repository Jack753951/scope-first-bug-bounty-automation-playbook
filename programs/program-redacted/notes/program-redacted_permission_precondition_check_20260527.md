> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# <program-name> permission-control precondition check — 2026-05-27

Status: PARKED — clean negative control not established
Mode: authorized in-scope live-bounty work; low-speed browser/noVNC; owned accounts only

## What was checked

1. Confirmed <bug-bounty-platform> <program-name> program scope page is accessible and current browser session is logged into <bug-bounty-platform>.
2. Confirmed scope table still lists:
   - `<in-scope-host>` — in scope, bounty eligible, max severity critical.
   - `<in-scope-host>` — in scope, bounty eligible, max severity critical; public API documentation reference only.
3. Connected to local noVNC and confirmed Kali browser session is logged into <program-name> at `<in-scope-host>`.
4. Opened <program-name> settings from the left navigation.
5. Confirmed Team management surfaces are visible:
   - Teammates
   - Permissions
   - Schedule
6. Opened Permissions page.

## Redacted observations

- <program-name> settings loaded successfully in the authenticated owned-account session.
- Team/resource settings navigation is visible.
- Permissions page shows the current plan does not provide granular workspace permissions.
- Permissions page shows an `Admin permission set` assigned to a teammate group label visible in the UI.
- Multiple conversation permission rows are visible and appear assigned broadly through the current group/everyone-style controls.
- This confirms a permission surface exists, but does not establish a clean low-privilege negative control.

No raw emails, passwords, OTPs, cookies, tokens, API keys, verification links, phone numbers, customer data, or non-owned data were recorded.

## Evidence pointers

Local screenshots, for redacted internal use only:

```text
setting/local/screenshots/program-redacted_live_20260527/front_display2_precondition_20260527.png
setting/local/screenshots/program-redacted_live_20260527/front_settings_after_gear_20260527.png
setting/local/screenshots/program-redacted_live_20260527/front_settings_after_load_20260527.png
setting/local/screenshots/program-redacted_live_20260527/front_permissions_page_20260527.png
```

## Decision analysis

Selected bundle:

```text
removed-downgraded-stale-access / auth-role-separation
```

Positive control:

```text
Account A/current authenticated owned <program-name> session can access <program-name> settings and Permissions page.
```

Negative control:

```text
NOT established.
```

Concrete blocker:

```text
Current available <program-name> state still lacks a clean Account B/C low-privilege, removed, downgraded, or resource-excluded negative control. The visible permission model is group/plan constrained, and changing the current admin permission set without a known safe fallback could affect the owned workspace control state.
```

Why no proof was executed:

- A reportable access-control claim requires a clean expected-deny account state.
- Current observations only show settings/permission surfaces and broad/admin-like permission configuration.
- Proceeding directly would risk proving expected admin/group access, not unauthorized access.
- Mutating admin permission set/group membership from this state could risk lockout or confusing provenance without a safer staged control plan.

## Current decision

```text
Decision: PARK
Reason: no clean negative control; permission surface confirmed; proof should resume only after a safe low-priv/removed/downgraded control is available.
```

## Safe next options

1. If an already-owned low-privileged <program-name> account/session exists, use it as negative control and resume the run card.
2. If Account A can safely create or select a non-admin group/resource exclusion without risking admin lockout, prepare a micro-plan before changing anything.
3. If no clean negative control exists, switch target rather than forcing Account C signup or risky permission mutations.
4. Keep Account C same-domain signup line parked unless new evidence appears for unverified/non-matching-domain join, unexpected admin default contrary to docs, or removed/downgraded retention.

Stop-before preserved: no customer/non-owned data, no outbound message/comment, no channel/OAuth/integration/webhook/callback/tunnel, no token/API handling, no scanner/fuzzer/DAST, no destructive action, no report submission.
