> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# DVWA Command Injection True Attacker-Side Callback

Status: completed / verified command execution + marker + attacker-VM callback
Date: 2026-05-22
Route/tool: Windows Hermes control plane -> SSH/SCP -> `<attacker-vm>` Docker-published listener -> Docker-backed DVWA target on `<victim-vm>`
Visible model/runtime: current Hermes session; no Claude/Codex worker usage artifact

## Target / scope

- Target URL: `http://<lab-ip>:18080`
- Victim VM: `<victim-vm>` / `<lab-ip>`
- Attacker VM: `<attacker-vm>` / `<lab-ip>`
- Vulnerable target container: `dvwa-impact-lab` from `vulnerables/web-dvwa:latest`
- Attacker callback listener container: `dvwa-attacker-callback` from `php:8.2-apache`
- Callback bind: `<lab-ip>:18182 -> container:80`
- Artifact run: `<artifact-output-dir>/dvwa_cmdinj_impact_wave1_20260522T061407Z/`

## Verified impact

Command execution evidence:

`<artifact-output-dir>/dvwa_cmdinj_impact_wave1_20260522T061407Z/http/command_injection_response.html`

Verified excerpt:

```text
uid=33(www-data) gid=33(www-data) groups=33(www-data)
www-data
DVWA_CMDINJ_dvwa_cmdinj_impact_wave1_20260522T061407Z
```

Attacker-side callback evidence:

`<artifact-output-dir>/dvwa_cmdinj_impact_wave1_20260522T061407Z/attacker_docker_callback/requests.jsonl`

Verified callback record:

```json
{"ts":"2026-05-22T06:14:12+00:00","remote":"<lab-ip>","query":"marker=DVWA_CMDINJ_dvwa_cmdinj_impact_wave1_20260522T061407Z","ua":"","path":"/callback.php?marker=DVWA_CMDINJ_dvwa_cmdinj_impact_wave1_20260522T061407Z"}
```

This proves:

1. Single command-injection vulnerability produced server-side OS command execution.
2. Execution identity was `www-data`.
3. Payload wrote/read a lab marker under `/tmp`.
4. Target/victim side made an outbound HTTP callback to the attacker VM listener.
5. Callback marker matched the command-execution marker.

## Infrastructure changes

- Installed Docker runtime on `<attacker-vm>` during an operator-approved NAT window.
- Pulled `php:8.2-apache` for disposable callback listener use.
- Patched `scripts/labs/dvwa_command_injection_impact_wave1.sh` to support external callback listeners via:
  - `CALLBACK_URL_OVERRIDE`
  - `__MARKER__` substitution
  - `USE_LOCAL_CALLBACK_LISTENER=0` mode for Docker-published listener workflows

## Cleanup / restore

- Removed victim disposable target container `dvwa-impact-lab`.
- Removed attacker disposable callback listener container `dvwa-attacker-callback`.
- Closed aggressive-lab NAT window:
  - `nic2="null"`
  - `cableconnected2="off"`
- Verified aggressive-lab Internet closed:
  - `ping 1.1.1.1` failed
  - `curl https://download.docker.com` timed out resolving
- Verified lab services remain available:
  - Juice Shop HTTP 200 on `<lab-ip>:3000`
  - WebGoat login HTTP 200 on `<lab-ip>:8080/WebGoat/login`

## Boundaries

- Authorized local lab only.
- Single vulnerability: DVWA command injection.
- Marker-only payload under `/tmp`.
- Attacker callback is host-only lab network (`<lab-ip>/24`).
- No persistence.
- No credential theft.
- No OS destruction.
- No public target.

## Notes / caveats

- The runner summary's `callback_count: 0` refers to its old local Python listener artifact under `callback/requests.jsonl`. The verified attacker-side callback is stored separately under `attacker_docker_callback/requests.jsonl` because this run used the Docker-published listener.
- Historical artifact labels say `<attacker-vm>`; future reruns should use the current default attacker route `<attacker-vm>` unless a later handoff supersedes it.
- Aggressive-lab-v2 Docker is available per current navigation and can be reused for future callback/control drills without reopening NAT, unless new images must be pulled.
- 2026-05-23 standardized packet/checklist: `handoff/dvwa_attacker_callback_evidence_packet_standard_20260523.md`.
