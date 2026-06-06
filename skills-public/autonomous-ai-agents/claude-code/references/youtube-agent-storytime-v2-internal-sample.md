> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# YouTube Agent — Storytime.exe v2 Internal Sample + Claude Code Visionreview Pattern

Use this when `youtube_agent` needs an upload-free generated-media internal sample reviewed before any channel activation or canary decision, especially Storytime.exe / meme-theater work.

## Trigger

- User says to continue a disabled/internal Storytime.exe lane after reference analysis.
- Prior visual/reference review allowed one improved internal sample but explicitly forbids activation/upload.
- Need Claude Code visual/structure review without spending app-reserved Anthropic API paths.

## Safe implementation boundary

Keep this as an internal evidence rung only:

- Do not create `channels/storytime_exe.json`.
- Do not move disabled config into active discovery.
- Do not upload, schedule, publish, run OAuth, refresh tokens, change destinations, or change `DEFAULT_PRIVACY`.
- Do not reuse competitor frames, captions, audio, SFX, stickers, social-platform assets, or third-party mascot/IP.
- Mark sample manifests `local_reference_only: true`, `upload_free: true`, and `production_safe: false` until public-clearance work is explicitly approved.

## Artifact packet shape

For a generated-media internal sample, produce a compact, reviewable packet under `handoff/<lane>_<date>/`:

- local MP4 sample,
- timed visual beats JSON,
- music/SFX cue manifest,
- provenance manifest,
- ffprobe JSON,
- opening 4s sheet,
- 1fps and 2fps contact sheets,
- waveform,
- spectrogram,
- silence-detect log,
- short report,
- Claude Code visionreview prompt/raw JSON/final markdown.

## Storytime.exe v2 acceptance heuristics

For Storytime.exe / meme-theater internal baselines, check:

- 20–28s duration,
- 4–5 hard-cut persona/story beats,
- locked top title band plus either per-beat caption strip or, for theater rungs, character-local speech bubbles near the active character,
- clear first-4s micro-beats,
- generated/project-owned characters and props,
- visible prop-driven punchline,
- no watermark/editor branding,
- no third-party character/IP resemblance,
- documented synthetic or licensed audio/SFX provenance,
- explicit blockers before activation.

If user feedback says the sample lacks theater, movement, or emotional audio, require a full story-theater remediation rather than a simple louder-audio patch:

- make story source/provenance explicit (`original_joke_style_placeholder` vs documented online/user/public-domain source),
- remove bottom subtitle boxes when requested and use character-head bubbles/captions,
- add character blocking/movement and per-beat background/prop changes,
- map SFX to `emotion` and `story_function`,
- target internal audition loudness around `-20` to `-16 LUFS` with headroom,
- review bubble overlap, punchline readability, and final-card crowding before calling the sample ready for user review.

If user feedback says character motion is meaningless or text should have no frames, add a stricter static-stage/no-box rung. If the user later clarifies that the reference uses mostly static PNG/cutout cats with scale/translate/shake/hard-cut motion, treat that as a renderer-design correction: prefer `static_actor_state + transform_timeline` over GIF-playback-first architecture, split `actors` from `effects`, and encode per-beat `actor_state`, `transform`, `timing`, and `story_reason`. See `references/youtube-agent-storytime-static-png-transform-and-review-routing.md` for the detailed correction.

- keep `stage_home_positions` fixed by default;
- allow character movement only when the beat marks `mode=interaction` or `mode=transition` and includes a `story_reason`;
- render dialogue/title/transition narration as bare stroked text only (`speech_bubble_boxes=false`, `bottom_subtitle_box=false`, and no character/text backplates);
- add short transition narration text during cuts;
- before reviewing the adjusted prototype, provide Claude Code a compact reference target board/brief first, then the prototype/contact sheets, and require the review to confirm that order.

Do not overcorrect the static-stage lesson into a rigid reusable template. For Storytime-style generated media, the durable rule is story-specific stability, not global sameness:

- each story should be able to define its own cast, roles, home positions, backgrounds, layouts, motivated movements, narration, and SFX/emotion map;
- stable positions mean stable within that story's scene plan, not always cat-left/dog-right/tablet-center or the same background pack;
- prefer a `story_scene_spec` / scene-schema abstraction once one representative sample proves the visual grammar;
- when improving a sample, fix obvious local quality issues and move hard-coded cast/layout/movement constants into spec fields, but do not build a fully generic engine before the quality bar is proven;
- after the representative sample is acceptable, require a second mini-story with a different cast/layout/background to prove the renderer is not just swapping dialogue in a fixed theater.

## Claude Code review route

User preference / correction: for Storytime.exe and other generated-media visual/creative work, do not treat Hermes quick visual QA as sufficient when the work is nontrivial, even if the immediate change is deterministic preprocessing such as background removal. Default to Claude Code usage when quota/auth is available: at minimum run role-separated read-only reviews (creative/channel-fit and technical/visual-readability), record raw JSON usage/model/session artifacts, then write a Hermes synthesis. If implementation/layout polish is needed and the user has asked to spend Claude Code usage, route the next bounded implementation rung to Claude Code rather than having Hermes silently do all changes.

Use Claude Code print mode in read-only review style:

```bash
claude -p "$(cat handoff/<packet>/claude_visionreview_prompt.md)" \
  --allowedTools 'Read' \
  --output-format json \
  --max-turns 5 \
  > handoff/<packet>/claude_visionreview.raw.json
```

If it hits `error_max_turns` but produced a session id, resume narrowly and forbid tools:

```bash
claude -p 'Continue the previous generated-media review from the artifacts already read. Do not use tools. Return concise markdown only: route/model; verdict; visual QA; safety/provenance; blockers; next action.' \
  --resume <session_id> \
  --output-format json \
  --max-turns 1 \
  > handoff/<packet>/claude_visionreview_resume.raw.json
```

Extract `result` from the successful JSON into `claude_visionreview.md` and record the visible model/runtime model if exposed. If exact runtime is not exposed, state that limitation.

For audio review, do not overstate Claude Code's capabilities when it only read cue sheets, waveform, spectrogram, ffprobe, and loudness logs. Label it as evidence-based audio review rather than native playback unless the tool actually played/analyzed audio directly. Pair Claude Code's comments with local `volumedetect`/`ebur128` or equivalent loudness checks before reporting audio readiness.

## Verification checklist before reporting success

- Compile/check changed renderer/test files.
- Run focused tests; if pytest is unavailable in the venv, use `python -m unittest` for unittest-style tests rather than recording pytest absence as a durable problem.
- Run/generate the fixture again after any renderer patch before doing visual QA; contact sheets can otherwise reflect the previous render.
- Run optional upload-free OSS QA when available, especially scene/static and opening-distinctness probes, e.g. `python tools/oss_media_qa.py <mp4> --out-dir handoff/oss_media_qa/<packet> --probe scene-static` and `--probe opening-distinctness --opening-seconds 4`.
- Run project validate.
- Confirm `.agent.lock` is clear.
- Confirm active Storytime config remains absent.
- Update `handoff/accepted_changes.md`, `handoff/active_strategy_queue.md`, and the lane decision log.

## v2B → v2C internal-improvement pattern

When a read-only Claude Code review returns a verdict like `CONTINUE_INTERNAL_MAKE_V2C`, keep the next rung narrow: exactly one upload-free internal sample plus tests and a handoff record. Do not treat the verdict as activation/canary approval.

Useful v2C fixes from the Storytime.exe meme-native lane:

- Seed cast continuity early (for example a small CAT indicator in beat 1) if later characters appear abruptly.
- Make the final prop larger and cleaner, then add an explicit vote/comment-bait card (`WHO BONKED IT?`, buttons, `COMMENT YOUR VERDICT`) inside the internal sample rather than relying on a small receipt-only punchline.
- Keep captions short enough for mobile contact-sheet readability; expect bottom captions to wrap if close to the visual-safe limit.
- If the shared validator only allows the existing role set, do not invent new terminal roles unless you also update the class validator intentionally. Combine the final vote/comment card into an allowed `drop_punchline` beat and record the compromise.
- In renderer helpers, check whether `local` is normalized 0..1 or seconds before adding time gates. For the v2C final beat, using a seconds threshold against normalized `local` kept the vote card from appearing; use a fractional threshold (for example `local < 0.67`) or compute elapsed seconds explicitly.
- After patching renderer timing/roles, rerun focused unittest, regenerate the fixture, rerun OSS QA, and re-open the updated contact sheet visually.

## Reference/material library pattern

When the user wants to gather Storytime.exe references or candidate assets, create or use a quarantine-first library rather than mixing references into active renderer/assets paths. Keep it under handoff unless/until a separate manifest/license gate promotes assets.

Recommended shape:

- `handoff/storytime_exe_reference_library/README.md` — boundary, folder roles, risk labels.
- `reference_submission_template.md` — one copy per URL/file/asset pack. A reusable starter lives at `templates/storytime-reference-submission-template.md`.
- `index.md` — stable IDs, risk label, review state.
- `00_inbox/` — new user submissions.
- `01_reference_urls/` — URL-only style/timing references.
- `02_user_owned_examples/` — user-owned local examples for read-only analysis.
- `03_candidate_licensed_assets/` — quarantined purchased/licensed packs before approval.
- `04_license_notes/` — license text/PDF paths and redacted purchase/use summaries.
- `05_review_packets/` — Hermes/Claude/Codex read-only reviews and decision artifacts.
- `06_approved_for_generation/` — empty by default; only populated after explicit manifest/license validation.

Use risk labels in submissions/reviews:

- `GREEN_PRODUCTION_CANDIDATE` — likely usable after manifest validation.
- `YELLOW_INTERNAL_REFERENCE_ONLY` — useful for style/timing, not literal reuse.
- `RED_DO_NOT_REUSE` — competitor/IP/watermark/unclear/high-risk; do not copy.
- `UNKNOWN_NEEDS_REVIEW` — insufficient source/license info.

For user-provided URLs, treat them as structural references only: learn hard-cut timing, first-second hooks, caption hierarchy, phone readability, character expression systems, final payoff/comment-card design, and meme-native SFX timing language. Do not download or reuse competitor frames/audio/SFX as production assets. For candidate licensed packs, require commercial YouTube, editing/compositing, repeated automated-render permission, attribution/Content ID notes, and a manifest gate before promotion.

## YouTube Agent pre-upload MP4 review gate

For `youtube_agent`, do not rely on post-upload observation to catch obvious subtitle/voice sync issues. Before any exact artifact is privately uploaded, scheduled-private, scheduled-public, published, or promoted as a channel canary, run a pre-upload MP4 review via Claude Code or another MP4/contact-sheet-capable reviewer.

Same-session hardening rule: when a recurring artifact bug is root-caused, especially subtitle/voice drift, do not stop at handoff notes or one-off rerenders. Solidify the fix into the relevant project scripts/gates in the same session unless the user explicitly defers it. For `redditstories`/`redditscary` English channels, mainline renders must use word-timed subtitle timing and upload/schedule gates must fail closed when metadata lacks passing subtitle alignment evidence.

Minimum pre-upload review packet:

- exact local MP4 path and intended channel/destination;
- intended privacy/schedule mode;
- ffprobe JSON;
- 1fps/2fps contact sheet and opening 3-5s contact sheet if available;
- waveform/loudness evidence;
- subtitle/timing transcript or render timing metadata if available;
- local render/QA report;
- for narrated/subtitled Shorts, an independent subtitle/audio alignment report comparing SRT cue spans to spoken-word timing. Do not let generic render QA substitute for this unless it actually performs that comparison.

Reviewer must explicitly check:

- voice timing vs subtitle timing using alignment evidence, not just still contact sheets;
- early/late/stuck/missing subtitles;
- first 3-5s audio/subtitle readability;
- final CTA/subtitle timing;
- obvious visual/audio/readability blockers;
- if the artifact is a repaired cover-and-reburn over an existing master, whether old subtitle ghosting, band seams, or opening-frame artifacts make it unsuitable for anything beyond private replacement review.

Use verdicts: `APPROVE_FOR_UPLOAD`, `REVISE_BEFORE_UPLOAD`, `BLOCK_UPLOAD`. Only `APPROVE_FOR_UPLOAD` can proceed to the existing exact-artifact upload/schedule gates. If review is inconclusive, rerun with better evidence rather than treating uncertainty as approval. If the review caveat says "private replacement only," keep the upload private and do not schedule/public-promote without a separate user-approved review.

## Reporting language

Report the result as an internal baseline, not as activation approval. Recommended wording:

- `STRONG_INTERNAL_SAMPLE / internal-only, not activation-cleared`
- `CONTINUE_INTERNAL / NOT_ACTIVATION_READY`

List blockers separately: `production_safe=false`, internal-only synthetic audio, source/anecdote attestation, mobile contrast/legibility pass, and canary/A-B comparison if relevant.
