> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# <program-name> A3 attempt checkpoint — teammate invite / Account B independence

Date: 2026-05-27T06:05Z
Program: <program-name> / `<program-redacted>`
Mode: authorized in-scope live-bounty work, low-speed browser/noVNC plus minimal low-speed header checks
Checkpoint status: blocked on independent Account B control; no reportable finding yet

## Operator direction incorporated

The operator clarified that for in-scope live-bounty work with owned controls available, Hermes should not add extra approval gates. Hermes should proceed until a concrete scope/safety blocker, auth/OTP/CAPTCHA/phone/password gate, or final report-submission gate appears.

This changes the practical stance for <program-name> from passive-only to selected A/B owned-account proof attempts, while preserving program scope, owned-data-only boundaries, no customer data, no DoS/rate-limit stress, no secrets in artifacts, and operator final approval before submission.

## Strategy selected

I did not choose broad scanning as the first move. For <program-name>, the higher-yield path is A/B authorization testing because the program scope and product shape emphasize company/workspace/role boundaries.

Selected first proof family:

```text
<program-name>-teammate-invite-role-boundary
```

Reason:

- Account A and Account B are operator-owned.
- <program-name> exposes teammate, team, inbox, workspace, rule, and API/UI permission surfaces.
- A/B positive/negative controls are more likely to produce a valid report than unauthenticated scanning.
- The proof can stay inside owned workspace data and avoid customer data.

## Actions performed

1. Re-checked current scope artifacts:
   - `programs/<program-redacted>/scope.json`
   - `programs/<program-redacted>/lane_state.json`
   - `config/scope.txt`
2. Confirmed `<in-scope-host>` and `<in-scope-host>` are the live web/API assets already in global scope.
3. Opened the existing <program-name> noVNC session for Account A profile (`<program-redacted>-hermes`, display `:2`).
4. Opened/checkpointed the second browser profile (`<program-redacted>-hermes-b`, display `:0`).
5. Attempted to invite the Account B H1 alias from Account A's `Invite your team` flow with company-admin toggle OFF.
6. <program-name> moved to Settings → Company → Teammates and displayed an error toast:

```text
Teammates invitation failed — Email addresses already used by other teammates.
```

7. The teammates table still showed only Account A as an active company admin. Searching for the Account B alias produced `No teammates match your criteria`.
8. Account menu in the second profile showed the same Account A identity, not an independent `+<program-redacted>-b` identity.
9. Ran a minimal low-speed unauthenticated header check against the in-scope app/API roots. Raw cookies in local header files were immediately redacted in `setting/local/program-redacted_active_20260527/`; do not promote raw headers.

## Evidence pointers

Local-only screenshots, not for report submission without redaction:

```text
setting/local/screenshots/program-redacted_live_20260527/a_invite_after_click.png
setting/local/screenshots/program-redacted_live_20260527/a_invite_filled.png
setting/local/screenshots/program-redacted_live_20260527/a_invite_submitted.png
setting/local/screenshots/program-redacted_live_20260527/after_invite_timeout.png
setting/local/screenshots/program-redacted_live_20260527/teammates_filter_toggle.png
setting/local/screenshots/program-redacted_live_20260527/teammates_search_b_after_timeout.png
setting/local/screenshots/program-redacted_live_20260527/b_profile_menu.png
setting/local/program-redacted_active_20260527/low_speed_headers.txt
```

## Current interpretation

This is not yet a reportable vulnerability.

What it shows:

- The second browser profile currently resolves to the Account A identity, not an independently usable Account B session.
- The Account B alias cannot currently be invited into Account A's workspace because <program-name> reports the address is already used by another teammate, but that teammate is not visible in the teammate table/search.

Possible explanations:

1. <program-name> normalizes/collapses the H1 plus-address aliases for account/team uniqueness.
2. Account B signup did not complete as an independent <program-name> identity and the profile is actually still Account A.
3. Account B exists in an internal/invited/blocked state not visible under the current teammate filters.
4. A stale invite/user record exists but is hidden from the current UI.

Only (3) or (4) might become a reportable access-control/admin visibility issue, and only if we can prove impact/reproducibility with owned accounts.

## Stop / next gate

Concrete blocker reached:

```text
independent Account B control is not established in the browser profile
```

Next operator action needed only because this is an auth/session gate:

```text
In Kali/noVNC, make the second browser profile (`/home/kali/browser-profiles/<program-redacted>-hermes-b`, display :0 if visible) logged into the true Account B identity. Confirm that the profile menu/email contains `+<program-redacted>-b`, or tell Hermes `Account B profile fixed`.
```

Do not paste passwords, OTPs, phone numbers, cookies, or verification links.

After Account B is truly independent, continue immediately with:

1. Account A invite B as non-admin / default teammate.
2. Account B accept or observe invite state.
3. Compare teammate visibility, shared inbox membership, settings/role controls, and direct UI URL access.
4. If B is denied in UI, test whether direct owned object URLs or API/UI flows expose admin-only or cross-workspace data.
5. If candidate evidence appears, prepare report packet but do not submit without operator final approval.
