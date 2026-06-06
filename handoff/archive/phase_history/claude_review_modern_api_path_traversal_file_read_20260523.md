> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Claude Code read-only review — modern_vuln_api path traversal file-read safe-marker

Date: 2026-05-23
Route/tool: Hermes `delegate_task` read-only evidence review with file/terminal toolsets
Visible model/runtime: `gpt-5.5` reported by delegate result; exact hosted runtime otherwise not exposed
Usage artifact path: delegate result in current Hermes transcript; no separate JSON file emitted by delegate_task

## Scope reviewed

- Preview: `handoff/modern_api_path_traversal_file_read_preview_20260523.md`
- Runner: `scripts/labs/modern_api_path_traversal_file_read_wave1.sh`
- Evidence: `<artifact-output-dir>/modern_api_path_traversal_file_read_20260523T094352Z/`
- Target source: `labs/modern_vuln_api/modern_vuln_api.py`

## Reviewer conclusion

Evidence supports: `verified_file_read_safe_marker_lab_only`.

The proof shows a lab-owned marker file read through path traversal on the intentionally vulnerable local `modern_vuln_api` endpoint. It does not support claims about real products, public targets, arbitrary sensitive file read, secret access, shell, persistence, or exfiltration.

## Evidence supporting the classification

- Route: `GET /file-read?name=` on `http://<lab-ip>:18083`.
- Positive payload: `name=../hermes_modern_api_file_read_marker.txt`, URL-encoded by the runner.
- Runtime: victim-side Docker container `modern-api-pathread-18083` using `python:3-alpine`.
- Pre-health: `200`.
- Post-health: `200`.
- Public control: `http/public_control.json` returned `PUBLIC_FILE_CONTROL_HERMES_LOCAL_LAB` with status `200`.
- Missing-file negative control: status `404`.
- Positive traversal: `http/traversal_positive.json` returned `FILE_READ_SAFE_MARKER_HERMES_LOCAL_LAB` and resolved path `/tmp/hermes_modern_api_public_files/../hermes_modern_api_file_read_marker.txt`.
- Boundary/cleanup: attacker and victim Internet were closed before/after; cleanup removed the target container.
- Runner log records `VERDICT=verified_file_read_safe_marker_lab_only`.

## Missing evidence / overclaim risks

- Do not claim real-target exploitability or a production finding.
- Do not claim arbitrary sensitive system-file read; the evidence only proves a lab-owned temp fixture marker read.
- `resolved` is a `Path` string, not canonical `realpath`; content evidence is still enough for safe-marker proof.
- Raw HTTP headers / verbose curl transcript and Docker inspect/log metadata would strengthen a formal evidence packet, but are not required for this local-lab safe-marker classification.

## Recommendation

Stop and packetize / record. No rerun is necessary unless the project wants stronger packet-grade metadata such as curl verbose output, raw headers, canonical realpath, or container inspect summary.
