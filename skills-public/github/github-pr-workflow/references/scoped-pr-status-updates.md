> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Scoped PR status updates on dirty long-running branches

Use this when a user asks to update GitHub status after a follow-up but the working tree contains many unrelated modified/untracked files.

## Pattern

1. Confirm branch and PR:

```bash
git status --short
git branch --show-current
git remote -v
gh pr list --head "$(git branch --show-current)" --json number,title,state,url,headRefName,baseRefName,statusCheckRollup --limit 5
```

2. Stage only the completed scope:

```bash
git add path/one.py tests/test_one.py handoff/specific_artifact.md
```

Avoid `git add .` unless the whole tree was intentionally inspected and belongs to the PR.

For generated media/QA packets, never assume `git add packet_dir/` staged every file you intend to report. Repo `.gitignore` rules may silently omit large artifacts such as `.mp4`, `.wav`, `.png`, or generated intermediates. Immediately inspect staged files and sizes before validation:

```bash
git diff --cached --name-status -- packet_dir/ path/to/code.py tests/test_code.py
git diff --cached --stat -- packet_dir/ path/to/code.py tests/test_code.py
```

If the PR comment says a packet was committed, distinguish between committed metadata/contact sheets/specs and ignored local render outputs. Do not imply uploadable media binaries were committed when they were intentionally ignored.

3. Validate before commit:

```bash
# project-specific tests first
python -m unittest tests.test_relevant -v
python -m py_compile touched_module.py
# project-specific safety wrapper if present
powershell -NoProfile -ExecutionPolicy Bypass -File './run_agent.ps1' validate

git diff --cached --check
# lightweight staged scan; tune patterns to repo risk
 git diff --cached | grep -Ei 'AIza|gho_|ghp_|sk-|api[_-]?key|client_secret|token' || true
```

Treat real secrets as blockers. Mentions in handoff safety notes are usually not secrets, but still inspect before committing.

4. Commit and push:

```bash
git commit -m "feat: scoped status update"
git push -u origin HEAD
```

5. Update GitHub with temp files:

```bash
cat > /tmp/pr-status.md <<'EOF'
Status update

Commit: abc1234
Validation:
- tests: PASS
- project validate: PASS
Safety:
- no upload/publish/schedule/token changes
EOF

gh pr comment <PR_NUMBER> --body-file /tmp/pr-status.md

cat > /tmp/pr-body.md <<'EOF'
## Summary
- Current branch scope

## Validation
- tests: PASS

## Safety boundary
- no sensitive/runtime side effects
EOF

gh pr edit <PR_NUMBER> --title 'feat: current branch scope' --body-file /tmp/pr-body.md
```

6. Verify remote status:

```bash
gh pr view <PR_NUMBER> --json number,title,state,url,headRefName,baseRefName,mergeable,statusCheckRollup
gh pr checks <PR_NUMBER> || true
git log --oneline -n 3
git status --short
```

## Reporting rule

If the working tree is still dirty after the scoped push, say so clearly. Do not imply the repository is clean; say that the requested scope was committed/pushed and that other pre-existing artifacts remain uncommitted.
