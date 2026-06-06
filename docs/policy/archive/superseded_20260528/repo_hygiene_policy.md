> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Repository Hygiene Policy

Status: active policy
Scope: `<private-workspace>` authorized bug bounty automation platform

## Decision

Do not reset this repository and do not restart from a blank repository as the default cleanup strategy.

This repo is messy, but it contains authorization boundary history, lane state, scope/policy decisions, platform code, tests, evidence pointers, and operator workflow context. Those are more valuable than a visually clean tree. Cleanup must preserve provenance first, then reduce noise.

Default cleanup strategy:

1. Freeze and inventory.
2. Classify files by role.
3. Split work into reviewable commits.
4. Quarantine uncertain material instead of deleting it.
5. Promote only tested/policy-backed artifacts to active project truth.

## When a new repository is allowed

A new repo or clean-room copy is allowed only as a staging/migration aid, not as the source of truth, unless the operator explicitly approves a repository reset.

Allowed use cases:

- build a temporary clean staging copy for structure comparison;
- prototype a reduced tree shape without secrets/evidence;
- generate a migration manifest.

Not allowed by default:

- replacing the main repo while leaving scope/policy/evidence history behind;
- copying only attractive files and losing lane decisions or authorization trail;
- using a clean repo to bypass hard cleanup decisions.

## Forbidden cleanup commands without explicit operator approval

Do not run broad destructive cleanup commands in this repo:

```bash
git reset --hard
git clean -fd
git clean -fdx
rm -rf handoff programs reports logs scans loot config docs/policy docs/runbook intelligence
```

If deletion is needed, prefer recoverable quarantine or recycle/trash. Never hard-delete security evidence, scope files, credentials, logs, scans, loot, governance artifacts, or program lane state during broad cleanup.

## Repository zones

### Active project truth

Keep small, current, and reviewed.

- `.hermes.md`
- `PROJECT_CHARTER.md`
- `README.md`
- `AGENTS.md`
- `docs/policy/`
- `docs/runbook/`
- `docs/strategy/platform/engineering_direction_20260527.md`
- `handoff/current_navigation.md`
- `handoff/active_strategy_queue.md`
- `handoff/current_artifact_index.md`
- `handoff/live_bounty_lane_queue.json`
- `programs/<slug>/scope.json`
- `programs/<slug>/lane_state*.json`

Rule: edit existing active-truth files instead of creating dated variants, unless archiving an immutable checkpoint.

### Platform code

Reusable code must live under stable paths and be testable.

- `platform/`
- `modules/`
- `schemas/`
- `tests/`
- production-quality `scripts/`

Promotion requirements:

- no secrets;
- no live target-touching default;
- explicit input/output contract;
- local or fixture test;
- safe failure mode;
- policy gate if target-touching is possible.

### Program/lane state

- `programs/<slug>/`
- `handoff/live_bounty_evidence/<slug>/`

Rule: do not bulk-delete or bulk-rewrite. Lane state is provenance. Redact sensitive material rather than erase history unless operator requests removal.

Every active lane should end in one of:

- `EXECUTE`
- `PASSIVE_ONLY`
- `PARK`
- `KILL`
- `ARCHIVED`

### Handoff

Current handoff should stay compact.

- Active rolling files stay in `handoff/` only when existing tools require those paths.
- New multi-file working sets should go under `handoff/current/` or a named archived folder.
- Old dated handoffs should move to `handoff/archive/<topic-or-phase>/` after they are indexed.

Do not create new root-level handoff sprawl unless it is a temporary checkpoint that will be archived in the same cleanup batch.

### Historical/reference material

- `docs/charter/historical/`
- `notes/`
- `intelligence/cve_briefs/`
- archived handoff folders

Rule: preserve useful context, but mark it as reference or historical so agents do not treat it as current direction.

### Runtime, local, ignored, or sensitive material

Usually not committed except for `.gitkeep` or sanitized summaries.

- `logs/`
- `scans/`
- `loot/`
- `<artifact-output-dir>/`
- browser/session profiles
- raw request/response captures
- credentials, cookies, tokens, OTPs, verification links

Rule: never promote raw sensitive material into active truth, memory, or committed docs.

## Commit policy

Avoid mega-commits. Cleanup must be split by intent:

1. `chore(repo): snapshot cleanup inventory`
2. `chore(repo): establish platform structure`
3. `policy: define repo hygiene and operator gates`
4. `feat(platform): add dry-run no-target substrate`
5. `test(platform): cover inbox and lane contracts`
6. `docs: archive retired workbench material`
7. `chore(cleanup): quarantine transient artifacts`

Each commit must answer:

- Is it target-touching? Default answer should be no.
- Does it contain program-private or sensitive data?
- What validates it?
- How can it be reverted safely?

## Cleanup workflow

### Phase 0 — Freeze

Run read-only inventory:

```bash
git status --short
git diff --stat
git diff --name-status
```

Create a temporary safety branch before large cleanup:

```bash
git switch -c cleanup/worktree-stabilization-20260528
```

Do not run live scans or target-touching automation during cleanup.

### Phase 1 — Classify

Classify every modified/untracked/deleted path into one bucket:

- keep active truth;
- keep platform code/test/schema;
- archive historical/reference;
- quarantine uncertain/transient;
- ignore generated/local;
- delete only with explicit operator approval.

### Phase 2 — Promote

Promote only files that satisfy the relevant zone rules. Temporary scripts must not become production tools without tests and safety gates.

### Phase 3 — Quarantine

Move uncertain material to an ignored local quarantine, for example:

```text
setting/local/quarantine/<YYYYMMDD>/
```

Quarantine is preferred over deletion when a file might contain evidence, private program context, or an unrecovered decision trail.

### Phase 4 — Verify

Minimum verification after cleanup:

```bash
bash ./bin/hermes review
bash tests/test_current_live_bounty_contracts.sh
bash tests/test_recurring_substrate_dry_run.sh
bash tests/test_operator_inbox_summary.sh
```

If shell scripts changed, run `bash -n` or the project review. If scope logic changed, verify unauthorized targets are rejected.

### Phase 5 — Record

Append a short summary to `handoff/accepted_changes.md`:

- what was promoted;
- what was archived;
- what was quarantined;
- what was deliberately not touched;
- validation commands and results.

## Anti-chaos rules for future development

- One active direction file; edit it, do not create daily strategy variants.
- One active navigation file; archive snapshots only when needed.
- No new root-level scratch files.
- New automation starts as no-target/dry-run unless explicitly approved otherwise.
- Every live-lane artifact references scope, policy, stop-before rule, and operator gate.
- Every platform script has tests before being treated as reusable infrastructure.
- Handoff files are indexed or archived; they are not allowed to accumulate silently.
- Cleanup is a normal engineering task, not a panic reset.
