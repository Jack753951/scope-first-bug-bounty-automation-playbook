> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Daily SOP — Bug Bounty Automation Platform

The operator should spend minutes on decisions, not hours on manual recon. Agents and scheduled jobs should produce short inbox items with EXECUTE / PASSIVE-ONLY / PARK / KILL recommendations.

## 1. Morning inbox check — 5 minutes

Read:

- `handoff/current_navigation.md`
- `handoff/active_strategy_queue.md`
- latest operator inbox / lane runner status if present
- latest `intelligence/cve_briefs/` item when CVE lane is active

Operator decision types:

- approve/deny a scarce opportunity or setup cost;
- complete auth / OTP / CAPTCHA / phone / payment / KYC;
- choose between top candidates when strategy tradeoff matters;
- final approval before report submission.

## 2. Automated candidate generation

Workers should keep the following queues fresh:

- H1/latest/new/updated target shortlist.
- CVE/RCE detector candidates.
- Program-specific lane states under `programs/<slug>/`.
- Evidence/report packets under `reports/` when candidates mature.

Each candidate should include:

```text
Program / asset:
Scope basis:
Lane type:
Report title if true:
Positive control:
Negative control:
Owned object/resource:
Allowed actions:
Blocked actions:
Operator cost:
Evidence needed:
Decision: EXECUTE / PASSIVE-ONLY / PARK / KILL
Next action:
```

## 3. Execution bias

Prefer:

- fresh/private/recently updated H1 targets;
- self-serve SaaS with owned A/B controls;
- access-control / lifecycle / API-UI mismatch bundles;
- latest CVE detector lanes that can be reduced to passive/version checks on live targets and local lab validation.

Avoid spending operator time on:

- phone/payment/KYC unless signal is already strong;
- sales/demo-only targets;
- known-CVE live exploitation;
- ambiguous signup/session drift;
- no-control findings.

## 4. Evidence and report packet

A candidate is report-ready only when it has:

- scope reference;
- expected-vs-observed behavior;
- positive and negative controls;
- owned object/resource labels only;
- redacted screenshots or request snippets;
- proof boundary and what was not tested;
- cleanup/no-customer-data statement;
- final operator approval pending.

## 5. End-of-day closeout

Agents should update:

- `handoff/active_strategy_queue.md`
- `handoff/current_navigation.md`
- relevant `programs/<slug>/` lane state
- report/evidence packet if candidate exists

End every lane with one of:

- EXECUTE: next bounded action is clear.
- PASSIVE-ONLY: live action limited to fingerprint/version/exposure checks.
- PARK: useful but missing controls/scope/operator setup.
- KILL: not worth more time.
