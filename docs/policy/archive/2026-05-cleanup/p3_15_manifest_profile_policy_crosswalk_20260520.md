> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# P3.15 Manifest/Profile Policy Crosswalk

Status: historical documentation-only crosswalk; active gate language superseded by growth-first policy on 2026-05-27
Supersession note: keep the schema-semantics cautions, but do not treat old T3/T4/T5 review vocabulary as an active approval gate. Use current hard stops and focused validation in `docs/policy/review_tiering_policy.md` and `docs/policy/multi_party_review_decision_policy.md`.

Status: accepted documentation-only crosswalk
Date: 2026-05-20
Prepared by: Hermes
Review basis: `handoff/cowork_p3_14_module_field_promotion_direction_review.md`
Scope: documentation only; no schema, manifest, profile, validator, runner, scanner, target, report, or runtime behavior changed

## Purpose

P3.14 decided to defer formal field promotion for module manifest/profile risk fields. The safe next step is a documentation-only crosswalk that maps existing `module_manifest/1.0` and `module_profile/1.0` fields to P3.13 active-testing policy dimensions.

This document prevents duplicate semantics before any future schema version is proposed.

## Binding decision

No P3.13 future field is promoted in P3.15.

The following remain non-contractual design memory only:

- `risk_tier`
- `execution_modes_supported`
- `default_execution_mode`
- `target_kind`
- top-level `target_touching`
- `network_posture`
- `authentication_required`
- `credential_class`
- `callback_kind`
- `transport_posture`
- `state_changing`
- `evidence_redaction_required`
- `rate_profile`
- `stop_condition_ids`
- `program_rule_keys_required`
- `requires_operator_approval`
- `default_output_state`
- broad free-form `tags`

They must not be added to `module_manifest/1.0`, `module_profile/1.0`, validators, runner logic, profiles, module fixtures, run manifests, or report/evidence consumers without a fresh T3+ review. If they affect planned/live behavior, escalation to T4/T5 and explicit operator approval may be required.

## Current manifest/profile contract surface

Current relevant files:

- `modules/_schema/module_manifest.schema.json`
- `modules/_schema/module_profile.schema.json`
- `modules/profiles/audit-baseline.json`
- `modules/_schema/README.md`
- `modules/profiles/INDEX.md`

Current committed manifests observed:

- `modules/checks/level1/policy_decision_metadata_audit/module.json`
- `modules/checks/level1/security_headers_baseline/module.json`

Both committed manifests are offline/dry-run-safe Level 1 fixtures:

- `execution.requires_network=false`
- `execution.network_access=none`
- `execution.target_touching=false`
- `execution.destructive=false`
- `execution.intrusive=false`
- `output_contracts.emits_findings=false`
- `output_contracts.emits_evidence=false`
- `safety_gates.allows_oast_callbacks=false`
- selected by the conservative `audit-baseline` profile

## Manifest field crosswalk

| Existing `module_manifest/1.0` field | Existing meaning | P3.13 policy dimension | Current posture | Future promotion note |
|---|---|---|---|---|
| `schema_version` | Strict contract version, currently `module_manifest/1.0` | Versioning / migration boundary | Stable 1.0 contract | Any semantic expansion should use a new reviewed version, not silent 1.0 drift. |
| `module_id` / `version` | Stable module identity | Module identity and audit binding | Already useful for run manifest/provenance | Keep separate from authorization; identity is not permission to run. |
| `risk_level` | Severity-like metadata enum: `info`, `low`, `medium`, `high` | Partial proxy for P3.13 risk tier | Not equivalent to `risk_tier` | Future design must decide whether this remains severity-like metadata or is replaced/supplemented by numeric tier. Do not allow contradictory `risk_level`/`risk_tier` semantics. |
| `target_types` | Allowed target shape vocabulary: `url`, `domain`, `ip`, `cidr` | Target kind / scope applicability | Shape only, not authorization | Does not imply scope allow. Live use still requires global/program scope and policy decision. |
| `technique_tags` | Controlled technique vocabulary such as passive metadata and active low-level actions | Technique class / risk starting map | Useful but limited | Existing active tags are not live authorization. Higher-risk tags need controlled vocabulary, fail-closed validation, and review before expansion. |
| `execution.supports_dry_run` | Module supports dry-run planning | Execution mode support | Required `true` | Not equivalent to `execution_modes_supported`; dry-run support must not imply live support. |
| `execution.requires_network` | Whether module requires network access | Network posture | Existing profile constrains to `false` | Future `network_posture` must reconcile with this field and default-deny absence/contradiction. |
| `execution.network_access` | Enum: `none`, `dns`, `target-http`, `target-tcp` | Network access class / target-touching hint | Existing profile constrains to `none` | Existing values partially cover `network_posture`, but do not encode controlled-lab vs authorized-remote vs callback. |
| `execution.target_touching` | Whether module touches target | Target interaction posture | Existing profile constrains to `false` | Do not add duplicate top-level `target_touching` unless a new schema version resolves migration semantics. |
| `execution.destructive` | Destructive behavior flag, const false in schema | Destructive-action prohibition | Must be false | Keep as hard safety invariant; any true value would be T5/out-of-platform unless a separate safe lab-only design exists. |
| `execution.intrusive` | Intrusive behavior flag, const false in schema | Intrusive/fuzz/probe escalation | Must be false | Existing 1.0 cannot represent intrusive modules. Future live-capable designs need separate T4/T5 review. |
| `execution.default_profile` | Preferred profile membership | Profile selection / allowlist binding | Used by `audit-baseline` | Profile membership is a selection constraint, not execution approval. |
| `external_tools` | Declared tool dependencies | Tooling/provenance hint | Existing fixtures use `python-stdlib` | Tool metadata is not permission to execute scanners/subprocesses. Future external scanner integration is a separate runtime boundary. |
| `output_contracts.*_schema` | Declared output schema references | Run/finding/evidence lifecycle boundary | Points to existing 1.0 contracts | Does not authorize non-empty findings/evidence. |
| `output_contracts.emits_findings` | Whether module emits findings | Candidate output posture | Existing fixtures false | Future true must remain candidate-only and require evidence/report-readiness gates. |
| `output_contracts.emits_evidence` | Whether module emits evidence | Evidence capture/redaction posture | Existing fixtures false | Future true requires redaction/minimization tests and no loot/secrets. |
| `safety_gates.require_policy_decision` | Requires central policy artifact | Policy gate dependency | Required true | Should remain mandatory before runner planning/execution. |
| `safety_gates.require_scope_match` | Requires scope allow | Authorization/scope gate | Required true | Scope match is necessary but not sufficient for live technique allow. |
| `safety_gates.manual_verification_required` | Requires human/agent verification | Candidate-only lifecycle | Required true | Protects against automatic confirmed findings. |
| `safety_gates.scanner_output_only` | Output remains scanner/triage signal | Triage-only posture | Required true | Name is imperfect for offline modules, but current meaning is non-confirming output. |
| `safety_gates.store_redacted_evidence_only` | Evidence must be redacted | Evidence minimization | Required true | Useful policy proxy; future evidence contracts must enforce value-level leakage checks. |
| `safety_gates.stores_raw_secrets` | Raw secret storage flag | Secret/loot prohibition | Required false | Any true value is blocked. |
| `safety_gates.writes_to_loot` | Loot write flag | Loot prohibition | Required false | Any true value is blocked. |
| `safety_gates.allows_destructive_actions` | Destructive action flag | T5/out-of-platform behavior | Required false | Any true value is blocked. |
| `safety_gates.allows_oast_callbacks` | Callback/OAST flag | Callback / OAST posture | Required false | Callback support is high-risk and must stay out of 1.0. |

## Profile field crosswalk

| Existing `module_profile/1.0` field | Existing meaning | P3.13 policy dimension | Current `audit-baseline` posture | Future promotion note |
|---|---|---|---|---|
| `schema_version` | Strict profile version | Versioning / migration boundary | `module_profile/1.0` | Broader profile semantics should use a reviewed new version. |
| `profile_id` | Stable selector | Profile identity / audit binding | `audit-baseline` | Identity is not authorization. Runner still needs policy artifact. |
| `mode_allowlist` | Allowed runner mode | Execution mode control | Only `dry-run` | Existing profile intentionally cannot authorize `planned` or `live`. |
| `risk_level_allowlist` | Allowed manifest risk levels | Risk filter | `info`, `low` | Not equivalent to tier allowlist. Future tier design must avoid contradictory risk filters. |
| `target_type_allowlist` | Allowed target shape | Target shape filter | `url`, `domain`, `ip`, `cidr` | Still not scope authorization. |
| `technique_tag_allowlist` | Allowed technique vocabulary | Technique class filter | passive-only metadata tags | Active tags require separate profile/review and do not imply live authorization. |
| `execution_constraints.supports_dry_run` | Required dry-run support | Dry-run support | true | Must remain true for dry-run profiles. |
| `execution_constraints.requires_network` | Required network posture | Network posture | false | Ensures current profile remains offline/local. |
| `execution_constraints.network_access` | Required network access enum | Network posture / target-touching proxy | `none` | Blocks DNS/HTTP/TCP target access. |
| `execution_constraints.target_touching` | Required target-touching posture | Target interaction posture | false | Blocks live-ish behavior. |
| `execution_constraints.destructive` | Required destructive flag | Destructive-action gate | false | Hard denial. |
| `execution_constraints.intrusive` | Required intrusive flag | Intrusive/fuzz/probe gate | false | Hard denial. |
| `output_constraints.emits_findings_allowed` | Whether selected modules may emit findings | Finding lifecycle | false | Keeps current profile preview-only/non-finding. |
| `output_constraints.emits_evidence_allowed` | Whether selected modules may emit evidence | Evidence lifecycle | false | Keeps current profile non-evidence. |
| `required_safety_gates_true` | Manifest gates that must be true | Safety invariant bundle | policy/scope/manual/redaction/scanner-output gates | Good profile-level enforcement, but does not replace policy decision checks. |
| `required_safety_gates_false` | Manifest gates that must be false | Prohibited behavior bundle | raw secrets, loot, destructive, OAST callbacks | Good profile-level enforcement; future broader profiles must remain fail-closed. |

## Mapping from P3.13 policy dimensions to current fields

| P3.13 policy dimension | Current field(s) that partially cover it | Gap / ambiguity |
|---|---|---|
| Risk tier | `risk_level`, profile `risk_level_allowlist` | Severity-like risk level is not the same as Tier 0-5 operational risk. |
| Execution mode | profile `mode_allowlist`; manifest `execution.supports_dry_run` | Manifest does not declare all supported modes; profile currently only allows `dry-run`. |
| Target kind | manifest `target_types`, profile `target_type_allowlist` | Shape only; no local-lab vs controlled-lab vs authorized-remote semantics. |
| Target touching | manifest/profile `execution.target_touching`; `network_access` conditionals | Already covered for current 1.0; avoid duplicate top-level field. |
| Network posture | manifest/profile `requires_network`, `network_access` | Does not distinguish lab vs bug-bounty remote, callback, proxy, tunnel, or transport posture. |
| Technique class | `technique_tags`, profile `technique_tag_allowlist` | Current vocabulary is narrow and mostly passive; no higher-risk technique registry. |
| Destructive/intrusive behavior | `execution.destructive`, `execution.intrusive`, safety gates | Current schema hard-denies; no safe representation for later lab-only intrusive cases. |
| Callback/OAST | `safety_gates.allows_oast_callbacks` | Only hard-deny exists; no callback infrastructure/rule/secret-safety contract. |
| Credential/auth posture | none, except generic safety gates | Missing credential origin, account ownership, auth scope, and secret handling design. |
| Program-rule requirements | `require_policy_decision`, `require_scope_match` | No program-rule key vocabulary or allow/deny registry yet. |
| Operator approval | none in manifest/profile; policy/handoff gates only | Approval is contextual per run/target/time/technique and should bind to decision artifacts, not a static boolean. |
| Rate limits / stop conditions | none | Needs separate reviewed registries before schemas reference them. |
| Output state | `output_contracts.emits_findings/evidence`, finding/result schemas | Manifest does not declare default output state; output contracts currently prevent emission under Level 1 fixtures. |
| Evidence redaction | `store_redacted_evidence_only`, evidence schema | Current field is a gate flag; future live evidence needs content-level tests and redaction pipeline. |
| Run/audit provenance | `module_id`, `version`, profile hash binding in runner, run schema | Run manifest/policy artifact remains the right place for actual execution decision and approval evidence. |

## Recommended interpretation rules

1. Existing fields are sufficient to document current offline/dry-run posture.
2. Existing fields are not sufficient to authorize live testing.
3. `dry-run` support is not live support.
4. `target_types` is not scope authorization.
5. `risk_level` is not P3.13 `risk_tier` until a reviewed migration defines equivalence or replacement.
6. `technique_tags` are classification metadata and profile filters, not executable permission.
7. `safety_gates.require_scope_match=true` is necessary but not sufficient; global/program scope and technique rules still need a policy decision artifact.
8. Any contradiction between manifest, profile, policy artifact, run manifest, program rules, or operator approval must fail closed.
9. Absence of a future field means not supported / not authorized, not legacy allow.
10. Runner behavior must not infer planned/live authorization from metadata alone.

## Recommended future migration shape

If a later T3+ review decides to promote fields, the preferred order is:

1. Keep `module_manifest/1.0` and `module_profile/1.0` unchanged.
2. Draft a new explicit schema version or migration note.
3. Decide whether `risk_level` remains severity-like metadata or becomes/references operational `risk_tier`.
4. Promote only low-ambiguity fields first, probably manifest-side:
   - execution-mode declaration constrained to `offline`/`dry-run` first;
   - conservative network posture over existing `requires_network`/`network_access`;
   - output default constrained to candidate/not-executed states.
5. Keep profile changes behind manifest semantics.
6. Keep callback, transport, credentials, rate profiles, stop conditions, program-rule keys, and approval evidence out until their registries/contracts exist.
7. Add negative tests for contradictory old/new semantics before any runner consumption.
8. Treat planned/live runner consumption as a separate T4/T5 boundary.

## Explicitly deferred

Deferred beyond P3.15:

- schema edits;
- manifest fixture edits;
- profile edits;
- validator edits;
- runner edits;
- module discovery behavior changes;
- run manifest / finding / evidence schema changes;
- report-readiness consumer changes;
- scanner/module execution;
- live/planned target interaction;
- Phase 4A lab activation.

## Safety boundary

P3.15 is documentation-only.

No live scans, probes, scanner/module execution, target interaction, fuzzing, brute force, exploit attempts, callbacks/OAST, proxy/pivot/tunnel/transport behavior, external service calls, SIEM integration, report drafting/submission, platform adapter, credentials, loot-class data, scheduler/CI, deployment, billing, OAuth, production settings, `config/scope.txt` changes, lab target selection, or real program scope/rule activation were introduced.
