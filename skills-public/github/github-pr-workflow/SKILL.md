> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

---
name: github-pr-workflow
description: "GitHub PR lifecycle: branch, commit, open, CI, merge."
version: 1.1.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [GitHub, Pull-Requests, CI/CD, Git, Automation, Merge]
    related_skills: [github-auth, github-code-review]
---

# GitHub Pull Request Workflow

Complete guide for managing the PR lifecycle. Each section shows the `gh` way first, then the `git` + `curl` fallback for machines without `gh`.

## Prerequisites

- Authenticated with GitHub (see `github-auth` skill)
- Inside a git repository with a GitHub remote
- If the repo has a handoff/decision-log convention, treat GitHub as a workflow support layer rather than the only memory layer: update the repo handoff before/with PR work, and preserve any project-specific Obsidian or long-term strategy notes separately when the change affects future direction.

### Quick Auth Detection

```bash
# Determine which method to use throughout this workflow
if command -v gh &>/dev/null && gh auth status &>/dev/null; then
  AUTH="gh"
else
  AUTH="git"
  # Ensure we have a token for API calls
  if [ -z "$GITHUB_TOKEN" ]; then
    if [ -f ~/.hermes/.env ] && grep -q "^GITHUB_TOKEN=" ~/.hermes/.env; then
      GITHUB_TOKEN=$(grep "^GITHUB_TOKEN=" ~/.hermes/.env | head -1 | cut -d= -f2 | tr -d '\n\r')
    elif grep -q "github.com" ~/.git-credentials 2>/dev/null; then
      GITHUB_TOKEN=$(grep "github.com" ~/.git-credentials 2>/dev/null | head -1 | sed 's|https://[^:]*:\([^@]*\)@.*|\1|')
    fi
  fi
fi
echo "Using: $AUTH"
```

### Extracting Owner/Repo from the Git Remote

Many `curl` commands need `owner/repo`. Extract it from the git remote:

```bash
# Works for both HTTPS and SSH remote URLs
REMOTE_URL=$(git remote get-url origin)
OWNER_REPO=$(echo "$REMOTE_URL" | sed -E 's|.*github\.com[:/]||; s|\.git$||')
OWNER=$(echo "$OWNER_REPO" | cut -d/ -f1)
REPO=$(echo "$OWNER_REPO" | cut -d/ -f2)
echo "Owner: $OWNER, Repo: $REPO"
```

---

## 1. Branch Creation

This part is pure `git` — identical either way:

```bash
# Make sure you're up to date
git fetch origin
git checkout main && git pull origin main

# Create and switch to a new branch
git checkout -b feat/add-user-authentication
```

Branch naming conventions:
- `feat/description` — new features
- `fix/description` — bug fixes
- `refactor/description` — code restructuring
- `docs/description` — documentation
- `ci/description` — CI/CD changes

## 2. Making Commits

Use the agent's file tools (`write_file`, `patch`) to make changes, then commit:

```bash
# Stage specific files
git add src/auth.py src/models/user.py tests/test_auth.py

# Commit with a conventional commit message
git commit -m "feat: add JWT-based user authentication

- Add login/register endpoints
- Add User model with password hashing
- Add auth middleware for protected routes
- Add unit tests for auth flow"
```

### Repository cleanup / commit batching pattern

When a repo has many mixed modified/untracked artifacts and the user asks to "clean up until you need me", be active but conservative:

1. Inspect and group changes by durable intent before committing: code/fixtures, policy docs, handoff/review records, quarantine/archive moves, and accidental generated artifacts.
2. Stage explicit paths or directories for one coherent batch at a time; avoid `git add .` until you have inspected the status and know no generated/sensitive artifacts are included.
3. Run `git diff --cached --check` before each commit.
4. Run a lightweight staged-diff scan for secrets, dangerous execution patterns, and unintended live target URLs. Treat findings as blockers unless clearly synthetic/test/example data.
5. Run the project’s local review/test gate before committing substantial batches. If the repo provides a wrapper like `./bin/hermes review`, use it after tests and again at the end.
6. Commit with a conventional message per batch, then re-check `git status --short` and continue until clean or until a real operator decision is needed.
7. If a package manager installed generated directories or dependency metadata that are not part of the intended change, remove/restore them explicitly (for example, restore accidental `package.json` dependency additions and delete untracked `node_modules/`) after checking they are generated artifacts.

Useful commands for this cleanup loop:

```bash
git status --short
git diff -- <paths> | sed -n '1,220p'
git add <explicit paths>
git diff --cached --check
# Run repo-specific tests/review here, e.g. python -m unittest discover ... && ./bin/hermes review
git commit -m "docs: archive review handoff records"
git status --short
```

Commit message format (Conventional Commits):
```
type(scope): short description

Longer explanation if needed. Wrap at 72 characters.
```

Types: `feat`, `fix`, `refactor`, `docs`, `test`, `ci`, `chore`, `perf`

## 3. Pushing and Creating a PR

### Push the Branch (same either way)

```bash
git push -u origin HEAD
```

### Create the PR

**With gh:**

```bash
gh pr create \
  --title "feat: add JWT-based user authentication" \
  --body "## Summary
- Adds login and register API endpoints
- JWT token generation and validation

## Test Plan
- [ ] Unit tests pass

Closes #42"
```

Options: `--draft`, `--reviewer user1,user2`, `--label "enhancement"`, `--base develop`

**With git + curl:**

```bash
BRANCH=$(git branch --show-current)

curl -s -X POST \
  -H "Authorization: token $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  https://api.github.com/repos/$OWNER/$REPO/pulls \
  -d "{
    \"title\": \"feat: add JWT-based user authentication\",
    \"body\": \"## Summary\nAdds login and register API endpoints.\n\nCloses #42\",
    \"head\": \"$BRANCH\",
    \"base\": \"main\"
  }"
```

The response JSON includes the PR `number` — save it for later commands.

To create as a draft, add `"draft": true` to the JSON body.

### Commenting safely from shells

When posting PR comments that contain Markdown inline code, backticks, `$variables`, or multi-line content, do not pass the body directly in a shell-quoted `--body "..."` string. Bash/MSYS will interpret unescaped backticks and can silently strip or execute parts of the comment. Instead, write the body to a temporary file and use `--body-file`, then verify the rendered comment and delete any malformed duplicate:

```bash
cat > /tmp/pr-comment.md <<'EOF'
P3.6 artifacts committed and pushed.

Commit: c60d3d1 (`docs: align periodic reviews with decision policy`)
Branch: `origin/feature-branch`
EOF

gh pr comment 1 --body-file /tmp/pr-comment.md
rm -f /tmp/pr-comment.md

# If a malformed comment was posted, delete it by comment id:
gh api -X DELETE repos/OWNER/REPO/issues/comments/COMMENT_ID
```

This is especially important on Windows hosts where Hermes terminal uses bash/MSYS: inline backticks in `gh pr comment --body "..."` are command substitution. The same problem occurs with unquoted heredocs (`<<EOF`) used to build body files: Markdown backticks and `$variables` are expanded while the file is being written. Use a single-quoted heredoc delimiter (`<<'EOF'`), placeholder replacement for dynamic values, and prefer a repo-local temp file over `/tmp/...` when Windows Python might touch the file. If a malformed comment is posted, delete it by comment id and repost. For a copy-pasteable safe pattern, see `references/windows-gitbash-safe-pr-body-files.md`. For repos with local handoff artifacts, also confirm audit-important rolling files have stable named copies or archive coverage before posting the PR update; see `references/windows-gitbash-pr-comments-and-handoff.md`.

### Updating an existing PR after a scoped follow-up

When the user asks to “update GitHub status” after a follow-up on a dirty long-running branch, do not assume the whole working tree belongs in the update:

1. Inspect `git status --short`, current branch, remote, auth, and existing PR (`gh pr list --head <branch>` or `gh pr view`).
2. Stage only the files for the completed scope; avoid `git add .` when unrelated modified/untracked artifacts exist.
3. Run local validation first, then `git diff --cached --check` and a lightweight staged secret/safety scan before committing. For generated media/QA packets, inspect `git diff --cached --name-status` and `--stat` after staging: `.gitignore` may intentionally omit large local render outputs (`.mp4`, `.wav`, generated `.png`), so PR comments must accurately distinguish committed packet metadata/contact sheets/specs from ignored local binaries.
4. Commit and push the scoped batch.
5. Update GitHub in two channels:
   - `gh pr comment N --body-file /tmp/status.md` with commit, validation, and safety notes.
   - `gh pr edit N --title ... --body-file /tmp/pr-body.md` when the PR title/body no longer reflect the current branch scope.
6. Verify with `gh pr view N --json number,title,state,url,headRefName,baseRefName,mergeable,statusCheckRollup` and `gh pr checks N`.
7. In the final report, explicitly distinguish committed/pushed files from unrelated pre-existing working-tree changes.

Use temp files for both comment and body updates so Markdown code spans, backticks, and `$variables` survive shell quoting.

## 4. Monitoring CI Status

### Check CI Status

**With gh:**

```bash
# One-shot check
gh pr checks

# Watch until all checks finish (polls every 10s)
gh pr checks --watch
```

**With git + curl:**

```bash
# Get the latest commit SHA on the current branch
SHA=$(git rev-parse HEAD)

# Query the combined status
curl -s \
  -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/$OWNER/$REPO/commits/$SHA/status \
  | python3 -c "
import sys, json
data = json.load(sys.stdin)
print(f\"Overall: {data['state']}\")
for s in data.get('statuses', []):
    print(f\"  {s['context']}: {s['state']} - {s.get('description', '')}\")"

# Also check GitHub Actions check runs (separate endpoint)
curl -s \
  -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/$OWNER/$REPO/commits/$SHA/check-runs \
  | python3 -c "
import sys, json
data = json.load(sys.stdin)
for cr in data.get('check_runs', []):
    print(f\"  {cr['name']}: {cr['status']} / {cr['conclusion'] or 'pending'}\")"
```

### Poll Until Complete (git + curl)

```bash
# Simple polling loop — check every 30 seconds, up to 10 minutes
SHA=$(git rev-parse HEAD)
for i in $(seq 1 20); do
  STATUS=$(curl -s \
    -H "Authorization: token $GITHUB_TOKEN" \
    https://api.github.com/repos/$OWNER/$REPO/commits/$SHA/status \
    | python3 -c "import sys,json; print(json.load(sys.stdin)['state'])")
  echo "Check $i: $STATUS"
  if [ "$STATUS" = "success" ] || [ "$STATUS" = "failure" ] || [ "$STATUS" = "error" ]; then
    break
  fi
  sleep 30
done
```

## 5. Auto-Fixing CI Failures

When CI fails, diagnose and fix. This loop works with either auth method.

### Step 1: Get Failure Details

**With gh:**

```bash
# List recent workflow runs on this branch
gh run list --branch $(git branch --show-current) --limit 5

# View failed logs
gh run view <RUN_ID> --log-failed
```

**With git + curl:**

```bash
BRANCH=$(git branch --show-current)

# List workflow runs on this branch
curl -s \
  -H "Authorization: token $GITHUB_TOKEN" \
  "https://api.github.com/repos/$OWNER/$REPO/actions/runs?branch=$BRANCH&per_page=5" \
  | python3 -c "
import sys, json
runs = json.load(sys.stdin)['workflow_runs']
for r in runs:
    print(f\"Run {r['id']}: {r['name']} - {r['conclusion'] or r['status']}\")"

# Get failed job logs (download as zip, extract, read)
RUN_ID=<run_id>
curl -s -L \
  -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/$OWNER/$REPO/actions/runs/$RUN_ID/logs \
  -o /tmp/ci-logs.zip
cd /tmp && unzip -o ci-logs.zip -d ci-logs && cat ci-logs/*.txt
```

### Step 2: Fix and Push

After identifying the issue, use file tools (`patch`, `write_file`) to fix it:

```bash
git add <fixed_files>
git commit -m "fix: resolve CI failure in <check_name>"
git push
```

### Step 3: Verify

Re-check CI status using the commands from Section 4 above.

### Auto-Fix Loop Pattern

When asked to auto-fix CI, follow this loop:

1. Check CI status → identify failures
2. Read failure logs → understand the error
3. Use `read_file` + `patch`/`write_file` → fix the code
4. `git add . && git commit -m "fix: ..." && git push`
5. Wait for CI → re-check status
6. Repeat if still failing (up to 3 attempts, then ask the user)

## 6. Merging

**With gh:**

```bash
# Squash merge + delete branch (cleanest for feature branches)
gh pr merge --squash --delete-branch

# Enable auto-merge (merges when all checks pass)
gh pr merge --auto --squash --delete-branch
```

**With git + curl:**

```bash
PR_NUMBER=<number>

# Merge the PR via API (squash)
curl -s -X PUT \
  -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/$OWNER/$REPO/pulls/$PR_NUMBER/merge \
  -d "{
    \"merge_method\": \"squash\",
    \"commit_title\": \"feat: add user authentication (#$PR_NUMBER)\"
  }"

# Delete the remote branch after merge
BRANCH=$(git branch --show-current)
git push origin --delete $BRANCH

# Switch back to main locally
git checkout main && git pull origin main
git branch -d $BRANCH
```

Merge methods: `"merge"` (merge commit), `"squash"`, `"rebase"`

### Enable Auto-Merge (curl)

```bash
# Auto-merge requires the repo to have it enabled in settings.
# This uses the GraphQL API since REST doesn't support auto-merge.
PR_NODE_ID=$(curl -s \
  -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/$OWNER/$REPO/pulls/$PR_NUMBER \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['node_id'])")

curl -s -X POST \
  -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/graphql \
  -d "{\"query\": \"mutation { enablePullRequestAutoMerge(input: {pullRequestId: \\\"$PR_NODE_ID\\\", mergeMethod: SQUASH}) { clientMutationId } }\"}"
```

## 7. Complete Workflow Example

```bash
# 1. Start from clean main
git checkout main && git pull origin main

# 2. Branch
git checkout -b fix/login-redirect-bug

# 3. (Agent makes code changes with file tools)

# 4. Commit
git add src/auth/login.py tests/test_login.py
git commit -m "fix: correct redirect URL after login

Preserves the ?next= parameter instead of always redirecting to /dashboard."

# 5. Push
git push -u origin HEAD

# 6. Create PR (picks gh or curl based on what's available)
# ... (see Section 3)

# 7. Monitor CI (see Section 4)

# 8. Merge when green (see Section 6)
```

## Related references

- `references/repo-cleanup-batching.md` — compact playbook for mixed working-tree cleanup, staged-diff safety scans, accidental dependency artifacts, and final verification before reporting clean status.
- `references/scoped-pr-status-updates.md` — follow-up PR update pattern for dirty long-running branches: stage only scoped files, commit/push, comment/edit PR with temp files, verify checks, and report unrelated dirty state honestly. When the scoped change alters runtime semantics, run adjacent suites and update older assertions in the same scoped commit so full discovery stays green before posting the PR comment.
- `references/generated-media-pr-batching.md` — product/video branches with lots of generated media or visual-QA artifacts: commit durable code/docs/spec metadata separately, exclude local render outputs unless explicitly requested, and report committed vs uncommitted artifacts clearly.
- `references/windows-gitbash-safe-pr-body-files.md` — safe `gh pr comment` / `gh pr edit --body-file` patterns for Windows Git-Bash/MSYS: quoted heredocs, placeholder replacement, repo-local temp files, verification, and deleting malformed comments.

## Useful PR Commands Reference

| Action | gh | git + curl |
|--------|-----|-----------|
| List my PRs | `gh pr list --author @me` | `curl -s -H "Authorization: token $GITHUB_TOKEN" "https://api.github.com/repos/$OWNER/$REPO/pulls?state=open"` |
| View PR diff | `gh pr diff` | `git diff main...HEAD` (local) or `curl -H "Accept: application/vnd.github.diff" ...` |
| Add comment | Prefer `gh pr comment N --body-file /tmp/comment.md` for Markdown/backticks; use `--body "..."` only for plain text | `curl -X POST .../issues/N/comments -d @body.json` |
| Request review | `gh pr edit N --add-reviewer user` | `curl -X POST .../pulls/N/requested_reviewers -d '{"reviewers":["user"]}'` |
| Close PR | `gh pr close N` | `curl -X PATCH .../pulls/N -d '{"state":"closed"}'` |
| Check out someone's PR | `gh pr checkout N` | `git fetch origin pull/N/head:pr-N && git checkout pr-N` |
