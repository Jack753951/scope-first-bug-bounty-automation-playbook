> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Video Channel Scaffold Safety Gates

Use this reference when adding a new channel/content engine to a Shorts/video automation repo before it is safe to activate uploads.

## Proposal-only scaffold pattern

- Keep the new channel outside active discovery paths, e.g. `channels_disabled/<channel>.json` or `handoff/<channel>.proposal.json`.
- Do not add `channels/<channel>.json` until explicit user approval and a separate activation gate.
- Add machine-readable warnings in the disabled config, such as `enabled: false`, `status: PROPOSAL_ONLY_DO_NOT_LOAD_AS_ACTIVE_CHANNEL`, and an `activation_warning` explaining whether the loader honors `enabled`.
- If the active loader discovers every `channels/*.json`, add a regression test asserting the active file is absent.

## Safe scaffold contents

Allowed before activation:

- Pure schema/helper modules with no network, no filesystem writes, no OAuth imports, no upload/scheduler imports.
- Data-only pilot packs under `handoff/` or another non-runtime path: JSON/YAML specs for 3-5 draft concepts that validate the content schema but do not trigger generation/render/upload.
- Upload-free validation/report runners that import only the pure schema helper, validate the pilot pack, assert disabled-only channel state, and write a markdown report under `handoff/`.
- Deterministic local preview layers under `handoff/` (for example HTML + JSON storyboard previews plus an index/manifest) that make hook, pacing, captions, character mapping, visual beats, and SFX cues inspectable before any MP4 render or upload path exists. For meme-theater formats, include semantic caption cards plus manifest-backed `background_asset` and `prop_assets` in the preview plan so scene staging is reviewable, not just narration text.
- Upload-free timing/contact-sheet layers under `handoff/` after the HTML/JSON storyboard rung and before production render. For formats whose quality depends on fast cuts, generate per-spec HTML/JSON sheets with fixed review frames (for example hook/setup/escalation/climax/payoff), active cast, caption card, background, props, visual beats, SFX cues, and emotion beats. Treat these as review gates only; they must not import production `agent`, `pipeline`, `youtube_api`, `database`, scheduler, OAuth, token, or runtime `data/` modules.
- Upload-free local MP4 fixture layers under `handoff/` after the HTML/JSON preview rung. Keep these as short deterministic review artifacts (for example vertical 540x960 fixtures plus ffprobe JSON and a manifest), not production renderer outputs. They may use FFmpeg but must not import production `agent`, `pipeline`, `youtube_api`, `database`, scheduler, OAuth, token, or runtime `data/` modules.
- Internal user-viewing gates after the local fixture rung. These should aggregate the prior evidence into a machine-readable PASS/FAIL report before telling the user a sample is ready to view. For meme/story formats, include checks for English joke localization, source/template metadata, sticker/background/prop visual references, SFX manifest, non-silent audio mix, waveform or ffprobe evidence, visual contact sheets, disabled-only state, and forbidden upload/OAuth/scheduler/runtime imports. See `references/video-internal-user-viewing-gates.md` for the detailed acceptance checklist and wording.
- Unit tests for schema validation, pilot-pack validity, preview/report output, MP4/ffprobe fixture output when FFmpeg is available, user-viewing gate output, forbidden imports, privacy constants, and active-channel tripwires.
- Asset placeholder directories with README files documenting legal sourcing.
- An isolated asset profile manifest for non-stock formats (for example `assets/<channel>/licenses/manifest.json`) plus a pure validator that ensures assets stay under the channel asset tree, carry source/license metadata, and placeholders cannot be marked production-ready.
- Explicit engine metadata on disabled configs when the new format differs from existing channels, e.g. `channel_type`, `script_engine`, `asset_profile`, `render_engine`, and `activation_state`.
- A fail-closed route in the production entry point for experimental engines: if an experimental config is accidentally moved into active discovery, raise before normal script generation, stock downloads, rendering, upload, OAuth, scheduler, or runtime data writes.
- Handoff docs that state what changed, what stayed out of scope, and the next gated layer.

Favor a modular ladder over one-off scripts: `data-only spec -> validator/report -> local preview/storyboard -> local MP4 fixture -> private reviewed render -> tiny public canary`. Each rung should be deterministic, testable, and reversible, with upload/OAuth/scheduler activation kept as separate explicit gates.

Avoid before activation:

- Upload, scheduling, OAuth/token-path, or publish/privacy changes.
- Moving disabled/proposal config into active channel discovery.
- Downloading competitor footage, meme images, ripped SFX, screenshots, or assets with unclear licensing.
- Editing runtime data, generated videos, token files, or DBs.

## Validation checklist

Run or request equivalent local checks:

1. Parse all active channel JSON files plus the disabled/proposal JSON and any pilot-spec JSON/YAML pack.
2. Compile changed Python modules and tests.
3. Run focused unit tests and any existing safety/render tests.
4. If a preview layer exists, run its generator and assert the index, manifest, per-item HTML/JSON previews, and PASS report are produced in non-runtime paths. For sticker/meme formats, inspect at least one rendered HTML/frame visually and verify that background assets, role stickers, props, and caption cards are actually visible/readable with no obvious clipping or broken layout. When a local `file://` preview looks blank or DOM tooling reports an empty document despite the file containing HTML, serve the repo via a temporary localhost static server (for example `python -m http.server <port> --bind 127.0.0.1`) and inspect the `http://127.0.0.1:<port>/...` URL instead; stop the server after QA.
5. If a timing/contact-sheet layer exists, run its generator and assert the index, manifest, per-item HTML/JSON sheets, and PASS report are produced in non-runtime paths. Visually inspect at least one sheet and confirm all review frames are visible, captions are readable, backgrounds/role stickers/props render, and visual/SFX/emotion badges are not clipped or missing.
6. If an MP4 fixture layer exists, run its generator and assert MP4 files, ffprobe JSON, manifest, and PASS report are produced only in non-runtime paths such as `handoff/`. Probe geometry/duration rather than trusting file existence alone.
7. If a user-viewing gate exists, run it directly and require PASS before reporting that an internal sample is ready for user review. Verify the gate counts every expected evidence artifact (metadata/template/source fit, visual references, SFX manifest, non-silent audio, waveform/ffprobe/contact sheet, disabled-only and forbidden-import safety checks) and writes both JSON and markdown reports.
8. Add/keep tests that forbid accidental imports of upload, scheduler, OAuth, production agent, pipeline, database, or YouTube API modules from proposal/preview/fixture/gate helpers.
7. Run project validation command if present.
8. Confirm no active `channels/<new_channel>.json` exists.
9. Confirm privacy/safety constants remain unchanged.
10. Confirm `.agent.lock` or similar run lock is not left behind.
11. If a worker says validation is blocked by its local Python/venv, rerun the same checks directly in Hermes/project shell before recording final status; update handoff notes from BLOCKED to PASS when the authoritative rerun passes.
12. Update review and accepted-change handoff files.

## FFmpeg fixture pitfalls

- On Windows/MSYS, FFmpeg `drawtext` can crash or fail if Fontconfig cannot find a default font. For deterministic local fixtures, pass an explicit font file such as `C\\:/Windows/Fonts/arial.ttf` (escape the colon for FFmpeg filter syntax) rather than relying on font discovery.
- FFmpeg `drawtext=textfile=...` does **not** word-wrap. If a long line is centered with `x=(w-text_w)/2`, `text_w` can exceed the canvas and produce negative x coordinates, clipping both sides of the text. Pre-wrap text before passing it to `drawtext`, use a conservative per-line budget, reduce font size for fixtures, and prefer fixed safe margins for fixture cards.
- Do not trust MP4 existence or ffprobe geometry alone for visual layout. Extract at least one representative frame (for example `ffmpeg -ss 00:00:01 -i <fixture>.mp4 -frames:v 1 <frame>.png`) and inspect that text is not clipped before telling the user the fixture is reviewable.
- If a fixture generator supports temp output dirs in tests, do not assume text/image inputs are under the repo root. Path helpers should use repo-relative paths when possible and fall back to escaped absolute POSIX-style paths for temp directories.
- Keep fixture artifacts intentionally small and review-oriented; they are gates for layout/pacing inspection, not a substitute for the production renderer QA path.

## OAuth guidance

New channels do not need YouTube OAuth during proposal-only or draft-only scaffolding. OAuth/token setup is only needed when the project will call YouTube APIs for upload, scheduled publishing, channel reads, analytics, or management actions. Defer OAuth until the activation/upload gate, and keep tokens separated per channel/account when the repo supports that.

## Agent review pattern

For high-risk scaffolds, use a two-pass review:

- Codex implements or audits the engineering scaffold.
- Claude Code reviews safety boundaries and schema gaps, especially when conserving GPT/OpenAI usage is useful.
- If Claude Code print mode repeatedly hits max-turn limits on a large diff, use a narrower piped diff with more turns or a read-only review subagent; capture the review verdict without treating the CLI limit as a project blocker.

Ask reviewers to distinguish blockers from non-blocking notes and explicitly answer whether OAuth/upload/scheduler behavior changed.
