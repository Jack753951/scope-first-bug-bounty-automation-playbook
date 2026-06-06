> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Live Bounty Tactical Preview and No-Finding Learning Loop

Use this reference when a live bounty run ends with `no_finding`, `surface_only`, `needs_second_account`, or another blocked/parked outcome. The goal is to keep safety gates while improving hit rate, not to turn each failed run into a one-off narrative.

## Durable lesson

After repeated no-finding runs, the main failure mode is usually not "no vulnerabilities exist". It is often one of:

- wrong target shape for the available controls;
- empty tenant/workspace with no safe owned objects;
- missing Account B / tenant B / role matrix;
- high-value surfaces blocked by policy or requiring payment/KYC/order/support state;
- thanks-only/VDP program suited for workflow practice rather than high-hit-rate hunting;
- preview collapsed too early into a checklist and did not preserve adjacent attack paths.

A no-finding run is useful only if it updates target selection, prerequisites, or the next tactical preview.

## Tactical preview shape

Before selecting the live lane, explicitly expand then contract:

```text
1. Build a permission-oriented target model: users, tenants, roles, objects, sharing, search/indexing, APIs, integrations, exports, audit/history, and lifecycle transitions.
2. List the default high-hit lane plus 3-5 adjacent lanes.
3. Classify each lane as safe_now, later_only, or blocked.
4. For each lane, name prerequisites: Account B, Tenant B, role matrix, safe owned object, API token, benign marker, program guidance, or operator-local action.
5. Select one bounded safe_now lane with positive/negative controls and stop conditions.
6. Preserve rejected/blocked lanes as next-preview seeds instead of discarding them.
```

Good adjacent lanes to consider without importing aggressive defaults:

- invite lifecycle and stale invitations;
- role downgrade / stale permissions;
- share revoke and public/private mismatch;
- draft/comment/internal-note boundary;
- audit/history visibility;
- export/import metadata leakage;
- API token scope mismatch;
- UI/API parity mismatch;
- GraphQL/object graph authorization;
- search/index/cache private-data exposure;
- OAuth/OIDC/account-linking confusion;
- webhook/integration misbinding (usually later_only);
- mobile/API parity mismatch;
- configuration/version exposure.

## No-finding closeout questions

For every parked or no-finding live lane, record the cause in a small feedback log and update future scoring:

```text
target/program:
status: no_finding | surface_only | needs_second_account | blocked | parked
missing controls: Account B? Tenant B? role matrix? safe owned object? API token? benign marker?
policy blockers: payment/KYC/order/support/upload/callback/scanner/fuzzer?
product blockers: empty state? no objects? no API? single-user-only?
evidence blocker: not reproducible? not impactful? cannot redact safely?
selection-rule update:
next-preview seeds:
park/resume decision:
```

## Target selection rules learned from no-finding runs

- Consumer/payment/order-heavy targets without benign free owned objects should be down-ranked until a safe owned-object plan exists.
- Empty SaaS/VDP workspaces are good for workflow practice but poor for high-hit-rate hunting unless they expose roles, owned objects, APIs, invite/share flows, or tenant controls.
- Thanks-only/VDP runs can validate intake, scope, evidence hygiene, and closeout, but should not be mistaken for the best vulnerability-yield route.
- If Account B / Tenant B is the key missing control, classify the target as `needs_second_account` or `needs_tenant_b`, not as exhausted.
- If no safe owned object exists, park quickly and move to a better-shaped target rather than broadening into risky surfaces.

## Operator Account A/B action-card pattern

When the next safe lane depends on operator-local account work, ask for non-sensitive status tokens rather than secrets. Safe replies include:

```text
Account B ready
Tenant B ready
Role matrix ready
Object visible
No safe object
blocked_auth
blocked_captcha
blocked_email_verification
blocked_phone_verification
blocked_warning
blocked_policy
blocked_no_object
stop
```

Never ask the operator to paste passwords, OTPs, cookies, tokens, verification links, phone numbers, raw aliases, payment/order/KYC/support data, or PII screenshots into chat or repo artifacts.

## Integration with project artifacts

In this user's cybersec lab, prefer keeping session-specific instances in repo handoff/Obsidian, while this skill stores the class-level pattern. Good repo artifacts include:

- `handoff/live_bounty_tactical_preview_template_<date>.md`
- `handoff/live_bounty_no_finding_feedback_log.md`
- `handoff/live_bounty_account_ab_operator_action_card_<date>.md`
- `handoff/active_strategy_queue.md`
- `handoff/current_navigation.md`
- `notes/obsidian_projects/Cybersec Lab.md`

Do not copy raw targets, secrets, OTPs, cookies, tokens, or private scope into the skill library.
