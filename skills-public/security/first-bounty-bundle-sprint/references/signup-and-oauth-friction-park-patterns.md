> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Signup / OAuth friction park patterns

Session-derived patterns for first-bounty live target selection.

## Browser-side signup submit succeeds at network layer but frontend never advances

Pattern:

- Signup form can be filled with the H1 alias and env-backed password.
- Invisible CAPTCHA or anti-abuse widget may produce a token.
- Submit triggers the expected signup API request.
- Network layer may show an HTTP 2xx response, but browser console shows CORS or frontend handling failure.
- No verification email arrives and the page stays on the signup route.

Decision rule:

```text
PARK, unless the operator independently receives a verification email or an official test credential path exists.
```

Why:

- This is signup/session plumbing drift, not a practiced access-control bundle.
- Without an owned account there is no positive control, negative control, or owned object.
- Do not turn the signup API behavior itself into a report candidate unless there is a clear security impact beyond broken account creation.

Safe handling:

- Record only non-secret evidence: route, endpoint path, HTTP class, browser error class, and no-email outcome.
- Do not store password, CAPTCHA token, OTP, cookies, verification links, or raw response bodies containing secrets.
- Do not attempt CAPTCHA bypass or alternate direct-account-creation API calls.
- Move to the next freshness-first target if no email appears.

## Fresh campaign with company/OAuth-only login

Pattern:

- Target has excellent freshness signals: active campaign, doubled payouts, clear H1 scope, low/no resolved reports on a promising asset.
- Public app shows `Sign in with Google`, SSO, company identity, or no self-serve account path.
- Client bundle may expose interesting route/API names, but no owned controls exist.

Decision rule:

```text
PARK for first-bounty execution when operator cost is OAuth/company identity and there is no official test identity or self-serve control setup.
```

Why:

- Freshness does not override the bundle precondition gate.
- Route/API names are hypotheses only; they do not create a positive/negative control pair.
- OAuth/company identity setup is operator cost 4 and usually too expensive before a strong proof path exists.

Safe handling:

- Do not attempt company OAuth or impersonate employees without explicit operator approval and program authorization.
- Do not open embedded third-party docs/Drive/Atlassian/internal-looking links just because they appear in a public bundle.
- Preserve the hypothesis compactly, then continue target screening for lower-friction web/API targets.

## Preferred next-target filter after these failures

Prefer targets with all of:

- active bounty/private/fresh update signal;
- self-serve sandbox or free account;
- clear web/API object model;
- two owned users/roles or removable invite/user lifecycle;
- no phone/payment/KYC/OAuth/company-identity gate before controls.
