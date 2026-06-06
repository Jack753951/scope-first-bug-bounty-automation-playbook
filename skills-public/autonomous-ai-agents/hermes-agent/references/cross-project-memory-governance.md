> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Cross-Project Memory Governance

Use this when the user asks whether Hermes memory is shared across projects, or when multiple repos/profiles need to coexist without contaminating each other.

## Core model

- Hermes long-term memory is profile-level, not repo-level, unless the memory backend/profile setup says otherwise.
- Repo context files such as `.hermes.md`, `AGENTS.md`, or project handoff files are project-local context, but persistent `user` / `memory` entries can affect every project using the same Hermes profile.
- Hermes profiles are the cleanest built-in isolation boundary because profiles can separate configs, sessions, skills, and memory.

## Hidden risks of shared memory

1. Cross-project contamination
   - A creative/content preference can bias a cybersecurity workspace.
   - A strict security workflow can over-constrain a harmless creative or productivity task.

2. Goal drift
   - Shared memories can pull a project toward the wrong success metric.
   - Example: a cybersecurity lab should not become primarily a CTF workflow just because CTF calibration notes exist.

3. Stale operational facts
   - Do not store PR numbers, issue numbers, commit SHAs, temporary file paths, scan results, phase-done logs, or run artifacts as durable memory.

4. Sensitive leakage
   - Do not store secrets, tokens, cookies, credentials, hashes, loot, target details, client-sensitive information, private bug bounty scope details, or transient scan output in global memory.

5. Instruction collision
   - Avoid imperative memory such as "always run X".
   - Prefer declarative facts scoped by project/path, such as "Project Y uses repo handoff as engineering truth".

## Recommended layers

- Global memory: small, durable cross-project user preferences and broadly applicable operating principles.
- Project context files: project-specific rules and current operating contract.
- Repo handoff: engineering truth, phase history, worker reviews, accepted changes.
- Obsidian/project notes: durable strategy, decisions, methodology, project-health reviews.
- Skills: reusable procedures and workflows.
- Session search: recall transient past work without polluting long-term memory.

## Isolation options

### Single profile with hygiene

Best when convenience and cross-project learning matter more than hard separation.

Rules:
- Save only durable cross-project facts in global memory.
- Keep project-specific strategy in Obsidian/project notes.
- Keep engineering truth in repo handoff.
- Convert reusable workflows into skills.

### Per-project profiles

Best for sensitive, high-complexity, or very different workspaces.

Possible split:
- `default` for general work
- `cybersec` for security labs and authorized testing
- `youtube` for content automation
- `investment` for finance/investment workflows

Tradeoff:
- Better isolation, less contamination.
- More setup and some shared preferences must be intentionally copied or documented.

### Hybrid recommendation

Keep default/global memory small, use project profiles when risk or complexity warrants it, and use Obsidian plus skills to share process-level learning across projects without blindly copying memory entries.

## Cross-project optimization procedure

When another project has already improved memory flow:

1. Read its memory policy, `.hermes.md`, handoff policy, or Obsidian note.
2. Compare process, not raw memory entries.
3. Extract common principles into a shared memory-governance note or skill reference.
4. Keep project-specific overrides in each repo.
5. Convert reusable procedures into skills.
6. Save only a compact pointer in Hermes memory.

## User-facing answer pattern

When asked "does Hermes memory share across projects?":

1. Say yes if the same profile is used; qualify if profiles/backends differ.
2. Explain repo context versus profile memory.
3. List risks: contamination, stale facts, secrets, instruction collision, goal drift.
4. Recommend layered storage and profile isolation only where justified.
5. Offer to compare the other project's memory policy and produce shared governance plus per-project overrides.
