> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Cross-OS shared-repo dirty tree cleanup

Use this when a Windows repo is mounted into a Linux/Kali guest via VirtualBox/shared-folder/symlink and the user asks to clean or commit a large dirty working tree.

## Pattern

1. Verify status from both surfaces before and after cleanup:
   - Windows host repo: `git status --short`
   - Linux/Kali guest shared path: `cd /mnt/<share> && git status --short`
   - If a symlink is part of the workflow, also verify it: `cd ~/projects/<repo> && git status --short`.
2. Classify changes before staging:
   - code/tests/fixtures
   - durable handoff/reports/notes
   - rolling pointer files
   - generated/transient run outputs
   - sensitive/no-commit areas
3. Prefer explicit path staging over `git add .` in long-lived workspaces with mixed historical artifacts.
4. Commit in coherent batches, e.g. code/tests first, then durable handoff/report records, then small tool fixes, then misplaced docs/briefs.
5. Run validation before final handoff:
   - `git diff --check`
   - focused or full tests appropriate to the repo
   - project review command, if present
   - lightweight added-line secret/danger scan when committing security-lab artifacts.
6. Re-check `git status --short` from every active surface after commits.

## CRLF false-dirty pitfall on Windows-hosted shares

When a Windows working tree is mounted into Linux/Kali, the guest may show many false modified files caused only by line-ending normalization. Symptoms include huge `git diff --stat` with near-equal additions/deletions and `git diff --word-diff=porcelain` lines ending in visible `\r` markers.

If the Windows host is clean but the Linux guest shows massive false modifications, check guest repo-local config:

```bash
cd /mnt/<share>
git config --get core.autocrlf || true
git diff --word-diff=porcelain -- <one-file> | sed -n '1,30p'
```

A practical repo-local fix for a Windows-hosted shared working tree is often:

```bash
cd /mnt/<share>
git config core.autocrlf true
git status --short
```

Do not commit CRLF-only churn. Normalize the guest's git config first, then continue cleanup only if real content changes remain.

## Safety note for cybersec labs

Do not stage `loot/`, secrets, credentials, private scope/rules, captures, broad raw scanner dumps, or target-sensitive artifacts. Handoff/report artifacts can be durable, but scanner output is triage unless manually verified and accepted by the project gate.
