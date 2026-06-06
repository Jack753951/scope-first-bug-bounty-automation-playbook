> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Freshness-First Bounty Candidates — 2026-05-28

Status: active candidate intake
Boundary: public metadata / policy-source intake only. No target contact, no scan, no fuzz, no exploit, no OAST/callback, no account mutation, no credential handling, no report submission.

## Strategy

Operator confirmed the two highest-value zones:

1. Latest vulnerabilities.
2. Latest targets.

Highest priority is the intersection:

```text
fresh vulnerability × fresh/under-tested/scoped bounty target -> first-bounty candidate
```

If no intersection is ready, keep two parallel lanes:

- `fresh_vuln_lane`: newest advisory/PoC/patch diff -> local proof/passive detector -> scoped match.
- `fresh_target_lane`: newest/high-fit program -> access-control/business-logic bundle -> owned-control proof.

## Sources checked this pass

Fetched public metadata only at 2026-05-28 UTC:

- CISA KEV JSON feed.
- NVD CVE 2.0 recent critical CVEs, filtered for web/API/auth/access/RCE-ish descriptions.
- GitHub Security Advisories public API, critical severity, latest published.
- Intigriti public programs page.
- <bug-bounty-platform> public directory landing page only; logged-in target selection still requires operator/noVNC UI or safer authenticated export.

## Fresh-vulnerability shortlist

These are NOT approved for live testing. They are candidate themes for local proof/passive matching and policy-gated target matching.

| Rank | Candidate | Why now | Bounty relevance | Safe first action | Decision |
|---|---|---|---|---|---|
| 1 | Dify auth/tenant/trace/path traversal cluster: `<specific-cve-id>`, `<specific-cve-id>` | NVD recent 2026-05-18; descriptions mention free self-registration and tenant/app boundary issues. | Strong fit for SaaS multi-tenant access-control bundle; source-available/product-model friendly. | Local/source review only; build expected-vs-observed bundle notes. Search only for programs that explicitly include their own Dify deployment or AI app platform scope. | EXECUTE_LOCAL_RESEARCH |
| 2 | Langflow / IBM Langflow RCE/origin validation: `<specific-cve-id>`, `<specific-cve-id>` | CISA KEV added 2026-05-21; GHSA/NVD recent mentions Langflow OSS. | Fresh exploited AI-app surface; may match targets exposing self-hosted AI workflow tools. | Passive/source/local proof only; do not exploit live. Look for in-scope target tech match by policy-approved passive means. | PASSIVE_ONLY |
| 3 | LiteLLM SQL injection: `<specific-cve-id>` | CISA KEV added 2026-05-08; AI proxy credential-management impact. | High impact if scoped, but live proof risks credentials/secrets; likely reportable only with owned lab or explicit target scope. | Local proof and passive target matching only; live data access is hard stop. | PASSIVE_ONLY |
| 4 | Traefik Gateway API tenant/internal REST exposure: `<specific-cve-id>` | NVD recent 2026-05-15; multi-tenant route/provider boundary. | Good conceptual bridge to tenant isolation and API/UI mismatch; likely useful as proof-bundle inspiration. | Local/Kubernetes lab rehearsal only; live requires explicit infrastructure scope and permission. | LOCAL_LAB_REFERENCE |
| 5 | Open WebUI file upload path traversal: `<specific-cve-id>` | NVD recent 2026-05-15; source-available AI product; authenticated upload/path issue. | Good safe-marker upload/path traversal bundle if a bounty target explicitly scopes Open WebUI or owned instance. | Local safe-marker proof; live only with explicit target/product scope and owned object. | EXECUTE_LOCAL_RESEARCH |
| 6 | LiquidJS RCE: `<specific-cve-id>` | GHSA critical published 2026-05-27. | Template engines can appear in SaaS, but live proof likely unsafe without source/owned template context. | Source/patch diff; find source-available bounty targets using LiquidJS. | RESEARCH_ONLY |

## Fresh-target shortlist from Intigriti public page

These require logged-in policy review before any testing. Do not execute target actions from this table alone.

| Rank | Program/source | Public signal | First-bounty fit hypothesis | Friction/risk | Next safe action | Decision |
|---|---|---|---|---|---|---|
| 1 | <program-redacted> Public Bug Bounty | Intigriti public program listing; SaaS/search/API company. | Strong API/search/indexing/product-surface potential; likely docs/API surface; possible access-control or metadata leak lanes. | Need logged-in program policy, bounty status, scope, and signup feasibility. | Open policy in logged-in Intigriti; score for self-signup, API docs, owned org/object, access-control acceptance. | EXECUTE_POLICY_REVIEW |
| 2 | <program-redacted>.be Dedicated Bug Bounty Program | Intigriti public program listing; dedicated BBP. | Dedicated program may be less crowded than huge public targets; HR/account/job flows can have access-control/business-logic issues. | HR data/customer-data boundary likely sensitive; must avoid non-owned data. | Read scope/rewards; look for owned account/profile/application flows only. | POLICY_REVIEW |
| 3 | AS Watson retail programs: Kruidvat / Superdrug / Watsons / ICI PARIS XL / Marionnaud / The Perfume Shop | Multiple Intigriti public listings under same group. | E-commerce/account/order/loyalty surfaces; possible business logic/access-control if own accounts only. | Payment/order/customer-data friction; many findings may be excluded. | Policy review only; prefer account/profile/loyalty non-purchase flows if bounty policy allows. | POLICY_REVIEW |
| 4 | Intigriti Challenge 0526 | Very fresh by name/date. | Freshness is high; may be challenge not bounty. Useful for skill/rehearsal, not necessarily paid bounty. | May not count toward first paid bounty. | Check if reward-bearing; otherwise keep as practice/reference only. | PARK_FOR_BOUNTY |
| 5 | Grafana Labs VDP / Anaconda VDP / Toast VDP | Public listings but VDP-labeled. | Source/API-rich and useful for learning/source review. | VDP likely no bounty; not first-bounty primary. | Park for paid-bounty goal unless policy shows rewards. | PARK |

## Intersection candidates

| Rank | Intersection | Why it matters | Immediate safe step | Blockers |
|---|---|---|---|---|
| 1 | AI/devtool fresh vulns (`Dify`, `Langflow`, `LiteLLM`, `Open WebUI`, `LiquidJS`) × source/API-rich bounty targets | This is where AI-source reasoning and first-bounty freshness can compound. | In H1/Intigriti UI, search for programs with AI, LLM, developer-tool, workflow, search, docs/API/source exposure. Do policy review only. | Need program-level scope and no live exploit. |
| 2 | <program-redacted> public BBP × API/search metadata leak / access-control bundle | Fresh target source from Intigriti with likely API/search object model; aligns with metadata-only leak and API/UI mismatch. | Read logged-in policy, identify allowed assets and whether self-serve account/API docs exist. | Need account setup and policy confirmation. |
| 3 | <program-redacted> dedicated BBP × account/profile/job application business logic | Dedicated program plus common workflow objects can yield access-control/business-logic bugs. | Policy review and owned-account-only surface map. | HR/customer/personal data hard stop; may need careful redaction. |

## Current top recommendation

Do not expand detectors yet. Use noVNC/logged-in UI to do policy review for the top fresh targets:

1. Intigriti: <program-redacted> Public Bug Bounty.
2. Intigriti: <program-redacted>.be Dedicated Bug Bounty Program.
3. <bug-bounty-platform>: latest/newly updated or private opportunities visible in logged-in UI, especially AI/devtool/API-rich SaaS.

For each, fill only:

```text
program:
platform:
public/private:
bounty_or_vdp:
recently_launched_or_updated:
scope_assets:
out_of_scope:
self_signup:
free_plan:
team/workspace/role:
owned_object:
api/docs/source:
operator_cost:
likely_bundle:
policy_allows_access_control:
policy_allows_low_rate_automation:
stop_before:
decision:
```

## Next operator-facing action

In Kali/noVNC, with <bug-bounty-platform> and Intigriti logged in, open policy pages for:

- <program-redacted> Public Bug Bounty on Intigriti.
- <program-redacted>.be Dedicated Bug Bounty Program on Intigriti.
- <bug-bounty-platform> newest/private/high-fit SaaS opportunity visible to the account.

Do not test. Only read program policy/scope and report the candidate names/URLs or let Hermes capture a redacted policy summary.
