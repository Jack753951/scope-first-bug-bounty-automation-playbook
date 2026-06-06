> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Local Proof Packet — LiquidJS <specific-cve-id> marker-only RCE surrogate

Status: verified local-lab proof / sanitized summary
Date: 2026-05-28
Verified at: 2026-05-28T10:30:01Z
Verdict: `verified_liquidjs_cve_2026_45618_marker_only_local_lab`

## Selected candidate

- Source: GitHub Advisory
- ID: `<specific-ghsa-id>`
- CVE: `<specific-cve-id>`
- Title: `LiquidJS is Vulnerable to Remote Code Execution`
- Vulnerable package/range: npm `liquidjs < 10.26.0`
- Tested vulnerable version: `liquidjs@10.25.7`
- Patched control version: `liquidjs@10.26.0`
- Advisory published: `2026-05-27T18:24:14Z`

## Boundary

Local Kali victim-lab only. No live target, public IP/domain, scanner/fuzzer/DAST, callback/OAST, credential/token handling, secret/system file access, persistence, destructive action, or report submission.

The proof used a marker-only command surrogate that wrote a synthetic marker file inside the run artifact directory. It did not read secrets, contact third parties, open callbacks, persist, or modify system paths.

## Execution

- Victim VM: `<victim-vm>` / `<lab-ip>` host-only
- Node on victim: see `<artifact-output-dir>/liquidjs_rce_cve_2026_45618_20260528T101739Z/node_versions.txt`
- Windows package cache: `<artifact-output-dir>/package-cache/liquidjs_rce_cve_2026_45618_20260528T101739Z/`
- Victim run artifact: `/home/kali/codex-output/<artifact-output-dir>/liquidjs_rce_cve_2026_45618_20260528T101739Z/`
- Pulled sanitized evidence: `<artifact-output-dir>/liquidjs_rce_cve_2026_45618_20260528T101739Z/`

Downloaded package checksums:

```text
982d303c22ab1dc0a0c3fd022cb034533f8963dd03cf73574e9bc262a930a7d7 *liquidjs-10.25.7.tgz
1f21df53f287b850d7105b04a88626745af489966e4adcc1328f04b2836b85a8 *liquidjs-10.26.0.tgz
```

## Sanitized evidence

Key observed proof values from `summary.json`:

```json
{
  "status": "ok",
  "verdict": "verified_liquidjs_cve_2026_45618_marker_only_local_lab",
  "advisory": "<specific-ghsa-id>",
  "cve": "<specific-cve-id>",
  "package": "liquidjs",
  "vulnerable_version": "10.25.7",
  "patched_control_version": "10.26.0",
  "vulnerable_marker_written": true,
  "vulnerable_marker_matches": true,
  "patched_marker_written": false,
  "patched_render_preview": "false",
  "boundary": "<victim-vm> local artifact directory only; marker file write only; no live target; no secrets"
}
```

Evidence files:

- `<artifact-output-dir>/liquidjs_rce_cve_2026_45618_20260528T101739Z/summary.json`
- `<artifact-output-dir>/liquidjs_rce_cve_2026_45618_20260528T101739Z/vulnerable_proof.json`
- `<artifact-output-dir>/liquidjs_rce_cve_2026_45618_20260528T101739Z/patched_control.json`
- `<artifact-output-dir>/liquidjs_rce_cve_2026_45618_20260528T101739Z/posture.txt`

## Verified proof pattern

A crafted LiquidJS template can regain access to internal objects and reach a function-constructor execution path in vulnerable versions. In the local lab, this was constrained to a marker-only action: writing `LIQUIDJS_CVE_2026_45618_SAFE_MARKER_VULN` under the run artifact directory.

The vulnerable control (`10.25.7`) wrote the synthetic marker. The patched control (`10.26.0`) did not write the marker and rendered `false`.

## Stop-before rules

- Do not test on live targets without exact program scope/rules and explicit operator approval.
- Do not execute arbitrary commands outside a disposable local lab.
- Do not read `/etc/passwd`, environment variables, tokens, cookies, SSH keys, cloud metadata, application secrets, or user data.
- Do not use callbacks/OAST, persistence, reverse shells, web-root writes, or destructive commands.
- Do not promote this to report-ready without an authorized app data-flow proving attacker-controlled template input in an in-scope asset.
