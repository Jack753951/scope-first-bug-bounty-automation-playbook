> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Codex / Engineering Review Notes

Date: 2026-05-19
Current phase: P2.23 offline end-to-end workflow fixture

## Summary

P2.23 adds a trial-only `candidate_workflow_fixture/0.1-trial` offline workflow demonstrator:

- `scripts/build_candidate_workflow_fixture.py`
- `scripts/test_candidate_workflow_fixture.py`
- `scripts/README.md` entry for the new helper

It chains committed finding fixtures through the existing P2.19-P2.22 trial helpers in memory:

```text
finding fixtures
-> candidate_review_packet/0.1-trial
-> candidate_review_gap_report/0.1-trial
-> candidate_verification_plan/0.1-trial
-> report_readiness_gate/0.1-trial
-> candidate_workflow_fixture/0.1-trial
```

The fixture builder emits one deterministic JSON document with per-stage artifacts and a compact cross-stage summary. Any upstream stage error fails closed and prevents later-stage artifacts from being generated.

## Worker Route

Implementation was performed locally by Hermes using strict TDD because the operator approved the suggested direction directly in-session and the slice was narrow, offline, and deterministic. RED was observed before implementation:

```text
FileNotFoundError: scripts/build_candidate_workflow_fixture.py
```

Then Hermes implemented the minimal script and completed local verification. Claude Code MAX/OAuth was not invoked for this narrow local slice; no Anthropic API-backed worker was used.

## Safety Boundary

No live scans, target interaction, network calls, subprocess launch, scanner/module runtime imports, schema promotion, report drafting, report submission adapters, runtime wiring, scope-file edits, secrets, scheduler/deployment/billing/OAuth changes, or output file writes were introduced.

The new builder reads only P2.19-allowlisted committed finding fixtures through `build_candidate_review_packet.py`, rejects live-target flags such as `--target`, `--url`, `--host`, `--scope`, and `--live`, rejects positional arguments, and preserves only non-promotional downstream gate states (`blocked`, `needs_manual_review`).

## Validation

Passed:

```bash
python -m py_compile scripts/build_candidate_workflow_fixture.py scripts/test_candidate_workflow_fixture.py
python -m unittest scripts/test_candidate_workflow_fixture.py
python -m unittest scripts/test_candidate_workflow_fixture.py scripts/test_report_readiness_gate.py scripts/test_candidate_verification_plan.py scripts/test_candidate_packet_gaps.py scripts/test_candidate_review_packet.py
python -m unittest discover -s scripts -p 'test_*.py'
HACKLAB=<private-workspace> ./bin/hermes review
```

Focused P2.23 test:

```text
Ran 6 tests in 0.020s
OK
```

P2.19-P2.23 adjacent suite:

```text
Ran 96 tests in 0.496s
OK
```

Full scripts unittest:

```text
Ran 354 tests in 65.271s
OK (skipped=8)
```

Hermes review:

```text
Python Compile: OK (59 files via python)
Shell Scripts: All shell scripts: bash -n OK
Runtime Safety: Lock: clear
Recon Scope: 12 entries in scope.txt
```

CLI smoke:

```text
candidate_workflow_fixture/0.1-trial ok {'blocked_count': 1, 'candidate_count': 2, 'gap_finding_count': 2, 'gate_result_count': 2, 'input_count': 2, 'needs_manual_review_count': 1, 'verification_plan_count': 2}
bad_exit_payload error LIVE_TARGET_FLAG_NOT_ALLOWED
```

The live-target flag smoke intentionally exits non-zero (`2`) while emitting structured JSON.

## Follow-up

Next likely phase is P2.24 project structure / core extraction review only if duplication across P2.19-P2.23 is now proven worth refactoring. Otherwise proceed to P2.25 Phase 2 closeout periodic review before Phase 3. Do not add report generation, platform adapters, schema/runtime promotion, or live target behavior until the closeout review explicitly approves the next boundary.
