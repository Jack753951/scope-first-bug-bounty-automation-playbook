> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# verified_lab_flow_modern_api_deserialization_bounded_gadget

Status: verified-impact / authorized local lab / bounded deserialization gadget proof
Date: 2026-05-22; updated 2026-05-23 with dedicated operator-run proof
Route/tool: Windows Hermes control plane -> SSH/SCP -> `<attacker-vm>` historical proof; dedicated operator run from `<attacker-vm>` to `<victim-vm>`
Target implementation: `labs/modern_vuln_api/modern_vuln_api.py`
Artifacts: historical `<artifact-output-dir>/modern_api_wave2_20260522T022303Z/`; dedicated `<artifact-output-dir>/modern_api_deser_operator_20260523T093300Z/`
Sources mapped: OWASP A08 Software and Data Integrity Failures / insecure deserialization, CWE-502, Exploit-DB/GitHub/HTB deserialization patterns

## Why this target was added

Juice Shop did not provide a clear serialized-object input surface. This disposable target adds an intentionally unsafe pickle endpoint, but the proof payload is bounded to an in-process marker recorder instead of shell execution.

## Verified flow

### Dedicated operator-run proof — 2026-05-23

Script/run-card:

- `scripts/labs/operator_deser_bounded_marker_run.sh`
- `handoff/deser_operator_run_card_20260523.md`
- Verified handoff: `handoff/modern_api_deserialization_bounded_marker_operator_verified_20260523.md`

Observed:

```text
run_id=modern_api_deser_operator_20260523T093300Z
target=http://<lab-ip>:18082
pre_health=200
invalid_control_status=400
deserialize_marker_status=200
deser_log_pre_status=200
deser_log_post_status=200
post_health=200
marker_found=yes
VERDICT=verified_bounded_marker_lab_only
```

Marker:

```text
DESER_OPERATOR_modern_api_deser_operator_20260523T093300Z
```

Positive response/log evidence contains `type: bounded_pickle_gadget` and the unique marker. Cleanup removed `modern-api-deser-18082`; attacker/victim Internet remained closed.

### Historical broad-family proof — 2026-05-22

Request:

```text
POST /deserialize
Content-Type: application/json
{"payload_b64": "<protocol-0 pickle calling __main__.record_deser_marker>"}
```

Observed:

```text
deserialize -> HTTP 200
log_status=200
marker_found=yes
DESER_SAFE_MARKER_HERMES_LOCAL_LAB
```

Response excerpt:

```text
{'recorded': True, 'marker': 'DESER_SAFE_MARKER_HERMES_LOCAL_LAB'}
```

## Impact

Level 4 lab impact: untrusted deserialization invoked a server-side callable. The payload is intentionally constrained: no shell, no filesystem writes, no persistence, no external callback.

## Evidence

Dedicated operator-run artifacts:

- `<artifact-output-dir>/modern_api_deser_operator_20260523T093300Z/summary.md`
- `<artifact-output-dir>/modern_api_deser_operator_20260523T093300Z/run.log`
- `<artifact-output-dir>/modern_api_deser_operator_20260523T093300Z/http/deserialize_invalid_control.json`
- `<artifact-output-dir>/modern_api_deser_operator_20260523T093300Z/http/deserialize_marker_response.json`
- `<artifact-output-dir>/modern_api_deser_operator_20260523T093300Z/http/deser_log_post.json`
- `<artifact-output-dir>/modern_api_deser_operator_20260523T093300Z/http/post_health.json`
- `<artifact-output-dir>/modern_api_deser_operator_20260523T093300Z/cleanup/`

Historical broad-family artifacts:

- `<artifact-output-dir>/modern_api_wave2_20260522T022303Z/deser/payload.json`
- `<artifact-output-dir>/modern_api_wave2_20260522T022303Z/deser/response.json`
- `<artifact-output-dir>/modern_api_wave2_20260522T022303Z/deser/log.json`
- `<artifact-output-dir>/modern_api_wave2_20260522T022303Z/observations.jsonl`

## Boundaries

- No command execution payload.
- No reverse shell.
- No persistence.
- No public target.
