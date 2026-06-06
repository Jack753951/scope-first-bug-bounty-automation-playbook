> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# DVWA Command Injection Callback-Control Wave 2

Status: completed / verified command execution + lab marker + Docker-bridge callback
Date: 2026-05-22
Route/tool: Windows Hermes control plane -> SSH/SCP -> `<attacker-vm>` -> Docker-backed DVWA on `<victim-vm>`
Visible model/runtime: current Hermes session; no Claude/Codex worker usage artifact

## Target / scope

- Target: `http://<lab-ip>:18080`
- Victim: `<victim-vm>`
- Tester: `<attacker-vm>`
- Target container: `dvwa-impact-lab` from `vulnerables/web-dvwa:latest`
- Callback listener container: `dvwa-callback-lab` from `vulnerables/web-dvwa:latest`
- Callback path used by payload: Docker bridge `http://172.17.0.4:80/callback.php?marker=__MARKER__`
- Artifact run: `<artifact-output-dir>/dvwa_cmdinj_impact_wave1_20260522T054954Z/`

## Verified impact

Evidence file:

`<artifact-output-dir>/dvwa_cmdinj_impact_wave1_20260522T054954Z/http/command_injection_response.html`

Verified output excerpt:

```text
uid=33(www-data) gid=33(www-data) groups=33(www-data)
www-data
DVWA_CMDINJ_dvwa_cmdinj_impact_wave1_20260522T054954Z
```

Callback evidence file:

`<artifact-output-dir>/dvwa_cmdinj_impact_wave1_20260522T054954Z/callback_docker_listener/requests.jsonl`

Verified callback record:

```json
{"ts":"2026-05-22T05:50:03+00:00","remote":"172.17.0.5","query":"marker=DVWA_CMDINJ_dvwa_cmdinj_impact_wave1_20260522T054954Z","ua":""}
```

This proves:

1. Single command-injection vulnerability produced server-side OS command execution.
2. Execution identity was `www-data`.
3. Payload wrote/read a lab marker under `/tmp`.
4. Target container made an outbound HTTP callback to a controlled Docker-bridge listener.

## Important limitation

This is not yet a true attacker-VM callback. Aggressive-lab has inbound SSH only and no Docker runtime; high-port listeners on aggressive-lab and Windows host were unreachable. The callback in this wave is a controlled Docker-bridge callback between target container and listener container on victim-lab. It is still useful impact evidence, but should be labeled precisely.

## Cleanup

- Disposable `dvwa-impact-lab` target container was removed.
- Temporary `dvwa-callback-lab` listener container was removed after callback evidence was copied to local artifacts.
- `juice-shop-lab` and `webgoat-lab` remained running.

## Boundaries

- Authorized local lab only.
- Single vulnerability: command injection.
- Marker-only payload.
- Callback to lab listener only.
- No persistence.
- No credential theft.
- No OS destruction.
- No public target.

## Project benefit

- Upgrades the previous DVWA command-injection proof from `command exec + marker` to `command exec + marker + outbound callback`.
- Establishes a repeatable callback-control evidence pattern despite aggressive-lab inbound firewall limitations.
- Reveals the exact limitation: true attacker-host callback requires either aggressive-lab Docker/published listener or operator-approved host-only firewall opening.

## Added / changed

- Updated `scripts/labs/dvwa_command_injection_impact_wave1.sh` with `CALLBACK_URL_OVERRIDE` and `__MARKER__` substitution.
- Added callback evidence under the run artifacts.
- Added source coverage inventory handoff.
