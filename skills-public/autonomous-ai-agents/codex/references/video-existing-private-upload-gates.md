> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Video existing-artifact private upload gates

Use this reference when a Shorts/video automation project has a local MP4 that already passed upload-free review and the next rung is a safe private canary path.

## Core rule

Do not use a normal `create`/generate command as a shortcut for uploading a reviewed artifact. Generation commands can create a new video, new metadata, or a different script path. A private canary for an already-reviewed artifact needs an explicit existing-artifact upload path.

## Minimal command contract

A future `upload-existing-private`-style command should require explicit inputs:

- Channel name.
- Existing MP4 path.
- Matching metadata JSON path.
- Fresh approval phrase that names private-only upload and the exact artifact.

It should not accept public/unlisted privacy, scheduler, publishAt, or normal create/draft generation flags.

## Fail-closed preflight order

1. Require channel, MP4 path, metadata JSON path, and approval phrase.
2. Resolve paths and refuse missing files, non-MP4 video, invalid UTF-8 JSON, or metadata `local_path` mismatch.
3. Confirm metadata has enough upload snippet data: title, topic, narration/description source, hashtags/tags.
4. Hard-code `privacy_status="private"` and `publish_at=None`.
5. Refuse scheduler/public/unlisted knobs even if the normal upload pipeline could clamp them later.
6. Run strict render QA immediately before upload; abort on FAIL or exception. Do not rely only on a downstream clamp-to-private gate for private canaries.
7. Require configured expected destination id/title to be populated; then run the upload channel guard immediately before the YouTube insert.
8. Ensure the command never calls generation paths such as `create_short`, `make_draft`, or `make_and_upload`.
9. Insert/mark DB state deliberately after preflight; preserve enough recovery information if later steps fail.

## Partial-failure contract

- Preflight fails before upload: no DB insert, no upload attempted.
- DB insert fails before upload: no upload attempted.
- Upload fails after DB insert: preserve the DB row with no YouTube id, print the row id and failure reason, and do not retry automatically.
- Upload succeeds but DB mark/upload recording fails: immediately print the returned YouTube id, write a handoff note with channel/path/metadata/id, and require manual DB repair before analytics loops depend on the upload.
- Never delete local MP4s, metadata, token files, OAuth files, or DB rows as rollback.

## Handoff wording

Design-only or approval-packet docs must explicitly say:

- Publication/canary/upload authorization remains `NO` until the user gives separate explicit approval.
- Example approval wording is documentation only, not current approval.
- No auth/auth-check, OAuth/token/client-secret, scheduler, default privacy, destination fields, runtime data, or channel activation changes were made.

## Validation after implementation

Run focused tests for the pure metadata/preflight path, strict render-QA aborts, private-only upload arguments, and partial-failure DB behavior. Then run local project validation and check `.agent.lock` is absent.