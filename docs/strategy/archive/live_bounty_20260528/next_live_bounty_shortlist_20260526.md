> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Next live bounty high-hit-rate shortlist — 2026-05-26

Status: passive shortlist only / no target touched
Source: Hermes A0 passive OSINT using public <bug-bounty-platform> program-directory search endpoints
Date: 2026-05-26
Boundary: no target asset navigation, no account creation, no scope expansion, no scan/fuzz/exploit, no credential handling, no report submission. Public program-directory metadata/snippets are triage only and must be replaced by exact policy intake before any live request.

## Reviewer identity

- Reviewer route/tool: Hermes coordinator + terminal Python HTTPS requests to `https://<bug-bounty-platform>.com/programs/search?...`
- Visible runtime model: gpt-5.5
- Provider / CLI version if visible: openai-codex provider; exact backend deployment not exposed
- Review focus: passive OSINT / target scoring / high-hit-rate bug-class fit
- Limitation: scoring is based on directory metadata/snippets and keyword fit, not full legal policy confirmation

## Query set used

Public <bug-bounty-platform> program-directory searches only:

```text
workspace
tenant
team role
api authorization
project invite
organization role
share link
```

No program target assets were requested. No accounts were created. No scans, crawls, fuzzers, DAST, probes, or exploit payloads were run.

## Recommended next route

Use this shortlist to choose the next candidate after the second phone/Account B gate is ready, or if <program-redacted> remains blocked by `blocked_no_owned_object`.

Priority is not just highest score. Prefer the first candidate whose exact policy confirms:

1. self-service account/testing path;
2. Account A/B or tenant A/B feasibility;
3. safe owned object creation;
4. access-control/authz testing allowed;
5. no payment/KYC/order/support dependency for first proof.

## Passive scoring summary

| Rank | Program | Passive score | Why it appears promising | Main caution | Initial bug-class fit |
|---:|---|---:|---|---|---|
| 1 | `<program-redacted>` — <program-name> | 17 | Workspace/customer-ops/team platform; directory snippets match API, workspace/team, roles/invites, projects/objects, authz, self-owned accounts, share/public-private; open submissions | Full policy must confirm researcher account/testing route and avoid customer/support/message external effects | tenant/workspace isolation; role confusion; API authz; object ownership |
| 2 | `discourse` — Discourse | 15 | Forum/community platform with users, roles, permissions, posts/topics, APIs and public/private boundaries; open and bounty-active in snippet | Public/community content risk; first lane must use private/safe owned objects or local/user-owned instance if policy permits | role/permission confusion; object ownership; share/public-private |
| 3 | `hex` — Hex | 12 | Workspace/API/data-app style candidate; directory fit for API, workspace/team/roles, authz, share/public-private; triage active | Data/workspace content may be sensitive; avoid integrations, data connections, secrets | tenant/workspace isolation; API authz; role confusion |
| 4 | `frontegg` — Frontegg | 13 raw, downgraded to 12 | Identity/tenant/authz product shape is highly relevant: tenants, roles, API, authz, self-owned accounts | Identity/security platform and possible payment/tenant complexity; exact rules required; avoid auth bypass beyond owned controls | tenant isolation; role confusion; API authz |
| 5 | `airtable` — Airtable | 11 | Workspace/base/share/API product shape; rich object and permission surface | Infra/mobile risk in snippets; likely mature/high-competition; strict policy needed | object ownership; share/private boundary; API authz |
| 6 | `<program-slug>` — <program-redacted> | 11 | Already completed flow; known workspace/automation/API/role surface; exact policy captured | First lane produced `surface_only`; deeper value requires second tenant/user/API plan; workflow/run-script/integration remain A4 blocked | tenant/workspace isolation; API authz after separate plan |
| 7 | `<program-slug>` — <program-redacted> | 13 raw, downgraded to 10 | SaaS/customer-engagement/API/workspace shape likely rich | Messaging/customer-impact, scanner restrictions, mobile/integration risks; avoid outbound sends/integrations | role/API authz only if policy and owned sandbox permit |
| 8 | `databricks` — Databricks | 15 raw, downgraded to 10 | Workspace/project/API/role fit is strong | High-impact cloud/data platform; avoid clusters, execution, secrets, integrations unless explicitly allowed | docs-only or very narrow owned workspace authz, if policy permits |

Programs with high raw keyword score but lower practical fit for the immediate next lane:

- `starbucks`, `starbucks_china`, `starbucks_japan`: consumer/payment/account/order risk; likely not ideal for A/B object testing without purchase/payment state.
- `modern_treasury`, `paypal`, `grab`: finance/payment risk; avoid for now.
- `uber`, `netflix`, `spotify`, `pixiv`, `shopify`: large/mature/complex programs; may be valuable later but need careful policy intake and likely more competition or higher-risk surfaces.
- `lark_technologies`, `pingidentity`, `adobe`, `mercadolibre`, `floqast`: possible fit but either enterprise/identity/payment/platform complexity or policy-specific constraints require a separate intake before prioritizing.

## Top candidate details

### 1. `<program-redacted>` — <program-name>

<bug-bounty-platform>: `https://<bug-bounty-platform>.com/<program-redacted>`

Passive reasons:

- Public directory snippet matched `workspace` and `api authorization` queries.
- Product shape appears to involve teams/customer operations and likely shared objects, roles, comments/conversations, inboxes, or APIs.
- Good high-hit-rate shape if the program allows owned-account/team testing.

Potential first lane after policy intake:

```text
bug class: role/permission or workspace object ownership
prerequisites: two owned users or test team, safe owned object, no external customer/email/support effects
first proof: one object family only, A positive / B negative, no outbound messages
```

Primary caution:

Customer-ops/email/helpdesk products can have external-message/support side effects. Do not send messages, invite third parties, connect mailboxes, or touch integrations unless exact policy and a separate plan allow it.

### 2. `discourse` — Discourse

<bug-bounty-platform>: `https://<bug-bounty-platform>.com/discourse`

Passive reasons:

- Product has obvious user/role/permission/content/API/share boundaries.
- Good object model: topics, posts, categories, groups, invites, private messages, permissions.

Potential first lane:

```text
bug class: role/permission confusion or private/public object boundary
prerequisites: owned test accounts; policy confirms which hosted/community assets are in scope; safe private object or group/category
first proof: private object access negative control from Account B or lower role
```

Primary caution:

Do not use public content, spam, social engineering, or other users' data. Full scope must identify exact allowed Discourse-hosted property or test environment.

### 3. `hex` — Hex

<bug-bounty-platform>: `https://<bug-bounty-platform>.com/hex`

Passive reasons:

- Workspace/data app/API style surface is a good match for tenant isolation and API authorization.
- Likely has projects/docs/apps/sharing/roles.

Potential first lane:

```text
bug class: workspace isolation or API authz mismatch
prerequisites: owned workspace(s), safe dummy project/object, no data connections/secrets
first proof: Account A project read vs Account B denied; optional API mirror only if docs/policy allow
```

Primary caution:

Do not connect databases, import sensitive data, create secrets, run compute/jobs, or publish/share externally without a separate plan.

### 4. `frontegg` — Frontegg

<bug-bounty-platform>: `https://<bug-bounty-platform>.com/frontegg`

Passive reasons:

- Identity/multi-tenant product shape strongly matches role, tenant, and API authorization bugs.

Potential first lane:

```text
bug class: role/tenant authorization matrix
prerequisites: official researcher/test tenant path, second user/role support, allowed API checks
first proof: role downgrade / lower-role negative control on one harmless owned object
```

Primary caution:

Identity platforms are sensitive. Avoid authentication bypass, account takeover, brute force, MFA, password reset, session secret handling, or tenant-crossing tests without explicit policy and owned controls.

### 5. `airtable` — Airtable

<bug-bounty-platform>: `https://<bug-bounty-platform>.com/airtable`

Passive reasons:

- Workspace/base/table/API/share-link product shape is ideal for object ownership and public/private boundary testing.

Potential first lane:

```text
bug class: share/public-private boundary or API object authorization
prerequisites: owned base/table, Account B or unauth control, policy allows account-owned object testing
first proof: private base/table not accessible after share revoke or to Account B
```

Primary caution:

Do not import sensitive data, publish public bases broadly, connect integrations/automations, or test beyond owned workspace.

## Immediate next actions

1. Before second phone is ready: use this shortlist for passive policy intake of only the top 1-2 candidates, starting with `<program-redacted>` unless the operator prefers a different program.
2. After second phone is ready: first try the <program-redacted> Account B gate only if it can produce a safe owned object; otherwise park <program-redacted> quickly.
3. If <program-redacted> is parked, move to the highest-scoring SaaS/workspace candidate whose exact policy confirms A/B or tenant testing.

## Do-not-do list

- Do not add any shortlist host to `config/scope.txt` until exact policy intake and operator confirmation.
- Do not browse candidate app/login/target assets during passive shortlist.
- Do not run recon/scanners/fuzzers/DAST from this artifact.
- Do not create accounts, tenants, invitations, API keys, credentials, integrations, workflows, or public shares from this artifact.
- Do not submit or draft a report from passive OSINT alone.
