> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Modern API path traversal file-read safe-marker — Hermes tactical preview

Status: preview complete / local-lab target expansion
Date: 2026-05-23
Lane: second file read / path traversal safe-marker target
Target: `labs/modern_vuln_api/modern_vuln_api.py` `/file-read?name=`

## Source / OSS reconnaissance

Existing project references already cover this lane:

- WebGoat path traversal source and prior waves: `scripts/labs/webgoat_pathtraversal_*`, `handoff/webgoat_pathtraversal_file_read_retry_20260523.md`.
- Skill reference: `owasp-single-vuln-lab-wave` / `references/webgoat-path-traversal-zipslip-proofs.md`.
- Prior outcome: WebGoat direct random-picture retrieval stayed `attempted-not-verified` because raw/encoded traversal returned HTTP 400 and no marker content was read.

Decision: `write-custom` bounded local target expansion. Reason: the current WebGoat direct-read surface rejected traversal before marker read evidence; adding a small disposable source-controlled endpoint gives a clean lab-owned safe-marker file-read proof without sensitive system files or public targets.

## Five tactical preview questions

1. Maximum safe proof:
   - Lab-owned marker file read via path traversal, plus public-file control and missing-file control.
   - No `/etc/passwd`, no secrets, no token/credential files, no shell, no persistence.

2. Can the current target prove it?
   - Yes after bounded local target expansion in `modern_vuln_api.py`: `/file-read?name=` naively joins user input under a lab public directory, while `../hermes_modern_api_file_read_marker.txt` reaches a lab-owned marker in temp.

3. Minimum positive/control evidence:
   - Pre-health 200.
   - Public control `name=public.txt` returns `PUBLIC_FILE_CONTROL_HERMES_LOCAL_LAB`.
   - Missing control returns 404.
   - Positive traversal returns `FILE_READ_SAFE_MARKER_HERMES_LOCAL_LAB`.
   - Post-health 200 and cleanup evidence.

4. If blocked/unsuitable, alternate lanes:
   - Source-level review of WebGoat `random-picture` intended route and encoding rules.
   - Another recoverable local target with an equivalent safe-marker file-read fixture.

5. Proof-library capability added:
   - A clean file-read safe-marker proof pattern, complementing WebGoat upload-write/Zip Slip overwrite and modern_vuln_api XXE safe-marker.

## Execution plan

- Run from `<attacker-vm>` against Docker-published `modern_vuln_api` on `<victim-vm>`.
- Use port `18083` to avoid colliding with recent SSRF/deser/XXE runs.
- Preserve artifacts under `<artifact-output-dir>/modern_api_path_traversal_file_read_<timestamp>/`.
- Cleanup target container and verify attacker/victim Internet remains closed.

## Boundary

Local authorized lab only. Lab-owned files only. No sensitive system-file reads, no secrets/credentials, no public target, no shell, no persistence, no exfiltration, no finding/report promotion.
