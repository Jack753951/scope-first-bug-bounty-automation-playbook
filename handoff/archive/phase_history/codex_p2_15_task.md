> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Codex Task — P2-15 offline preview ledger / archive index

Implement only the safe offline contract work approved by `handoff/claude_p2_15_direction_review.json`.

Read first:
- `.hermes.md`
- `handoff/claude_p2_15_direction_review.json`
- `modules/_schema/README.md`
- `scripts/validate_preview_manifest.py`
- `scripts/test_preview_manifest.py`
- `tests/fixtures/preview_manifest/1.0/README.md`

Review tier: T3 contract/platform boundary.

Approved boundary:
- Implement `schema_plus_validator` only.
- Do NOT implement builder/indexer (`scripts/build_preview_ledger.py`) in P2-15.
- Do NOT wire anything into `module_runner.py`, recon, CI, hooks, scheduler, or any scan/module execution path.

Create/update:
- Create `modules/_schema/preview_ledger.schema.json` for closed `preview_ledger/1.0`.
- Create `scripts/validate_preview_ledger.py` stdlib-only read-only validator.
- Create `scripts/test_preview_ledger.py` using strict TDD-style coverage.
- Create committed fixture(s) under `tests/fixtures/preview_ledger/1.0/`.
- Update `modules/_schema/README.md` and `scripts/README.md`.
- Update `handoff/codex_review.md` and `handoff/accepted_changes.md` with actual validation results and safety boundary.

Hard constraints:
- Standard library only: json, re, hashlib, pathlib, datetime, argparse, dataclasses, sys, typing are OK.
- No socket, urllib, http, subprocess, threading, multiprocessing.
- Validator is pure read-only: no writes, repairs, deletes, renames, moves, module execution, network, scanner, callbacks, target touching.
- Ledger must be a manifest-of-manifests index only. Each entry must bind exactly to `runs/<run_id>/preview/preview_manifest.json` by path, SHA-256, size, and `schema_version_observed == "preview_manifest/1.0"`.
- Do not parse/hash/walk the four inner artifacts from the ledger validator; only hash the referenced `preview_manifest.json` file.
- Strict-equal versioning: reject anything other than `preview_ledger/1.0` and per-entry `preview_manifest/1.0`.
- Closed objects everywhere; reject unknown fields.
- Duplicate run_id denied.
- Symlink checks fail closed.
- CLI emits single-line JSON with `schema_version: preview_ledger_validation/1.0`; nonzero on deny.
- Error output must not echo raw file contents, target identifiers, or environment values.
- No credentials/secrets/tokens/connection strings; if needed, write `[REDACTED]`.

Implementation notes:
- Use the direction review as source of truth for fields, validator behavior, and test requirements.
- Use existing style from `scripts/validate_preview_manifest.py` and `scripts/test_preview_manifest.py` where safe.
- For repo root CLI behavior: prefer an explicit `--repo-root` option. If you implement any default, make it conservative and documented. Tests should cover explicit repo root.
- Committed valid ledger fixture can reference the P2-14 committed preview manifest fixture at `tests/fixtures/preview_manifest/1.0/valid_minimal/runs/20260516T020304Z_runner/preview/preview_manifest.json`. If the validator requires repo-root-relative `runs/...`, copy a minimal valid manifest bundle into the ledger fixture root so path equality remains exact.

Required validation before reporting done:
- `python -m py_compile scripts/validate_preview_ledger.py scripts/test_preview_ledger.py`
- `python -m unittest scripts.test_preview_ledger -v`
- `python -m unittest scripts.test_preview_manifest scripts.test_preview_ledger -v`
- `python -m unittest discover -s scripts -p 'test_*.py'`
- `python -m json.tool modules/_schema/preview_ledger.schema.json`
- `git diff --check`
- `USER=${USER:-Owner} HACKLAB=<private-workspace> ./bin/hermes review`

Final note in handoff:
- Explicitly state no live scans, no target interaction, no module/scanner execution, no subprocess/network/callback behavior, no findings/evidence/reports, no scope/config changes, no scheduler/deployment/billing/production settings changed.
