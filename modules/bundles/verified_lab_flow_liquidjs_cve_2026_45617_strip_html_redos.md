> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Verified Lab Flow — LiquidJS <specific-cve-id> strip_html ReDoS

Status: `verified_liquidjs_cve_2026_45617_strip_html_redos_local_lab`
Last verified: 2026-05-28
Source advisory: `<specific-ghsa-id>`
CVE: `<specific-cve-id>`
Package under test: `liquidjs@10.25.7` (`< 10.26.0` vulnerable; `10.26.0` patched control)
OWASP mapping: A06 Vulnerable and Outdated Components; availability/DoS via regex backtracking
Target lane: `local-learning-lab`

## When to use

Use this bundle when a target or source review shows attacker-controlled LiquidJS content flowing through the `strip_html` filter and the proof can be constrained to a local or authorized owned-data availability surrogate.

## Latest verified artifacts

```text
<artifact-output-dir>/three_latest_npm_vulns_20260528T110251Z/evidence/
```

Key evidence:

- `liquidjs_redos_proof.json`
- `summary.json`
- `posture.txt`

Latest values:

```text
status: verified
vulnerable_max_elapsed_ms: 5841.175
patched_max_elapsed_ms: 7.685
```

## Success criteria

- Vulnerable control uses `liquidjs@10.25.7` or another version below `10.26.0`.
- Patched control uses `liquidjs@10.26.0` or newer.
- The same synthetic input causes a materially larger render time in the vulnerable version than in the patched version.
- Execution remains local/recoverable and does not attempt uncontrolled resource exhaustion.

## Live-target prerequisite mapping

This is not live authorization. For bounty use, require exact scope, program rules permitting availability proof, a demonstrated attacker-controlled `strip_html` data-flow, small bounded payloads, manual observation, and operator review before report-ready promotion.
