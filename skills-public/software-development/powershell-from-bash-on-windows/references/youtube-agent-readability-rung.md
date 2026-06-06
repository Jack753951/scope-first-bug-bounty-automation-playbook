> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# YouTube Agent upload-free readability rung pattern

Use this when a generated `youtubestrict/youtube_agent` draft passes render QA but Claude/Cowork or visual QA says it is still `REVISE_INTERNAL` due overlay readability, hook text, or reviewability issues.

## Trigger

- `run_agent.ps1 draft ... --draft-script-engine ...` produces a local draft and metadata, but the frame strip shows small card text, weak contrast, subtitle/card overlap, or hook punctuation loss.
- The next step must remain upload-free/internal-only and must not switch `channels/*.json` active engines.

## TDD before render

Add focused RED tests before rendering another video:

1. Hook text preservation: if the scripted hook includes meaningful punctuation, test the overlay cleaning path separately from generic metadata cleaning. Example: `Mom texts: are you mad?` should remain `Mom texts: are you mad?`, while the FFmpeg drawtext escape layer should emit `Mom texts\: are you mad?`.
2. Card readability: assert exact filter properties that reviewers care about, such as darker scrim opacity, stronger border/outline, larger mechanism node font size, and larger caption font size.
3. Do not test by visually inspecting a freshly rendered MP4 first; render after GREEN, then generate a frame strip/contact sheet for QA.

Useful test targets from the 2026-05-18 Psychology rung:

- `pipeline.clean_hook_overlay_text(...)` preserves safe top-hook punctuation before `escape_drawtext_text(...)` handles FFmpeg escaping.
- `psychology_visuals.append_psychology_insight_filters(...)` emits a strong card scrim like `0x10151C@0.94`, readable mechanism node labels around `fontsize=40`, and mechanism captions around `fontsize=36`.

## Upload-free render + visual QA loop

From Git-Bash/MSYS, run the PowerShell wrapper with POSIX-style script path from the repository root:

```bash
powershell -NoProfile -ExecutionPolicy Bypass -File './run_agent.ps1' draft --channel psychology --topic 'boundary pause relationship text' --draft-script-engine psychology_insight_v1 1
```

Then create a review strip, e.g.:

```bash
ffmpeg -y -i data/psychology/output/<job>/final_short.mp4 -vf "fps=1/3,scale=270:-1,tile=3x3" -frames:v 1 -update 1 handoff/visual_qa/<job>_strip.jpg
```

Visual QA should explicitly check:

- top hook punctuation/readability,
- insight card and mechanism-flow readability,
- black screen/broken image,
- subtitle crop/overlap,
- whether the artifact is only internal-review-ready or actually production/canary-ready.

A PASS for internal review is not a publication approval. If split-screen/comment-prompt microtext remains small, keep the next rung local-only.

## Handoff notes to record

Record in `handoff/accepted_changes.md`, `handoff/codex_review.md`, and `handoff/codex_task.md`:

- RED failure observed,
- GREEN implementation summary,
- latest draft path,
- metadata path,
- frame strip path,
- render QA duration/verdict,
- visual QA verdict and caveats,
- safety statement: no upload/publication, no scheduler/OAuth/token/client-secret/default-privacy changes, no destination ID filling, no active engine switch, no runtime data deletion.

## Pitfalls

- Generic sanitizers may remove punctuation that is semantically useful in overlays. Add a hook-specific cleaning function rather than weakening the global sanitizer used for metadata/provider safety.
- `escape_drawtext_text(...)` is the place to FFmpeg-escape colons; do not remove the colon earlier and then try to reconstruct it in the rendered filter.
- Static render QA only proves the video exists and subtitles are present; it does not prove overlays are readable at phone-scroll speed.
