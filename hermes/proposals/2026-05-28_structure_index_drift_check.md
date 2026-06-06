> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Proposal — Structure/index drift check after hacking2 restructure

Date: 2026-05-28
Status: proposal / operator decision needed

## Summary

`bin/hermes doctor` and `bin/hermes status` pass, so the Hermes-as-primary control path is operational. However, the repository is not yet fully normalized against `INDEX.md`; it still carries legacy tracked top-level zones and a few untracked/local artifacts that can recreate the old `hacking` sprawl if left unmanaged.

## Checks performed

- `bash ./bin/hermes doctor` → passed.
- `bash ./bin/hermes status` → passed; active live lanes empty, daily sweep ok.
- JSON parse check over `handoff`, `hermes/state`, `programs`, `modules/_schema` → passed.
- `git diff --check` → passed; only CRLF warnings on modified markdown.
- Handoff root markdown files → only current allowed files observed: `accepted_changes.md`, `current_navigation.md`, `operator_inbox_20260528.md`.

## Findings

### Operationally OK

- Required read files exist.
- Hermes runtime state files exist.
- Active lane queue parses and is empty.
- Handoff root is compact and not currently spawning dated strategy variants.

### Index/drift risks

1. `INDEX.md` canonical map omits existing tracked top-level areas from the old repo, including at least:
   - `cves/`, `fixtures/`, `schemas/`, `targets/`, `templates/`, `tools/`, `skills/`, `public_exports/`, `pictures/`
   - root files: `PROJECT_CHARTER.md`, `bugbounty_report_template.md`

2. Existing top-level local/runtime dirs are present and mostly ignored, but not described in `INDEX.md`:
   - `.claude/`, `.n/`, `.playwright-mcp/`, `.pytest_cache/`, `__pycache__/`, `<artifact-output-dir>/`, `tmp/`, `setting/`

3. Untracked files currently visible:
   - `.claude/settings.local.json` — local Claude permissions; should probably be ignored or explicitly governed.
   - `hermes/state/latest_liquidjs_package_cache.txt` — runtime pointer from the LiquidJS proof; likely should be ignored or folded into tracked proof docs.
   - `labs/proofs/liquidjs_rce_cve_2026_45618_marker_proof_20260528.md` — new proof packet; should be reviewed and tracked if accepted.
   - `modules/bundles/verified_lab_flow_liquidjs_cve_2026_45618_marker_rce.md` — new reusable bundle; should be reviewed and tracked if accepted.

4. Forbidden-pattern scan found two historical archived files:
   - `handoff/archive/cleanup_20260528/periodic_reviews/review_template_v0.md`
   - `skills/.archive/INSTALL_old.md`

These are not active-root drift, but they show that the weekly drift scan should either exempt archives or record them as known legacy exceptions.

5. Large archived files exist under `handoff/archive/...`; active handoff root is clean, but `handoff/accepted_changes.md` is already over 1,000 lines. It is append-only by policy, so this is expected but should not become the general place for detailed evidence.

## Recommended next actions

### Small immediate fix batch

1. Patch `.gitignore` to ignore `.claude/` if Claude local permissions are intentionally machine-local.
2. Decide whether `hermes/state/latest_liquidjs_package_cache.txt` should be ignored as runtime state or deleted after the proof packet records the package cache path.
3. Review and commit the two LiquidJS proof docs if accepted.

### Index normalization batch

Patch `INDEX.md` to classify legacy-but-still-tracked top-level zones instead of leaving them implicit. Suggested categories:

- active canon/governance: existing root canon files, `hermes/`, `handoff/`, `config/`
- platform/code/tests: `bin/`, `scripts/`, `platform/`, `schemas/`, `fixtures/`, `tests/`, `tools/`
- reusable security content: `modules/`, `labs/`, `skills/`, `wordlists/`, `templates/`
- intel/evidence/report surfaces: `intelligence/`, `cves/`, `notes/`, `reports/`, `public_exports/`, `pictures/`
- runtime/local ignored: `setting/`, `<artifact-output-dir>/`, `logs/`, `loot/`, `scans/`, `tmp/`, cache dirs
- historical: `archive/`

### Anti-sprawl rule to add to active truth

Future new root-level dirs/files should require either:

- an `INDEX.md` entry first; or
- placement under an already-governed zone; or
- explicit ignored-runtime classification in `.gitignore`.

## Operator decision requested

Approve one of:

1. Minimal hygiene only: ignore `.claude/`, ignore/remove transient `latest_liquidjs_package_cache.txt`, track LiquidJS proof docs.
2. Full index normalization: patch `INDEX.md` with all existing top-level zones and known runtime exceptions.
3. Defer cleanup: keep current state but treat this proposal as the active warning record.
