> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Content Review Purpose Correction Routing

Use this pattern when the user corrects the purpose or success criterion of creative/content review, especially when an external reviewer such as Claude Code is being asked to judge visual, audio, or channel fit.

## Trigger

The user says a review should be centered on a different human-facing outcome, for example:

- "the channel should target what humans find funny / interesting / attention-grabbing"
- "vision review should use this as the principle"
- "don't just check technical correctness"
- "review should judge whether viewers would keep watching"

## Routing

1. Treat the correction as a project workflow/review-purpose rule, not just a chat preference.
2. Update the relevant repo handoff or active routing file so future workers see it before opening dated artifacts.
3. Add or update a project-local strategy/Obsidian note when the correction affects long-term creative reasoning.
4. Save only a compact global-memory signpost if it changes future cross-session behavior; keep exact gates, verdict vocabulary, artifact paths, and channel-specific rationale project-local.
5. If the correction generalizes beyond the project, update the class-level skill with this routing pattern rather than creating a narrow one-session skill.

## Review prompt implications

Future creative/vision review prompts should distinguish:

- technical readiness: render quality, subtitle/audio alignment, mobile readability, provenance, safety gates;
- audience readiness: human fun, interest, curiosity, first-seconds retention, payoff clarity, shareability, and channel fit.

A technically correct artifact can still require revision if it is not entertaining, interesting, or attention-grabbing enough for the channel goal. Use verdicts that separate these dimensions when helpful, such as `REVISE_FOR_HUMAN_FUN` versus `REVISE_TECHNICAL_BLOCKERS`.

## Safety boundary

A review-purpose correction is not runtime approval. Do not infer permission to generate, upload, schedule, publish, alter OAuth/token files, change channel configs, change default privacy, or promote assets into production.

## Verification

- Repo handoff/routing note contains the new review purpose.
- Project strategy/Obsidian note records the long-term rationale if applicable.
- Global memory, if updated, is compact and declarative.
- The update explicitly says no activation/runtime authority was granted unless the user separately approved it.
