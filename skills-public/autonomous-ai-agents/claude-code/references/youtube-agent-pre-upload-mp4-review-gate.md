> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# youtube_agent pre-upload MP4 review gate

Use this reference when `youtube_agent` is about to upload, schedule, promote, or canary an exact MP4 artifact.

## Durable lesson

Do not treat local render QA as enough when the user has reported obvious subtitle/voice drift. A render QA pass that checks duration, metadata, subtitle presence/length, font caps, or profile labels is a readability/shape pass, not an audio-subtitle timing pass.

For exact artifacts, pre-upload review should be Claude Code-led for this user/project:

1. DEFAULT/EXPECTED: a Claude Code read-only reviewer explicitly checks the MP4/contact-sheet/audio-subtitle evidence and returns a verdict.
2. SUPPLEMENTAL: deterministic alignment QA artifacts comparing SRT timestamps to spoken-word timing should be attached as evidence, especially for redditstories/redditscary subtitle-sync regressions.
3. EMERGENCY FALLBACK ONLY: deterministic alignment evidence without Claude Code review may be used only when Claude Code is unavailable and the handoff explicitly says so; schedule/upload should otherwise block until Claude Code returns a verdict.

If Claude Code has not returned a verdict and no explicit emergency fallback is documented, block upload/schedule.

## Required verdicts

Use exactly one of:

- `APPROVE_FOR_UPLOAD`
- `REVISE_BEFORE_UPLOAD`
- `BLOCK_UPLOAD`

Only `APPROVE_FOR_UPLOAD` may proceed to private upload, scheduled-private upload, public scheduling, publication, or canary promotion.

## Review prompt requirements

A Claude Code review prompt should name the exact local MP4 and require checking:

- voice/subtitle alignment across the artifact,
- first 3-5 seconds timing and readability,
- final CTA/end-card timing,
- obvious visual/audio blockers,
- limitations of the review route.

For this user, report route/tool, visible model/runtime if exposed, provider/CLI where visible, and artifact path.

## Hardening pitfall

If a timing fix was proven only in a one-off rerender script, do not assume the main pipeline is fixed. Verify the production/default render path uses the same word-timed/forced-alignment behavior, or require exact-artifact alignment evidence before upload/schedule.

## Scheduled exact-artifact pattern

When the user asks to schedule a specific canary/time and the repo already has candidate MP4s, prefer the exact-artifact path over generic generation/looping:

1. Resolve the exact MP4 + metadata pair for each channel.
2. Require local render QA PASS for the exact path.
3. Require subtitle/voice sync evidence in metadata for English `redditstories` / `redditscary` (`subtitle_timing_mode` word-timed or forced-alignment class + `subtitle_alignment_status=pass`).
4. Create a small contact sheet with ffmpeg and run a visual pre-upload review for readability, first seconds, final/CTA area, black/broken frames, and duplicate subtitle-band blockers.
5. Write `pre_upload_mp4_review_verdict=APPROVE_FOR_UPLOAD` into metadata only after the evidence is collected; include route/tool and limitations.
6. Check OAuth destination guard immediately before upload/schedule.
7. Use `upload-existing-scheduled` with an approval phrase that names the channel, exact local MP4 path, publish time, private scheduled upload, and explicit negatives: no Windows Task Scheduler, no `DEFAULT_PRIVACY`, no immediate public, no generic create/loop, no active engine/channel default changes.
8. After upload, read back the YouTube video via API and verify `privacyStatus=private`, expected `publishAt` (UTC equivalent of requested local time), and `selfDeclaredMadeForKids=false`; record DB id, YouTube id/URL, destination, and validation results in repo handoff.

If a channel's candidate only fails because it lacks metadata verdict but already has deterministic word-timed evidence, it is acceptable to add the verdict after a fresh pre-upload review. Do not bypass actual render QA or destination guard.

## Safety

Do not delete, unpublish, reschedule, re-upload, mutate OAuth/token/channel config/default privacy, or change Windows Task Scheduler unless the user explicitly asks for that exact side effect. Treat user wording like "schedule tomorrow 9" as approval for that exact scheduled-private artifact path only, not as approval for daily public publishing, generic loops, channel default changes, or scheduler changes.
