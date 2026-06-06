> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Parking a Content Direction Without Changing the Main Phase

Use this when the user decides to shelve, pause, or "先擱置" a proposed project lane, content format, channel direction, or experiment idea after discussion.

## Routing rule

A parked direction is usually project-local state, not global Hermes memory and not a standalone skill.

Record it in the target repo's decision/handoff layer when future workers might otherwise reopen the idea or mistake it for active strategy. Keep the reusable lesson in this skill only.

## Procedure

1. Classify the user's statement as a boundary decision, not implementation approval.
   - Examples: "先擱置", "not now", "pause this direction", "let's shelve it".
2. Update the project-local accepted-change / decision log with a short entry:
   - what direction was parked,
   - why if known,
   - decision label such as `DIRECTION_PARKED`,
   - explicit safety boundary: note-only, no generation/render/upload/schedule/config/runtime mutation unless separately requested.
3. If the project has an active strategy queue or routing index, update it only if needed to prevent reopening the lane.
4. Do not save the parked idea to global memory unless it is a stable cross-project user preference.
5. Do not create a narrow skill for the parked topic. If the session revealed a reusable method, update an umbrella skill instead.
6. In chat, acknowledge briefly and state the current main lane/phase so the user knows what remains active.

## Pitfalls

- Do not treat shelving one idea as approval to advance another lane.
- Do not turn a parked project idea into a permanent global prohibition; the user may reopen it later.
- Do not record long narrative rationale in global memory. Put detailed rationale in repo handoff or Obsidian if it will guide future strategy.
- Do not use this as a reason to run generation, upload, OAuth, scheduler, privacy, or channel-config actions.

## Minimal handoff entry shape

```markdown
- YYYY-MM-DD <direction> parked:
  - User decided to shelve <direction> for now after <brief context>.
  - Decision label: `<DIRECTION_PARKED>`.
  - Current active project focus remains <main lane/phase> unless the user explicitly reopens this direction later.
  - Safety boundary: note-only; no generation/render/upload/publish/schedule/OAuth/channel config/privacy/scheduler/runtime-data action.
```
