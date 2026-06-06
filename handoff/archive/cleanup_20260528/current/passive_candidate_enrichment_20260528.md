> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Passive Candidate Enrichment — 2026-05-28

Status: active passive enrichment
Boundary: public metadata and documentation reading only. No target testing, no scanning, no fuzzing, no exploit, no OAST/callback, no login/session scraping, no credential handling, no account mutation, no report submission.

## Operator instruction

Operator requested that Hermes continue collecting information autonomously until operator action is genuinely needed.

Execution rule:

- Hermes may collect public metadata, public program preview pages, documentation, public advisories, and source/public docs.
- Hermes must stop and ask for operator action for CAPTCHA/OTP/2FA, non-public logged-in program policy that cannot be safely fetched, safe phrase, account creation/mutation, target testing, or final submission.

## Candidate 1 — <program-redacted> Public Bug Bounty

Source checked:

- `https://app.intigriti.com/programs/<program-redacted>/coveopublicbugbounty/preview/detail`
- `https://docs.<program-redacted>.com/`
- `https://docs.<program-redacted>.com/llms.txt`
- `https://docs.<program-redacted>.com/en/llms/sections/manage-an-organization.txt`
- `https://docs.<program-redacted>.com/en/llms/sections/index-content.txt`
- `https://docs.<program-redacted>.com/en/llms/sections/security.txt`
- `https://docs.<program-redacted>.com/en/llms/sections/build-a-search-ui.txt`

Public preview facts captured:

- Program title: `<program-redacted> Public Bug Bounty - Bug Bounty Program - Intigriti`.
- Public preview exposes bounty range text: Tier 2 `$100 - $5,500`.
- Public preview text says <program-redacted> has a lot of attack surface and eligible reports can be rewarded when scope is reviewed carefully.
- Program specifics visible publicly: two-factor authentication required.
- Full submission/application requires valid Intigriti account.

Public docs facts captured:

- <program-redacted> documentation exposes large API/developer surface:
  - Commerce API.
  - Customer Service API.
  - Field API.
  - Push API.
  - Search API.
  - Source API.
  - Usage Analytics Write API.
  - Atomic / Headless / CLI / REST API docs.
- Documentation has sections for organization management, members, groups, API keys, security, compliance, entitlements, indexing content, sources, fields, mappings, permissions, query pipelines, and analytics.
- `Manage an Organization` docs explicitly index pages for members/groups, member management, privilege management, granting privileges, privilege reference, SAML SSO, API keys, programmatic API-key management, access-token privilege inspection, organization activity, resource snapshots, temporary access, organization endpoints, notifications, and deployment regions.
- `Index Content` docs explicitly index connectors/sources, fields/mappings, permission models, secured search, security identities, group/granted security identities, permission sets/levels, Push API, item management, security identity management, REST API source, SharePoint/Box/Confluence/Dropbox/Google Drive/Salesforce/Zendesk/ServiceNow-style connectors, and crawling-account permissions.
- `Build a Search UI` docs expose Atomic, Headless, hosted search page, JavaScript framework, and analytics tracking surfaces.
- Public docs explicitly mention secure/unified workplace search returning only data users can see in repositories for which they have permissions.

Attacker hypothesis, bounded:

- Strong candidate for access-control/API-permission research because product model appears to involve organizations, sources, indexes, permissions, API keys, and search visibility.
- Strongest bounded hypotheses to validate only after policy/account gate:
  - Organization member privilege mismatch: UI blocks an action but API accepts it for low-privileged member.
  - Search result authorization mismatch: indexed secured content metadata or result counts leak across permissions without content access.
  - Source/connector ownership mismatch: user can enumerate, edit, or trigger operations on sources/connectors outside assigned privileges.
  - API-key privilege confusion: token/API-key privilege inspection or scoped key behavior differs from documented/admin UI expectations.
  - Usage Analytics Write API abuse: low-privileged or client-side context can write misleading analytics/events across organization or source boundaries.
  - Temporary access / resource snapshot / notification subscription edge cases: stale or overbroad access after role/member changes.
- Good bundle fits:
  - `api-ui-permission-mismatch`.
  - `metadata-only-leak`.
  - `object-ownership-idor`.
  - `auth-role-separation`.
  - `tenant/search-result-visibility`.

Current score estimate before logged-in policy review:

| Field | Value |
|---|---|
| platform | Intigriti |
| program | <program-redacted> Public Bug Bounty |
| bounty_or_vdp | bounty preview, Tier 2 `$100-$5,500` visible |
| fresh_target_signal | public BBP discovered in current intake; freshness unknown until logged-in policy page confirms date/update |
| source/API/docs | strong |
| self_signup/free_plan | unknown |
| team/workspace/role | likely, but unconfirmed |
| owned_object | likely possible if account/trial exists, unconfirmed |
| operator_cost | unknown; probably account/trial dependent |
| policy_allows_access_control | unknown until logged-in policy review |
| policy_allows_low_rate_automation | unknown until logged-in policy review |
| provisional decision | `POLICY_REVIEW_REQUIRED`, high priority |

Blocker requiring operator or logged-in UI:

- Need logged-in Intigriti policy details: exact in-scope assets, out-of-scope exclusions, allowed testing methods, automation/rate limits, reward table, self-signup/trial rules, and report exclusions.

## Candidate 2 — <program-redacted>.be Dedicated Bug Bounty Program

Sources checked:

- `https://app.intigriti.com/programs/<program-redacted>/randstadbededicatedbugbountyprogram/preview/detail`
- `https://www.<program-redacted>.be/`
- `https://www.<program-redacted>.be/veiligheidsprobleem-melden/`

Public preview facts captured:

- Program title: `<program-redacted>.be Dedicated Bug Bounty Program - Bug Bounty Program - Intigriti`.
- Public preview page exists and requires login/sign-up for full participation details.
- Public preview did not expose clear bounty range in the snippets captured.

Public <program-redacted> security/disclosure page facts captured:

- <program-redacted> says system security is a top priority and asks researchers to report vulnerabilities.
- <program-redacted> asks researchers not to increase the vulnerability/problem by downloading more data than needed to demonstrate it or by deleting/modifying personal data.
- <program-redacted> forbids/asks not to use physical attacks, social engineering, distributed denial-of-service, spam, or third-party applications.
- <program-redacted> asks for sufficient reproduction information such as affected IP address/URL and description.
- <program-redacted> promises a response within 7 working days with evaluation and expected solution date.
- If instructions are followed, <program-redacted> says it will not take legal steps related to the report.
- <program-redacted> may mention the reporter name unless the reporter requests otherwise.

Attacker hypothesis, bounded:

- Product surfaces include job search, my <program-redacted> login/register, saved jobs, candidate profile, employer flows, job applications, complaint/contact flows, and possible document/profile data.
- Good bundle fits only if logged-in program policy and owned-account flow allow them:
  - `object-ownership-idor` on saved jobs/profile/application objects.
  - `api-ui-permission-mismatch` around candidate/employer flows.
  - `metadata-only-leak` if only owned/controlled data is exposed.
  - `business-logic` around application/profile state.

Risk notes:

- HR/personal data is highly sensitive. Any evidence must avoid non-owned applicant/customer/employer data.
- If this remains VDP-like despite Intigriti BBP title, it may not serve first paid bounty.

Current score estimate before logged-in policy review:

| Field | Value |
|---|---|
| platform | Intigriti |
| program | <program-redacted>.be Dedicated Bug Bounty Program |
| bounty_or_vdp | Intigriti title says BBP; reward details unknown |
| fresh_target_signal | discovered in current intake; freshness unknown |
| source/API/docs | moderate public surface; docs/API unknown |
| self_signup/free_plan | candidate profile registration exists publicly; employer flow may differ |
| team/workspace/role | unclear |
| owned_object | likely candidate profile/saved jobs/application objects, unconfirmed |
| operator_cost | moderate; likely account/profile setup |
| policy_allows_access_control | unknown |
| policy_allows_low_rate_automation | unknown; public disclosure text warns against DDoS/spam/third-party apps |
| provisional decision | `POLICY_REVIEW_REQUIRED`, second priority |

Blocker requiring operator or logged-in UI:

- Need logged-in Intigriti policy details and reward eligibility. Public <program-redacted> disclosure page alone is not enough to select this as first paid-bounty lane.

## Latest vulnerability lane carry-forward

Keep these as source/local/passive-only research candidates until they intersect an in-scope program:

| Theme | Why keep | Safe next action |
|---|---|---|
| Dify auth/tenant/trace/path traversal cluster | Fresh NVD; AI app; tenant/access-control semantics fit first-bounty bundle. | Source/local proof notes only; search for programs explicitly scoping Dify/AI workflow products. |
| Langflow / IBM Langflow | CISA KEV / GHSA freshness; AI workflow; high impact. | Source/local/passive only. |
| LiteLLM SQLi | CISA KEV; credential-management impact. | Passive/source review only; live proof risks secrets. |
| Open WebUI path traversal | Source-available AI app; safe-marker local proof feasible. | Local proof only. |
| LiquidJS RCE | GHSA critical fresh; source/patch-diff friendly. | Patch/source review; only live if owned template context exists. |

## Current ranking

1. <program-redacted> Public Bug Bounty — highest first-bounty target candidate from this passive pass because it is a public BBP with strong API/docs/search/permission surface.
2. <program-redacted>.be Dedicated BBP — useful but sensitive; needs logged-in reward/scope review before spending operator time.
3. Dify/Langflow/LiteLLM/Open WebUI latest-vuln lane — high-value research stream, but not yet connected to a scoped bounty target.

## Next autonomous steps Hermes can do without operator

- Continue public/passive enrichment of <program-redacted> documentation around organization members, groups, API keys, sources, permissions, search tokens, analytics write API, and entitlement boundaries. Initial pass completed; next pass should focus only on the exact logged-in policy and account feasibility rather than more docs unless a specific hypothesis needs support.
- Continue public/passive search for H1/Intigriti programs with AI/devtool/API-rich surfaces.
- Prepare a <program-redacted> policy-review checklist for the operator/logged-in UI.

## Operator-needed blockers

- Logged-in Intigriti policy page for <program-redacted>.
- Logged-in Intigriti policy page for <program-redacted>.
- Any account creation, free trial, API key creation, organization setup, CAPTCHA/OTP, or test execution.
