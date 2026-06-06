> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Data-Driven Module Profile Contract

Use this reference when evolving offline module discovery/profile selection after committed safe fixtures and a dry-run-only runner exist.

## Purpose

A module profile is a repo-local data contract that defines which validated module manifests are eligible for a named planning profile such as `audit-baseline`. The runner should not rely only on hard-coded semantic checks; it should load `modules/profiles/<profile_id>.json`, validate it, apply its constraints to every selected manifest, and bind the selected profile into the run preview.

## Recommended files

- `modules/profiles/<profile_id>.json` — versioned profile data.
- `modules/profiles/INDEX.md` — human-readable profile inventory and safety posture.
- `modules/_schema/module_profile.schema.json` — JSON Schema for profile shape.
- `scripts/validate_module_profile.py` — stricter semantic validator for fail-closed behavior that schema alone cannot express.
- Runner/planner output should include `execution.profile_id` and `execution.profile_sha256`.

## Profile contract checks

Fail closed when any of these occur:

- Profile file missing for the requested profile.
- JSON malformed or schema invalid.
- `profile_id` inside the file does not match the requested profile/path.
- Unsupported profile ID is requested.
- Constraints allow unsafe posture for the profile (for example network access, target touching, non-dry-run execution, intrusive/destructive tags for an audit baseline).
- Constraints select no modules when a non-empty selection is required.
- Discovered or explicit module manifests are outside the repo-local allowed tree or fail the module manifest validator.

Apply the same profile gate to both discovery mode and explicit manifest paths. Do not allow explicit paths to bypass repo-local containment, manifest validation, or profile safety constraints.

## Run preview binding

For deterministic review and auditability, include both profile identity and content hash in the dry-run plan / run manifest preview:

- `execution.profile_id`
- `execution.profile_sha256`

The hash lets Hermes/Claude/Codex reviewers prove which profile rules produced a planned selection and detect stale or tampered profile data.

## Stable error-code vocabulary

Prefer structured fail-closed codes over free-form strings so Hermes logs, tests, triage, reports, and agents can parse outcomes reliably. Keep existing human-readable `errors` / `warnings` fields for compatibility, but add additive machine-readable fields instead of replacing prose:

- `error_codes`: array of stable codes for fatal/fail-closed outcomes.
- `warning_codes`: array of stable codes for non-fatal skips or advisory conditions.
- `error_details`: array of objects with at least `code` plus contextual fields such as `profile_id`, `profile_path`, `module_id`, `manifest_path`, `constraint`, `actual`, `allowed`, or `message`.
- `warning_details`: same object shape for warning conditions.

Suggested vocabulary:

- `PROFILE_NOT_FOUND`
- `PROFILE_MALFORMED_JSON`
- `PROFILE_SCHEMA_INVALID`
- `PROFILE_ID_MISMATCH`
- `PROFILE_UNSUPPORTED`
- `PROFILE_MEMBERSHIP_MISMATCH`
- `PROFILE_CONSTRAINT_RISK`
- `PROFILE_CONSTRAINT_TARGET_TYPE`
- `PROFILE_CONSTRAINT_TECHNIQUE_TAG`
- `PROFILE_CONSTRAINT_EXECUTION`
- `PROFILE_EMPTY_SELECTION`

Use `PROFILE_MEMBERSHIP_MISMATCH` as a fatal `error_code` when an explicit manifest is outside the requested profile membership, and as a non-fatal `warning_code` when discovery skips a valid but non-member manifest. Keep human-readable details alongside the code, but do not require downstream tools to grep prose.

## Validation pattern

Use TDD/fixtures for:

- Valid baseline profile accepted.
- Missing/malformed/schema-invalid profile rejected with the expected stable `error_codes` and object-shaped `error_details`.
- Profile ID/path mismatch rejected.
- Unsupported profile rejected.
- Explicit manifest membership mismatch rejected as `PROFILE_MEMBERSHIP_MISMATCH`.
- Unsafe profile constraints rejected with the specific constraint code (`PROFILE_CONSTRAINT_RISK`, `PROFILE_CONSTRAINT_TARGET_TYPE`, `PROFILE_CONSTRAINT_TECHNIQUE_TAG`, or `PROFILE_CONSTRAINT_EXECUTION`).
- Discovery non-member manifests skipped with `PROFILE_MEMBERSHIP_MISMATCH` in `warning_codes` / `warning_details`, while malformed manifests and duplicate IDs still fail closed.
- Discovery and explicit manifest paths both run through the same profile gate.
- Planned output binds profile ID and SHA-256.
- Full repo JSON parsing and project review wrapper still pass.

Route non-trivial profile contract changes through independent Claude/Cowork review because the profile is a safety gate, not just a UX preference.