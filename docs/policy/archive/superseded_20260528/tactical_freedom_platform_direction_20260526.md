> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Tactical freedom platform direction — 2026-05-26

Status: operator direction captured / platform design input / no target touched
Source: operator correction that the project should not exclude tactics merely because real attackers use dangerous or destructive methods; the ethical line should be refusing to complete harmful access, data contact, or destructive impact, not refusing to reason about realistic attack paths.
Repo truth: `handoff/current_navigation.md`, `handoff/active_strategy_queue.md`, `.hermes.md`; historical rebalance reference archived at `docs/policy/archive/2026-05-cleanup/tactical_risk_rebalance_20260526.md`

## Operator direction

The project should move away from tactic exclusion as the default design pattern. Real high-value bug bounty work requires thinking like an attacker: dangerous-looking tactics, exploit-chain reasoning, tool-assisted probing, and impact-oriented paths may all be relevant. The ethical boundary is not tactical timidity. The ethical boundary is stopping before unauthorized access, non-owned data contact, destructive action, credential theft, persistence, stealth, uncontrolled denial of service, or report submission without human review.

The desired platform direction is therefore:

```text
Model the full realistic attack path.
Execute only bounded, authorized, recoverable proof steps.
Stop before harm, data access, persistence, or destructive impact.
Use multi-agent review to preserve tactical imagination while enforcing proof boundaries.
```

## Correction to prior L0-L5 framing

The earlier L0-L5 ladder archived in `docs/policy/archive/2026-05-cleanup/tactical_risk_rebalance_20260526.md` helped prevent binary `safe_now` vs `blocked_high_risk` thinking, but it can still overfit the workflow around labels. The next design should treat the ladder, if used at all, as an internal risk note—not as the main planning primitive and not as a reason to discard tactics.

Preferred primitive:

```text
Tactic candidate -> prerequisite boundary -> bounded proof surrogate -> stop condition -> evidence packet
```

Instead of asking "is this tactic too dangerous?", the platform should ask:

1. What would a real attacker attempt to gain impact here?
2. What part of that path can be legally and safely modeled in scope?
3. What is the strongest non-harmful proof surrogate?
4. What exact condition forces stop-before-access / stop-before-damage?
5. What evidence demonstrates impact without touching non-owned data or causing harm?
6. Which agent is responsible for adversarial imagination, which agent is responsible for safety/proof critique, and which agent synthesizes the final route?

## Non-negotiable ethical stops

The project may reason about realistic attacker paths, but it must not create or run workflows that complete these outcomes against non-disposable / unauthorized targets:

- credential theft or token/session theft;
- malware, stealth, persistence, evasion, or uncontrolled propagation;
- destructive actions, denial-of-service, resource exhaustion, or data deletion;
- unauthorized access completion;
- intentional access to non-owned private data;
- broad exfiltration or automated data harvesting;
- uncontrolled scanning/fuzzing beyond scope/rate limits;
- report submission without operator review.

For local disposable labs, destructive or invasive behavior can be simulated only when the target is intentionally vulnerable/recoverable and the proof records recovery boundaries.

## Platform design implication

Build an automation platform that separates thinking from touching:

### 1. Attack-path ideation layer

Purpose: generate realistic attacker hypotheses without prematurely filtering tools or techniques.

Inputs:
- program policy / scope / rules;
- app surface map;
- proof library patterns;
- public disclosures / CVEs / CWE patterns;
- local lab analogs;
- prior no-finding feedback.

Output:
- attack-path candidates;
- likely impact;
- required prerequisites;
- expected evidence;
- harm boundary;
- legal/scope blockers.

### 2. Boundary compiler

Purpose: convert attack-path candidates into safe proof plans.

For each candidate, produce:
- owned-object / owned-account requirements;
- exact target and in-scope asset constraints;
- allowed request budget;
- data-contact boundary;
- state-change boundary;
- destructive-impact boundary;
- callback/OAST/tunnel allowance;
- stop-before-harm rule;
- redaction requirements.

### 3. Proof-surrogate generator

Purpose: find the strongest legal evidence without completing the harmful outcome.

Examples:
- marker write/readback instead of destructive command impact;
- permission-denied vs direct-request comparison instead of accessing third-party data;
- metadata-only proof instead of content exfiltration;
- self-owned object replay instead of guessing IDs;
- controlled callback to owned listener only when allowed;
- local disposable target reproduction when live proof would cross a boundary;
- source/sink reachability plus guarded local reproduction when live target cannot be touched.

### 4. Execution runner

Purpose: run only the bounded plan, never the raw attacker path.

Properties:
- scope-guarded;
- request-budgeted;
- artifacted;
- resumable;
- pre/post health where relevant;
- no secrets in logs;
- automatic stop if response indicates non-owned data, privilege crossover, destructive effect, or unexpected scope expansion.

### 5. Evidence and report-readiness layer

Purpose: turn proof into a high-value bug bounty packet without overclaiming.

Outputs:
- proof narrative;
- controls;
- impact analysis;
- exact limitations;
- screenshots/log excerpts with redaction;
- retest/remediation suggestions;
- report-ready / candidate / no-finding / blocked classification.

## Multi-agent operating model

Use multiple agents for role separation, not bureaucracy:

1. Adversarial planner
   - Maximizes realistic attack-path imagination.
   - Must include strong attacker-like paths even if they may later be bounded or rejected for execution.

2. Boundary engineer
   - Converts attacker paths into lawful bounded proof surrogates.
   - Designs stop conditions and artifact requirements.

3. Toolsmith / implementation worker
   - Builds small scripts/wrappers/runners for the bounded plan.
   - Reuses mature OSS tools where appropriate.

4. Evidence critic
   - Challenges false positives, weak controls, overclaiming, and missing proof.
   - Ensures the finding is valuable, not merely noisy.

5. Hermes synthesis
   - Chooses the route, enforces authorization gates, records repo-local artifacts, and decides whether to stop, rerun, local-simulate, or ask the operator for scope/credentials/approval.

## Engineering changes recommended

1. Replace tactic labels as the main output of previews with `attack_path_candidates`.
2. Add a `proof_boundary` object to every candidate.
3. Add `stop_before` fields for data access, destructive impact, privilege completion, rate/DoS, and out-of-scope expansion.
4. Add `proof_surrogate` fields that specify how to demonstrate impact without completing the harmful action.
5. Add multi-agent packet templates:
   - adversarial planner output;
   - boundary engineer output;
   - implementation/run card;
   - evidence critic review;
   - Hermes synthesis.
6. Update live-bounty queue/status helpers to preserve high-impact candidates even when execution is blocked.
7. Update no-finding feedback so failed lanes produce new attack-path hypotheses, not only safer retests.
8. Keep DDoS/resource exhaustion, credential theft, malware, stealth/persistence/evasion, non-owned data access, and destructive outcomes as hard stop conditions rather than mere lower-priority tactics.

## Acceptance rule

The platform is successful when it can do all of the following:

- think through realistic attacker paths without shrinking to conservative scanning;
- automatically transform dangerous paths into ethical proof surrogates where possible;
- preserve high-value blocked candidates for later authorized scope instead of deleting them;
- run bounded scripts only after scope/policy/budget/preconditions are satisfied;
- produce bug-bounty-quality evidence packets with impact and controls;
- stop automatically before unauthorized access, data contact, destructive effects, DDoS, malware, persistence, credential theft, or report submission.

## Immediate next slice

Create an offline/local design and schema slice before touching any live target:

- draft `schemas/attack_path_candidate.schema.json`;
- draft `schemas/proof_boundary.schema.json` or embed it into lane state;
- update `docs/strategy/live_bounty/live_bounty_tactical_preview_template_20260526.md` to use attack-path candidates and proof surrogates;
- add a multi-agent planning packet template under `handoff/templates/`;
- update `handoff/active_strategy_queue.md` and `handoff/current_navigation.md` to point future workers at this direction.

This slice is governance/design/platform architecture only. It does not authorize live scanning, exploitation, target-touching automation, account actions, or report submission.
