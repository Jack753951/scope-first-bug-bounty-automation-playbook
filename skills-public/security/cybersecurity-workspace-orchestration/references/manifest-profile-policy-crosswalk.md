> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Manifest/profile policy crosswalk

Use this reference when the cybersec workspace needs to compare existing module manifest/profile contracts against a future active-testing or risk-tier policy without prematurely promoting new schema fields.

## When to use

- A review proposes future fields such as `risk_tier`, `execution_modes_supported`, `network_posture`, callbacks, transport posture, credential class, approval flags, rate profiles, stop conditions, or output-state policy.
- Existing `module_manifest/1.0` and `module_profile/1.0` contracts already exist and the next step is documentation or closeout, not implementation.
- The task is to answer: “what can current contracts express, what remains design memory, and what must not be mistaken for authorization?”

## Safe documentation-only pattern

1. Create a crosswalk artifact under `handoff/` that maps current manifest/profile fields to the policy concepts.
2. State explicit non-actions at the top or bottom:
   - no schema change
   - no validator change
   - no runner/executor change
   - no manifest/profile fixture change unless separately requested
   - no discovery/runtime behavior change
   - no target interaction, module execution, scanning, callbacks, or lab activation
3. Preserve existing field names and semantics. Do not rename `risk_level` to `risk_tier`, add top-level `target_touching`, or treat future design terms as contract fields.
4. Separate “currently enforceable” from “partially represented” from “future/non-contractual design memory.”
5. Update `handoff/active_strategy_queue.md` and `handoff/accepted_changes.md` with the boundary and validation results.
6. Run safe validation such as `git diff --check` and the project review wrapper (`./bin/hermes review` with required env vars on Git-Bash/MSYS) before reporting done.

## Field interpretation reminders

Existing `module_manifest/1.0` examples:

- `risk_level` is not the same as future `risk_tier`.
- `target_types` describe supported target categories; they are not scope authorization.
- `technique_tags` classify behavior; they do not authorize execution.
- `execution.supports_dry_run` proves a dry-run planning path, not live support.
- `execution.requires_network`, `execution.network_access`, and `execution.target_touching` are useful safety signals but do not by themselves encode controlled-lab versus authorized-remote posture, callback behavior, proxy/tunnel posture, credential class, or approval requirements.
- Output contracts may permit future shapes, but candidate findings/evidence must remain triage-only unless manual verification and report gates exist.

Existing `module_profile/1.0` examples:

- `mode_allowlist`, `risk_level_allowlist`, `target_type_allowlist`, `technique_tag_allowlist`, and execution/output constraints are profile gates, not authorization.
- `required_safety_gates_true/false` can enforce conservative profile posture, but still cannot replace scope/program rules/operator approval.
- For an `audit-baseline`-style profile, keep it dry-run-only, no-network, non-target-touching, passive/info-low, and no findings/evidence emission unless a later reviewed boundary changes that.

## Pitfalls

- Do not promote future active-testing policy vocabulary into schemas during a crosswalk slice.
- Do not let a documentation crosswalk imply that active testing is now allowed.
- Do not use broad free-form `tags` as a substitute for closed technique/network/risk vocabularies.
- Do not blur module safety posture with target authorization; both are required before any target-touching automation.
