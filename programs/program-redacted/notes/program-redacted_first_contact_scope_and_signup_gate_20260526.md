> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# <program-name> (`<program-redacted>`) first contact scope + signup gate — 2026-05-26

Status: third live target formally opened; currently blocked at operator signup/phone/identity gate
Route/tool: Kali VM `<attacker-vm>` through existing noVNC/Chromium UI; local dry-run gate through `recon.sh`
Boundary: authorized in-scope only, manual/noVNC, low-speed, owned-account flow. No scanning, fuzzing, DAST, exploit, callback/OAST/tunnel, customer interaction, non-owned data, credential/token storage, or report submission.

## Operator authorization

The operator authorized Hermes to open the third real target within <program-name>'s in-scope <bug-bounty-platform> assets.

Hermes did not ask the operator to manually copy the asset table. Instead, Hermes used the already logged-in <bug-bounty-platform> session in Kali/noVNC to inspect the <program-name> Scope page and download the official CSV.

Local raw scope CSV copy:

```text
setting/local/hackerone_scope/<program-redacted>/scopes_for_program-redacted_at_2026-05-26_08_10_14_UTC.csv
```

The raw CSV is kept under `setting/local/` as local evidence and should not be treated as a public report artifact.

## Confirmed in-scope assets from logged-in <bug-bounty-platform> CSV

```text
<in-scope-host>        URL                       bounty=true submission=true max_severity=critical
<in-scope-host>       URL                       bounty=true submission=true max_severity=critical
com.frontapp.mobile     APPLE_STORE_APP_ID        bounty=true submission=true max_severity=high
com.frontapp.mobile     GOOGLE_PLAY_APP_ID        bounty=true submission=true max_severity=high
<program-name> for Mac           DOWNLOADABLE_EXECUTABLES  bounty=true submission=true max_severity=high
<program-name> for Windows       DOWNLOADABLE_EXECUTABLES  bounty=true submission=true max_severity=high
```

Instruction attached to `<in-scope-host>`:

```text
This scope is our public API documented at https://dev.frontapp.com/
```

Executable download instruction:

```text
https://<program-domain>/download
```

## Repo authorization changes made

Created:

```text
programs/<program-redacted>/scope.json
programs/<program-redacted>/lane_state.json
```

Added to global whitelist:

```text
<in-scope-host>
<in-scope-host>
```

Not added to global whitelist for first web lane:

```text
<program-domain>
mobile app store identifiers
<program-name> for Mac / <program-name> for Windows executable lane
```

Reason: current first lane is web-owned-account viability via `<in-scope-host>`; mobile/binary/API lanes require separate bounded plans.

## Dry-run gate validation

Commands run locally only; no scanner/network stages executed because dry-run mode was used.

```bash
env HACKLAB="$PWD" ./recon.sh --dry-run --program <program-redacted> --policy-mode dry-run https://<in-scope-host>/
env HACKLAB="$PWD" ./recon.sh --dry-run --program <program-redacted> --policy-mode dry-run https://<in-scope-host>/
```

Result:

```text
safe_target PASS context=initial_target target=https://<in-scope-host> reason=in scope
safe_target PASS context=initial_target target=https://<in-scope-host> reason=in scope
```

Out-of-scope control:

```bash
env HACKLAB="$PWD" ./recon.sh --dry-run --program <program-redacted> --policy-mode dry-run https://<program-domain>/
```

Result:

```text
safe_target FAIL context=initial_target target=https://<program-domain> reason=not in scope
```

## First target contact actually performed

Opened a separate Kali Chromium profile:

```text
/home/kali/browser-profiles/<program-redacted>-hermes
```

Opened in-scope URL:

```text
https://<in-scope-host>/
```

Observed redirect/state:

```text
https://<in-scope-host>/signin
```

Visible sign-in page:

```text
Email address
Password
Sign in
Try for Free
Sign in with Google
Sign in with Office 365
Forgot password
Privacy Notice
Google User Data Privacy Notice
```

No CAPTCHA/OTP/payment/customer data was visible at the sign-in screen.

Clicked `Try for Free` from the sign-in page to inspect signup requirements.

Observed signup/free-trial URL:

```text
https://<program-domain>/signup
```

Important nuance: `<program-domain>` itself is not in the downloaded Scope CSV and was not added to global scope. This contact occurred as the normal signup path linked from the in-scope app sign-in page and consistent with prior policy preview. Do not continue on `<program-domain>/signup` except as the official <program-name> signup gate for the in-scope app lane; do not broaden this into marketing-site testing.

Visible signup fields:

```text
Work email
First name
Last name
Company
Job title
Industry
Phone number
Company size
Terms acknowledgement by submitting
Submit
```

A chat widget is visible with:

```text
Get a Demo
Pricing
Product Tour
Chat with our AI Virtual Rep
```

Do not interact with the chat widget; it risks customer/support interaction and is blocked for the first lane.

No CAPTCHA/OTP/payment was visible yet, but phone number and identity fields are an operator gate.

## Current gate

Current state:

```text
A2_PENDING_OPERATOR_AUTH / blocked_operator_action
```

Operator gate:

```text
Fill the signup form locally in Kali/noVNC using operator-owned/approved details only.
```

Allowed for operator or Hermes to enter transiently in the live browser, if comfortable and policy-consistent:

```text
<bug-bounty-platform> alias email derived from username <researcher-alias>, e.g. <researcher-alias-email> if accepted
safe first/last name labels if accepted
company name with [Bug Bounty] marker
job title
industry
company size
one operator-owned phone number, preferably typed by the operator in noVNC; if sent to Hermes, use transiently only and do not store/repeat it
```

Do not paste any of these into chat/repo:

```text
actual email alias
phone number
password
OTP
verification link
cookies
tokens
API keys
payment/KYC details
```

Operator noted having two phone numbers available if needed. Treat that as account-gate capacity only; do not store phone numbers.

## Next autonomous action after operator gate

After the operator completes signup/auth locally and the browser reaches a logged-in owned <program-name> workspace without CAPTCHA/OTP/phone/email/payment blockers, Hermes may continue with browser-only low-speed surface mapping:

```text
profile/account page
workspace/company empty state
roles/permissions labels
non-sensitive settings names
whether Account B or teammate control is required
whether API docs/token path is needed later
```

Stop before:

```text
customer messages/comments
outbound communication
invites to third parties
Account B invite unless operator-controlled and separately approved
API token creation or retention
integrations/webhooks/callbacks/OAST/tunnels
billing/payment/support/KYC
scanner/fuzzer/DAST
report submission
```

## Evidence pointers

Local screenshots:

```text
setting/local/screenshots/program-redacted_scope_20260526/scope_no_hai.png
setting/local/screenshots/program-redacted_scope_20260526/app_first_contact.png
setting/local/screenshots/program-redacted_scope_20260526/signup_entry.png
```

These are local operational evidence, not report-ready finding evidence.
