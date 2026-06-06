> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Repo Noise Inventory and Recoverable Cleanup

Use this reference when a user says a repo has too many redundant/noisy files, asks for cleanup, or asks to organize project artifacts without losing evidence.

## Core rule

Inventory first, classify second, cleanup third. When deletion is approved or clearly within the requested cleanup scope, prefer recoverable deletion:

- Windows: send files to the Recycle Bin.
- macOS/Linux desktop: send to trash when available.
- Headless/server: quarantine/move to a local ignored folder instead of hard-deleting unless the user explicitly approves hard deletion.

Never hard-delete security evidence, browser/session profiles, scope files, credentials, logs, scans, loot, or project governance artifacts during a broad cleanup pass.

## Classification buckets

Use these buckets in the report:

1. Active project truth
   - current navigation, active queue, accepted changes, scope/policy files, schemas, scripts, tests, templates.
   - Keep; optionally index.

2. Reference / historical handoff
   - dated direction reviews, proposals, named implementation/review artifacts.
   - Keep; mark active/reference/superseded in an index.

3. Runtime evidence / provenance
   - `kali-output/`, `scans/`, `logs/`, `handoff/live_bounty_evidence/`, lab run directories.
   - Usually ignored; do not delete piecemeal. Archive/compress whole run directories only after explicit confirmation.

4. Local cache/profile/tool material
   - `setting/local/`, browser profiles, acquired external tools, VM/cache files.
   - Usually ignored and may contain sessions/cookies; do not expose or commit. Clean only with explicit scope.

5. Transient/debug outputs
   - root temp JSON, one-run stdout/status checks, failed temp-path leak artifacts, generated helper scratch files.
   - Recycle/trash or move to ignored quarantine after inspection.

6. Unverified current-intel drafts
   - current CVE/advisory/news drafts without primary-source verification.
   - Move to ignored local quarantine or a clearly marked `unverified/` location; do not promote to project truth.

## Suggested workflow

1. Run a read-only inventory:
   - `git status --short`
   - top-level file counts/sizes
   - largest handoff files
   - untracked root files
   - duplicate groups only as hints, not delete instructions
   - `git check-ignore -v` for suspected cache/evidence paths

2. Write or update a repo-local inventory report, for example:
   - `handoff/redundant_file_inventory_<YYYYMMDD>.md`

3. Identify P0 cleanup candidates only:
   - obvious temp/debug outputs,
   - root files that belong in ignored quarantine,
   - duplicate stdout-check files when a durable status/result already exists.

4. Before deleting, inspect candidate contents enough to confirm they are not secrets, scope, evidence, or the only copy of a result.

5. Delete via recycle/trash, not `rm`, when the user requested recoverable deletion.
   - On Windows from Git-Bash, invoke PowerShell/.NET recycle APIs, e.g. `Microsoft.VisualBasic.FileIO.FileSystem::DeleteFile(..., 'SendToRecycleBin')`.
   - If recycle fails, do not silently fall back to hard deletion; quarantine instead or report the blocker.

6. Move unverified-but-potentially-useful drafts into ignored quarantine, e.g. `setting/local/quarantine/`, with `_unverified_do_not_use` in the filename.

7. Patch `.gitignore` narrowly to prevent recurrence:
   - specific root temp patterns,
   - `handoff/tmp/`,
   - stdout-check/debug patterns,
   - but avoid ignoring authoritative status/result artifacts unless their lifecycle is documented.

8. Record the cleanup in `accepted_changes.md` or the project’s equivalent durable handoff:
   - files recycled/trashed,
   - files quarantined,
   - ignore rules added,
   - boundaries: what was not touched.

9. Verify:
   - original paths missing,
   - quarantine paths present,
   - new ignore rules match with `git check-ignore -v`,
   - project review/static checks still pass when relevant.

## Pitfalls

- Do not deduplicate evidence directories by identical content. Repeated files often prove control steps or retries.
- Do not treat ignored bulk as a problem just because it is large; storage cleanup is separate from repo hygiene.
- Do not delete `config/scope.txt` or mutate scope while doing noise cleanup.
- Do not convert unverified current-intel drafts into accepted project guidance during cleanup.
- Do not leave helper cleanup scripts behind; recycle/trash or quarantine the helper if one was created.
