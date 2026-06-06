> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Module Profiles

Profiles are repo-local JSON contracts consumed by the dry-run module runner.
They constrain which already-validated module manifests may be selected during
offline discovery. Profiles are data only: they do not execute modules, scanners,
subprocesses, callbacks, or network clients.

## Contract shape

A `module_profile/1.0` document lives at `modules/profiles/<profile_id>.json`
and must pass `scripts/validate_module_profile.py` before the runner may use it.
The runner then binds the selected profile into planned `run/1.0` previews via
`execution.profile_id` and `execution.profile_sha256`.

Required profile fields:

- `schema_version`: currently `module_profile/1.0`.
- `profile_id`: stable ID matching the file requested by the runner.
- `name` / `description`: human-readable authoring context.
- `mode_allowlist`: currently only `dry-run`.
- `risk_level_allowlist`: allowed manifest risk levels.
- `target_type_allowlist`: allowed target type vocabulary.
- `technique_tag_allowlist`: allowed manifest technique tags.
- `execution_constraints`: exact execution posture required from manifests.
- `output_constraints`: whether findings/evidence emission is allowed.
- `required_safety_gates_true` / `required_safety_gates_false`: mandatory safety gates.

Unknown, missing, malformed, unsupported, path-escaping, mismatched, or unsafe
profile files fail closed.

## audit-baseline

Path: `modules/profiles/audit-baseline.json`

Purpose: conservative Level 1 metadata audit planning.

Safety envelope:

- mode allowlist: `dry-run`
- risk allowlist: `info`, `low`
- target types: `url`, `domain`, `ip`, `cidr`
- technique tags: passive-only metadata tags
- `supports_dry_run=true`
- `requires_network=false`
- `network_access=none`
- `target_touching=false`
- `destructive=false`
- `intrusive=false`
- findings/evidence emission disallowed at this stage
- scope/policy/manual-verification safety gates remain mandatory

`audit-baseline` is the current conservative policy, not a permanent limit on
future product shape. Any broader profile must go through explicit schema,
safety, documentation, and test review.

## Stable error-code vocabulary

P2-8 added additive structured issue fields while preserving existing
human-readable `errors` / `warnings` arrays. P2-9 keeps that vocabulary in the
standard-library-only `scripts/profile_issues.py` helper so runner and validator
CLIs share constants without adding execution behavior. Runner and discovery JSON
payloads may include:

- `error_codes`: sorted unique machine-readable error codes.
- `warning_codes`: sorted unique machine-readable warning codes.
- `error_details`: objects with `code`, `message`, `severity`, `component`, and
  optional `path`, `field`, `profile_id`, `module_id`.
- `warning_details`: same shape for non-fatal exclusions/skips.

Profile loader / validator codes:

- `PROFILE_ID_INVALID`: requested profile id fails the allowed ID format.
- `PROFILE_NOT_FOUND`: `modules/profiles/<profile>.json` is absent.
- `PROFILE_PATH_INVALID`: resolved profile path escapes `modules/profiles` or is not a file.
- `PROFILE_READ_ERROR`: profile cannot be read due to an OS/read failure.
- `PROFILE_MALFORMED_JSON`: profile JSON cannot be parsed.
- `PROFILE_SCHEMA_INVALID`: profile contract validator rejects the profile.
- `PROFILE_ID_MISMATCH`: loaded `profile.profile_id` does not match the requested id.

Profile selection / constraint codes:

- `PROFILE_MEMBERSHIP_MISMATCH`: manifest `execution.default_profile` differs from selected profile.
- `PROFILE_CONSTRAINT_MODE`: requested mode is not allowed by the profile.
- `PROFILE_CONSTRAINT_RISK`: manifest `risk_level` is outside the profile allowlist.
- `PROFILE_CONSTRAINT_TARGET_TYPE`: requested or manifest target types violate profile/manifest constraints.
- `PROFILE_CONSTRAINT_TECHNIQUE_TAG`: manifest technique tags are outside the profile allowlist.
- `PROFILE_CONSTRAINT_EXECUTION`: execution flags violate profile constraints.
- `PROFILE_CONSTRAINT_OUTPUT`: output contracts violate profile output constraints.
- `PROFILE_CONSTRAINT_SAFETY_GATE`: manifest safety gates do not satisfy profile requirements.
- `PROFILE_EMPTY_SELECTION`: discovery completed without selected manifests and no more specific hard loader/schema error explains the denial.

Discovery treats non-member manifests as structured warnings/exclusions when
other manifests may still be selected. Explicit manifest mode treats membership
or constraint violations as hard errors.

## Example failures

Missing profile:

```json
{
  "error_codes": ["PROFILE_NOT_FOUND"],
  "errors": ["module profile not found: modules/profiles/unknown.json"]
}
```

Unsafe profile contract:

```json
{
  "error_codes": ["PROFILE_SCHEMA_INVALID"],
  "errors": ["module profile modules/profiles/audit-baseline.json: profile.execution_constraints.requires_network must be false"]
}
```

Target-touching manifest under `audit-baseline`:

```json
{
  "error_codes": ["PROFILE_CONSTRAINT_EXECUTION", "PROFILE_CONSTRAINT_TECHNIQUE_TAG"],
  "errors": ["module manifest modules/checks/.../module.json: execution.target_touching violates profile audit-baseline"]
}
```

These codes are emitted at the point of detection and should not be derived by
parsing free-form messages.
