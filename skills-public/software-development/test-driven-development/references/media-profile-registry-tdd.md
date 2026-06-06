> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Media Profile Registry TDD Pattern

Use this pattern when a generated-media project needs asset/render/QA profile labels before those labels are allowed to influence runtime behavior.

## Intent

Create a narrow, data-only registry that gives reviewers and metadata consumers stable labels such as:

- `asset_profile`
- `render_profile`
- `qa_profile`
- `media_profile_schema_version` or `schema_version`

The first rung must not change generation, rendering, QA pass/fail, upload, publication, scheduling, OAuth/token handling, channel destination, privacy, or channel config behavior.

## RED tests first

Write focused tests before implementation:

1. Known active lanes resolve to exact profile labels and a stable schema version.
2. Unknown lanes fail closed.
3. Unknown payload fields fail closed.
4. Activation/side-effect vocabulary fails closed anywhere in keys or values, including terms like `upload`, `publish`, `public`, `privacy`, `schedule`, `scheduler`, `oauth`, `token`, `destination`, and channel IDs.
5. Validation returns a copy, not the original mutable object.
6. Paused/internal lanes are intentionally absent unless explicitly activated by a separate decision.

Expected RED for a new registry is often `ModuleNotFoundError`; that is acceptable if the missing module is the intended feature gap.

## GREEN implementation

Keep implementation intentionally small:

- A single schema/version constant.
- A closed set of allowed fields.
- A mapping for active lanes only.
- `resolve_*_profiles(lane)` that fails closed on unknown lanes.
- `validate_*_payload(payload)` that rejects missing fields, unknown fields, schema drift, non-string/empty values, and activation vocabulary.
- Return defensive copies.

## Follow-on rungs

Only after the registry is GREEN and adjacent tests pass:

1. Add metadata passthrough tests for the existing metadata helper.
2. Add read-only report label tests if useful.
3. Do not make profiles drive runtime behavior until a separate direction review authorizes that boundary change.

## Verification

Run the focused registry tests, adjacent metadata/channel-engine tests, Python compile checks, project safety validation, lock/default-privacy checks, and whitespace/diff checks before reporting success.
