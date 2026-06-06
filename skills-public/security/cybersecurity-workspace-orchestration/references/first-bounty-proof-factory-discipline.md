> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# First-bounty proof-factory discipline

Use this reference when the user asks how to improve the Cybersec Lab toward the first bounty, or when a live-bounty lane starts drifting into ad-hoc UI/anomaly investigation.

## Session lesson

A Front live-bounty lane drifted from the practiced bundle workflow into an Account B/C signup/company/domain provenance investigation. The signal looked interesting (a second owned account appeared as an active teammate with broad permissions), but it lacked a clean low-privilege or removed-user negative control. The later Account C idea also carried high operator cost (email/phone/verification) and was plausibly explained by verified email-domain workspace grouping. The correct project-owner move was to park the line earlier and return to bundle-first proof discipline.

## Project-owner stance

Hermes should act as project owner for this workspace, not just a task follower. The long-term delivery goal is the first reportable bounty. Preserve capability-building, but do not let it dilute the first-bounty sprint.

Prefer this operating model:

1. Pick a practiced bundle before touching the live target.
2. Score the target for first-bounty suitability before spending operator auth effort.
3. Require positive/negative controls before claiming access-control impact.
4. Time-box each target/bundle lane and kill or park low-signal lines quickly.
5. Convert only clear expected-vs-observed mismatches into report packets.

## Target selection gate

For first-bounty work, rank programs by whether they support low-cost control setup:

- self-signup allowed;
- free plan sufficient;
- owned object/resource creation possible;
- low-priv teammate/user possible;
- removed/downgraded user state possible;
- no payment, phone, domain, mailbox, OAuth, or integration required for the first proof;
- web/API access-control bugs are in scope and bounty-eligible;
- direct URLs, IDs, API docs, or permission docs exist;
- rules/scope are clear.

Targets that need high operator cost before a clear signal exists should be parked, not pursued as first-bounty candidates.

## Bundle-first run card

Before live testing, fill this mentally or in an artifact:

```text
Program:
Scope:
Bundle:
Hypothesis:
Report title if true:

Positive control:
Negative control:
Owned object/resource:
Expected matrix:

Allowed actions:
Blocked actions:
Operator cost:
Kill criteria:
Evidence required:
Time box:
Decision:
```

If the report title is vague (for example, "signup behavior seems strange"), do not execute. Reframe into a bundle or park.

## Preferred first-bounty bundles

Prioritize bundles that can produce clean owned-data evidence without scanners or risky state changes:

1. Auth / role separation.
2. Removed or downgraded stale access.
3. Object ownership / IDOR.
4. Metadata-only leak.
5. API/UI permission mismatch, only after token/redaction and operator gates are explicit.
6. Invite/membership lifecycle, only with clean expected role matrix.

## Kill criteria

Kill or park a live line when any of these happen:

- no clean negative control exists;
- no owned object/resource exists;
- behavior is plausibly normal product logic and no documentation contradiction is found;
- operator cost rises to phone/payment/domain/OAuth/mailbox/verification while signal remains weak;
- no clear report title can be written;
- proof would touch customer/non-owned data, secrets, tokens, callbacks, destructive actions, or broad automation;
- 30-60 minutes pass without expected-vs-observed mismatch.

## Evidence standard

A first-bounty proof should show:

- admin/positive control expected behavior;
- low-priv/removed/other-tenant negative control expected denial;
- observed mismatch on owned data only;
- timestamped, redacted screenshots or snippets;
- exact scope/rule reference;
- what was not tested;
- cleanup and stop-before statements;
- no final submission without operator approval.

## Common pitfall

Do not treat a live UI anomaly as a proof lane. An anomaly is only actionable if it maps to a practiced bundle and passes the precondition gate. Otherwise, save it as a parked hypothesis and move to a higher-yield target/bundle combination.