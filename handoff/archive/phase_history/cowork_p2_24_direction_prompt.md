> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# P2.24 Direction Review Prompt — Core Extraction vs Phase 2 Closeout

Date: 2026-05-19
Owner: Hermes
Requested reviewer: Claude/Cowork via Claude Code MAX/OAuth or Cowork-equivalent read-only review
Review tier: T3 direction review, design-only
Milestone: Phase 2 bug-bounty candidate review workflow closeout

## Context

The cybersec lab has completed a sequence of offline, trial-only bug-bounty candidate review consumers:

```text
P2.19 build_candidate_review_packet.py
P2.20 review_candidate_packet_gaps.py
P2.21 build_candidate_verification_plan.py
P2.22 build_report_readiness_gate.py
P2.23 build_candidate_workflow_fixture.py
```

The chain now demonstrates the intended candidate -> review -> gap/action -> verification checklist -> report-readiness gate workflow without live target interaction, schema promotion, report drafting, platform adapters, or runtime scanner/module execution.

P2.23 `handoff/codex_review.md` records the current recommendation:

```text
Next likely phase is P2.24 project structure / core extraction review only if duplication across P2.19-P2.23 is now proven worth refactoring. Otherwise proceed to P2.25 Phase 2 closeout periodic review before Phase 3. Do not add report generation, platform adapters, schema/runtime promotion, or live target behavior until the closeout review explicitly approves the next boundary.
```

Hermes performed a lightweight inventory and observed repeated shapes across P2.20-P2.23:

- repeated `LIVE_TARGET_FLAGS = {"--target", "--url", "--host", "--scope", "--live"}`;
- repeated stdin/stdout JSON consumer pattern;
- repeated `*_Error` classes with `code`, `path`, and `message` fields;
- repeated `_error_payload(...)` and compact JSON emitters;
- repeated CLI argument rejection and assignment-style live-flag checks;
- repeated summary/status naming conventions;
- repeated trial-only safety boundary text in README entries.

P2.19 is slightly different because it intentionally reads only allowlisted committed fixtures with `--repo-root`; P2.20-P2.22 are stdin-only consumers; P2.23 chains helpers in memory.

## Requested review question

Please decide whether P2.24 should be:

1. `DEFER_REFACTOR_AND_CLOSE_PHASE_2`
   - Duplication is acceptable for now.
   - Go directly to P2.25 Phase 2 closeout periodic review.

2. `EXTRACT_MINIMAL_CORE_HELPER`
   - A narrow helper extraction is worth doing before closeout.
   - Keep it limited to stable offline-consumer primitives that do not change output contracts.

3. `ROUTE_BACK_FOR_SCOPE_CLARIFICATION`
   - The boundary is unclear or risks growing into schema/runtime promotion.

## Design-only constraints

This review must not modify code or run target-touching tools.

Do not propose or implement:

- live scans, target interaction, network clients, scanners, fuzzers, callbacks, OAST, proxy/pivot behavior;
- module execution, runner runtime wiring, recon integration, scheduler/CI hooks, or platform adapters;
- schema promotion from `0.1-trial` to stable contracts;
- confirmed-finding status promotion;
- report drafting/generation/submission adapters;
- writes to `config/scope.txt`, loot, credentials, production settings, billing, OAuth, or deployment.

## If recommending minimal extraction

Keep the target small and TDD-friendly. Suggested candidate file:

```text
scripts/core/offline_consumer.py
```

Possible contents, if and only if reviewer agrees they are stable enough:

- `LIVE_TARGET_FLAGS` constant;
- `Issue`/`ConsumerError` dataclass with `code`, `path`, `message`;
- `error_payload(schema_version, errors, summary=None, extra=None)` helper;
- `compact_emit(payload)` helper;
- `reject_all_args(argv, *, live_message, arg_message)` helper that preserves current live-target flag behavior including `--target=value`;
- no JSON schema validation, no business logic, no file I/O, no subprocess, no network, no target fields.

Required implementation guardrails if extraction is approved:

1. Use TDD first.
2. Add focused tests for the helper before touching consumers.
3. Migrate at most one consumer first, then run full scripts unittest.
4. Assert byte-for-byte or object-equality compatibility for representative existing outputs before and after migration.
5. Preserve every existing schema version, status value, error code, field name, summary counter, and exit code.
6. Do not change P2.19 allowlist/file-reading behavior.
7. Do not create generic framework hooks that make future live-target arguments easier to accept.

## If recommending closeout instead

Please define P2.25 closeout review inputs and questions, including:

- whether P2.19-P2.23 proved enough workflow value;
- whether Phase 3 should prioritize real offline fixture quality, a second Level 1 module fixture, candidate/evidence UX, or report-readiness reviewer prompts;
- what not to build next to avoid over-engineering;
- which boundaries must stay locked until explicit operator approval.

## OSS Recon Gate

Because this is a possible core helper/platform-boundary refactor, briefly compare against 2-4 mature patterns without copying target-touching defaults. Useful comparisons may include:

- SARIF result/status separation and non-promotional result levels;
- Nuclei template/helper separation but not its live scanning runtime;
- Semgrep/CLI JSON error-shape conventions;
- DefectDojo finding lifecycle concepts, while preserving candidate-only semantics.

Return adopt/adapt/ignore decisions. Keep the review design-only.

## Expected reviewer output

Write the result to:

```text
handoff/cowork_p2_24_direction_review.md
```

Required sections:

```text
# P2.24 Direction Review

## Verdict
DEFER_REFACTOR_AND_CLOSE_PHASE_2 | EXTRACT_MINIMAL_CORE_HELPER | ROUTE_BACK_FOR_SCOPE_CLARIFICATION

## Rationale

## Duplication Assessment

## OSS Recon Gate Notes

## If Proceeding: Minimal Task Boundary

## If Deferring: P2.25 Closeout Questions

## Safety Boundary Confirmation

## Blocking Issues

## Non-Blocking Recommendations
```

Hermes acceptance criteria for this direction step:

- review remains design-only;
- verdict is explicit;
- safety boundary is preserved;
- any suggested implementation is limited to offline helper extraction with compatibility tests;
- if deferring, P2.25 closeout questions are clear enough to route immediately.
