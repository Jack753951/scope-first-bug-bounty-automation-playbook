> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Live bounty attack-path candidate packet

Status: template / planning only
Boundary: this packet models realistic attacker paths for authorized security research planning. It does not authorize target-touching, scanning, exploitation, account creation, callbacks/OAST/tunnels, non-owned data access, destructive actions, DDoS/resource exhaustion, credential handling, malware, stealth/persistence/evasion, or report submission.

## Reviewer identity

- Reviewer route/tool:
- Visible runtime model:
- Provider / CLI version if visible:
- Review focus: adversarial planning | boundary engineering | evidence critique | Hermes synthesis
- Limitation:

## Program facts

```text
program_slug:
packet_id:
authorization_source:
scope_artifact:
current_handoff:
operator-owned controls available: Account A / Account B / tenant A / tenant B / owned object / none
policy/rules facts known:
explicitly forbidden actions:
```

## Product model

Describe the target as a permission and state-transition system.

```text
actors:
tenants_or_workspaces:
roles:
objects/resources:
api_surfaces:
state_transitions:
object-id provenance paths:
public/private/share boundaries:
sensitive surfaces:
```

## Attack-path candidates

Preserve realistic attacker-like hypotheses even when they cannot be executed today. Do not delete a high-impact idea merely because the raw attacker path is dangerous; compile it into a proof boundary or park/preserve it.

| candidate_id | title | impact potential (1-5) | surrogate feasibility (1-5) | authorization readiness (1-5) | impact hypothesis | required prerequisites | execution status |
|---|---|---|---|---|---|---|---|
| | | | | | | | bounded_executable / blocked_preserve / needs_scope / needs_operator_control / needs_local_simulation / reference_only |

For each candidate, fill this block:

### Candidate: `<candidate_id>`

#### Ranking inputs

```text
impact_potential: 1-5
surrogate_feasibility: 1-5
authorization_readiness: 1-5
```

#### Role-separated notes

```text
adversarial_planner_findings:
boundary_engineer_controls:
evidence_critic_objections:
hermes_synthesis_decision:
```

#### Attacker path

```text
1.
2.
3.
```

#### Proof boundary

```text
in_scope_assets:
owned_accounts_or_objects:
request_budget:
allowed_state_changes:
blocked_state_changes:
callback_oast_tunnel_allowance: not_allowed / allowed_by_policy_with_operator_approval / local_lab_only
data_contact_boundary:
```

#### Proof surrogate

```text
method:
why_it_proves_impact_without_harm:
positive_control:
negative_control:
```

#### Stop-before rules

```text
unauthorized_access:
non_owned_data:
destructive_impact:
dos_or_resource_exhaustion:
credential_or_token_access:
malware_persistence_evasion:
scope_expansion:
report_submission:
```

#### Evidence requirements

```text
minimum_positive_evidence:
minimum_negative_control:
redaction:
status_threshold_candidate:
status_threshold_report_ready:
```

## Decision

```text
selected_candidate_id:
decision: select_bounded_lane / park_preserve / blocked_awaiting_scope / blocked_awaiting_operator / switch_target / needs_local_simulation
reason:
next_artifact:
```

Selection rule: selected executable lanes must have a proof boundary, proof surrogate, stop-before rules, positive control, negative control, and redaction plan. If a candidate lacks those, preserve it as parked/blocked rather than erasing it.

## JSON companion shape

When machine validation is useful, write a JSON companion conforming to:

```text
schemas/attack_path_candidate.schema.json
```
