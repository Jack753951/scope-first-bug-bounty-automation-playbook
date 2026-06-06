> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Cowork Direction Review — P3.13 Module Risk-Tier / Active-Testing Policy Follow-up

Status: direction review (design-only, no implementation)
Date: 2026-05-20
Source prompt: `handoff/cowork_p3_13_module_risk_tier_direction_prompt.md`
Source policy under review: `handoff/active_testing_policy.md`
Supporting context: `handoff/p3_12_closeout_current_thread_pause_20260520.md`, `handoff/review_tiering_policy.md`, `handoff/multi_party_review_decision_policy.md`, `handoff/oss_recon_gate.md`, `handoff/active_strategy_queue.md`

## Reviewer identity

- Route/tool: Cowork direction review delivered through the Claude Code chat surface in the operator's `cybersec lab (hacking)` workspace (not via `hermes cowork` CLI on this turn). Inputs were read with the Read tool against the local repo; no network, scanner, or target-touching tool was used.
- Visible runtime model: `claude-opus-4-7` (Claude Opus 4.7), per the harness environment block exposed to the assistant. The harness also exposes a Haiku helper (`claude-haiku-4-5-20251001`) as a possible sub-call target; whether one was used for this specific response is not surfaced to the assistant.
- Provider / CLI version: Anthropic Claude Code harness on Windows (`win32`). Lower-level deployment, region, and exact session identifiers are not exposed to the assistant.
- Limitation: the assistant cannot verify with certainty that the visible model string was not rewritten by harness wrappers; record this as a reviewer-self-disclosure caveat rather than a stronger attestation.
- Independence note: this review is a single-agent direction review by the Cowork role. It is not a substitute for the Multi-Party Review Decision Gate; Hermes still owns synthesis, and any T3+ follow-up needs independent implementation/safety review.

## Summary

`handoff/active_testing_policy.md` is substantively sound. Its risk-tier vocabulary, execution modes, technique-to-tier map, required-gates list, and output semantics already cover the cyber-safety surface that the next offline platform phase needs. Splitting or renaming the tier vocabulary now would create churn without unlocking new safety.

What is missing is policy-doc connective tissue, not new contracts. A narrow P3.13 slice should:

1. add a single cross-mapping table tying risk tier to execution mode, review tier, scope/rule semantics, operator approval, human-in-loop, evidence minimization, and audit logging;
2. tighten explicit fail-closed wording for the technique classes named in the prompt;
3. state an explicit "ambiguity in scope or program rules = fail closed" rule;
4. add a clearly non-contractual future-field candidate appendix so future module manifest/profile design has a discoverable starting point without prematurely promoting fields into a schema.

No code, schema, manifest, runner, scanner, scope file, program-rule file, or runtime behavior should change in P3.13. No new field should be promoted to any contract. The OSS Recon Gate stays not-applicable for the policy/docs-only slice itself; it becomes required if and when any of those future fields graduate toward a real manifest/profile/runner contract.

## Required output block

```text
Review tier: T1 (policy/docs-only clarification)
Milestone: P3.13 module risk-tier / active-testing policy follow-up
Decision: APPROVE_WITH_CHANGES
Safety boundary: policy/docs only — no schema, manifest, runner, validator, scanner, scope/config, program-rule, scheduler/CI, credentials/loot, deployment, billing, OAuth, or production surface changes; no live target behavior, scanner/module execution, callbacks/OAST, proxy/pivot/transport, fuzzing, brute force, exploit, or target-touching automation; no promotion of any field into a contract.
OSS Recon Gate: not applicable for the P3.13 docs-only slice; required before implementation of any future field listed in the non-contractual candidate appendix.
Recommended P3.13 scope: narrow append-only edit to handoff/active_testing_policy.md that adds (a) a cross-mapping table, (b) per-technique-class fail-closed clarifications, (c) explicit ambiguous-scope fail-closed rule, (d) a clearly non-contractual future-field candidate appendix.
Blocking issues: none for the docs-only slice.
Non-blocking improvements: see §6.
Future field candidates, if any: see §5 (non-contractual).
Required tests/safety assertions for any future implementation: see §7.
Out-of-scope/deferred items: any manifest/profile/runner/validator field implementation; any contract promotion; any importer/exporter; any live mode change; any scope/rule change; any operator-approval workflow code; any SOC trial consumer; any reviewer-answer capture artifact.
Operator approval required: no for the P3.13 docs-only slice. Yes before any future field graduates to a schema/manifest/runner contract, and before any T4/T5 activation regardless of tier.
```

## Answers to prompt questions

### 1. Is the current risk-tier vocabulary good enough for the next offline platform phase?

Yes, with one caveat. The five-band live model (Tier 0 offline/docs/fixtures, Tier 1 passive observation, Tier 2 non-destructive triage probes, Tier 3 vulnerability verification, Tier 4 high-risk/intrusive/callback-capable, Tier 5 prohibited) plus the four execution modes (`offline`, `dry-run`, `planned`, `live`) covers every realistic short-term module class. Renaming or splitting the tiers now would force every later artifact, prompt, and review to be re-aligned without producing any concrete safety win.

Caveat: a future module-manifest design will need a separate axis for "credential/auth posture" and "callback/transport posture" because those cross-cut multiple tiers. These belong in the non-contractual future-field appendix (§5), not in a renamed tier set.

### 2. What minimal policy/doc update should happen now as P3.13?

A single append-only edit to `handoff/active_testing_policy.md` that adds four small sections, in this order:

1. **Cross-mapping table** between risk tier and the seven dimensions named in the prompt (see §4 below for the recommended table; the policy edit should embed an equivalent table).
2. **Explicit fail-closed clauses** for the technique classes named in the prompt (see §3 below; the edit should keep the existing tier sections intact and add a short "Fail-closed clauses for specific technique classes" subsection that quotes them once, authoritatively).
3. **Ambiguous-scope-or-rule clause**: when global scope, program scope, or program rules are missing, ambiguous, or in conflict, the platform must fail closed at the higher-restriction interpretation, route to clarification, log the ambiguity, and not execute target-touching behavior under any execution mode other than `offline` or `dry-run`.
4. **Non-contractual future-field appendix** clearly marked as design notes, non-binding, non-schema, and not implemented in this slice (see §5).

No tier should be renamed, no execution mode should be renamed, no existing text should be deleted, and nothing in `Tier 5: Prohibited / Out-of-Platform Behavior` should be softened.

### 3. Which technique classes need explicit fail-closed wording now?

The current policy implies fail-closed behavior in most of these classes but does not always state it as a single sentence per class. Recommend explicit wording for:

- **Passive observation** (header/TLS/CSP/robots/security.txt at low volume): fail closed if global scope or program scope does not allow the host, even when the technique is otherwise considered low-risk. Passive ≠ permitted.
- **Benign probing / discovery** (limited template checks, low-volume reflection checks, bounded discovery): fail closed if program rules do not explicitly permit automated testing for the technique, or if the request would be state-changing.
- **Template checks (Nuclei-style and similar)**: fail closed by default for `intrusive`, `dos`, `fuzz`, `brute-force`, `credential`, `destructive`, and `exploit` tags. Allow-list approach, not deny-list, in any future manifest validator.
- **Fuzzing**: fail closed by default. Live use requires named operator approval, narrow target scope, rate limits, stop conditions, and explicit program-rule allow. Do not infer fuzz authorization from a generic "automated testing allowed" rule.
- **Brute force / password guessing**: fail closed by default and treated as prohibited unless program rules explicitly authorize it for a named endpoint with a rate/window plan. Many programs forbid this entirely; never default-enable.
- **Exploit-shaped verification (XSS/SQLi/SSRF/IDOR/file-upload/CVE PoC)**: fail closed unless the program rule explicitly permits exploit-shaped probes for the technique class, and unless evidence minimization and stop conditions are pre-declared. Confirmation must remain manual/agent-verified, never automation-promoted.
- **SSRF / OAST / Collaborator-style callbacks**: fail closed unless (a) callback infrastructure is platform-owned and platform-controlled, (b) callback domain is not secret-bearing, (c) program rule explicitly permits OAST, (d) operator approval exists. Do not collect inbound credentials, tokens, or secrets via callback.
- **Authentication / session / account-boundary testing**: fail closed if any of credential origin, account ownership, scope coverage of the account, or program-rule allow is unclear. Never test against unrelated production tenants or shared credentials.
- **Credential-sensitive testing** (password reset, MFA, OAuth flow, session fixation, token replay): fail closed unless explicit program-rule allow and explicit operator approval exist; secrets discovered during testing must not be exfiltrated, persisted in `loot/`-equivalent surfaces, or logged in plain form.
- **Proxy / pivot / transport behavior** (SOCKS, HTTP proxy, tunnel, bind/reverse listener, port forward, DNS transport, relay, beacon): fail closed at T4 minimum, escalate to T5 if persistent/scheduled/production-like. Default mode is `offline`/`dry-run` only; live transport requires explicit operator approval and explicit scope/program-rule allow that names transport.

Each of these can be one sentence in the policy. They do not require new code, only clearer prose anchoring the existing tier text.

### 4. Risk-tier ↔ policy dimension cross-mapping

Recommend the following table be added to `active_testing_policy.md`. It is a starting default and matches the tier text already in the policy; modules may be escalated for implementation reasons.

| Tier | Default execution mode | Review tier | Global scope (`config/scope.txt`) | Program scope/rule | Operator approval | Human-in-loop verification | Evidence minimization / audit |
|---|---|---|---|---|---|---|---|
| 0 (offline/docs/fixtures) | `offline` only; `dry-run` permitted if non-target-touching | T0–T2; T3 if new contract introduced | not required for purely-synthetic local content | not required | not required | not required | minimal; log file/handoff source only |
| 1 (passive observation) | `offline`/`dry-run` until runtime exists; later `planned`/`live` under gates | T3 first runtime integration; T4 if newly target-touching | required | required when a program context exists | required at first live activation | manual classification of any anomalous response | conservative rate; full request/response audit; no payload injection |
| 2 (non-destructive triage probes) | `offline`/`dry-run`/`planned`; `live` only after explicit review | T4 first live-capable integration | required | program rule must explicitly permit the technique class | required at first live activation per technique class | manual review before any state language stronger than candidate | bounded rate; redact tokens/PII/auth headers; full audit |
| 3 (vulnerability verification) | `offline`/`dry-run`/`planned` for workflow; `live` only narrowly | T4 minimum; T5 if credentials/customer data/callback/persistence | required | program rule must explicitly permit exploit-shaped probes for the technique | required per technique class and per target before live | mandatory; automation stays candidate/needs-verification | redact bodies/cookies/tokens; minimize captured evidence; full audit |
| 4 (intrusive/callback-capable) | `offline`/`dry-run`/`planned` by default | T4 or T5 by blast radius | required | program rule must explicitly permit the specific technique, with rate/window plan | required before activation; per-window | mandatory; explicit stop conditions | strict minimization; owned callback infra; no secret collection; full audit |
| 5 (prohibited) | none | n/a | n/a | n/a | not applicable — out of platform | not applicable | not applicable |

The table is a default. A specific module may be escalated when implementation details increase risk. The platform should never silently de-escalate.

### 5. Future module manifest / profile field candidates (non-contractual)

Recommend adding the following as an explicitly non-contractual appendix to `active_testing_policy.md`. Each item is a candidate for some future T3 manifest/profile review; none is promoted in P3.13, none becomes a schema, none changes the runner or validator now, and the appendix should state that explicitly.

- `risk_tier`: integer 0–5; required; matches policy tier vocabulary.
- `execution_modes_supported`: list with subset of `{offline, dry-run, planned, live}`; required.
- `default_execution_mode`: one of supported modes; defaults to the most restrictive supported mode.
- `target_kind`: e.g. `web_http`, `tls_endpoint`, `dns_zone`, `local_fixture`, `synthetic`; required for non-Tier-0.
- `target_touching`: boolean; required; false at Tier 0.
- `network_posture`: one of `{none, local, controlled_lab, authorized_remote}`; required for non-Tier-0.
- `authentication_required`: boolean; required for non-Tier-0.
- `credential_class`: one of `{none, lab, ctf, bug_bounty_self_provisioned, customer_provided}`; required if `authentication_required` is true.
- `callback_kind`: one of `{none, oast_owned, oast_third_party_prohibited}`; required at Tier 3+ if any out-of-band interaction is possible.
- `transport_posture`: one of `{direct, http_proxy, socks_proxy, tunnel, pivot, beacon, relay}` plus `{none}`; required if non-direct; non-`none` values default to T4.
- `state_changing`: boolean; required; true forces program-rule allow and operator approval at first live activation.
- `evidence_redaction_required`: boolean; required for Tier 2+; recommended true for all live capable modules.
- `rate_profile`: ID referencing a separate rate-profile registry (also future, also non-contractual here); required for non-Tier-0 live capable modules.
- `stop_condition_ids`: list of IDs from a stop-condition registry; required for Tier 3+ live capable modules.
- `program_rule_keys_required`: list of program-rule keys whose `allow` is required for a live decision (e.g. `automation`, `fuzz`, `brute_force`, `oast`, `auth_test`, `transport_proxy`).
- `requires_operator_approval`: boolean or enum; required true for first live activation per technique class at Tier 2+; required true always at Tier 4+.
- `default_output_state`: must be a member of allowed automation states; never `confirmed` or `report_ready`.
- `tags`: vocabulary-controlled set, e.g. `passive`, `discovery`, `template`, `fuzz`, `brute_force`, `oast`, `ssrf`, `xss`, `sqli`, `idor`, `auth`, `proxy`, `pivot`. Tag values themselves are the lock; free-text tags are not allowed.

The appendix should clearly say: this is design memory, not contract. Each field becomes binding only when adopted by a future T3+ manifest/profile direction review with OSS Recon Gate run on it, an independent implementation/safety review, and Hermes synthesis.

### 6. What remains blocked until fresh T3/T4/T5 review or explicit operator approval?

Even after P3.13, the following remain blocked:

- Any module manifest field listed in §5 being implemented, schema-promoted, or validated by the runner.
- Any module/profile/runner/validator code change.
- Any first-time live-capable module of any technique class (T4 minimum; T5 if credentials, customer data, callback, persistence, scheduler, or production-like surface).
- Any callback / OAST / Collaborator-style infrastructure standup.
- Any proxy/pivot/transport code with live capability.
- Any `config/scope.txt` change.
- Any program scope/rule activation that authorizes target-touching automation.
- Any scheduler/CI automation that touches targets.
- Any credentials/OAuth/tokens/secret-handling change.
- Any report drafting/submission/platform adapter.
- Any SOC trial consumer, reviewer-answer capture, schema promotion for current `*/0.1-trial` documents, SIEM/Elastic/Kibana/Splunk integration, scanner-result importer or runner adapter, or evidence-locator gate driven by scanner outputs (still deferred per P3.12 closeout).
- Any deployment, billing, OAuth, production setting, or persistent-automation change.

### 7. Required tests/safety assertions for any future implementation

When any §5 field is later proposed for actual implementation (no earlier than a separate T3 direction review with OSS Recon Gate), the implementation slice should produce, at minimum:

- Schema/manifest validator tests that reject missing `risk_tier`, out-of-range `risk_tier`, unknown enum values, and contradictory pairs (e.g. `target_touching: true` at Tier 0, `transport_posture: socks_proxy` at Tier 1, `callback_kind: oast_owned` at Tier 1).
- Negative tests proving the runner refuses to plan a `live` execution when (a) global scope does not cover the target, (b) program scope is missing or denies, (c) any `program_rule_keys_required` is not allowed, (d) `requires_operator_approval` is true and approval evidence is absent, (e) `default_execution_mode` is more restrictive than the requested mode.
- Negative tests proving dry-run cannot be treated as live authorization.
- Negative tests proving callback/OAST is rejected unless `callback_kind == oast_owned` and operator approval is present.
- Negative tests proving brute force, fuzz, and exploit-shaped probes require an explicit program-rule allow and never run from a generic `automation: true`.
- Negative tests proving credential-class `customer_provided` requires explicit operator approval and explicit program-rule allow.
- Negative tests proving non-direct `transport_posture` defaults to T4 and is rejected if program-rule key for transport is not allowed.
- Output-contract tests proving findings stay in the allowed automation states and never promote to `confirmed`/`exploited`/`report_ready`.
- Audit-log assertions: policy source hashes, target identity, module identity, execution mode, decision artifact path/hash, and approval evidence must be present in any planned/live run manifest.
- Ambiguity tests: missing/contradictory scope or rule data forces fail-closed `not_executed` or `reviewer_decision_required`.
- Idempotency tests: re-running the same plan against the same scope/rule/manifest/operator-approval state must produce identical decisions and identical audit hashes.

These tests should be written before any first live activation, regardless of how narrow the live scope is.

## Non-blocking improvements (advisory, not for P3.13)

- Consider extracting a small `handoff/policy_cross_reference.md` later that links `active_testing_policy.md`, `review_tiering_policy.md`, `multi_party_review_decision_policy.md`, and `oss_recon_gate.md` with the precedence rule "the stricter rule wins" stated once and quoted from each. Not a P3.13 deliverable.
- Consider a future rate-profile registry and stop-condition registry as separate sibling policy docs once any §5 field is being implemented. Not a P3.13 deliverable.
- Consider a separate `handoff/credential_handling_policy.md` once any non-Tier-0 module that touches `credential_class` is being designed. Not a P3.13 deliverable.

These are explicitly deferred and must not become hidden blockers.

## Multi-Party Review Decision final block

```text
Decision: PASS_WITH_CONDITIONS (direction review only; APPROVE_WITH_CHANGES for the P3.13 slice)
Tier: T1 for this direction review and the recommended P3.13 docs-only slice; T3 minimum for any future field implementation; T4/T5 for any future live activation per technique class
Milestone: P3.13 module risk-tier / active-testing policy follow-up
Hermes authority: direct for the P3.13 docs-only slice if the safety boundary remains intact; conditional for any later edit that crosses into manifest/profile/runner/validator territory; escalation-only for any T4/T5 activation
Reviewers consulted:
- Cowork direction review (this document); route/tool: Claude Code chat surface; visible model/runtime: claude-opus-4-7; limitation: lower-level harness/runtime details and exact use of helper models not exposed to the assistant; this is a single-agent direction review and does not stand in for the independent implementation/safety review the Multi-Party Review Decision Gate requires at T3+.
Validation performed:
- read .hermes.md, the named prompt, active_testing_policy.md, review_tiering_policy.md, multi_party_review_decision_policy.md, oss_recon_gate.md, p3_12_closeout_current_thread_pause_20260520.md, active_strategy_queue.md, current cowork_task.md, current cowork_result.md, and the head of accepted_changes.md;
- no code execution, no scanner/module run, no target-touching tool, no network call;
- this review writes only the direction-review file and (optionally) the rolling cowork_result.md pointer.
Blocking findings: none for the docs-only slice.
Non-blocking recommendations: see §6.
Safety boundary: policy/docs only; no schema/manifest/runner/validator/scanner/scope/config/program-rule/scheduler/CI/credentials/loot/deployment/billing/OAuth/production change; no live target behavior; no callback/OAST/proxy/pivot/transport; no fuzzing/brute force/exploit/target-touching automation; no contract promotion.
OSS Recon Gate: not applicable for the P3.13 docs-only slice; required before any future field in §5 graduates toward a real manifest/profile/runner contract.
User approval required: no for the P3.13 docs-only slice; yes before any future field implementation that crosses into manifest/profile/runner/validator territory, before any T4/T5 activation, and before any change to scope/rule/credentials/loot/scheduler/deployment/billing/OAuth/production surface.
Accepted changes updated: not applicable from this direction review; Hermes should update `handoff/accepted_changes.md` if and when the recommended P3.13 docs-only edit lands.
Next action: route to Hermes to either (a) directly apply the narrow P3.13 docs-only edit as recommended in §2 within the T1 boundary, or (b) open a Claude Code Impl / Codex task scoped strictly to that edit. Either path keeps the SOC trial consumer, schema promotions, and any live capability still deferred.
```
