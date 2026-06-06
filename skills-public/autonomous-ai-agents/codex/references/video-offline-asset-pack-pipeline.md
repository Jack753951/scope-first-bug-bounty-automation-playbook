> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Video Offline Asset Pack Pipeline

Use this when a Shorts/video automation project needs meme/sticker/prop/background assets but should not connect to external asset sites or reuse competitor media yet.

## Pattern

1. Keep the experiment upload-free and outside active channel discovery.
   - Prefer `channels_disabled/`, `handoff/`, or fixture-only preview scripts.
   - Do not create or enable `channels/<experiment>.json` unless the user explicitly activates it.
2. Generate deterministic, project-owned placeholder assets locally.
   - SVG is a good first pass: small, diffable, inspectable, and safe for HTML previews.
   - Put generated candidates under an isolated path such as `assets/<experiment>/generated/{characters,backgrounds,props}/`.
3. Maintain a machine-readable manifest.
   - Record `source_type: project_generated` (or equivalent), license/source notes, generator version/date, and review status.
   - Mark candidates as not production-ready until visually reviewed: e.g. `ready_for_production: false`.
4. Wire previews to real local assets with graceful fallback.
   - HTML/storyboard previews should prefer generated SVG stickers/backgrounds/props.
   - Keep emoji/text fallback only for missing assets, not as the primary preview path.
   - For meme-theater/storytime formats, promote the preview plan beyond `cast + narration`: include `caption_cards`, `background_asset`, and `prop_assets` so scene staging is inspectable before any production renderer exists.
5. Improve caption pacing at the preview rung.
   - Avoid fixed N-word chunking as the final preview behavior; it hides pacing defects.
   - Split narration on sentence boundaries and semantic connectors such as `when`, `then`, `while`, `and`, `like`, `but`, `because` to approximate setup → interruption → escalation → reaction → payoff.
   - Keep hard word/character budgets only as a fallback for long fragments.
6. Add tests for safety boundaries, not just file existence.
   - Generator writes expected SVG files under the isolated asset root.
   - Manifest records local/generated provenance and production-readiness state.
   - Preview output references generated characters, backgrounds, and props.
   - Preview-plan tests assert representative semantic caption boundaries so future changes do not regress to mechanical chunks.
   - Active channel discovery is unchanged; disabled experiment remains disabled.
7. Validate without upload side effects.
   - Run focused tests, compile checks, JSON parse checks, project validate/status commands, and a visual preview check when possible.
   - For fast meme-theater/video timing, prefer a contact sheet dense enough to catch micro-beat issues (for a ~12s Short, 9 frames at 1.5s intervals is more useful than a coarse 5-frame sheet). Visually verify hook readability, role stickers, props/evidence objects, SFX/emotion badges, and that text/notes do not cover the main subject.
   - For contact-sheet/video QA, check concrete story evidence rather than only layout: e.g. role UI, sticker identity, prop actions, chat/evidence text, emotion badges, climax pose, final CTA card, and whether any frame is cropped/overlapped/broken.
   - If a creative/third-party review returns `REVISE`, keep the work in the offline rung and patch the fixture/spec/asset mapping first; do not treat an implemented preview as canary-ready just because tests pass. If the reviewer says it is still user-watchable as a local experiment, preserve that distinction: internal viewing is allowed, publication/canary is not.
   - Confirm no lock files, OAuth/token changes, scheduler changes, or default privacy changes.
8. Run an independent code/safety rereview before calling the rung complete.
   - Ask the reviewer to separate blocking defects from non-blocking suggestions and to inspect upload/OAuth/scheduler/runtime-data boundaries, disabled-only state, default privacy, path guards, graceful media-tool fallback, and test coverage.
   - Apply low-risk non-blocking corrections that clarify safety contracts (for example report wording that overstates a path guard), then rerun the focused tests/generator/compile check at minimum.
   - Record the review artifact under `handoff/` and summarize it in the engineering review log.
9. Record handoff notes.
   - Update engineering review / accepted-change logs and any project notes used by the multi-agent workflow.

## Pitfalls

- Do not let "original placeholder" become implied production clearance. Keep explicit review flags until legal/quality review passes.
- Do not scrape competitor stickers/frames just to make the preview look better. Improve local generation or ask for a licensed/AI provider gate.
- Do not place experimental assets/configs where normal automation will upload or schedule them.
- Do not rely on transcript-only QA for meme-theater formats; inspect rendered HTML/frames visually because performance value is in casting, props, labels, and rhythm.
- Do not stop visual validation at “file exists.” Open the HTML/contact sheet/frame and verify that backgrounds load, role stickers load, props are visible, caption cards are readable, and no obvious clipping or broken layout appears.
- Keep generated reports aligned with actual guard semantics. If code allows custom outputs anywhere under `handoff/`, don't write a report claiming every output is restricted to one fixture subdirectory; either tighten the guard or clarify the report.
- If a media renderer gracefully handles a missing tool (e.g. FFmpeg not installed), consider also documenting or testing behavior when the tool exists but render execution fails; at minimum don't confuse missing-tool fallback with full render-failure recovery.
- If manifest entries are sorted or regenerated, tests should find placeholder/project-generated records by `source_type` or `id` instead of assuming a fixed list index.
