> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# WebGoat Path Traversal File Read Retry — 2026-05-23

Status: attempted-not-verified / useful control evidence
Source: Hermes local-lab run
Date: 2026-05-23
Route/tool: Hermes -> `scripts/kali-run.ps1` -> `<attacker-vm>` against Docker-backed WebGoat on `<victim-vm>`
Visible runtime/model: gpt-5.5 / openai-codex
Artifact root: `<artifact-output-dir>/webgoat_pathtraversal_file_read_20260523T090724Z/`

## Tactical preview answers

1. Maximum safe proof: bounded path traversal file-read of a lab/training marker, with control image read and blocked raw traversal control. Avoid `/etc/passwd`, secrets, credentials, or loot.
2. Current target suitability: WebGoat PathTraversal has a relevant lesson and existing runner, but this exact direct-read endpoint may intentionally reject traversal encodings. Still worth retrying because it improves the file-read/path-traversal proof shelf.
3. Minimum evidence: pre-health 200, authenticated throwaway session, control file read 200, positive encoded traversal response containing lesson marker, raw traversal blocked/negative control, post-health 200.
4. Fallback lanes if blocked: (a) use WebGoat source-level analysis to identify the intended file-read route/encoding and write a better bounded runner; (b) switch to equivalent local target / modern_vuln_api safe-marker file read or adjacent XXE/path traversal safe-marker lane.
5. Proof-library capability added: direct path-traversal file-read control evidence and endpoint rejection behavior, not verified impact.

## Execution result

Command run from Windows control plane via Kali bridge:

```text
powershell.exe -NoProfile -ExecutionPolicy Bypass -File scripts/kali-run.ps1 -Command "bash /mnt/hacking/scripts/labs/webgoat_pathtraversal_file_read_wave1.sh"
```

Remote output path:

```text
/home/kali/<artifact-output-dir>/webgoat_pathtraversal_file_read_20260523T090724Z
```

Pulled locally to:

```text
<artifact-output-dir>/webgoat_pathtraversal_file_read_20260523T090724Z/
```

Summary:

```text
pre_health: 200
login_status: 302
lesson_status: 200
js_status: 200
control_cat_status: 200
raw_traversal_blocked_status: 400
encoded_traversal_status: 400
secret_marker_found: no
submit_status: 200
post_health: 200
```

## Hermes classification

- Result: `attempted-not-verified`.
- Project value: useful control/rejection evidence for the WebGoat direct file-read lane; confirms health/session/lesson/control are reachable but this specific raw/encoded traversal path did not return the expected marker.
- Do not claim verified file-read impact from this run.
- Keep WebGoat upload-write and Zip Slip overwrite as verified path traversal family proofs; keep modern_vuln_api XXE safe-marker as verified file-read-style proof.

## Boundary

Authorized local WebGoat lab only. Throwaway WebGoat user. No public target, no sensitive system files, no credential theft, no exfiltration, no persistence, no shell, no automatic report/finding promotion.

## Next options

1. Source-level WebGoat PathTraversal route review to identify whether a direct marker read is intended and what encoding/path shape is correct.
2. Equivalent local disposable target for clean marker file read if the training endpoint is intentionally rejecting direct traversal.
3. Adjacent safe-marker proof: modern_vuln_api / custom local path traversal read with positive and negative controls.
