> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Media Subtitle/Audio Alignment Debugging

Use this reference when a generated short/video appears to have captions out of sync with narration.

## Durable lesson

Do not rely on contact sheets or still-frame visual QA to validate subtitle timing. Contact sheets can prove readability and placement, but they can miss systematic drift where subtitles are readable yet early/late by 1-2 seconds. Use an independent audio-to-word timing pass.

## Investigation pattern

1. Identify the exact local artifact directory and its `final_short.mp4`, `voiceover.mp3` or audio track, and `subtitles.srt`.
2. Run an independent speech-to-word timing estimate on the audio, preferably with a small/fast local Whisper model for triage.
3. Parse SRT blocks and normalize text for matching.
4. Compare each SRT block start/end with the estimated span of the words it contains.
5. Report:
   - number of subtitle rows,
   - count and percentage with absolute drift > 0.5s,
   - mean absolute start/end deltas,
   - max absolute start/end deltas,
   - representative worst rows.
6. Treat widespread >0.5s drift or max drift around 1s+ as a public/publish blocker until fixed and re-QAed.
7. Separately run visual QA/contact sheets for readability, placement, crop, and pacing; do not let visual readability override timing metrics.

## Common root cause

Average-distributed SRT timing is unsafe for narration. If the system chunks script text and evenly divides the total audio duration, natural pauses, phrase length, TTS emphasis, and sentence breaks accumulate drift over time.

Fix at the source by generating SRT from real word timings or forced alignment while preserving the intended script text.

Important hardening pitfall: a local/opt-in repair path is not enough. If a prior fix added `generate_srt(..., align_with_word_timings=True)` only to one-off rerender scripts, the main render path may still call `generate_srt(audio, job_dir, narration)` and keep producing average-distributed captions. After confirming the fix works on a rerender, add regression tests and wire the fix into the production/default path for the affected channel class, or add an explicit fail-closed gate that blocks upload/scheduling unless the exact artifact has passing alignment evidence.

Do not let a generic render QA PASS imply timing safety unless that QA actually compares subtitle timestamps against spoken-word timing. Presence/line-length/font checks are readability gates, not alignment gates.

## Safety pattern for live-media projects

When the affected artifact may already be uploaded privately:

- Keep the existing upload private.
- Do not publish, schedule, replace, or re-upload without explicit user approval for the exact artifact/action.
- Create upload-free local rerenders first.
- Re-run the same alignment QA on the rerender.
- Only after timing QA passes should the artifact enter private human review or public-canary discussion.

## Replacement rerender pattern when raw assets are gone

If a flawed uploaded artifact has lost its raw clip/project assets and only the master `final_short.mp4`, `voiceover.mp3`, `subtitles.srt`, and metadata remain, do not pretend it is a clean raw-assets rerender. Use a conservative repair label and gate it accordingly:

1. Transcribe `voiceover.mp3` with word timestamps (for triage, a small local Whisper model can be sufficient if the same model is used for independent QA and thresholds are explicit).
2. Preserve the existing subtitle text/chunking unless there is a separate script edit request.
3. Rebuild SRT cue timings from real word spans rather than average audio division.
4. Cover the old burned subtitle band with an opaque enough overlay; visually inspect contact sheets for ghosted old captions before upload.
5. Burn the new word-timed subtitles and rerun alignment QA on the exact repaired MP4/job directory.
6. Run a separate visual/contact-sheet QA because timing PASS does not prove the repair looks clean.
7. Mark the artifact as a cover-and-reburn/private replacement candidate only; do not public-promote without explicit user review and, preferably, a clean raw-assets rerender.

A useful failure signature from `youtube_agent`: old average-timed Reddit Shorts can show many rows over ±0.5s drift while generic render QA still passes, because the generic gate checks existence/length/readability but not spoken-word timing. Treat that as a script hardening issue: wire word-timed subtitles into the main render path or require exact-artifact passing alignment evidence before upload/scheduling.

## Report metadata

For this user, media QA and third-party review reports should include:

- reviewer route/tool,
- visible runtime model if exposed,
- provider or CLI version if visible,
- review focus,
- limitations if the exact underlying model is not exposed.
