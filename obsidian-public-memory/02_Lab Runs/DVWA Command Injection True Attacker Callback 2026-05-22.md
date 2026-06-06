> Public filtered Obsidian memory export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# DVWA Command Injection True Attacker Callback 2026-05-22

Status: completed / verified command execution + marker + attacker-VM callback
Repo handoff: `<user-home>`
Bundle: `<user-home>`
Artifacts: `<user-home>`

## Result

Verified command execution:

```text
uid=33(www-data) gid=33(www-data) groups=33(www-data)
www-data
DVWA_CMDINJ_dvwa_cmdinj_impact_wave1_20260522T061407Z
```

Verified attacker-side callback:

```json
{"ts":"2026-05-22T06:14:12+00:00","remote":"<lab-ip>","query":"marker=DVWA_CMDINJ_dvwa_cmdinj_impact_wave1_20260522T061407Z","ua":"","path":"/callback.php?marker=DVWA_CMDINJ_dvwa_cmdinj_impact_wave1_20260522T061407Z"}
```

## Infrastructure outcome

- Docker installed on `<lab-vm>`.
- Temporary NAT setup window was closed after use.
- Disposable target/listener containers removed.
- Juice Shop and WebGoat still reachable.

## Why this matters

This is the first verified local-lab proof where one vulnerability produced:

1. OS command execution,
2. marker file write/readback,
3. outbound callback to the attacker VM.

This better matches the project direction: one-vulnerability max-impact proofs on recoverable local靶機.
