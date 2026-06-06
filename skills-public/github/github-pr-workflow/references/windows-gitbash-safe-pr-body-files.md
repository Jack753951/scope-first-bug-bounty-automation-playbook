> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Windows Git-Bash safe PR comments/body files

Use this when posting GitHub PR comments or editing PR bodies from Hermes on Windows Git-Bash/MSYS, especially when the Markdown contains backticks, `$VARIABLES`, command snippets, or file paths.

## Pitfall

An unquoted heredoc delimiter expands command substitutions and variables while creating the body file:

```bash
cat > /tmp/pr-comment.md <<EOF
Commit: abc123 (`docs: record thing`)
Path: `setting/local/...`
EOF
```

In bash, backticks are command substitution. This can execute local commands, strip inline code from the comment, create stray files, or paste command output into the PR comment.

## Safe pattern

1. Use a single-quoted heredoc delimiter so Markdown is literal.
2. If a runtime value is needed, use a placeholder and replace it afterward.
3. Prefer a repo-local temporary file over `/tmp/...` when a Windows Python interpreter may be used; Windows Python can interpret `/tmp/foo` as `\tmp\foo` and fail.
4. Post with `--body-file`, then verify the rendered comment.
5. If a malformed comment was posted, delete it by comment id and repost.

```bash
commit=$(git rev-parse --short HEAD)

cat > pr-update.tmp.md <<'EOF'
Phase update pushed.

Commit: COMMIT_PLACEHOLDER (`docs: record tool acquisition wave`)

Validation:
- PASS: `HACKLAB=<user-home> USER=Owner ./bin/hermes review`.
- Note: `jq` is not installed, so JSON validation was skipped.
EOF

python - <<PY
from pathlib import Path
p = Path('pr-update.tmp.md')
s = p.read_text(encoding='utf-8').replace('COMMIT_PLACEHOLDER', '$commit')
p.write_text(s, encoding='utf-8')
PY

gh pr comment 1 --body-file pr-update.tmp.md
rm -f pr-update.tmp.md
```

## Verify and repair

```bash
gh api repos/OWNER/REPO/issues/PR_NUMBER/comments \
  --jq '.[-1] | {id:.id,body:.body,url:.html_url}'

# If malformed:
gh api -X DELETE repos/OWNER/REPO/issues/comments/COMMENT_ID
```

## Notes

- The same pattern applies to `gh pr edit --body-file`.
- Do not pipe `gh api ... | python` for verification on Windows if the JSON may be empty or the pipe may close early; a simple `--jq` preview is usually enough.
