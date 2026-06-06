> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Windows Git-Bash PR comments and repo handoff artifacts

Use this reference when a repository workflow includes local handoff files and GitHub PR tracking from a Windows host where the terminal is Git-Bash/MSYS.

## Problem pattern

Inline `gh pr comment --body "..."` is fragile when the body contains Markdown backticks, `$variables`, command-looking snippets, or multi-line content. Bash/MSYS can treat backticks as command substitution before `gh` receives the text, causing silently mangled PR comments.

## Safe pattern

1. Write the comment body to a temporary tracked-or-untracked Markdown file.
2. Post it with `gh pr comment <PR> --body-file <file>`.
3. Remove the temporary body file if it is only a posting helper.
4. Read back the last comment or use the returned URL to verify Markdown/backticks survived.
5. If a malformed duplicate exists, delete it by issue-comment id with `gh api -X DELETE repos/OWNER/REPO/issues/comments/COMMENT_ID`.

Example:

```bash
cat > /tmp/pr-comment.md <<'EOF'
Workflow cleanup committed and pushed.

Commit: e2095a4 (`fix: archive rolling handoff files`)
Branch: `feat/example-branch`
EOF

gh pr comment 1 --body-file /tmp/pr-comment.md
rm -f /tmp/pr-comment.md
gh pr view 1 --json comments --jq '.comments[-1] | {url,author:.author.login,body}'
```

## Handoff artifact discipline before PR updates

When a repo uses rolling handoff files such as `handoff/claude_code_task.md` / `handoff/claude_code_result.md`, treat those as convenience pointers. Before pushing and commenting, confirm audit-important work also has stable named artifacts, e.g. `handoff/claude_code_task_p3_6.md` and `handoff/claude_code_result_p3_6.md`, or that the repo's own helper archives rolling files automatically.

Before commit/push:

```bash
git status --short --branch
git diff --cached --check
# Run repo-specific review, e.g. HACKLAB=/path ./bin/hermes review
# Run a staged safety scan for secrets / forbidden target-touching surfaces if the repo is security-sensitive.
```

After push:

```bash
git status --short --branch
gh pr checks <PR> || true
```
