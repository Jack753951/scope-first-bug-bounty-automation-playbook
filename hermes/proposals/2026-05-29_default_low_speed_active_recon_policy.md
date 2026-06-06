> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Proposal — Make low-speed active recon a default tactical base

Status: accepted by operator on 2026-05-29; implemented in safety/validator/recon-profile slice
Created: 2026-05-29T10:27:48Z

## Problem

The current `SAFETY.md` one-sentence rule groups `scans/fuzzing/DAST/OAST/SSRF/exploit attempts/high-volume automation` together as stop-and-ask categories. This keeps live work safe, but it also makes low-speed active recon feel exceptional instead of a normal first-bounty tactic after exact scope and owned-data boundaries are already established.

## Desired operating change

Allow bounded, low-speed active recon as a default tactic only when all of the following are true:

1. Exact target is already authorized in both `config/scope.txt` and `programs/<slug>/scope.json`.
2. Program rules do not prohibit the technique.
3. Per-program `scope.json` explicitly permits the technique or lane state has operator approval for that technique class.
4. Requests are low-volume, rate-limited, non-destructive, non-evasive, and evidence-safe.
5. The recon avoids customer/non-owned data, secrets, credentials, cookies, tokens, OTPs, verification links, billing, payment, KYC, OAuth/integration activation, webhooks/callbacks/OAST/tunnels, SSRF, exploit chains, and final submission unless those actions are separately approved as standing A3 capabilities.
6. Out-of-scope controls fail closed before execution.
7. Tool output is redacted before promotion to handoff/report artifacts.

## Proposed `SAFETY.md` replacement sentence

Replace the current one-sentence rule with:

```text
Proceed only when the target and action are explicitly in `config/scope.txt` and `programs/<slug>/scope.json`, stay inside an operator-approved owned-data proof boundary, and are low-volume, reversible, and evidence-safe. Bounded low-speed active recon is allowed by default only for exact in-scope assets whose program rules and per-program scope file permit the specific technique, with fail-closed scope checks, conservative rate limits, no exploitation, no customer/non-owned data, no secrets/tokens/cookies/OTP/passwords/verification links, no callbacks/OAST/tunnels/SSRF, no destructive or stealthy behavior, and redacted evidence handling. Otherwise stop and ask before scope changes, credentials/secrets, non-owned/customer data, fuzzing beyond the approved low-speed profile, DAST beyond approved non-intrusive templates, OAST/SSRF/exploit attempts/high-volume automation, integrations/webhooks/API-token/payment/KYC/external side effects, report-ready promotion, public disclosure, or final submission.
```

## Technique taxonomy

### A1 passive/public — default

Examples:
- public docs and policy reading
- CT log diff
- disclosed report mining
- CVE/feed matching
- public source/static review

### A2 low-speed active recon — proposed default after exact scope approval

Examples:
- single-host HTTP metadata probe
- TLS/header/title/status/tech fingerprinting
- robots/sitemap/security.txt/.well-known fixed-path checks
- safe OPTIONS/HEAD/GET checks
- non-intrusive nuclei templates only
- tiny deterministic endpoint existence checks from public docs

Default caps:

```text
max_concurrency: 1-2
max_requests_per_second: 0.2-1.0
request_delay_ms: 1000-5000
max_requests_per_host_per_run: 50
max_runtime_per_host: 5-10 min
retries: 0-1
redirects: limited
randomization/evasion: none
```

### A3 bounded proof/discovery — lane-approved routine tier

A3 is now the single proof tier. It includes former A4 controlled actions when the lane has a standing capability record.

Examples:
- small wordlist directory/content discovery
- parameter name discovery against owned/sandbox object routes
- schema-guided API checks using public OpenAPI docs
- low-count negative-control authz checks with owned accounts
- API credential creation in owned accounts
- SSRF/OAST marker callback to operator-controlled receivers
- bounded exploit chains with marker-only or recoverable owned-state impact

Default caps:

```text
max_concurrency: 1
max_requests_per_second: 0.1-0.5
max_requests_per_host_per_run: 100-300
fixed allowlisted paths only unless operator approved broader wordlist
no recursive crawling by default
no mutation except approved owned objects
```

### Former A4 controlled actions — folded into A3

The separate A4 tier is deprecated. Actions previously labeled A4 are either:

- controlled A3 capabilities when exact scope, technique allowlist, caps, cleanup, and stop-before controls exist; or
- hard-stop actions when they would touch customer/non-owned data, extract secrets/credentials, enumerate internal networks, persist, evade, cause destructive impact outside recoverable owned state, or submit a report.

## Proposed `scope.json` additions

Each program should carry a machine-readable active recon profile:

```json
{
  "techniques": {
    "allowed": ["http_probe", "tls_fingerprint", "fixed_path_metadata", "nuclei_non_intrusive"],
    "forbidden": ["oast", "ssrf", "exploit_attempt", "credential_brute_force", "intrusive_fuzz", "dos"],
    "automation_permitted": true,
    "automation_profile": "A2_LOW_SPEED_ACTIVE_RECON",
    "automation_notes": "Exact in-scope hosts only; non-intrusive metadata and fixed-path checks; no authenticated mutation."
  },
  "rate_limits": {
    "max_concurrency": 1,
    "max_requests_per_second": 0.5,
    "request_delay_ms": 2000,
    "max_requests_per_host_per_run": 50
  }
}
```

## Engineering changes needed

1. Update `SAFETY.md` only after explicit operator approval.
2. Update `hermes/loops/hourly_diff.md` so A2 low-speed active recon is a normal scoped mode, not a special exception.
3. Add validator checks that reject active recon unless:
   - host is in `config/scope.txt`
   - host is in `programs/<slug>/scope.json`
   - technique is in `techniques.allowed`
   - technique is not in `techniques.forbidden`
   - automation profile is present
   - rate caps exist
4. Tune `config/recon.conf` defaults downward for live bounty mode:
   - `NAABU_RATE` lower for live targets or disabled unless allowed
   - `HTTPX_THREADS` lower
   - `NUCLEI_RATE_LIMIT` lower
   - keep `NUCLEI_EXCLUDE_TAGS=dos,intrusive,fuzz`
   - do not use `NUCLEI_EXCLUDE_TAGS_FULL` on live bounty targets
5. Add `--profile live-low-speed` / `--profile lab-aggressive` separation to recon wrappers if not already present.
6. Ensure every run writes audit metadata:
   - timestamp
   - program slug
   - exact host list
   - technique profile
   - request caps
   - scope check result
   - output path
   - redaction status

## Decision requested

Approve one of:

```text
approve safety proposal as written
approve A2 only, keep A3 fuzz/discovery operator-gated
revise proposal: <changes>
reject proposal
```

Recommended: approve A2 low-speed active recon as default for exact-scope lanes and use A3 as the standing lane-approved proof tier, including former A4 controlled actions.
