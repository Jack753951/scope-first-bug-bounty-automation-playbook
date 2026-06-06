> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Windows gateway auto-start fallback

Use this when `hermes gateway install` fails on Windows while creating the Scheduled Task, especially localized errors such as Traditional Chinese `錯誤: 存取被拒。` from `schtasks /Create`.

## What happened

Hermes gateway cron jobs only fire while the gateway is running. On Windows, `hermes gateway install` normally creates an ONLOGON Scheduled Task. Some systems deny `schtasks /Create` for the current user. Hermes has a Startup-folder fallback, but localized `schtasks` messages may not match the fallback detector.

## Durable fix in Hermes source

In `hermes_cli/gateway_windows.py`, `_FALLBACK_PATTERNS` should recognize localized access-denied messages, not only English/Spanish. Include at least:

```python
_FALLBACK_PATTERNS = re.compile(
    r"(access is denied|access denied|acceso denegado|存取被拒|拒绝访问|schtasks timed out|schtasks produced no output)",
    re.IGNORECASE,
)
```

This lets `hermes gateway install` automatically choose the Startup-folder fallback when `schtasks` is blocked.

## Manual fallback if install still aborts

Create the generated gateway wrapper and Startup-folder launcher with Python from the Hermes venv:

```powershell
& "$env:LOCALAPPDATA\hermes\hermes-agent\venv\Scripts\python.exe" -c "from hermes_cli import gateway_windows as gw; s=gw._write_task_script(); e=gw._install_startup_entry(s); print('script=', s); print('startup_entry=', e)"
```

Expected files:

- Gateway wrapper: `%LOCALAPPDATA%\hermes\gateway-service\Hermes_Gateway.cmd`
- Login launcher: `%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\Hermes_Gateway.cmd`

Then verify:

```powershell
hermes gateway status
hermes cron status
```

Expected status should mention the Windows login item and show `Gateway is running — cron jobs will fire automatically`.

## Notes

- Startup-folder fallback starts Hermes after Windows login, not while the machine is fully powered off.
- Fully powered-off auto-start requires BIOS/UEFI RTC wake or Wake-on-LAN; Hermes alone cannot power on a shut-down host.
- If status commands print Python `UnicodeDecodeError` reader-thread traces while still reporting success, treat that as a separate Windows subprocess-output encoding bug, not as proof the gateway is down.
