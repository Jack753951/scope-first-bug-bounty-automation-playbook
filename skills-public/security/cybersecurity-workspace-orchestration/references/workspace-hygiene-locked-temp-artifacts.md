> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Workspace hygiene: locked temp artifacts in cybersecurity repos

Use this when a cybersec workspace has a leftover temp directory such as `.tmp_recon_cli_<id>/` that pollutes `git status` or review output, but the agent cannot inspect it because Windows ACLs deny access.

## Principle

Treat unknown scan/recon/temp artifacts as potentially containing evidence, target data, or sensitive material until inspected. Do not `rm -rf`, force-delete, or take ownership from the agent just to quiet `git status`.

## Safe sequence

1. Perform read-only checks first:
   - confirm path exists and whether it is a directory
   - inspect metadata only when allowed
   - try `git status --short -- <path>` to see whether it is only status pollution
   - do not traverse contents if permission is denied

2. If the artifact pattern is a known transient workspace class, add a narrow ignore rule rather than deleting the locked object. Example:

```gitignore
.tmp_recon_cli_*/
```

Prefer a narrow project-specific pattern over broad `.tmp_*/` unless the repo already has that convention.

3. Verify the ignore rule removed the status/review pollution:

```bash
git status --short -- .gitignore .tmp_recon_cli_<id> 2>&1 | cat
```

Expected result: only `.gitignore` is reported; no permission warning for the locked temp path.

4. Run the project review/preflight wrapper if available. If the wrapper uses a different configured repo path and reports unrelated `not a git repo` or missing-scope messages, record that separately instead of treating the ignore change as the cause.

5. Ask the operator to inspect and delete only from an elevated/admin shell when necessary. Provide copy-pasteable PowerShell:

```powershell
cd <user-home>

Get-Item -LiteralPath .\.tmp_recon_cli_<id> -Force | Format-List *
icacls .\.tmp_recon_cli_<id>

takeown /F .\.tmp_recon_cli_<id> /A /R /D Y
icacls .\.tmp_recon_cli_<id> /grant Administrators:F /T
Get-ChildItem -LiteralPath .\.tmp_recon_cli_<id> -Force -Recurse
```

Delete only after confirming it contains no evidence, scans, loot, credentials, or reports:

```powershell
Remove-Item -LiteralPath .\.tmp_recon_cli_<id> -Recurse -Force
```

## Pitfalls

- Do not assume `mode 777` from MSYS/Git-Bash means Windows ACL access is actually available.
- If `icacls`, `Get-ChildItem`, or `takeown` fail with access denied/non-admin errors, stop at the ignore-rule hygiene fix and have the operator retry in an elevated PowerShell.
- Do not add broad ignore patterns that could hide important repo files or evidence by accident.
- Do not describe the cleanup as complete if the locked directory still exists; distinguish `git status pollution mitigated` from `artifact inspected/deleted`.
