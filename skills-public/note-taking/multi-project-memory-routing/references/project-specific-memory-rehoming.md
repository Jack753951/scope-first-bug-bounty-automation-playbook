> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Project-Specific Memory Rehoming

Use this pattern when the user identifies a global Hermes memory entry as too project-specific, but the content may still be useful later.

## Trigger

- User says a memory can be deleted, removed from cross-project memory, or "should be in Obsidian/project memory instead".
- The entry contains a single project's strategy, creative direction, investment assumption, experiment result, artifact preference, or operational detail.

## Procedure

1. Classify the entry before changing storage.
   - Cross-project user preference or safety principle -> keep/compact in Hermes memory.
   - Project-specific strategy/decision/research/assumption -> rehome to that project's Obsidian namespace.
   - Project engineering truth/validation/worker output -> repo handoff.
   - Reusable workflow -> skill or skill reference.
2. If the user only says "delete" but the entry is still valuable project context, treat deletion as removal from global Hermes memory, not necessarily destruction. State this distinction and, when safe, rehome it to Obsidian/project notes.
3. Remove or compact the global memory entry after rehoming, so future sessions do not carry project-specific detail globally.
4. Verify by reading back the destination note or otherwise confirming the target write succeeded.
5. In the final response, report both sides:
   - removed from Hermes global memory/user profile;
   - stored at the concrete project-local Obsidian or handoff path.

## Note shape

Project Obsidian notes should include compact metadata:

```markdown
Status: active | reference | superseded
Source: User | Hermes | Mixed
Date: YYYY-MM-DD
Repo truth: path/to/repo-handoff.md or n/a — project-specific memory note
```

## Pitfall

Do not answer "deleted" when the real correction is "wrong layer". Rehoming preserves useful project knowledge while keeping global memory clean.
