> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Repository cleanup batching notes

Use this when a working tree has mixed accepted changes, review artifacts, generated files, and possible accidental package-manager output.

## Durable pattern

- Start from `git status --short`, then inspect diffs by path group.
- Prefer path-specific staging over `git add .`.
- Batch commits by intent:
  - quarantine/archive moves (`chore:`)
  - workflow/tooling changes (`feat:` or `fix:`)
  - validation fixtures and offline test harnesses (`feat:`)
  - handoff/review record archives (`docs:`)
- Before each commit:
  - `git diff --cached --check`
  - scan staged diff for obvious secrets/tokens/private keys
  - scan staged diff for dangerous exec patterns newly introduced
  - scan staged diff for unintended live URLs when working in security repos
  - run the repo-specific review/test command
- After each commit: `git status --short` and continue.

## Accidental dependency artifacts

If package-manager output appears without an explicit dependency change request:

1. Inspect `package.json`, lockfiles, and generated directories.
2. Search whether new dependencies are referenced by project source.
3. If not intended, restore metadata and remove generated directories, e.g.:

```bash
git restore -- package.json package-lock.json 2>/dev/null || true
rm -rf node_modules
```

Only delete recursively after confirming the path is a generated dependency directory, not project source.

## Final verification

End with:

```bash
<repo-specific tests>
<repo-specific review command>
git status --short
git log --oneline -8
```

Report the final clean/dirty status, validation commands, and commit list. If clean and tests/review pass, no operator decision is needed.