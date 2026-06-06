> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Safety-sensitive existing-artifact upload TDD pattern

Use this reference when adding a CLI path that uploads or mutates external state from an already-generated artifact (for example a private canary upload of a reviewed local MP4).

## Test-first boundary cases

Write RED tests before implementation for:

1. Command registration and lock behavior: the side-effecting command must be marked lock-protected if concurrent runs could duplicate uploads or mutate shared state.
2. Exact artifact inputs: require an explicit artifact path and metadata path; reject non-existent files, wrong extensions, invalid UTF-8/JSON, and metadata `local_path` mismatches.
3. Fail-closed destination gates: require pre-populated expected destination identifiers/titles before touching OAuth/upload APIs; call the existing destination guard before upload.
4. Explicit approval phrase: require fresh wording that names the channel, exact resolved artifact path, private-only intent, no scheduler, no public/unlisted, and no active config/default changes. Treat examples in docs as shape only, never authorization.
5. No generation path: patch/mock the generator entrypoint and assert it is not called.
6. Private-only upload call: assert `privacy_status="private"` and `publish_at=None` are passed, with no CLI knobs for public/unlisted/scheduled variants.
7. Pre-upload QA: strict artifact/render QA must run immediately before the external side effect and abort on FAIL/error.
8. Partial failure contract: if upload fails after local DB insert, leave an unuploaded row and preserve the local artifact; if upload succeeds but DB finalization fails, write an explicit recovery note with the external id and re-raise.

## Validation bundle

After GREEN, run focused unit tests, compile touched modules, project validate/status checks, lock absence check, and `git diff --check`. If the project uses handoff files, record the safety envelope and validation commands there.

## Pitfalls

- Do not use the normal `create` or generation command as a shortcut to upload a reviewed artifact; it may regenerate a different video.
- Do not let docs/examples double as current approval.
- Do not fill destination identifiers or run auth/auth-check automatically unless the user explicitly authorized that separate step.
- Do not rely only on global privacy defaults; assert the actual upload call is private and unscheduled.
