> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Mandatory Pre-Save Routing Pattern

Use when the user explicitly asks that memory saves be classified through the memory-routing workflow before anything is stored.

## Pattern

1. Treat the request as a standing workflow preference for durable memory operations.
2. Before calling `memory(add|replace|remove)`, classify the candidate fact:
   - global Hermes memory: stable cross-project preference, safety/routing rule, or compact signpost;
   - user profile: stable user preference or communication/workflow preference;
   - repo handoff / notes: project-local engineering truth, accepted changes, validation, roadmap, or daily note;
   - Obsidian: strategy, rationale, research, methodology, decision record, or periodic review synthesis;
   - skill: reusable procedure, checklist, pitfall, or tool workflow;
   - session_search only: past-session recall lead that is not current authority.
3. If the candidate is project-specific, first route the detail to the project's handoff/notes or Obsidian namespace. Save only a compact global pointer if it will affect future sessions.
4. If global memory is near capacity, do not append a session narrative. Replace/compact an overlapping existing entry into a denser declarative signpost, or skip global memory and state where the detail was routed.
5. If the user correction is about how to perform a class of tasks, update the relevant skill in addition to memory.
6. In the final response, state the routing result: what was put in memory, what stayed project-local, what went into a skill, and what was intentionally not stored.

## Pitfall

Do not satisfy a "remember this" request by directly adding a global memory entry. The routing decision comes first; the memory tool call, if any, is only the final step after classification.
