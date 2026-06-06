> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# P3.14 Module Field Promotion Direction Result

Status: DIRECTION_REVIEW_COMPLETE_DEFER_FORMAL_PROMOTION
Date: 2026-05-20
Prepared by: Hermes
Source prompt: `handoff/cowork_p3_14_module_field_promotion_direction_prompt.md`
Direction review: `handoff/cowork_p3_14_module_field_promotion_direction_review.md`
Reviewer route/tool: Hermes `delegate_task` subagent fallback after `./bin/hermes cowork` hit `Error: Reached max turns (10)`
Visible runtime/model: delegate_task wrapper reported `gpt-5.5`; lower-level runtime/session identifier not exposed by the subagent harness

## Decision

P3.14 direction review recommends deferring formal module manifest/profile field promotion now.

Immediate safe next slice: documentation-only mapping/planning from current `module_manifest/1.0` / `module_profile/1.0` fields to P3.13 policy concepts.

No new field is approved for schema, manifest, profile, validator, runner, or runtime consumption.

## Reason

Existing schemas already contain partial equivalents, such as manifest `risk_level`, `target_types`, `technique_tags`, `execution.target_touching`, `execution.network_access`, and `safety_gates.*`, plus profile allowlists/constraints. Adding parallel P3.13 field names now would create duplicate semantics and migration ambiguity.

High-risk fields such as `callback_kind`, `transport_posture`, `credential_class`, `requires_operator_approval`, `program_rule_keys_required`, `rate_profile`, and `stop_condition_ids` need later registry/approval/activation designs and are not safe as isolated schema checkboxes.

## OSS Recon Gate result

The review compared Nuclei, OWASP ZAP, Semgrep, SARIF, and DefectDojo.

Adopt/adapt themes:

- controlled metadata/tag discipline;
- fixture-driven validation;
- separation of module/rule identity from run/result/evidence identity;
- provenance and lifecycle discipline.

Rejected unsafe patterns:

- executable scanner metadata as authorization;
- scanner-confirmed vulnerability semantics;
- automatic target interaction;
- heavy platform lifecycle coupling too early.

## Safety boundary

Design/review/handoff only.

No code, schema, manifest, profile, runner, validator, scanner wrapper, report generator, scheduler/CI, config/scope, program scope/rule, credential, OAuth, deployment, billing, production setting, target interaction, scanner/module execution, callback/OAST, proxy/pivot/tunnel/transport, fuzzing, brute force, exploit attempt, or report submission changed.

## Next safe action

Create a P3.15 documentation-only crosswalk artifact that maps current module manifest/profile fields to P3.13 policy dimensions and explicitly preserves non-contractual status for future fields.

Alternative: pause Phase 3 for dry-run/local MVP closeout if the operator wants to stop schema-policy planning here.
