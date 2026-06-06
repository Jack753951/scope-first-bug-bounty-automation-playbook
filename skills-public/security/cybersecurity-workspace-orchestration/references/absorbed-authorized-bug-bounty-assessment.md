> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

---
name: authorized-bug-bounty-assessment
description: Use when working on HackerOne/Bugcrowd/Intigriti/client-authorized live bug bounty or pentest targets, converting scope/rules into safe tactical reconnaissance, bundle selection or creation, low-risk execution, review loops, and report-ready evidence without importing local-lab aggressive defaults.
version: 1.2.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [security, bug-bounty, live-target, authorized-assessment, bundles]
    related_skills: [owasp-single-vuln-lab-wave, ctf-challenge-workflow]
---

# Authorized Bug Bounty Assessment

## Overview

Use this workflow for legally authorized live targets such as HackerOne, Bugcrowd, Intigriti, client pentests, VDPs, or user-owned public assets. It is the live-target counterpart to local-lab one-vulnerability proof waves.

Core purpose: keep tactical freedom and tactical vision while preventing local-lab assumptions from leaking into public/live targets. The assessment should grow the project systematically through reusable bundles, evidence packets, and report-readiness decisions, not one-off browsing or uncontrolled scanning.

The intended continuous loop is:

```text
scope/rules intake
-> A0 passive OSINT / target scoring
-> choose one high-fit bug class and prerequisite matrix
-> reconnaissance / timeboxed viability surface map
-> agent preview
-> choose existing bundle OR acquire/adapt tools/scripts into a new bundle
-> execute bounded bundle
-> summarize evidence
-> agent review
-> Hermes synthesis / next preview
-> repeat
-> report generation when evidence is report-ready
-> consolidate new or improved bundles back into the project library
```

After one or more no-finding workflow-practice runs, do not keep repeating broad surface maps. Shift to a high-hit-rate selection loop: bug-class-first, OSINT-first, A/B-control-first, and quick parking of targets that lack safe owned objects, second-account/tenant controls, roles, API authz surface, or policy allowance. Treat no-finding as a learning event: classify whether the miss was caused by target shape, missing Account B/Tenant B/role/object controls, policy blockers, or premature checklist-style preview. See `references/high-hit-rate-live-bounty-selection.md` and `references/live-bounty-tactical-preview-and-no-finding-learning.md`.

Every loop should improve one of:

- tactical view: better target model, attack path map, preconditions, or controls;
- tactical freedom: safe ways to test more classes without violating rules;
- reusable capability: a bundle, script, checklist, target-map pattern, evidence packet, or report template;
- decision quality: clearer candidate/report-ready/no-finding classification.

## When to Use

Use when:

- The user provides a HackerOne, Bugcrowd, Intigriti, YesWeHack, client, or owner-authorized live target.
- The task involves account signup/login, profile/member pages, carts, reviews, object ownership, IDOR/access-control checks, or normal-user business logic on a real service.
- A local-lab proof primitive needs to be translated into a live authorized assessment plan.
- The work must decide whether a candidate is report-ready without overclaiming.
- The task mentions bug bounty, VDP, responsible disclosure, safe harbor, program policy, or client authorization.

Do not use when:

- The target is a disposable local lab, CTF, PortSwigger/WebGoat/DVWA/Juice Shop, or source-controlled vulnerable app. Use `owasp-single-vuln-lab-wave` or `ctf-challenge-workflow` instead.
- Authorization/scope/rules are missing or ambiguous.
- The request is broad scanning, exploitation, brute force, stealth, persistence, credential theft, real exfiltration, uncontrolled DoS, or automatic submission.

## Live Target vs Local Lab Rule

Never treat a live bug bounty target as a safer-looking local lab. Local lab workflows may allow scanners, fuzzers, destructive reset, exploit-flow reproduction, callbacks, or marker-file impact proofs. Live targets default to conservative assessment:

```text
local lab: recoverable target + aggressive proof possible
live bounty: real users/service + low-speed manual + evidence redaction + stop conditions
```

If a proof idea requires destructive/state-changing behavior, external callbacks/OAST, upload of active content, payment/KYC/order flow, mobile MITM/rooted device flow, or non-owned account data, stop and check the program rules plus operator approval before continuing.

## Authority and Role Split

Default role split for this project:

```text
Hermes: coordinator, scope gate, tactical preview owner by default, bundle routing, final synthesis, memory/handoff hygiene.
Claude Code / Cowork: implementation-heavy bundle work, code review, strategy review, or read-only evidence review when useful or tier requires it.
Codex: surgical fixes, deterministic script edits, secondary review.
Operator: legal authorization, account ownership, CAPTCHA/OTP/phone/email verification, final report-submission decision.
```

Important correction: the standing local-lab process currently has **Hermes as previewer** and **Claude Code/Cowork as post-evidence reviewer**, with Hermes doing final synthesis. For live bug bounty, keep that as the default unless the operator explicitly flips roles for a specific run. If a workflow says `agent preview` without specifying the agent, Hermes owns it by default; if the preview requires deep source/code/tool design, Hermes may route a preview subtask to Claude Code/Cowork.

## Required Scope Package

Before target-touching work, collect or create a scope package:

```text
program_slug:
program_url:
operator_handle:
authorization_source:
in_scope_assets:
out_of_scope_assets:
allowed_test_classes:
forbidden_actions:
required_headers:
rate_limits_or_time_windows:
account_policy:
external_callback_policy:
evidence_redaction_rules:
reporting_rules:
```

For this project, convert exact program facts into `programs/<program-slug>/scope.json` and confirm any `config/scope.txt` entries before live requests. Do not infer scope from similar domains or product branding.

If either program scope or global scope whitelist is missing/ambiguous, fail closed. Ask for the missing scope/rules instead of probing.

## Default Live-Target Safety Profile

Default mode until program rules explicitly allow more:

```text
mode: manual / browser-assisted / low-speed
max_concurrency: 1
scripted delay: >= 5 seconds
initial budget: small and stated in the handoff
required header: include program-required researcher header where tooling permits
account rule: owned/authorized accounts only
status language: candidate-only until report-readiness gate
```

Blocked by default unless explicitly allowed by scope/rules and separately approved:

```text
broad scanning
port scans / infrastructure scans
ffuf/dir brute force / high-volume crawling
nuclei/sqlmap/aggressive scanners
credential brute force / password spraying
rate-limit testing / DoS
social engineering / phishing
OAST/callback/tunnels/public listeners
payment/pay/cash/checkout/AML/KYC flows
file/video upload testing
mobile MITM/rooted-device workflows
partner/seller/admin/internal surfaces without legitimate accounts
third-party user data access
retention of secrets/tokens/PII
report submission before evidence review
```

Allowed first-wave activities when scope permits:

```text
official signup/login using owned throwaway accounts
read-only surface map from normal UI flows
account-owned profile/member/cart/review/settings path inventory
normal provenance collection for object IDs from own UI/API responses
low-volume account A vs account B authorization checks
redacted request/response summaries
candidate/no-finding/report-readiness classification
```

## Operating Autonomy and Checkpoints

For this user's bug bounty workflows, Hermes should behave as the project owner, not merely as a step-by-step assistant. Once the program scope/rules are captured and the operator has approved the lane boundary, Hermes should continue through safe, authorized, non-sensitive steps until one of these checkpoint conditions is reached:

```text
lane_complete_or_exhausted
target_complete_or_parked
operator_action_required: auth / OTP / CAPTCHA / email / phone / local browser / paid action / legal ambiguity
scope_or_policy_ambiguity
unexpected third-party data or sensitive data exposure
candidate could become report_ready
stronger technique needed: scanner / fuzzer / DAST / callback / upload / payment / run-script / integration / cross-tenant / non-owned data
report submission decision
```

Do not checkpoint at every minor step if the next action is clearly within the approved lane, already in scope, low-risk, and does not require secrets or operator-local interaction. Continue autonomously with compact handoff updates, request-budget discipline, and stop-condition checks. When stopping, state the reason and the exact next operator decision needed.

## Continuous Bundle Loop

This is the central operating pattern. Do not treat each test as an isolated action; every cycle should feed the next preview and improve the bundle library.

### 1. Passive target scoring and target model

Before target-touching work, use A0 passive OSINT and program metadata to decide whether the target can support a high-hit-rate bug class. Score for self-service signup, Account A/B feasibility, tenant/workspace controls, roles, safe owned objects, official API/docs, access-control/authz allowance, lack of payment/KYC/order/support dependency, share/public-private boundaries, and disclosed report/product-shape fit.

Collect only low-risk, scope-approved context:

- program policy and forbidden actions;
- in-scope hostnames/apps/API surfaces;
- normal UI navigation paths;
- owned account roles and session boundaries;
- visible object types and how IDs are legitimately obtained;
- technology/version hints only when passively visible;
- prior local-lab proof patterns that may map to this live surface.

Do not start with scanners. Do not start by making broad surface mapping the whole run. Start with one high-fit bug class, one prerequisite matrix, and one target map. If the target lacks Account B/tenant/role/API/safe-object prerequisites, park it quickly instead of turning an empty-state browse into a full assessment.

### 2. Agent preview

Before execution, produce a short preview that expands tactical options before narrowing. Do not let safety turn the preview into a rigid checklist: first model the target as a permission system, enumerate the default high-hit lane plus several adjacent lanes, classify each as `safe_now`, `later_only`, or `blocked`, then select one bounded lane and preserve the rejected/blocked ideas as next-preview seeds. For live bug bounty preview, include an OSS/public-test-case grounding pass unless the lane is purely clerical. Use safe, read-only sources such as OWASP Testing Guide / ASVS / WSTG, PortSwigger Web Security Academy labs, Nuclei template metadata for understanding classes (not for running scans by default), ZAP/Burp documentation, GitHub Security Lab writeups, public HackerOne disclosed reports, and mature open-source project docs relevant to the target's feature shape. The goal is to improve test design and controls, not to import aggressive defaults.

The preview must answer:

1. What is the best safe proof type for this live lane: access-control boundary, self-owned data read/write control, harmless marker, business-logic inconsistency, version/config exposure, or reportable policy violation?
2. What bundles already exist that can be reused safely?
3. If no bundle fits, what minimal new script/bundle is needed, and which mature OSS tools/docs can be adopted, wrapped, adapted, or used as reference-only?
4. What are the positive and negative controls?
5. What are the stop conditions?
6. What evidence would make this `candidate`, `needs_manual_review`, `report_ready`, or `no_finding`?
7. Which project capability will this add if retained?

Default preview owner: Hermes. Claude Code/Cowork may be used for preview if the lane needs source/code/tool design or an independent tactical viewpoint.

### 3. Choose existing bundle or create/adapt a new bundle

Prefer existing project bundles when the proof shape matches and live-target safety can be preserved.

If no bundle fits:

- perform OSS/tooling reconnaissance before writing new code;
- compare mature tools, official docs, public templates, and prior lab scripts;
- decide `adopt`, `wrap`, `adapt`, `reference-only`, or `write-custom`;
- keep raw downloads and tool outputs in ignored local acquisition paths;
- build a bounded bundle with plan/dry-run default where possible;
- commit only project-owned scripts/docs/manifests/sanitized summaries.

A live-target bundle must specify:

```text
when to use:
scope/rules prerequisites:
inputs:
request budget/rate:
required headers:
account/session assumptions:
positive controls:
negative controls:
artifact paths:
redaction rules:
stop conditions:
candidate/report-ready decision rules:
cleanup/reversal if any:
```

### 4. Execute bounded bundle

Execution must be consistent with the live-target safety profile:

- one lane at a time;
- minimal requests;
- no broad scanner/fuzzer defaults;
- account-owned data only;
- no secrets/PII retained;
- stop on anomalies, rate limits, CAPTCHA, account warnings, policy uncertainty, or unexpected third-party data exposure;
- save sanitized artifacts and a request summary.

If a bundle requires stronger behavior than the program allows, do not execute it. Downgrade, adapt, or mark `blocked-awaiting-scope`.

### 5. Summarize evidence

After each bundle execution, write a compact handoff:

```text
lane:
authorization boundary:
route/tool:
visible runtime/model if agent-assisted:
request budget used:
positive evidence:
negative/control evidence:
redactions performed:
observed impact:
limitations:
status: no_finding | candidate | needs_manual_review | blocked | report_ready
project benefit:
new/updated artifacts:
next preview seed:
```

Do not call a live-target issue confirmed/reportable until report-readiness review passes.

### 6. Agent review

Review challenges the evidence and overclaim risk. For preview/review of nontrivial lanes, ground the review in relevant public methodology and examples: OWASP WSTG/ASVS controls, PortSwigger labs, public disclosed reports, mature open-source test cases, and official product/protocol documentation. Prefer citations/links in the handoff when they influenced the decision. Do not treat public exploit scripts or scanner templates as permission to run them on a live target; use them to understand expected evidence, controls, and safe negative tests.

Review questions:

- Does the scope/rules package allow the tested behavior?
- Is every object/account/data item owned or authorized?
- Is the ID provenance normal and explainable?
- Are positive and negative controls meaningful?
- Is any sensitive information exposed or retained?
- Is the impact real or only metadata/noise?
- Is a stronger safe proof needed before report generation?
- Should the lane stop, rerun, switch bundle, or proceed to report?

Default reviewer: Claude Code/Cowork for nontrivial evidence review when available, with Hermes final synthesis. Hermes may self-review lightweight/no-finding loops, but should escalate if the result could become report-ready, involves ambiguity, or changes scripts/bundles.

### 7. Hermes synthesis and next preview

Hermes decides one of:

```text
stop_no_finding
retain_candidate
needs_manual_review
rerun_with_control
switch_lane
create_or_improve_bundle
prepare_report_packet
blocked_awaiting_scope_or_operator_action
```

Then seed the next preview. The process repeats until the lane is exhausted or a report packet is ready.

## Account and Session Handling

Use only accounts owned by the operator or explicitly authorized by the owner. Prefer the operator creating accounts locally in their normal browser/network, especially if signup involves CAPTCHA, OTP, email/phone verification, anti-abuse checks, or regional/device checks.

When a program says to use a HackerOne alias email, do not imply the operator must create a new mailbox. Explain that this usually means a HackerOne-provided/forwarded researcher alias tied to their H1 account. The operator should find/copy it from HackerOne or program instructions and handle verification locally. If the alias is unavailable, stop and offer the documented alternative such as an exact researcher header/proxy strategy; do not tell the operator to use a private email blindly and do not ask them to paste the alias, verification link, OTP, cookie, or password into chat.

When the project has a Kali/noVNC/VM browser and the operator says they are already logged in there, treat that VM browser as the authoritative live-target session. Do not open an unrelated agent/browser-tool session and conclude the operator is not logged in. First check the remote UI/tunnel status, inspect the VM screen or screenshot, and continue from that logged-in VM state while preserving the normal side-effect boundary. See `references/live-target-remote-ui-control.md`.

Rules:

1. Do not store passwords, OTPs, recovery codes, phone numbers, cookies, long-lived tokens, or PII in repo, memory, or durable handoffs.
2. If emails are provided in chat, record only that owned account inputs were received; do not reprint full addresses in artifacts unless the operator explicitly asks.
3. Pause for CAPTCHA, OTP, phone verification, account warning, OS/VM lock screen, local password prompt, lockout, or anti-abuse prompts. Do not bypass, automate, request, type, or store secrets for them.
4. Use non-sensitive labels such as Account A / Account B in notes and evidence packets.
5. If browser automation hits `Access Denied` or bot detection on signup/login, do not keep retrying. Route to operator-local signup and resume with post-login surface labels/screenshots/session access if safely shareable.
6. If a noVNC/VM/browser session locks mid-assessment, checkpoint artifacts, mark `blocked_operator_action`, ask the operator to unlock locally without sharing the password, and after unlock re-confirm the logged-in browser state before continuing from the checkpoint.

## Machine-Readable Lane State and Evidence Queue

When live-bounty work spans multiple sessions, lanes, or operator gates, do not leave the resumable state only in prose handoffs. Add a local-only machine-readable substrate so Hermes can resume from lane checkpoints without re-reading every artifact or adding new approval-heavy ceremony.

Recommended pattern:

```text
schemas/live_bounty_lane_state.schema.json
schemas/live_bounty_evidence.schema.json
handoff/live_bounty_lane_queue.json
programs/<program_slug>/lane_state*.json
handoff/live_bounty_evidence/<program_slug>/<lane_id>/*.json
scripts/live-bounty-lane-status.py
scripts/evidence-redaction-check.py
tests/test_live_bounty_state_and_redaction.sh
```

Minimum behavior:

- queue validation rejects entries whose `state_file` is missing;
- lane state records `next_operator_action` and `next_autonomous_action` separately;
- evidence schema keeps candidate/no-finding/report-ready vocabulary explicit and rejects unreviewed promotional labels;
- redaction checks fail closed before evidence promotion;
- redaction findings redact their own excerpts so the checker does not re-leak tokens, cookies, emails, OTPs, or other sensitive strings into logs;
- normal ISO dates should not false-positive as phone numbers;
- a local-only lane runner may select the highest-priority queued lane and emit structured next-action JSON with exit codes such as `0` ready for autonomous local work, `10` blocked on operator action, `20` blocked on scope/policy, and `30` invalid/fail-closed;
- lane runners must reject target-like args such as `--target`, `--url`, `--host`, `--scope`, and `--live` as structured JSON before argparse can leak plain-text errors, including bare flags;
- lane runners should treat terminal local statuses such as `no_finding`, `surface_only`, and `parked` as structured `lane_closed_or_parked` checkpoints with `target_touching: false`, not as invalid queue states;
- local-only preview-grounding generators may write `handoff/references/<program>_<lane>_grounding_<date>.md` from queue/state with OWASP WSTG/ASVS, PortSwigger, public reports/docs, positive/negative controls, blocked techniques, stop conditions, and evidence thresholds, but must explicitly mark scanner/template metadata as reference-only and non-authorizing;
- preview-grounding generators must also reject target-like args as structured JSON before argparse, including bare flags;
- independent review blockers become regression tests before patching.
- when a local-only substrate reaches queue/status/runner/grounding/redaction/tests/review coverage, create a closeout/checkpoint artifact and mark the engineering lane sealed by default; see `references/live-bounty-local-substrate-closeout.md` for the reusable closeout pattern and anti-drift reopen criteria.

This substrate is not target-touching automation and does not authorize signup/login, scanning, fuzzing, DAST, exploit attempts, credential handling, cross-tenant tests, or report submission. It only makes the next safe gate and action machine-readable.

See `references/live-bounty-machine-lane-state.md` for the detailed pattern.

## Evidence and Candidate Labels

Use candidate language until a report-readiness gate passes:

```text
no_finding
candidate
needs_manual_review
blocked_awaiting_scope
blocked_operator_action
not_report_ready
report_ready
```

Evidence should be minimal and redacted:

- request method/path and sanitized parameters;
- account label, not raw identity;
- status code / key headers / redacted response excerpt;
- positive and negative controls;
- object-ID provenance: where the ID came from in normal UI/API flow;
- impact statement constrained to owned data and observed behavior;
- screenshots only if secrets/PII/cookies are removed.

For IDOR with unpredictable IDs, do not guess opaque IDs. Record the normal provenance trail from owned UI/API responses, links, or state. Reports should show how IDs were obtained and why cross-account access is meaningful.

## Testing-Guidance Requests

When the user needs permission, test accounts, sandbox/staging access, or clarification before doing a live-target test, do not force the question through a vulnerability report workflow by default. Prefer the program's official `Ask a question`, `Contact program`, inbox, or discussion route. Use `Submit report` only as a last resort, clearly labeled as a testing-guidance request, and expect HackerOne/Hai pre-submission checks to flag it as `not a vulnerability report` or missing conventional report evidence. In that case, stop before final Submit and recommend the official contact route if available.

For two-account IDOR/object-ownership testing where the operator lacks a second fully owned verified account, ask for test accounts/sandbox/approved account-creation guidance first. Do not suggest SMS rental, phone-verification bypass, customer support, employee outreach, or cross-account testing without authorization. See `references/hackerone-guidance-requests.md`.

## Report Generation Gate

Only generate a report packet when all are true:

- asset and action are in scope;
- behavior is allowed by program rules;
- evidence is reproducible and minimal;
- impact is clear and meaningful;
- request/response evidence is redacted;
- affected account/data belongs to the operator/test accounts or is explicitly authorized;
- no forbidden technique was used;
- duplicate/known issue checks were considered where possible;
- remediation and retest steps are drafted;
- Hermes synthesis says `report_ready`.

Report packet should include:

```text
summary:
affected asset:
program/scope reference:
severity rationale:
steps to reproduce:
expected vs actual:
impact:
evidence summary with redactions:
safety notes:
remediation:
retest:
limitations:
not-submitted-until-operator-approval:
```

Never auto-submit. Operator makes the final submission decision.

## Handoff Pattern

Create or update a concise dry-run packet:

```text
handoff/<program_slug>_phase5a_dry_run_packet_<date>.md
```

Recommended sections:

1. status and authorization source;
2. policy facts observed;
3. in-scope assets selected for first lane;
4. blocked/forbidden actions;
5. account/session handling decision;
6. request budget;
7. first-lane hypothesis;
8. current blockers;
9. signup/login outcome if attempted;
10. selected bundle or bundle gap;
11. agent preview summary;
12. execution summary;
13. agent review summary;
14. candidate/report-readiness status;
15. next preview seed.

Append a short boundary entry to `handoff/accepted_changes.md` whenever scope, account gate, live-target posture, bundle inventory, evidence status, or report-readiness changes.

## References

- `references/high-hit-rate-live-bounty-selection.md` — OSINT-first / bug-class-first / A-B-control-first target selection pattern for improving finding probability after no-finding workflow-practice runs; includes scoring dimensions, quick-park rules, and no-finding hypothesis backlog.
- `references/high-hit-rate-first-target-selection.md` — session-derived pattern for choosing the first higher-fit target after no-finding/surface-only live runs: passive Kali/HackerOne policy intake, candidate comparison, target-selection preview artifact, and stopping at logged-in asset-table/account/scope gates.
- `references/live-bounty-tactical-preview-and-no-finding-learning.md` — tactical preview expansion/contraction pattern, no-finding feedback-loop template, target-shape lessons, and safe Account A/B operator status tokens.
- `references/live-bounty-machine-lane-state.md` — pattern for turning multi-session live-bounty lanes into local-only machine-readable queue/state/evidence/redaction artifacts, including queue coherence and redaction-output hygiene regressions.
- `references/hermes-owned-live-bounty-loop.md` — session-derived pattern for Hermes-owned live bug bounty loops, including operator-as-local-sensor handling, single-account surface mapping, and the Hermes preview / Claude Code-Cowork review role split.
- `references/live-target-remote-ui-control.md` — pattern for treating the logged-in Kali/noVNC/VM browser as the authoritative live-target session instead of confusing it with the agent's separate browser-tool session.
- `references/hackerone-guidance-requests.md` — pattern and template for asking programs for test accounts/sandbox/scope clarification before two-account IDOR or similar tests; includes submit-report fallback pitfalls.
- `references/single-account-surface-map.md` — practical pattern for one-owned-account live-target surface mapping: empty-state classification, blocked state-changing/sensitive flows, `needs_second_account` handling, and handoff table shape.
- `references/live-bounty-target-shortlist-and-parallel-hermes.md` — session-derived pattern for choosing productive single-account targets while waiting for Account B, deciding whether extra phone-verified accounts are worth it, and safely using multiple Hermes sessions in one live-bounty repo.
- `references/live-bounty-authorization-gate-sanity.md` — dry-run sanity pattern for proving repo-level scope/policy gates are usable before live automation: in-scope pass, out-of-scope fail, override safety, and `gate_fail_closed_needs_fix` handling.
- `references/thanks-only-vdp-first-flow.md` — pattern for practicing a full low-pressure VDP/thanks-only workflow: passive shortlist, policy intake only, pending scope draft, operator-confirmed whitelist, dry-run gate, manual single-account surface map, and no-finding/candidate closeout; includes the <program-redacted> VDP header-name pitfall.
- `references/<program-redacted>-vdp-no-finding-closeout.md` — session-derived closeout pattern for <program-redacted>-like SaaS VDP first-flow no-finding lanes: browser-only owned workspace observation, generated workspace subdomain scope caution, screenshot hygiene, terminal lane state, and consolidation checklist.
- `references/proof-library-live-bounty-bridge.md` — pattern for converting local-lab proof bundles into live-bounty prerequisites, blocked-state labels, evidence thresholds, and project-value framing for no-finding dry runs.
- `references/post-proof-consolidation.md` — lightweight semi-automatic cleanup gate for every new proof/bundle/live-surface artifact: classify, update indexes/navigation/Obsidian, run focused validation, and report benefit/changes without auto-promoting candidates.
- `references/thanks-only-vdp-first-flow.md` — passive selection and first-lane workflow for low-pressure thanks-only/VDP programs where the goal is to practice the complete legal/intake/gate/surface-map/closeout loop rather than maximize bounty.
- `references/broad-authorization-to-bounded-test-matrix.md` — converts broad operator authorization such as “do all authorized possible tests after scope is legal” into a policy/scope/safety-bounded matrix with dry-run gate, identity/header gate, stop conditions, and later-plan exclusions.

## Proof Library → Live Bounty Bridge

When a project has accumulated local-lab bundles/proof packets and begins authorized live-bounty work, create a bridge artifact instead of treating each live test as isolated browsing. The bridge maps each local proof pattern to:

```text
live bounty usable when:
blocked when:
minimum live evidence:
account/role prerequisites:
state-changing risk:
report-readiness threshold:
current program status:
```

Use labels such as `surface_only`, `needs_second_account`, `blocked_state_change`, `blocked_sensitive_flow`, `gate_fail_closed_needs_fix`, `gate_fixed_dry_run_verified`, `candidate`, and `report_ready`. A no-finding live dry run can still be a high-value project result if it validates the safety profile, prevents overclaiming, creates a target empty-state map, identifies account/program-guidance prerequisites, discovers gate-readiness defects before automation, or upgrades local bundles into live-prerequisite proof cards. See `references/proof-library-live-bounty-bridge.md`.

## Post-Proof Consolidation Gate

After every new proof, bundle, live surface map, report packet, bridge artifact, or authorization-gate/tooling fix, run a lightweight consolidation pass before wrap-up. Do not wait for a periodic cron job; the current session has the freshest context and is least likely to misclassify status.

Classify the artifact first:

```text
local_lab_verified_proof
local_lab_candidate
attempted_not_verified
live_surface_map
live_candidate
report_packet
tooling_gate_fix
bridge_or_decision_aid
reference_only
```

Then update only the authority files that affect future decisions:

- `handoff/accepted_changes.md` with a concise append-only boundary entry;
- `handoff/current_navigation.md` and `handoff/active_strategy_queue.md` if the next safe action or status labels changed;
- project Obsidian note with repo-truth paths and a compact summary;
- proof index for local reusable proof patterns;
- live-bounty bridge for live-target prerequisites, blocked states, or no-finding surface maps;
- script/tool inventory or focused tests for gate/tooling fixes.

Reusable proof/bundle artifacts should have these fields or an explicit reason they are reference-only:

```text
Use when:
Do not use when:
Minimum evidence:
Positive control:
Negative control:
Required accounts / roles:
State-changing risk:
Safe local runner:
Artifact root:
Live bounty prerequisites:
Blocked live states:
Report-readiness threshold:
```

Always validate the consolidation itself: run focused tests for any changed scripts/tools, `git diff --check`, and the project's local review command when available. Wrap up using the user's preferred shape: `Benefit`, `Changes`, `Validation`, and `Next safe action`. This gate must not auto-promote `surface_only`/`candidate` to verified/reportable, authorize live targets, expand scope, run scanners, submit reports, or store secrets/PII. See `references/post-proof-consolidation.md`.

## Thanks-only / VDP First Complete-Flow Runs

When the operator wants to practice the full bug-bounty/VDP workflow rather than maximize bounty probability, prefer a low-pressure VDP/thanks-only program with clear researcher account guidance and a simple owned-account lane. Treat this as workflow validation, not vulnerability hunting.

Required sequence:

```text
passive shortlist only
-> policy intake only
-> programs/<slug>/scope.json marked pending operator confirmation
-> operator-approved minimal config/scope.txt entry
-> dry-run gate pair: selected in-scope target passes, example.org fails
-> account/session run card
-> manual low-speed single-account surface map
-> no-finding/candidate/report-readiness classification
-> post-proof consolidation
```

Do not touch target assets during shortlist or policy intake. Dedicated research signup/login paths observed in policy are still target assets; they are only eligible after scope confirmation and dry-run gate. If the policy requires a researcher header or HackerOne alias, preserve the exact header spelling from the policy and choose an alias/header strategy before signup. Browser-only work is safest with the HackerOne alias when available; header-based testing requires proxy/header injection before target-touching requests.

For SaaS VDPs, keep the first lane to auth/session/profile/workspace empty-state mapping. Block integrations, webhooks, external callbacks, workflow execution, run-script features, API-key/secrets flows, tenant invitations, public sharing, and cross-tenant claims until there is a separate owned-account/tenant plan with controls. See `references/thanks-only-vdp-first-flow.md`.

## Target Selection While Account Prerequisites Are Blocked

If a high-value lane such as two-account IDOR/BOLA is blocked on a second phone-verified account, do not treat the program as exhausted. Re-route to single-account prep that improves the next live lane:

1. Prefer auth/member boundary surfaces first: login/session/logout/account recovery, auth-required vs unauthenticated responses, session expiry, account-state behavior, and member/profile identifiers visible through normal UI.
2. Prefer self-owned account surfaces second: profile, my-page, settings, cart, review, customer-service/inquiry empty states, object-type inventory, and object-ID provenance from normal UI/API flows.
3. Classify object-ownership ideas that need Account B as `needs_second_account`, not `no_finding`.
4. Defer payment, checkout, cash, KYC/AML, upload/video-upload, seller/partner, and admin-like surfaces until program guidance plus a narrow benign plan exist.
5. If the operator can legally obtain a second phone/SIM under their own name, treat that as a clean way to create Account B, but not as broad authorization for high-risk testing. Two accounts are usually enough for first-pass IDOR/BOLA; a third account needs a specific group/team/referral/multi-role rationale.

## Parallel Hermes / Worker Routing for Live Bounty

Multiple Hermes sessions can be useful in one project, but split by risk:

- Safe parallel lanes: read-only program policy comparison, target shortlisting, report/evidence template drafting, local bundle preparation, and sanitized evidence review.
- Avoid parallel live target-touching. Keep one coordinator responsible for live requests, request budget, browser/session state, and final execution decisions.
- Avoid concurrent writes to shared authority files such as `config/scope.txt`, `programs/<slug>/scope.json`, `handoff/accepted_changes.md`, `handoff/current_navigation.md`, and rolling task/result files. Do not use `--no-lock` for shared-file writes unless the operator explicitly accepts merge/safety risk.
- Prefer named per-program artifacts for parallel work: `handoff/<program_slug>_surface_map_<date>.md`, `handoff/<program_slug>_phase5a_dry_run_packet_<date>.md`, `programs/<program_slug>/scope.json`.

## Authorization-Gate Sanity Before Automation

Before moving from manual browser-assisted work to any script/bundle/scanner-like runner, prove the repository's authorization gate is operational, not merely present. Run dry-run/planned checks showing one exact in-scope target is allowed and one clearly out-of-scope target is denied. Also verify override flags remain dry-run-only or otherwise blocked.

If the gate fails closed due to slug/schema/scope-entry incompatibility, record `gate_fail_closed_needs_fix` and keep live testing manual until fixed. A fail-closed gate is safer than accidental allow, but it is not automation-ready. Once compatibility is fixed, record a distinct dry-run-only label such as `gate_fixed_dry_run_verified`: exact in-scope dry-run passes, out-of-scope dry-run fails, and the fix is regression-covered. This label is still not permission for live scanner-like automation; it only means the gate is usable for readiness checks. See `references/live-bounty-authorization-gate-sanity.md`.

## Thanks-only / VDP First Complete-Flow Lane

When the operator wants a simple first end-to-end live-bounty practice run, prefer a low-pressure VDP/thanks-only/response program and treat the goal as workflow completion rather than payout. Start with passive program-directory discovery only; do not touch target assets during shortlisting. Choose programs with open submissions, explicit rules, simple owned-account web surfaces, and preferably researcher-specific signup/login paths or headers. Avoid finance, government, critical infrastructure, broad CDN/cloud targets, hardware/firmware-only programs, and booking/payment-heavy services for the first full-flow practice.

The safe sequence is: passive shortlist artifact -> selected program policy intake -> `programs/<program_slug>/scope.json` -> operator-confirmed `config/scope.txt` entries -> dry-run gate pass/fail -> manual/noVNC account creation/login if allowed -> tiny single-account auth/session/profile/empty-state surface map -> candidate/no-finding/report-readiness classification -> post-proof consolidation. A no-finding VDP run is successful if it proves the workflow, scope gate, evidence discipline, and closeout path. See `references/thanks-only-vdp-first-flow.md`.

## Broad Operator Authorization Still Needs a Test Matrix

When the operator says to do all possible tests once scope is confirmed, treat that as authorization to enumerate the full allowed first-lane surface, not as permission to use every tool or attack class. Convert the instruction into a bounded test matrix whose rows are allowed by program policy, exact scope, project safety posture, and owned-account constraints. Include method, evidence, stop/status, and a separate "later only" section for stronger actions that require a distinct plan. Run the repo dry-run gate first with one in-scope target and one out-of-scope negative control. If scanner-style dry-run stages reject full URLs as host-only context, that can be acceptable for a manual/browser first lane but must not be presented as scanner automation readiness.

Before live account creation/login, resolve any program-specific researcher identity requirement. Copy the exact header name from policy; do not normalize it from memory. In the <program-redacted> VDP case the policy wording used `X-HackerOne-Research: [H1 username]`, so browser-only first flow should prefer a HackerOne email alias unless a proxy/header plan is explicitly selected. See `references/broad-authorization-to-bounded-test-matrix.md`.

## Common Pitfalls

1. **Using local-lab intensity on a live target.** A live service is not recoverable just because it is in scope. Default to manual, low-speed, owned-account-only.
2. **Treating scope as obvious from brand/domain.** Use the program's exact asset list and rules. Add only confirmed minimal assets to scope config.
3. **Retrying through bot detection or local auth gates.** If signup/login returns `Access Denied`, CAPTCHA, account warnings, OS/VM lock screen, or local password prompts, stop and route to operator-local action rather than bypassing, repeated automation, or credential handling.
4. **Storing account secrets in durable artifacts.** Emails may be sensitive too; prefer Account A/B labels and note that operator-owned inputs were received.
5. **Overclaiming candidates.** Cross-account status changes, 200 responses, or visible object IDs are not findings without controls, provenance, and impact.
6. **Forgetting or misnaming program-required researcher headers.** If the program asks for a header, copy the exact header name from the current policy into the scope packet and test plan; do not infer a generic name. Some programs use variants such as `X-HackerOne-Research: [H1 username]`. If browser-only testing can instead comply through a HackerOne email alias, prefer that for a first complete-flow practice run.
7. **Confusing HackerOne alias with a new mailbox.** When directing the operator through signup, say plainly that a HackerOne alias is usually provided/forwarded by HackerOne and is not a request to create a new email account. If they cannot find the alias, pause and switch to the documented header/proxy decision rather than improvising with a personal email.
8. **Testing payment/KYC/order/upload too early.** These are high-impact/high-risk and need explicit program-rule support plus operator approval.
9. **Letting safety kill tactical freedom.** Safety should shape bounded proof design, not eliminate attack-path thinking. Use preview to enumerate safe options before selecting one: default high-hit lane, adjacent permission-boundary lanes, prerequisites, `safe_now/later_only/blocked` status, and next-preview seeds.
10. **Treating no-finding as the end of learning.** A no-finding or surface-only run should update target scoring and prerequisites. Record whether the miss came from missing Account B/Tenant B/roles/safe objects/API controls, product empty state, policy blockers, or evidence limits; then park/resume deliberately instead of repeating broad browsing.
11. **Letting every run stay one-off.** Each cycle should improve the bundle library, evidence packet standards, target-map patterns, feedback logs, preview seeds, or review checklist.
12. **Role confusion.** Default is Hermes preview + Claude Code/Cowork review + Hermes synthesis. Flip only if explicitly chosen for that run.
13. **Forcing permission questions into vulnerability reports.** If a live-bounty lane is blocked on test accounts, sandbox, or scope guidance, use official program contact/ask routes first. A report-form draft can be useful, but HackerOne pre-submission review may correctly block it as not a vulnerability report; do not press Submit just to bypass that warning.
14. **Assuming a fail-closed scope gate is automation-ready.** If dry-run checks cannot show an in-scope target passing and an out-of-scope target failing, keep the lane manual/browser-assisted and fix slug/schema/scope grammar before running live automation.

## Verification Checklist

- [ ] Program authorization URL or written authorization recorded.
- [ ] Exact in-scope and out-of-scope assets/actions captured.
- [ ] `programs/<program-slug>/scope.json` exists when this project requires it.
- [ ] `config/scope.txt` contains only explicitly confirmed assets.
- [ ] Account handling uses owned/authorized accounts; no secrets stored.
- [ ] Local auth interruptions such as VM/noVNC lock screens are checkpointed as `blocked_operator_action`; operator unlocks locally and logged-in state is re-confirmed before navigation resumes.
- [ ] Request budget and stop conditions are recorded.
- [ ] First lane is single-vulnerability/single-behavior and reversible.
- [ ] No scanner/fuzzer/brute force/destructive/payment/upload/callback action used by default.
- [ ] Reconnaissance / surface map completed before execution.
- [ ] Agent preview completed and recorded.
- [ ] Existing bundle considered before writing new code.
- [ ] OSS/tooling reconnaissance completed before new bundle/script creation.
- [ ] Bundle has request budget, rate, required headers, controls, redaction, stop conditions, and status labels.
- [ ] Execution used owned/authorized accounts/data only.
- [ ] Artifacts are sanitized; no credentials/tokens/OTP/PII/loot retained.
- [ ] Agent review or Hermes review classified status honestly.
- [ ] Hermes synthesis records project benefit, new/updated artifacts, and next preview seed.
- [ ] Report packet generated only after report-readiness gate.
- [ ] No report submitted without explicit operator approval.
