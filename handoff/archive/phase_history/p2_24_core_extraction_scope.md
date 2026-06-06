> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# P2.24 Project Structure/Core Extraction Scope Note

Date: 2026-05-19
Status: Prepared for direction review only

## Purpose

P2.24 exists to decide whether Phase 2 should pause for a tiny core-helper extraction or close out as-is. It is not an implementation phase yet.

## Current Phase 2 workflow chain

```text
P2.19 finding fixtures
  -> candidate_review_packet/0.1-trial
P2.20 review packet
  -> candidate_review_gap_report/0.1-trial
P2.21 gap report
  -> candidate_verification_plan/0.1-trial
P2.22 verification plan
  -> report_readiness_gate/0.1-trial
P2.23 full offline workflow fixture
  -> candidate_workflow_fixture/0.1-trial
```

## Observed duplication

Common shapes across the P2.20-P2.23 consumers:

- live-target flag denylist: `--target`, `--url`, `--host`, `--scope`, `--live`;
- all-args-rejected CLI posture for stdin-only consumers;
- structured error objects with code/path/message;
- error JSON payloads with deny/error status and summary counters;
- compact single-line JSON emitters;
- non-promotional state vocabulary such as `blocked`, `needs_manual_review`, `not_ready`, `reviewer_decision_required`.

P2.19 remains intentionally different because it reads committed finding fixtures under an allowlist through explicit `--repo-root`.

## Why not refactor automatically

A helper extraction could improve maintainability, but it could also create a premature framework that hides per-stage safety boundaries. The project has repeatedly chosen conservative trial-only consumers over stable schema/runtime promotion. Therefore P2.24 should first ask for direction review rather than immediately editing code.

## Candidate minimal helper, if approved

Possible path:

```text
scripts/core/offline_consumer.py
```

Possible scope:

- constants and pure helpers only;
- no file I/O;
- no subprocess;
- no network;
- no target-touching;
- no schema promotion;
- no report drafting;
- no runner/recon integration;
- no change to existing JSON output contracts.

## Recommended next command

After review prompt creation, route the direction review through the existing worker process, for example:

```bash
HACKLAB=<private-workspace> ./bin/hermes claude-impl
```

Only if the reviewer returns `EXTRACT_MINIMAL_CORE_HELPER` should implementation be planned. If the reviewer returns `DEFER_REFACTOR_AND_CLOSE_PHASE_2`, proceed to P2.25 closeout review instead.
