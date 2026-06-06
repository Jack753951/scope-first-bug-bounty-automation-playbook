> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Safe public repo export from private workspaces

Use this when the user wants to publish selected artifacts from a private/local project into a public GitHub repo, especially when the source workspace contains handoffs, local lab notes, operational runbooks, generated artifacts, tokens, or agent skills.

## Core pattern

1. Treat the source workspace as private by default. Do not copy raw handoff folders, local skill folders, logs, scan outputs, or generated artifacts directly into a public repo.
2. Create a public-clean export layer first, for example:

```text
public_exports/
  docs/
  templates/
  skills/<skill-name>/SKILL.md
  tools/
```

3. Stage from `public_exports/` into the target repo, not from the private source paths. If a temporary staging script exists, it should be a collector/checker, not a publisher.
4. Keep publication as a separate human-visible step: `git diff`, review, commit, push. Do not make the stager call `git push` by default.

## Fail-closed staging script requirements

A public stager should:

- Default to a staging folder, not the real repo.
- If `-TargetRoot` points at an existing repo, confirm `git remote -v` mentions the intended repo name before writing.
- Refuse to overwrite existing files unless an explicit flag such as `-OverwriteFiles` is passed.
- Copy only explicitly selected files; avoid recursive folder copies from private runbooks or local skill `references/` unless each reference is allowlisted and cleaned.
- Write a `PUBLIC_SAFETY_REPORT.md` with file, line, pattern, and text for every hit.
- Exit non-zero on safety hits unless an explicit override such as `-AllowSanityHits` is passed.
- Exclude its own staging notes/report files from the scan to avoid self-inflicted false positives.

## High-signal safety patterns to scan before public push

Use project-specific patterns plus generic sensitive indicators. Common patterns from private agent/cybersec workspaces:

```text
Owner\\
Desktop\\<private-project>
<private repo/project names>
scope\.txt
192\.168\.
GHSA-
CVE-20
client_secret
token\.json
kali-output
private VM names
loot/
BEGIN (RSA |OPENSSH |EC |DSA )?PRIVATE KEY
gh[pousr]_[A-Za-z0-9_]+
sk-[A-Za-z0-9_-]{20,}
refresh_token
access_token
```

Not every hit is a secret; some are safe prose such as "do not commit tokens". For public reputation work, prefer rewriting to generic terms (`provider credential files`, `local auth tokens`, `<project-root>`) instead of relying on reviewers to understand every false positive.

## What tends to be reputation-positive and safer to publish

Best first public batch:

- General multi-agent collaboration policy.
- Memory governance / project handoff hygiene.
- Authorization-first lab safety contract, with private VM names and network details removed.
- Authorized live-target dry-run / intake template.
- AI resource routing and periodic review process, rewritten as generic guidance.
- Public-clean skill `SKILL.md` files that describe methodology without private operational history.

Avoid publishing raw:

- Private handoff files with project state, target names, exact lab IPs, CVE/GHSA attempts, or artifact paths.
- Local skill `references/` directories containing session-specific runbooks.
- Scope files, loot, scans, logs, token/client files, channel configs, generated media/data, or evidence bundles.

## PowerShell implementation pitfall

When truncating matched lines in a report, compute substring length from the cleaned string, not the original line:

```powershell
$cleanLine = ($m.Line.Trim() -replace '\s+', ' ')
$text = $cleanLine.Substring(0, [Math]::Min(160, $cleanLine.Length))
```

Using `$m.Line.Length` after `Trim()` can overrun if the original line had leading/trailing whitespace.

## Review posture

If the scan fails, that is success: the gate prevented an unsafe public push. Next action is to produce public-clean source files or rewrite flagged text, not to weaken the gate. A script that stages successfully but exits non-zero on hits is acceptable and desirable for public-export workflows.
