> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Phase 4A External Tool Adapter Spike Result — 2026-05-20

Status: implemented and bounded-lab tested
Reviewer route/tool: Hermes OSS Recon Gate + TDD local implementation + red-team Kali bounded execution
Visible runtime model: not fully exposed by tool; Hermes session model label shown to operator as gpt-5.5
Review focus: external-tool adapter extensibility, safety gates, local-lab execution
Limitation: this validates httpx/katana adapter path only; it does not approve random exploit scripts, public targets, or bulk nuclei/ffuf execution.

## Implemented files

```text
scripts/import_external_tool_observations.py
scripts/run_external_tool_lab.py
scripts/test_external_tool_observation_importer.py
scripts/test_external_tool_lab_runner.py
tests/fixtures/external_tools/httpx_sample.jsonl
tests/fixtures/external_tools/katana_sample.jsonl
tests/fixtures/external_tools/malformed_sample.jsonl
tests/fixtures/external_tools/live_juice_shop_20260520/httpx.jsonl
tests/fixtures/external_tools/live_juice_shop_20260520/katana.jsonl
handoff/phase4a_external_tool_adapter_oss_recon_20260520.md
handoff/phase4a_external_tool_adapter_run_20260520/
```

## OSS Recon Gate decision

Decision: APPROVE_WITH_CHANGES for offline httpx/katana observation importer and bounded local-lab capture.

Deferred:

```text
random GitHub exploit scripts
nuclei bulk template execution
ffuf wordlist fuzzing
public target execution
automatic candidate/confirmed/reportable promotion
```

## TDD evidence

RED:

```text
python -m unittest scripts.test_external_tool_observation_importer -v
-> failed because scripts/import_external_tool_observations.py did not exist
```

GREEN:

```text
python -m unittest scripts.test_external_tool_observation_importer -v
-> 5 OK
```

Covered behavior:

```text
httpx JSONL -> non-promotional observations
katana JSONL -> discovered_url observations without following URLs
path allowlist rejects non-fixture inputs
malformed JSONL fails closed with zero observations
unknown tools such as random-exploit are rejected
```

## Importer safety posture

The importer is offline-only:

```text
network_io: false
subprocess_execution: false
promotes_findings: false
imports_response_bodies: false
```

Observation states remain:

```text
ok
observation
```

No `confirmed`, `verified`, `reportable`, or `accepted` status values are emitted.

## Bounded local-lab execution

Execution route:

```text
Windows Hermes control plane -> red-team Kali <lab-ip> -> Juice Shop target <lab-ip>:3000
```

Tools installed/used on red-team Kali:

```text
/home/kali/go/bin/httpx v1.9.0
/home/kali/go/bin/katana v1.6.1
```

Run output:

```text
/home/kali/phase4a-calibration/juice-shop-external-tools-20260520T115348Z
```

Copied safe artifacts:

```text
handoff/phase4a_external_tool_adapter_run_20260520/summary.md
handoff/phase4a_external_tool_adapter_run_20260520/httpx_observations.json
handoff/phase4a_external_tool_adapter_run_20260520/katana_observations.json
```

Limits:

```text
local lab only
httpx metadata only
katana depth=1
rate limit 2 req/sec
no raw response body
no callback
no nuclei/ffuf/exploit scripts
pre/post health checks
```

Counts:

```text
httpx_lines=1 -> imported observations=1
katana_lines=17 -> imported observations=17
```

Pre-health and post-health both returned HTTP 200 OK, so this bounded run did not reproduce the earlier availability failure.

## Reusable project capability retained

The one-off Kali helper used during the first capture remains under `setting/local/`, but the reusable project capability is now preserved in committed/tested scripts:

```text
scripts/run_external_tool_lab.py
scripts/import_external_tool_observations.py
```

`run_external_tool_lab.py` generates bounded local-lab httpx/katana execution plans by default and writes an executable bash script only with `--execute-lab-approved`. It rejects public targets, unknown tools, and unsafe limits, and preserves the learned defaults: pre/post health checks, rate/depth/time bounds, no raw body capture, no callbacks, and no promotion to findings.

## Extensibility result

This slice proves the project can safely ingest modern external-tool JSONL outputs through an adapter layer without trusting tool output as a finding.

Useful platform lessons:

```text
1. External tools need separate executor vs importer boundaries.
2. Importers should be offline and non-target-touching.
3. Runtime captures should be copied into reviewed/safe fixtures before downstream tests.
4. Tool provenance, line hashes, run IDs, and scanner_output_only flags are essential.
5. Crawler output expands endpoint inventory quickly even at depth=1, so execution needs scope/rate/health gates.
```

## Next safe step

Add a controlled lab execution adapter for external tools with:

```text
--execute-lab-approved
pre/post health checks
per-step timeout
rate/depth limits
scope regex validation
artifact manifest
redaction policy
candidate-only conversion
```

Only after that should nuclei allowlisted templates be tested. Random exploit scripts should require static review, pinned commit/hash, no-callback/no-destruction review, and local-lab-only execution.
