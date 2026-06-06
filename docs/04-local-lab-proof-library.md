# 04 — Local Lab Proof Library

Status: public methodology

## Goal

Turn one-off lab experiments into reusable proof patterns that can later guide
authorized live testing without implying live confirmation.

## Proof wave shape

```text
1. Choose one vulnerability behavior/class.
2. Read mature public references and source/tooling first.
3. Select the maximum safe proof for the disposable lab.
4. Define positive evidence and negative controls.
5. Run a bounded script with pre/post health checks.
6. Preserve artifacts and cleanup result.
7. Classify honestly: verified lab-only, candidate, attempted-not-verified,
   blocked, deferred, or reference-only.
8. Promote only reusable patterns into a bundle.
```

## Evidence types worth preserving

- True attacker-side callback in an isolated lab, with source/context labels.
- Browser-runtime marker in the correct origin/session context.
- Safe-marker file read/write with false-positive controls.
- Role/account boundary proof with unauthenticated, normal-user, and privileged controls.
- Bounded state-change evidence with cleanup verification.
- Metadata exposure triage that stays candidate-only until impact is proven.

## Bundle fields

```text
Name:
Vulnerability behavior:
Applicable product/surface shape:
Authorization boundary:
Required lab topology:
Preconditions:
Positive evidence:
Negative controls:
Cleanup:
Limitations:
Live-target prerequisites:
Stop-before rules:
Reusable commands/scripts:
```

## Non-goals

- Do not claim real-world exploitability from a lab-only proof.
- Do not store secret-bearing raw responses.
- Do not turn scanner output into a finding without manual proof and controls.
