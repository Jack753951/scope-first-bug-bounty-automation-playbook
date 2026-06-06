> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Phase 4A External Tool Adapter Pattern

Use this when adding modern external security tools (for example ProjectDiscovery `httpx`/`katana`, later `nuclei`, ZAP, or ffuf) to an authorized cybersecurity lab/bug-bounty platform.

## Core lesson

Do not jump from “GitHub tool exists” to “run it against a target.” Split external-tool support into two different boundaries:

1. **Offline importer** — reads reviewed tool output fixtures/captures and normalizes safe fields into non-promotional observations. It must not execute tools, open network connections, follow URLs, import raw response bodies, or emit confirmed/reportable findings.
2. **Bounded lab executor** — a separate, explicitly approved local-lab path that runs mature tools with strict target, rate, depth, timeout, health-check, redaction, and artifact controls.

This split lets the project improve modernity and extensibility without weakening scope gates or report-readiness discipline.

## Recommended first tools

Start with mature, structured-output tools rather than random exploit PoCs:

- `httpx` JSONL: low-risk HTTP metadata such as URL, status, title, content length, response time, and tech fingerprints.
- `katana` JSONL: crawler-discovered URLs with source relationships; useful for endpoint inventory, but needs depth/rate/scope limits.

Defer until stronger executor controls exist:

- `nuclei` live execution: requires template allowlist, intrusive/DoS/fuzz/OAST exclusion, rate/time limits, and candidate-only conversion.
- `ffuf`: requires tiny allowlisted wordlists, health checks, and request-volume controls.
- Random GitHub exploit scripts: require pinned commit/hash, static review, no callback/no destruction/no persistence/no credential/loot checks, local-lab-only scope, explicit operator approval, timeouts, and redaction.

## OSS Recon Gate decisions

For external-tool integrations, compare output contracts and defaults before implementation:

- `httpx`: ADAPT JSONL metadata shape and provenance fields; do not trust as finding evidence by itself.
- `katana`: ADAPT discovered-url/source relationships; do not automatically follow imported URLs.
- `nuclei`: ADAPT template ID/severity/provenance ideas, but defer live bulk execution.
- ZAP baseline/alert model: ADAPT confidence/evidence taxonomy later; do not copy scanner-confirmed semantics.
- `ffuf`: ADAPT JSON parser later; defer execution because fuzzing volume can stress targets.

## Offline importer contract

Minimum safety properties:

- Accept only allowlisted tools, initially `httpx` and `katana`.
- Accept only reviewed repo-local fixtures/captures, for example `tests/fixtures/external_tools/**/*.jsonl`, unless a later reviewed phase designs a broader artifact path contract.
- Parse JSONL fail-closed: malformed lines should produce an error and zero observations rather than partial unsafe promotion.
- Normalize only safe fields: target URL, HTTP method/status/title/content length/response time, selected tech tags, source relationship, line number, line hash, tool name/version if visible, run ID.
- Do not import raw response bodies, tokens, cookies, screenshots, or request/response dumps.
- Emit only non-promotional states such as `ok` and `observation`; never `confirmed`, `verified`, `reportable`, or `accepted`.
- Include explicit safety flags such as `network_io=false`, `subprocess_execution=false`, `promotes_findings=false`, and `imports_response_bodies=false`.

## TDD pattern

Write RED tests before the importer exists:

- `httpx` fixture imports as one or more `observation` records.
- `katana` fixture imports discovered URLs without following them.
- Unknown tool such as `random-exploit` is rejected.
- Non-allowlisted input path is rejected.
- Malformed JSONL fails closed with zero observations.
- Mock/patch subprocess and network APIs in tests to prove the importer is offline-only.
- Assert forbidden promotional vocabulary does not appear in status fields.

Then implement the minimal importer and run focused tests plus the project review wrapper.

## Bounded local-lab execution pattern

If the operator explicitly approves a local lab capture, run from the red-team Kali/tool VM, not from the victim VM. Keep Windows/Hermes as control plane.

Example limits for `httpx`:

```bash
httpx -l targets.txt \
  -status-code -title -tech-detect -content-length -response-time \
  -json -timeout 5 -retries 0 -rate-limit 2 -silent -no-color
```

Example limits for `katana`:

```bash
katana -u http://<lab-ip>:3000 \
  -depth 1 -rate-limit 2 -timeout 5 \
  -crawl-scope '^http://<lab-ip>:3000(/|$)' \
  -jsonl -omit-raw -omit-body -silent -no-color \
  -output katana.jsonl
```

Required executor-side controls before generalizing:

- pre-health and post-health checks
- scope/private-lab target validation
- per-step timeout
- rate/depth limits
- no raw body / no callback / no cloud upload
- artifact manifest
- redaction policy
- import step into offline observations
- candidate-only downstream conversion

## Tor/GitHub guidance

Using Tor Browser to view GitHub generally does **not** reveal more public scripts. It more often introduces CAPTCHA, login, rate-limit, and speed friction. Tor can be useful for privacy or network-source isolation, but it does not improve supply-chain trust. For finding modern tools, prefer GitHub search/API, project topics, recent releases, stars/freshness, and trusted ecosystems (ProjectDiscovery, OWASP, PortSwigger, reputable research teams), then apply the same static review and local-lab gates.

## Availability and health lessons

A bounded tool can still stress or reveal instability in a local lab. If service health degrades, stop active steps, capture which step preceded degradation, check target route/VM/container state, recover only because it is an owned lab, and convert the incident into executor requirements: health checks, timeout, kill/recovery, redaction, and audit logging. Do not interpret lab availability impact as permission to escalate.

## Result interpretation

Crawler/scanner output is inventory or triage. Even a modern tool result remains:

```text
scanner_output_only=true
manual_review_required=true
status=observation
```

Downstream candidate/report gates may use these observations, but they must not become confirmed/reportable without manual or agent-assisted verification, evidence review, impact analysis, remediation, and retest notes.
