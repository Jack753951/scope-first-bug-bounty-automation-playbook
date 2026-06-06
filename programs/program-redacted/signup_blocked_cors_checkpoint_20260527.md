> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# <program-slug> signup blocked: browser-side CORS checkpoint (2026-05-27)

## Summary

Owned-account signup did not advance to a visible verification page after pressing `SIGN UP` on `https://www.<program-slug>.com/create-account`.

## What was observed

- The signup form remained on `/create-account`.
- Email and password fields were populated through the ignored env-backed secret bridge; no password/OTP/token/phone value was recorded here.
- Invisible reCAPTCHA was present and produced a non-empty `g-recaptcha-response` value.
- Pressing `SIGN UP` triggered `POST https://api.<program-slug>.com/auth/signup?locale=en-sg`.
- The API request received HTTP 200 at the network layer, but the browser logged a CORS failure:
  - `Access to XMLHttpRequest at 'https://api.<program-slug>.com/auth/signup?locale=en-sg' from origin 'https://www.<program-slug>.com' has been blocked by CORS policy`
  - reason: `Access-Control-Allow-Origin` contained multiple values.
- Because the XHR was blocked by the browser, the frontend did not transition to a verification page.

## Boundary / safety notes

- No CAPTCHA bypass was attempted.
- No OTP/email verification link/password/phone/cookie/token was stored in artifacts.
- No broad scanning or fuzzing was performed.
- A dummy unauthenticated `POST {}` from curl hit Cloudflare challenge; that was used only to understand boundary behavior and did not include signup secrets.

## Decision

PARK <program-slug> production signup for first-bounty bundle execution unless the operator wants to spend more time on account creation.

Reason: this is signup/session plumbing drift, not a practiced access-control bundle. It currently blocks creation of the owned account needed for positive/negative controls.

## Next options

1. Low-cost retry: operator manually refreshes/open noVNC and clicks `SIGN UP` once more, then checks whether any verification email arrived for the H1 alias.
2. Try alternate official surface if documented/available from H1 scope, especially UAT/provided credentials, without bypassing auth controls.
3. Park <program-slug> and move to the next freshness-first target with lower signup friction.
