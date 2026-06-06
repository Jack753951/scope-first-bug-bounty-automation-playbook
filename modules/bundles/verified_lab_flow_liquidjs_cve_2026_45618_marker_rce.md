> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Verified Lab Flow — LiquidJS <specific-cve-id> marker-only RCE surrogate

Status: `verified_liquidjs_cve_2026_45618_marker_only_local_lab`
Last verified: 2026-05-28
Source advisory: `<specific-ghsa-id>`
CVE: `<specific-cve-id>`
Package under test: `liquidjs@10.25.7` (`< 10.26.0` vulnerable; `10.26.0` patched control)
OWASP mapping: A03 Injection / template injection family; A06 Vulnerable and Outdated Components context
Target lane: `local-learning-lab`

## When to use

Use this bundle when the project needs a recoverable local-lab proof pattern for template-engine RCE where attacker-controlled LiquidJS templates can reach execution primitives.

This bundle is a marker-only proof. It demonstrates code-execution reachability only by writing a synthetic marker file inside a lab-owned artifact directory. It does not claim live exploitability, sensitive file read, network callback, persistence, reverse shell, web-root write, or destructive impact.

## Candidate selection

The candidate was selected from the 2026-05-28 GitHub Advisory refresh:

- ID: `<specific-ghsa-id>`
- CVE: `<specific-cve-id>`
- Title: `LiquidJS is Vulnerable to Remote Code Execution`
- Class: template-engine RCE / injection
- Safe proof reason: npm package behavior can be verified in `<victim-vm>` with a synthetic marker-only command and a patched-version negative control.

## Runner / artifacts

Local package cache:

```text
<artifact-output-dir>/package-cache/liquidjs_rce_cve_2026_45618_20260528T101739Z/
```

Victim-side artifact:

```text
/home/kali/codex-output/<artifact-output-dir>/liquidjs_rce_cve_2026_45618_20260528T101739Z/
```

Pulled sanitized evidence:

```text
<artifact-output-dir>/liquidjs_rce_cve_2026_45618_20260528T101739Z/
```

Key files:

- `summary.json`
- `vulnerable_proof.json`
- `patched_control.json`
- `posture.txt`
- `node_versions.txt`

## Latest verified values

```text
status: ok
verdict: verified_liquidjs_cve_2026_45618_marker_only_local_lab
vulnerable_version: 10.25.7
patched_control_version: 10.26.0
vulnerable_marker_written: true
vulnerable_marker_matches: true
patched_marker_written: false
patched_render_preview: false
```

## Lab posture and recovery

- Victim: `<victim-vm>` / host-only `<lab-ip>`.
- Proof writes only under `/home/kali/codex-output/<artifact-output-dir>/liquidjs_rce_cve_2026_45618_20260528T101739Z/`.
- No live target, scanner/fuzzer/DAST, callback/OAST, token/cookie/secret handling, or system secret read was used.
- npm package acquisition was done from the Windows control plane after operator approval; the victim install used transferred local node environments to avoid opening victim NAT for package resolution.

## Success criteria

A run may be classified as `verified_liquidjs_cve_2026_45618_marker_only_local_lab` only when all are true:

- advisory and package range are recorded;
- vulnerable package is `liquidjs@10.25.7` or another intentionally vulnerable version below `10.26.0`;
- patched control is `liquidjs@10.26.0` or newer;
- vulnerable run writes only the synthetic marker inside the run artifact directory;
- patched control does not write the marker;
- no secrets, system files, callbacks, live targets, or destructive actions are touched.

## Live-target prerequisite mapping

For live bounty, this proof pattern is usable only when all are true:

- exact asset is in `config/scope.txt` and matching `programs/<slug>/scope.json`;
- program rules allow this class of manual owned-data proof;
- app demonstrably exposes attacker-controlled LiquidJS template input or equivalent template content path;
- proof can be constrained to operator-owned synthetic marker effects;
- execution stops before arbitrary command expansion, secret read, persistence, callback/OAST, lateral movement, or customer data contact;
- evidence is redacted and manually reviewed before report-ready promotion.

This bundle is a local proof pattern, not live authorization.
