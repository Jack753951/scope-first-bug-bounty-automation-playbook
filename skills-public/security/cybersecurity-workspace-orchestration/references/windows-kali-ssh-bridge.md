> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Windows-to-Kali SSH Bridge Hardening

Use when a cybersecurity workspace runs on Windows/Git-Bash but delegates pentest tooling to a Kali VM over PowerShell + OpenSSH wrappers.

## Durable lessons

- Do not conclude Kali tools are unavailable just because Git-Bash, Windows, or WSL Ubuntu lacks them. Check the project bridge first (`scripts/kali-run.ps1`, `scripts/kali-check-tools.ps1`, `setting/local/kali-ssh.json`, or equivalent).
- Windows OpenSSH reads `%USERPROFILE%\.ssh\config` by default even when explicit host/user/key/port args are supplied. If a user config contains a UTF-8 BOM, SSH may fail with `Bad configuration option: \357\273\277host`. For wrappers, create a project-local empty config and pass `ssh.exe -F <empty_config>` to avoid unrelated user-config breakage.
- For multiline remote commands sent through PowerShell, prefer invoking the helper in-process with parameter splatting (`& $KaliRun @params`) rather than spawning nested `powershell.exe -File ... -Command <multiline>`, which can corrupt argument boundaries.
- Normalize CRLF command payloads to LF before running them through remote `bash -lc`; otherwise Kali/bash can see stray `\r` characters and misparse commands.
- Quote remote payloads explicitly for bash. A reusable PowerShell helper can single-quote values and replace embedded single quotes with the standard `'"]'"'` sequence. Keep this helper in the wrapper rather than hand-escaping every call.
- Expand remote output paths like `~/codex-output` to `/home/<user>/codex-output` before single-quoting. A quoted literal `~` will not tilde-expand in bash.
- Use setup-safe proofs such as `hostname`, `uname -a`, `/etc/os-release`, `command -v <tool>`, and `pgrep` for GUI/browser launch verification. Browser process proof is useful in CLI-only sessions when screenshots are unavailable.

## Safety boundary

Tool inventory, host identity checks, and wrapper dry-runs are setup checks. Scanning, brute force, exploitation, callbacks, and target-touching automation still require explicit authorization and scope from the cybersecurity orchestration skill.
