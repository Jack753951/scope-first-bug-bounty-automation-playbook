> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# youtube_agent Storytime SFX audition review pattern

Use this when the user asks for a Storytime.exe/generated-media sample that uses newly collected sound effects and wants Claude Code to review the visuals and audio.

## Durable workflow correction

- Follow `catalog first, classify second` for all user-provided media candidates.
- Put files/URLs into the repo素材庫/quarantine manifest before assigning risk labels or deciding keep/drop.
- Record `download_date` for each new candidate, plus local path, file size, duration, codec metadata, SHA256, source pack, and any license/status gaps.
- Do not copy quarantined candidates into active `assets/` just because they were used in an internal audition.

## Internal SFX audition packet shape

Create an upload-free packet under `handoff/`, not an active channel output:

- `*.mp4` sample using the current safe visual baseline.
- cue sheet JSON mapping `time`, `slot`, `filename`, trim, volume, purpose, risk label, download date, source pack, and production status.
- provenance JSON that explicitly says local audition only, upload-free, not production-ready, no active asset copy, no channel activation, and license/Content-ID gaps remain.
- contact sheets, waveform, spectrogram, silencedetect, ffprobe, and a local report.
- optional full-track loudness checks (`volumedetect`, `ebur128`) if audio balance matters.

## Claude Code review prompt

Use Claude Code as a read-only reviewer with a compact artifact list. Ask for:

1. reviewer identity / route / visible model if exposed;
2. verdict (`STRONG_INTERNAL_SAMPLE`, `USABLE_INTERNAL_SAMPLE_WITH_FIXES`, `REVISE_INTERNAL_SAMPLE`, or `REJECT`);
3. visual review: first 4s, beat ladder, pause/drop, final vote card, mobile/readability;
4. audio review: cue alignment, conceptual fit, keepers, trim/lower/remove candidates;
5. safety/provenance: no production clearance, item-level license/Content-ID gaps, no active copy/upload/channel activation;
6. blockers before public/canary;
7. next safe action.

If Claude Code lacks native audio playback, require it to say so and base audio review on cue sheet/waveform/spectrogram/silence/ffprobe evidence.

## Max-turn recovery

For broad generated-media packets, Claude Code may hit `error_max_turns` while reading artifacts. Preserve the raw JSON, extract `session_id`, then resume with a one-turn no-tools prompt asking it to return only the required Markdown review. Save both raw outputs and the extracted Markdown.

## Safety boundaries

- Internal sample/review is not production approval.
- Do not infer public/canary readiness from a positive internal verdict.
- Do not upload, schedule, touch OAuth/token/client_secret, create channel configs, change `DEFAULT_PRIVACY`, or copy candidate media into active `assets/` during this workflow.
- After review, update repo handoff/decision files and verify `.agent.lock`, channel config absence, `DEFAULT_PRIVACY`, and no active candidate SFX copy.
