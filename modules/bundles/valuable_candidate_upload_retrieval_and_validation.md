> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# valuable_candidate_upload_retrieval_and_validation

Status: valuable-candidate / partial verified state-change
Date: 2026-05-22
Route/tool: Windows Hermes control plane -> SSH/SCP -> `<attacker-vm>` -> authorized Juice Shop victim
Artifact root: `<artifact-output-dir>/kali_intel_wave3_20260522T005554Z/`
Sources mapped: CISA KEV/NVD/Exploit-DB unrestricted upload and file-write patterns; OWASP A01/A05/A08; CWE-434
Related verified bundle: `verified_lab_flow_file_upload_marker_pdf.md`

## Why keep this bundle

Even without RCE, arbitrary web retrieval, or confirmed server-side storage path, upload validation is a high-value modern web workflow. This bundle records what the current target accepts and what remains unproven.

## Preconditions

- Admin lab token obtained through the existing SQLi auth-bypass lab flow.
- Requests sent from Kali to authorized local victim only.
- Harmless marker files only; no webshell, malware, or persistence.

## Attempts

Uploaded marker files to `/file-upload`:

```text
vf3_marker.pdf -> HTTP 204
vf3_marker.txt -> HTTP 204
```

Then probed likely retrieval locations:

```text
/assets/public/images/uploads/vf3_marker.pdf -> HTTP 200 marker_found=no
/ftp/vf3_marker.pdf -> HTTP 404 marker_found=no
/file-upload/vf3_marker.pdf -> HTTP 200 marker_found=no
/uploads/vf3_marker.pdf -> HTTP 200 marker_found=no
```

## Verification decision

- Verified: authenticated upload endpoint accepts marker uploads and returns HTTP 204.
- Not verified: public retrieval of uploaded file.
- Not verified: arbitrary file write path.
- Not verified: executable upload / webshell / RCE.

## Impact level

Level 3 / Level 4 boundary:

- state-changing upload accepted;
- server-side storage likely but retrieval path not proven;
- no execution or arbitrary path control proven.

## Value retained

- Records accepted extensions/content types for current lab.
- Records negative retrieval locations and marker checks.
- Provides a safe framework for future upload abuse testing against a target that supports retrieval or dangerous file types.

## Next steps

- Inspect API/docs/client source for upload storage or challenge completion endpoint.
- Try image extension/content-type mismatch in lab only.
- Add a dedicated vulnerable upload lab target if Juice Shop cannot demonstrate retrieval/execution.
