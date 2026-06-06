> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

---
name: powershell-from-bash-on-windows
description: "Run Windows PowerShell scripts reliably from Git-Bash/MSYS-style terminal tools."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [windows]
metadata:
  hermes:
    tags: [Windows, PowerShell, Git-Bash, MSYS, CLI, Orchestration]
    related_skills: [hermes-agent, claude-code, codex]
---

# PowerShell from Bash on Windows

Use this when a terminal tool is running through Git-Bash/MSYS/bash on Windows but the project commands are written as PowerShell examples such as `powershell -File .\script.ps1`.

## Trigger

- Host is Windows, but shell syntax is POSIX/bash.
- A user gives a PowerShell command containing `.\script.ps1` or other backslash paths.
- A `powershell -File .\script.ps1` call fails with a message like the `-File` argument does not exist, even though the file is present.

## Reliable Pattern

1. Set the terminal `workdir` to the project root.
2. Convert the PowerShell script path from `.\script.ps1` to `./script.ps1` before running it from bash:

```bash
powershell -NoProfile -ExecutionPolicy Bypass -File './run_hermes_pipeline.ps1' -Mode full
```

3. For maximum robustness, use a native absolute Windows path when passing `-File`:

```bash
powershell -NoProfile -ExecutionPolicy Bypass -File '<user-home>
```

4. Use POSIX commands for shell-side checks (`ls`, `grep`, `cat`, `command -v`) rather than PowerShell builtins, unless they are inside the `powershell -Command` or `powershell -File` invocation.

5. After the script runs, read generated reports or logs to verify where the workflow stopped or completed.

6. When the user gives a block of several PowerShell wrapper invocations, run them sequentially from the project root with `./script.ps1` paths, preserving the user's order unless there is an obvious prerequisite failure. For Hermes-style worker pipelines, a good verification pass is: inspect the generated handoff/check markdown, validate JSON and script syntax when the project context requires it, run the project scan if network is available, then rerun the handoff check so `latest_check.md` points at newly generated artifacts. If `git status` reports `not a git repository`, record that fact and continue with file/report inspection rather than treating it as a blocker.

7. If the PowerShell wrapper orchestrates interactive/native CLIs (Codex, Claude Code, node-based CLIs), avoid treating stderr output as a PowerShell exception. Around the native CLI invocation, temporarily set `$ErrorActionPreference = "Continue"`, capture `$LASTEXITCODE`, then restore the previous preference. This preserves real exit codes while allowing benign/progress stderr.

```powershell
$oldErrorActionPreference = $ErrorActionPreference
$ErrorActionPreference = "Continue"
try {
    & $NativeExe @args 2>&1 | Tee-Object -FilePath $LogFile
    $workerExitCode = $LASTEXITCODE
} finally {
    $ErrorActionPreference = $oldErrorActionPreference
}
exit $workerExitCode
```

7. For Python project wrappers, do not trust `.venv\Scripts\python.exe` merely because the file exists. Add a `Test-Python` helper that actually executes the interpreter and checks the minimum supported version; prefer the venv only after it passes. Setup scripts may safely remove and recreate a broken venv. See `references/python-project-wrapper-hardening.md`.

8. For preflight/review scripts, run compile checks with absolute paths and capture compile output into the generated report/log. This makes agent-launched and scheduler-launched runs deterministic even when the current working directory differs.

9. If an AI CLI worker running inside a sandbox reports missing Python/ffmpeg or a broken venv, verify with a direct local PowerShell invocation before treating the result as authoritative. Run the project-local validation commands from the repository root, e.g. `powershell -NoProfile -ExecutionPolicy Bypass -File './run_codex_review.ps1'` and `powershell -NoProfile -ExecutionPolicy Bypass -File './run_agent.ps1' validate`. If local validation passes, record the mismatch as a sandbox/PATH limitation in the handoff report instead of telling the user to reinstall tools. When the workflow has durable handoff files such as `handoff/codex_review.md` and `handoff/accepted_changes.md`, update those files to replace the stale "blocked by missing Python" note with the successful local validation result, then rerun the preflight/handoff check so `handoff/latest_check.md` is current. Also test direct lightweight CLI entrypoints such as `python agent.py validate`; if direct startup fails because of unrelated heavy dependencies, fix the CLI import boundary with lazy imports rather than forcing all dependencies to be available for every command. For the YouTube agent project, the detailed command sequence and upload-free draft/render-QA loop are documented in `references/youtube-agent-hermes-pipeline.md`.

10. When helping a user set Windows environment variables from PowerShell, use the exact .NET call syntax with parentheses, commas, and quoted string arguments. The scope string `"User"` is literal and should not be replaced with the Windows username:

```powershell
[Environment]::SetEnvironmentVariable("ANTHROPIC_API_KEY", "sk-ant-...", "User")
$env:ANTHROPIC_API_KEY = [Environment]::GetEnvironmentVariable("ANTHROPIC_API_KEY", "User")
```

Explain that the first command persists the variable for the current Windows user, while the second reloads it into the current PowerShell process. If the user is in `cmd` or Git Bash, `$env:...` will not work; have them open Windows PowerShell or use shell-appropriate syntax. A running agent/session may not inherit newly-set User environment variables until restarted, so verify both in the user's fresh PowerShell and, when relevant, in the agent's own environment.

11. When adding project validation commands for automation, keep them read-only: parse configs, check lock files, verify tools/env/defaults, but do not generate, upload, call external APIs, change OAuth, mutate databases, or register schedules.

12. For PowerShell project wrappers that launch Python/Node tools and depend on User-scoped Windows API keys, import known User environment variables into the current Process before launching the runtime. This avoids telling the user to reinstall keys when `validate` can see User env vars but the already-running process cannot.

```powershell
function Import-UserEnvironmentVariable {
    param([string]$Name)
    if (-not [Environment]::GetEnvironmentVariable($Name, "Process")) {
        $value = [Environment]::GetEnvironmentVariable($Name, "User")
        if ($value) {
            [Environment]::SetEnvironmentVariable($Name, $value, "Process")
        }
    }
}

foreach ($name in @("ANTHROPIC_API_KEY", "PEXELS_API_KEY", "ELEVENLABS_API_KEY")) {
    Import-UserEnvironmentVariable $name
}
```

13. When diagnosing provider API keys in PowerShell wrappers, avoid exposing secrets. It is safe to report presence, length, and a short non-sensitive prefix only:

```powershell
$v = [Environment]::GetEnvironmentVariable("ANTHROPIC_API_KEY", "User")
if ($v) {
    "User ANTHROPIC_API_KEY present: yes, len=$($v.Length), starts=$($v.Substring(0,[Math]::Min(7,$v.Length)))"
} else {
    "User ANTHROPIC_API_KEY present: no"
}
```

If the wrapper imports User env vars successfully but the provider returns `401 invalid x-api-key`, the fix is to rotate/update the provider key, not to reinstall dependencies.

14. For PowerShell public-staging or safety-report scripts, prefer fail-closed behavior: write a line-level report, exit non-zero on unresolved hits, and require an explicit bypass flag for human-reviewed false positives. When truncating matched lines, compute substring length from the cleaned string rather than the original line so trimming whitespace cannot cause an out-of-range exception:

```powershell
$cleanLine = ($m.Line.Trim() -replace '\s+', ' ')
$text = $cleanLine.Substring(0, [Math]::Min(160, $cleanLine.Length))
```

For GitHub public-export workflow details, see `github-repo-management/references/safe-public-repo-export.md`. 

- In Git-Bash/MSYS, do not execute a `.ps1` wrapper directly as `./run_agent.ps1 status` or `./script.ps1`; bash will try to parse PowerShell syntax and fail with errors like `param([string]$PythonPath)` / `command not found`. Always invoke through PowerShell: `powershell -NoProfile -ExecutionPolicy Bypass -File './run_agent.ps1' status`.
- In Git-Bash/MSYS, `.\\run_hermes_pipeline.ps1` can be transformed or interpreted incorrectly and reach PowerShell as `.run_hermes_pipeline.ps1`. If that happens, retry with `./run_hermes_pipeline.ps1` or an absolute path.
- PowerShell wrappers that call native Node/TUI CLIs such as Codex or Claude Code may see banner/progress output on stderr. With `$ErrorActionPreference = "Stop"` plus `2>&1`, PowerShell can surface this as `NativeCommandError` even when the real success/failure signal is `$LASTEXITCODE`. Scope `$ErrorActionPreference = "Continue"` only around the native CLI call, capture output/logs, then restore strict mode and exit with `$LASTEXITCODE`.
- Do not record a one-time `command not found` or missing login as a durable environment fact. Capture the setup fix instead: install the CLI, log in, use a full executable path for the current session, or restart so PATH refreshes.
- After installing a Windows CLI via `winget`, the current Git-Bash/MSYS-based agent process may not inherit the updated PATH. Probe PowerShell with `Get-Command <tool>` and common install locations before concluding the tool is unavailable; if found, invoke the full `.exe` path from PowerShell for verification/setup.
- When quoting Windows paths for PowerShell from bash, prefer single quotes around the `-File` argument to avoid backslash interpretation.
- When using `powershell -Command` from bash/Git-Bash, wrap the whole PowerShell command in single quotes if it contains PowerShell variables such as `$vp`, `$mp`, `$approval`, or `$env:NAME`. If you use outer double quotes, bash expands `$vp`/`$mp` before PowerShell sees them, producing confusing commands like `=(Resolve-Path ...)` or missing `--video-path` arguments. Example:

```bash
powershell -NoProfile -ExecutionPolicy Bypass -Command '$vp=(Resolve-Path "data/.../final_short.mp4").Path; $mp=(Resolve-Path "data/.../metadata.json").Path; $approval="approve channel $vp private only no scheduler no public unlisted no active engine channel default"; & "./run_agent.ps1" upload-existing-private --channel channel --video-path $vp --metadata-path $mp --approval-phrase $approval'
```

- For VirtualBox hardening from Git-Bash, call the native VBoxManage executable by full path when it is not on PATH, e.g. `'/c/Program Files/Oracle/VirtualBox/VBoxManage.exe'`. On VirtualBox 7.x, runtime clipboard disabling uses `controlvm <vm> clipboard mode disabled` and `controlvm <vm> clipboard filetransfers off`; `controlvm <vm> clipboard disabled` is invalid. Use `controlvm <vm> draganddrop disabled` for drag-and-drop. For user-requested bidirectional clipboard/drag-and-drop on a running lab VM, use `controlvm <vm> clipboard mode bidirectional` and `controlvm <vm> draganddrop bidirectional`, then verify with `showvminfo --machinereadable | grep -E 'clipboard|draganddrop'`; if the guest still cannot paste, start `VBoxClient --clipboard` or reboot the guest. `modifyvm` may fail while the VM is running/locked, so use `controlvm` for runtime changes and repeat persistent `modifyvm` settings after shutdown. For CPU/RAM changes, gracefully power off first, apply `modifyvm --memory/--cpus`, then boot and verify from inside the guest with `free -m` and `nproc`. For lab VMs, do not disable NAT before setup downloads are complete: use setup mode with NAT for `apt`/Docker pulls, snapshot, then switch to isolated attack mode by disabling NAT and writable shared folders. When enabling temporary NAT on a running VM, verify both `nicN="nat"` and `cableconnectedN="on"`; if NAT is set but the guest interface is still down/unavailable, run `controlvm <vm> setlinkstateN on` and re-check guest `ip route`/DNS. Verify SSH or `guestcontrol` credentials before claiming you can install inside the guest; otherwise provide a script for the user to run inside the VM. For Kali shared-folder remounts, clipboard fixes, Docker group aftermath, VirtualBox `<inaccessible>` snapshot/differencing-disk triage, replacement attacker cloning, temporary NAT recovery, CPU/RAM baseline snapshots, local vulnerable-lab verification patterns, and Kali/Xfce auto-lock/DPMS disable via SSH, see `references/virtualbox-kali-lab-ops.md` and `references/kali-xfce-auto-lock-disable.md`.
- For live-target work that uses the project Kali/noVNC browser, first start the existing tunnel wrapper from Git-Bash with PowerShell, then open the local noVNC URL for the operator and, when appropriate, open the target page inside Kali via SSH rather than a separate agent browser session. If physical display `:0` is at LightDM or `x11vnc` fails with Xauthority/MIT-MAGIC-COOKIE errors, use the Xvfb/Xfce fallback in `references/kali-novnc-xvfb-fallback.md` and record that it is a fresh desktop/readiness checkpoint rather than preserved browser state:

```bash
powershell -NoProfile -ExecutionPolicy Bypass -File './scripts/kali-vnc-control.ps1' -Action start
ssh.exe -F setting/local/ssh/empty_ssh_config \
  -i setting/local/ssh/kali_codex_ed25519 \
  -p 22 \
  -o UserKnownHostsFile=setting/local/ssh/known_hosts \
  -o StrictHostKeyChecking=accept-new \
  kali@<lab-ip> \
  "mkdir -p /home/kali/browser-profiles/<program>-hermes && DISPLAY=:0 nohup chromium --user-data-dir=/home/kali/browser-profiles/<program>-hermes --no-first-run --new-window '<authorized-url>' >/tmp/hermes_<program>_chromium.log 2>&1 & echo opened_<program>_chromium_profile"
```

Use this only after scope/rules allow the target URL. Keep a separate browser profile per program to avoid mixing sessions. Do not perform CAPTCHA/OTP/email/phone/password/VM unlock for the operator; open the page, give the noVNC URL, and stop at those gates.
- Git-Bash/MSYS may rewrite Unix-looking paths passed to Windows executables, including `wsl.exe` and Windows-launched Python/PowerShell helpers that are generating remote Linux scripts. `/mnt/c/...` or `/home/kali/...` can become `C:/Program Files/Git/...` and then be embedded in the remote command/script incorrectly. For commands that intentionally pass Linux/remote paths through a Windows executable, prefix the command with a path-conversion exclusion such as `MSYS_NO_PATHCONV=1` or `MSYS2_ARG_CONV_EXCL='*'`, then inspect the generated script/config before copying it to the remote host. Examples:

```bash
MSYS_NO_PATHCONV=1 wsl.exe -d Ubuntu -- bash /mnt<user-home>
MSYS2_ARG_CONV_EXCL='*' python scripts/lab_modules/phase4b_get_only_metadata_probe.py --output-dir /home/kali/codex-output/run_id --write-script setting/local/run.sh
```
- When a bash pipeline mixes MSYS redirection paths with native Windows programs (for example redirecting `gh` output to `/tmp/file.md` and then reading it with Windows `python.exe` or passing it back to `gh.exe`), do not assume `/tmp/...` is the same path in both runtimes. Use a Windows-native temp path such as `<user-home>`, use `$TEMP` after verifying it is native, or convert with `cygpath -w/-u` before crossing the MSYS/native boundary. This avoids false `FileNotFoundError` / "file not found" failures during PR body edits and other CLI workflows.
- For PowerShell wrappers that SSH to Linux/Kali and pass multiline shell code, avoid nested `powershell.exe -File ... -Command <multiline>` when calling another local `.ps1`; invoke it in-process with parameter splatting (`& $Script @params`) so the multiline command remains one argument. In the SSH wrapper, normalize CRLF to LF, quote the payload for `bash -lc`, pass `ssh.exe -F <project_empty_config>` if the user's SSH config may be broken, and expand quoted remote `~/...` paths to `/home/<user>/...` before execution. See `cybersecurity-workspace-orchestration/references/windows-kali-ssh-bridge.md` for the remote-Kali case study.
- Windows OpenSSH reads the user's `%USERPROFILE%\.ssh\config` by default even when a script passes explicit host/user/key options. If `ssh.exe` fails with `Bad configuration option: \357\273\277host`, the SSH config has a UTF-8 BOM before `Host`. Either rewrite the config as UTF-8 without BOM, or for scripted probes create an empty project-local config and pass `ssh.exe -F <empty_config> ...` so a broken user config does not mask a valid remote connection. Do not conclude the remote tool bridge is unavailable until this has been checked.
- With `$ErrorActionPreference = "Stop"`, PowerShell can promote native stderr from commands like `node.exe`/Codex into `NativeCommandError`/`RemoteException`, aborting a wrapper before `$LASTEXITCODE` is recorded. Do not solve this by ignoring failures globally; scope `$ErrorActionPreference = "Continue"` narrowly around the native CLI call and still exit with `$LASTEXITCODE`.
- AI CLI workers may run with a narrower sandbox/PATH than the user's local PowerShell session. A worker report saying Python, `.venv`, ffmpeg, or ffprobe is missing can be a sandbox observation rather than the project state. Confirm using direct local validation before recommending setup_env/reinstall steps or writing "blocked" into final handoff files.
- PowerShell method calls such as `[Environment]::SetEnvironmentVariable(...)` require parentheses/comma syntax. Users often paste a space-separated form like `[Environment]::SetEnvironmentVariable ANTHROPIC_API_KEY sk-ant-...`, which produces `ParserError` / `UnexpectedToken` at `ANTHROPIC_API_KEY`. Correct the syntax rather than diagnosing the API key.
- Do not ask users to replace the literal scope string `"User"` with their username. In `[Environment]::SetEnvironmentVariable(name, value, "User")`, `"User"` means the Windows per-user environment variable target.
- After setting a User-scoped variable, the current PowerShell process may need `$env:NAME = [Environment]::GetEnvironmentVariable("NAME", "User")`; already-running agent processes may still not see it until restarted. If `$env:...` is "not recognized", the user is likely not in PowerShell.
- When a PowerShell-launched workflow reports an API `401` such as `invalid x-api-key`, distinguish credential presence from credential validity. Check User/Process scope and key shape without printing the secret (length and prefix only). If the key is present and shaped correctly but the provider rejects it, tell the user to rotate/update the provider key rather than rerunning setup or claiming the variable is missing.

## Verification

- Confirm the target `.ps1` exists with `ls` or `python -c` from the bash shell.
- Confirm the PowerShell script's own report/log file was updated.
- If a wrapper says it stopped, inspect the generated report before deciding whether to rerun or escalate.

## References

- `references/virtualbox-kali-xfce-auto-lock.md` — disable Kali/Xfce auto-lock, screen blanking, DPMS, and screensaver from the Windows control plane via the Kali SSH wrapper; use this when the user means the VM, not the Windows host.
- `references/windows-kali-scp-pull-symmetry.md` — when a Windows-to-Kali SSH wrapper uses project-local `-F empty_ssh_config`, patch the matching SCP artifact-pull wrapper to pass the same `-F` so a BOM-broken user SSH config cannot break result retrieval.
- See `references/youtube-agent-hermes-pipeline.md` for an example of this pattern in a Hermes pipeline wrapper.
- See `references/youtube-agent-upload-free-draft-review.md` for the youtube_agent local-only draft override + internal visual QA pattern.
- See `references/youtube-agent-stock-relevance-rung.md` for the upload-free stock-footage relevance policy pattern: script-level preferred/deny terms, `footage_relevance_report.json`, network-independent tests, and handoff recording.
- See `references/youtube-agent-readability-rung.md` for the upload-free media readability loop: hook-specific punctuation preservation, card contrast/font regressions, frame-strip QA, and handoff recording.
- See `references/youtube-agent-upload-free-modular-script-rungs.md` for the YouTube Agent modular script-engine rung pattern: draft-only overrides, Claude/Cowork read-only review, one-variable TDD changes, visual frame-strip QA, handoff updates, and verification bundle.
- See `references/youtube-agent-scheduler-sync.md` for synchronizing Windows Task Scheduler and Hermes cron with the YouTube Agent handoff gate: disabling stale `agent.py loop` production automation, preserving read-only canary jobs, verifying stale locks by PID, and recording the sync.
- See `references/youtube-agent-hermes-gateway-watchdog.md` for the Windows Scheduled Task watchdog pattern that keeps `hermes gateway run` alive so Hermes cron jobs actually fire, without duplicating production loops or enabling upload gates.
- See `references/youtube-agent-script-only-production-cron.md` for converting approved YouTube Agent production-loop cron jobs to Hermes `no_agent` script-only execution: repo-owned wrapper, fixed-channel Hermes scripts under `~/.hermes/scripts/`, dry-run verification, `deliver=local`, and paused upload-gate preservation.
- See `references/python-project-wrapper-hardening.md` for Python venv validation, absolute-path compile checks, and read-only validation-command design.
