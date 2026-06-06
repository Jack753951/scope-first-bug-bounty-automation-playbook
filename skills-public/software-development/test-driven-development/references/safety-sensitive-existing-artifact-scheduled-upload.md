> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Safety-sensitive existing-artifact scheduled upload (TDD pattern)

Use this reference when adding or changing commands that schedule/upload an already-rendered artifact, especially YouTube `publishAt` flows. This is class-level guidance distilled from a one-off Psychology canary and should be adapted to future channels/artifacts.

## Core shape

Prefer a narrow existing-artifact path over enabling a generic generation/scheduler lane when the user wants to schedule one reviewed canary:

1. Require exact `--channel`, `--video-path`, `--metadata-path`, and `--publish-at` inputs.
2. Require a fresh approval phrase naming the exact channel, resolved video path, publish time, and forbidden side effects.
3. Load metadata without invoking the generation pipeline.
4. Verify metadata `local_path` matches the exact MP4.
5. Require expected destination fields before OAuth/upload.
6. Run strict render QA immediately before upload.
7. Enforce upload destination guard immediately before upload.
8. Upload with `privacy_status="private"` plus the exact validated `publishAt`.
9. Record a DB row and document any partial-failure recovery.
10. After a one-off schedule, restore any temporary gate toggles so generic generation remains clamped.

## RED tests to write first

Add failing tests before implementation for these gates:

- CLI command is lock-protected.
- Missing expected destination fields fail before upload.
- Approval phrase must include exact channel, path, publish time, and side-effect prohibitions.
- Metadata `local_path` mismatch fails.
- The success path does not call the generation pipeline.
- Upload is private with `publishAt`, not public/unlisted/immediate.
- Upload failure after DB insert is surfaced, not silently accepted.
- `publishAt` validation rejects:
  - empty value
  - malformed value such as `not-a-date`
  - timezone-naive value such as `2026-05-20T01:00:00`
  - past timestamp such as `2000-01-01T00:00:00+00:00`

For future-proof success fixtures, use a far-future timestamp like `2099-05-20T01:00:00+00:00`, not a near real date that will drift into the past.

## Publish time validation

Implement fail-closed validation before DB insert/upload:

- strip whitespace
- accept valid ISO 8601 with timezone
- optionally accept trailing uppercase `Z` by parsing it as `+00:00`
- reject timezone-naive datetimes
- reject non-future datetimes compared to `datetime.now(timezone.utc)`
- return the original stripped valid string for approval phrase matching and upload metadata, unless the API requires normalization

Optional hardening: require a minimum future buffer, e.g. now + 5/15 minutes, if the provider rejects very-near-future schedules.

## Gate restoration pitfall

If a one-off canary needs a temporary channel gate toggle (for example a render acknowledgement required only by the scheduled-upload path), reset it immediately after the one-off upload. Then verify the generic channel path still reports the safe/clamped state. This prevents a canary exception from becoming accidental channel activation.

## Validation checklist

After GREEN:

- focused pytest for the upload/schedule path
- py_compile for touched Python files
- project validate command
- destination/gate status check for the channel
- `.agent.lock` clear
- `git diff --check`
- independent engineering review for upload/scheduler/privacy/OAuth-adjacent changes
- update repo handoff / accepted changes with explicit safety boundaries

## Safety language for handoff

Record what did NOT happen: no generic `create`/`draft`/`loop`/`remake`, no Windows Task Scheduler edit, no privacy default change, no channel engine switch, no runtime-data deletion, and no secrets printed/copied.
