> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Web Exposure Bundle Wave Lessons

Session-derived class-level pattern for lightweight OWASP/CVE-usable exposure bundles such as API documentation, metrics/observability, and JavaScript source-map disclosure checks.

## When this applies

Use this pattern when the operator asks for more OWASP/CVE-oriented lab checks and the safest useful first step is not an exploit PoC, but a bounded exposure triage bundle that can later feed manual verification or a formal module.

Good bundle candidates:

- Swagger/OpenAPI/API docs exposure (`A05`, API inventory/management leads).
- Metrics/Prometheus/Actuator exposure (`A05`, contextual observability/monitoring risk).
- JavaScript source-map/client artifact disclosure (`A05`, sometimes `A06` dependency/version leads).

Default stance: exposure scanners produce leads, not findings. Most require context and manual impact analysis before report language.

## Implementation shape

1. Build a shared fixed-path GET-only helper when several exposure checks share logic.
2. Each adapter should default to plan JSON only.
3. Require explicit lab approval before rendering a runner.
4. Reject public targets fail-closed unless a separate authorized-assessment gate exists.
5. Store only bounded metadata by default: status, content type, content length, hashes, candidate signal, and short details.
6. Emit:
   - `observations.jsonl`
   - `http_probe_results.jsonl` or equivalent normalized probe output
   - `possible_vulnerabilities.md`
   - `summary.txt`
   - `artifact_manifest.txt`
   - `tool_stdout.txt` / `tool_stderr.txt`
7. Use candidate-only wording everywhere.

## False-positive suppression

A critical control for modern SPAs and catch-all routers:

- Fetch `/` and hash the root body.
- For every candidate path, compare response-body hash to the root hash.
- If HTTP 200 but body hash equals root body, downgrade to `generic_root_fallback_control` unless there is strong class-specific evidence.

Do not treat HTTP 200 alone as meaningful for:

- `/swagger`, `/openapi.json`, `/main.js.map`, `/metrics`, etc.
- inferred `.js.map` paths from bundled app assets.
- framework/catch-all routes that serve the same HTML shell.

## Candidate logic examples

API docs candidates need more than status code, e.g. keywords such as:

- `swagger`
- `swagger-ui`
- `openapi`
- `paths`
- `components`

Metrics candidates need metrics-like markers, e.g.:

- `# HELP`
- `# TYPE`
- `process_`
- `nodejs_`
- `http_`

Source-map candidates need source-map-like content, e.g.:

- JSON-ish source-map structure
- `sources`
- `sourcesContent`
- `mappings`
- `webpack`
- body hash differs from root

## Mature OSS references to record

Use OSS Recon Gate but keep first runs fixed-path and low-impact. Record tools as `wrap/reference` unless actually vendored/executed.

API docs:

- OWASP ZAP — OpenAPI import and passive API review.
- nuclei — allowlisted exposure templates after scope gate.
- ffuf — bounded API docs path discovery.
- dirsearch — reference-only alternative path discovery.

Metrics:

- Prometheus/promtool — offline Prometheus text-format sanity.
- nuclei — exposed metrics templates after scope gate.
- ffuf — bounded path discovery.
- OWASP ZAP — passive metadata review.

Source maps / client artifacts:

- Retire.js — client-side dependency/CVE hint review after asset inventory.
- SecretFinder — reference-only unless redaction/loot hygiene is explicit.
- trufflehog — offline redacted secret-pattern review only.
- LinkFinder — reference-only endpoint extraction from JS assets; verify license before vendoring.

## Manual verification gate

Before any report candidate:

- Verify unauthenticated reachability.
- Capture redacted evidence only.
- Determine whether exposed content is meaningful to an attacker.
- Identify whether the data is app-level, infrastructure-level, dependency/version evidence, or harmless.
- Keep raw secrets, tokens, labels, full response bodies, source maps, and proprietary artifacts out of git/handoff unless a separate evidence hygiene decision allows it.

## Pitfalls

- Over-mapping exposure leads to CVEs. API docs/metrics/source maps are usually misconfiguration or information exposure leads, not CVEs by themselves.
- Treating SPA fallback 200s as findings. Root-body hash suppression is mandatory for these bundles.
- Running broad templates too early. Start fixed-path in the local lab, record mature tools, and only broaden under scope/recovery/rate gates.
- Keeping raw response bodies. Store hashes and redacted/manual evidence instead.
