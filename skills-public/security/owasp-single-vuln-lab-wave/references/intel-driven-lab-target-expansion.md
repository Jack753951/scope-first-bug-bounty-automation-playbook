> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Intel-driven lab bundles and target expansion

Session-derived update: 2026-05-22

## What changed

The operator explicitly allowed downloading or modifying new local target environments when the current靶機 cannot cover useful modern vulnerability patterns. This does not remove scope/safety boundaries: new targets must be local, intentionally vulnerable, recoverable, and documented before target-touching tests run.

## Default decision sequence

1. Start with the current authorized lab target if it can still produce useful `verified-impact` or `valuable-candidate` bundles.
2. Use external intelligence (CISA KEV, NVD, Exploit-DB/searchsploit, GitHub PoCs/tooling, HTB/training-lab patterns, OWASP/CWE) to pick weakness patterns and proof types.
3. Run target-touching validation from `<lab-vm>`; Windows/Hermes stays the control plane for indexing, files, handoff, Obsidian, and synthesis.
4. If the current target lacks the needed surface, add or modify a local vulnerable target rather than repeatedly probing an unsuitable app.
5. Preserve both successful impact and useful non-successes as bundles with the correct status vocabulary.

## Keep as valuable bundles even without max impact

Retain a bundle when it records any reusable security value:

- false-positive controls (SPA/root fallback, reflected payload text vs runtime execution, 403 error-page traps);
- exploit preconditions and missing proof type;
- safe marker workflow for state-changing endpoints;
- unauth/auth/role differential workflow for future IDOR/BAC proof;
- mature tool routing, artifact naming, and evidence hygiene;
- a clear decision that a product-specific CVE is only pattern inspiration for this target.

Use statuses:

- `verified-impact`
- `valuable-candidate`
- `attempted-not-verified`
- `blocked/deferred`
- `reference-only`

## Wave 3 example pattern

A useful Juice Shop wave retained four bundles even without full RCE/control:

- KEV-style path/file-read variants: verified `/ftp` reads, blocked traversal controls, root-fallback suppression.
- Upload retrieval/validation: authenticated marker upload accepted; retrieval/RCE/arbitrary write not proven.
- Browser-backed XSS probe: Chromium workflow retained; runtime proof not yet conclusive.
- Auth/access boundary expansion: SQLi-derived admin token plus unauth/auth differentials for future IDOR work.

## When to add new local targets

Add or modify a local target when the current target cannot demonstrate the required proof cleanly:

- IDOR/API target for own-object vs other-object proof.
- Upload target for marker retrieval, content-type/extension checks, and safe execution-boundary proof.
- SSRF target plus isolated local callback service.
- XXE/deserialization target with explicit parser or serialized-object input surfaces.

Before testing a new target, document target role/IP/port, reset/snapshot or container reset command, pre/post health check, and scope entry. Disable or isolate internet/NAT before aggressive target-touching unless it is needed only for setup downloads.
