> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# youtube_agent Storytime.exe reference-library hygiene

Use this when a session handles Storytime.exe examples, downloaded references, candidate licensed assets, or user-provided material for the `youtube_agent` project.

## Class-level rule

Keep a quarantine-first reference library for Storytime.exe. Reference material can teach structure, timing, caption hierarchy, persona grammar, and payoff templates, but it must not silently become production material.

User-corrected workflow: **catalog first, classify second**. When the user supplies files/URLs/assets, first create or append the素材庫/quarantine record with path/source notes/hash/metadata/download date, then assign fit/risk labels. Do not let classification live only in chat.

User-corrected pitfall: do not treat "not in the repo" as "no assets available." For Storytime local iterations, check the user's provided/downloaded asset locations (especially `<user-home>`) and any existing library manifests before falling back to generated placeholders. If assets are found outside the repo, create a quarantine catalog under `handoff/storytime_exe_reference_library/00_inbox/<catalog-id>/` with `asset_catalog.json`, `INDEX.md`, SHA256s, original paths, candidate roles, risk labels, and `production_ready=false`. Future render/review workers should consume the catalog path, not rediscover assets ad hoc.

Recommended repo location:

- `handoff/storytime_exe_reference_library/`

Recommended subfolders:

- `00_inbox/` — new user submissions and filled templates.
- `01_reference_urls/` — URL-only public/competitor references.
- `02_user_owned_examples/` — files the user owns, still read-only until reviewed.
- `03_candidate_licensed_assets/` — candidate licensed packs before manifest promotion.
- `04_license_notes/` — license text/proof summaries with sensitive info redacted.
- `05_review_packets/` — Hermes/Claude/Codex reviews, contact sheets, risk triage, decisions.
- `06_approved_for_generation/` — empty by default; only after explicit manifest/license gate.

## Risk labels

- `GREEN_PRODUCTION_CANDIDATE`: source/license appears clear, but still needs manifest validation before active generation.
- `YELLOW_INTERNAL_REFERENCE_ONLY`: useful structure/style/timing reference; no literal reuse.
- `RED_DO_NOT_REUSE`: high-risk copyrighted/IP/watermarked/unclear material; avoid beyond notes.
- `UNKNOWN_NEEDS_REVIEW`: not enough source/license information.

## yt-dlp correction pattern

If the user clarifies that examples were downloaded with yt-dlp, immediately correct any earlier licensed-candidate assumption:

- Set `risk_label = YELLOW_INTERNAL_REFERENCE_ONLY`.
- Set `review_state = READ_ONLY_REVIEWED` if already analyzed, or `NEW/NEEDS_INFO` if not.
- Keep `production_ready = false`.
- Record that allowed reuse is only abstract structure/template learning.
- Explicitly forbid literal frames, captions, translations/paraphrases, audio, SFX, characters/IP, watermarks, and production renderer ingestion.

This is true even if the references are very useful creatively. yt-dlp is approved for reference intelligence, not for asset acquisition.

## Allowed structural lessons from downloaded references

- duration bands;
- beat maps;
- hard-cut cadence;
- caption hierarchy;
- locked title band / changing sub-caption pattern;
- persona staircase;
- final-third payoff or stinger structure;
- opening hook architecture;
- requirements for original/licensed replacements.

## Not allowed from downloaded references

- copied frames/stills;
- copied or translated captions;
- copied audio/music/SFX/voices/stingers;
- copied characters/mascots/IP;
- watermarks/editor branding;
- moving files into active `assets/` or renderer paths;
- treating the downloaded file as public/canary material.

## Claude Code review workflow

For Storytime reference reviews, prefer Claude Code as a read-only visual/format reviewer:

1. Build a compact packet: ffprobe, opening_4s, 1fps/2fps contact sheets, waveform/spectrogram/silence log, and source/risk notes.
2. For user-provided SFX/audio candidates, build an upload-free MP4 audition packet from already-cataloged quarantine assets only; include cue sheet, provenance, per-cue risk/download date, and loudness evidence. See `youtube-agent-storytime-sfx-audition-review.md` for the detailed pattern.
3. Run Claude Code with read-only tools or no tools and explicit no-upload/no-OAuth/no-scheduler/no-channel-config boundaries.
4. Capture raw JSON when possible, extract the review, then have Hermes synthesize and verify locally.
5. Update `handoff/accepted_changes.md`, Storytime decision log, and the library index.

## Local iteration vs production promotion

For Storytime.exe, local-only learning drafts should be fast and asset-backed when the user has already supplied/downloaded material. Use cataloged meme/GIF/WebP assets, SFX, BGM, and VO placeholders to approximate the intended viewing experience. Avoid placeholder-only drafts as the default; reserve them for isolating renderer/schema bugs. Keep audit footers, license notes, and reference mosaics in sidecar reports/contact sheets unless the task specifically asks to visualize them in-frame.

This speed rule does **not** promote assets to production. Downloaded or unreviewed assets remain `UNKNOWN_NEEDS_REVIEW` or `YELLOW_INTERNAL_REFERENCE_ONLY`, `production_ready=false`, and no upload/canary/publication/OAuth/scheduler/channel config/default-privacy action is implied.

## Production promotion gate

Before anything moves from reference/candidate folders into generation/public use, require:

- explicit source/license record;
- commercial YouTube permission;
- edit/compositing permission;
- repeated automated-render permission;
- attribution/Content ID restrictions recorded;
- SHA256/provenance manifest;
- watermark/trial-branding check;
- local visual/media QA;
- explicit user approval for upload/canary/publication.

Until then, Storytime.exe remains disabled/internal/upload-free, and no `channels/storytime_exe.json` should be created from reference-library work alone.
