> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# <program-name> (`<program-redacted>`) target selection preview — 2026-05-26

Status: selected candidate / pending exact asset-scope confirmation
Route/tool: Kali VM `<attacker-vm>` via `scripts/kali-run.ps1`; public <bug-bounty-platform> JSON endpoints only
Boundary: passive policy/program-directory intake only. No <program-name> app/signup/login target asset navigation, no account creation, no scope expansion, no scan/fuzz/exploit, no credential handling, no customer interaction, no report submission.

## Decision

Recommended first target for the new high-hit-rate workflow: `<program-redacted>` / <program-name>.

<bug-bounty-platform> program: `https://<bug-bounty-platform>.com/<program-redacted>`

Why this is the best next target from the checked candidates:

- It is an open, bounty-paying <bug-bounty-platform> program with public policy metadata available.
- Product shape is a customer-operations/team workspace platform, which is a strong fit for tenant/workspace isolation, role/permission confusion, object ownership, and API authorization mismatch.
- Policy explicitly says <program-name> is especially interested in cross-company/cross-tenant data disclosure.
- Policy has a clear researcher signup route and identity requirement: use the <program-name> signup URL in policy and a <bug-bounty-platform> `@researcher-alias.example` alias, with company name pattern `[Bug Bounty] SomeCompanyName`.
- Policy links API documentation: `https://dev.frontapp.com/`.
- It has clearer immediate signup/testability than `hex`, which requires emailing for a bounty instance and currently shows `offers_bounties=false` in the public JSON.
- It is less identity-platform-sensitive than `frontegg`, though Frontegg remains a strong backup once we want a more authN/authZ-heavy lane.
- It is less constrained by temporary bounty suspension than `discourse`.
- It avoids Airtable's enterprise-account/request path as the first new-process run.

## Passive facts observed from Kali

Observed through public <bug-bounty-platform> program JSON/search endpoints:

```text
program: <program-name>
handle: <program-redacted>
submission_state: open
offers_bounties: true
resolved_report_count: 231
last_policy_change_at: 2025-10-14T23:46:27.082Z
program_url: https://<bug-bounty-platform>.com/<program-redacted>
```

Relevant policy facts captured from public policy text:

- Only test accounts you own or accounts you have permission from the owner to test.
- Do not disclose vulnerability information outside the <bug-bounty-platform> report without written authorization.
- Do not store/transfer/retain sensitive or private data except as needed to report the finding.
- Do not disrupt/degrade <program-name> service.
- Do not download/modify customer data or interact with <program-name> customers; policy example explicitly calls out posting comments/messages in customer accounts.
- Do not test websites out of scope or not listed in assets.
- Signup route in policy: `https://<program-domain>/signup?affiliate=partners`.
- Account naming requirement: company name must include `[Bug Bounty] SomeCompanyName`.
- Email requirement: use <bug-bounty-platform> `@researcher-alias.example` alias email.
- API docs: `https://dev.frontapp.com/`.
- Policy interest/severity examples include cross-company full message/discussion disclosure, cross-company sensitive data disclosure, and low-privilege users executing/viewing admin-only API/data.
- Important nuance: within-company teammate visibility and some API-returned non-sensitive data may be expected behavior; do not overclaim those.

Important unresolved scope fact:

- The public unauthenticated JSON did not expose the program's full structured asset table. The endpoint `https://<bug-bounty-platform>.com/<program-redacted>/assets` returned `401`, so the exact in-scope asset list must be confirmed from the operator's logged-in <bug-bounty-platform> view before any <program-name> target request or `config/scope.txt` change.

## Candidate comparison

| Program | Fit | Reason to select / defer |
|---|---:|---|
| `<program-redacted>` | highest | Best immediate blend: bounty, open submissions, explicit signup path, workspace/customer-ops/team/API shape, cross-tenant interest. Needs logged-in asset table confirmation first. |
| `frontegg` | high backup | Excellent auth/tenant/role fit and exact domains in policy (`portal.au.frontegg.com`, `api.au.frontegg.com`), but identity platform risk is higher; better as second target after <program-name> process proves itself. |
| `hex` | high technical fit, deferred | Strong focus areas: cross-workspace leaks and AuthN/AuthZ across web/API/CLI/MCP/AI. But policy says do not test production and to email for bug bounty instance; public JSON shows `offers_bounties=false`. This is not ideal for immediate first run. |
| `airtable` | viable later | Staging-only, rich workspace/share/API surface, but enterprise features require a request path and the program is mature. Not the cleanest first run. |
| `discourse` | viable but not first | Exact target `try.discourse.org` and open-source review are good, but temporary bounty suspension and public/community content/spam risk make it less ideal for this specific first new-process live run. |

## Tactical preview — expanded options before narrowing

Product/permission model sketch:

```text
Actors: company owner/admin, workspace admin, teammate / lower-privilege user, possibly API token/session user
Tenants/workspaces/orgs: company + workspaces/inboxes/teams
Objects/resources: conversations/messages/discussions, inboxes, tags/topics, teammates, API resources, admin settings
Public/private/share boundaries: mainly company/workspace/team/admin vs lower-privilege boundaries; avoid customer-facing message sends
API/UI parity surfaces: admin actions and visibility through UI vs <program-name> API
Lifecycle transitions: invite, role change, workspace membership, conversation/message/discussion ownership, tag/topic manipulation
Sensitive/later-only surfaces: real customer messages, outbound email/message sending, integrations/plugins, support/customer interaction, credential reports, disruptive tests
```

| Lane idea | Why <program-name> might fail here | Required controls | Risk class | Status | What would unlock it |
|---|---|---|---|---|---|
| Role/permission confusion on non-sensitive admin data/action | Policy explicitly discusses low-privilege user viewing/executing admin-only data/actions through API | Account A owner/admin + Account B lower-privilege teammate; benign setting/object; no customer data | A2/A3 | best candidate after scope/account gate | Logged-in H1 asset confirmation, Account A/B, safe company/workspace with no real customer data |
| Tenant/company isolation | Program is especially interested in cross-company/cross-tenant data disclosure | Two owned companies/tenants or clean negative control; only synthetic data | A3 | later after A/B or tenant B | Ability to create two owned companies without violating signup/account rules |
| UI/API permission mismatch | API docs exist and policy discusses expected/non-sensitive API data | Lower role UI denied + direct API denied/allowed comparison; no token retention in artifacts | A2/A3 | strong second lane | Official API access with owned account and redaction plan |
| Invite lifecycle / role downgrade stale permissions | Team/customer-ops platforms often have invite/member state transitions | Owned invite to Account B, role downgrade/revoke, no spam/third-party invite | A2/A3 | later-only until Account B exists | Account B and explicit low-speed invite test plan |
| Message/discussion disclosure | Policy severity table includes message/discussion disclosure | Synthetic messages only; no customer accounts/data; no outbound sends | A3/A4 | later-only/high caution | Safe synthetic mailbox/object model and strict no-customer/no-send plan |
| Integration/plugin/topic boundary | Policy mentions plugins/topics; customer-ops products often integrate with external systems | Owned test integration only, no external callback/customer impact | A4 | blocked for first run | Separate A4 plan and explicit policy/operator approval |

## Selected first lane, if operator confirms scope/assets

```text
selected_lane: role/permission confusion or API/UI permission mismatch on a non-sensitive, owned company/workspace object
authorization basis: <bug-bounty-platform> `<program-redacted>` policy + exact logged-in asset table still pending
why selected: high evidence/control ratio; matches policy interest; avoids payment/order/KYC/customer-data; maps directly to completed local auth/session role-separation proof patterns
request budget: initial A2 viability only, manual/noVNC, low-speed, max 20-30 minutes
required accounts: Account A owner/admin; Account B lower-privilege teammate if creation/invite is policy-safe
object/resource needed: harmless synthetic workspace/company object or non-sensitive admin-only object; no real customer messages
positive control: Account A can view/perform intended admin/non-sensitive action
negative control: Account B lower role cannot view/perform it through UI and API
normal provenance: object IDs/paths only from own UI/API responses, not guessed
redaction: Account A/B labels only; redact alias, company name if identifying, tokens, cookies, message content, IDs if sensitive
stop conditions: any customer data, outbound message/customer interaction, CAPTCHA/OTP/email/phone gate, account warning, rate limit, asset-scope ambiguity, need for API key/secret retention, integration/callback/workflow requirement, or candidate approaching report-ready
candidate threshold: lower-role or cross-company access appears inconsistent but evidence/control incomplete
report_ready threshold: exact in-scope asset, allowed class, reproducible A/B controls, no third-party data, meaningful impact, redacted evidence, independent review
```

## Operator gate before any target-touching

<program-name> is selected, but not yet authorized in repo scope.

Required operator/local steps:

1. In logged-in <bug-bounty-platform>, open `https://<bug-bounty-platform>.com/<program-redacted>` and confirm the structured asset table / in-scope assets visible to your account.
2. Confirm whether the signup URL and resulting app host(s) are listed in assets or otherwise covered by the program's scope.
3. Confirm you have access to a <bug-bounty-platform> `@researcher-alias.example` alias and can create the account locally in Kali/noVNC if needed.
4. Do not paste alias, password, OTP, cookies, tokens, verification links, phone number, or raw PII into chat/repo.

Safe reply phrases:

```text
<program-name> assets confirmed
<program-name> assets not visible
<program-name> signup in scope
<program-name> signup not in scope
<program-name> alias ready
blocked_auth
blocked_email_verification
blocked_policy
stop
```

## Next safe action

If the operator confirms exact <program-name> assets and signup scope, create `programs/<program-redacted>/scope.json`, ask for explicit confirmation before adding the minimal exact host(s) to `config/scope.txt`, run the dry-run gate pair, then prepare a <program-name> A2 viability packet using the tactical preview template.

Until then: no <program-name> app navigation, no signup, no `config/scope.txt` changes, and no target-touching automation.
