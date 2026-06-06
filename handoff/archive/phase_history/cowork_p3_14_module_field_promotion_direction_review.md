> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

Review tier: T3 direction review for a possible module manifest/profile contract change; design-only, no implementation.
Milestone: P3.14 module manifest/profile risk-field promotion direction review
Decision: DEFER formal field promotion now; APPROVE only documentation-only mapping/planning as the next safe slice.
Safety boundary: Design-only review artifact. No code, schema, manifest, profile, runner, validator, scanner wrapper, report generator, scheduler/CI, config/scope.txt, program scope/rule, credential, OAuth, deployment, billing, production setting, target interaction, scanner/module execution, callback/OAST, proxy/pivot/tunnel/transport, fuzzing, brute force, exploit attempt, or report submission change was made or recommended for immediate activation.

OSS Recon Gate:

Relevant references:
- Nuclei templates
  - Useful pattern: compact module-like metadata with id/name/severity/tags/classification/references that can aid discovery, filtering, and operator review.
  - Adopt/adapt/ignore: adapt the metadata/tag discipline and controlled vocabulary idea; do not adopt Nuclei template metadata as execution authority.
  - Safety concern: Nuclei templates are commonly executable and target-touching; copying their tag/severity model directly could make risk labels look like permission to run.
  - Contract impact: module manifest/profile may eventually use controlled technique/risk selectors, but run manifest and runner behavior must still require independent policy decisions, scope/rule checks, execution-mode checks, and operator approval for T4/T5. Finding/evidence lifecycle remains candidate-only.

- OWASP ZAP alert model
  - Useful pattern: separates risk, confidence, evidence, CWE/WASC-style taxonomy, and alert lifecycle cues.
  - Adopt/adapt/ignore: adapt risk/confidence separation conceptually for findings/review, not for module execution authorization.
  - Safety concern: ZAP alerts can be interpreted as scanner-confirmed vulnerability claims; this platform must not let automated module output become confirmed/report-ready by default.
  - Contract impact: finding/evidence lifecycle can later benefit from confidence/review status, but module manifest/profile promotion should not import scanner-confirmed semantics. Runner behavior must continue to emit only candidate/needs-verification/not-executed style states until manual or agent-assisted verification.

- Semgrep rule metadata and fixture testing
  - Useful pattern: stable rule ids, severity, metadata, controlled tags, and positive/negative fixture tests around rule behavior.
  - Adopt/adapt/ignore: adapt rule id/tag discipline and fixture-driven validation. Ignore code-only assumptions and any assumption that metadata alone captures runtime safety.
  - Safety concern: Semgrep rules are static/local; web/runtime module fields need stronger authorization, network, callback, credential, and target-touching gates than static analysis metadata usually expresses.
  - Contract impact: supports documentation-only mapping and future schema test design. Module manifest/profile fields should be validated with malformed/contradictory fixtures before runner consumption. Run manifest behavior should bind policy artifact hashes and decisions rather than trusting metadata alone.

- SARIF
  - Useful pattern: explicit separation of tool/rules/results/artifacts/runs plus provenance and stable ids.
  - Adopt/adapt/ignore: adapt separation of rule/module identity from run/result/evidence identity and provenance hashing. Do not overfit to source-code locations or SARIF's full complexity.
  - Safety concern: SARIF can represent observations/results but does not itself authorize target interaction or encode program-scope decisions.
  - Contract impact: supports keeping module manifest/profile as declarations, run manifest as execution-decision ledger, and finding/evidence as separate lifecycle artifacts. Runner behavior must not infer live permission from module metadata.

- DefectDojo
  - Useful pattern: lifecycle discipline for findings, dedup/status, engagement/test boundaries, mitigation/retest concepts.
  - Adopt/adapt/ignore: adapt lifecycle/status discipline; ignore heavy platform workflow coupling for the first promotion slice.
  - Safety concern: importing a full vulnerability-management lifecycle too early could blur candidate vs confirmed states and add process burden before module contracts are stable.
  - Contract impact: reinforces candidate-only automation and manual verification before reportability. Does not justify immediate manifest/profile field promotion.

Contract impact summary:
- Program scope: no change now. Future live-capable use must continue to require global scope plus program scope/rules; program rules can only narrow.
- Policy decisions: no change now. Future fields must be advisory/declarative inputs to the policy gate, not replacements for it.
- Finding schema: no change now. Future tests must prove automation cannot emit confirmed/exploited/report_ready claims.
- Evidence schema: no change now. Future live-capable designs must require redaction/minimization and no raw secrets/loot.
- Run manifest: no change now. Future implementation must bind module id/version, profile id/hash, execution mode, policy artifact/hash, target identity, approval evidence where required, and decision artifact path/hash.
- Module manifest: no schema change now. Existing analogous fields (`risk_level`, `target_types`, `technique_tags`, `execution.target_touching`, `execution.network_access`, `safety_gates.*`) should be documented against P3.13 policy terms before any new field is added.
- Module profile: no schema change now. Existing allowlists and constraints should be mapped to policy terms before expanding profile contract.
- Runner behavior: no change now. Future runner consumption must fail closed and must not treat metadata, dry-run, or generic automation permission as live authorization.

Safety decision:
- Offline-only preview possible: yes, documentation-only mapping/planning is safe.
- Requires active behavior: no.
- Requires new policy gate: not for documentation-only mapping; yes before live-capable field consumption.
- Requires schema migration: no for the recommended immediate slice; yes if any new field is later promoted.

Recommended P3.14 implementation scope, if any:
Documentation-only mapping first. Do not promote new P3.13 future fields into `module_manifest.schema.json` or `module_profile.schema.json` in P3.14. The safe near-term artifact is a mapping note that relates existing manifest/profile 1.0 fields to P3.13 policy concepts and explicitly states that the P3.13 candidate names remain non-contractual until a later versioned schema review.

Rationale:
- Existing schemas already contain partial equivalents: manifest `risk_level`, `target_types`, `technique_tags`, `execution.supports_dry_run`, `execution.requires_network`, `execution.network_access`, `execution.target_touching`, `execution.destructive`, `execution.intrusive`, and `safety_gates.*`; profile `mode_allowlist`, `risk_level_allowlist`, target/technique allowlists, execution/output constraints, and required safety gates.
- Adding parallel fields such as `risk_tier`, `execution_modes_supported`, or `network_posture` now would create duplicate semantics and migration ambiguity unless the schema version, runner policy gate, run manifest, tests, and fixture strategy are updated together.
- A manifest/profile contract change is T3 and OSS-gated; any runtime consumption that affects live/planned decisions escalates toward T4/T5. The current task is explicitly design-only.

Fields to promote now:
None as formal schema/manifest/profile contract fields.

Smallest safe future subset, if a later T3 implementation is approved:
1. Prefer a new schema version, not silent mutation of `module_manifest/1.0` or `module_profile/1.0`.
2. Start with manifest-only or documentation-only-to-manifest mapping before profile expansion:
   - `risk_tier` only if clearly mapped from or replacing `risk_level`, not coexisting indefinitely with contradictory meaning.
   - `execution_modes_supported` and `default_execution_mode` only if they remain offline/dry-run constrained at first and cannot imply live authorization.
   - `target_touching` only if reconciled with the already-existing `execution.target_touching` field; do not add a duplicate top-level field unless version migration removes ambiguity.
   - `network_posture` only if it is a conservative abstraction over existing `execution.requires_network` / `execution.network_access`, with `none` as default-deny and no `authorized_remote` live enablement without T4/T5 gates.
   - `default_output_state` only if constrained to allowed triage states and tied to finding/result schema tests.
3. Profile changes should lag manifest changes until manifest semantics stabilize; profile should select/deny based on manifest declarations rather than inventing independent policy meaning.

Fields to keep non-contractual:
- `callback_kind`: premature and high-risk. Callback/OAST behavior is T4/T5-adjacent and requires owned infrastructure, no secret collection, program-rule allow, audit, stop conditions, and operator approval.
- `transport_posture`: premature and high-risk. Proxy/pivot/tunnel/beacon/relay semantics default T4/T5 and must not appear as harmless metadata before a transport safety design exists.
- `credential_class` and nuanced `authentication_required`: premature for schema promotion until credential/account ownership and secret-handling policy are designed.
- `requires_operator_approval`: dangerous as a bare boolean because approval is contextual by target, technique, time window, program rule, and run. If added later, it should reference approval evidence/decision artifacts, not be a static bypassable flag.
- `program_rule_keys_required`: valuable but premature until program-rule key vocabulary exists and is validated fail-closed.
- `rate_profile` and `stop_condition_ids`: useful later, but require separate registries and validation before references become meaningful.
- `state_changing`: important later, but dangerous if introduced without runner-level denial and program-rule checks.
- `evidence_redaction_required`: generally desirable, but should be integrated with evidence/run lifecycle tests rather than added as an isolated manifest checkbox.
- Broad free-form `tags`: should not be promoted unless controlled vocabulary and live-deny semantics are already defined.

Schema/versioning recommendation:
- Do not modify `module_manifest.schema.json` or `module_profile.schema.json` for P3.14.
- Preserve strict version semantics for existing `module_manifest/1.0` and `module_profile/1.0`.
- If field promotion is later approved, introduce a new explicit schema version (for example, `module_manifest/1.1` or `module_manifest/2.0`, depending on compatibility) with migration notes and fixture coverage.
- Avoid optional fields with ambiguous runtime meaning in 1.0. Optional-with-default-deny is acceptable only when validators and runners prove absence means deny/not-executed, not legacy allow.
- Do not make new fields required in the existing 1.0 contract; that would break current fixtures/profiles and encourage rushed migrations.
- The first implementation slice should be documentation-only mapping or a separate planning artifact; if a schema slice follows, prefer manifest first, then profile selection constraints, then run-manifest/runner consumption in later reviewed phases.

Required tests/safety assertions before any implementation:
- Schema/version tests:
  - reject unknown schema versions and schema-version drift;
  - reject unknown fields unless the new version explicitly allows them;
  - prove 1.0 fixtures remain either valid under 1.0 or intentionally migrated with recorded compatibility notes;
  - reject duplicate/contradictory old/new semantics such as `risk_level: low` with `risk_tier: 4`, or `execution.target_touching: false` with top-level `target_touching: true`.
- Manifest/profile validation tests:
  - reject missing or out-of-range `risk_tier` if/when required in a new version;
  - reject unsupported execution modes and any default mode not present in `execution_modes_supported`;
  - reject live/planned modes for modules lacking required policy gates;
  - reject network/callback/transport/credential declarations that imply lower risk than active_testing_policy.md permits;
  - reject free-form tags outside an allowlisted vocabulary.
- Runner/policy negative tests before any runner consumption:
  - dry-run never becomes live authorization;
  - generic `automation: true` or broad in-scope domain never authorizes fuzzing, brute force, exploit-shaped probes, callbacks, credential-sensitive tests, or transport behavior;
  - missing/ambiguous/contradictory global scope, program scope, program rule, approval evidence, or policy artifact forces `not_executed`, `blocked`, or `reviewer_decision_required`;
  - requested execution mode cannot exceed manifest/profile/policy allowance;
  - non-direct transport and callback fields fail closed unless separately T4/T5-approved.
- Output/evidence tests:
  - automation cannot emit `confirmed`, `exploited`, or report-ready vulnerability claims;
  - findings stay candidate/needs_verification/not_executed-style only;
  - evidence redaction/minimization is required before any non-empty evidence path is accepted;
  - raw secrets, tokens, credentials, loot paths, callbacks containing secrets, and unredacted private data are rejected.
- Run manifest/audit tests:
  - planned/live run manifests include policy source hashes, target identity, module identity/version, profile id/hash, execution mode, decision artifact path/hash, and approval evidence when required;
  - idempotent policy decisions produce deterministic denial/allow records;
  - malformed external-style metadata cannot bypass policy gates.

Blocking issues:
- Formal promotion of any P3.13 future field now would be under-specified because duplicate semantics with existing 1.0 fields are unresolved.
- No current program-rule key registry, approval evidence contract, rate-profile registry, or stop-condition registry exists to safely support the higher-risk candidate fields.
- Any runner consumption of new fields would exceed this design-only boundary and likely escalate to T4/T5 if it affects planned/live behavior.

Non-blocking improvements:
- Add a future documentation-only crosswalk table from current manifest/profile 1.0 fields to P3.13 policy dimensions.
- Draft a future migration plan that chooses whether `risk_level` remains a severity-like metadata field or is replaced/supplemented by numeric `risk_tier`.
- Consider a later small registry design for program-rule keys, rate profiles, and stop conditions before referencing them from schemas.
- Keep OSS reference decisions attached to the P3.14 milestone so later Codex/Claude implementation tasks do not re-litigate unsafe defaults.

Out-of-scope/deferred items:
- Any schema, manifest, profile, validator, runner, module, scanner wrapper, report, scheduler/CI, scope/rule, credential, deployment, billing, OAuth, or production change.
- Any scanner/module execution or target interaction.
- Any live/planned activation, callback/OAST, proxy/pivot/tunnel/transport, fuzzing, brute force, exploit-shaped verification, credential-sensitive testing, or report submission.
- Any automatic promotion of findings beyond candidate/needs-verification style states.
- Any implementation of `risk_tier`, `execution_modes_supported`, `network_posture`, `callback_kind`, `transport_posture`, `program_rule_keys_required`, `requires_operator_approval`, `rate_profile`, or `stop_condition_ids` without a fresh T3+ implementation task and required independent reviews.

Operator approval required: no for this design-only direction review and no for a documentation-only mapping artifact that does not change contracts or runtime behavior. Yes before any T4/T5 activation, any target-touching execution, callbacks/OAST, proxy/pivot/transport, fuzzing, brute force, exploit-shaped or credential-sensitive testing, scope/rule changes, credentials/OAuth, scheduler/CI, deployment, billing, production changes, or report submission. Operator approval may also be required if reviewers disagree materially about a T3 contract promotion or if a proposed schema field creates activation ambiguity.

Reviewer identity: route/tool and visible model/runtime; if not exposed, state limitation.
- Route/tool: Hermes delegate_task subagent fallback route, writing a local design-only direction-review artifact after the prior `./bin/hermes cowork` attempt reportedly failed with max turns.
- Local tools used: read_file for local policy/schema/handoff inputs; write_file for this Markdown artifact. No terminal execution, scanner/module execution, network/target interaction, or schema/code edit was used.
- Visible model/runtime: the subagent harness exposes the assistant as an OpenAI Codex-style Hermes Agent session, but it does not expose a stable lower-level runtime/session identifier suitable for audit. Treat exact runtime, deployment, region, and hidden helper usage as not exposed to this reviewer.
- Independence note: this is a single delegated direction review. It supports Hermes synthesis but does not replace any later implementation, safety, architecture, or operator approval gate required by `handoff/multi_party_review_decision_policy.md`.
