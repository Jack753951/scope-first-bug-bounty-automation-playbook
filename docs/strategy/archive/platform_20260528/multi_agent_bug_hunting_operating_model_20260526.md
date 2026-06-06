> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Multi-agent bug-hunting operating model — 2026-05-26

Status: proposed operating model / no target touched
Boundary: planning, role routing, and offline artifact design only. This does not authorize scanning, fuzzing, exploitation, callbacks, scope expansion, credential handling, or report submission.

## Thesis

The project can reach a high-performing bug-bounty workflow, but not by making one agent browse harder. The advantage is role separation and parallel reasoning:

- Hermes owns safety gates, scope, memory routing, evidence discipline, and final synthesis.
- Strategy/Cowork-style agents own target/lane selection, product modeling, tactical preview, no-finding lessons, and report narrative.
- Engineering/Codex/Claude-Code-style agents own deterministic tools: coverage diff, A/B matrix helpers, redaction, schema validators, bundle indexes, and tests.
- Safety reviewers own fail-closed checks, forbidden-flow detection, scope validation, and operator-gate triggers.
- The operator owns authentication, OTP/CAPTCHA/phone/email, final live activation gates, and report submission.

## Current gap

Current project assets prove legal workflow and safety discipline, but the system is not yet a high-yield hunter loop because these loops are incomplete:

1. Passive target/lane scoring exists, but must become routine and stricter.
2. A/B account/object matrix exists as a plan, but needs repeated execution data.
3. Bundle freshness exists as intake/proposal, but lacks coverage-delta automation.
4. No-finding feedback exists, but must drive target rejection and next-lane selection more aggressively.
5. Multi-agent review exists for engineering/safety, but is not yet used as a daily bug-hunting crew with separate hypotheses.

## Multi-agent crew pattern

For each live-bounty candidate, use five roles:

### Role 1 — Scout / Target Selector

Inputs:
- public program metadata
- policy snippets
- docs/SDKs/release notes
- disclosed reports if public
- current no-finding feedback rules

Output:
- score using `docs/strategy/live_bounty/live_bounty_high_hit_rate_target_filter_20260526.md`
- recommended lane or park decision
- prerequisites: Account B, tenant B, role matrix, safe object family, API docs

Allowed actions:
- passive OSINT only

### Role 2 — Product Modeler / Hypothesis Generator

Inputs:
- selected target facts
- visible product shape
- docs/API/schema/release notes
- attack-class matrix

Output:
- 5–10 hypotheses before narrowing
- object/role/tenant/state model
- which hypotheses are `safe_now`, `later_only_needs_plan`, `blocked_by_policy`, `blocked_by_missing_control`, or `blocked_high_risk`

Allowed actions:
- planning only until exact scope and operator prerequisites exist

### Role 3 — Safety Gate / Scope Reviewer

Inputs:
- program scope artifact
- `config/scope.txt`
- proposed lane
- target-touching plan

Output:
- PASS / BLOCK / ESCALATE
- forbidden flows
- stop conditions
- required operator gates

Allowed actions:
- local file checks, dry-run checks, policy verification

### Role 4 — Matrix Executor / Evidence Clerk

Inputs:
- approved one-lane plan
- Account A/B labels only
- safe owned object labels only

Output:
- redacted A positive / B negative matrix
- request/interaction budget
- evidence status: surface_only, candidate, report_ready, blocked

Allowed actions:
- only low-speed, browser/manual/noVNC or approved request replay within exact scope; no scanner/fuzzer/DAST by default

### Role 5 — Learning Integrator / Bundle Maintainer

Inputs:
- result packet
- no-finding log
- bundle inventory
- vuln-intel candidates

Output:
- selection rule update
- bundle update proposal
- new detector/helper/test proposal if needed
- next best target/lane

Allowed actions:
- repo docs/tooling updates only, no target touch

## Recommended per-lane workflow

1. A0 passive scout shortlist, 2–3 candidates max.
2. Parallel hypothesis generation by 2–3 agents with different focuses:
   - authorization/object model
   - API/docs/release-note diff
   - safety/prerequisite blockers
3. Hermes synthesis chooses one lane or parks the target.
4. Operator handles auth/OTP/phone/email if needed and replies with safe phrase only.
5. Matrix executor runs exactly one bounded matrix.
6. Safety reviewer checks evidence for overreach/PII/third-party data.
7. Report reviewer decides: report_ready, candidate_needs_control, no_finding, parked.
8. Learning integrator updates feedback and bundle/freshness deltas.

## What multi-agent should optimize

Use multiple agents for divergent thinking and independent review, not for parallel live probing.

Good parallelization:
- target scoring vs product modeling vs policy safety review
- two independent hypothesis lists before selecting one lane
- implementation + safety + architecture review for tooling changes
- report-readiness review separate from evidence collection
- no-finding root-cause review separate from original tester

Bad parallelization:
- multiple agents browsing the same live target at once
- multiple agents running requests without shared budget/state
- agents independently expanding scope
- agents self-approving their own findings
- parallel scanners/fuzzers/DAST

## 30-day maturity ladder

Week 1:
- Execute <program-redacted> Account B gate only if safe object exists; otherwise park quickly.
- Add bundle freshness coverage-delta tool.
- Add A/B matrix artifact template.

Week 2:
- Run 2–3 passive target previews with multi-agent hypothesis generation.
- Select only one high-fit target for live A2 viability.
- Update no-finding feedback after every parked lane.

Week 3:
- Build object ownership ledger and redacted evidence packet generator.
- Add JS/API endpoint diff helper if selected target exposes rich frontend/API docs.

Week 4:
- Conduct a full multi-agent lane: scout, modeler, safety, executor, report reviewer, learning integrator.
- Measure: time-to-park, prerequisites found, candidate quality, report readiness, feedback quality.

## Success metrics

Do not measure only number of findings. Track:

- target candidates rejected before login because low-fit
- percentage of lanes with Account B/tenant/object prerequisites satisfied
- time-to-park for low-fit targets
- number of distinct safe hypotheses generated per preview
- candidate-to-report-ready conversion rate
- no-finding lessons that changed the next selection
- bundle freshness gaps closed
- evidence packets that pass redaction/safety review first time

## Safety invariants

- No raw secrets, OTPs, phone numbers, cookies, tokens, full emails, verification links, or PII in artifacts.
- No target-touching without exact scope and policy artifact.
- No scanner/fuzzer/DAST/callback/OAST/upload/parser/workflow/run-script/integration/API-key flows without separate explicit plan.
- No report submission without operator approval.
- Operator handles auth/OTP/CAPTCHA/final submit.
