> Public filtered Obsidian memory export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# DVWA Command Injection Impact Wave 1 2026-05-22

Status: completed / verified command execution + marker file; callback blocked
Repo handoff: `<user-home>`
Bundle: `<user-home>`
Artifacts: `<user-home>`

## What happened

A disposable DVWA container was launched on `<lab-vm>` and attacked from `<lab-vm>` through the command injection lesson.

Verified server-side command execution:

```text
uid=33(www-data) gid=33(www-data) groups=33(www-data)
www-data
DVWA_CMDINJ_dvwa_cmdinj_impact_wave1_20260522T052046Z
```

## Important distinction

Verified:
- command execution as `www-data`
- lab marker file write/readback under `/tmp`

Not verified:
- outbound callback; listener ports were blocked/unreachable

## Project benefit

This is the first max-impact style bundle that proves OS command execution identity rather than only app-level impact. It also reveals that callback/control drills need Docker-published listener infrastructure or explicit host-only firewall configuration.

## Added / changed

- Added DVWA command-injection impact runner.
- Added verified command-execution bundle.
- Recorded callback blocker for next infrastructure slice.
