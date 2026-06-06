> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# H1 Freshness Triage Patterns

Use this reference when comparing HackerOne targets for a first-bounty sprint.

## Signals that should quickly park/kill

- `Temporary Bounty Suspension`, disabled rewards, or explicit suspended bounty language: KILL for first-bounty work even if the program was recently updated.
- Immediate phone/KYC/payment/country-specific verification gate before any strong bundle signal: PARK unless the target is unusually compelling.
- Very broad public campaigns with only a few days remaining: fallback only; they may be mined out and time-constrained.

## Signals that can justify asking the operator

- Fresh private opportunity or newly available slot.
- Recently launched/updated scope with medium-sized web/API surface.
- Bounty active, clear Safe Harbor, and self-serve account/object/role surface likely.
- Scarce claim language such as `up to 1 per 30 days` or `Claim your spot`.

## Operator ask shape for scarce claims

Do not click scarce claim buttons on your own. Give the operator a crisp binary decision:

```text
I recommend: claim <program>
Reason: <fresh/private/scope/bounty/surface summary>
Tradeoff: consumes <scarce slot / monthly private opportunity>
Reply: claim <program> / skip <program>
```

## Example decisions

- Fresh private SaaS opportunity with active bounty and manageable scope: ask operator whether to claim.
- Recently updated program with bounty suspended: KILL.
- New regional fintech with immediate country-specific phone gate: PARK unless operator cost is acceptable and signal is already strong.
