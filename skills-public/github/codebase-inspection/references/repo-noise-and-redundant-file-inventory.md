> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Repo noise and redundant file inventory

Use when the user asks whether a project has redundant files, noisy artifacts, stale handoff files, excessive generated outputs, or cleanup candidates.

## Principle

Do a read-only classification first. Do not delete, move, redact, reset, or archive files during the first inventory unless the user explicitly asks for cleanup and the scope is safe.

For security, finance, client, browser-profile, or evidence-heavy repos, treat large ignored directories as potentially useful local evidence/cache, not trash.

## Inventory dimensions

Report at least these classes:

1. Modified tracked files
   - Active changes, operator edits, or unreviewed work. Never call them redundant by default.
   - Security-sensitive files such as scope, credentials, auth config, scheduler, deployment, or billing config require explicit human review.

2. Untracked root-level transients
   - Temp JSON/MD, local tool output, current-intel drafts, accidental path-leak filenames.
   - These are usually the safest first cleanup candidates after inspecting content.

3. Untracked handoff/debug status artifacts
   - One-run stdout/status/check JSON files in coordination directories.
   - Decide whether they are authoritative latest pointers or should move to tmp/quarantine/ignored paths.

4. Active engineering substrate
   - New schemas, scripts, tests, templates, validators, and current workflow docs.
   - Usually keep; add drift-lock tests or an index rather than deleting.

5. Handoff/planning sprawl
   - Dated strategy/review files may be useful but need lifecycle labels: active, reference, superseded, archived, debug/transient.
   - Prefer a current-artifact index over deleting old review context.

6. Ignored bulk
   - Logs, scans, browser profiles, local tool acquisitions, raw caches, worker logs, evidence directories.
   - Verify with `git check-ignore -v`; if ignored and storage is acceptable, do not treat as repo pollution.
   - If disk pressure matters, archive/compress whole run directories rather than deleting individual duplicate evidence files.

7. Duplicate groups
   - Many duplicates in evidence/cache directories are expected provenance artifacts.
   - Deduplicate manually only for clearly generated cache, never for proof/evidence without a retention decision.

## Suggested safe commands

Use project-appropriate tools, but the sequence is:

```bash
git status --short
git rev-parse --show-toplevel
# Summarize files/sizes by top directory with a script, excluding .git and common caches.
# Check ignore status for representative bulk paths:
git check-ignore -v <path1> <path2> ... 2>&1 || true
```

For line/language composition, use the main `pygount` flow in this skill, but for redundant-file inventory also calculate:

- file count and size by top-level directory;
- largest files under handoff/docs;
- potential transient filename patterns (`*tmp*`, `*_stdout*.json`, `*_status*.json`, dated draft outputs, logs);
- duplicate hash groups for small/medium files;
- dated handoff prefix counts.

## Report format

Write a read-only inventory artifact when the repo uses handoff files. Include:

- status: read-only inventory / no deletion performed;
- scope path;
- route/tool and visible model/runtime if relevant;
- executive summary;
- top-level size/file-count table;
- git status noise classes;
- concrete P0 cleanup candidates;
- files/directories not to delete yet;
- recommended cleanup plan.

## Cleanup ordering

Recommended order:

1. Classify root transients and handoff debug JSON.
2. Review modified tracked files before any reset/deletion.
3. Create/update a current-artifact index with active/reference/superseded/local-only/debug labels.
4. Patch `.gitignore` only for recurring, clearly transient patterns.
5. Add an append/prepend helper for large append-only handoff logs if manual edits are risky.
6. Define retention/archive policy for ignored bulk directories.
7. Only then perform deletion/move/archive with explicit scope.

## Pitfalls

- Do not delete evidence/cache directories because they are large; first determine retention and sensitivity.
- Do not treat untracked strategy files as junk; they may be accepted project truth not yet committed.
- Do not inspect or summarize secrets, cookies, loot, tokens, raw private scope, or sensitive evidence in detail. Classify paths and risk only.
- Do not flatten all old reviews into one summary without preserving named artifacts or superseded/reference labels.
