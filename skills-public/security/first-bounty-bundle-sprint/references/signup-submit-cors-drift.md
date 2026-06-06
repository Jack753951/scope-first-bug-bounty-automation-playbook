> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Signup submit CORS / frontend drift checkpoint

Use this reference when a live bounty signup form appears filled correctly but does not advance to email/OTP/CAPTCHA/phone verification after submit.

## Pattern

Observed class of failure:

- Signup page remains on the same route after clicking submit.
- Fields are populated and client-side validation appears satisfied.
- Invisible CAPTCHA may already have produced a non-empty token.
- Network shows the signup API request was attempted, but the browser console reports CORS failure.
- A common concrete signal is `Access-Control-Allow-Origin` containing multiple values, so the browser blocks the XHR even when the network layer shows an HTTP 2xx response.

## Diagnostic sequence

1. Do not assume the operator missed a visible CAPTCHA or OTP page.
2. Inspect browser state first:
   - current URL/title/body text;
   - whether fields are populated, redacting email/password/phone;
   - whether CAPTCHA iframe/token exists;
   - visible buttons/errors.
3. Capture network/console only at metadata level:
   - endpoint path/host;
   - HTTP status;
   - browser error category;
   - redacted reason such as duplicate CORS origin values.
4. Do not persist passwords, OTPs, verification links, cookies, tokens, phone numbers, or full private emails.
5. If the API returned 2xx but frontend was CORS-blocked, ask the operator only to check whether a verification email arrived; do not keep clicking indefinitely.

## Decision rule

Treat this as signup/session plumbing drift, not as a practiced vuln bundle.

PARK the target unless one of these becomes true:

- operator confirms a verification email/session exists;
- official UAT/provided credentials are available;
- the signup defect itself is explicitly in-scope and reportable under the program policy, with no need for secret/customer data and no CAPTCHA/anti-abuse bypass.

For first-bounty execution, prefer moving to the next freshness-first target rather than spending high operator time on account-creation plumbing.