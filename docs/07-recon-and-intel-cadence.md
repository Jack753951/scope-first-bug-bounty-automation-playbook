# 07 — Recon and Intelligence Cadence

Status: public methodology

## Cadence tiers

| Tier | Examples | Default boundary |
| --- | --- | --- |
| Minute | certificate transparency, scope-change alerts, advisory feeds | passive/feed-only |
| Hourly | diffs on changed assets, public docs changes, disclosed-report mining | passive or dry-run |
| Daily | inventory refresh, tech fingerprints, recent advisories, candidate scoring | passive/candidate-only |
| Weekly | deeper wordlist planning, JS endpoint extraction, bundle review | scope-gated before contact |
| Monthly | strategy metrics, capability-library cleanup, stale lane review | planning/review |

## Candidate scoring dimensions

- authorization clarity;
- product/surface fit for existing proof bundles;
- account/data prerequisites;
- policy exclusions;
- expected proof quality;
- request budget and cleanup feasibility;
- bounty/report value;
- time-to-first-meaningful-evidence.

## Fail-closed examples

- Program policy unavailable or login-only.
- Asset table ambiguous.
- Technique not explicitly allowed.
- Account creation requires verification not yet cleared.
- Proof would require non-owned/customer data.
- Evidence redaction cannot be guaranteed.
