> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# verified_lab_flow_modern_api_ssrf_isolated_callback

Status: verified-impact / authorized local lab / disposable target
Date: 2026-05-22
Route/tool: Windows Hermes control plane -> SSH/SCP -> `<attacker-vm>` -> local disposable target `http://127.0.0.1:18080`
Target implementation: `labs/modern_vuln_api/modern_vuln_api.py`
Artifacts: `<artifact-output-dir>/modern_api_wave1_20260522T021059Z/`
Sources mapped: OWASP A10 SSRF, CWE-918, CISA KEV/NVD/Exploit-DB SSRF pattern inspiration

## Why this target was added

Juice Shop did not provide an isolated callback proof surface. This disposable target adds a safe SSRF-style server-side fetch endpoint and an internal callback log, so SSRF evidence can be generated without public OAST or third-party infrastructure.

## Verified flow

1. The lab target exposes `/fetch?url=...`, which performs server-side HTTP GET.
2. The callback endpoint `/callback` records incoming requests.
3. The test sent:

```text
GET /fetch?url=http://127.0.0.1:18080/callback?marker=SSRF_MARKER
```

Observed:

```text
fetch_status=200
callback_log_status=200
callback_count=1
```

## Impact

Level 3 lab impact: server-side request was induced and observed through an isolated local callback. This proves SSRF behavior in a contained lab without external callbacks.

## Evidence

- `<artifact-output-dir>/modern_api_wave1_20260522T021059Z/ssrf_fetch.json`
- `<artifact-output-dir>/modern_api_wave1_20260522T021059Z/callback_log.json`
- `<artifact-output-dir>/modern_api_wave1_20260522T021059Z/observations.jsonl`

## Boundaries

- Callback is local only (`127.0.0.1`).
- No cloud metadata endpoint.
- No external OAST.
- No real internal network scan.

## Cleanup / recovery

Stop target with:

```bash
~/hermes-labs/modern_vuln_api/stop_modern_vuln_api.sh 18080
```

## 2026-05-23 true-attacker callback expansion

Status: verified-impact lab-only / operator-confirmed trigger.

Verified handoff: `handoff/modern_api_ssrf_true_attacker_callback_verified_20260523.md`
Evidence packet: `handoff/modern_api_ssrf_true_attacker_callback_evidence_packet_20260523.md`
Operator run-card: `handoff/ssrf_operator_run_card_20260523.md`
Historical blocked setup attempt: `handoff/modern_api_ssrf_attacker_callback_attempt_20260523.md`
Verified artifacts: `<artifact-output-dir>/modern_api_ssrf_operator_20260523T074358Z/`
OSS references: `setting/local/oss_refs/ssrf_callback_20260523/`
Runner: `scripts/labs/operator_ssrf_true_callback_run.sh`

What was learned:

- OSS-first sources for this lane include PayloadsAllTheThings SSRF and SSRFmap; public OAST/interactsh patterns should be adapted to local host-only callback evidence.
- Raw host high ports were not reachable across VMs, but Docker-published attacker listener port `<lab-ip>:18183` was reachable from victim `<lab-ip>`.
- Docker-published `modern_vuln_api` on victim `<lab-ip>:18081` is a better target surface than a plain host process for cross-VM testing.
- Temporary NAT was used earlier to pull `python:3-alpine` on attacker and victim, then closed/verified.
- The final `/fetch?url=attacker-callback` trigger was executed only by explicit operator confirmation after the local execution layer denial; Hermes did not retry/bypass the denied trigger.

Verified operator run `modern_api_ssrf_operator_20260523T074358Z`:

```text
pre_health=200
ssrf_trigger_status=200
post_health=200
callback_marker_found=yes
callback_source_victim_ip_found=yes
callback_trigger_path_found=yes
VERDICT=verified_impact_lab_only
```

Authoritative callback evidence from `callback/requests.jsonl` includes the trigger callback from victim to attacker:

```text
client=<lab-ip>
path=/ssrf-callback?marker=modern_api_ssrf_operator_20260523T074358Z
User-Agent=HermesModernVulnAPI-SSRF-Lab
```

Boundary: local authorized lab only, exactly one trigger, no metadata endpoints, no localhost/internal scan, no public OAST, no public/unknown target, no secrets/credentials/exfiltration, no automatic report/finding promotion.
