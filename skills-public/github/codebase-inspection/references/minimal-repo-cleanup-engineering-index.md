> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Minimal Repo Cleanup and Engineering Index Pattern

Use when a repo has become chaotic with many policies, dated handoffs, strategy variants, and untracked/modified files, especially in safety-sensitive security projects.

## Core decision rule

Do not default to a blank new repo, `git reset --hard`, or `git clean -fdx` when the tree contains policy, scope, evidence, lane state, or handoff provenance.

Prefer:

1. Freeze and inventory.
2. Classify files into active truth / platform code / program state / evidence / historical / quarantine.
3. Archive or quarantine uncertain files instead of deleting.
4. Establish a small engineering index and active policy index.
5. Split cleanup into reviewable commits.
6. Verify after each batch.

## Recommended active index set

For a Hermes-style project, create or maintain:

- `docs/ENGINEERING_INDEX.md` — read order, active truth, repo zones, promotion gates, commit discipline.
- `docs/policy/README.md` — active policy set and archived/superseded policy boundary.
- `handoff/INDEX.md` — current handoff map and root-level sprawl rule.
- `handoff/current_artifact_index.md` — current artifact pointers.
- `handoff/current/worktree_cleanup_index_<date>.md` — cleanup checkpoint.

## Archive pattern

- Superseded policy/memory variants: `docs/policy/archive/<date-or-batch>/`.
- Dated root handoff files: `handoff/archive/phase_history/<batch>/`.
- Uncertain sensitive/runtime material: ignored local quarantine, not committed.

## Anti-chaos rules

- Future corrections patch active files instead of creating dated variants.
- `handoff/` root holds current map/queue/state/rolling IPC only.
- Platform code promotion requires tests/schema or a documented validation command.
- Live-target automation defaults to dry-run/no-target unless explicitly scoped and gated.
- Global memory stores only compact signposts; project state belongs in repo handoff or Obsidian/project notes.

## Verification

After cleanup/index edits, run the project’s local static review plus focused tests. For a Hermes cybersec repo, typical checks are:

```bash
git diff --check
bash tests/test_current_live_bounty_contracts.sh
bash tests/test_recurring_substrate_dry_run.sh
bash tests/test_operator_inbox_summary.sh
bash ./bin/hermes review
```

## Pitfalls

- Do not delete historical policy just because it is superseded; archive it so provenance remains.
- Do not make new policy to say “stop making policy” unless the repo lacks a hygiene policy; otherwise patch the active hygiene/index file.
- A clean-looking tree that loses authorization/evidence history is worse than a messy but traceable tree.
