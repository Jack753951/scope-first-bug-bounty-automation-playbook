> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# verified_lab_flow_dvwa_command_injection_container_control

Status: verified-impact / local-lab only
Date: 2026-05-22
Route/tool: `<attacker-vm>` HTTP/curl -> Docker-published DVWA on `<victim-vm>`

## Purpose

Demonstrate a one-vulnerability max-impact local-lab proof for OS command injection without persistence, credential theft, public targets, or uncontrolled destruction.

## Trigger

Use when an authorized disposable lab target exposes DVWA low-security command injection or an equivalent command-injection training endpoint.

## Verified evidence

Run artifact:

`<artifact-output-dir>/dvwa_cmdinj_impact_wave1_20260522T052046Z/`

Key evidence:

`http/command_injection_response.html`

Verified output:

```text
uid=33(www-data) gid=33(www-data) groups=33(www-data)
www-data
DVWA_CMDINJ_dvwa_cmdinj_impact_wave1_20260522T052046Z
```

Impact demonstrated:

1. Server-side OS command execution.
2. Execution identity: `www-data`.
3. Lab marker file write/readback at `/tmp/DVWA_CMDINJ_dvwa_cmdinj_impact_wave1_20260522T052046Z.txt`.

## Callback blocker

Outbound callback was not verified in this wave. High-port listeners on aggressive-lab and Windows host were unreachable from the target path. Do not claim callback success from this run.

Next callback/control lane should use one of:

- Docker-published callback listener container.
- Operator-approved host-only firewall opening for a callback port.
- A dedicated callback lab target with explicit recovery and audit notes.

## Boundaries

Allowed in this bundle:

- DVWA disposable Docker container only.
- Command execution proof as `www-data`.
- Lab marker file under `/tmp`.
- Container cleanup after run.

Disallowed in this bundle:

- Public/unknown targets.
- Real credential theft.
- Persistence/backdoor installation.
- OS destruction or host filesystem damage.
- Unbounded reverse shell/C2.
- Automatic finding/report promotion.

## Reuse notes

- Prefer Docker-published target ports in this lab because victim host services on arbitrary ports are firewall-blocked.
- Keep command payloads marker-only unless a separate destructive/recovery drill is explicitly planned with snapshot/restore evidence.
