> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Redundant / noisy file inventory — 2026-05-26

Status: read-only inventory followed by conservative cleanup pass / Recycle Bin used for deletes
Scope: `<private-workspace>`
Reviewer route/tool: Hermes local scan + git status + git check-ignore
Visible runtime model: gpt-5.5 via Hermes
Boundary: inventory plus local file hygiene only; no target-touching actions and no evidence directories were deleted.

Cleanup performed after this inventory:
- Sent to Windows Recycle Bin: `UsersOwnerAppDataLocalTemptmpjikmnusiout.json`, `handoff/live_bounty_lane_runner_stdout_check.json`, `handoff/live_bounty_preview_grounding_stdout_check.json`, `handoff/live_bounty_preview_grounding_status.json`.
- Moved root CVE drafts to ignored local quarantine: `setting/local/quarantine/cve_brief_20260526_unverified_do_not_use.json` and `.md`.
- Moved older tracked root CVE briefs to unverified CVE archive: `cves/unverified/2026-05-22_websearch_fallback_unverified.md` and `cves/unverified/2026-05-23_websearch_fallback_unverified.md`.
- Added `handoff/current_artifact_index.md` to classify active/reference/superseded/local-only artifacts before further hardening.
- Updated `.gitignore` for recurring temp/CVE/stdout-check patterns.

## Executive summary

The repository does have redundancy/noise, but it is not all the same kind.

Main finding:

```text
Most byte-size noise is already ignored runtime/cache evidence.
Most git-status noise is untracked handoff/planning artifacts from recent work.
The riskiest cleanup targets are unignored transient root/debug JSON/MD files, not evidence archives.
```

Current scan snapshot:

```text
Total scanned files, excluding common caches/.git: 8,631
Total scanned size: ~182.36 MB
Largest top-level areas:
- setting/:      5,945 files, ~148.99 MB  mostly ignored local Chrome/tool/cache material
- cves/:            16 files, ~13.27 MB   mostly ignored raw JSON/CSV caches
- <artifact-output-dir>/:  1,455 files, ~11.83 MB   ignored local lab evidence artifacts
- handoff/:        434 files, ~3.34 MB    project coordination truth + some debug/status noise
- scripts/:        144 files, ~1.40 MB    active tooling
- notes/:           46 files, ~1.32 MB    project notes / Obsidian bridge
```

## Git status noise classes

### A. Modified tracked files — review before any cleanup

These are not redundancy by default; they are active changes or user/operator edits.

```text
M config/scope.txt
M handoff/accepted_changes.md
M handoff/active_strategy_queue.md
M programs/<program-slug>/notes/coupang_tw_phase5a_dry_run_packet_20260525.md
M handoff/current_navigation.md
M notes/obsidian_projects/Cybersec Lab.md
M recon.sh
```

Recommendation:
- Do not delete or reset automatically.
- Review with `git diff` and classify as accepted project changes, operator scope edits, or stale edits.
- `config/scope.txt` is operator-owned / security-sensitive; never auto-clean.

### B. Untracked root-level transient / suspicious files — likely cleanup candidates

```text
UsersOwnerAppDataLocalTemptmpjikmnusiout.json
cve_brief_20260526.json
cve_brief_20260526.md
```

Why noisy:
- They are at repo root.
- They are not currently ignored by `.gitignore`.
- `UsersOwnerAppDataLocalTemptmpjikmnusiout.json` looks like a temp-path leak artifact.
- `cve_brief_*.json/md` are current-intel drafts and should probably live under `cves/`, `handoff/`, or `setting/local/quarantine/`, depending verification status.

Recommendation:
- Quarantine or move after human review.
- Add `.gitignore` rules for root transient patterns only if this recurrence is expected.

Suggested classification:

```text
UsersOwnerAppDataLocalTemptmpjikmnusiout.json -> delete or move to setting/local/quarantine/ after confirming no useful content
cve_brief_20260526.json/md -> if unverified, move to setting/local/quarantine/ or cves/unverified/; if verified, promote to cves/ or handoff/ with primary-source citations
```

### C. Untracked debug/status JSON in handoff — likely stale runtime checks

```text
handoff/live_bounty_lane_runner_status.json
handoff/live_bounty_lane_runner_stdout_check.json
handoff/live_bounty_preview_grounding_status.json
handoff/live_bounty_preview_grounding_stdout_check.json
```

Why noisy:
- These look like one-run status/stdout checks.
- They are not ignored by `.gitignore`.
- Durable state should be summarized in accepted handoff entries or named evidence artifacts, not root-level handoff debug stdout files.

Recommendation:
- Keep only if they are intentionally latest machine-readable status pointers.
- Otherwise move to `handoff/tmp/` or `setting/local/`, or ignore `handoff/*_stdout_check.json` / selected status files.
- If kept, document why they are authoritative latest pointers.

### D. New live-bounty / tactical-freedom handoff artifacts — probably useful, not redundant yet

Examples:

```text
docs/strategy/live_bounty/live_bounty_tactical_preview_template_20260526.md
docs/strategy/platform/multi_agent_bug_hunting_engineering_plan_20260526.md
docs/strategy/platform/multi_agent_bug_hunting_operating_model_20260526.md
docs/policy/tactical_freedom_platform_direction_20260526.md
docs/strategy/live_bounty/live_bounty_no_finding_feedback_log.md
docs/strategy/live_bounty/live_bounty_attack_class_matrix_20260526.md
docs/strategy/live_bounty/live_bounty_high_hit_rate_target_filter_20260526.md
docs/strategy/live_bounty/next_live_bounty_shortlist_20260526.md
docs/strategy/live_bounty/proof_library_live_bounty_bridge_20260525.md
```

Recommendation:
- Do not delete now.
- Consolidate later into:
  - one current navigation pointer,
  - one active strategy queue summary,
  - compact named reference docs,
  - archived superseded dated drafts.

### E. New schemas/scripts/tests/templates — active engineering substrate, not redundant

```text
schemas/
scripts/live-bounty-lane-runner.py
scripts/live-bounty-lane-status.py
scripts/live-bounty-preview-grounding.py
scripts/live-bounty-preview-synthesize.py
scripts/evidence-redaction-check.py
tests/test_live_bounty_*.sh
templates/live_bounty_attack_path_candidate_packet.md
```

Recommendation:
- Keep.
- Add drift-lock tests later, not cleanup.

### F. Ignored evidence/cache/log bulk — large but intentionally local

Already ignored by `.gitignore` and verified with `git check-ignore`:

```text
setting/local/
<artifact-output-dir>/
logs/
scans/
handoff/worker_logs/
cves/*.json
cves/*.csv
```

Recommendation:
- Do not treat as repo redundancy if storage is acceptable.
- If disk pressure appears, archive outside repo or compress old evidence, but do not delete evidence automatically.
- For browser profiles under `setting/local/chrome-*`, assume possible cookies/session/local storage; do not expose or commit.

## Largest handoff files

Largest visible handoff files include:

```text
handoff/worker_logs/codex_20260518_013951.log                      ~392.7 KB  ignored
handoff/accepted_changes.md                                        ~256.3 KB  active append-only history
handoff/cowork_p3_7_direction_review.md                             ~84.6 KB
handoff/cowork_p1_4_proposal.md                                     ~67.8 KB
handoff/cowork_p3_6_direction_review.md                             ~58.0 KB
handoff/cowork_phase1_proposal.md                                   ~51.7 KB
handoff/cowork_p3_5_direction_review.md                             ~47.1 KB
handoff/archive/active_strategy_queue_pre_navigation_cleanup_*.md    ~34.8 KB
handoff/current_navigation.md                                       ~26.5 KB
```

Recommendation:
- `accepted_changes.md` is getting too large and should stay append/prepend-only, but future entries should be shorter with links to named artifacts.
- Old direction reviews should be classified as `active`, `reference`, or `superseded` in a lightweight index rather than deleted.
- Worker logs are already ignored and can be rotated/compressed if needed.

## Duplicate / repeated artifact patterns

The duplicate scan found many repeated groups, mostly expected:

```text
setting/local/tool_acquisition/... PayloadsAllTheThings/sqlmap files
<artifact-output-dir>/... repeated health_pre/health_post JSON
<artifact-output-dir>/... repeated WebGoat registration/login HTML
scans/... repeated safe_input/live_hosts tiny files
setting/local/chrome-* LevelDB/CURRENT/MANIFEST/cache files
```

Recommendation:
- Do not deduplicate these manually inside evidence directories; repeated controls are part of evidence provenance.
- If storage becomes a concern, archive entire old run directories rather than deleting individual duplicate files.

## Cleanup priority list

### P0 — safe inventory / classify before cleanup

1. Inspect and classify root transient files:
   - `UsersOwnerAppDataLocalTemptmpjikmnusiout.json`
   - `cve_brief_20260526.json`
   - `cve_brief_20260526.md`
2. Decide whether handoff debug stdout/status JSON should be tracked latest pointers or moved/ignored:
   - `handoff/live_bounty_lane_runner_*check.json`
   - `handoff/live_bounty_preview_grounding_*check.json`
3. Review modified tracked files before any reset/deletion, especially `config/scope.txt` and `recon.sh`.

### P1 — reduce future handoff sprawl

1. Add `scripts/append-accepted-change.py` or equivalent to prevent manual large-file overwrite risk.
2. Keep `accepted_changes.md` entries compact and move long details into named artifacts.
3. Add a current-artifacts index with statuses:
   - active
   - reference
   - superseded
   - archived
   - local-only sensitive / ignored

### P1 — active strategy/navigation cleanup

1. Merge current high-hit-rate/tactical-freedom guidance into `current_navigation.md` and `active_strategy_queue.md` as compact pointers.
2. Mark older dated handoff docs as reference/superseded in an index instead of leaving every file equally discoverable.
3. Add a “current must-read files” list for workers so Claude/Codex do not wander through stale handoff files.

### P2 — ignored bulk retention policy

1. Define retention/archival policy for:
   - `<artifact-output-dir>/`
   - `setting/local/`
   - `logs/`
   - `scans/`
   - `handoff/worker_logs/`
2. Prefer archive/compress whole run directories, not piecemeal deletion.
3. Keep secrets/session/browser profiles local and ignored.

## Recommended next action

Do not delete anything yet.

Best next engineering slice:

```text
repo noise cleanup plan v1
```

Deliverables:
- `handoff/current_artifact_index.md` with active/reference/superseded/local-only categories.
- `scripts/append-accepted-change.py` for safe accepted-change writes.
- `.gitignore` patch for obvious root transient/debug outputs, after confirming patterns.
- Optional `scripts/repo-noise-inventory.py` that reproduces this report without touching files.

This should be done before any aggressive cleanup, because the project has sensitive evidence and operator-owned scope files.
