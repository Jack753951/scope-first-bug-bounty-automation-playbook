> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Windows cron gateway + mandatory multi-party review

Use when configuring Hermes cron jobs on Windows, especially recurring project-health / third-party review jobs.

## Durable lessons

### Windows gateway install fallback

`hermes gateway install` on Windows normally creates a Scheduled Task. On some systems `schtasks /Create` can fail with localized Access Denied output, for example Traditional Chinese:

```text
錯誤: 存取被拒。
```

If Hermes does not automatically fall back to the Startup folder, create the login fallback explicitly:

1. Generate the gateway wrapper script using Hermes' Windows gateway helper, or inspect the existing path:
   `C:\Users\<user>\AppData\Local\hermes\gateway-service\Hermes_Gateway.cmd`
2. Add a Startup-folder launcher:
   `C:\Users\<user>\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\Hermes_Gateway.cmd`
3. The Startup launcher should run the wrapper minimized, e.g.:

```bat
@echo off
rem Hermes Agent Gateway - Messaging Platform Integration
start "" /min cmd.exe /d /c C:\Users\<user>\AppData\Local\hermes\gateway-service\Hermes_Gateway.cmd
```

The wrapper should set `HERMES_HOME`, `PYTHONIOENCODING=utf-8`, `HERMES_GATEWAY_DETACHED=1`, `VIRTUAL_ENV`, cd into the Hermes agent install, and run:

```bat
C:\Users\<user>\AppData\Local\hermes\hermes-agent\venv\Scripts\python.exe -m hermes_cli.main gateway run --replace
```

Verify with:

```powershell
hermes gateway status
hermes cron status
```

Expected meaning:
- Gateway running manually means cron fires only while that process survives.
- Startup-folder fallback means gateway starts on Windows login.
- Hermes cannot power on a fully shut down PC; RTC wake/Wake-on-LAN/Windows wake timers are separate OS/firmware setup.

### Localized schtasks fallback patch

If maintaining Hermes source, `_FALLBACK_PATTERNS` in `hermes_cli/gateway_windows.py` should recognize localized access-denied strings, not only English. Useful variants include:

```python
r"(access is denied|access denied|acceso denegado|存取被拒|拒绝访问|schtasks timed out|schtasks produced no output)"
```

Also watch for Windows codepage/Unicode decode noise when reading `schtasks` output. Treat the durable fix as localized fallback detection or robust decoding, not as a claim that Scheduled Tasks are broken.

## Mandatory multi-party cron review pattern

Recurring review cron jobs can silently degrade into single-agent reviews unless the prompt and toolsets force real delegation.

For any cron job named/positioned as `third-party review`, `deep system review`, project-health review, or gated content/automation review:

1. Enable the `delegation` toolset in `enabled_toolsets` in addition to the normal `terminal`, `file`, and `skills` toolsets.
2. Add a prompt preamble requiring an actual `delegate_task` call with three independent reviewer tasks. Do not allow simulated role-play inside one Hermes response to count as multi-party review.
3. Require role separation appropriate to the repo:
   - Strategy/Cowork reviewer: goal drift, active lane, handoff durability, next-step value.
   - Engineering/Codex reviewer: repo/test/handoff evidence, script structure, verification, technical debt.
   - Safety/Governance reviewer: scheduler, upload/publish, OAuth/token, default privacy, scope/target-touching, secrets/loot boundaries.
4. Require the final Hermes synthesis to compare reviewer outputs, name disagreements/gaps, and produce a clear decision: `CONTINUE`, `REVISE`, `PAUSE`, `ESCALATE`, or `BLOCKED`.
5. If delegation is unavailable, times out, or lacks evidence, the final output must explicitly say the three-party review was incomplete. Never claim multi-party review without reviewer summaries.
6. Keep side-effect boundaries stricter than the review gate. A review gate does not authorize publish/upload/scheduler/OAuth/scope/target-touching changes.

Suggested prompt preamble:

```text
MANDATORY THREE-PARTY CROSS-REVIEW GATE — DO NOT SKIP

This cron job must not degrade into a single Hermes-only review.

Required mechanism:
- You MUST call delegate_task with three independent reviewer tasks before producing the final user-facing answer. This is not simulated role-play inside one response.
- Give each reviewer the same concise evidence packet: job name/id, repo/workdir, required files read, relevant command outputs, safety boundaries, and the original job instructions below.
- If delegate_task is unavailable, times out, or any reviewer lacks evidence, final output MUST say: 「三方審查未完整完成」 and name the missing reviewer/evidence.
- Hermes final synthesis must compare the three reviewer outputs, resolve disagreements, and produce a clear decision: CONTINUE / REVISE / PAUSE / ESCALATE / BLOCKED.
```

## Verification checklist

After editing cron jobs:

```powershell
python -m json.tool C:\Users\<user>\AppData\Local\hermes\cron\jobs.json > $null
hermes cron list
hermes cron status
```

Confirm each target job shows:
- `prompt_preview` begins with the mandatory review gate.
- `enabled_toolsets` includes `delegation`.
- Schedules, workdirs, delivery targets, original skills, and safety boundaries were preserved.

If the gateway may have cached job state, restart it manually when safe:

```powershell
hermes gateway restart
```

If restart is blocked by approval or not desired, note that the next login/Startup fallback or gateway restart should reload the edited jobs file.
