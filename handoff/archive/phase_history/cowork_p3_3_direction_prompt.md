> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# P3.3 Direction Review Prompt — Second Level 1 Module Fixture Boundary

Date: 2026-05-19
Owner: Hermes
Requested reviewer: Claude/Cowork via Claude Code MAX/OAuth
Review tier: T3 direction review + OSS Recon Gate, design-only
Milestone: Phase 3, post P3.1/P3.2 fixture-hardening work

## Context

Phase 2 is closed (`handoff/cowork_p2_25_closeout_review.md`, verdict `CLOSE_PHASE_2`). Phase 3 has started with offline/local, non-target-touching slices only.

Completed Phase 3 work so far:

```text
P3.1 — curated near-real offline fixture set for the P2.19 -> P2.23 candidate workflow chain.
       See `handoff/cowork_p3_1_direction_review.md` and
       `handoff/third_party_p3_1_implementation_review.md`.

P3.2 — test-only terminal-state expectation matrix for all P3.1 curated findings.
       See the top entry in `handoff/accepted_changes.md`.
```

Important numbering note: P2.25 originally called the second Level 1 module fixture "P3.2". The project has since used `P3.2` for the terminal-state matrix hardening slice. This review should either approve the second Level 1 module fixture as `P3.3`, or explicitly recommend a safer next slice/name if the numbering should be corrected.

Existing relevant assets:

```text
modules/checks/level1/policy_decision_metadata_audit/module.json
modules/checks/level1/security_headers_baseline/
modules/profiles/INDEX.md
scripts/module_runner.py
scripts/validate_module_manifest.py
scripts/validate_module_io_bundle.py
scripts/validate_preview_manifest.py
scripts/validate_preview_ledger.py
scripts/test_module_runner.py
scripts/test_security_headers_baseline.py
scripts/README.md
handoff/cowork_p2_25_closeout_review.md
handoff/cowork_p2_24_direction_review.md
handoff/oss_recon_gate.md
handoff/review_tiering_policy.md
```

## Requested review

Perform a design-only T3 direction review and OSS Recon Gate for the next Phase 3 implementation slice.

Primary candidate: add a second Level 1 dry-run-only module fixture that proves the runner/profile/bundle/preview contracts are general across more than one committed module, while preserving all existing safety gates.

Suggested module shape from P2.25:

```text
modules/checks/level1/scope_match_audit/
```

Alternative acceptable shape if better justified:

```text
modules/checks/level1/policy_decision_trace_audit/
```

This review must decide:

1. Should the next implementation slice be the second Level 1 module fixture?
2. If yes, what exact module shape/name should be approved?
3. What files may the implementer write?
4. What files are forbidden?
5. What tests must be added or extended?
6. What behavior is explicitly out of scope?
7. Does the P3.2 numbering collision require any accepted-history clarification?
8. Which OSS patterns should be adapted/rejected before implementation?

## Proposed goals for the implementation slice

If approved, the implementation slice should remain offline/local and dry-run-only:

- Add one second Level 1 module fixture under `modules/checks/level1/<module_id>/`.
- The module must be manifest-only or pure fixture/evaluator only; no live target interaction, network, scanner, subprocess, callback, OAST, proxy, pivot, or external tool behavior.
- It must declare no findings/evidence emission unless the direction review explicitly argues otherwise. Preferred default: `emits_findings=false` and `emits_evidence=false`.
- It must validate under the existing `module_manifest/1.0` schema without schema edits.
- It must be discoverable by the existing module runner/profile selection path.
- A dry-run preview over the relevant profile should include both existing Level 1 modules and produce an allowed bundle-consistency result.
- The slice should not promote any `0.1-trial` schema and should not touch the P2.19-P2.23 candidate workflow chain.

## OSS Recon Gate

Compare against mature/open-source module/plugin/check organization patterns at a design level only. Include adopt/adapt/ignore decisions for at least:

- Nuclei templates / ProjectDiscovery style metadata and severity tags;
- OWASP ZAP passive scanner add-ons / alert metadata;
- Semgrep rule metadata and non-executing rule fixtures;
- DefectDojo engagement/test/product separation for imported findings;
- SARIF result/run separation and `level` vocabulary.

Reject anything that implies live scanning, scanner imports, confirmed/verified finding status, evidence collection, report drafting/submission, platform adapters, scheduler/CI wiring, target execution, or schema promotion.

## Safety boundary

This is design-only. The reviewer may read local files and write the requested review artifact only. Do not run live scans, probes, fuzzing, exploit tooling, callbacks, OAST infrastructure, proxies, pivots, tunnels, scanners, module execution against targets, or any target-touching automation.

Do not modify implementation files during this review. Forbidden during review:

```text
config/scope.txt
recon.sh
config/recon.conf
modules/**
scripts/*.py
tests/**
loot/**
scans/**
reports/**
.env
credentials/OAuth/scheduler/deployment/billing/production settings
```

## Expected output

Write the review to:

```text
handoff/cowork_p3_3_direction_review.md
```

Required sections:

```text
# P3.3 Direction Review

## Verdict
PROCEED_WITH_SECOND_LEVEL1_MODULE_FIXTURE | PROCEED_WITH_CHANGES | DO_NOT_PROCEED

## Rationale

## Numbering / Roadmap Clarification

## Approved Module Scope

## OSS Recon Gate Notes

## Implementation Boundary

## Required TDD / Validation Gates

## Safety Boundary Confirmation

## Blocking Issues

## Non-Blocking Recommendations
```

If proceeding, provide a concrete worker-ready implementation boundary and acceptance criteria. Keep it narrow enough for a single Claude Code Impl or Codex fallback implementation pass, with Hermes verification afterward.
