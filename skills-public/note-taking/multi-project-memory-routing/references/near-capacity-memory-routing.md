> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Near-Capacity Hermes Memory Routing

Use this pattern when a durable preference or cross-project pointer should be saved but Hermes memory is close to full.

## Pattern

1. Do not force a large new memory entry into an already-full global memory store.
2. Check whether an existing memory entry covers the same project, preference class, or routing policy.
3. Prefer replacing/compacting that existing entry into a denser declarative summary that preserves stable facts and removes stale detail.
4. Add only the new durable preference/signpost, not the session narrative that caused it.
5. If no safe compaction target exists, route the detail to the project handoff or Obsidian and keep only a short pointer in memory, or skip global memory and explain why.
6. Do not delete or rewrite sensitive/project-authoritative handoff state just to make global memory fit.

## Good memory shape

```text
User permits Hermes to apply memory-routing judgment across projects: decide whether durable information belongs in Hermes memory, repo handoff, Obsidian, skills, or session_search; keep project facts local.
```

## Bad memory shape

```text
Today we tried to add memory X, memory was at 98%, then replaced entry Y after P3.4-alt completed...
```

The first is a reusable cross-session preference. The second is a session log and belongs, if anywhere, in session history or project handoff.
