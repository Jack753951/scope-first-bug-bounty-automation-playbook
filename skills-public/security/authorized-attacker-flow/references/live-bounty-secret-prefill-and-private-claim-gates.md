> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Live bounty secret prefill and H1 private claim gates

Session-derived pattern from Cybersec first-bounty work.

## H1 private opportunity claim

If HackerOne shows a private opportunity that is a strong target and the only visible cost is the private-opportunity cadence/slot (for example `up to 1 per 30 days`), and there is no account/reputation-risk warning, Hermes may claim/open it directly for this user.

Still stop before:
- auth/login
- OTP/CAPTCHA/email verification
- phone
- payment/KYC/billing
- OAuth/integration/API-token/credential claim
- final report submission
- any unclear account-risk action

Record the slot/cadence cost in the run card or accepted-changes artifact.

## Email prefill

For H1 program signups, prefill the registration email using the user's alias pattern when policy permits:

```text
<researcher-alias>+<program-slug>@<researcher-alias>
```

Do this before asking the operator, unless the program requires a different format or rejects plus aliases.

## API-key-like secrets in profile env

The user may store reusable live-bounty secrets in the active Hermes profile `.env`, not in memory/repo/handoff/Obsidian/chat:

```env
HACKLAB_PHONE_PRIMARY_E164=+<countrycode><number>
HACKLAB_PHONE_SECONDARY_E164=+<countrycode><number>
HACKLAB_SIGNUP_PASSWORD=<primary signup password>
HACKLAB_SIGNUP_SECONDARY_PASSWORD=<secondary/account-b signup password>
HACKLAB_H1_EMAIL_PREFIX=<researcher-alias>
```

Use only presence/length checks when verifying these variables; do not print values.

## Browser-entry rule

Even if a phone number or password exists in `.env`, do not send it through browser automation by default because the tool-call argument and session/tool logs may contain the value.

Default behavior:
- email: prefill automatically from alias rule
- password: use `.env` only after explicit per-use authorization such as `allow fill <target> primary password`
- secondary password: use for Account B / clean negative control only after explicit per-use authorization
- phone: use `.env` only after explicit per-use authorization
- OTP/CAPTCHA/verification links: always operator-handled; never store or request them

If the user explicitly accepts the risk for a specific fill action, fill the field, stop at submit/verification gates, and do not write the secret value to artifacts.
