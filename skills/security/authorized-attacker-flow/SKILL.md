> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

---
name: authorized-attacker-flow
description: Use when turning an authorized bug-bounty or lab target into an attacker-perspective workflow that preserves realistic attack paths while enforcing scope, proof-surrogate boundaries, stop-before rules, and evidence discipline before any target-touching action.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [security, bug-bounty, attacker-perspective, scope, proof-surrogate, evidence]
    related_skills: [cybersecurity-workspace-orchestration, multi-project-memory-routing]
---

# Authorized Attacker Flow

> **Note (2026-05-28):** Hermes orchestration retired in this project. Active driver = Claude Code single-agent. Active safety gate = `/SAFETY.md`. Skill methodology still applies; treat references to Hermes/Cowork/Codex worker routing as historical context, not active orchestration.

## Overview

This skill converts “think like an attacker” into a repeatable, auditable workflow for authorized cybersecurity work. The goal is not to sanitize away realistic adversarial thinking; the goal is to compile each idea into a bounded proof path with explicit authorization, owned test data, stop-before rules, and evidence requirements.

Core primitive:

```text
attacker objective -> path hypothesis -> authorization check -> proof boundary -> proof surrogate -> stop-before -> evidence packet -> decision
```

Hermes remains the safety and synthesis gate. Workers/reviewers can propose attack paths, objections, and evidence critiques, but they do not grant permission to execute target-touching steps.

## When to Use

Use this skill when:

- The user asks for an attacker-view bug bounty, CTF, lab, or authorized asset workflow.
- A target has just passed signup/auth and needs first-pass real-world surface mapping.
- You need to preserve high-impact ideas without executing unsafe or out-of-scope actions.
- You need to convert vague “what would an attacker do?” ideation into concrete, gated next actions.
- You are about to move from passive observation into any request, state change, callback, integration, scanner, fuzzer, or exploit-adjacent test.

Do not use this skill to authorize:

- Targets without explicit local-lab, CTF/training, user-owned, written client, or bug-bounty scope.
- Credential theft, malware, persistence, evasion, stealth, destructive impact, spam, or resource exhaustion.
- Access to non-owned data or customer/third-party systems.
- Target-touching automation when program scope/rules are missing, ambiguous, or disallow the technique.

## Phase 0 — Authorization and Workspace Gate

Before any active action, collect and verify:

1. Target identity and authorization basis:
   - local lab / intentionally vulnerable app
   - CTF or training platform
   - user-owned asset
   - written client authorization
   - explicit bug bounty scope
2. In-scope assets and out-of-scope controls.
3. Program rules, prohibited techniques, rate limits, account constraints, third-party constraints, and report rules.
4. Operator-owned accounts/objects/test data available for proof.
5. Secret-handling boundary: never record passwords, OTPs, phone numbers, cookies, tokens, API keys, or verification links in repo artifacts.

Fail closed if scope is missing or ambiguous.

## Phase 1 — Attacker Objective Inventory

Build an attacker-view inventory before testing. Prefer questions over tools:

- What assets does the app protect?
- What identity and trust boundaries exist?
- What role, workspace, org, tenant, or account boundaries exist?
- What user-controlled objects exist?
- What integrations, callbacks, import/export, email, file, webhook, OAuth, SSO, domain verification, billing, support, or admin features exist?
- What actions create outbound communication or touch third parties?
- What could be proven with only operator-owned accounts and data?

For SaaS apps, map at least these surfaces:

- profile/account settings
- workspace/org settings
- team, invite, roles, permissions, removed-user behavior
- object creation and sharing boundaries
- API docs/schema and token screens without creating or storing tokens unless explicitly approved
- webhooks/integrations/OAuth/SSO/domain/email features as gated candidates, not automatic actions
- import/export/attachment/file-processing features
- audit logs, notification, support, and billing boundaries

## Phase 2 — Candidate Packet

Create at least five candidate paths so the workflow does not collapse into the easiest lane. Each candidate should be machine-readable when possible.

Required fields:

```json
{
  "candidate_id": "short_stable_id",
  "attacker_objective": "what an attacker wants",
  "path_hypothesis": "how the path might work",
  "impact_potential": 1,
  "surrogate_feasibility": 1,
  "authorization_readiness": 1,
  "proof_boundary": {
    "in_scope_assets": [],
    "owned_accounts_or_objects": [],
    "allowed_state_changes": [],
    "blocked_state_changes": [],
    "callback_oast_tunnel_allowance": "none|operator-approved|program-approved",
    "data_contact_boundary": "owned-data-only"
  },
  "proof_surrogate": "safe way to demonstrate without harm",
  "stop_before": [],
  "evidence_requirements": [],
  "execution_status": "bounded_executable|blocked_preserve|needs_scope|needs_operator_control|needs_local_simulation|reference_only"
}
```

Scoring guidance:

- `impact_potential`: 1 low nuisance, 5 account/tenant/data/security-control impact.
- `surrogate_feasibility`: 1 hard to prove safely, 5 easy with owned data.
- `authorization_readiness`: 1 unclear/disallowed, 5 explicitly in-scope with owned objects and clear rules.

Sort candidates by: authorization readiness first, then surrogate feasibility, then impact. High-impact blocked ideas should be preserved, not deleted.

Bundle preservation rule: when the user asks not to exclude useful "bundles" or when the target surface is still poorly understood, group related hypotheses into named bundle families and preserve them with status, proof gates, and parking rationale. Do not narrow to a single proof lane by silently discarding adjacent families; prune only after evidence, scope, safety, or operator gates justify it.

## Phase 3 — Proof Boundary Gate

A candidate can become `bounded_executable` only if all are concrete and non-empty:

- in-scope asset(s)
- owned account(s), owned object(s), or equivalent lab data
- allowed state changes
- blocked state changes
- callback/OAST/tunnel allowance, even if the value is `none`
- data-contact boundary
- stop-before list
- evidence requirements

Only one candidate should be selected for execution at a time. Multiple selected lanes create scope drift.

Required stop-before categories:

- unauthorized access completion
- non-owned/customer data
- destructive impact
- DDoS/resource exhaustion/rate-limit stress
- credential, token, cookie, API-key, secret, or OTP access/storage
- malware, persistence, evasion, stealth
- scope expansion
- third-party or customer communication
- report submission without operator approval

## Phase 4 — Execution Modes

Use the least active mode that can answer the question.

1. Passive observation:
   - UI mapping, docs reading, source/static review, public metadata, screenshots.
   - No unexpected requests beyond normal manual navigation.
2. Manual owned-data proof:
   - Slow, browser-only actions using operator-owned accounts/objects.
   - No scanners/fuzzers/DAST.
3. Scripted proof surrogate:
   - Only after scope/rules and proof boundary allow it.
   - Must have dry-run, logging, rate limit, and out-of-scope fail-closed controls.
4. Blocked/preserve:
   - Keep the candidate and reasoning for future local simulation, operator approval, or program clarification.

## Phase 5 — Evidence Packet

Evidence must be sufficient but non-sensitive:

- timestamp and target/scope reference
- account/object labels only, no secrets
- screenshots or notes showing owned empty-state/object boundaries
- request/response snippets only if they contain no tokens, cookies, PII, customer data, or secrets
- clear expected vs observed behavior
- proof boundary and stop-before confirmation
- what was not tested and why
- reproducibility notes that do not enable abuse outside the authorized scope

Never store phone numbers, OTPs, passwords, cookies, bearer tokens, API keys, verification links, customer messages, or proprietary data.

## Role-Separated Review — Tactical Advisory Rule (No Extra Gate)

For any non-trivial lane, role separation is used to improve tactical coverage, evidence quality, and disagreement capture. It must not create an extra blocking safety gate on top of the actual authorization boundary: program scope, operator-owned controls, secret-handling limits, target rules, and standing project safety rules. Reviewers advise; they do not veto. Hermes may proceed with actions already allowed by scope/operator boundaries while preserving reviewer objections as tactical risks and evidence gaps.

Minimum useful roles:

- Adversarial planner: propose realistic attacker paths, likely preconditions, and plausible impact. This role should preserve high-impact ideas even when blocked.
- Boundary engineer: convert each path into proof boundary, proof surrogate, allowed/blocked state changes, callback/OAST/tunnel allowance, data-contact boundary, and stop-before rules.
- Evidence critic: identify evidence that would be weak, sensitive, non-reportable, overclaimed, or likely to touch secrets/customer/non-owned data.
- Hermes synthesis: compare disagreements, select at most one bounded lane, park/preserve the rest, or require operator/scope gate. Hermes is the only role that can declare a lane ready to execute, and only inside the documented proof boundary.

Hard boundaries:

1. A reviewer objection MUST be recorded, but it MUST NOT by itself downgrade an otherwise authorized lane to blocked. Downgrade only when a concrete blocker exists: out-of-scope asset, missing operator-owned account/object, missing explicit approval for a state-changing action, secret/token/cookie/OTP/phone handling risk, non-owned/customer data, prohibited technique, third-party communication/callback, destructive impact, scanner/fuzzer/DAST without approval, or report submission without operator approval.
2. For any non-trivial lane, try to include one actual Claude Code/Cowork tactical/boundary/evidence review and one actual Codex deterministic/skeptical review before proof execution. If either route is unavailable, skipped, unauthenticated, timed out, or replaced by Hermes for speed, record the attempted command/tool, blocker, timestamp, and fallback decision. Do not invent review authority; continue only within the existing scope/operator/safety boundary.
3. Define `non-trivial` as any candidate or lane that crosses beyond passive UI/docs mapping toward object creation, second-account action, invite, role change, token/API use, workflow activation, external channel connection, callback/webhook/OAST, scanner/fuzzer/DAST, or report-ready evidence.
4. Each external worker must receive a compact memory-sync packet, not just the target MD file. The packet must include or require reading: `.hermes.md`, `handoff/current_navigation.md`, `handoff/active_strategy_queue.md`, `handoff/current_artifact_index.md`, `notes/obsidian_projects/Cybersec Lab.md`, recent `handoff/accepted_changes.md`, active `programs/<slug>/scope.json`, active `programs/<slug>/lane_state.json`, the current candidate/evidence packet, exact safety boundary, and stop-before list.
5. Each role packet MUST record route/tool, visible model/runtime when available, artifact paths, context read attestation, validation performed, verdict, and invocation evidence (command summary, session/run id when available, raw output path or JSON usage/run artifact path). Shape-only attestation is insufficient for non-trivial lanes.
6. Reviewers MUST NOT all fill the same generic table. Each role must provide role-specific findings and at least one of: objection, constraint, evidence gap, or preserved future lane.
7. Hermes synthesis MUST document disagreements and the reason for selecting, parking, blocking, or escalating each candidate.
8. Role reviewers do not grant target authorization. Scope, operator-owned data, and stop-before boundaries still control execution.
9. After worker outputs are written, run the local worker-attestation/review gate when available, e.g. `scripts/check-worker-attestation.py` and/or `bash ./bin/hermes review`; treat these checks as artifact-integrity validation, not as new target authorization. If a shape check fails, fix/archive the artifact, but do not let artifact formatting alone redefine the target-testing boundary.
10. After synthesis, sync durable non-sensitive progress back to the repo memory layer: update the current lane state/checkpoint including a structured `worker_route_status` or equivalent route evidence block, append `handoff/accepted_changes.md`, update `handoff/active_strategy_queue.md` or `handoff/current_artifact_index.md` when navigation changes, and update the Cybersec Lab Obsidian bridge for long-term process decisions. Keep secrets, raw target data, tokens, cookies, OTPs, phone numbers, and private scope out of broad memory surfaces.

Reviewer routing baseline:

- Claude Code / Cowork: adversarial-planner, boundary-engineer, safety-reviewer, evidence-critic, strategy reviewer.
- Codex: deterministic-reviewer, schema/checklist reviewer, focused tactical objections, script/test sanity.
- Hermes: final-synthesizer, authorization/scope gate, verification runner, memory-sync owner.

Reviewers should disagree usefully. If everyone fills the same generic table, the review failed and the lane remains `blocked_preserve` or `needs_operator_control`.

## Practical First-Pass Recipe for SaaS Bug Bounty

Reference example: `references/<program-name>-post-signup-first-run-20260526.md` shows a <program-name> post-signup run where onboarding choices were kept low-risk, channel connection became the hard stop-before, and the output was a five-candidate attacker-flow packet.

Mandatory coordination reference: `references/multi-agent-memory-sync-rule.md` defines the hard rule that non-trivial lanes must actually invoke suitable external workers such as Claude Code/Cowork and Codex, pass them a memory-sync packet, verify their artifacts, and sync non-sensitive progress back to repo/Obsidian memory surfaces.

BLOCK reduction reference: `references/block-reduction-bundle-preservation.md` describes how to keep testing safely after a review BLOCK by resolving only non-target-touching blockers, preserving all useful hypothesis bundles, and moving to passive-mapping-extended without promoting to proof execution.

Practical review reference: `references/<program-name>-multi-agent-practical-review-20260526.md` shows the workflow doing its job on a tempting SaaS permission candidate: Claude preserved attacker hypotheses, Codex blocked premature proof execution, Hermes normalized a partial Claude artifact, and the lane stayed passive-only.

Proceed-to-checkpoint reference: `references/in-scope-owned-controls-proceed-to-checkpoint.md` records the operator preference that once a live-bounty asset is in scope and only owned accounts/objects are used, Hermes should choose the high-yield tactic and continue toward a reportable/blocked/no-finding checkpoint without extra approval gates; ask only for auth/secret/final-submit or concrete scope/safety blockers.

Passive resume visibility reference: `references/<program-name>-passive-resume-visibility-20260526.md` records the safe pattern when a passive-only noVNC lane is reachable but the app/browser window is not visible: document the resume state, avoid kill/restart/reset without explicit approval, and fall back to public docs mapping or operator-assisted restore.

Checkpoint-before-live passive resume reference: `references/checkpoint-before-live-passive-resume.md` records the safe pattern for resuming practical live-bounty work after an interrupted cleanup/migration session: checkpoint broad repo changes first, keep local VM/log/screenshot artifacts out of git, resume only at the least-active authorized mode, write a named program resume artifact, update lane/readiness/navigation state, and validate/redact before reporting.

Reviewer advisory / owned-account gate reference: `references/reviewer-advisory-and-owned-account-gates.md` records the correction that reviewers provide tactical/evidence advice, not extra blocking gates, plus the pattern for preparing Account B signup to an operator phone/submit gate and translating public bug-flow research into owned-data tests.

Account B passive surface reference: `references/<program-name>-account-b-passive-surface-map-20260526.md` records the pattern for post-operator-auth SaaS onboarding/dashboard mapping: keep lane state schema-valid, classify default owned objects as `surface_only`, preserve setup-guide gates, and run redaction/lane/diff/project validation.

Vuln-intel to proof-loop reference: `references/vuln-intel-to-proof-loop.md` records the offline automation rung for latest漏洞 → proof bundle coverage diff → local-lab run-card → draft proof pattern → live-target prerequisite map. Use it when the operator asks for a full vulnerability-to-proof-to-live-target pipeline; do not stop at a coverage diff.

1. Verify program scope and local whitelist.
2. Confirm account creation/login is complete without storing secrets.
3. Update lane state/checkpoint to reflect the new gate.
4. Perform browser-only surface map:
   - landing/dashboard/onboarding state
   - profile and workspace settings
   - roles/team/invite screens without sending invites unless approved
   - object creation options without contacting third parties
   - API/integration/webhook/token screens as candidates, not actions
   - if default onboarding creates owned labels/objects, record them as owned/passive surfaces and candidate signals, not as proof-ready evidence
5. Write five candidate packets.
6. Select at most one bounded executable candidate.
7. If selected candidate requires second account, OTP, CAPTCHA, billing, callback, token creation, invite email, or third-party communication, stop and request operator action/approval.
8. Execute only the bounded manual proof or stop with a preserved candidate list.
9. Update handoff artifacts and accepted changes.
10. Run validation appropriate to changed files: JSON/lane-state validation, evidence redaction check, diff check, project review if required.

For live-bounty lane state, prefer existing schema enums and put descriptive nuance in `next_autonomous_action`, `operator_gates`, `learning.next_preview_seed`, evidence JSON, or markdown handoff. Do not invent custom `state`/`status` strings if a local schema/status helper validates the file.

## Common Pitfalls

1. Mistaking ideation for authorization. A plausible attacker path is only a candidate until scope and proof boundary allow execution.
2. Deleting dangerous ideas. Preserve them as `blocked_preserve`, `needs_local_simulation`, or `needs_scope` so future work can learn from them safely.
3. Jumping from UI discovery to scanner/fuzzer. SaaS first contact should usually start with manual owned-account observation.
4. Creating or storing tokens as evidence. Token screens are candidates; token generation/storage needs explicit approval and strict redaction.
5. Touching customer data to prove impact. Use owned accounts/objects or stop.
6. Treating callbacks/webhooks/OAST as harmless. They are target-touching/third-party communication and need explicit allowance.
7. Letting multiple lanes run at once. Pick one executable lane; preserve the rest.
8. Submitting reports automatically. Final submission is operator-approved only.
9. Treating onboarding as harmless. SaaS onboarding can create durable objects, connect external channels, send invites, or grant OAuth/mailbox access. For first-contact mapping, prefer low-risk profile customization and `set up later`/skip paths; stop before channel connection, invite send, token creation, or workflow activation.
10. Treating partial worker output as a clean pass. If Claude/Codex times out or returns wrapper errors but includes useful content, preserve the raw artifact, normalize a valid summary if needed, record the caveat, and keep execution within concrete scope/operator/safety boundaries.
11. Turning a passive-only visibility problem into a destructive browser/session reset. If noVNC is reachable but the target browser is not visible, capture non-sensitive resume-state screenshots, preserve the boundary event, and use public docs mapping or operator-assisted restore. Do not kill, reset, or restart existing browser/session processes unless the operator explicitly approves that restore action.
12. Resuming live work on top of a broad dirty cleanup/migration tree. If the repo has many unrelated staged/unstaged moves or handoff changes, first run review, inspect for accidental local/runtime artifacts, checkpoint the cleanup boundary, then create new live-lane artifacts. Do not mix target observations into the same uncheckpointed diff as migration cleanup.
13. Letting reviewer vocabulary become an execution brake. Reviewers may say `BLOCK` or `REQUEST_CHANGES`, but Hermes must translate that into concrete blockers or evidence gaps. If the only issue is reviewer caution, continue safe in-scope work; if there is a real blocker, name it precisely.
13. Running public scripts just because they match a bug class. For live bounty work, downloaded/known scripts are research inputs. Convert them into slow owned-data proof surrogates with dry-run, scope fail-closed checks, rate limits, and explicit operator approval before target-touching use.
14. Inventing schema state names to make handoff text expressive. Machine-readable lane state should stay validator-compatible; put narrative detail in evidence, learning, operator gates, and markdown.
15. Treating setup-guide progress as permission. SaaS guides often bundle safe checklist viewing with unsafe actions such as channel connection, invite send, workflow activation, or API token creation; map the gate and stop.

## Verification Checklist

- [ ] Authorization basis is explicit.
- [ ] Scope file/rules were checked and ambiguity fails closed.
- [ ] Secrets and sensitive values are excluded from artifacts.
- [ ] At least five candidate paths are preserved.
- [ ] Candidate selection uses authorization readiness and proof feasibility, not just impact.
- [ ] The selected lane has concrete proof boundary, proof surrogate, stop-before, and evidence requirements.
- [ ] Only one lane is executable at a time.
- [ ] Any active request/state change matches the allowed execution mode.
- [ ] Handoff/checkpoint artifacts reflect current state.
- [ ] JSON/diff/project validation passed after file changes.
