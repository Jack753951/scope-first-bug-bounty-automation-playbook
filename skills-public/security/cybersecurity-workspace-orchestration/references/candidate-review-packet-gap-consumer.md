> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Candidate review packet and gap-report consumers

Use this note for bug-bounty automation phases that transform offline candidate findings into reviewer-facing artifacts before any live execution or formal report drafting.

## Pattern

1. Build a trial-only candidate review packet from already-committed, allowlisted fixtures or validated offline finding data.
   - Example contract name: `candidate_review_packet/0.1-trial`.
   - Preserve only triage states such as `candidate`, `needs_verification`, `not_ready`, or `reviewer_decision_required`.
   - Emit deterministic JSON to stdout; do not create a schema file until multiple consumers prove the shape.
2. Add a separate gap/action consumer before report drafting.
   - Read exactly one packet from stdin.
   - Emit deterministic JSON to stdout, e.g. `candidate_review_gap_report/0.1-trial`.
   - Convert each finding into explicit human-review blockers/actions such as missing evidence, low confidence, info-severity report block, manual verification required, scanner-output-only, missing remediation, missing verification guidance, or missing scope-review question.
3. Add a separate verification-plan/checklist consumer after the gap report, still before report drafting.
   - Read exactly one `candidate_review_gap_report/0.1-trial` from stdin.
   - Emit deterministic JSON to stdout, e.g. `candidate_verification_plan/0.1-trial`.
   - Convert each gap into stable human checklist items with stable item codes such as `CHECK_*`, reviewer instructions, source gap code, and deterministic ordering.
   - Use only non-promotional plan states such as `blocked` and `needs_manual_review`; avoid carrying `not_ready` / `reviewer_decision_required` forward as plan statuses when the review direction calls for clearer gate language.
   - Fail closed on unknown `review_state`, unknown gap codes, invalid/non-integer/boolean gap counts, and duplicate gap codes within one finding.
4. Keep all consumers as decision-support artifacts, not report generators.
   - They may say `not_ready`, `reviewer_decision_required`, `blocked`, or `needs_manual_review` according to the contract stage.
   - They must not say `ready`, `approved`, `confirmed`, `verified`, or `accepted` as workflow states.
5. Run independent review after implementation because the boundary is easy to weaken accidentally.

## Safety boundaries

The packet builder and gap consumer should remain:

- standard-library-only where possible
- offline / read-only except for explicitly reviewed fixture creation
- deterministic
- stdout-only for generated artifacts
- not connected to runner/recon/CI/scheduler/platform adapters
- not allowed to read `config/scope.txt`, credentials, loot, OAuth/session files, or raw evidence files unless a later reviewed phase explicitly introduces that capability
- not allowed to accept live-target affordances such as `--target`, `--url`, `--host`, `--scope`, or `--live`, including assignment forms such as `--target=example.invalid`
- not allowed to accept generic positional CLI arguments; all CLI args should fail closed unless the phase explicitly designs a CLI contract
- not allowed to provide output-file/input-file options; keep stdin/stdout-only until a separate persistence phase is reviewed
- not allowed to import network/process/runtime primitives (`socket`, `http`, `urllib`, `requests`, `httpx`, `subprocess`, `asyncio`, `selectors`, etc.)
- not allowed to open files or write outputs unless a separate persistence phase is reviewed

## Tests to include

- RED test for missing script or missing consumer behavior before implementation.
- Happy path: deterministic output from packet → gap consumer → verification plan.
- Wrong schema version, upstream status not ok, upstream errors, malformed JSON.
- Promoted finding statuses are rejected.
- Verification-plan consumer rejects unknown review states, unknown gap codes, boolean/non-integer gap counts, and duplicate gap codes per finding.
- Live-target flags are rejected with structured JSON errors, including both separated and assignment-style forms (`--target example.invalid`, `--target=example.invalid`).
- Unknown dash args and positional args are rejected with structured JSON errors.
- Output vocabulary does not contain promotion words as states.
- AST/static checks for forbidden imports and write/exec/process primitives.
- Schema-promotion check: no `modules/_schema/*candidate_review_gap_report*` or `*candidate_verification_plan*` (or equivalent) until intentionally promoted.
- Full adjacent tests plus project review wrapper.

## Pitfalls

- Do not let CTF scaffolding keep expanding after it has served calibration value. Redirect the next slice back to bug-bounty candidate review, evidence gaps, verification planning, or report-readiness blockers.
- Do not create a formal bug-bounty report or submission draft from packet/gap/verification-plan data. After a verification-plan consumer, the next safe slice is usually a report-readiness gate/classifier, not a report generator.
- Do not let a report-readiness gate generate Markdown/HTML/PDF, platform-specific report text, impact/repro/remediation prose, status promotion, or schema promotion unless a separate direction review explicitly approves that boundary.
- Do not assume rejecting `--target`/`--url` is enough. A positional argument like `example.com` is also a target affordance and must fail closed when the consumer is specified as stdin-only.
- Do not preserve stale worker-plan terminology. For this user's workspace, refer to the subscription route as `Claude Code MAX/OAuth`, not `Pro/OAuth`.
