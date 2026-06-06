> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Mature Tool Wrapper Wave — Local Lab Pattern

Use this reference from `owasp-single-vuln-lab-wave` when the operator asks for OWASP/local-lab module expansion and explicitly allows mature tooling.

## Durable workflow lesson

Do not categorically reject broad scanners, fuzzers, Burp/session workflows, TLS scanners, or aggressive/destructive tooling for the authorized disposable local lab. Instead, wrap/adapt mature tools behind gates:

- target must be the authorized recoverable local lab or another explicitly scoped disposable target;
- verify snapshot/recovery before aggressive/destructive waves;
- run NAT/network only for tool download/update when needed, record source/version/license, then return to host-only/lab execution where feasible;
- execute with fixed target/scope, timeout, rate/thread cap, and pre/post health checks;
- keep scanner/tool output candidate-only / needs_manual_review;
- never let scanner wording auto-promote to confirmed/reportable/submission language;
- preserve false-positive suppression metadata, not just candidates.

## TDD shape used successfully

Start with RED tests before adding wrappers:

- `--plan-only` emits JSON and does not require lab approval;
- `--out-script` refuses without `--lab-approved`;
- public targets fail closed even if the user asked for tooling generally;
- generated bash contains candidate-only status, health checks, parser, and artifact manifest;
- generated bash passes `bash -n`;
- wrapper Python passes `py_compile`.

## Wrapper design pattern

Create a shared helper for mature-tool modules instead of one-off scripts:

- module spec includes `slug`, OWASP mappings, tool name, wrapper decision (`wrap`/`adapt`), safety gates, command rendering, and parser signals;
- generated runner writes `observations.jsonl`, `possible_vulnerabilities.md`, `health.txt`, `summary.txt`, `artifact_manifest.txt`, and local raw tool output;
- raw tool output remains local lab artifact only;
- normalize candidates and controls into JSONL;
- possible-vulnerability summaries must include missing evidence before confirmation.

## Tool-specific lessons

### ffuf

Useful for sensitive/admin/metadata path discovery when constrained to a tiny static wordlist, rate cap, thread cap, and timeout.

Add SPA/default-fallback suppression: repeated HTTP 200 with identical dominant length should become control/suppressed output, not a candidate. Keep the suppression in observations so future review knows why it was ignored.

### Nikto

Nikto can briefly leave the lab app busy; use shorter `-maxtime`, command timeout, and a cooldown before post-health. If post-health fails on the disposable victim, restore snapshot and rerun the final wave.

Do not treat every Nikto line as a candidate. Prefer plugin-ID lines such as `[013587]` or `[999986]` as candidates, while metadata/informational lines become controls. Some versions append `.json` to `-output tool_raw.json`; keep parser tolerant and fall back to text.

### nmap

For this class, keep nmap fixed to a known lab host/port and selected HTTP NSE scripts. Treat open service/header fingerprinting as metadata/control unless it includes a specific risky disclosure requiring manual confirmation.

## Final verification checklist

- Focused tests pass.
- `py_compile` new wrappers/helper.
- `bash -n` generated runners.
- Final local-lab artifacts pulled back.
- Final pre/post health is good for each wrapper.
- Hermes review passes.
- Git staged check and strong-secret scan before commit.
- PR comment labels route/tool, model/runtime if visible, usage artifact path if produced, and candidate-only semantics.
