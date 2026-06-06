> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# HackerOne alias signup gates for live bounty lanes

Use this when a live bounty lane reaches an account signup/auth form after scope has already been confirmed.

## Durable lesson

If the operator has already supplied a HackerOne username and alias convention, do not bounce the work back to the operator as an unknown identity gate. Use the alias convention proactively for non-secret form fields, then stop only at true operator gates such as phone, OTP, CAPTCHA, password, payment/KYC, or final submission.

For this user in the cybersec lab, the known H1 username is `<researcher-alias>`; plus-addressing can be used for per-program signups:

```text
<researcher-alias>+<program-or-project>@<researcher-alias>
```

Example:

```text
<researcher-alias>+<program-redacted>@<researcher-alias>
```

Do not store or repeat full phone numbers, OTPs, passwords, cookies, API keys, verification links, or other secrets in repo artifacts, memory, or final summaries.

## Workflow

1. Confirm authorization first:
   - logged-in HackerOne scope/assets captured or otherwise verified;
   - program scope file created/updated;
   - global scope whitelist contains only explicitly confirmed target hosts;
   - dry-run in-scope pass and out-of-scope fail-closed checks pass.
2. Use noVNC/Kali browser for the live form; avoid separate browser sessions when the operator expects VM UI continuity.
3. Fill non-secret identity fields yourself when the values are known and policy-consistent:
   - H1 alias email using plus-addressing;
   - safe researcher labels for first/last name when acceptable;
   - company name using the program-required bug-bounty marker if applicable;
   - generic job title such as Security Researcher;
   - conservative industry/company-size choices when the field requires a value.
4. Stop at true operator gates:
   - phone number unless the operator explicitly authorizes transient use;
   - OTP/email verification/CAPTCHA;
   - password manager or real password entry;
   - payment, billing, KYC, recovery, support/customer interaction;
   - report submission.
5. If the operator explicitly provides a phone number and authorizes use:
   - use it once, transiently, only in the current target form;
   - do not save it, echo it back, write it to handoff/memory, or reuse it on another target;
   - stop immediately at SMS/voice OTP and let the operator handle verification or report only a non-sensitive status.
6. Record only sanitized state in lane artifacts, e.g.:

```text
signup_prefilled_except_phone
blocked_phone
blocked_email_verification
blocked_captcha
front_signup_complete
stop
```

## Pitfalls

- Do not ask the operator to manually summarize scope if the logged-in HackerOne UI is already available in Kali/noVNC and the task is to operate that UI.
- Do not treat a known H1 alias convention as an operator gate.
- Do not over-redact so much that you stop useful work: non-secret, policy-consistent signup fields can be filled, but secret/PII gates still require explicit transient authorization or operator input.
- If the official signup flow redirects through a host not listed as a test asset (for example a marketing/signup host), treat it only as the auth/signup gate reached from an in-scope app, not as expanded testing scope.
