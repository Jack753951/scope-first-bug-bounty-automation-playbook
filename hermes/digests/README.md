> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# hermes/digests/

Daily Hermes-to-operator digests.

## File naming

`<YYYY-MM-DD>.md` — one per calendar day, UTC. Written by daily_sweep step 9.

## Content shape

```markdown
# Hermes Daily Digest — <YYYY-MM-DD>

Generated <iso ts>.

## What Hermes did today

- <bullet per significant action>

## What changed

- Lanes: <state transitions>
- Scope: <additions / removals>
- Pending intake: <changes>
- CVE matches: <count and pointers>

## What needs operator attention

Cross-link to today's `handoff/operator_inbox_<date>.md`.

## What Hermes is parking until tomorrow

- <bullet per deferred item>

## Drift detection (Mondays only)

- <results of weekly drift check>

## Budget

- Tokens used: <n>
- Claude calls: <n>
- Codex calls: <n>
- USD: <amount>

## Stop conditions / failures

- <bullet per stop / failure event>
```

## Retention

Keep all digests indefinitely in git. They are the audit trail of Hermes' autonomous behaviour.
