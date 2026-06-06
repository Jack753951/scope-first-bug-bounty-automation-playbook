> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Memory Compaction Notification Pattern

Use this reference when global Hermes durable memory is near capacity and a compacted entry may affect how future project workers interpret context.

## Problem

A project may rely on a compact global memory pointer such as delegated ownership, safety posture, worker routing, or deletion preference. When that pointer is shortened to save memory, future agents may misread the shorter entry as a project reset or as loss of prior direction.

## Pattern

1. Load this routing skill before deciding where the change belongs.
2. Keep detailed project state out of Hermes durable memory.
3. Add a short notice to the affected repo's memory/handoff policy:
   - memory may be compacted;
   - compaction is not a project reset;
   - repo handoff remains engineering truth;
   - project Obsidian remains strategy/decision truth;
   - list the compact intent that should survive.
4. If a shared Obsidian alignment note exists, add the same notice there.
5. If the preference affects project operations, spell out the project-local interpretation.
6. Add a brief accepted-change/handoff entry when the repo uses append-only engineering logs.
7. Verify only the documentation/policy edit; do not run unrelated tests or touch runtime data.

## Deletion Preference Example

When the user prefers recoverable deletion:

- Ordinary project files/folders: move to Windows Recycle Bin when feasible instead of permanent deletion.
- Sensitive material: ask before deletion, quarantine, or secure cleanup. Examples include OAuth files, tokens, client secrets, credentials, loot, private scan evidence, publication state, and client/target-sensitive data.
- Clearly rebuildable caches/artifacts: direct deletion is acceptable when needed, for example `__pycache__`, `.pytest_cache`, or deterministic build cache.

## Compact Notice Template

```markdown
## YYYY-MM-DD global memory compaction notice

Hermes durable memory is near capacity and may be compacted. Future workers should not treat a shorter global-memory entry as a project reset or direction change. The authoritative project context remains this repo's handoff files plus active Obsidian notes.

Current compact global-memory intent:

- <stable routing/safety/ownership point>;
- <stable project preference>;
- <stable coordination rule>.

Cross-project deletion preference, if applicable:

- ordinary files/folders should be moved to the Windows Recycle Bin when feasible;
- sensitive material requires user confirmation before deletion/quarantine/secure cleanup;
- clearly rebuildable caches/artifacts may be directly deleted.
```
