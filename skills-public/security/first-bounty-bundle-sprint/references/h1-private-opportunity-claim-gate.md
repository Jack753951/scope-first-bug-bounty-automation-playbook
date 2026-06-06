> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# H1 private opportunity claim gate

Session lesson: when using HackerOne Opportunity Discovery for first-bounty target selection, `Claim your spot` on an available private opportunity can be a scarce account-side action because H1 may show a cadence such as `up to 1 per 30 days`.

Operator preference captured during Syfe selection:

- Treat private-opportunity claims as pre-authorized when the only visible cost is consuming the slot/cadence and there is no warning about reputation, account health, terms risk, payment, KYC, or irreversible program/account effects.
- Do not stop just to ask whether to spend the private-opportunity slot in that low-risk case; Hermes should act as project owner and claim the high-ranked freshness/private candidate.
- Still stop before auth/login, OTP, CAPTCHA, phone, payment, KYC, OAuth/integration activation, API-token/credential handling, final report submission, or any unclear account-risk action.

Recommended decision wording:

```text
Claim directly: private opportunity has strong target signal; visible cost is only slot/cadence; no account-risk warning observed.
Stop/ask: claim flow presents account-risk warning, identity/KYC/payment requirement, credential/secret handling, or final submission.
```

Why this belongs in the first-bounty loop:

- Private opportunities can be higher yield than public mined-out programs.
- Asking the operator for every slot spend slows the freshness-first strategy.
- The real operator gates remain secrets/auth/OTP/phone/payment/KYC/final submit, not ordinary H1 opportunity claiming.
