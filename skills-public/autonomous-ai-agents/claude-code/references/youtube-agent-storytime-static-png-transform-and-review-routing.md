> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# YouTube Agent — Storytime.exe static PNG transform + Claude Code role-review correction

Use this when working on Storytime.exe / cat-meme-theater internal samples, especially after reference scouting of Chinese 猫meme小剧场 style channels.

## Session-derived correction

The user corrected two workflow/design drifts:

1. Do not make the user remind Hermes to use role-separated Claude Code review. Non-trivial Storytime visual/creative work should default to Claude Code review/implementation rungs where useful, with Hermes as verifier/synthesis.
2. The reference-template cats appear to be roughly 90% static PNG/cutout actors. The apparent motion is mostly renderer/editor transforms, not true GIF character animation.

Treat both as class-level workflow lessons for future Storytime work.

## Required review route for non-trivial Storytime visual/creative work

For any non-trivial Storytime renderer/sample/polish rung:

1. Hermes may generate/verify the local artifact and extract evidence.
2. Run a Claude Code creative/channel-fit reviewer:
   - Role: reference fit, meme-theater feel, premise/proof/payoff/comment arc, channel identity, whether it is drifting into a rigid template.
   - Use read-only print mode where possible: `claude -p "$(cat <prompt>)" --allowedTools 'Read' --output-format json --max-turns 5-10`.
3. Run a separate Claude Code technical/visual-readability reviewer:
   - Role: safe area, mobile text size, composition/crowding, asset matte/halo quality, output specs, evidence gaps.
4. Report route/tool, visible model/runtime, raw JSON artifact paths, session IDs, exposed usage/cost if available, each reviewer verdict, and Hermes synthesis.
5. If implementation is more than a tiny deterministic patch, prefer a bounded Claude Code implementation rung, then Hermes reruns local validation.

Do not stop at Hermes quick visual QA for this class of task.

## Human-fun verdict discipline for Storytime reviews

The primary Storytime success criterion is not technical correctness; it is whether a real Shorts viewer would stop, understand the premise, feel the reaction/payoff, and consider it funny/interesting enough to keep watching. For Storytime Claude Code review prompts, explicitly ask both reviewers to judge:

- first 1-3 seconds: scroll-stopping curiosity gap, not just a descriptive banner or diagram label;
- setup/escalation/proof/payoff: whether the joke is shown in the frame, not only named by captions;
- reaction readability: face/body/state changes must be large enough to read at phone size, not tiny glyph swaps on otherwise identical cutouts;
- timing evidence: if audio is clicks-only or silent, say comedic timing cannot be honestly judged and keep the verdict internal-revise;
- authority/proof cues: silhouettes, phone receipts, chat lines, and props should be visually self-evident, not thin edge artifacts or labels doing all the work;
- final verdict/comment prompt: the cast should react as part of the payoff, not merely stand near `COMMENT VERDICT` text.

Use verdicts such as `PROMOTE_INTERNAL_DIRECTION`, `REVISE_FOR_HUMAN_FUN`, `REVISE_TECHNICAL_BLOCKERS`, and `REJECT_DIRECTION`. A renderer can pass tests and still be `REVISE_FOR_HUMAN_FUN` if it is not entertaining or retention-worthy. Do not use upload/canary approval language for internal sample rungs.

Session example: v2J reaction-frame improved v2I by adding visible phone proof (`it was me lol`), reaction states, authority recoil, and final `GUILTY?` payoff, but both human-fun and technical Claude Code reviews still returned `REVISE_FOR_HUMAN_FUN` because the opening remained diagram-like, expression states were tiny glyph overlays, the authority silhouette was too thin, and clicks-only audio prevented timing review. The next rung pattern was larger drawn expression variants plus synthetic VO/quiet bed/stronger stings and a clearer head-and-shoulders authority cue.

User-corrected pitfall: do not confuse "asset-backed" with generated placeholders or blurred reference mosaics. In the v2K/v2L sequence, the user corrected Hermes because v2K still did not use the previously downloaded meme GIF/WebP and SFX files. For local-only human-fun review, first check the Storytime reference library/quarantine catalogs (and user Downloads-derived catalogs) and use cataloged meme visuals, SFX, BGM, and VO placeholders as primary sample materials. Generated SVG/SFX placeholders are acceptable for renderer isolation only, not as the default creative iteration. Keep audit/license footers and reference mosaics out of the primary MP4 unless explicitly requested; put them in sidecars/contact sheets.

## Static PNG/cutout + transform model

Do not optimize Storytime primarily around Tenor GIF playback. The reference-mechanics model is:

- Static PNG/WebP cutout actor states are the base asset type.
- Motion comes from transform timelines:
  - scale / zoom punch-in,
  - translate / slide in-out,
  - shake / jitter,
  - rotate / tilt,
  - squash / overshoot,
  - hard-cut actor swaps,
  - entrance/exit timing.
- Render only the 1-2 actors needed for each beat; avoid a permanent reactor lineup unless the story calls for one.
- Split schema concepts:
  - `actors`: recurring story characters / identity anchors,
  - `actor_states`: static expression/pose cutouts,
  - `transforms`: timeline primitives and timing,
  - `effects`: one-shot GIF/video/full-panel accents for punchlines or proof reveals.
- Use Tenor/GIF assets as internal reference or rare effect panels, not as the production actor-system default.

Suggested next schema direction:

```json
{
  "actors": [{"id": "cat_a", "role": "suspect", "home_position": [270, 560]}],
  "actor_states": {"cat_a": {"shock": "assets/cat_a_shock.png", "guilty": "assets/cat_a_guilty.png"}},
  "beats": [{
    "start": 0.0,
    "end": 2.5,
    "actors_on_stage": [
      {"actor": "cat_a", "state": "shock", "transform": "zoom_punch_shake", "story_reason": "receipt reveal reaction"}
    ],
    "effects": []
  }]
}
```

## Tenor API caveat

Tenor API v2 docs currently state that as of Jan 2026 new API clients are no longer accepted and instructions are reference-only for new users. Any Tenor API downloader/helper should be marked legacy/existing-key-only. Without an existing key, do not make Tenor API the main acquisition plan.

For production-safe Storytime assets, prefer:

- self-made recurring PNG/WebP actor library,
- explicitly licensed commercial packs with automated YouTube/compositing permission,
- generated/project-owned transparent actor states after license/provenance review.

Tenor/local meme pixels remain internal-only unless separately cleared.

## Artifact/handoff expectations

Record these corrections in repo handoff files when they affect a rung:

- reference mechanics: static PNG/cutout + transform timeline,
- role-separated Claude Code reviews,
- raw Claude JSON and markdown review artifacts,
- Hermes synthesis with `CONTINUE_INTERNAL_REVISE` / `NOT_UPLOAD_READY` style boundary language when appropriate,
- accepted_changes entry with safety boundary unchanged.
