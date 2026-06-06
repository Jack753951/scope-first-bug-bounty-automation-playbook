> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Local Proof Packet — tmp <specific-cve-id> path traversal with patched control

Status: verified local-lab proof / sanitized summary
Date: 2026-05-28
Verified at: 2026-05-28T11:00:42.460Z
Verdict: `verified_tmp_cve_2026_44705_path_traversal_patched_control_local_lab`

## Selected candidate

- Source: GitHub Advisory
- ID: `<specific-ghsa-id>`
- CVE: `<specific-cve-id>`
- Title: `tmp has Path Traversal via unsanitized prefix/postfix that enables directory escape`
- Vulnerable package/range: npm `tmp < 0.2.6`
- Tested vulnerable version: `tmp@0.2.5`
- Patched control version: `tmp@0.2.6`
- Advisory published: `2026-05-27T00:34:06Z`

## Boundary

Local Kali victim-lab only. No live target, public IP/domain, scanner/fuzzer/DAST, callback/OAST, credential/token handling, secret/system file access, persistence, overwrite of existing files, or report submission.

The proof intentionally caused the maximum useful recoverable impact: creating a synthetic marker outside the intended temporary base directory. The runner cleaned the lab-owned temp directories after recording evidence.

## Execution

- Victim-side artifact: `/home/kali/codex-output/<artifact-output-dir>/three_latest_npm_vulns_20260528T110251Z/`
- Pulled sanitized evidence: `<artifact-output-dir>/three_latest_npm_vulns_20260528T110251Z/evidence/`
- Package environment was built on the Windows control plane and transferred to the isolated victim.

## Sanitized evidence

Key observed values from `tmp_path_traversal_proof.json`:

```text
status: verified
vulnerable_version: 0.2.5
patched_control_version: 0.2.6
vulnerable escaped: true
vulnerable marker wrote: true
patched marker wrote: false
patched error: Relative value not allowed
```

Evidence files:

- `<artifact-output-dir>/three_latest_npm_vulns_20260528T110251Z/evidence/summary.json`
- `<artifact-output-dir>/three_latest_npm_vulns_20260528T110251Z/evidence/tmp_path_traversal_proof.json`
- `<artifact-output-dir>/three_latest_npm_vulns_20260528T110251Z/evidence/posture.txt`

## Verified proof pattern

A vulnerable application that passes attacker-controlled values into `tmp.fileSync({ dir, prefix, postfix })` can create a file outside the intended temporary base directory. In the vulnerable control, the marker file escaped the configured base into a sibling lab-owned path. In the patched control, the relative traversal value was rejected.

## Stop-before rules

- Do not test on live targets without exact scope/rules and explicit operator approval.
- Do not write real system paths, web roots, cron paths, app configs, or existing files.
- Do not read secrets or system files.
- Do not promote to report-ready without an authorized app data-flow proving attacker-controlled tmp options in an in-scope asset.
