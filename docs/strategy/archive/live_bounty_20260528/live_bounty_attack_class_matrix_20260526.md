> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Live bounty attack-class matrix — 2026-05-26

Status: active / reusable matrix
Source: Hermes synthesis from proof-library bridge and live-bounty high-hit-rate filter
Date: 2026-05-26
Boundary: planning only. Does not authorize target-touching, scope expansion, scanning, exploit execution, callbacks, workflow/run-script/integration tests, non-owned data access, or report submission.

## Reviewer identity

- Reviewer route/tool: Hermes local synthesis
- Visible runtime model: gpt-5.5
- Provider / CLI version if visible: openai-codex provider; exact backend deployment not exposed
- Review focus: tactical live-bounty planning and evidence thresholds
- Limitation: exact program rules still win; this matrix must be adapted per `programs/<slug>/scope.json`

## How to use this matrix without killing tactical freedom

This matrix defines reusable proof shapes and evidence standards. It is not the full attack surface and not a ban on other tactics.

For each preview:

1. Start with the five default matrices below because they have the best first-pass evidence/control ratio.
2. Then add adjacent product-specific hypotheses from OSINT, docs, disclosed reports, PortSwigger/OWASP examples, SDKs, and visible feature shape.
3. Classify each adjacent idea as `safe_now`, `later_only_needs_plan`, `blocked_by_policy`, `blocked_by_missing_control`, or `blocked_high_risk`.
4. If an adjacent idea is better than the default matrix and has clean owned controls, select it. Otherwise preserve it as a next-preview seed instead of deleting it.

A good preview increases options; the matrix only helps decide which option can be executed safely and evidenced well today.

## Matrix 1 — IDOR / BOLA / object ownership

Use when:

- Account A and Account B are operator-owned or program-provided.
- Object IDs are obtained from normal UI/API provenance.
- Program allows low-speed account-owned authorization testing.
- Object is safe: project, story, document, folder, note, cart/wishlist-like benign state, profile metadata, or similar.

Do not use when:

- Only one account exists.
- Object IDs must be guessed.
- Evidence requires payment/order/KYC/support/recovery/upload/seller/admin.
- Any request might expose third-party data.

Minimum proof:

| Test | Account A positive | Account B negative | Evidence |
|---|---|---|---|
| Read own object | A can read A object | B cannot read A object | redacted status/path/body excerpt |
| Edit own object | A can edit harmless marker | B cannot edit A marker | before/after marker + denied B attempt |
| List isolation | A list includes A object | B list excludes A object | list excerpt with IDs redacted/labelled |
| API direct fetch | A token/session fetches A object | B token/session denied | 403/404/redirect or equivalent |

Status labels:

- `candidate`: one boundary looks inconsistent but controls incomplete.
- `report_ready`: scoped, allowed, reproducible, A/B controls complete, no third-party data, meaningful impact.
- `blocked_missing_account`: no Account B.
- `blocked_no_owned_object`: no safe object.

## Matrix 2 — Tenant / workspace isolation

Use when:

- Two owned tenants/workspaces can exist, or program provides test tenants.
- Tenant/workspace/resource identifiers appear in UI/API.
- Resources are safe and owned.

Minimum proof:

| Test | Tenant A positive | Tenant B negative | Evidence |
|---|---|---|---|
| Resource read | A reads A resource | B cannot read A resource | redacted request/response |
| Workspace switch | A sees only A tenant resources | B sees only B tenant resources | UI/API list controls |
| Resource mutation | A changes harmless owned marker | B denied changing A marker | marker diff + denial |
| Invite/membership boundary | A owner/member action works as allowed | B non-member denied | role/member labels only |

Blocked by default:

- Cross-tenant testing without owned controls.
- Third-party tenant data.
- Integrations/webhooks/workflow execution/run-script unless separately approved.

## Matrix 3 — Role / permission confusion

Use when:

- Owned tenant supports owner/admin/editor/viewer/member roles.
- Operator can create or invite a second owned user without spam/social-engineering risk.
- UI and API expose comparable actions.

Minimum proof:

| Role test | Higher role | Lower role | Evidence |
|---|---|---|---|
| UI action | Owner can access control | Viewer/member cannot | UI state + denied attempt |
| API action | Owner API succeeds | Lower role API denied | status/path/body excerpt |
| Disabled UI bypass | Lower role UI disabled | Direct request also denied | control + negative request |
| Role change | Owner changes benign role | Lower role cannot self-escalate | before/after role labels |

Do not test:

- Billing/admin/seller/partner surfaces without explicit legitimate role.
- Password/security setting mutation unless plan allows it.
- Invite spam or third-party accounts.

## Matrix 4 — API authorization mismatch

Use when:

- Official API docs or observed first-party API endpoints exist.
- Account-owned tokens/sessions are available without storing secrets in artifacts.
- Endpoint maps to a UI object already proven safe.

Minimum proof:

| API test | Positive control | Negative control | Evidence |
|---|---|---|---|
| GET object | A reads A object | B denied A object | endpoint path + redacted status/body |
| PATCH/PUT marker | A updates harmless marker | B denied A marker | marker before/after + denial |
| List endpoint | A list shows A objects | B list omits A objects | redacted IDs/labels |
| UI/API mismatch | UI denies lower role | API also must deny | mismatch only if API succeeds incorrectly |

Blocked:

- Broad endpoint fuzzing.
- DAST/scanners.
- Token/secret/API-key storage.
- Non-documented destructive methods.

## Matrix 5 — Share link / public-private boundary

Use when:

- Owned object supports private/public/share/unshare/revoke states.
- Public/unauth view is clearly intended and safe.
- No third-party or secret content is exposed.

Minimum proof:

| Boundary | Expected | Evidence |
|---|---|---|
| Private unauth | Unauthenticated cannot access | 401/403/404/redirect |
| Shared unauth | Shared link only exposes intended object | redacted page/API excerpt |
| Revoked link | Link stops working after revoke | before/after status |
| Permission downgrade | Lower role loses access | role state + denied access |

Blocked:

- Public publication to real audience unless explicitly approved.
- Sensitive content in shared object.
- Guessing unlisted links.

## <program-redacted> Account B run-card seed

When the second phone/account is ready:

1. Operator creates/verifies Account B locally. Hermes records only `Account B`.
2. Reconfirm <program-redacted> program policy/scope and current logged-in noVNC state.
3. Identify safe object families from normal UI only.
4. If no safe owned object exists, label `blocked_no_owned_object` and park.
5. If a safe object exists, run only one object family through Matrix 1.
6. Do not touch payment, checkout, KYC, order creation, support/contact, recovery, coupon redemption, seller/admin, scanner/fuzzer, or guessed IDs.

## <program-redacted>/SaaS deepen seed

For a future SaaS/workspace target, prefer Matrix 2-4. First do passive API/docs review, then Account A/B or tenant A/B controls, then one safe object family. Do not execute workflows, run-script, integrations, callbacks, Workbench/tool prompts, or API-key/credential creation without a separate A4 plan.
