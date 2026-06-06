> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Global Memory as Index; Project Namespace First

Use this when a user says project memory should be moved out of Hermes durable memory and into project memory stores, while global memory should preserve only the rule to consult those stores first.

## Pattern

1. Confirm the distinction:
   - Global Hermes memory is a compact cross-project routing/index layer.
   - Obsidian project namespaces hold long-term strategy, preferences, assumptions, decisions, experiments, and review synthesis.
   - Repo handoff holds engineering truth, accepted changes, validation, current active lanes, and safety gates.

2. Before compacting global memory, preserve project readability:
   - create or update a shared cross-project routing note in Obsidian if one exists;
   - create or update each affected project namespace with a memory-routing note;
   - for repos with handoff governance, add a short compatibility note so future workers know shorter global memory does not mean the project direction changed;
   - add a concise accepted-change/changelog entry when the repo treats memory governance as project state.

3. Rehome project-specific facts before removing them from global memory:
   - content/channel/style preferences -> project Obsidian strategy or system notes;
   - investment assumptions -> investment project Obsidian strategy/assumptions notes;
   - security/cybersec phases, gates, workflow, environment/scope boundaries -> repo handoff plus Cybersec Obsidian methodology/routing notes;
   - runtime/tooling quirks tied to one project -> that project’s Obsidian system/runtime note or repo handoff.

4. Compact global memory to declarative pointers only:
   - where to look for each project;
   - what broad safety/routing constraints apply;
   - user-wide preferences that genuinely apply across projects.

5. Preserve authority order in the new notes:
   1. current explicit user instruction;
   2. live repo/files/config/validation/tool output;
   3. repo handoff for engineering truth and gates;
   4. Obsidian project namespace for long-term strategy and decisions;
   5. Hermes durable memory for compact pointers;
   6. session_search as recall leads only.

## Hacking / sensitive project compatibility

For sensitive projects, include a future-agent note:

- global memory was intentionally compacted;
- do not infer that project direction changed because details disappeared from global memory;
- consult repo handoff and the project Obsidian namespace for phase, scope, gates, roadmap, evidence/report workflow, and safety posture;
- do not place raw targets, scan outputs, exploit payloads, hashes, loot, private scope/rules, credentials, tokens, cookies, or client-sensitive evidence in global memory or broad shared notes.

## Verification

After rehoming/compaction:

- read back the Obsidian routing/index notes and project-specific notes;
- read back repo handoff notes if changed;
- verify global memory now contains only compact pointers and user-wide preferences;
- if a repo handoff was edited, run the project’s lightweight docs/static check only, not unrelated runtime workflows;
- report both what was removed from global memory and where it now lives.

## Pitfalls

- Do not answer “yes, everything should move to Obsidian” without preserving repo handoff as engineering authority.
- Do not leave only “check Obsidian” in global memory; keep enough namespace pointers for future agents to know where to look.
- Do not delete a project-specific global memory item before rehoming it if the content is still useful.
- Do not put sensitive security artifacts into Obsidian just because they are project-specific; store methodology and decisions, not raw evidence or secrets.
