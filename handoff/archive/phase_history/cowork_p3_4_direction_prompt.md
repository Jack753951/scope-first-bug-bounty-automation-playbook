> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# P3.4 Direction Review Prompt — Manifest-Only Third Level 1 Module Candidate

Date: 2026-05-19
Owner: Hermes
Requested reviewer: Claude/Cowork via Claude Code MAX/OAuth
Review tier: T3 direction review + OSS Recon Gate, design-only
Milestone: Phase 3, candidate fourth slice after P3.3 two-module runner discovery coverage

## Context

Phase 2 closed with a safe offline contract layer and a first Level 1 module fixture. P2-16 later added `level1.security_headers_baseline`, which means the "second Level 1 module" objective discussed in P2.25 was already physically satisfied before P3.3. P3.3 therefore redirected to a test-only slice proving two-module discovery / CLI / module I/O preview bundle consistency across the two existing modules under `audit-baseline`.

P3.3 landed as tests/docs/handoff only and preserved the no-runtime boundary:
- no edits under `modules/**`
- no runner behavior changes
- no profile/schema changes
- no live target behavior
- no scanner/network/subprocess behavior
- `module_runner.py` loads module manifests as data only and does not import or execute module `check.py` files

The P3.3 review parked an optional P3.4 candidate:

> If, after P3.3 lands, the operator still wants a strictly manifest-only datapoint, P3.4 can be a small slice that adds one manifest under `modules/checks/level1/<neutral_name>/module.json` with no `check.py` and no evaluator. That slice would need its own OSS Recon Gate and direction review.

This prompt asks whether that optional P3.4 candidate should proceed now, and if so exactly how small and safe it must remain.

## Proposed P3.4 Candidate

Add a third Level 1 module directory that is intentionally manifest-only:

- Recommended neutral module id/name from P3.3 review: `level1.policy_decision_trace_audit`
- Path candidate: `modules/checks/level1/policy_decision_trace_audit/module.json`
- Explicitly forbidden in this slice: `check.py`, evaluator code, fixtures that imply execution, module runner imports, scanner integrations, network clients, subprocess calls, schema/profile/runner behavior changes.

Intended purpose: create one additional manifest-only datapoint that proves the module registry can represent metadata-only audit checks without colocated evaluator code. This should remain a data contract fixture, not a runtime module.

## Questions for Reviewer

Please provide a design-only T3 review with the sections below:

1. Verdict
   - One of:
     - `PROCEED_WITH_MANIFEST_ONLY_P3_4`
     - `PROCEED_WITH_CHANGES`
     - `DEFER_P3_4_MANIFEST_ONLY`
     - `REJECT_P3_4_MANIFEST_ONLY`

2. Rationale
   - Is a third manifest-only Level 1 module useful after P3.3, or is it redundant ceremony?
   - Does it strengthen the contract story enough to justify a small repo change?
   - What risk does it introduce even without evaluator code?

3. Approved module scope, if any
   - Exact module id/path/name.
   - Required manifest fields and values.
   - Whether profile `audit-baseline` should select it.
   - Whether tests should assert exact three-module selection or only include/existence.
   - Whether docs should explicitly say manifest-only means no evaluator code present.

4. OSS Recon Gate Notes
   Compare at least these references at the design level only; no code import or live probing:
   - Nuclei template metadata and matcher separation
   - OWASP ZAP passive rule / add-on metadata separation
   - Semgrep rule metadata / fixture separation
   - SARIF run/result/toolComponent separation
   - DefectDojo / importer lifecycle risks to reject

   For each, state adopt/adapt/ignore and safety concerns. Avoid copying active-scan, verified/confirmed, import-database, OAST, callback, or intrusive semantics.

5. Required TDD / validation gates if implementation proceeds
   - Expected RED test before adding manifest.
   - Minimal GREEN implementation files.
   - Focused test command(s).
   - Full suite command.
   - Hermes review command.
   - Independent implementation review requirement.

6. Forbidden changes
   Explicitly list files/areas that implementation must not touch, including at minimum:
   - `config/scope.txt`
   - `recon.sh`
   - `config/recon.conf`
   - `scripts/module_runner.py` runtime behavior, unless the reviewer explicitly says a docs/test-only adjustment is required
   - `modules/profiles/audit-baseline.json`, unless the reviewer explicitly approves profile membership edit for the new manifest
   - `modules/_schema/**`
   - candidate workflow `*/0.1-trial` schemas and scripts
   - `loot/**`, `scans/**`, `reports/**`, `.env`, credentials, OAuth, scheduler, deployment, billing, production settings

7. Safety boundary confirmation
   Confirm the review is design-only and does not authorize active scans, target interaction, module execution, scanner imports, report drafting/submission, schema promotion, or platform adapters.

## Current Known Constraints

Existing Level 1 modules:
- `level1.policy_decision_metadata_audit`
- `level1.security_headers_baseline`

Existing profile:
- `modules/profiles/audit-baseline.json`
- Conservative dry-run constraints: no network, no target touching, low/info risk only.

P3.3 accepted implementation already tests exact two-module selection in the live repo. If P3.4 adds a third selected module, that test must be intentionally updated as part of P3.4, not accidentally broken.

## Output File

Write the final review to:

`handoff/cowork_p3_4_direction_review.md`

Do not modify code, manifests, tests, schemas, runtime files, scope files, or configs in this direction-review task.
