> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Phase 4A External Tool Adapter OSS Recon Gate — 2026-05-20

Status: design-approved for offline adapter spike; live execution remains local-lab bounded only
Reviewer route/tool: Hermes OSS Recon Gate + local repository inspection + GitHub metadata lookup
Visible runtime model: not fully exposed by tool; Hermes session model label shown to operator as gpt-5.5
Review focus: external-tool integration, schema compatibility, safety gates, extensibility
Limitation: this is design/adapter guidance, not approval for arbitrary third-party exploit execution

## Proposed change

Introduce an offline importer for mature third-party web-recon tool outputs, starting with:

- ProjectDiscovery httpx JSONL
- ProjectDiscovery katana JSONL

The importer normalizes tool output into a local observation packet that can later feed model review, candidate packet creation, and report-readiness gates without making scanner output a confirmed finding.

## Review tier

T3/T4 boundary: external tool integration and runner-boundary-adjacent work.

This slice is approved only as:

```text
offline importer + committed fixtures + bounded local-lab execution notes
```

It is not approval for generic live execution, public targets, callbacks, heavy fuzzing, random exploit PoCs, or automatic reportable findings.

## OSS references considered

### ProjectDiscovery httpx

- Useful pattern: JSONL output, per-input HTTP metadata, status/title/tech/content-length/response-time fields, composable pipeline usage.
- Adopt/adapt/ignore: ADAPT.
- Safety concern: httpx normally touches targets; in this project, importer must be offline and live execution must be separately gated.
- Contract impact: add observation provenance fields (`tool.name`, `tool.version`, `raw_field_subset`) and target URL normalization; do not promote to finding.

### ProjectDiscovery katana

- Useful pattern: crawler-discovered URLs as JSONL events with source/input relationships and method/status metadata.
- Adopt/adapt/ignore: ADAPT.
- Safety concern: crawler depth and JavaScript parsing can expand scope or stress targets; live use requires depth/rate/scope gates.
- Contract impact: add `relationship: discovered_url`, `parent/source` fields, and scope-retention checks.

### ProjectDiscovery nuclei

- Useful pattern: templates with IDs, metadata, severity, references, matcher/extractor concepts.
- Adopt/adapt/ignore: DEFER live execution; ADAPT schema lessons.
- Safety concern: templates vary from informational to intrusive/OAST/DoS-capable; never run bulk templates without allowlist, tag exclusion, rate/time limits, and no callback.
- Contract impact: future importer should keep template ID/severity/provenance but set status to `observation` or `candidate` only after review.

### OWASP ZAP alert model

- Useful pattern: alert risk/confidence/evidence fields and web scanner taxonomy.
- Adopt/adapt/ignore: ADAPT for later report-review comparison.
- Safety concern: ZAP active scan can be intrusive; baseline/passive alerts still require triage.
- Contract impact: useful reference for confidence and evidence text, but do not copy scanner-confirmed semantics.

### ffuf

- Useful pattern: JSON output for content discovery, status/size/word/line counts.
- Adopt/adapt/ignore: DEFER execution; ADAPT output parser later.
- Safety concern: fuzzing/wordlists can create high request volume; requires tiny allowlisted wordlists and health checks.

## Contract impact summary

- Program scope: no change; external outputs must remain under authorized/local lab scope before downstream use.
- Policy decisions: no live execution in importer; separate lab execution adapter must produce policy decision/audit artifact.
- Finding schema: no direct finding creation in this slice.
- Evidence schema: observation packet references raw tool line hash and selected safe fields only.
- Run manifest: include tool name, tool version if visible, source file, imported count, dropped count, errors.
- Module manifest/profile: future plugin profiles should declare `network_touching: false` for importer and `network_touching: true` for executor.
- Dry-run runner: preserve plan-only/default-deny behavior.

## Safety decision

- Offline-only preview possible: yes.
- Requires active behavior: no for importer; yes only for separate bounded local-lab capture.
- Requires new policy gate: yes before generalized live execution.
- Requires schema migration: no; keep trial observation schema local until two consumers exist.

## Implementation guidance

Implement now:

- `scripts/import_external_tool_observations.py`
- committed fixtures under `tests/fixtures/external_tools/`
- focused unittest coverage for httpx/katana JSONL, path allowlist, malformed JSON, and non-promotional vocabulary

Defer:

- nuclei live execution
- ffuf execution
- random GitHub exploit scripts
- automatic candidate promotion
- public target support

Required tests:

- importer rejects paths outside `tests/fixtures/external_tools` unless explicitly allowed later
- importer performs no subprocess/network calls
- output contains no `confirmed`, `verified`, `reportable`, or `accepted` status values
- malformed JSONL lines become errors and do not produce partial unsafe promotion
- katana-discovered out-of-scope/public URLs are marked/dropped by scope classifier in future runner; for this slice, record as observations only

Unsafe defaults to prevent:

- importing raw response bodies, tokens, cookies, secrets
- following discovered URLs automatically
- running third-party tools from importer
- trusting scanner severity as final severity

## Decision

APPROVE_WITH_CHANGES:

Proceed with offline httpx/katana importer and optional bounded local-lab execution capture from red-team Kali. Keep nuclei/ffuf/random exploit scripts deferred until importer, health gates, and allowlists are stronger.
