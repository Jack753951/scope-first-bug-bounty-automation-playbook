> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Corrected latest-vulnerability lane — 2026-05-27

## Correction

Operator is right: the latest-vulnerability lane should not use a 2025 CVE as the primary lane when the goal is freshness. The previously created Next.js <specific-cve-id> detector is retained only as a reusable/reference fallback, not the active latest-vulnerability lane.

## Source checked

GitHub Security Advisories npm ecosystem, current critical advisories visible for 2026-05. Examples observed:

- 2026-05-21 <specific-cve-id> Boxlite path traversal arbitrary host file write.
- 2026-05-19 <specific-cve-id> 9router unauthenticated RCE via MCP custom plugin routes.
- 2026-05-14 <specific-cve-id> n8n XML node prototype pollution patch bypass.
- 2026-05-14 <specific-cve-id> n8n arbitrary file read via Git node.
- 2026-05-14 <specific-cve-id> n8n HTTP Request node pagination prototype pollution to RCE.
- 2026-05-14 <specific-cve-id> Flowise authenticated host RCE.
- 2026-05-14 <specific-cve-id> Strapi relational filtering sensitive data leak.
- 2026-05-13 <specific-cve-id> Strapi SQLi in content-type-builder.
- 2026-05-12 <specific-cve-id> SillyTavern path traversal.
- 2026-05-12 <specific-cve-id> SillyTavern SSO header authentication bypass.
- 2026-05-08 <specific-cve-id> Cline Kanban cross-origin websocket hijacking.

## Multi-agent correction result

Primary 2026 latest-vuln lane:

```text
<specific-cve-id> — Strapi relational filtering sensitive data leak
```

Reason:

- Published in 2026-05, within the requested 1-2 month freshness window.
- Strapi is common enough in bug-bounty web/API scopes.
- Local lab can be built with synthetic public/private content relationships.
- Detector can start as safe local behavior proof, then live transfer can be passive/fingerprint or explicitly authorized synthetic-data checks only.
- Better first-bounty relevance than supply-chain/malware advisories.

## Why not use the other 2026 candidates as primary

- n8n / Flowise RCE/file-read/prototype-pollution lanes: high impact, but live testing is invasive and likely requires auth/workflow creation; good local-lab research, not first live scanner.
- 9router MCP RCE: severe but niche and unsafe to test live without explicit target authorization.
- Boxlite path traversal/write: potentially high impact but lower prevalence and write-path behavior is dangerous live.
- Strapi SQLi: strong but narrower/riskier than relational-filtering leak for a first detector.
- SillyTavern auth/path traversal: likely niche and often consumer/local deployments, lower H1 prevalence.
- Cline Kanban websocket hijack: interesting devtool lane, but more specialized.
- sanitize-html XSS: good fallback, but needs content injection/rendering context and can drift into stored XSS proof complexity.

## Safe local-lab design for <specific-cve-id>

Build a disposable Strapi target with:

- public collection type: `article`
- restricted/private related collection: `secretNote` or `internalProfile`
- seed data:
  - public article with relation to private note
  - public article without relation
  - private note containing harmless marker only, e.g. `STRAPI_REL_FILTER_CANARY_<random>`
- unauthenticated/public role with normal API access only to public article fields.

Proof pattern:

1. Baseline public article query returns only allowed public fields.
2. Control query for private collection directly is denied or redacted.
3. Relational filtering query attempts to influence results through related private fields.
4. Local proof is only verified if the query result reveals existence/value-dependent behavior of private relation that should not affect public result.
5. No real secrets; marker-only synthetic data.

## Detector/live-transfer rule

Live detector must not extract private data.

Allowed live modes, only after scope/rules check:

1. passive fingerprint:
   - detect likely Strapi (`/admin`, `/api/*`, Strapi headers/assets, admin bundle hints);
   - no vulnerability claim.
2. operator-supplied synthetic object check:
   - only against owned Strapi instance or program-provided sandbox;
   - only marker data created by us;
   - candidate-only output.

Blocked live modes:

- enumerating real collections;
- querying unknown private fields;
- trying to infer real customer/admin data;
- SQLi/RCE/file-read probing;
- broad path/endpoint fuzzing without explicit program allowance.

## Current action

Replace the active latest-vulnerability lane with <specific-cve-id>. Keep the existing Next.js 2025 detector artifact as `reference/fallback`, not as the freshness lane.
