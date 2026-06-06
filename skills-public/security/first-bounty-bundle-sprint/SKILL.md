> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

---
name: first-bounty-bundle-sprint
description: Use when driving Cybersec Lab toward the first reportable bounty with live targets, bundle-first proof discipline, target scoring, multi-role tactical perspectives, and fast execute/park/kill decisions without adding conservative review gates.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [security, bug-bounty, first-bounty, bundle-first, multi-agent, tactical-review]
    related_skills: [authorized-attacker-flow, cybersecurity-workspace-orchestration, owasp-single-vuln-lab-wave]
---

# First Bounty Bundle Sprint

## Overview

This skill turns Cybersec Lab from a broad research platform into a focused first-bounty delivery loop.

Core rule:

```text
target scoring -> practiced bundle -> multi-role tactical lens -> control/precondition gate -> minimal proof -> execute/park/kill -> report packet if candidate
```

Use external strong agents aggressively for tactical breadth, dissent, evidence critique, and alternate attack paths. Prefer Claude Code / Codex / Cowork or Hermes `delegate_task` for non-trivial target ranking, tactic selection, evidence review, and platform-extraction decisions, but do not let their review become a new safety gate or make Hermes more conservative than the actual authorization boundary requires. Reviewers advise. Hermes synthesizes. Concrete blockers stop work; generic caution does not.

## When to Use

Load this skill when:

- The user asks how to get the first bounty / first reportable vuln.
- Selecting or triaging live bug-bounty targets.
- A live target has a SaaS/web/API surface and we need to choose a proof lane.
- A UI or signup anomaly appears and risks distracting from practiced bundle execution.
- Multi-agent tactical review would improve attacker perspective, boundary clarity, evidence quality, or target prioritization.
- A candidate needs execute/park/kill decision discipline.

Do not use this skill to authorize:

- Out-of-scope targets.
- Live scanners/fuzzers/DAST/exploits/callbacks/OAST/tunnels without explicit approval.
- Non-owned/customer data access.
- Secret/token/cookie/OTP/password/phone/API-key/verification-link storage.
- OAuth/integration/channel/mailbox/API-token/billing/payment/report-submission activation without explicit operator approval.

## Project Owner Stance

Hermes is the project owner for this lane.

Hermes should:

1. Preserve the long-term objective: first reportable vuln / first bounty.
2. Choose the next strategy instead of asking the operator to manage process details.
3. Treat the operator as a high-value human plugin / external reviewer, not as a passive permission clerk: use the operator for target intuition, freshness judgment, tactical disagreement, account-control setup, auth/OTP/CAPTCHA/phone/final-submit gates, and concrete decisions where human context materially improves speed or quality.
4. Ask the operator only for useful interventions: auth/OTP/CAPTCHA/phone/final submit, target-selection correction, control setup, or concrete blockers. Do not offload project ownership, public research, or process management to the operator.
5. When the operator says to proceed until needed, autonomously gather public/passive information first: public program previews, public docs/API references, advisories, source/local notes, and candidate scoring. Stop only at real gates such as non-public logged-in policy, CAPTCHA/OTP/2FA, scarce account-state actions, account/API/trial setup, live target testing, safe phrase, or final submit.
6. Avoid wasting operator cost on high-friction, low-signal lines.
6. Enforce bundle-first discipline.
7. State explicitly when no practiced bundle was used.
8. Redirect away from ambiguous UI/signup/domain/session provenance drift.

### Strong attacker mindset, bounded execution

The operator wants stronger attacker thinking in this project. For first-bounty work, do not let safety/process language collapse into passive-only hesitation or generic caution. Think like a high-output bounty hunter, then execute like a professional researcher inside authorization boundaries.

Required stance:

- Generate aggressive hypotheses: stale access, IDOR, role/tenant confusion, API/UI mismatch, invite lifecycle breaks, metadata leaks, direct-URL/API bypass, source/advisory diff pivots, and business-logic abuse paths.
- Move quickly through `EXECUTE / PARK / KILL` decisions; do not spend hours on weak signup/session anomalies when no report title, owned object, or negative control exists.
- Treat generic caution, reviewer preference for more process, or abstract risk as advisory only. Stop only for concrete authorization, scope, safety, data, credential, destructive-action, or evidence blockers.
- If scope/program policy and owned controls are clear, proceed to the smallest bounded proof rather than adding another policy/review artifact.
- Keep execution bounded: no out-of-scope contact, no customer/non-owned data, no secrets/OTP/token storage, no destructive or evasive actions, no final submission without operator gate.

Default phrase for this stance: `aggressive hypotheses, bounded execution`.

## Target Scoring Gate

Before touching a new live target beyond normal authorized first contact, score whether it is suitable for a first-bounty sprint.

Reference: `references/first-bounty-target-source-intake.md` captures the target-source intake pattern from the H1/Bugcrowd/Intigriti/YesWeHack registration phase, including how to keep login/friction issues from blocking first-bounty work.

Reference: `references/h1-freshness-triage-patterns.md` captures compact HackerOne freshness triage shortcuts for private opportunities, suspended bounties, phone/KYC gates, and scarce claim decisions.

Reference: `references/target-source-intake-platforms.md` captures first-bounty platform/source priority after this user registered Bugcrowd and Intigriti: keep H1 primary, add Bugcrowd + Intigriti early, use YesWeHack as backup, and collect/score 5 candidate programs per new source before any target testing.

Reference: `references/latest-rce-detector-lane-correction.md` captures the latest-vuln lane correction: when the user asks for fresh remote-control/RCE CVEs, search and rank RCE candidates explicitly, then split into local detector EXECUTE, live PASSIVE-ONLY, and live exploit PARK/KILL rather than substituting a safer but off-target data-leak lane.

Reference: `references/latest-vuln-lane-freshness.md` captures the parallel latest-vulnerability lane rule: current-year and preferably last 1-2 months for the active lane; older high-quality detectors are `reference/fallback`, not the primary freshness lane.

Reference: `references/target-source-platform-intake.md` captures the recommended platform-source order and intake discipline for first-bounty target discovery: HackerOne as the existing primary source, Bugcrowd and Intigriti as high-priority registered sources, YesWeHack as backup/diversity, with HackenProof/Immunefi/Synack deferred unless the target class changes. Use it before testing new programs so the work stays candidate-scoring-first rather than signup/testing-first.

Reference: `references/freshness-first-vuln-target-lanes.md` captures the user's clarified high-value zones: latest vulnerabilities and latest targets. Prioritize the intersection of fresh vulnerability × fresh/under-tested/scoped bounty target; otherwise run compact `fresh_vuln_lane` and `fresh_target_lane` records without letting either detector work or signup drift sprawl.

Reference: `references/autonomous-passive-enrichment-policy-gates.md` captures the operator preference that Hermes should autonomously gather all safe public/passive information and only ask the operator for real gates: CAPTCHA/OTP/2FA, non-public logged-in policy, scarce account-state actions, account/API/trial setup, live target testing, safe phrase, or final submission. It also records the <program-redacted>/<program-redacted> passive enrichment pattern and the pitfall of turning first-bounty work into a learning track when the operator handles learning separately.

Reference: `references/novnc-browser-operator-gate-pattern.md` captures the noVNC/browser correction: when Kali/noVNC or a logged-in browser may already be available, Hermes must first try the existing browser route itself and only ask the operator after a real CAPTCHA/OTP/2FA/terms/account-action/live-test gate appears.

Reference: `references/h1-novnc-scope-csv-run-card-pattern.md` captures the H1/noVNC pattern from this sprint: use Kali SSH + `xdotool`/screenshots when noVNC canvas is awkward, read H1 policy/scope autonomously, download and parse H1 scope CSVs, compare them against operator-owned `config/scope.txt`, and stop at scarce claim or live-target gates.

Preferred target traits:

Freshness rule: prefer newly launched, newly invited, recently updated, or bounty/scope-changed programs when other factors are comparable. Older popular programs are often already heavily mined; do not over-invest unless they have a fresh asset, new scope, new bounty, unusual product surface, or unusually clean owned-control bundle.

| Criterion | Good | Bad |
|---|---|---|
| Freshness | newly launched/updated/invited/scope-changed | old popular target with no fresh change |
| Signup | self-serve | sales/demo/manual approval only |
| Cost | free plan enough | payment/KYC required |
| Operator burden | no/low OTP, no phone | phone/payment/domain/OAuth required early |
| Controls | admin + low-priv possible | only one role/account |
| Owned object | project/task/file/inbox/resource creatable | empty state only / needs real customer data |
| Scope | web/API access-control in bounty | unclear/private/out-of-scope |
| Product model | roles, teams, tenants, object IDs | mostly static/marketing |
| API/docs | docs/direct URLs visible | opaque with no object model |

Use this quick score:

```text
freshness: 0-3          # new/updated/invited/scope-changed beats old mined-out targets
self_signup: 0-2
free_plan: 0-2
low_priv_control: 0-3
owned_object: 0-3
scope_clarity: 0-2
operator_cost_low: 0-3
access_control_surface: 0-3
api_or_direct_url_surface: 0-2
Total /23
```

First-bounty priority:

- 15-20: strong target, proceed to bundle precondition gate.
- 10-14: possible, only proceed if operator cost is low and bundle fit is clear.
- <10: park unless user explicitly selects it.

## Operator Cost Score

Track operator cost before continuing.

### Env-backed operator credential convenience

For this user's cybersec profile, registration convenience secrets such as fixed signup passwords and phone numbers may live in the profile `.env` like API keys. In live bounty signup flows, Hermes may prefill the deterministic H1 email alias and env-backed password/phone fields when needed, then stop at OTP/CAPTCHA/email-verification/final-submit gates. Do not record phone numbers, passwords, OTPs, verification links, cookies, or tokens in memory, repo handoff, screenshots, or reports. If a tooling path would expose a secret in tool-call arguments or logs, prefer a safer transfer path when available; otherwise be explicit about the exposure tradeoff and keep the secret out of durable artifacts.

Reference: `references/env-backed-signup-secret-bridge.md` captures the preferred class-level pattern for ignored env mirrors plus symbolic-key scripts that fill signup fields in Kali/noVNC via CDP/clipboard/Playwright without printing secrets.

Reference: `references/signup-submit-cors-drift.md` covers the case where a filled signup form submits an API request but the browser stays on the same page because the XHR is blocked by frontend/CORS plumbing; diagnose with redacted browser network/console metadata, ask the operator only to check whether a verification email arrived, and otherwise park instead of chasing signup drift.

Track operator cost before continuing.

| Cost | Meaning |
|---|---|
| 0 | Hermes can do passive/local/no-secret work. |
| 1 | Operator confirmation only, or low-risk H1 private-opportunity claim where the only visible cost is consuming a slot/cadence and no account-risk warning is shown. |
| 2 | Login / OTP / email verification. |
| 3 | New account or new mailbox verification. |
| 4 | Phone, owned domain, SSO/OAuth/mailbox/channel setup. |
| 5 | Payment/KYC/production integration/customer-like setup. |

For this user's H1 first-bounty workflow, if an H1 private-opportunity card is clearly suitable and the only visible cost is the private-opportunity cadence/slot (for example `up to 1 per 30 days`) with no account/reputation-risk warning, treat it as a crisp operator-resource gate: summarize the competing choices, recommend claim/skip, and ask for explicit approval before consuming the slot. Still stop before auth/OTP/CAPTCHA/phone/payment/KYC/OAuth/integration/API-token/final submit or unclear account-risk actions.

For first-bounty sprint, prefer cost <= 2 by default. If cost >= 3 and the signal is not already strong, park. However, when the operator explicitly confirms an early first-bounty push can consume several hours, do not apply the normal low-cost bias mechanically: a higher-cost setup may be acceptable if the paid-bounty scope, bundle fit, owned controls, report title, evidence path, and stop-before rule are all strong.

### H1 private opportunity claim gate

When HackerOne Opportunity Discovery offers a private opportunity with language such as `up to 1 per 30 days`, classify the visible slot/cadence consumption as an operator-resource cost, not automatically as account risk.

For this user's first-bounty workflow, Hermes should not consume a scarce H1 private-opportunity slot by default. If a private opportunity is a strong freshness-first candidate and no reputation/account-health warning is visible, prepare a concise claim recommendation and ask for explicit operator approval. After approval, claim/open it, record the account-impact assessment in the run card, and proceed to policy/scope review only.

Still stop and ask the operator before any unclear account-risk action or before auth, OTP, CAPTCHA, phone, payment, KYC, OAuth/integration, API-token/credential claim, production account-control setup, live target testing, or final report submission.

### H1 private-opportunity claims

When HackerOne shows a private opportunity with a `Claim your spot`-style action and the only visible downside is a cadence/slot limit such as `up to 1 per 30 days`, treat it as an operator-resource gate. Do not click it during autonomous triage. Recommend a decision only after comparing it against non-scarce candidates and checking whether it is likely to beat the current public/collaboration target.

After explicit operator approval, immediately record the account-impact assessment in the run card and proceed to policy/scope review only.

Still stop and ask the operator before any unclear account-risk action or before auth, OTP, CAPTCHA, phone, payment, KYC, OAuth/integration, API-token/credential claim, production account-control setup, live target testing, or final report submission.

### Scarce Opportunity / Claim Gate

Some platforms expose account-level scarce opportunities, such as private invites, `claim your spot`, or “up to 1 per 30 days” selections. Treat these as operator-cost decisions even when the click is technically simple.

Rules:

1. Do not consume a scarce invitation/claim/slot without explicit operator approval.
2. Before asking, summarize the top competing choices and give a crisp recommendation, not a vague “what next?” process question.
3. Ask for a copy-pasteable binary decision when possible, e.g. `claim <program>` / `skip <program>`.
4. If the claim reveals phone/KYC/payment/high-friction signup before a strong bundle surface appears, park quickly and preserve the reason.
5. Private/fresh opportunities can beat old public programs, but scarcity does not override scope, bounty status, operator cost, or bundle preconditions.

### Freshness Kill/Park Shortcuts

During freshness-first target triage:

- If a program shows bounty suspension, disabled rewards, or “temporary bounty suspension,” KILL for first-bounty purposes even if recently updated.
- If signup immediately gates on phone number, KYC, payment, or country-specific mobile verification and no unusually strong bundle signal is already visible, PARK rather than spending operator cost.
- If signup submission appears to hit the API but the browser never advances, no verification email arrives, and the observable problem is frontend/CORS/session plumbing, PARK rather than chasing signup drift; see `references/signup-and-oauth-friction-park-patterns.md`.
- If a fresh/campaign target exposes only Google/SSO/company-identity login and no official/self-serve owned controls, PARK despite good freshness unless the operator explicitly approves that setup; see `references/signup-and-oauth-friction-park-patterns.md`.
- Campaigns with very short remaining time can be fallback candidates, but prefer fresh/private/mid-sized SaaS with clear web/API/object surfaces over huge or mined-out public programs.
- Campaigns with very short remaining time can be fallback candidates, but prefer fresh/private/mid-sized SaaS with clear web/API/object surfaces over huge or mined-out public programs.

## Bundle-First Rule

Every live lane must map to a practiced bundle before execution.

Preferred first-bounty bundles:

1. `auth-role-separation`
   - Admin A can do action; low-priv B should not.
2. `removed-downgraded-stale-access`
   - B loses permission; B should no longer access direct URL/API/object.
3. `object-ownership-idor`
   - A owns object; B/other tenant C should not read or modify.
4. `metadata-only-leak`
   - Content blocked but subject/snippet/counts/participants/events leak.
5. `api-ui-permission-mismatch`
   - UI denies; API allows.
6. `invite-membership-lifecycle`
   - pending/accepted/expired/removed invite state diverges.
7. `upload-path-traversal-safe-marker`
   - only if target has owned upload object and safe marker proof boundary.

If an anomaly does not map to a bundle, park it as a hypothesis. Do not improvise a new live proof lane.

## Lab-to-Live Transfer Gate

Combine the local 靶機 flow with live bounty work as an aggressive-thinking / bounded-execution transfer discipline. Preserve the valuable parts of lab work — scanner/fuzzer/callback/exploit-flow instincts, proof primitives, controls, and false-positive handling — but convert the live execution into program-allowed, scoped, low-noise proof steps instead of blindly copying lab firepower.

Before a live proof lane is executed, map it back to one proven or intentionally selected lab capability:

```text
Lab capability / bundle:
Local proof primitive:
Evidence pattern learned:
Controls learned:
Live target adaptation:
What becomes stricter on live target:
What is explicitly NOT transferred from lab:
```

Transfer examples:

| Lab flow | Live bounty adaptation |
|---|---|
| WebGoat IDOR / access-control lesson | `object-ownership-idor`, `auth-role-separation`, or `removed-downgraded-stale-access` with owned A/B accounts only |
| JWT/token decode or claim confusion lesson | metadata-only token structure review unless program rules and owned accounts permit a bounded auth-boundary check |
| DOM/runtime XSS safe marker | safe marker only, no weaponized payload, no customer-facing persistence, no broad crawling |
| Path traversal / Zip Slip marker proof | owned upload/object only; marker-only proof; no `/etc/passwd`, no secrets, no destructive overwrite |
| SSRF/callback local proof | live only if program explicitly allows callbacks/OAST/SSRF testing; otherwise park as hypothesis |
| Service/exposure scanner bundles | fixed-path, low-rate, candidate-only reconnaissance; suppress SPA/default fallback; never broad scan without approval |

Rules for the bridge:

1. Keep aggressive hypothesis generation. Scanner/fuzzer/callback/destructive-lab lessons are often the highest-value source of attack paths.
2. Translate lab tactics into live-safe execution: scoped targets, fewer requests, explicit program-rule checks, owned accounts/objects, stop-before rules, redacted evidence, and minimal payloads.
3. If the program explicitly allows scanner/fuzzer/callback/OAST lanes, do not discard them as “too aggressive”; run them as bounded, low-rate, explainable proof steps with clear request caps and controls.
4. If the program is silent or forbids the lane, preserve the hypothesis and use a surrogate proof or park it instead of firing the lab version directly.
5. Prefer live lanes that match already-practiced evidence primitives: role matrix, owned object, removed user, direct URL/API mismatch, metadata leak, safe marker.
6. If the live target needs a proof primitive we have not practiced, park the target lane or create a local lab rehearsal first.
7. Do not call a live result reportable just because the lab proof succeeded; live proof still needs program scope, owned controls, expected-vs-observed mismatch, and redacted evidence.
8. Preserve useful lab-derived hypotheses even when not executable live today; label them `needs_authorized_live_target`, `local_bootstrap_ready`, or `reference_only` instead of discarding them.

Live run cards should include the transfer line:

```text
Lab-derived bundle: <name or none>
Transferred controls: <positive/negative controls>
Transferred evidence pattern: <screenshots/requests/matrix/marker>
Live restrictions applied: <rate/payload/action reductions>
```

If no lab-derived bundle applies, say so explicitly and either run the standard first-bounty bundle gate or park the lane.

## Latest-Vulnerability Parallel Lane

When running a latest-vulnerability lab/detector lane alongside the live target funnel, keep it freshness-honest. The active lane should use current-year advisories and preferably vulnerabilities from the last 1-2 months, unless an explicit exception is documented. Technically strong older detectors may be preserved as `reference/fallback`, but must not be presented as the primary `latest` lane.

Before committing the lane, check current advisory sources and record:

```text
Freshness window:
Primary candidate:
Advisory/source date:
Why bounty-relevant:
Safe local proof:
Allowed live transfer:
Reference/fallback detectors:
Decision: EXECUTE / PARK / KILL
```

Prioritize candidates with common bounty-scope deployment, synthetic local proof, passive/owned-control live transfer, and no need for destructive RCE/file-read/customer-data proof. See `references/latest-vuln-lane-freshness.md`.

## Precondition Gate

Before executing, fill this checklist:

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
Decision: EXECUTE / PARK / KILL
```

Hard rule: no clean negative control means no access-control claim.

Examples of negative controls:

- low-priv teammate/user
- removed user
- downgraded user
- different workspace/tenant user
- unauthenticated user
- expired invite user

## Multi-Role Tactical Lens

Use external agents often for tactical breadth, but preserve execution velocity.

### Internal lens always runs

Hermes must mentally run these roles before target-touching execution:

```text
Adversarial planner:
  Best attack path:
  Highest-value adjacent path:

Boundary engineer:
  Required controls:
  Hard stops:
  Missing preconditions:

Evidence critic:
  Evidence needed:
  Weak/overclaim risk:

Deterministic reviewer:
  Most likely benign explanation:
  Kill criteria:

Final synthesizer:
  Bundle:
  Decision: EXECUTE / PARK / KILL
  Next action:
```

### External agents preferred for non-trivial decisions

Use `delegate_task` / Claude Code / Codex / Cowork when the decision benefits from tactical diversity. For first-bounty sprint work, the default is to use at least one external strong-agent pass for target shortlist ranking, non-obvious bundle selection, or candidate/report review unless the lane is an obvious quick kill.

- target shortlist ranking;
- choosing between multiple bundle lanes;
- state-changing owned-account proof boundaries;
- report-candidate evidence review;
- ambiguous product behavior where benign explanation is plausible;
- new reusable runner/module/evidence contract.

Suggested roles:

- adversarial-planner: attacker paths and impact hypotheses.
- boundary-engineer: owned controls, stop-before rules, proof surrogate.
- evidence-critic: evidence sufficiency, overclaim risk, report shape.
- deterministic-reviewer: skeptical kill criteria and benign explanations.

### No extra review gate rule

External reviews must not add new safety gates.

A reviewer blocks only when they identify a concrete blocker:

- out-of-scope or ambiguous authorization;
- non-owned/customer data;
- secrets/tokens/cookies/OTP/password/phone/verification link risk;
- destructive, evasive, persistent, brute-force, resource-exhaustive behavior;
- OAuth/integration/channel/mailbox/API-token/billing/report submission activation;
- malformed runner-facing state or failing validation;
- evidence/data loss risk.

Generic `BLOCK`, `REQUEST_CHANGES`, caution, desire for more review, or preference for extra approvals is advisory only. Hermes must translate review into either:

```text
Concrete blocker -> stop/fix/ask operator
Evidence gap -> park or collect allowed evidence
Tactical improvement -> incorporate and continue
Generic caution -> record and continue/defer
```

## Ten-Hour Live Funnel Mode

When the operator can allocate a full focused day, treat the work as a live funnel, not a research day. Do not let tool/skill/repo exploration consume the sprint unless it directly unblocks the selected proof lane.

Default 10-hour cadence:

```text
Hour 1:
  Score 5-8 H1 programs / targets.

Hours 2-3:
  Check top 1-2 targets for signup, scope, team/role/object/API/direct-URL surface.

Hours 4-6:
  Execute one practiced bundle on the best target.

Hours 7-8:
  Build evidence packet, negative control, screenshots/request snippets, redaction, and cleanup notes.

Hour 9:
  Run tactical/evidence review: overclaim, duplicate risk, benign explanation, missing controls.

Hour 10:
  Draft report or update queue with EXECUTE/PARK/KILL decision so the next day resumes immediately.
```

Daily output targets:

```text
Minimum:
  5 targets scored
  1 run card
  1 EXECUTE/PARK/KILL decision

Normal:
  8-12 targets scored
  2 run cards
  1 complete proof lane
  1 evidence packet or explicit kill reason

High-output:
  15 targets scored
  2-3 run cards
  1-2 proof lanes
  1 report candidate or high-quality parked hypothesis
```

If 10-hour days are available and there is no reportable candidate after 30 focused live days, treat it as a strategy failure, not bad luck: change target class, move from popular programs to mid/small SaaS, favor role/API/direct-URL mismatch, source-available targets, or program-permitted low-rate scanner/fuzzer/callback lanes.

## Time Box and Kill Criteria

Default time box: 30-60 minutes per target/bundle lane.

Kill or park if:

- no clean positive/negative control;
- no owned object/resource;
- no clear report title;
- no expected-vs-observed mismatch;
- behavior is likely normal product logic;
- operator cost rises above value of signal;
- proof needs customer/non-owned data;
- proof needs OAuth/channel/token/payment/phone but signal is weak;
- the lane drifts into signup/session/provenance speculation.

Decision vocabulary:

- EXECUTE: preconditions met and proof stays in boundary.
- PARK: useful hypothesis but missing control or high operator cost.
- KILL: benign/low-value/not bounty-relevant enough to revisit soon.

## Report-Title-First Rule

Before testing, write the report title that would be true if the proof succeeds.

Good titles:

- Low-priv teammate can access admin permissions page via direct URL.
- Removed user retains access to shared inbox metadata.
- User from another workspace can read owned object by ID.
- API allows deleting owned project despite UI denying permission.

Weak titles:

- Signup behavior seems strange.
- Account appears in same company.
- Company name might group users.
- UI looks inconsistent.

If the title is weak, park before spending operator cost.

## Evidence Requirements

A reportable proof packet needs:

- scope reference;
- role/control matrix;
- owned object/resource labels only;
- expected vs observed behavior;
- redacted screenshots or request snippets;
- proof boundary and stop-before confirmation;
- what was not tested and why;
- cleanup/no-customer-data statement;
- final operator approval before submission.

Do not store secrets, tokens, cookies, OTPs, passwords, phone numbers, verification links, full private emails, or customer/non-owned data.

## Output Shape

Keep artifacts compact. For each sprint lane, prefer:

1. `run_card.md`
2. `evidence_index.json`
3. `decision.md`
4. `report_draft.md` only if candidate exists

Avoid long narrative artifacts unless they preserve important tactical learning.

## Front / Account B Lesson

If a second account appears as active teammate or admin-like member:

- Do not call it privilege escalation by itself.
- First map to `auth-role-separation` or `invite-membership-lifecycle`.
- Require clean low-priv / removed-user / never-invited provenance.
- Treat verified email-domain grouping as a likely benign explanation unless proven otherwise.
- If email verification is required and same-domain grouping explains the behavior, park.
- Do not spend operator phone/email/signup effort unless the report title is strong.
- State explicitly whether a practiced bundle actually ran.

## Common Pitfalls

1. Chasing anomalies instead of executing bundles.
2. Letting external reviewers become conservative gatekeepers.
3. Treating missing optional review as a blocker.
4. Treating a second account with broad permissions as a vuln without negative control.
5. Spending phone/email/OAuth/payment effort on weak signals.
6. Passing raw passwords/phones/OTP-like values through prompts, handoff files, screenshots, shell history, or visible tool output when a symbolic env-backed fill bridge can perform the same signup step without persisting secrets.
7. Confusing local-lab proof maturity with live-target authorization, or overcorrecting by discarding high-value scanner/fuzzer/callback/exploit-flow ideas instead of converting them into program-allowed bounded proof steps.
8. Running multiple live lanes at once.
9. Writing long notes without an execute/park/kill decision.
10. Asking the operator to open/navigate noVNC or logged-in platform pages before Hermes has tried the already-provisioned browser/noVNC route itself. First test the accessible browser; ask only after a real gate appears.
11. Asking the operator to do public/passive enrichment that Hermes can safely perform, especially after the operator says to continue autonomously until a real gate is reached.
12. Converting the first-bounty project into a learning track after the operator says learning will be handled separately; keep repo/handoff focused on target selection, proof lanes, evidence, and reports.

## Verification Checklist

Before finalizing any first-bounty sprint step:

- [ ] Lab-to-live transfer line is filled, or `no lab-derived bundle` is explicitly stated.
- [ ] Target score is recorded or obviously high.
- [ ] For H1 scope CSVs or platform scope exports, live target scope is intersected with operator-owned `config/scope.txt`; any missing whitelist entries are parked or explicitly sent to the operator.
- [ ] A practiced bundle is named.
- [ ] Multi-role lens was applied internally or via external agents.
- [ ] External review, if used, did not create extra safety gates.
- [ ] Positive and negative controls are present, or the lane is parked.
- [ ] Operator cost is acceptable for the signal.
- [ ] Kill criteria are explicit.
- [ ] Evidence contains no secrets/customer/non-owned data.
- [ ] Decision is EXECUTE / PARK / KILL.
- [ ] If no bundle ran, say so explicitly.
