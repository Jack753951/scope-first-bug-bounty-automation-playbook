> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Local Proof Packet — LiquidJS <specific-cve-id> strip_html ReDoS

Status: verified local-lab proof / sanitized summary
Date: 2026-05-28
Verified at: 2026-05-28T11:00:42.460Z
Verdict: `verified_liquidjs_cve_2026_45617_strip_html_redos_local_lab`

## Selected candidate

- Source: GitHub Advisory
- ID: `<specific-ghsa-id>`
- CVE: `<specific-cve-id>`
- Title: `LiquidJS Vulnerable to ReDoS via Quadratic Backtracking in strip_html Filter Regex`
- Vulnerable package/range: npm `liquidjs < 10.26.0`
- Tested vulnerable version: `liquidjs@10.25.7`
- Patched control version: `liquidjs@10.26.0`
- Advisory published: `2026-05-27T18:08:19Z`

## Boundary

Local Kali victim-lab only (`<victim-vm>`, host-only). No live target, public IP/domain, scanner/fuzzer/DAST, callback/OAST, credential/token handling, secret/system file access, persistence, or report submission.

The proof intentionally maximized local impact only to the point of a recoverable CPU/event-loop stall. It did not attempt uncontrolled resource exhaustion or crash the VM.

## Execution

- Victim-side artifact: `/home/kali/codex-output/<artifact-output-dir>/three_latest_npm_vulns_20260528T110251Z/`
- Pulled sanitized evidence: `<artifact-output-dir>/three_latest_npm_vulns_20260528T110251Z/evidence/`
- Package environment was built on the Windows control plane and transferred to the isolated victim; the victim did not need NAT/package resolution.

## Sanitized evidence

Key observed values from `liquidjs_redos_proof.json`:

```text
status: verified
vulnerable_version: 10.25.7
patched_control_version: 10.26.0
vulnerable_max_elapsed_ms: 5841.175
patched_max_elapsed_ms: 7.685
input_bytes_at_max: 210000
```

Evidence files:

- `<artifact-output-dir>/three_latest_npm_vulns_20260528T110251Z/evidence/summary.json`
- `<artifact-output-dir>/three_latest_npm_vulns_20260528T110251Z/evidence/liquidjs_redos_proof.json`
- `<artifact-output-dir>/three_latest_npm_vulns_20260528T110251Z/evidence/posture.txt`

## Verified proof pattern

A crafted string containing many unmatched `<script` opener tokens passed through LiquidJS `strip_html` produces a large CPU/event-loop stall in vulnerable versions. In this run, `liquidjs@10.25.7` took about `5841.175` ms for a 210 KB synthetic input, while `liquidjs@10.26.0` completed the same control in about `7.685` ms.

This demonstrates a practical ReDoS/availability impact with a positive vulnerable control and patched negative control.

## Stop-before rules

- Do not run against live targets without exact scope/rules and explicit operator approval.
- Do not increase payload size to uncontrolled VM/resource exhaustion.
- Do not combine with scanners/fuzzers or broad endpoint discovery.
- Do not promote to report-ready without an authorized app data-flow proving attacker-controlled input reaches `strip_html` on an in-scope asset.
