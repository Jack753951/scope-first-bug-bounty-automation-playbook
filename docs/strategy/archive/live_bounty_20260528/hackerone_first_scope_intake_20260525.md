> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# <bug-bounty-platform> First Authorized Scope Intake — 2026-05-25

Status: blocked-awaiting-operator-scope
Created: 2026-05-25T03:29:35Z
Route: Phase 5A authorized-assessment readiness
Repo truth: `handoff/current_navigation.md`, `handoff/active_strategy_queue.md`, `programs/_examples/public-bounty.example.json`, `handoff/phase5a_authorized_live_target_dry_run_template.md`

## Boundary

This file does not authorize target-touching work by itself. It is the intake packet the operator can fill from a <bug-bounty-platform> program policy before Hermes turns anything into `programs/<program-slug>/scope.json` or runs any live-target command.

Until completed and checked:

```text
blocked-awaiting-scope
```

Hard blocks unless explicitly permitted by the <bug-bounty-platform> policy and mirrored into `programs/<program-slug>/scope.json`:

```text
public/live probing
broad scanning
active vulnerability scanning
intrusive fuzzing
credential brute force
social engineering
DoS / stress / rate-limit testing
state-changing destructive tests
payment / abuse flows
external callback / OAST / tunnel
real user data access or collection
report submission
```

## What to paste/provide

Please provide only the program policy/scope facts needed for authorization. Do not paste private tokens, cookies, credentials, report drafts, user data, or non-public customer data.

### 1. Program identity

```text
<bug-bounty-platform> program handle/name:
Program policy URL:
Policy/version date shown by <bug-bounty-platform>:
Your <bug-bounty-platform> account authorized for this program? yes/no:
Any private/invite-only caveat? yes/no/details:
```

### 2. In-scope assets

For each asset, preserve exact type and constraints from <bug-bounty-platform>.

```text
Asset 1:
  type: domain / wildcard / URL / API / mobile / source repo / hardware / other
  value:
  eligible for bounty? yes/no/unknown
  max severity / special rules:
  notes:

Asset 2:
  type:
  value:
  eligible for bounty? yes/no/unknown
  max severity / special rules:
  notes:
```

### 3. Out-of-scope assets/actions

```text
Out-of-scope domains/URLs/apps:
Explicitly forbidden vulnerability classes:
Explicitly forbidden tools/actions:
Third-party/provider exclusions:
Customer/user-data restrictions:
Testing window or blackout periods:
Rate limits / automation limits:
```

### 4. Allowed first-test lane

Pick exactly one low-risk first lane unless the program policy says otherwise.

Preferred first live-target lanes:

```text
access control / IDOR with throwaway accounts
role/session boundary check with throwaway accounts
file exposure / metadata leakage without private data access
safe reflected/stored XSS marker only if policy allows
upload validation/retrieval only with benign test files if policy allows
```

Proposed first lane:

```text
Lane:
Why this lane is in-scope:
Accounts/roles available:
Safe marker/test data available:
Expected max request budget:
Stop conditions:
```

High-risk lanes remain blocked for the first test unless you explicitly quote policy allowance and approve them separately:

```text
SSRF with callback / OAST
path traversal file read
RCE / command injection
deserialization
payment / business-abuse flows
anything destructive or state-changing outside throwaway data
```

## Conversion checklist for Hermes

After operator fills this file, Hermes must do these before any target-touching work:

```text
[ ] Create `programs/<program-slug>/scope.json` from `programs/_examples/public-bounty.example.json` shape.
[ ] Validate exact in-scope and out-of-scope assets against <bug-bounty-platform> policy text.
[ ] Add/update only the minimum global `config/scope.txt` entries needed for the selected asset, with operator confirmation.
[ ] Run the program policy validator / dry-run gate.
[ ] Create a single-lane live-target dry-run packet from `handoff/phase5a_authorized_live_target_dry_run_template.md`.
[ ] Confirm allowed automation, rate limits, account/test-data availability, redaction rules, and report-submission rules.
[ ] Start with passive/manual reconnaissance or a bounded low-risk request budget only.
```

## Current decision

```text
verdict: blocked-awaiting-operator-scope
reason: waiting for the operator to provide a <bug-bounty-platform> program policy/scope package
no target touched: true
no scope/config authorization change: true
```
