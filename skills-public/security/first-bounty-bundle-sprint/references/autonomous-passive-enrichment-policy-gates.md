> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Autonomous Passive Enrichment + Operator Gate Pattern

Use when the operator says to continue collecting information until they are actually needed.

## Core rule

Hermes should autonomously perform all non-target-touching, non-secret, public/passive enrichment before asking the operator for help.

Do autonomously:

- Public program preview reading.
- Public bounty directory/source intake.
- Public documentation reading, including API docs, `llms.txt`, changelogs, security pages, and disclosed reports.
- Public advisory/CVE/GHSA/KEV/vendor-patch collection.
- Source/local-only reasoning for latest-vulnerability candidates.
- Candidate scoring, attack-surface hypothesis generation, and `EXECUTE / PASSIVE_ONLY / PARK / KILL` recommendations.
- Compact repo artifacts that separate facts, hypotheses, blockers, and next operator-needed actions.

Stop and ask the operator only for:

- CAPTCHA, OTP, 2FA, email verification, phone, or recovery-code steps.
- Non-public logged-in policy details that cannot be safely fetched without exposing session/secret material.
- Applying/joining/claiming when the action consumes scarce opportunity, changes account state, or has unclear account/reputation impact.
- Account creation, free trial setup, organization/workspace creation, API key/token creation, OAuth/SSO/integration setup, payment, KYC, or production-side changes.
- Any live target contact beyond ordinary public page reads, including scans, fuzzing, exploit attempts, OAST/callbacks, or state-changing proof.
- Safe phrase / operator gate / final report submission.

## Artifact shape

Create or update a compact passive enrichment artifact:

```text
# Passive Candidate Enrichment — <date>

Boundary: public/passive reading only; no target testing, no scanning, no fuzzing, no exploit, no OAST/callback, no login/session scraping, no account mutation, no credential handling, no report submission.

## Candidate <n> — <program>
Sources checked:
Public facts:
Public docs / attack surface:
Attacker hypotheses, bounded:
Score before logged-in policy:
Blockers requiring operator/logged-in UI:
Decision:
```

## First-bounty ranking heuristic from this session

When public enrichment identifies a program with a paid bounty preview and rich API/docs surface, prefer that over sensitive HR/consumer workflows until logged-in policy proves otherwise.

Example pattern captured:

- <program-redacted> Public Bug Bounty: public Intigriti preview exposed bounty range, 2FA requirement, and rich docs/API surface around organization management, members/groups, privileges, API keys, sources/connectors, secured search, security identities, Push/Search/Source APIs, analytics write API, Atomic/Headless UI, temporary access, notifications, and resource snapshots. This produced strong bounded hypotheses for API/UI permission mismatch, metadata leak, tenant/search-result visibility, source ownership, API-key privilege confusion, analytics abuse, and stale temporary access.
- <program-redacted>.be Dedicated BBP: public disclosure page and HR/job surfaces suggested possible account/profile/application workflows, but sensitive personal-data boundaries and unknown reward/scope made it lower priority until logged-in policy review.

## Pitfalls

- Do not ask the operator to do public research that Hermes can do safely.
- Do not turn passive enrichment into live reconnaissance. Public docs are okay; target probing is not.
- Do not store private program text, secrets, cookies, tokens, OTPs, phone numbers, or account-sensitive details in the skill or memory.
- Do not let `latest vuln` research drift into detector sprawl without a scoped target or local/passive proof path.
- Do not convert the project into a learning track when the operator says they will handle learning separately; keep the repo focused on first-bounty execution.
