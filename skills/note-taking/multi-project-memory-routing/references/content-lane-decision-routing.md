> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Content-Lane Decision Routing Pattern

Use this when a user clarifies creative/channel direction and says to remember it, while also asking the agent to continue project work.

## Pattern

1. Separate durable preference from project state.
   - Durable preference: compact, reusable creative preference or safety principle that may help future sessions.
   - Project state: exact lane decision, dated artifact paths, validation results, generated samples, next gates.

2. Route the exact lane decision to repo-local truth first.
   - Add a named decision artifact in `handoff/` or the project's equivalent.
   - Update the rolling decision log / active strategy queue / accepted changes if the project has them.
   - Keep it append/prepend-only for shared handoff Markdown.

3. Use global Hermes memory only for a compact signpost.
   - Replace/compact an overlapping memory entry when memory is near capacity.
   - Do not store sample paths, run results, PRs, cron IDs, or dated validation logs globally.

4. Continue execution only inside the explicit lane.
   - If the lane is internal/reference-only, generate or review local artifacts only.
   - Do not infer approval for upload, publication, scheduler, OAuth, active channel config, destination, privacy, or production activation.
   - Write the safety boundary into the generated report and accepted-change entry.

5. Verify and report exact artifacts.
   - Run focused tests/QA appropriate to the artifact.
   - Confirm activation guards stayed closed.
   - Report exact local paths and the next safe action.

## Example shape

A user says a disabled media channel should preserve meme-native culture during internal tests. Route as:

- Repo decision artifact: internal reference lane vs future production-safe lane.
- Active queue: current status and blockers.
- Accepted changes: generated local-only sample and validation.
- Global memory: one compact preference/signpost such as `Project X content prefs: meme-native internal tests are valuable; public/canary still needs asset risk gate.`

Do not turn the dated sample or validation packet into global memory or a narrow one-session skill.
