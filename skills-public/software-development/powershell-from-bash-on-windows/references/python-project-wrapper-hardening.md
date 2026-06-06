> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Python project wrapper hardening

Use this reference when maintaining PowerShell entrypoints for a Python project that may be invoked from Git-Bash/MSYS, Hermes, Codex, Claude Code, or Task Scheduler.

## Durable pattern

PowerShell wrappers should not trust `.venv\Scripts\python.exe` only because the file exists. Stale virtual environments can point to a removed or broken base Python. Instead:

1. Implement a small `Test-Python` helper that executes a candidate interpreter.
2. Verify both viability and minimum version, e.g. Python 3.9+.
3. Prefer the project venv only after it passes the helper.
4. Fall back to `python` / `py -3` candidates if appropriate.
5. In setup scripts, if the venv exists but fails validation, remove and recreate it rather than silently continuing.

## Example PowerShell helper

```powershell
function Test-Python {
    param([string]$PythonPath)

    if (-not $PythonPath) { return $false }

    try {
        $code = 'import sys; raise SystemExit(0 if sys.version_info >= (3, 9) else 1)'
        & $PythonPath -c $code *> $null
        return ($LASTEXITCODE -eq 0)
    } catch {
        return $false
    }
}
```

## Compile / validation checks

For preflight wrappers, use absolute paths when invoking `py_compile` or project validation scripts. This avoids accidental reliance on the current working directory when the wrapper is launched by an agent, scheduler, or another script.

Capture compile stderr/stdout into the generated report so the next agent can diagnose without rerunning immediately.

## Safe validation command design

A project-level `validate` command is useful if it is explicitly read-only. Good checks include:

- parse channel/config JSON files
- verify required config fields are present
- check required environment variables and external tools
- confirm a lock file is absent before generation workflows
- assert conservative defaults such as private/unlisted publishing privacy

Avoid API calls, generation, uploads, database writes, scheduler changes, or OAuth mutations in validation commands.
