> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# CTF-to-Platform Tooling Backlog

Date: 2026-05-18
Status: Proposed next implementation slice

## Objective

Turn recent CTF workflow lessons into small, safe tooling that improves the broader authorized bug-bounty platform without adding target-touching risk.

## Proposed Slice P2.17: CTF Artifact + Review Decision Skeleton

Review tier recommendation: T2/T3

Rationale:

- Primarily local artifact/workflow tooling.
- Does not perform scanning or exploitation by itself.
- Touches workflow conventions and may define reusable metadata, so independent review is useful before it becomes a contract.

### Deliverables

1. Local artifact preparer

Suggested path:

```text
scripts/ctf_prepare_challenge.py
```

Responsibilities:

```text
- create setting/local/ctf/<slug>/
- write challenge.json metadata
- write solve_notes.md skeleton
- include output-side review checklist
- include Kali-first reminder if external service/URL is present
- never fetch external targets by default
```

2. Review decision helper

Suggested path:

```text
scripts/ctf_review_decision.py
```

Responsibilities:

```text
- read a small JSON result file
- classify result as hint/candidate/verified/needs_second_review
- trigger second review for:
  - abnormal flag format
  - multiple candidates
  - tool timeout
  - external writeup-only answer
  - checker/UI-only success
  - oracle/stateful/custom-crypto task
```

3. Metadata template

Suggested path:

```text
templates/ctf_verifier_metadata.yaml
```

Fields:

```yaml
id: example-verifier
category: crypto|web|reverse|forensics|misc|pwn|unknown
mode: offline|oracle|active-service|reconstruction
requires_scope: true
destructive: false
uses_external_service: false
oracle_required: false
confidence: candidate
second_review_triggers:
  - abnormal_format
  - multiple_candidates
  - solver_timeout
  - external_source_only
evidence_outputs:
  - raw_artifact
  - candidate
  - verification_log
```

4. Tests / dry-run fixtures

Suggested path:

```text
tests/fixtures/ctf_review_decision/
```

Cases:

```text
- verified_normal_flag.json
- no_wrapper_flag_verified.json
- ui_only_candidate_needs_review.json
- multiple_candidates_needs_review.json
- solver_timeout_needs_review.json
- external_writeup_only_needs_review.json
```

## Acceptance Criteria

```text
[ ] scripts are offline/local by default
[ ] no external network calls unless explicitly designed later
[ ] setting/local remains ignored
[ ] review decision helper returns structured JSON
[ ] abnormal/no-wrapper flag cases are represented in fixtures
[ ] tests pass
[ ] docs mention Kali-first policy for external interaction
```

## Why this advances the main project

This adds a low-risk bridge from CTF practice to the bug-bounty platform:

```text
CTF candidate answer
  -> structured evidence
  -> review decision
  -> second-review trigger
```

The same shape later maps to:

```text
scanner finding candidate
  -> structured evidence
  -> review decision
  -> verifier/script selection
```
