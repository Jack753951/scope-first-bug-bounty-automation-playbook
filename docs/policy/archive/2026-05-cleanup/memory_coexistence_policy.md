> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Memory Coexistence Policy — Cybersec Workspace

Status: active operating guidance
Scope: Hermes memory, repo handoff files, Obsidian notes, and session_search for cybersec coexisting with YouTubeAgent and other user projects
Source aligned with: `<user-home>\Desktop\youtubestrict\youtube_agent\handoff\memory_governance.md`

## Current State

Hermes is currently using the built-in memory backend under the `default` profile. In this setup, durable memory is shared across projects that use the same Hermes profile. Project context files such as `.hermes.md` are repo-local, but persistent `USER PROFILE` / `MEMORY` entries are profile-level unless separate Hermes profiles are used.

## Authority Order

When facts conflict, use this order:

1. Current explicit user instruction.
2. Live project files, config, validation output, and current repo state.
3. Project repo handoff files for accepted engineering state.
4. Active Obsidian project notes for long-term strategy, research, decisions, experiments, and review conclusions.
5. Hermes durable memory for compact cross-project preferences, safety rules, and pointers.
6. `session_search` as recall only; verify against files before treating it as current truth.

## Memory Layers And Authority

### 1. Hermes durable memory

Purpose: compact cross-project guidance and stable pointers.

Allowed:

- User-wide stable preferences: language, command style, review depth, visual QA preference.
- Cross-project operating principles that remain true for weeks/months.
- Short index facts pointing to the correct project memory location.

Avoid:

- Daily progress, phase-done logs, PR/issue/commit IDs, dated run results, one-off validation status.
- Full project strategies or long review conclusions.
- Anything likely to be stale within a week.
- Secrets, tokens, credentials, OAuth details, cookies, private API keys.
- Cybersec target details, scan output, hashes, loot, client-sensitive data, or bug bounty private scope/rules.

Rule of thumb: Hermes memory is a signpost, not a database.

### 2. Repo handoff files

Purpose: engineering source of truth for this repository.

Use for:

- Accepted implementation changes.
- Validation outcomes.
- Claude/Codex/Hermes worker outputs that affect the repo.
- Blocked follow-ups and safety gates.
- Current engineering constraints a future worker must see.

For cybersec, core files include:

- `.hermes.md`
- `handoff/accepted_changes.md`
- `handoff/model_usage_routing_policy.md`
- `docs/policy/review_tiering_policy.md`
- `docs/policy/oss_recon_gate.md`
- `handoff/periodic_reviews/YYYY-MM-DD/`
- `handoff/memory_coexistence_policy.md`

Rule of thumb: repo handoff records what changed, what was verified, what is safe/unsafe, and what remains blocked.

### 3. Obsidian project notes

Purpose: long-term project knowledge that should be searchable, linked, and understandable outside one repo diff.

Use for:

- Strategy and roadmap rationale.
- Research and methodology notes.
- Decision records and periodic review synthesis.
- Durable lessons from CTF/lab calibration that improve authorized bug bounty workflow.
- Cross-session context that should guide future planning.

Each durable note should include:

```markdown
Status: active | superseded | rejected | experiment | reference
Source: User | Hermes | Claude | Codex | Mixed
Date: YYYY-MM-DD
Repo truth: path/to/handoff-or-code-file, if applicable
```

Rule of thumb: Obsidian records why a decision exists and how future agents should reason about it.

### 4. Skills

Purpose: reusable procedures and judgment criteria.

Use skills for workflows, not raw memory. If a process is reusable across projects, convert it into a skill or update an existing one instead of stuffing long instructions into Hermes memory. The shared skill for this framework is `multi-project-memory-routing`; it must remain a process/checklist skill, not a project database.

### 5. session_search

Purpose: recall and discovery.

Use for:

- Finding earlier conversations when the user says "last time" or "remember when".
- Recovering leads for where a decision may have been written.

Do not use as authority without verification. If `session_search` finds a claim, verify it against repo handoff, Obsidian active notes, or live files before acting.

## Main Risks

1. Cross-project contamination
   - A YouTube/content preference can affect cybersec decisions.
   - A cybersec safety rule can over-constrain harmless creative work.

2. Stale operational state
   - PR numbers, phase completion notes, temporary artifacts, target details, and scan output become wrong quickly if stored in memory.

3. Security and privacy leakage
   - Secrets, tokens, cookies, target details, hashes, loot, client-sensitive data, or bug bounty scope details must not be saved into global memory.

4. Instruction collision
   - Project-specific workflows can compete if written as imperative memory entries.
   - Bad pattern: "Always run X".
   - Better pattern: "Project Y uses X when working under path Z".

5. Goal drift
   - Cross-project memory may cause the agent to reuse the wrong success metric, such as optimizing cybersec like a content pipeline or treating CTF calibration as the main cybersec roadmap.

## Project Namespace Convention

Prefer one Obsidian vault with project namespaces:

```text
Shared/
Projects/YouTubeAgent/
Projects/Cybersec Lab/
Projects/InvestmentAutomation/
```

For cybersec, durable strategy/methodology notes belong under:

```text
Projects/Cybersec Lab/
```

Shared cross-project rules belong under:

```text
Shared/
```

Do not put cybersec target details, scan output, credentials, loot, hashes, or client-sensitive data in either location.

## Recommended Isolation Options

### Option A — Keep one Hermes profile, enforce strict memory hygiene

Best when projects intentionally share learning and the user wants convenience.

Rules:

- Save only durable, cross-project facts in global memory.
- Store project-specific durable strategy in Obsidian project notes.
- Store engineering truth in repo handoff.
- Never save secrets, target details, scan results, PR numbers, issue numbers, commit SHAs, or phase-done logs into memory.
- Use declarative memory, not imperative commands.

### Option B — Use Hermes profiles per major project

Best when project separation matters more than convenience.

Possible profile split:

- `cybersec`
- `youtube`
- `investment`
- `default` for general work

Benefit:

- Separate configs, sessions, skills, and memory.
- Less cross-project contamination.

Cost:

- Some useful user preferences must be copied or maintained in multiple profiles.
- More setup and routing discipline.

### Option C — Hybrid model

Recommended long-term:

- Keep a small default/global profile for universal preferences.
- Use project profiles for high-sensitivity or high-complexity projects.
- Keep a shared Obsidian namespace for cross-project operating principles.
- Keep repo-local `.hermes.md` and handoff as the source of truth for each project.

## Cross-Project Alignment With YouTubeAgent

YouTubeAgent already defines the stronger general policy in:

```text
<user-home>\Desktop\youtubestrict\youtube_agent\handoff\memory_governance.md
```

Cybersec adopts the same layer model and adds stricter restricted-data rules.

Common rules shared by both projects:

1. Hermes memory is compact cross-project guidance and pointers, not a database.
2. Repo handoff files are engineering truth.
3. Obsidian project namespaces store long-term strategy and decision rationale.
4. `session_search` is recall only and must be verified.
5. Periodic reviews must check memory drift, handoff drift, goal drift, and structure drift.
6. Shared Obsidian notes contain only cross-project governance, not project state.

Cybersec-specific overrides:

1. Never store target details, scan output, payloads, credentials, tokens, cookies, hashes, loot, client-sensitive data, or bug bounty private scope/rules in Hermes memory.
2. Keep CTF as workflow calibration only unless it directly improves authorized bug bounty workflow.
3. Do not let YouTube/content success metrics influence cybersec roadmap decisions.
4. Preserve scope/authorization gates and triage-only semantics as non-negotiable project rules.

YouTubeAgent-specific overrides remain in its repo policy and include no upload/publication/scheduler/OAuth/channel activation without explicit approval.

## Maintenance Checklist

Run this during periodic project reviews or after major phases:

- Hermes memory contains only compact cross-project facts and pointers.
- Obsidian project index links to active strategy, decisions, experiments, and review process.
- Superseded Obsidian notes are clearly marked.
- Repo handoff reflects accepted engineering changes and validation status.
- `session_search` findings used in the phase were verified against files.
- No secrets or credential material were copied into notes.
- Other projects would not accidentally inherit project-specific rules from global memory.
- Cybersec has not drifted into CTF-as-main-roadmap or schema-building without workflow value.

## Current Shared Governance Artifacts

- YouTubeAgent repo policy: `<user-home>\Desktop\youtubestrict\youtube_agent\handoff\memory_governance.md`
- Cybersec repo policy: `<private-workspace>\handoff\memory_coexistence_policy.md`
- Shared Obsidian policy: `<user-home>\Documents\ObsidianProjects\Projects\YouTubeAgent\Shared\Memory_Governance.md`
- Cybersec Obsidian policy: `<user-home>\Documents\ObsidianProjects\Projects\YouTubeAgent\Projects\Cybersec Lab\Memory Governance\Hermes Memory Coexistence Policy.md`
- Reusable process skill: `multi-project-memory-routing`

## Next Action

During the next periodic review, verify that both YouTubeAgent and cybersec use this same layer model and that only project-neutral guidance remains in Hermes durable memory.
