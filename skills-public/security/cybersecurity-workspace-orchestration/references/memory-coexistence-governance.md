> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Memory Coexistence in Cybersecurity Workspaces

Use this when coordinating a cybersecurity repo that shares Hermes memory with other projects.

## Why this matters

Cybersecurity workspaces have stricter memory hygiene than most projects. Shared Hermes memory is useful for stable preferences and cross-project process lessons, but dangerous if target details, authorization facts, scan artifacts, or transient run state leak into global memory.

## Layering rule

- Hermes global memory: compact cross-project preferences and durable operating principles only.
- `.hermes.md`: binding project-specific workflow, safety gates, role routing, and current repo contract.
- `handoff/`: engineering truth, accepted changes, review artifacts, phase history, current work state.
- Obsidian: durable strategy, methodology, project-health reviews, and decisions; never secrets or raw target data.
- Skills: reusable procedures such as review loops, memory governance, or safe workflow validation.
- Session search: recover old conversations instead of saving stale task progress into memory.

## Cybersec red lines

Do not save to Hermes memory or Obsidian:

- credentials, API keys, OAuth tokens, cookies, passwords
- hashes, loot, raw evidence, proprietary wordlists
- target-specific details, scan output, exploit output, client-sensitive data
- private bug bounty scope/rules unless deliberately sanitized into repo policy files
- PR/issue numbers, commit SHAs, phase completion logs, or worker run transcripts

## Review questions for periodic project-health checks

Include memory governance in periodic third-party reviews:

1. Are global memories still cross-project and durable, or have project details leaked in?
2. Are repo handoff files carrying engineering truth instead of global memory?
3. Are Obsidian notes storing strategy/decisions rather than secrets or transient scan output?
4. Are skills capturing reusable procedures instead of narrow session narratives?
5. Is shared memory causing goal drift, such as over-focusing on CTF calibration instead of authorized bug bounty automation?
6. Would a dedicated Hermes profile reduce risk for this project?

## Cross-project optimization

If another project has a better memory workflow, compare process rather than copying raw entries:

1. Read the other project's `.hermes.md`, handoff policy, and Obsidian memory/governance notes.
2. Extract shared principles into a common governance note or umbrella skill reference.
3. Keep cybersec-specific safety overrides in this repo.
4. Keep the other project's domain-specific overrides in that repo.
5. Save only compact pointers in global memory.

## Recommended response posture

When the user asks about shared memory, be direct:

- Same Hermes profile means memory can be shared across projects.
- Profiles are the cleanest isolation boundary.
- A hybrid model is usually best: small global memory, project handoff for engineering truth, Obsidian for durable decisions, skills for reusable procedures, and profiles when sensitivity or complexity warrants isolation.
