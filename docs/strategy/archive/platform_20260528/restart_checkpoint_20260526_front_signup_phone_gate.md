> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Restart checkpoint — <program-name> signup operator phone gate — 2026-05-26

Status: pause/restart requested by operator before phone submission
Program: <program-name> / `<program-redacted>`
Lane: third live target first-contact A2 owned-account signup/profile/workspace surface map
Current state: `A2_PENDING_OPERATOR_AUTH` / `blocked_operator_action`

## Authorization and scope status

<program-name> was formally opened as the third real target only within confirmed in-scope <bug-bounty-platform> assets.

Confirmed from logged-in <bug-bounty-platform> Scope CSV downloaded via Kali/noVNC:

```text
setting/local/hackerone_scope/<program-redacted>/scopes_for_program-redacted_at_2026-05-26_08_10_14_UTC.csv
```

Confirmed in-scope assets:

```text
<in-scope-host>        URL                       max severity: critical
<in-scope-host>       URL                       max severity: critical
com.frontapp.mobile     iOS App Store             max severity: high
com.frontapp.mobile     Google Play               max severity: high
<program-name> for Mac           Downloadable executable   max severity: high
<program-name> for Windows       Downloadable executable   max severity: high
```

Repo scope artifacts already created/updated:

```text
programs/<program-redacted>/scope.json
programs/<program-redacted>/lane_state.json
programs/<program-redacted>/notes/program-redacted_first_contact_scope_and_signup_gate_20260526.md
handoff/third_target_contact_checkpoint_20260526.json
config/scope.txt
```

Global scope entries added:

```text
<in-scope-host>
<in-scope-host>
```

`<program-domain>` was not added as global scope. It is only treated as the official signup page reached from the in-scope `<in-scope-host>/signin` flow, not as a marketing-site test target.

Dry-run gates already passed:

```text
https://<in-scope-host>/   safe_target PASS
https://<in-scope-host>/  safe_target PASS
https://<program-domain>/          safe_target FAIL closed
```

## Browser/noVNC state before restart

Kali/noVNC has a Chromium window/profile for this lane:

```text
/home/kali/browser-profiles/<program-redacted>-hermes
```

Current relevant page before restart:

```text
https://<program-domain>/signup
```

This was reached by opening in-scope:

```text
https://<in-scope-host>/
```

which redirected to:

```text
https://<in-scope-host>/signin
```

Then `Try for Free` was clicked.

## Signup form state before restart

Hermes filled the non-secret, low-sensitivity fields up to the phone gate.

Filled values/state:

```text
Work email: <bug-bounty-platform> alias plus-addressing for <researcher-alias> / <program-redacted>
First name: <researcher-alias>
Last name: Research
Company: BugBountyOcroResearch
Job title: SecurityResearcher
Industry: Technology
Company size: 1 - 10 employees
Phone number: not filled
Submit: not clicked
```

Important note: the page accepted the H1 alias as a syntactically valid work email after paste. Earlier xdotool typing corrupted the email field once; the current visible state after repair looked valid and had no email error.

## Why paused

Operator said: `做個紀錄我重開一次`.

Pause reason:

```text
operator wants to restart once before continuing from phone/signup gate
```

No phone number, password, OTP, verification link, cookie, token, API key, or payment data was recorded.

## Resume instructions

After restart, reopen noVNC and/or the Chromium profile if needed:

```text
http://127.0.0.1:6080/vnc.html?autoconnect=1&resize=scale
```

If the <program-name> signup window is gone, reopen using Kali command or manually navigate:

```text
chromium --user-data-dir=/home/kali/browser-profiles/<program-redacted>-hermes --no-first-run --new-window https://<in-scope-host>/
```

Then use the official app sign-in page's `Try for Free` path if needed.

Next operator action:

```text
Enter one operator-owned phone number locally in the <program-name> signup form, then either press Submit yourself or ask Hermes to proceed.
```

If asking Hermes to fill a phone number, provide it only transiently and explicitly authorize one-time use. Hermes must not store/repeat it.

Expected status replies after operator action:

```text
front_signup_complete
blocked_phone
blocked_email_verification
blocked_captcha
blocked_payment
blocked_policy
stop
```

## Safety boundary on resume

Allowed after successful operator auth gate:

```text
browser-only low-speed owned-account profile/workspace/empty-state/role-label surface map
```

Still blocked:

```text
scanner/fuzzer/DAST
DoS/rate-limit testing
exploit/callback/OAST/tunnel
third-party integrations
customer messages/comments/support chat
non-owned/customer data
API token creation or retention
credential/cookie/token/password/OTP storage
billing/payment/KYC
report generation/submission without operator final approval
```

## Latest validation before pause

```text
programs/<program-redacted>/lane_state.json schema ok
bash ./bin/hermes review: OK
git diff --check: OK
```
