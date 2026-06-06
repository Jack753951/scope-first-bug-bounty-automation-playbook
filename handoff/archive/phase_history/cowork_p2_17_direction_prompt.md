> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Claude/Cowork Direction Prompt — P2.17 CTF Artifact + Review Decision Skeleton

Date: 2026-05-18
Proposed tier: T3 design review
Milestone: Phase 2 P2.17
Boundary: offline/local workflow tooling only

## Context

Recent blind picoCTF drills were used to validate the cybersec lab workflow:

- `Some Assembly Required 4`: false-positive UI/checker risk from C-string/NUL behavior.
- `Java Script Kiddie`: file-format invariants, CRC, and parser validation for candidate collapse.
- `vault-door-8`: source-transform inversion and re-application verification.
- `Clouds`: custom crypto + chosen-plaintext oracle; generic Z3 timeout triggered structure/literature escalation; public writeup flags were rejected unless verified against the live instance.

Hermes recorded the workflow lessons in:

```text
handoff/ctf_workflow_validation_and_escalation.md
handoff/ctf_tooling_backlog.md
```

Obsidian methodology was also updated under the Cybersec Lab namespace.

## Proposed P2.17 Direction

Build an offline/local skeleton that turns CTF practice into reusable platform workflow components:

1. `scripts/ctf_prepare_challenge.py`
   - creates `setting/local/ctf/<slug>/`
   - writes `challenge.json`
   - writes `solve_notes.md` with output-side review checklist
   - does not fetch or touch external services by default

2. `scripts/ctf_review_decision.py`
   - reads a small JSON result file
   - classifies status as `hint`, `candidate`, `verified`, or `needs_second_review`
   - triggers second review for abnormal format, multiple candidates, solver timeout, external-source-only answer, UI/checker-only success, active oracle/custom-crypto cases

3. `templates/ctf_verifier_metadata.yaml`
   - non-binding template initially, not a formal schema unless review recommends one

4. `tests/fixtures/ctf_review_decision/`
   - representative no-network fixtures

## Review Questions

Please review before Codex implementation:

1. Is this slice correctly scoped as offline/local and non-target-touching?
2. Should `ctf_verifier_metadata.yaml` remain a template, or should it become a versioned schema later?
3. Which OSS/reference formats should inform the review-decision output shape without overfitting to CTF?
   - Possible references: SARIF result levels, Nuclei template metadata, DefectDojo finding states, Semgrep result severity/confidence.
4. Are the second-review triggers complete enough for the current workflow?
5. What should be explicitly forbidden in P2.17 to avoid accidental target-touching or premature contract lock-in?
6. What minimal acceptance tests should Codex implement?

## Required Output

Write a concise direction review to:

```text
handoff/cowork_p2_17_direction_review.md
```

Use this structure:

```text
Verdict: ACCEPT_FOR_CODEX | ROUTE_BACK | REJECT
Tier: T2/T3/T4
Boundary Summary:
OSS Recon Gate Notes:
Recommended Scope:
Required Acceptance Tests:
Forbidden Changes:
Codex Task Notes:
```

## Safety Boundary

No live scans, target interaction, network clients, subprocess execution against external hosts, scanner/module runtime wiring, `config/scope.txt` changes, credentials, loot, reports, scheduler, deployment, billing, or production settings.
