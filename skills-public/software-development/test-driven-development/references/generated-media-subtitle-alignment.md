> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Generated Media Subtitle Alignment Regression Pattern

Use this reference when a generated Short/video passes render QA but a human reports captions drifting against speech.

## Durable lesson

Do not treat matching video/audio duration as evidence that captions are aligned. A video can have perfectly matched container/audio durations while SRT chunks are wrong because caption timing was distributed evenly across script chunks instead of derived from speech timestamps.

## Root-cause pattern

Symptoms:

- Captions appear early or late even though final MP4 duration and voiceover duration match.
- Render QA passes; visual frames look readable; human playback still feels off.
- SRT chunks have nearly uniform durations that ignore TTS pauses, suspense beats, or sentence pacing.

Likely cause:

- The pipeline preserved script text but assigned subtitle intervals by average chunk spacing.

## TDD pattern

1. Add a focused RED test for a helper that keeps the original script text but accepts real word timings.
2. Assert chunk start/end times come from the supplied word timings, not average duration steps.
3. Add a test that the production subtitle generator only uses word timings through an explicit opt-in flag, preserving default behavior for existing callers.
4. Verify fallback behavior: if word timings are unavailable or malformed, the generator should fail safe to the previous path or Whisper SRT, not crash a production workflow.
5. Only after GREEN, rerender the local artifact upload-free.

## Verification pattern

- Run the focused subtitle tests.
- Run `py_compile` for the changed pipeline/helper scripts.
- Run the project safety validator.
- Generate an alignment QA report comparing SRT chunk timings to independent ASR/word timings.
- Treat any chunk drift over about ±0.5s as a public-canary blocker for Shorts unless a human explicitly accepts it.
- Use visual/contact-sheet QA for readability and placement, but do not let it replace playback/timing QA.

## Safety boundary

For upload/publication-sensitive video projects:

- Rerender locally only.
- Mark metadata as upload-free / do-not-upload without explicit approval when producing a replacement candidate.
- Do not replace an already uploaded private video, publish, schedule, mutate OAuth, or change destination/default privacy as part of the fix unless the user explicitly approves that exact artifact/action.

## Review metadata

When independent review is involved, record:

- reviewer route/tool,
- visible runtime model/provider,
- whether the exact underlying model is not exposed,
- review focus,
- validation commands and results,
- safety verdict.
