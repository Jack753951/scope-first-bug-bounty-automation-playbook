> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Minimal Repository Governance Cleanup

Use this reference when a user asks to thoroughly clean a messy repository, remove stale policy/memory/process documents, or prevent future project sprawl.

## Core lesson

For governance-heavy repositories, especially security or bug-bounty workspaces, cleanup is not primarily deletion. Cleanup is making the active truth small while preserving provenance.

Default stance:

1. Inventory first.
2. Ask or run an independent review when contracts, safety policy, memory routing, or evidence provenance are affected.
3. Create one active engineering index/read order.
4. Rewrite active indexes to identify the current policy set.
5. Archive superseded policy/memory/handoff files instead of deleting them.
6. Verify with project review/tests.
7. Record the cleanup in the repo's accepted-change log.

## Visible strong-agent / reviewer trace

If project policy says strong agents or external reviewers should be used, make the trace visible in the repo or final report. Do not rely on hidden tool-call summaries only.

Minimum trace:

- role of reviewer/agent;
- context packet supplied or files read;
- whether memory/context sync was performed;
- verdict and blockers;
- how findings changed the cleanup;
- validation after changes.

If the reviewer was a Hermes `delegate_task` subagent rather than a formal repo worker (Claude Code/Codex wrapper), say that explicitly. Do not imply formal worker receipts exist unless they were actually produced.

## Active-index pattern

Create or update a single engineering entrypoint, for example `docs/ENGINEERING_INDEX.md`, with:

- read order for future agents;
- active project truth table;
- repository zones;
- promotion gates;
- commit discipline;
- minimal cleanup rule: archive/quarantine when unsure, do not hard-delete.

Then link it from README, handoff index, and current artifact index.

## Policy/memory consolidation pattern

For policy and memory sprawl:

- keep a `docs/policy/README.md` active policy index;
- list active binding policies separately from templates/references;
- move superseded or phase-specific files to `docs/policy/archive/<cleanup-date>/`;
- state which active file supersedes each archive candidate;
- keep memory routing in one active file rather than multiple overlapping memory policies.

Do not erase old policy files when they carry authorization, safety, or decision history. Archive them and remove them from the active read path.

## Handoff cleanup pattern

For handoff sprawl:

- keep root `handoff/` for current navigation, queue, artifact index, accepted changes, machine state, and rolling IPC only;
- move dated strategy/review/run-card files to `handoff/archive/<topic-or-date>/`;
- write a short cleanup index under `handoff/current/` documenting moved files and untouched sensitive areas;
- do not overwrite append-only logs silently.

## Hard stops

Do not run broad destructive cleanup without explicit approval:

```bash
git reset --hard
git clean -fd
git clean -fdx
rm -rf handoff programs reports logs scans loot config docs/policy docs/runbook intelligence
```

Do not bulk-delete or rewrite:

- scope files;
- evidence, reports, logs, scans, loot;
- program lane state;
- accepted-change/audit logs;
- security-sensitive local runtime material.

## Verification

Minimum cleanup verification:

```bash
git diff --check
# plus project-specific static review/tests
```

For security automation repos, also run contract tests for scope/lane state and any dry-run/no-target substrate touched by the cleanup.

## Final report shape

Report in plain terms:

- what active indexes were added/updated;
- what was archived and where;
- what was deliberately not touched;
- what validation passed;
- whether strong-agent review was formal worker review or subagent review;
- remaining dirty-tree risk and next commit split.
