> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Phase 4A.1 — Bounded Local-Lab Content Discovery Run Card

Date: 2026-05-21
Status: DRAFT_FOR_REVIEW

## Scope and authorization

- Scope class: local lab / intentionally vulnerable app only.
- Attacker VM: `<attacker-vm>`.
- Attacker IP: `<lab-ip>`.
- Victim VM: `<victim-vm>`.
- Target URL: `http://<lab-ip>:3000/`.
- Network: VirtualBox host-only network only.
- External targets: not authorized.

## Objective

Exercise the first aggressive-lab execution gate with a small, bounded path/content-discovery rehearsal. The goal is to validate controls, evidence discipline, and candidate-only output, not to maximize findings.

## Allowed action class

Allowed:

- HTTP `GET` or `HEAD` requests to a fixed short path list against `http://<lab-ip>:3000/` only.
- Collect only status code, content type, content length, redirect target, and a short title/header fingerprint.
- Pre/post health checks against `/` only.

## Explicitly forbidden

Forbidden in this slice:

- brute force / credential guessing / login attempts;
- exploit PoCs;
- SQLi/XSS/RCE/SSRF payloads;
- callbacks/OAST/webhooks/reverse shells/listeners;
- recursive crawling;
- recursive download;
- file content exfiltration or loot collection;
- POST/PUT/PATCH/DELETE requests;
- requests to any host other than `<lab-ip>:3000`;
- following off-target redirects;
- using the normal source Kali VM as attacker.

## Request cap / rate / timeout

- Max path probes: 30 paths.
- Max total HTTP requests including health checks: 34.
- Per-request timeout: 3 seconds.
- Delay between probes: 0.2 seconds.
- Overall command timeout from Hermes: 120 seconds.
- Stop immediately if pre-health check fails.
- Stop immediately if post-health check fails and mark result `LAB_HEALTH_DEGRADED`.

## Fixed path list

```text
/
/ftp/
/robots.txt
/sitemap.xml
/.well-known/security.txt
/api/
/rest/
/rest/products/search
/assets/
/assets/public/
/public/
/uploads/
/backup/
/backups/
/admin/
/administrator/
/login
/register
/profile
/account
/basket
/checkout
/api-docs
/swagger.json
/swagger-ui/
/debug
/server-status
/.git/HEAD
/package.json
```

The list intentionally includes common discovery paths but no payloads, no credentials, no traversal strings, and no recursive expansion.

## Evidence / output

Output directory:

```text
handoff/phase4a_1_bounded_content_discovery_run_20260521/
```

Artifacts:

- `run_card.md` — copy of this run card.
- `pre_health.txt` — pre-run `curl -I /` result.
- `observations.jsonl` — candidate-only per-path observations.
- `post_health.txt` — post-run `curl -I /` result.
- `summary.md` — human-readable summary.

Observation fields:

```json
{
  "schema": "phase4a_content_discovery_observation/1.0",
  "target": "http://<lab-ip>:3000",
  "path": "/robots.txt",
  "method": "HEAD_OR_GET",
  "status_code": 200,
  "content_type": "text/plain",
  "content_length": 123,
  "location": null,
  "candidate_only": true,
  "finding_status": "observation_not_finding"
}
```

No response bodies are stored except short headers/metadata. If a path appears sensitive, record metadata only and require a separate manual review gate.

## Kill conditions

Abort and record blocker if any occurs:

- target becomes unreachable before or during the run;
- more than 2 consecutive timeouts;
- any redirect points outside `<lab-ip>:3000`;
- command attempts to contact non-target host;
- output contains secrets, cookies, tokens, or full file contents;
- operator interrupts.

## Review decision requested

Reviewer should answer:

- Does this stay within local-lab authorization?
- Are request cap and timeout bounded enough for a first aggressive-lab rehearsal?
- Does the path list avoid exploit payloads, credentials, recursive download, and destructive behavior?
- Is candidate-only output preserved?
- Is execution allowed exactly as specified?

Expected verdict format:

```text
VERDICT: ACCEPT | REVISE | BLOCK
BLOCKING ISSUES:
NON-BLOCKING NOTES:
```
