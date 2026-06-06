> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Env-backed live-bounty signup secret handling

Session lesson: the operator wants Hermes to reduce repetitive signup friction in authorized live-bounty work by using profile `.env` values similarly to API keys.

## Durable rule

For the cybersec profile, reusable signup fields may be stored in the profile `.env` and used by Hermes for authorized, owned-account setup:

- H1 email alias pattern: `<researcher-alias>+<project>@<researcher-alias>` unless program policy says otherwise.
- Primary signup password: env-backed fixed value.
- Secondary signup password: env-backed value for Account B / clean negative controls.
- Phone numbers: env-backed values, used when the user has authorized phone prefill for this lane/class.

## Handling boundary

Allowed:

1. Prefill deterministic email aliases.
2. Use env-backed password/phone fields for owned-account setup when the program permits self signup and the user has delegated that routine action.
3. Stop and notify the operator when SMS/email OTP, CAPTCHA, KYC/payment, phone-code confirmation, or final submit appears.
4. Record only non-sensitive state such as `password filled from env`, `phone gate reached`, or `operator SMS code needed`.

Forbidden:

- Do not write actual phone numbers, passwords, OTPs, verification links, cookies, bearer tokens, or API keys to memory, repo handoff, Obsidian, screenshots, report drafts, or broad logs.
- Do not ask the user to paste OTPs or verification links into chat.
- Do not treat env-backed phone/password access as permission to continue into payment/KYC, support contact, OAuth/integration, API-token creation, or final report submission.

## Tooling pitfall

Browser automation may place typed values in tool-call arguments or logs. Prefer safer transfer methods if available. If only direct typing is available and the user has authorized automatic fill, avoid repeating the secret in assistant text and keep durable artifacts to secret-free summaries.
