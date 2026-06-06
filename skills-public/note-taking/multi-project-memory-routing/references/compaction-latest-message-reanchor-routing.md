> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Compaction / Latest-Message Re-anchor Routing

Use this pattern when a context-compaction block, handoff summary, or recovered-session note appears immediately before a new user request.

## Problem

Compaction summaries are reference-only background. They can mention already-completed tasks, stale questions, or prior side-effect boundaries. If the agent answers one of those instead of the latest live user message, it can report the wrong status, imply actions that were not requested, or skip the user's actual orientation question.

## Procedure

1. Treat persistent memory and the current explicit user message as active authority; treat the compaction block as background only.
2. Identify the latest user message after the compaction block and restate its task internally before acting.
3. If the latest message is a status/orientation question, answer read-only from the relevant authority layers; do not continue implementation, staging, upload, scheduling, or cleanup work from the compacted history unless explicitly requested.
4. If the latest message asks for hygiene/review of the conversation, update the applicable class-level skill or reference rather than creating a session-specific skill.
5. When replying, do not answer a prior task that merely appeared in the compaction background. If needed, say that the prior material is only context and then answer the live request.

## Routing

- Reusable lesson: this reference / class-level skill.
- Project-specific status: repo handoff, active navigation, or Obsidian project namespace.
- User-wide preference correction: compact Hermes memory only if it is stable across projects.

## Verification

Before final response, check:

- The answer addresses the latest live user request, not a compacted historical request.
- Any project-status answer is read-only unless the user explicitly asked to proceed.
- No stale run artifacts from the compaction block were promoted into global memory or skill state.
