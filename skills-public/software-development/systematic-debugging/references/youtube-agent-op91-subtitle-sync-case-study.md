> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# YouTube Agent Op91 Subtitle Sync Case Study

Use as a concrete example when debugging recurring subtitle/voice mismatch in generated Shorts.

## Symptom

User reported the YouTube Short `Op91aXp6lN0` had the same obvious subtitle/voice mismatch that had appeared in another channel. The old local artifact was:

- `data/redditstories/output/Delivery_driver_blocks_city_st_1779332851/final_short.mp4`
- `data/redditstories/output/Delivery_driver_blocks_city_st_1779332851/voiceover.mp3`
- `data/redditstories/output/Delivery_driver_blocks_city_st_1779332851/subtitles.srt`

## Root cause evidence pattern

Independent alignment QA compared SRT cue timings to Whisper `tiny.en` word-timestamp spans and found widespread drift:

- rows: 29
- bad_over_0_5s: 22
- mean_abs_start_delta: ~0.510s
- mean_abs_end_delta: ~0.536s
- max_abs_start_delta/end_delta: ~1.346s

The generic render QA still passed because it checked MP4 existence, duration, metadata, subtitle presence, line length/readability, and profile labels — not spoken-word alignment.

Durable lesson: a render QA PASS is not an alignment PASS unless it explicitly compares caption times to speech.

## Repair used when raw assets were gone

Only the finished master, audio, SRT, and metadata remained, so the repair was labeled as a cover-and-reburn private replacement candidate:

1. Transcribe `voiceover.mp3` with word timestamps.
2. Preserve existing SRT text/chunking.
3. Rebuild SRT cue times from word spans.
4. Cover the old burned subtitle band with an opaque black overlay.
5. Burn the rebuilt SRT over the repaired master.
6. Re-run alignment QA and visual contact-sheet QA on the exact repaired MP4.
7. Send the exact artifact and evidence packet to Claude Code/read-only reviewer.
8. Upload only as private if review verdict is `APPROVE_FOR_UPLOAD` and caveats allow private replacement.

## Passing repaired-artifact evidence shape

The repaired artifact had:

- bad_over_0_5s: 0
- mean_abs_start_delta: 0.000s
- mean_abs_end_delta: 0.001s
- max_abs_end_delta: 0.040s
- render QA: PASS
- Claude Code verdict: `APPROVE_FOR_UPLOAD` for private replacement only
- YouTube read-back: `privacyStatus=private`, `uploadStatus=processed`, `publishAt=null`

## Pitfalls

- First visual repair can still show old subtitle ghosting if the overlay is translucent. Inspect contact sheets and switch to fully opaque coverage if needed.
- A cover-and-reburn repair is not equivalent to a clean raw-assets rerender. Do not public-promote it without explicit user review and, preferably, a clean rerender.
- If a prior fix exists only in a one-off rerender script, the bug will recur. Add regression tests and wire word-timed subtitles or an exact-artifact alignment gate into the main render/upload path.
