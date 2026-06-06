> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Codex Task — P2-16 Workflow Validation Sprint: security_headers_baseline

Implement only the narrow workflow-validation slice approved by `handoff/claude_p2_16_direction_review.json`.

Read first:
- `.hermes.md`
- `handoff/claude_p2_16_direction_review.json`
- `modules/checks/level1/policy_decision_metadata_audit/module.json`
- `modules/_schema/finding.schema.json`
- `modules/_schema/module_manifest.schema.json`
- `scripts/validate_module_manifest.py`
- `handoff/codex_review.md`
- `handoff/accepted_changes.md`

Review tier: T3 workflow/module boundary.

Hard scope:
- This is a workflow validation sprint, not a new generic platform layer.
- Implement one offline fixture-driven Level 1 module: `level1.security_headers_baseline`.
- Do NOT add new schemas under `modules/_schema/`.
- Do NOT bump any existing `*/1.0` contract.
- Do NOT modify preview_manifest/preview_ledger validators.
- Do NOT wire into module_runner, recon.sh, profiles, CI/hooks, schedulers, deployment, or production settings.
- Do NOT modify `config/scope.txt`.
- Do NOT add network, DNS, subprocess, threading, multiprocessing, async, ssl, requests/httpx/aiohttp, socket, urllib, http, or any target-touching behavior.
- Do NOT write runtime outputs to disk. The module CLI is stdout-only.
- Do NOT emit runtime findings/evidence into runs/, evidence/, loot/, or reports/.

Implement exactly/approximately per direction review:
- Create module dir: `modules/checks/level1/security_headers_baseline/`
- Create `check.py` with stdlib-only pure function:
  `evaluate(fixture: dict, *, run_id: str, policy_decision_sha256: str) -> list[dict]`
- Create `module.json` if it can pass existing module manifest validation while staying no-network/no-target-touching/emits_findings=false/emits_evidence=false.
- Create `README.md` documenting closed input fixture shape, no-network/no-write boundary, static severity hints, OWASP Secure Headers Project + ASVS V14.4 references, and explicit deferral of runtime emission.
- Create tests in `scripts/test_security_headers_baseline.py`.
- Create 6 committed input fixtures and 6 expected_findings fixtures under `tests/fixtures/security_headers_baseline/<scenario>/`.
- Create 6 triage markdown drafts plus README under `handoff/p2_16_triage/`.

Header coverage v1 exactly:
- Content-Security-Policy: missing; unsafe-inline present.
- X-Frame-Options: missing; value must be DENY or SAMEORIGIN.
- X-Content-Type-Options: missing; value must be nosniff.
- Strict-Transport-Security: missing; max-age >= 15552000; includeSubDomains present.
- Referrer-Policy: missing; value in fixed allowlist.

Input fixtures:
- closed JSON shape only: `{fixture_version,target,status_code,headers}`.
- `fixture_version == "security_headers_baseline_input/1"`.
- `target.type` only `url` or `domain`.
- committed target values only reserved names: `lab.local`, `*.example.test`, `invalid.`, or similar RFC 2606-safe placeholders.
- header entries: `{name,value}` only.

Findings:
- Must conform to existing `finding/1.0` as much as possible using current schema.
- Status must be `candidate`.
- scanner_output_only/manual_verification_required semantics must be preserved according to actual schema field names.
- source.module_id = `level1.security_headers_baseline` if schema supports it; if actual schema differs, adapt to schema without adding new fields.
- policy_decision_sha256 and run_id must be caller-supplied, never synthesized silently.
- evidence array empty in v1.
- Do not include target.value or any header VALUE in rendered finding strings.

TDD requirements:
- Add tests before production code where practical. If you discover existing shape constraints require adaptation, encode them in tests first.
- Tests must include fixture golden equality, schema-ish finding validation or at least validation against existing `scripts/validate_finding_evidence.py` if compatible, candidate/triage flags, source/provenance fields, redaction, closed input fixture errors, fixture version drift, target type denial, unsafe header name denial, determinism, pure function no fixture mutation/no file writes, forbidden import static scan, forbidden write static scan, CLI smoke success/failure, header name case-insensitivity, value comparison behavior, reserved-name fixture assertion.

Validation before reporting done:
- `python -m py_compile modules/checks/level1/security_headers_baseline/check.py scripts/test_security_headers_baseline.py`
- `python -m unittest scripts.test_security_headers_baseline -v`
- `python scripts/validate_module_manifest.py modules/checks/level1/security_headers_baseline/module.json --json` if module.json exists.
- `python -m unittest discover -s scripts -p 'test_*.py'`
- `git diff --check`
- `USER=${USER:-Owner} HACKLAB=<private-workspace> ./bin/hermes review`

Update handoff:
- Append/update `handoff/codex_review.md` with exact files and validation results.
- Append/update `handoff/accepted_changes.md` Latest with P2-16 summary and safety boundary.
- State explicitly: no live scans, no target interaction, no network/DNS/subprocess/callback, no runtime writes, no schema bumps, no runner/recon/CI/scheduler wiring, no scope/config changes, no confirmed findings.

If any direction review blocker cannot be satisfied cleanly with existing `finding/1.0`, do not invent a new schema. Keep to committed fixtures/triage drafts and record the limitation.
