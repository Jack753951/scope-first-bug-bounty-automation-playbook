> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# <program-name> A3 owned Account B permission checkpoint — 2026-05-27

Status: blocked on clean admin-vs-low-priv split / not report-ready
Boundary: in-scope <program-name> web app only; manual noVNC; owned accounts only; no scanner/fuzzer/DAST/exploit/callback/tunnel; no customer/non-owned data; no token/cookie/OTP/password/phone storage; no report submission.

## Operator instruction

Operator authorized continuing all in-scope operations/tactics to find a reportable vulnerability. Hermes treated this as approval for manual owned-control <program-name> testing, including owned teammate invite/permission checks, while preserving hard stops for secrets, customer data, destructive behavior, external integrations/callbacks, and final submission.

## What was tested

1. Reconnected to Kali noVNC at `127.0.0.1:6080` and confirmed <program-name> UI was open.
2. Enumerated visible Chromium windows via Kali `xdotool`/`xprop`.
3. Confirmed the visible top-level <program-name> windows were tied to the `<program-redacted>-hermes-b` browser profile.
4. Opened <program-name> settings from the visible authenticated session.
5. Checked Teammates, invite flow, teammate search, teammate detail, resource permissions, teammate groups, and global Permissions page.
6. Attempted owned Account B invite using the operator-owned project alias. The exact email is intentionally not stored here.

## Redacted observations

- Teammates list shows one active teammate matching Account B label/alias fragment.
- Invite flow for Account B returns: `This email is already used by a teammate in your company.`
- Searching teammate list for the Account B alias fragment shows the same active teammate.
- Account B detail page is accessible from the current session.
- Account B is in workspace access groups:
  - `Customer Support`
  - `Sandbox Admins`
- Resource permissions page shows broad checked permissions, including conversation actions, teammate manage, permissions manage, shifts create/edit/delete, inbox create/edit/delete, and tag create/edit/delete/nest.
- Global Permissions page shows `Admin permission set` assigned to `Customer Support`; granular permissions are not available on the current plan.

## Interpretation

This is a strong candidate signal only if Account B was expected to be a separate non-admin or lower-privilege account. In the current observed state, Account B is already an active teammate with admin-like group membership. Therefore it cannot serve as the low-privilege negative control required to prove a permission bypass.

The previously interesting invite error (`already used by a teammate`) is now explained by Account B actually existing as an active teammate in the company. It is not reportable by itself.

## Concrete blocker

A reportable permission/tenant issue now requires one of:

1. A visible Account A/admin session plus Account B intentionally downgraded or excluded from the relevant resource; or
2. A new owned Account C invited/accepted as lower-privilege/non-admin; or
3. A clear operator statement that Account B should never have become a company teammate/admin, plus signup/invite provenance proving it self-joined or gained admin without invitation.

Without one of those, current testing can only show expected admin access, not unauthorized access.

## Safe next tactics

Recommended next path:

- Establish clean controls:
  - Account A = admin/owner positive control.
  - Account B or C = lower-privilege negative control.
- Then test, in order:
  1. direct URL access to admin-only settings pages;
  2. direct URL access to shared inbox/resource settings after removing the low-priv account from that resource;
  3. UI/API mismatch only after token handling/redaction plan and operator action for token creation;
  4. invite/downgrade stale permissions after role/group change.

Stop-before remains: customer/non-owned data, outbound messages, external channel/OAuth/mailbox/webhook/integration connection, callbacks/OAST/tunnels, destructive action, scanner/fuzzer/DAST, secret/token/cookie/OTP/password/phone storage, and report submission.
