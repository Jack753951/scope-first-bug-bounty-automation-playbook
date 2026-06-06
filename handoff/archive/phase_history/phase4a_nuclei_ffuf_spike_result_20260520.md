> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Phase 4A Nuclei + FFUF Bounded Lab Spike Result — 2026-05-20

Status: implemented, bounded-lab tested, and modularized
Reviewer route/tool: Hermes TDD implementation + red-team Kali bounded execution
Visible runtime model: not fully exposed by tool; Hermes session model label shown to operator as gpt-5.5
Review focus: modern external-tool capability growth, modular runner/importer safety, local-lab target health
Limitation: local Juice Shop lab only; this does not approve random exploit scripts, public targets, bulk nuclei templates, or broad ffuf wordlists.

## Why these tools

```text
nuclei: modern template engine widely used in bug-bounty/recon pipelines; tested only with a local one-request informational template.
ffuf: practical high-signal content discovery/fuzzing tool; tested only with a seven-word tiny lab wordlist and rate limit.
```

## Modularized project capability

Updated reusable project modules:

```text
scripts/run_external_tool_lab.py
scripts/import_external_tool_observations.py
scripts/test_external_tool_lab_runner.py
scripts/test_external_tool_observation_importer.py
```

New fixture examples:

```text
tests/fixtures/external_tools/nuclei_sample.jsonl
tests/fixtures/external_tools/ffuf_sample.json
```

Live safe captures copied into repo:

```text
tests/fixtures/external_tools/live_juice_shop_nuclei_ffuf_20260520/nuclei.jsonl
tests/fixtures/external_tools/live_juice_shop_nuclei_ffuf_20260520/ffuf.json
```

Imported observations:

```text
handoff/phase4a_nuclei_ffuf_run_20260520/nuclei_observations.json
handoff/phase4a_nuclei_ffuf_run_20260520/ffuf_observations.json
```

Plan artifact:

```text
handoff/phase4a_nuclei_ffuf_lab_plan_20260520.json
```

## TDD evidence

RED was observed before implementation:

```text
python -m unittest scripts.test_external_tool_lab_runner scripts.test_external_tool_observation_importer -v
-> failed because nuclei/ffuf were not supported yet
```

GREEN after implementation:

```text
python -m unittest scripts.test_external_tool_lab_runner scripts.test_external_tool_observation_importer -v
-> 10 OK
```

## Safety boundaries encoded

Runner behavior:

```text
plan-only by default
--execute-lab-approved required before executable script write
local/private target only
unknown tools rejected
rate_limit <= 10
timeout <= 30
katana depth <= 2
pre-health and post-health included
nuclei uses a generated local info template only
nuclei uses -omit-raw so request/response bodies are not retained
ffuf uses a tiny seven-word generated wordlist
no /usr/share/wordlists broad wordlist
no nuclei template bulk execution
no interactsh/OAST
no ffuf recursion
no dump/os-shell/callback/loot
no report submission
```

Importer behavior:

```text
nuclei JSONL -> template_observation
ffuf JSON -> content_discovery_hit
scanner_output_only: true
manual_review_required: true
no network I/O
no subprocess execution
no response body import
no confirmed/verified/reportable/accepted status
```

## Bounded local-lab execution

Route:

```text
Windows Hermes control plane -> red-team Kali <lab-ip> -> Juice Shop <lab-ip>:3000
```

Red-team Kali output path:

```text
/home/kali/phase4a-calibration/juice-shop-nuclei-ffuf-20260520T123255Z
```

Tool versions observed before run:

```text
nuclei v3.8.0
ffuf 2.1.0-dev
```

Run limits:

```text
nuclei: one generated local info template, one GET, -jsonl, -omit-raw, -rl 2, timeout 5, retries 0
ffuf: seven generated words, -rate 2, timeout 5, maxtime 30, JSON output
```

Health:

```text
pre-health: HTTP/1.1 200 OK
post-health: HTTP/1.1 200 OK
current health after run: HTTP/1.1 200 OK
```

## Observed results

Nuclei:

```text
1 local info template observation
raw request/response absent after adding -omit-raw
```

FFUF:

```text
7 content-discovery hits from the tiny wordlist:
- /ftp -> 200, length 11318
- /assets -> 301 -> /assets/
- /rest -> 500, length 2992
- /api -> 500, length 2990
- /administration -> 200, length 9903
- /robots.txt -> 200, length 28
- /security.txt -> 200, length 475
```

Interpretation:

```text
These are observations/candidate leads only. They are useful for route inventory and later manual review, but not confirmed vulnerabilities.
```

## Runtime issue caught and fixed

The first nuclei attempt used:

```text
-interactions-cache-size 0
```

Nuclei v3.8.0 panicked:

```text
panic: gcache: Cache size <= 0
```

Fix:

```text
Use -interactions-cache-size 1 and -omit-raw.
```

This was encoded into the runner and covered by the focused test.

## Capability gain

Project capability increased from http metadata/crawling to:

```text
safe template-engine observations via nuclei
bounded tiny-wordlist content discovery via ffuf
safe offline import of nuclei/ffuf outputs
explicit non-promotional observation gate
runtime pitfall captured in reusable runner defaults
```

## Next useful rung

Candidate next modules:

```text
1. ZAP baseline/passive importer only, before live execution.
2. Feroxbuster/gobuster comparison through the same tiny-wordlist boundary.
3. Nuclei allowlisted-template registry with local YAML fixture validation before any real template pack use.
```
