> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Phase 4A — Controlled Lab Semi-Automated Calibration Plan

Status: roadmap/planning checkpoint
Date: 2026-05-20
Prepared by: Hermes
Scope: planning only; no target-touching, no lab activation, no scanner/module execution, no scope/config authorization change

## Decision

Insert a dedicated Phase 4A between Phase 3 dry-run/local MVP closeout and any real authorized bug-bounty private beta:

**Phase 4A — Controlled Lab Semi-Automated Calibration**

Chinese working name:

**Phase 4A — 授權靶場半自動流程校準**

This phase uses a local lab, intentionally vulnerable app, or explicit CTF/training target to calibrate the platform workflow and scripts before touching a real bug-bounty program.

## Placement

Recommended sequence:

1. Phase 3.15 — documentation-only manifest/profile policy crosswalk.
2. Phase 3.16 — dry-run/local MVP demo plan using only synthetic/local artifacts.
3. Phase 3.17 — Phase 3 closeout: confirm the offline MVP boundary and move lab activation out of Phase 3.
4. **Phase 4A — Controlled Lab Semi-Automated Calibration.**
5. Phase 4B — Lab-to-report workflow trial.
6. Phase 4C — Authorized bug-bounty private-beta planning.
7. Phase 5 — Real authorized bug-bounty controlled execution.

## Why Phase 4A, not Phase 3

Phase 3 should remain offline/dry-run only:

- no target touching;
- no real scanner/module execution;
- no live target claims;
- no report submission or platform adapter;
- no automatic confirmed findings.

A controlled lab is safer than a public target, but it still introduces a live-ish execution boundary: real HTTP services, real tool output, real candidate findings, and real human verification decisions. That makes it Phase 4 work and at least T4-style safety/runtime review before activation.

## Authorized target classes

Phase 4A may only use one of these classes after explicit operator selection:

- local lab controlled by the operator;
- intentionally vulnerable local app;
- CTF/training platform instance with explicit scope;
- user-owned asset explicitly designated for lab testing.

Examples that can be considered later:

- OWASP Juice Shop;
- DVWA;
- WebGoat;
- PortSwigger Web Security Academy lab;
- HackTheBox / TryHackMe machine with explicit lab scope.

This plan does not select or authorize any target by itself.

## Operating mode

Phase 4A is semi-automated, not autonomous.

Required loop:

1. Operator selects a lab target and scope.
2. Hermes records a narrow lab scope/rules artifact.
3. A T4/T5 direction review approves the exact live-ish lab boundary.
4. Scripts run only inside the approved lab scope.
5. Automation emits candidate findings only.
6. Hermes/agent review checks false positives, evidence shape, redaction, and report-readiness gaps.
7. Human operator decides whether to continue, verify manually, discard, or refine scripts.
8. Nothing is submitted externally and nothing is marked confirmed by automation alone.

## Calibration goals

Phase 4A success is measured by workflow quality, not by number of vulnerabilities found.

Primary questions:

- Does scope enforcement prevent accidental public target interaction?
- Are rate limits, timeouts, kill switch, and audit logs understandable and effective?
- Is scanner/module output too noisy for candidate triage?
- Do candidate findings include enough evidence for a reviewer to reason about impact?
- Does evidence redaction avoid secrets, cookies, tokens, loot, and sensitive payloads?
- Can the report-readiness gate block immature findings?
- Which manual verification checklist items are missing?
- Which scripts need better structured output, retry behavior, or error taxonomy?

## Non-goals and locked surfaces

Phase 4A is not:

- real bug-bounty target testing;
- autonomous exploitation;
- exploit chaining;
- fuzzing/brute force unless a later explicit lab-only review authorizes a narrow case;
- callback/OAST/pivot/proxy/tunnel work;
- credential handling or loot collection;
- automatic confirmed findings;
- report submission;
- scheduler/CI target-touching automation;
- production-like multi-program operation.

## Entry criteria

Before Phase 4A can begin:

1. Phase 3 dry-run/local MVP closeout is accepted.
2. The operator chooses the lab target class and exact scope.
3. The lab scope is documented separately from real bug-bounty program scope.
4. The required review tier is assigned; live-ish activation should default to T4, and escalate to T5 if credentials, persistence, callbacks, destructive behavior, external services, production assets, or scheduler/CI are involved.
5. Deny-by-default tests prove non-lab/public targets cannot be touched.
6. Audit logging, stop conditions, timeout/rate limits, and rollback/cleanup steps are documented.
7. The operator explicitly approves the exact activation.

## Exit criteria

Phase 4A can close when the lab calibration produces:

1. at least one end-to-end candidate-only lab workflow packet;
2. evidence that scope/rule gates deny out-of-lab targets;
3. an audit trail of what ran, when, and under which lab scope;
4. a false-positive/noise assessment;
5. a manual verification checklist update;
6. report-readiness gate observations;
7. a list of script/workflow fixes to complete before Phase 4B or 4C;
8. confirmation that no real bug-bounty target, production target, credentials, loot, or report submission path was touched.

## Relationship to first bounty

Phase 4A improves the path to the first bounty by proving the workflow on a safe target class before a real program. It should feed Phase 4C planning by identifying:

- which low-risk techniques are mature enough for private beta consideration;
- which evidence fields are actually needed;
- which report-readiness blockers are common;
- which manual operator decisions must stay in the loop;
- which automation surfaces remain too risky for real programs.

## Safety boundary

This document is planning only.

No live scans, probes, scanner/module execution, target interaction, fuzzing, brute force, exploit attempts, callbacks/OAST, proxy/pivot/tunnel/transport behavior, external service calls, SIEM integration, report drafting/submission, platform adapter, credentials, loot-class data, scheduler/CI, deployment, billing, OAuth, production settings, `config/scope.txt` changes, or real program scope/rule activation were introduced.
