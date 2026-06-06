> Public filtered Obsidian memory export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Work Record 2026-05-21

Status: session closeout / durable project memory
Date: 2026-05-21 22:41 local
Repo truth: `<user-home>`, `handoff/accepted_changes.md`, `scripts/SCRIPT_INVENTORY.md`
Related notes:

- [[../01_Methodology/Phase 4B Script-first Architecture Reset 2026-05-21|Phase 4B Script-first Architecture Reset 2026-05-21]]
- [[../01_Methodology/Module Bundle Distinction and Service Scanner Direction 2026-05-21|Module Bundle Distinction and Service Scanner Direction 2026-05-21]]
- [[Phase 4B Three Exposure Bundles 2026-05-21|Phase 4B Three Exposure Bundles 2026-05-21]]

## Session summary

Today consolidated the cybersec lab direction around a practical script-first / bundle-first workflow:

```text
script/tool -> bundle -> module
```

The important architectural decision is that `module.json` and heavier contracts are guardrails/report-integrity layers, not the operator-facing path during the learning stage. Useful workflows should first be proven as scripts and bundles against the authorized disposable local lab, then only later promoted into formal modules after their input/output, false-positive controls, safety boundaries, and verification expectations stabilize.

## Technical lessons captured

### 1. Bundle-first modularization is the right current layer

A bundle is now treated as the tactical reusable layer:

- human-readable workflow;
- script combination and command library;
- candidate-only interpretation guidance;
- artifacts and manual verification requirements;
- false-positive controls;
- mature OSS references.

A formal module is treated as a later graduation state, not the starting point.

### 2. False-positive suppression is mandatory for web exposure scanners

Juice Shop / SPA-router behavior can return HTTP 200 for many nonexistent paths. Therefore these bundle runners now compare response body hashes against `/` root and downgrade identical bodies to generic root/SPARouter fallback controls.

This prevented false positives for:

- service baseline probes such as Tomcat/Apache/HAProxy paths;
- source-map disclosure paths;
- Swagger/OpenAPI alternate paths;
- metrics alternate paths.

### 3. Windows Git-Bash runner compatibility

On this Windows Hermes/Git-Bash setup:

- `python` points to the active Hermes venv;
- `python3` may resolve to the WindowsApps shim and exit 49 for heredoc/stdin scripts.

Generated bash runners should therefore use:

```bash
python - "$outdir" <<'PY'
```

rather than:

```bash
python3 - "$outdir" <<'PY'
```

### 4. Service baseline scanner lessons

The `lab_service_baseline_targets` bundle tested Apache/Tomcat/OpenSSL/HAProxy/Envoy/Traefik-style baseline probes.

Runtime fixes included:

- quote service paths such as `'/;csv'` to avoid shell command splitting;
- preserve embedded Python newlines in generated bash;
- treat `Cipher is (NONE)` / no peer certificate on a plaintext HTTP port as a TLS control, not a TLS candidate;
- classify root-body-equivalent service paths as SPA fallback controls.

### 5. Three exposure bundles added

Three additional OWASP/CVE-usable exposure triage bundles were added and run against the local lab:

1. `lab_api_docs_exposure_triage`
2. `lab_metrics_exposure_triage`
3. `lab_source_map_disclosure_triage`

Candidate-only results:

- `/api-docs` and `/api-docs/` exposed Swagger UI markers.
- `/metrics` exposed Prometheus-style metrics markers.
- No source-map disclosure candidate remained after root-fallback filtering.

All remain candidate-only and require manual verification/redacted evidence before any report language.

## Mature OSS/tool references captured

The bundles now reference mature OSS tooling for later wrap/adopt/reference decisions:

- OWASP ZAP
- nuclei
- ffuf
- dirsearch
- Prometheus/promtool
- Retire.js
- SecretFinder
- trufflehog
- LinkFinder

Current decision: reference/wrap mature tools later, but start with fixed GET-only local-lab probes and no broad template execution by default.

## Engineering role split to remember

Preferred project role split:

- Hermes: coordinator, safety gate, memory/handoff keeper, verifier, and final synthesis.
- Claude Code Impl: primary code-engineering implementation support for nontrivial local/offline engineering slices, especially where visible implementation worker output and usage JSON are useful.
- Codex: surgical fallback, deterministic fixes, secondary review, script safety, validation, and automation.
- Cowork/Claude strategy: direction, research synthesis, documentation cleanup, architecture review, and independent review.

This is now also reflected in Hermes global project signpost memory: cybersec/hacking should keep script-first/context-driven bundles, with Claude Code Impl as primary code-engineering support and other agents as review/fallback.

## Current state at closeout

Validation passed for the latest bundle work:

```text
python -m unittest scripts.test_phase4b_three_exposure_bundles scripts.test_service_baseline_targets scripts.test_owasp_tool_wrapper_modules -v
# Ran 9 tests — OK

python -m py_compile ...
# OK

bash -n generated runners
# OK

HACKLAB=$(pwd) ./bin/hermes review
# Python Compile OK, Shell Scripts OK, Lock clear, Recon Scope 12 entries
```

Primary project files updated today include:

- `scripts/lab_modules/web_exposure_common.py`
- `scripts/lab_modules/lab_api_docs_exposure_triage.py`
- `scripts/lab_modules/lab_metrics_exposure_triage.py`
- `scripts/lab_modules/lab_source_map_disclosure_triage.py`
- `scripts/lab_modules/lab_service_baseline_targets.py`
- `scripts/test_phase4b_three_exposure_bundles.py`
- `scripts/test_service_baseline_targets.py`
- `modules/bundles/lab_api_docs_exposure_triage.md`
- `modules/bundles/lab_metrics_exposure_triage.md`
- `modules/bundles/lab_source_map_disclosure_triage.md`
- `modules/bundles/lab_service_baseline_targets.md`
- `handoff/phase4b_three_exposure_bundles_run_20260521.md`
- `handoff/service_baseline_targets_run_20260521.md`

## Suggested next session

Start with manual verification mini-bundles for:

1. `/api-docs`
   - verify unauthenticated access;
   - inspect redacted endpoint/schema impact;
   - decide whether it is only learning signal or report candidate.

2. `/metrics`
   - inspect first safe/redacted lines;
   - classify app vs infrastructure telemetry;
   - avoid raw sensitive labels/secrets in git.

Then decide whether to keep expanding exposure bundles or switch to a known intentionally vulnerable Juice Shop class such as auth/SQLi/path traversal with the same script-first bundle strategy.

## Closeout note

No public/real bug bounty activation happened today. All target-touching work stayed inside the authorized local lab and remained candidate-only.
