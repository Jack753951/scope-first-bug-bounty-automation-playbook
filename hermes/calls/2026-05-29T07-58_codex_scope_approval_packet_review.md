> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

## Task
Review the current workspace diff for the offline scope approval packet feature and either make deterministic fixes or return an accept/reject verdict.

## Required reads
- `SAFETY.md`
- `INDEX.md`
- `hermes/policies/autonomous_actions.md`
- `scripts/build_scope_approval_packet.py`
- `scripts/build_operator_inbox.py`
- `scripts/test_target_search_pipeline.py`
- `scripts/test_operator_inbox.py`
- `programs/<program-slug>/notes/scope_approval_packet_20260529.md`
- current `git diff`

## Inputs
Current intent:
- Add `scripts/build_scope_approval_packet.py` as an offline-only helper that reads normalized passive policy JSON plus `config/scope.txt` and writes operator approval packets without editing scope or touching live targets.
- Improve pending candidate rendering in `scripts/build_operator_inbox.py` so `handoff/operator_inbox_20260529.md` no longer shows generic `candidate` titles.
- Add unit tests in `scripts/test_target_search_pipeline.py` and `scripts/test_operator_inbox.py`.
- Update <program-slug> passive lane artifacts with generated packet paths.

Validation already run:
- `python -m unittest scripts/test_target_search_pipeline.py scripts/test_operator_inbox.py`
- `python -m py_compile scripts/build_scope_approval_packet.py scripts/build_operator_inbox.py`
- `python -m json.tool programs/<program-slug>/lane_state.json >/dev/null`
- `python -m json.tool programs/<program-slug>/notes/scope_approval_packet_20260529.json >/dev/null`

## Expected output
Return a concise verdict in the last message:

```text
Verdict: accept|reject|partial
Concrete blockers:
- ...
Changes made:
- ...
Tests run:
- ...
```

If you find small deterministic issues, patch them and run focused tests. If you find a safety/scope blocker, do not attempt live target contact or edit `config/scope.txt`; return `reject` with reason.

## Boundary
- Do not edit `SAFETY.md`, `INDEX.md`, `.hermes.md`, or `config/scope.txt`.
- Do not create or broaden `programs/<slug>/scope.json`.
- Do not contact any live target or fetch external URLs.
- Do not add scheduler/cron activation.
- Keep the feature offline/passive and fail-closed.

## Result
Codex CLI launched but could not execute any local command under `--sandbox workspace-write`; every attempt failed before file read with `windows sandbox: spawn setup refresh`. No files were changed by Codex. Output captured in `hermes/calls/2026-05-29T07-58_codex_scope_approval_packet_review.codex_out.md`.

## Verdict
partial

## Notes
Hermes retained the local offline/passive implementation and ran focused tests directly. Treat this as a failed external review attempt, not an accept verdict from Codex. Do not use this Codex call as approval for live target contact or scope changes.
