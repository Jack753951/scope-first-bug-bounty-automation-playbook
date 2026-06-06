> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Security Fixture Terminal-State Matrix Pattern

Use this when a cybersec/security workflow already has offline synthetic fixtures that run end-to-end, but the next slice needs stronger regression guarantees without changing runtime behavior.

## Trigger

Apply after a fixture-only slice has proven that cases can run through the offline chain, but assertions are still mostly aggregate, such as:

- at least one `blocked` state exists;
- at least one `needs_manual_review` state exists;
- no promotional words appear;
- deterministic output is byte-identical.

The next hardening slice should bind each fixture/finding to exact expected states at every stage.

## Pattern

1. Keep the slice test-only unless a separate direction review authorizes behavior changes.
2. Add a focused RED test that references a missing expectation matrix constant or fixture expectation file.
   - Expected RED example: `NameError: P3_2_EXPECTED_TERMINAL_STATES is not defined`.
3. Build the workflow from the existing committed offline fixtures.
4. Index every stage by stable finding ID.
5. Assert all stages contain exactly the expected finding IDs.
6. For each finding, assert stage-specific terminal values, for example:
   - packet readiness / triage readiness;
   - gap review state;
   - required gap codes as a subset, not necessarily exact equality if existing consumers may add safe explanatory codes;
   - verification plan state;
   - report-readiness gate state.
7. Assert no promotional values appear if the workflow is still trial-only / triage-only.
8. Run focused tests, full adjacent suite, and the project review gate.
9. Record the boundary in handoff: tests/handoff only, no fixture content changes unless explicitly needed, no consumer behavior changes, no live targets, no schema promotion, no report drafting, no runtime/recon wiring.

## Example shape

```python
EXPECTED_TERMINAL_STATES = {
    "synthetic.partial_evidence.candidate": {
        "packet_readiness": "not_ready",
        "gap_review_state": "not_ready",
        "plan_state": "blocked",
        "gate_state": "blocked",
        "required_gap_codes": {"LOW_CONFIDENCE", "MANUAL_VERIFICATION_REQUIRED"},
    },
    "synthetic.ambiguous_scope.candidate": {
        "packet_readiness": "reviewer_decision_required",
        "gap_review_state": "reviewer_decision_required",
        "plan_state": "needs_manual_review",
        "gate_state": "needs_manual_review",
        "required_gap_codes": {"MANUAL_VERIFICATION_REQUIRED"},
    },
}
```

When comparing gap codes, prefer `expected_codes.issubset(set(actual_codes))` unless the consumer contract promises exact code lists. This avoids making the regression brittle while still locking the safety-critical reasons.

## Pitfalls

- Do not implement dedupe, conflict resolution, severity remapping, or new workflow behavior inside a terminal-state assertion slice. If the matrix exposes a desired behavior change, route a separate direction review.
- Do not store real program names, real disclosed URLs, real bounty targets, or live target scope in fixture expectation matrices. Use synthetic IDs/domains.
- Do not assert that a control/non-finding case is reportable. In trial bug-bounty workflows, benign controls should remain blocked or not-ready until an explicit reporting contract exists.
- Do not infer the scope of the slice from a noisy working tree. Attribute changed files explicitly in the handoff entry.
