> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Session memory/skill hygiene review

Use this when the user asks to review the conversation and update memory and skills, especially after a context compaction or a long working session.

## Durable pattern

1. Separate the two axes before writing anything:
   - Memory = who the user is, durable preferences, expectations, stable routing/safety signposts.
   - Skills = how to do a class of task better next time.
2. Treat explicit user corrections about style, tone, format, legibility, verbosity, approach, or frustration as both:
   - a user-preference memory signal when durable; and
   - a skill signal for the workflow that produced the correction.
3. Prefer updating an already-loaded skill first. If the visible conversation was compacted and loaded-skill evidence is incomplete, use the latest visible task/context plus known project rules to choose the closest existing umbrella rather than creating a narrow session skill.
4. Prefer class-level skills with concise session-specific support files under `references/` over one-off narrow skills named after today's artifact, PR, error string, target, or phase.
5. Treat "be active" hygiene requests as a bias toward a small useful patch when there is any real reusable lesson; a no-op is appropriate only after checking for preference, workflow, correction, or tool-use lessons.
6. Respect tool limits in the hygiene prompt. If the user says only memory/skill tools are allowed, do not call file, terminal, search, browser, or project tools just to gather extra context.
7. Do not store project progress, run results, PRs, commits, dated artifacts, target details, scan output, secrets, or transient setup failures in global memory.
8. If memory is near capacity, compact or replace an overlapping existing entry rather than forcing a new long entry.
9. If a current phase/status fact matters, route it to repo handoff or active queue, not global memory. Save only the durable preference for how status should be answered.
10. If genuinely no durable preference or reusable procedure emerged, say `Nothing to save.`; do not invent a skill update.

## Skill update preference order

1. Patch a currently-loaded skill that governed the session.
2. Patch an existing umbrella skill.
3. Add a focused support file under an umbrella and add a one-line pointer in `SKILL.md`.
4. Create a new class-level umbrella only if no existing umbrella fits.

## Verification

- Memory entries are declarative, compact, and unlikely to go stale within a week.
- Skill changes describe reusable workflow or judgment, not a session log.
- Project-specific details stayed in project files, handoff, Obsidian, or session history.
- The final response says what was saved/updated, and mentions if overlapping skills may later be consolidated.