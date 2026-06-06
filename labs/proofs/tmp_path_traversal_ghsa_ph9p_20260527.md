> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Local Proof Packet — tmp path traversal safe-marker — <specific-ghsa-id>

Status: verified local-lab proof / sanitized summary
Date: 2026-05-27
Verdict: `verified_tmp_path_traversal_arbitrary_file_creation_lab_only`

## Selected candidate

- Source: GitHub Advisory
- ID: `<specific-ghsa-id>`
- Title: `tmp has Path Traversal via unsanitized prefix/postfix that enables directory escape`
- Vulnerable package/range: npm `tmp < 0.2.6`
- Tested version: `tmp@0.2.5`

## Boundary

Local Kali victim-lab only. No live target, public IP/domain, scanner/fuzzer/DAST, callback/OAST, credential/token handling, secret/system file access, persistence, or report submission.

## Execution

- Runner: `scripts/labs/tmp_path_traversal_safe_marker_wave1.sh`
- Focused regression: `tests/test_tmp_path_traversal_safe_marker.sh`
- Victim VM: `<victim-vm>` (`<lab-ip>` host-only)
- Run artifact: `<artifact-output-dir>/tmp_path_traversal_ghsa_ph9p_20260527T1238Z/`
- Temporary NAT: enabled only for npm package acquisition, then disabled; final check returned `INTERNET_CLOSED_EXPECTED`.

## Sanitized evidence

See:

- `<artifact-output-dir>/tmp_path_traversal_ghsa_ph9p_20260527T1238Z/proof.json`
- `<artifact-output-dir>/tmp_path_traversal_ghsa_ph9p_20260527T1238Z/summary.md`

Key observed proof values:

```text
status=ok
package_version=0.2.5
control_inside_safe_base=true
escaped_inside_safe_base=false
escaped_marker_found=true
control_marker_found=true
escaped_relative_to_safe_base=../escape-zone/TMP_PATH_TRAVERSAL_MARKER_-4092-0tS7B4yhMz4X
```

## Verified proof pattern

A vulnerable app that passes attacker-controlled `prefix` into `tmp.fileSync({ tmpdir, prefix })` can create a temp file outside the intended temporary base. This proof used a marker-only escape from `safe-base/` into sibling `escape-zone/`, both under the run artifact directory.

## Stop-before rules

- Do not test on live targets without exact program scope/rules and explicit approval.
- Do not read or write real/sensitive system files.
- Do not overwrite existing files.
- Do not attempt code execution, persistence, web-root write, or container escape.
- Do not promote this to report-ready without a real authorized app data-flow and manually reviewed evidence.
