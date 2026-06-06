> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Phase 4B OWASP/CVE continuation run — 2026-05-22

Status: completed local-lab continuation / candidate-only / needs_manual_review
Run id: `phase4b_owasp_cve_continuation_20260521T232928Z`
Target: `http://<lab-ip>:3000/` only
Artifacts: `<artifact-output-dir>/phase4b_owasp_cve_continuation_20260521T232928Z/`

## Scope and controls

- Scope checked against `config/scope.txt`: `<lab-ip>/16` private lab range is allowed.
- No public/real targets were touched.
- Fixed path lists only, GET-only probes, bounded timeout, no recursion/crawling, no callbacks/OAST, no credentials, no brute force, no exploit payloads, no destructive action, no raw secret/loot retention, and no finding/report promotion.
- Post-run lab health: `post_health=200`.

## Waves completed

### 1. `lab_auth_surface_no_bruteforce`

Added adapter and bundle for authentication-surface metadata without credential attempts.

Candidate-only result:

- `/rest/admin/application-configuration` returned status 200 with auth-surface keywords and needs manual review.

Controls:

- `/api/Users` returned 401 and was recorded as access-control observed.
- `/login` and `/#/login` were generic root/SPA fallback controls.
- `/rest/user/login` returned 500 and remains an error/robustness observation, not a bypass.

### 2. `lab_component_metadata_triage`

Added adapter and bundle for vulnerable/outdated component metadata and Retire.js/npm/OSV-style follow-up clues.

Candidate-only result:

- `/rest/admin/application-version` returned status 200 with version/package metadata clues and needs manual review.

Controls:

- package-manifest paths such as `/package.json`, `/package-lock.json`, `/yarn.lock`, `/bower.json`, `/assets/package.json` were generic SPA/root fallback controls in this run.
- No CVE is claimed from the version clue alone.

### 3. `lab_integrity_metadata_triage`

Added adapter and bundle for software/data integrity metadata: security.txt, robots, manifest/service-worker/static integrity clues.

Candidate-only results:

- `/.well-known/security.txt`, `/security.txt`, and `/robots.txt` returned status 200 with security/policy/disallow style metadata and need manual review.

Controls:

- `/manifest.json`, `/ngsw.json`, `/service-worker.js`, `/sw.js`, `/integrity.json`, and `/.well-known/change-password` were generic SPA/root fallback controls.

### 4. `lab_api_docs_metrics_manual_verification`

Added a checklist mini-bundle to convert the existing `/api-docs` and `/metrics` exposure outputs into manual verification steps and A09 logging/monitoring evidence questions. This wave does not add new network requests beyond prior artifacts; it records what must be verified manually before findings/report language.

## Files changed/added

- `scripts/lab_modules/lab_auth_surface_no_bruteforce.py`
- `scripts/lab_modules/lab_component_metadata_triage.py`
- `scripts/lab_modules/lab_integrity_metadata_triage.py`
- `scripts/test_phase4b_three_exposure_bundles.py`
- `setting/local/lab_auth_surface_no_bruteforce_run.sh`
- `setting/local/lab_component_metadata_triage_run.sh`
- `setting/local/lab_integrity_metadata_triage_run.sh`
- `modules/bundles/lab_auth_surface_no_bruteforce.md`
- `modules/bundles/lab_component_metadata_triage.md`
- `modules/bundles/lab_integrity_metadata_triage.md`
- `modules/bundles/lab_api_docs_metrics_manual_verification.md`
- `scripts/SCRIPT_INVENTORY.md`
- `handoff/owasp_2017_2021_2025_single_vuln_modularization_tracker_20260521.md`
- `handoff/active_strategy_queue.md`
- `handoff/accepted_changes.md`
- `handoff/phase4b_owasp_cve_continuation_run_20260522.md`
- `notes/daily/2026-05-22.md`

## Validation

- Focused tests: `python -m unittest scripts.test_phase4b_three_exposure_bundles -v` passed.
- Python compile: `python -m py_compile` passed for the new adapters/common/test files.
- Generated runners: `bash -n` passed for all three new runners.
- Local-lab execution: all three generated runners exited 0.
- Post-health: HTTP 200.
- Static review: `HACKLAB=$(pwd) ./bin/hermes review` passed; Python compile OK for 100 files, all shell scripts `bash -n` OK, lock clear, 12 scope entries.
- Git status: reviewed; this work plus several already-untracked Phase 4B files remain uncommitted.

## Deferred / uncertainty

- Retire.js/npm audit/OSV/Dependency-Check integration remains manual/deferred; this run only collected metadata clues.
- API-docs and metrics verification remain manual checklist work; no reportable finding language is claimed.
- XXE/deserialization remain checklist/probe-only future lanes because safe parser/input surfaces were not established in this bounded run.
- SSRF/OAST remains plan-only/blocked unless a fully isolated callback lab is built.
