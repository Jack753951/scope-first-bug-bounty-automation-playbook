> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# <program-name> Account C clean repro checkpoint — 2026-05-27

Status: waiting for operator auth/signup fields; no target proof executed yet
Boundary: in-scope <program-name> web app signup path only; manual/noVNC; owned Account C only; no scanner/fuzzer/DAST/exploit/callback/tunnel; no customer/non-owned data; no token/cookie/OTP/password/phone storage; no report submission.

## Purpose

Create a clean Account C negative-control / same-company signup repro to resolve the Account B provenance gap.

Hypothesis under test:

- If a fresh owned Account C independently signs up using the same company/workspace label as Account A, <program-name> may incorrectly auto-join C into Account A's existing company/workspace and/or grant broad teammate/admin-like permissions without invitation or approval.

This is not yet proven. Current Account B evidence remains a candidate signal only.

## Actions performed by Hermes

1. Reconnected to Kali/noVNC at `127.0.0.1:6080`.
2. Confirmed existing visible <program-name> app state was open in Kali.
3. Created/opened a dedicated clean Chromium profile for Account C:
   - `/home/kali/browser-profiles/<program-redacted>-hermes-c`
4. Opened official <program-name> signup path:
   - `https://<program-domain>/signup`
5. Confirmed the free-trial form is visible in noVNC.
6. Saved local-only screenshot evidence:
   - `setting/local/screenshots/program-redacted_live_20260527/account_c_signup_ready.png`

## Current operator gate

The signup form is waiting for operator-owned fields that Hermes must not record in artifacts:

- Account C work email / alias
- phone number if required
- password/OTP/email verification if later requested
- exact verification link if any

For the clean repro, operator should keep provenance clean:

1. Use a fresh owned Account C alias.
2. Do not accept any invite from Account A.
3. Do not approve/add Account C from Account A/admin.
4. Use the same company/workspace label as Account A if testing the same-company auto-join hypothesis.
5. Complete only the signup/auth gates needed to reach the first logged-in <program-name> state.
6. Stop after first successful login/onboarding screen and tell Hermes: `Account C signup gate completed`.

Do not paste passwords, OTPs, phone numbers, cookies, tokens, full email addresses, or verification links into chat/repo.

## Next autonomous action after operator gate

After operator says Account C signup/auth is completed, Hermes should immediately verify, using noVNC only:

1. Whether Account C is in a new independent workspace or Account A's existing company/workspace.
2. Whether Account C appears as an active teammate under Account A/admin views.
3. Whether Account C belongs to `Customer Support`, `Sandbox Admins`, or any admin-like group.
4. Whether Account C can access admin/settings/teammates/permissions direct URLs.
5. Whether the result supports or disproves same-company auto-join / unintended admin grant.

Stop before customer/non-owned data, outbound messages, external channel/OAuth/mailbox/webhook/integration connection, callbacks/OAST/tunnels, destructive action, scanner/fuzzer/DAST, secret/token/cookie/OTP/password/phone storage, and report submission.
