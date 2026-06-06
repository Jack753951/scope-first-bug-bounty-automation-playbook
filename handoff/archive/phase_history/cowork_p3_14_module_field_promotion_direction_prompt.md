> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Cowork Direction Review Prompt — P3.14 Module Manifest/Profile Risk-Field Promotion

Status: ready for T3+ design-only direction review
Date: 2026-05-20
Prepared by: Hermes
Source policy: `handoff/active_testing_policy.md`
Source review: `handoff/cowork_p3_13_module_risk_tier_direction_review.md`
Source checkpoint: `handoff/phase3_remaining_and_review_plain_language_20260520.md`

## Context

P3.13 accepted a policy/docs-only update. It added a non-contractual future-field candidate appendix for possible module manifest/profile fields such as `risk_tier`, `execution_modes_supported`, `target_touching`, `network_posture`, `callback_kind`, `transport_posture`, `program_rule_keys_required`, and `requires_operator_approval`.

Those fields are not currently schema, not implemented, not validated, and not consumed by any runner. This P3.14 review asks whether any subset should be promoted into a future versioned module manifest/profile contract, and if so, what the first safe slice should be.

This is a design-only direction review. Do not implement code. Do not change schemas, manifests, profiles, runners, validators, scanner wrappers, `config/scope.txt`, program scopes, modules, report generators, scheduler/CI, credentials, deployment, billing, OAuth, or production settings.

## Requested review

Review these inputs:

- `.hermes.md`
- `handoff/active_testing_policy.md`
- `handoff/cowork_p3_13_module_risk_tier_direction_review.md`
- `handoff/p3_13_module_risk_tier_policy_result.md`
- `handoff/review_tiering_policy.md`
- `handoff/multi_party_review_decision_policy.md`
- `handoff/oss_recon_gate.md`
- `modules/_schema/README.md`
- current module manifest/profile schemas if needed

Answer:

1. Should any P3.13 future fields be promoted into a formal module manifest/profile contract now, or should field promotion be deferred?
2. If promotion is recommended, what is the smallest safe subset?
3. Should the first subset target:
   - `module_manifest.schema.json` only;
   - `module_profile.schema.json` only;
   - both manifest and profile;
   - documentation-only mapping first?
4. Should fields be required immediately, optional-with-default-deny, or introduced in a new schema version?
5. Which fields are too dangerous or premature for the first promotion slice?
6. What exact validator/test assertions are required before implementation?
7. What remains blocked until T4/T5 or explicit operator approval?

## Initial Hermes hypothesis

The likely safest answer is not "promote everything." A narrow first candidate, if approved, may be one of:

- documentation-only mapping from existing schema terms to P3.13 policy terms; or
- a new manifest/profile version planning artifact; or
- a tiny schema-compatible validator hardening slice for already-existing fields if they map to current policy without new runtime meaning.

Riskier fields such as `callback_kind`, `transport_posture`, `credential_class`, `requires_operator_approval`, live `rate_profile`, and `stop_condition_ids` probably need a later T4/T5 activation design rather than immediate schema promotion.

## OSS Recon Gate required

Because field promotion would introduce or change a module/profile contract, include a design-only OSS Recon Gate comparison before recommending implementation.

Compare 2-5 relevant references, for example:

- Nuclei templates: metadata, tags, severity/classification, but avoid treating template metadata as execution authority.
- OWASP ZAP alert model: risk/confidence, but avoid scanner-confirmed semantics.
- Semgrep rule metadata: controlled tags and fixture testing, but avoid code-only assumptions.
- SARIF: run/result/rule/artifact separation, but avoid overfitting to code locations.
- DefectDojo: lifecycle/status discipline, but avoid coupling to heavy platform workflow too early.
- MITRE ATT&CK / D3FEND: optional taxonomy, but avoid mandatory taxonomy burden for every module.

For each reference, state:

- useful pattern;
- adopt/adapt/ignore;
- safety concern;
- impact on module manifest/profile, run manifest, finding/evidence lifecycle, and runner behavior.

## Safety boundary

Allowed:

- read local policy/schema/handoff files;
- write a direction-review artifact;
- recommend a future implementation scope and tests;
- recommend defer/block.

Forbidden:

- code implementation;
- schema/manifest/profile/runner/validator changes;
- scanner/module execution;
- target interaction;
- `config/scope.txt` or real program scope/rule changes;
- report drafting/submission;
- credentials, OAuth, tokens, private keys, loot;
- scheduler/CI, deployment, billing, production settings;
- live activation, fuzzing, brute force, exploit attempts, callbacks/OAST, proxy/pivot/tunnel/transport.

## Expected output

Write result to:

`handoff/cowork_p3_14_module_field_promotion_direction_review.md`

Use this format:

```text
Review tier:
Milestone:
Decision: APPROVE / APPROVE_WITH_CHANGES / DEFER / BLOCK
Safety boundary:
OSS Recon Gate:
Recommended P3.14 implementation scope, if any:
Fields to promote now:
Fields to keep non-contractual:
Schema/versioning recommendation:
Required tests/safety assertions:
Blocking issues:
Non-blocking improvements:
Out-of-scope/deferred items:
Operator approval required: yes/no; reason:
Reviewer identity: route/tool and visible model/runtime; if not exposed, state limitation.
```

Decision guidance:

- `APPROVE`: a narrow implementation slice is safe as-is.
- `APPROVE_WITH_CHANGES`: implementation may proceed only with narrowed field subset / tests / versioning constraints.
- `DEFER`: do not promote fields yet; use current policy as design memory.
- `BLOCK`: current policy/schema direction is unsafe or misleading and must be corrected before more platform work.
