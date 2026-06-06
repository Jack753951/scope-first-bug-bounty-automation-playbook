> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Third-Party Review — P2.18 CTF Verifier Metadata Trial Consumers

Date: 2026-05-18
Route: Hermes `delegate_task` independent review and follow-up review
Scope: P2.18 CTF verifier metadata linter/template/fixtures and project direction

## Purpose

The operator explicitly asked to enable third-party review work and reminded that the long-term goal is automated authorized bug-bounty acquisition, not over-focusing on CTF. This review checked both implementation safety and whether P2.18 should stop expanding into CTF tooling.

## Initial Result

REQUEST_CHANGES

## Blockers Found

1. P2.18 active-service / oracle / external-service descriptors needed a stronger `requires_scope: true` gate in addition to `kali_required: true`.
2. CLI documentation needed to be clearer that the linter emits JSON to stdout only and performs no output file writes.
3. Template wording still referred to P2.17 and needed to be corrected to P2.18 trial-only / non-binding status.

## Hermes Fixes

- Added `ACTIVE_SERVICE_REQUIRES_SCOPE` enforcement to `scripts/lint_ctf_verifier_metadata.py`.
- Added tests proving `active-service`, `uses_external_service: true`, and `oracle_required: true` require both `kali_required: true` and `requires_scope: true`.
- Updated `templates/ctf_verifier_metadata.yaml` to P2.18 trial-only wording and scope/Kali guardrails.
- Updated `scripts/README.md` wording for stdout-only/read-only behavior.

## Follow-Up Result

Follow-up review accepted the blocker fixes with only non-blocking recommendations. The remaining direction decision was to stop spending roadmap on CTF after P2.18 and redirect the next phase toward bug-bounty candidate finding review/reporting workflow.

## Direction Decision

Do not promote CTF verifier metadata to schema/runtime now. Treat P2.17/P2.18 as calibration scaffolding and move the next project stage back to bug-bounty automation.
