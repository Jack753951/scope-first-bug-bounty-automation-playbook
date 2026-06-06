> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# <program-slug> run card

Status: EXECUTE_PRECONDITION_REVIEW
Source: <bug-bounty-platform> `syfe_bbp` opportunity claimed/opened from Opportunity Discovery.
URL: https://<bug-bounty-platform>.com/syfe_bbp

## Account-impact decision

Operator approved `claim <program-slug>` and asked whether claiming has negative account impact.

Assessment:
- No direct negative account/reputation impact was visible from the H1 UI beyond consuming the private-opportunity cadence/slot (`up to 1 per 30 days`).
- Treat future H1 private-opportunity claims as pre-authorized when the only known cost is slot/cadence and there is no apparent account-risk warning.
- Still stop and ask before auth/OTP/CAPTCHA/phone/payment/KYC/OAuth/integration/API-token/final-submit or any unclear account-risk action.

## Program signals

- Program: <program-slug>
- Program type: Bug Bounty Program
- Highlights: Gold Standard Safe Harbor, Platform Standards, Managed by <bug-bounty-platform>, Collaboration Enabled, Retesting
- Response metrics visible:
  - Average time to first response: 1 day, 15 hours
  - Average time to triage: 2 days, 9 hours
  - Average time to bounty: 2 weeks, 1 day
  - Average time from submission to bounty: 2 weeks, 4 days
  - Average time to resolution: 3 months, 6 days
- Rewards visible:
  - Low: $50-$75
  - Medium: $150-$250
  - High: $500-$750
  - Critical: $1,000-$1,500
- Stats visible:
  - Response efficiency: 88%
  - Reports received in 90 days: 870
  - Reports resolved: 21
  - Assets in scope: 9

## Scope summary

All listed assets are in scope, bounty eligible, max severity Critical:

1. `www.<program-slug>.com`
   - Main domain.
   - Production signup must use only `@researcher-alias.example` address.
   - Signup URL: `https://www.<program-slug>.com/create-account?utm_source=bug_bounty&medium=bug_bounty`
2. `uat-bugbounty.nonprod.<program-slug>.com`
   - Primary test environment.
   - Provided credentials only valid for this environment.
   - Findings on test env need to be reproducible on production to be eligible.
3. `mark8.<program-slug>.com`
   - Market data API service.
4. iOS App Store: `https://apps.apple.com/sg/app/<program-slug>-stay-invested/id1497156434`
5. Android Play Store: `com.<program-slug>`
6. `api.<program-slug>.com`
   - User services API.
7. `api-uat-bugbounty.nonprod.<program-slug>.com`
   - Test environment API.
8. `alfred.<program-slug>.com`
   - Trading service APIs.
9. `alfred-uat-31.nonprod.<program-slug>.com`
   - Trading UAT endpoint; APK provided on H1 page.
   - Static-analysis findings must be validated against latest production build.

## Program rules / hard stops

Allowed baseline:
- Provide detailed reproducible reports.
- Submit one vulnerability per report unless chaining is needed.
- Only interact with owned accounts or accounts with explicit permission.
- Production requests should include `X-<bug-bounty-platform>-Research: [H1 username]`.

Hard stops / disallowed:
- Social engineering.
- Privacy violations, data destruction, service interruption/degradation.
- DoS against infrastructure or user accounts.
- Brute force or automated attack techniques on production.
- Any modification/destruction of user data.
- Support-team spam.
- Unscoped subdomain vulnerability submission without asking program team.
- Customer/non-owned data.

Non-qualifying / low-priority per policy:
- Third-party-hosted sites unless impact reaches <program-slug> main app.
- SSL/TLS/email best practices only.
- Outdated browser-only bugs.
- UAT information disclosure.
- Known vulnerable libraries without working PoC.
- Open redirect without additional impact.
- Promo-code URL/archive/enumeration issues.
- Root/jailbreak/SSL-pinning bypass alone.
- Credential leakage informational if 2FA is in place.
- Rate-limit/brute-force unless ATO or financial damage.
- Self-XSS/file-upload XSS.
- Editing own account details for non-KYC verified accounts.
- UI-only response manipulation with no real access impact.
- CORS unless data exfiltration.
- Debug View/login into any UAT account.
- Exposed API keys without PoC.
- Pasting auth token from another account to access details.

## First-bounty scoring

freshness: 2/3
self_signup: 2/2
free_plan: unknown 1/2
low_priv_control: unknown 1/3
owned_object: unknown 1/3
scope_clarity: 2/2
operator_cost_low: 2/3 initially; may drop if signup/phone/KYC appears
access_control_surface: 2/3
api_or_direct_url_surface: 2/2
Total: 15/23 provisional

Decision: EXECUTE precondition review, then continue only if signup/control setup remains low-cost.

## Candidate bundle

Primary bundle: `object-ownership-idor` or `api-ui-permission-mismatch` on owned accounts/objects.
Secondary bundle: `auth-role-separation` only if the product exposes safe team/role controls without payment/KYC/high operator cost.

Report title if true:
- User can access another owned test account's <program-slug> object/API resource by ID.
- API allows access to a portfolio/trading/account resource that UI/account controls deny.

## Precondition checklist

Positive control:
- Owned Account A can create/read an owned object/resource.

Negative control:
- Owned Account B, unauthenticated user, removed/downgraded teammate, or different workspace/account cannot access Account A's object.

Owned object/resource:
- Unknown until signup/test environment credential path is checked.

Expected matrix:
- A -> A resource: allow.
- B/unauth/removed -> A resource: deny, no metadata/content leak.
- UI-denied action -> API-denied action: deny.

Operator cost:
- Current: 1 (private opportunity claim approved and done/opened).
- Stop if auth/OTP/CAPTCHA/phone/payment/KYC or provided credential claim requires human action.

Kill criteria:
- Signup immediately requires phone/KYC/payment.
- No owned object/resource can be created safely.
- No clean negative control.
- Proof requires customer/non-owned data.
- Only UAT info disclosure or policy-listed non-qualifying behavior is found.
- Any proof would require brute force, DoS, support spam, social engineering, or production automation.

Evidence required if candidate emerges:
- Scope reference.
- Owned-account labels only.
- Request/response snippets with secrets/tokens/cookies redacted.
- Role/object matrix.
- Header usage confirmation for production requests.
- Expected-vs-observed mismatch.
- Cleanup/no-customer-data statement.
- Final operator approval before report submission.

## Next actions

1. Review H1 policy/scope again before touching target.
2. Attempt only low-speed first-contact/signup discovery.
3. Prefer UAT credential/test-env path if accessible without human gate; otherwise production signup with `@researcher-alias.example` only after operator-auth gate.
4. Build or update `programs/<program-slug>/evidence_index.json` once a concrete owned object/control exists.
5. PARK immediately if operator cost rises before a strong bundle precondition is visible.
