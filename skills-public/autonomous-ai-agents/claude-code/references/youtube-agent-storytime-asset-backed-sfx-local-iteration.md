> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# YouTubeAgent Storytime — asset-backed SFX local iteration correction

Use this reference with the `claude-code` skill when working on Storytime.exe / cat-meme-theater internal samples, especially after a user asks why provided素材, GIF/meme material, SFX, or BGM were not used.

## Trigger

Load/apply this pattern when:

- The task is a local-only Storytime sample or review rung.
- The user provided meme images, GIF-like assets, SFX, BGM, or reference materials.
- A previous draft was placeholder-only, renderer-only, or too conservative to judge human fun/retention.
- The goal is creative learning, not upload approval.

## User correction captured

The user corrected that placeholder-only local drafts make iteration too slow. For Storytime local/internal iterations, do not treat local learning like production approval. Use available/provided assets and audio to create a draft that can actually be judged for human fun, rhythm, and retention.

Keep strict gates for upload/OAuth/scheduler/channel/default-privacy/production licensing, but do not let those gates block local asset-backed experiments.

## Default local iteration policy

For local-only Storytime rungs, default to:

1. Asset-backed characters / meme visuals
   - Use provided/current meme images, GIF-like frames, project SVG emotion stickers, or local reference-derived safe transforms.
   - Avoid placeholder-only circles/boxes unless isolating a renderer/schema bug.
   - Tie character assets to explicit emotion states, e.g. smug, panic, shocked, guilty, angry, final-boss.

2. SFX-first timing
   - Use provided/generated SFX cues for beat hits, reaction swaps, transitions, proof reveals, authority entrances, and final stings.
   - Produce a cue sheet mapping each SFX to timestamp, beat role, and story reason.
   - Use at least several distinct cues; do not leave visual drafts silent when SFX exists.

3. BGM / VO placeholders when feasible
   - Add a low-volume bed/BGM or simple generated placeholder bed when no cleared BGM exists.
   - Add local TTS/VO placeholder when available; otherwise strengthen captions + SFX rhythm and record the VO gap explicitly.
   - Mark placeholder audio as `production_ready=false`.

4. Internal reference handling
   - Internal-only reference pixels/audio remain non-production.
   - For local stress/review, reference materials may be used as blurred/downsampled/mosaic overlays or sidecar comparisons when clearly marked `INTERNAL_REFERENCE_ONLY` / `production_ready=false`.
   - Do not copy reference assets into production-approved paths or claim license readiness.

5. Main MP4 should optimize the joke
   - Avoid baking large audit footers, provenance banners, or reference mosaic panels into the primary creative MP4 if they distract from the joke.
   - Put audit evidence in sidecar reports, contact sheets, provenance JSON, or a separate review-only render.
   - The primary MP4 should feel as close as possible to a real Shorts draft while remaining local-only.

## Claude Code implementation prompt checklist

When delegating to Claude Code, include:

- Route/tool identity and visible runtime/model reporting request.
- User correction: local iterations should use assets + SFX/BGM/VO fast; placeholder-only is not the normal creative path.
- Binding safety boundary: no upload, canary, OAuth, scheduler, channel config, `DEFAULT_PRIVACY`, production promotion, or token access.
- Explicit asset roots and SFX roots to inspect.
- Requirements for:
  - asset-backed character/emotion policy
  - SFX cue sheet
  - BGM/bed or VO evidence
  - provenance with `production_ready=false`
  - contact sheets, waveform/spectrogram/silencedetect where audio is relevant
  - validator rejection of placeholder-only main characters, missing SFX, missing audio evidence, missing safety flags, or active channel config
- Validation commands that Hermes must rerun locally after Claude Code finishes.

## Hermes verification checklist

After the worker reports success, Hermes must independently verify:

- Focused pytest for the new rung.
- Adjacent regression tests against the prior rung.
- Generator returns a PASS verdict and writes MP4/spec/report/provenance/cue-sheet/contact sheets.
- `channels/storytime_exe.json` remains absent.
- Visual QA of `contact_1fps.jpg` or equivalent: does it look asset-backed, meme-theater-like, and less placeholder-only?
- Audio evidence exists: SFX cue sheet, waveform/spectrogram/silencedetect, BGM/VO sidecars if promised.

## Verdict guidance

- `CONTINUE_FAST_ASSET_BACKED_INTERNAL_ITERATION`: good local learning artifact, still not upload-ready.
- `REVISE_FOR_HUMAN_FUN`: technically valid but not funny/retentive enough.
- `BLOCK_UPLOAD`: any active channel/upload/OAuth/default-privacy/production-license boundary violation.

Do not promote internal asset-backed samples to upload just because tests pass. Tests prove the packet shape and safety flags, not human entertainment quality or license clearance.
