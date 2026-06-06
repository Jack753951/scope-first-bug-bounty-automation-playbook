> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Direction Prompt — P2.19 Bug-Bounty Candidate Review Packet

Date: 2026-05-18
Proposed tier: T3 design review
Worker route preference: Claude Code MAX/OAuth read-only review first; use API-backed Claude only if explicitly justified.
Strategic correction: stop expanding CTF tooling after P2.18; CTF remains calibration only. The project goal is an authorized automated bug-bounty platform.
Boundary: offline/local only; no live scans, scanner execution, target interaction, runtime finding emission, scheduler, deployment, OAuth, billing, or production changes.

## Context

Recent phases established a dry-run contract spine:

- `finding/1.0` and `evidence/1.0` schemas + validator
- `run/1.0` and module manifest/profile gates
- module I/O preview contracts and consistency validator
- persisted preview bundles and preview ledger
- P2.16 `security_headers_baseline` offline module fixture that produces committed candidate-finding fixtures and triage draft markdown
- P2.17/P2.18 CTF calibration helpers are complete enough and should not keep consuming roadmap unless they directly improve bug-bounty workflow

The next value should move back toward authorized bug bounty automation: package candidate findings for human/agent review and report drafting without touching live targets.

## Proposed Objective

Add an offline/local candidate review packet layer that packages existing committed `finding/1.0` candidate fixtures into a deterministic review bundle for third-party triage/review.

This layer should help future bug bounty workflow answer:

- What candidate findings exist?
- Which are scanner-output-only?
- What manual verification is required?
- What evidence references exist and are redacted?
- Is policy/scope provenance present?
- What should a reviewer check before report drafting?

It must NOT promote candidate findings to confirmed findings.

## Candidate Deliverables

Option A — preferred if existing contracts support it:

```text
scripts/build_candidate_review_packet.py
scripts/test_candidate_review_packet.py
tests/fixtures/candidate_review_packet/
```

A standard-library-only offline builder that reads one or more committed `expected_findings.json` fixture files and emits deterministic JSON to stdout, for example:

```json
{
  "schema_version": "candidate_review_packet/0.1-trial",
  "status": "ok",
  "summary": {
    "candidate_count": 0,
    "needs_verification_count": 0,
    "targets": [],
    "modules": []
  },
  "findings": [
    {
      "id": "...",
      "status": "candidate",
      "title": "...",
      "target": {"type": "url", "value": "https://example.invalid"},
      "source": {"module_id": "...", "run_id": "...", "policy_decision_sha256": "..."},
      "severity_hint": "low",
      "confidence": "medium",
      "manual_verification_required": true,
      "scanner_output_only": true,
      "evidence_ref_count": 0,
      "report_readiness": "not_ready",
      "review_questions": []
    }
  ],
  "errors": [],
  "warnings": []
}
```

Option B — if builder is too early:

```text
handoff/p2_19_candidate_review_packet_design.md
```

A design-only packet shape with fixtures and acceptance tests, no implementation.

## Mandatory Constraints

- Reads existing committed fixture files only, not `runs/`, `scans/`, `loot/`, live target paths, or network sources.
- No filesystem writes by default; stdout only unless a separate direction review authorizes output paths.
- No target touching, HTTP, sockets, DNS, subprocess, scanner/module execution, callbacks, fuzzing, brute force, or exploit attempts.
- No status escalation to `confirmed`, `verified`, or `accepted`.
- No report publication, scheduler, OAuth, credential, billing, deploy, GitHub issue/PR creation, or notification behavior.
- Must validate each input finding through the existing `validate_finding_evidence.py` path where practical.
- Must preserve manual verification gates and scanner-output-only semantics.
- Must not add or bump `finding/1.0`, `evidence/1.0`, `run/1.0`, `preview_manifest/1.0`, or `preview_ledger/1.0` schema versions in this slice.

## OSS Recon Gate Questions

Compare design-only against 2-5 mature references:

- DefectDojo import/review lifecycle
- SARIF result/run/result.kind/level separation
- <bug-bounty-platform>/Bugcrowd report quality conventions if publicly documented
- Semgrep finding metadata / confidence
- Nuclei output metadata / template info

For each reference, state adopt/adapt/ignore and why. Do not copy unsafe target-touching defaults.

## Review Questions

1. Is this the right next bug-bounty-focused slice after P2.18, or should we choose a different offline/local slice?
2. Should this be a builder now, or design-only first?
3. Should the packet be a trial `candidate_review_packet/0.1-trial` document or reuse an existing schema?
4. Which input fixture paths should be allowed initially?
5. What review questions should be generated per finding?
6. What tests are mandatory before implementation?
7. How should this packet support later report drafting without becoming a report generator yet?

## Expected Output

Write review to:

```text
handoff/cowork_p2_19_direction_review.md
```

Return:

- Decision: ACCEPT_FOR_IMPLEMENTATION / ACCEPT_WITH_CHANGES / DEFER / BLOCK
- Tier and boundary confirmation
- OSS references considered
- Adopt/adapt/ignore decisions
- Recommended deliverables
- Required tests
- Forbidden changes
- Suggested worker route
