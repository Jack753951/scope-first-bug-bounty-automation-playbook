> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Tactical-freedom proof-surrogate platform

Use when a cybersecurity / bug-bounty workspace needs to preserve realistic attacker-like ideation without authorizing harmful execution.

Session lesson

- Do not delete a tactic merely because a real attacker could use it dangerously.
- Convert each realistic attack path into a bounded planning packet:
  - attack path / impact hypothesis
  - proof boundary
  - proof surrogate
  - stop-before rules
  - evidence requirements
  - execution status
- Hermes remains the synthesis and authorization gate. Multi-agent reviewers may propose paths or objections, but they do not grant execution permission.

Recommended class-level primitive

```text
attack path -> proof boundary -> proof surrogate -> stop-before -> evidence packet
```

Avoid making L0-L5 / risk labels the main primitive. Risk labels help route work, but the durable unit is a candidate path with explicit proof controls.

Minimum machine-readable candidate packet

Each packet should contain at least five realistic candidate paths so preview does not collapse into a single easy lane. For each candidate, include:

- `impact_potential` 1-5
- `surrogate_feasibility` 1-5
- `authorization_readiness` 1-5
- `proof_boundary`
- `proof_surrogate`
- `stop_before`
- `evidence_requirements`
- `execution_status`

For selected `bounded_executable` candidates, fail closed unless the proof boundary includes concrete, non-empty:

- in-scope assets
- owned accounts/objects or equivalent operator-controlled test data
- allowed state changes
- blocked state changes
- callback/OAST/tunnel allowance
- data-contact boundary

Required stop-before categories

- unauthorized access completion
- non-owned data
- destructive impact
- DDoS / resource exhaustion
- credential or token access
- malware / persistence / evasion
- scope expansion
- report submission

Preserve high-impact blocked ideas

Use execution statuses such as:

- `bounded_executable`
- `blocked_preserve`
- `needs_scope`
- `needs_operator_control`
- `needs_local_simulation`
- `reference_only`

Blocked high-impact candidates should become future preview seeds, local simulation ideas, or operator-gated routes, not disappear from the plan.

Multi-agent role separation

A useful review packet separates:

- adversarial planner: what realistic attacker-like paths exist
- boundary engineer: what proof boundary and stop-before controls are required
- evidence critic: what evidence would be weak, sensitive, or non-reportable
- Hermes synthesis: select one bounded lane, park/preserve, switch target, or require operator/scope gate

Pitfall

If reviewers only fill the same generic table, multi-agent review becomes duplicated opinion instead of role separation. Ask for role-specific findings and require Hermes to synthesize disagreements.

Validation pattern

For offline helpers, add tests proving:

- valid five-candidate packet passes
- dangerous blocked candidate is preserved
- selected executable lane missing proof surrogate fails
- selected executable lane missing stop-before fails
- selected executable lane with empty proof boundary fails
- selected executable lane missing callback/OAST/tunnel allowance fails
- multiple selected executable lanes fail
- sorting uses impact potential + proof-surrogate feasibility + authorization readiness

Boundary

This pattern is planning and validation only. It does not authorize target requests, browser automation, signup/login, scanning, fuzzing, DAST, exploit execution, callback/OAST/tunnel use, credential handling, non-owned data access, destructive action, DDoS/resource exhaustion, scope expansion, or report submission.
