> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# tmp path traversal <specific-ghsa-id> — verified local-lab continuation

Status: completed / verified local-lab proof pattern / no live target authorization
Date: 2026-05-27

## What changed from the metadata-only loop

The previous generated proof loop stopped at planning artifacts. The operator then explicitly asked to continue into a Kali 靶機 proof until a verified proof pattern. I selected a newer, clean local-lab candidate from the same 2026-05-27 vuln-intel set rather than the heavier product-specific CVE:

- Selected: `<specific-ghsa-id>` (`tmp < 0.2.6` path traversal via unsafe `prefix`/`postfix`/`dir`).
- Reason: fully verifiable with synthetic marker files in a disposable Kali victim-lab artifact directory; no account, live target, scanner, callback, or privileged Docker posture required.

## Execution summary

- Added tested runner: `scripts/labs/tmp_path_traversal_safe_marker_wave1.sh`.
- Added focused fail-closed regression: `tests/test_tmp_path_traversal_safe_marker.sh`.
- Ran on `<victim-vm>` via the Windows Hermes SSH bridge.
- Enabled victim NAT temporarily for npm package acquisition, then closed `nic2`/cable and verified `INTERNET_CLOSED_EXPECTED`.
- Pulled sanitized artifacts to `<artifact-output-dir>/tmp_path_traversal_ghsa_ph9p_20260527T1238Z/`.

## Verification result

The proof reached:

```text
verified_tmp_path_traversal_arbitrary_file_creation_lab_only
```

Evidence highlights:

```text
package_version=0.2.5
control_inside_safe_base=true
escaped_inside_safe_base=false
escaped_marker_found=true
control_marker_found=true
```

## Promoted artifacts

- Bundle: `modules/bundles/verified_lab_flow_tmp_path_traversal_arbitrary_file_creation.md`
- Proof packet: `labs/proofs/tmp_path_traversal_ghsa_ph9p_20260527.md`
- Runner: `scripts/labs/tmp_path_traversal_safe_marker_wave1.sh`
- Test: `tests/test_tmp_path_traversal_safe_marker.sh`

## Safety boundary

Local-lab proof only. This does not authorize live target testing. For live bounty use, require exact program scope/rules, a concrete app data-flow into vulnerable `tmp` options, operator-owned synthetic paths/files, redaction, and stop-before rules for overwrite, sensitive file access, web-root write, persistence, code execution, callbacks, or report submission.
