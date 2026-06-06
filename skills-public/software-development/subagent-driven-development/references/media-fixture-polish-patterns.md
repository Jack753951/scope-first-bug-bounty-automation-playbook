> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Media Fixture Polish Patterns

Use this reference when an upload-free media fixture already renders but artifact review finds readability, hook specificity, or motion-evidence issues.

## Pattern: TDD the visual polish

1. Add a focused regression test for the exact artifact contract before editing renderer code.
   - Caption/safe-area examples: exported fixture metadata has a bounded caption length; a `validate_*_safe_area(...)` helper returns `[]`; final CTA copy equals the approved shorter text.
   - Scenario-hook examples: first card includes concrete `scenario` metadata; hook headline is not generic; mechanism cards include expected `motion_cues`.
2. Run the focused test and confirm RED for the expected reason.
   - Missing helper/function is a valid RED when adding a new guard.
   - Missing metadata is a valid RED for a fixture-contract improvement.
3. Implement the smallest renderer/metadata change to satisfy the contract.
4. Regenerate the upload-free fixture artifacts.
5. Run focused tests, compile checks, JSON parse checks, project validate, and lock-file check.
6. Generate a visual QA contact strip from sampled MP4 frames and inspect it for clipping/overflow/readability.
7. If visual QA finds layout clipping, fix before finalizing, regenerate, and re-check visually.

## Safe-area linter heuristic

A lightweight dependency-free linter is useful before FFmpeg render:

- Mirror the renderer's caption x-position, font size, and wrap width.
- Enforce a conservative per-caption character cap for Shorts-safe CTA/footer text.
- Estimate line width as `len(line) * font_size * 0.58` against `frame_width - margin`.
- Wire the linter into fixture generation so unsafe captions fail before MP4 output.
- Keep the linter aligned with actual renderer font-size/wrap changes; if the renderer changes, update both together.

## Visual QA strip recipe

Use FFmpeg to tile representative frames into a small contact strip for fast inspection:

```bash
mkdir -p handoff/visual_qa
ffmpeg -y -hide_banner -loglevel error \
  -i handoff/<fixture>/<video>.mp4 \
  -vf "select='eq(n,25)+eq(n,125)+eq(n,225)+eq(n,325)+eq(n,425)',scale=270:-1,tile=5x1" \
  -frames:v 1 handoff/visual_qa/<fixture>_strip.jpg
```

Adapt frame numbers and tile dimensions to duration/FPS. Inspect for:

- first-frame hook clarity
- caption clipping/overflow
- footer clipping
- broken images/black frames
- mechanism/diagram labels readable enough for internal review
- final CTA visible and safe

## Common fixes

- Shorten final CTA/footer copy rather than shrinking everything first.
- Reduce overlay font size and wrap width together.
- Add concrete scenario metadata/headlines when a psychology/educational card feels generic.
- Add deterministic motion evidence (pulses, side rails, sequential node highlights) that avoids covering text.
- If footer text is clipped in a tiled visual QA strip, shorten it and regenerate the artifact before recording PASS.

## Safety boundaries

For upload-free fixtures in publishing-sensitive repos, preserve these boundaries unless explicitly approved:

- no upload/publication
- no scheduler changes
- no OAuth/token/client-secret edits
- no default privacy changes
- no active-channel activation
- no runtime user-data deletion
