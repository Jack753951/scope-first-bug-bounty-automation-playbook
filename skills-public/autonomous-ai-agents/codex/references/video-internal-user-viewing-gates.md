> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Video Internal User-Viewing Gates

Use this reference when a Shorts/video automation project has upload-free scaffolds and needs a machine-checkable rung before telling the user a local/internal sample is ready to watch.

## Purpose

A user-viewing gate is not a publish gate. It answers only: "Do the local artifacts have enough real story/visual/audio evidence for internal viewing?" Keep upload, public visibility, scheduler activation, OAuth, and production asset approval as separate explicit gates.

## Recommended evidence bundle

Require the gate to read artifacts directly rather than trusting a final markdown report:

- Disabled-only channel state: no active `channels/<channel>.json`; disabled/proposal config exists.
- Forbidden runtime surfaces: scan helper modules after stripping docstrings/comments for upload/OAuth/scheduler/runtime imports (`agent`, `pipeline`, `youtube_api`, Google auth/API clients, token/client-secret strings, scheduler, runtime `data/`, network fetches).
- Source/template metadata: source type, template family, rewrite/copy-safety summary, target audience, runtime, and provenance flags.
- Joke/story localization metadata for English meme/story formats: localized hook, relatable setup, absurd escalation, visual punchline prop, comment bait, and a reason the punchline is localized rather than literal translation.
- Visual evidence: contact sheet or preview index with actual `<image>` references to project-owned sticker/background/prop assets; fail if it is text-only.
- Safe SFX manifest: project-generated or otherwise licensed source types only, files exist, hashes present when available, and `production_ready=false` for placeholder packs.
- Audio mix evidence: WAV/file exists, duration is positive, waveform/ffprobe status exists, no `anullsrc`-only signature, and non-silence evidence. Prefer decoding samples directly when practical; manifest/waveform JSON alone is weaker.
- Asset manifest evidence: assets remain inside the channel asset tree and carry source/license/production-readiness metadata.

## Validation pattern

1. Run/generate prerequisite upload-free rungs (SFX pack, audio mix fixture, template renderer/contact sheet) before the gate, or have the gate materialize them locally without crossing upload/runtime boundaries.
2. Run focused tests for the gate and all prerequisite rungs.
3. Run the gate directly and require a PASS count with JSON + markdown report output.
4. Run project safety validation, compile checks, `git diff --check`, and confirm no run lock remains.
5. Visually inspect the preview index/contact sheet: verify guard text (`DISABLED-ONLY`, `NO UPLOAD`), all template entries, real thumbnails, no broken images, no severe clipping/overlap.
6. If an independent worker reports validation blocked by its sandbox (for example missing Python), rerun the exact requested checks in the authoritative project shell/venv before deciding final status. Record the worker blocker separately; if local checks pass, update handoff/review notes to PASS rather than leaving stale `NEEDS_CHANGES` wording.

## Acceptance wording

Use precise language:

- Accepted: "internal upload-free user-viewing rung passed."
- Not accepted: "production-ready", "publish-ready", "public-ready", or "channel activated" unless separate activation/publication gates passed with explicit user approval.

## Common residual notes

These are acceptable for an internal rung but must be tracked before production art/render decisions:

- Thumbnail labels may truncate in a contact sheet if the image evidence is still visible.
- Placeholder prop art may be icon/text-card-like; acceptable for visual QA candidates but not final production assets.
- Non-silence checks based only on generated summary JSON should later be hardened with direct WAV sample decoding.
