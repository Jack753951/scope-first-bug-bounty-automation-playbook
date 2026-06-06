> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Safe Private Repo Bootstrap From an Existing Workspace

Use this reference when pushing an already-developed local workspace to a new private GitHub repo, especially if the tree may contain logs, scan output, machine config, keys, generated reports, caches, or notes.

## Preflight

```bash
GH=${GH:-gh}  # or full path, e.g. '/c/Program Files/GitHub CLI/gh.exe'
$GH auth status 2>&1 | sed -E 's/(Token: ).*/\1[REDACTED]/'
git rev-parse --is-inside-work-tree 2>/dev/null || git init -b main 2>/dev/null || git init
git remote -v 2>/dev/null || true
```

## Harden `.gitignore` before staging

For security / lab / automation workspaces, strongly consider ignoring:

```gitignore
# worker/runtime state
.agent.lock
handoff/latest_check.md
handoff/worker_logs/

# caches/dependencies
__pycache__/
*.py[cod]
.pytest_cache/
node_modules/

# local machine config / keys
setting/local/
*.pem
*.key
id_rsa*
id_ed25519*
known_hosts

# logs, loot, scans, generated evidence/reports
logs/
loot/
scans/
kali-output/
reports/generated/
*.pcap
*.pcapng
*.cap
*.kdbx
creds*
credentials*

# env/secrets
.env
.env.*
*.secret
*secret*
*token*
```

Adapt names to the project. For non-security projects, the same principle applies: ignore local credentials, raw data, generated artifacts, and caches before the first `git add`.

## Verify ignores and staged candidates

```bash
# Check representative sensitive paths if present.
for p in setting/local/kali-ssh.json setting/local/ssh/kali_codex_ed25519 logs/audit.log scans/example/summary.md reports/generated/example/report.md node_modules; do
  [ -e "$p" ] || continue
  printf '%-80s ' "$p"
  git check-ignore -q "$p" && echo IGNORED || echo NOT_IGNORED
 done

# Dry-run candidate list respecting .gitignore.
git add -n . | sed -E "s/^add '//; s/'$//" > /tmp/candidate_files.txt

# Risky filenames should be empty or intentionally reviewed.
grep -Ei '(setting/local|logs/|scans/|loot/|node_modules|reports/generated|kali-output|\.env|\.pem|\.key|id_rsa|id_ed25519|pcap|\.cap$|kdbx|secret|token|credential)' /tmp/candidate_files.txt || true

# Obvious secret-content scan of candidate text files.
while IFS= read -r f; do
  [ -f "$f" ] || continue
  case "$f" in *.png|*.jpg|*.jpeg|*.gif|*.docx|*.sqlite|*.nbk) continue;; esac
  grep -InE '(BEGIN (RSA|OPENSSH|EC|DSA) PRIVATE KEY|gho_[A-Za-z0-9_]+|github_pat_[A-Za-z0-9_]+|AKIA[0-9A-Z]{16}|[A-Za-z0-9_]*(SECRET|TOKEN|PASSWORD|PRIVATE_KEY)[A-Za-z0-9_]*\s*=)' "$f" 2>/dev/null | sed "s#^#$f:#"
done < /tmp/candidate_files.txt | sed -n '1,100p'
```

Review any hit. Placeholder variable names in scripts may be fine; private keys/tokens are not.

## Create private repo, commit, push, verify

```bash
REPO=my-private-repo
DESC='Private project workspace.'
USER_LOGIN=$($GH api user --jq .login)
USER_ID=$($GH api user --jq .id)

git config user.name "$USER_LOGIN"
git config user.email "${USER_ID}+${USER_LOGIN}@users.noreply.github.com"
$GH auth setup-git >/dev/null

$GH repo view "$USER_LOGIN/$REPO" >/dev/null 2>&1 || \
  $GH repo create "$REPO" --private --description "$DESC" --disable-wiki

git remote get-url origin >/dev/null 2>&1 \
  && git remote set-url origin "https://github.com/$USER_LOGIN/$REPO.git" \
  || git remote add origin "https://github.com/$USER_LOGIN/$REPO.git"

git add .
git diff --cached --check
git commit -m 'Initial private project snapshot'
git push -u origin main

$GH repo view "$USER_LOGIN/$REPO" --json nameWithOwner,isPrivate,url,defaultBranchRef,pushedAt \
  --jq '{nameWithOwner,isPrivate,url,defaultBranch: .defaultBranchRef.name,pushedAt}'
git status --short --branch
```

## Pitfalls

- Do not rely on `--private` alone. Private repos can still expose secrets to collaborators, GitHub integrations, and future accidental visibility changes.
- Do not run `gh repo create --source . --push` before reviewing `.gitignore` and staged candidates.
- If `gh` is installed but Git-Bash cannot find it, use the full path for the current session rather than falling back to unauthenticated flows.
- Generated reports and scan artifacts can contain target details; ignore them by default and intentionally promote sanitized samples only.
