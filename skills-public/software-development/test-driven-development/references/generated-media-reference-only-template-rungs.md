> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Generated-media reference-only template rungs

Use this when the user provides downloaded competitor/public examples (for example yt-dlp local videos) and explicitly wants to learn only architecture/template patterns, not reuse assets.

## Goal

Turn reference examples into an internal structural template while preserving a hard boundary between abstract lessons and production assets.

## TDD pattern

1. Write RED tests for the reference policy before any renderer/spec change:
   - examples are `YELLOW_INTERNAL_REFERENCE_ONLY` or equivalent;
   - generated output is `production_ready=false`;
   - `reference_files_policy` says not to ingest downloaded/reference files;
   - active channel config remains absent/unchanged;
   - no upload/OAuth/scheduler/default-privacy side effects.
2. Write RED tests for abstract reusable structure:
   - duration band (for Shorts, usually 20-28s if the reference pattern suggests it);
   - 4-5 hard-cut beats;
   - locked title band and per-beat sub-caption;
   - persona staircase (setup -> respondents/escalation -> pause/authority -> payoff);
   - compact comedic pause/gutter;
   - final-third payoff/vote/comment card.
3. Write RED tests for forbidden literal reuse:
   - no copied frames;
   - no copied captions/text/translations/paraphrases;
   - no copied audio/music/voice/SFX/stingers;
   - no copied character/IP/mascot designs;
   - no watermark/editor-branding reuse;
   - no known surface terms from the reference examples appear in generated specs/manifests.
4. Implement the smallest internal sample/spec generator using original placeholder drawings and synthetic cue names/timings compatible with existing validators.
5. Generate upload-free output only after GREEN.
6. Run local media QA and visual/contact-sheet review. Treat render QA PASS as insufficient unless the visual review confirms the structure is originalized and readable.
7. Write a decision artifact that labels the rung as internal/template-only and names the next safe promotion gate: read-only review or original/licensed replacement asset manifest.

## Validation checklist

- Focused tests pass.
- Compile/syntax checks pass.
- Project validate passes.
- Generated JSON manifests parse.
- Provenance manifest records: local reference only, production_ready=false, channel_activation=false, reference files not ingested.
- Active channel config was not created.
- `.agent.lock` is clear.
- Contact sheet shows distinct beats and a readable final card.

## Pitfalls

- Do not label yt-dlp/downloaded examples as licensed production candidates merely because they are useful or user-provided. If the user clarifies they are downloads for reference, downgrade them to internal-reference-only immediately.
- Do not grep the source code for forbidden surface terms if the test itself stores those terms as deny-list literals; check generated specs/manifests instead.
- Existing schema validators may allow only specific `source_type`, role, motion, icon, and SFX enums. Keep the new rung within the current schema unless the task is explicitly to broaden the schema.
- A good template sample can still be non-production: placeholder characters and synthetic cue labels are acceptable for structure validation but must be replaced by owned/licensed assets before any canary/upload.