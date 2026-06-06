> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Live bounty tactical preview template — 2026-05-26

Status: active / reusable preview template
Source: Hermes synthesis after high-hit-rate workflow correction
Date: 2026-05-26
Boundary: planning and preview only. This template does not authorize target-touching, account creation, scope expansion, scanner/fuzzer/DAST, exploit execution, callbacks/OAST, payment/KYC/order/support flows, non-owned data access, credential handling, or report submission.

## Purpose

Use this template before any nontrivial authorized live-bounty/VDP execution. The goal is to improve tactical vision and tactical freedom before narrowing into one bounded, legal, evidence-ready lane.

Preview must not collapse into a checklist. It should first expand plausible attack paths from the product shape, public methodology, official docs, disclosed reports, SDK/API docs, and prior local proof patterns. Do not delete a tactic merely because a real attacker could use it dangerously. Instead, compile each realistic attack path into a proof boundary, proof surrogate, and stop-before rule; choose only the best lane that can be legally and safely executed now.

Correct loop:

```text
expand realistic attack paths -> compile proof boundary/surrogate/stop-before rules -> choose one bounded lane -> preserve rejected/blocked ideas as next-preview seeds
```

Primary machine-readable companion:

```text
schemas/attack_path_candidate.schema.json
templates/live_bounty_attack_path_candidate_packet.md
scripts/live-bounty-preview-synthesize.py
```

## Inputs

```text
program_slug:
program_url:
authorization_source:
current_scope_artifact: programs/<slug>/scope.json or pending
current_handoff:
operator-owned accounts available: Account A / Account B / tenant A / tenant B / none
policy facts known:
forbidden actions:
product shape:
public docs/API/SDK links:
disclosed report / methodology references:
local proof patterns that may map:
current blockers:
```

Do not include secrets, phone numbers, OTPs, cookies, passwords, raw aliases, tokens, API keys, or third-party data. Use Account A/B labels.

## Section 1 — Product/permission model sketch

Summarize the target as a permission system, not as a website map.

```text
Actors:
Tenants/workspaces/orgs:
Roles/memberships:
Objects/resources:
Object ID provenance paths:
Public/private/share boundaries:
API/UI parity surfaces:
Lifecycle transitions: create/share/invite/revoke/delete/archive/export/import
Sensitive or later-only surfaces:
```

## Section 2 — Attack-path expansion table

List at least one default high-hit lane and 3-5 adjacent creative lanes. More is allowed when useful. Preserve realistic attacker-like paths even when they are not executable today.

| Attack path idea | Why this product might fail here | Required controls | Proof surrogate | Stop-before rule | Status |
|---|---|---|---|---|---|
| Default IDOR/BOLA/object ownership | | Account A positive + Account B negative + owned object provenance | A/B status/body-shape comparison without reading non-owned content | stop before non-owned data access | bounded_executable / blocked_preserve / needs_scope / needs_operator_control / needs_local_simulation / reference_only |
| Tenant/workspace isolation | | Tenant A/B + owned resource | | | |
| Role downgrade / permission confusion | | Owner/member or editor/viewer controls | | | |
| UI/API permission mismatch | | UI action denied but API direct action possible, or reverse | | | |
| Share/revoke/public-private lifecycle | | Share link / revoke / public-private boundary | | | |
| Product-specific adjacent idea | | | | | |

Execution-status vocabulary:

```text
bounded_executable
blocked_preserve
needs_scope
needs_operator_control
needs_local_simulation
reference_only
```

Adjacent lane examples to consider when product shape supports them:

- invite lifecycle / stale invite / role change propagation;
- role downgrade stale permissions;
- share link revocation or public/private mismatch;
- draft/comment/internal-note boundary;
- audit-log or history visibility;
- export/import metadata or hidden-field leakage;
- API token scope mismatch;
- UI/API parity mismatch;
- GraphQL/object graph traversal authorization;
- search/index/cache private data exposure;
- OAuth/OIDC/account-linking flow confusion;
- webhook/integration misbinding (usually later-only/A4 unless explicitly allowed);
- mobile/API parity mismatch;
- configuration/version exposure with policy value.

## Section 3 — OSS/public grounding

Use read-only references to improve test design and controls. These are not permission to run scanners or exploit templates.

```text
OWASP WSTG/ASVS controls consulted:
PortSwigger labs/topics consulted:
Public disclosed reports consulted:
Official product docs/API/SDK consulted:
OSS/tooling/templates consulted as reference-only:
Adopt / wrap / adapt / reference-only / write-custom decision:
```

## Section 4 — Select one bounded lane for execution

```text
selected_lane:
selected_candidate_id:
why selected over alternatives:
why bounded now:
why high-hit-rate:
scope/policy basis:
request budget:
rate / concurrency:
required accounts/roles:
object/resource needed:
positive control:
negative control:
normal provenance path for IDs:
proof_surrogate:
stop_before unauthorized access:
stop_before non-owned data:
stop_before destructive impact:
stop_before DDoS/resource exhaustion:
stop_before credential/token access:
redaction requirements:
expected evidence:
status threshold for candidate:
status threshold for report_ready:
```

Selection rule: pick the highest-value lane that is both legal and evidence-ready today. If a creative adjacent lane is better than the default high-hit lane and has clean owned controls, select it.

## Section 5 — Parked ideas / next-preview seeds

Do not delete ideas just because they are not executable today. Preserve them.

| Idea | Current blocker | What would unlock it | Next-preview trigger |
|---|---|---|---|
| | | | |

## Section 6 — Operator action card, if needed

Use this only for local actions that Hermes must not perform or record.

```text
Operator action required: yes/no
Action label: Account B ready / tenant B ready / object visible / policy guidance needed / unlock noVNC / CAPTCHA / email verification / phone verification
Do not share: password, OTP, phone number, cookies, tokens, API keys, verification links, raw PII
User should reply with only: <safe status phrase>
Blocked status phrase if failed: blocked_auth / blocked_no_object / blocked_policy / blocked_warning
```

## Section 7 — Preview decision

```text
decision: proceed_safe_now | blocked_awaiting_operator | blocked_awaiting_scope | switch_target | park_target | create_bundle | ask_program_guidance
next_action:
next_artifact:
review_required: Hermes self-review / Claude-Cowork review / Codex script review / operator decision
```

## Anti-patterns

- Do not ask only “can we do IDOR?” and stop.
- Do not treat the default five high-hit bug classes as a whitelist.
- Do not convert creative A4 ideas into execution without proof-boundary, proof-surrogate, stop-before rules, exact policy/scope, owned controls, and explicit approval.
- Do not let a no-finding erase tactical ideas; preserve them as blocked/parked seeds.
- Do not write secrets, phone numbers, OTPs, cookies, tokens, or third-party data into this template.
- Do not treat the L0-L5/risk labels as the main planning primitive; the durable primitive is attack path -> proof boundary -> proof surrogate -> stop-before -> evidence packet.
