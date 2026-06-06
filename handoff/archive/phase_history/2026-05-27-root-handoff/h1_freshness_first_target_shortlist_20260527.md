> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# H1 freshness-first target shortlist — 2026-05-27

Status: needs operator decision for private opportunity claim
Mode: H1/program-page + minimal low-speed public landing-page checks only; no scanning, fuzzing, tokens, customer/non-owned data, or report submission.

## Context

<program-name> is parked because it lacks a clean low-priv/removed/downgraded negative control. Operator corrected the selection strategy: prefer latest/new/updated targets because older popular programs are often mined out. Operator is also a human plugin/reviewer; Hermes remains project owner.

## Candidates observed

### <program-slug> — private opportunity

Visible H1 card:

- Section: Available private opportunities (up to 1 per 30 days)
- Program: <program-slug>
- Tags: Domain 7, Android Play Store 1, iOS App Store 1
- Gold Standard
- Bounty: $50-$1k
- Visible metrics: 22 / 21 / 88%
- Action button: Claim your spot

Decision:

```text
RANK 1, but needs operator decision before claiming.
```

Reason:

- Strong freshness/private signal.
- Lower likely competition than public mined-out programs.
- Scope shape may include web/mobile; web first-bounty suitability unknown until after claim.
- Claiming consumes a scarce H1 private opportunity slot (up to 1 per 30 days), so this is an operator-resource decision.

Operator question:

```text
Do we claim the <program-slug> private opportunity slot?
```

If yes: create <program-slug> run card and proceed only with H1 scope/policy review first, then low-speed owned-account precondition checks. Stop at auth/OTP/CAPTCHA/phone/payment/KYC/final-submit.

If no: continue public campaign target screening.

### Banco Plata — parked

Observed H1 signals:

- Launched Jan 2026.
- Scope updated Apr 27 2026.
- Open Scope, Managed by <bug-bounty-platform>, Gold Standard Safe Harbor, Platform Standards.
- Response efficiency 97%.
- Scope includes:
  - iOS app id — in scope, critical, bounty eligible.
  - Android app id — in scope, critical, bounty eligible.
  - `*.platacard.mx` — wildcard, in scope, critical, bounty eligible.
  - `*.bancoplata.mx` — wildcard, in scope, critical, bounty eligible.
  - whistleblowing paths out of scope / ineligible.
- Rewards visible up to critical $3,000-$5,000.

Minimal public landing-page check:

- `bancoplata.mx` loads a credit-card application landing page.
- Clicking the application CTA reaches a phone-number gate with Mexico country code.

Decision:

```text
PARK
```

Reason:

- Good freshness and scope.
- But immediate signup/control setup requires Mexico phone / financial-card application context.
- Operator cost is too high for current signal.

### Discourse — killed for bounty-first

Observed H1 signals:

- Updated rewards page May 13 2026.
- Open-source Discourse program, managed by H1, collaboration enabled.
- Page states Temporary Bounty Suspension as of Apr 23 2026; bounties remain suspended.

Decision:

```text
KILL_FOR_FIRST_BOUNTY
```

Reason:

- Freshly updated, but bounty suspension makes it poor for first-bounty goal.
- Can be source-learning later, not current live sprint.

### Campaign cards — fallback public screening

Visible campaign cards:

- <program-redacted>: ends in 30 days, wildcard 81, domain 37, up to $30k, 100% metric visible.
- OPPO: ends in 3 days, hardware/mobile/domain-heavy, up to $23k, Gold Standard.
- Hilton: ends in 2 days, CIDR 9, wildcard 4, domain 4, up to $12k.
- Circle BBP: ends in 5 days, smart contract/source/domain, up to $15k.

Preliminary ranking if <program-slug> is not claimed:

1. <program-redacted> — best campaign freshness window, but huge scope; needs H1 scope/policy triage before target contact.
2. Hilton — strong brand/campaign, short time window; likely heavily mined and may require account/travel contexts.
3. Circle BBP — good campaign but smart-contract-heavy; not ideal unless switching bundle class.
4. OPPO — huge hardware/mobile mixed surface; low first-bounty fit.

## External advisory result

Hermes delegate_task review agreed:

1. <program-slug> is the next best candidate but requires operator decision because Claim your spot is a scarce account side effect.
2. Banco Plata should park due Mexico phone gate.
3. Discourse should not be used for bounty-first due bounty suspension.
4. If <program-slug> is declined, continue campaign screening, likely <program-redacted> before Hilton/Circle/OPPO.

## Current decision

```text
NEEDS_OPERATOR_DECISION: Claim <program-slug> private opportunity slot? yes/no
```

No secret, OTP, cookie, token, phone number, customer/non-owned data, or report submission occurred.
