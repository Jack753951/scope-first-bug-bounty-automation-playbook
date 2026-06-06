> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Attacker-perspective routing note

Use when the user asks whether `攻擊者視角`, realistic attacker paths, tactical freedom, or high-impact adversarial ideas are preserved in the Cybersec/Hermes workflow.

Core rule

Do not delete a tactic merely because a real attacker could use it dangerously. Preserve realistic attack-path thinking, then compile each path into bounded proof controls:

```text
attack path -> proof boundary -> proof surrogate -> stop-before -> evidence packet
```

Routing

- Live bug bounty / authorized assessment planning: load `cybersecurity-workspace-orchestration` reference `tactical-freedom-proof-surrogate-platform.md`.
- Multi-agent adversarial review: load `subagent-driven-development` reference `role-separated-adversarial-planning.md` and split reviewers into adversarial planner, boundary engineer, evidence critic, and Hermes synthesis.
- Disposable local single-vulnerability proof waves: load `owasp-single-vuln-lab-wave`; use its tactical preview and post-evidence review gates.

Operational meaning

- `adversarial planner` preserves realistic/high-impact paths and does not grant authorization.
- `boundary engineer` converts each path into scope, owned-object/account requirements, proof boundary, proof surrogate, stop-before rules, and execution status.
- `evidence critic` rejects weak, sensitive, non-owned, or non-reportable evidence.
- `Hermes synthesis` selects at most one bounded executable lane, parks/preserves blocked candidates, or stops at operator/scope gate.

Execution statuses to preserve

- `bounded_executable`
- `blocked_preserve`
- `needs_scope`
- `needs_operator_control`
- `needs_local_simulation`
- `reference_only`

Pitfall

Do not answer “yes, it is in skills” from memory alone. Inspect the relevant skill/reference files or loaded-skill content when possible, then name the exact skill/reference locations. If the umbrella SKILL.md is too large to patch directly, add/update this reference file and report that the pointer still needs a future SKILL.md split/compaction before it can be inserted at the top level.
