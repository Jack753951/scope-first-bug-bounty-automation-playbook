> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# <program-slug> Owned-Account Surface Mapping Run Card — 2026-05-29

Boundary: Operator approved exact <program-slug> scope entries and approved owned-account signup/login/surface mapping on 2026-05-29 via `approve <program-slug> exact scope: us.identity.<program-redacted>.com, app.<program-redacted>, cloud.<program-redacted>.com` followed by `都做`. This run card does not authorize vulnerability exploitation, scanners/fuzzers/DAST, SSRF/OAST/callbacks, API-token/OAuth app/webhook/integration creation, customer/non-owned data access, destructive actions, or report submission.

## Program

- Program: <program-slug>
- Platform: <bug-bounty-platform>
- Scope file: `programs/<program-slug>/scope.json`
- Global scope: `config/scope.txt`
- Lane: `programs/<program-slug>/lane_state.json`

## Approved exact hosts

```text
cloud.<program-redacted>.com
app.<program-redacted>
us.identity.<program-redacted>.com
```

Explicitly not approved:

```text
*.api.<program-redacted>.com
*.<program-redacted>.com
*.edge.gateways.<program-redacted>.com
*.kongcloud.io
kuma.io
```

## Decision

Decision: EXECUTE bounded surface mapping only.

## Lab-derived bundle

Lab-derived bundle: `auth-role-separation` / `object-ownership-idor` / `api-ui-permission-mismatch` readiness mapping only.

Transferred controls:
- Identify whether Account A / Account B, low-priv role, invite, workspace/org, owned object, and direct API/UI routes are available.
- Do not test authorization bypass yet.

Transferred evidence pattern:
- Sanitized visible page text.
- Local screenshots only if they contain no secrets/customer data.
- Surface matrix and gate list.

Live restrictions applied:
- Browser/manual/noVNC low-speed only.
- Exact approved hosts only.
- Stop at OTP/CAPTCHA/email verification/password/passkey gate if no secret-safe env-backed fill path is available.
- Stop before API token creation/storage, OAuth app setup, webhook/integration/channel creation, payment/KYC, scanner/fuzzer/DAST, SSRF/OAST/callbacks, non-owned data, and final report submission.

## Report title if true later

Not testing yet. Candidate titles after mapping may include:

- Low-priv <program-slug> Konnect user can access admin-only organization settings via direct URL/API.
- Removed <program-slug> organization member retains access to owned workspace or service metadata.
- Insomnia workspace role boundary allows unauthorized read/write of owned collections/projects.
- <program-slug> identity/OIDC flow exposes unsafe redirect/session-boundary behavior using owned accounts only.

## Positive controls needed

- Account A can reach dashboard/workspace/org surface.
- Account A can create or view owned object labels only, if creation is low-risk and separately permitted.
- Admin/owner role action is visible but not necessarily executed.

## Negative controls needed before proof lane

- Account B low-priv, removed, downgraded, or never-invited state.
- Separate workspace/organization when needed.
- Unauthenticated user only for public/login checks.

No clean negative control means no access-control claim.

## Allowed now

- Open approved exact hosts in Kali/noVNC.
- Capture sanitized visible text, gate flags, screenshots, page titles/URLs.
- Identify signup/login paths and product surfaces.
- Fill non-secret email/username fields only when safe; use env-backed secret bridge for stored password/phone only if already approved and tool path does not print secrets.
- Continue until verification email/code, CAPTCHA, OTP, password/passkey secret gate, or other hard gate appears.

## Blocked now

- Broad crawling, scanners, fuzzers, DAST, directory bruteforce.
- API-token, OAuth app, webhook, integration, SCIM/SAML configuration, billing/payment/KYC.
- Customer/non-owned/internal data.
- Sensitive token/cookie/localStorage capture.
- Any bypass/exploit proof or role/IDOR test before a separate bounded proof run card.
- Final report submission.

## Time box

30–45 minutes for first-contact surface mapping.

## Kill/Park criteria

- Only SSO/company identity login and no self-serve owned account route.
- Immediate OTP/CAPTCHA/phone/payment/KYC gate before useful surface appears.
- No Account A/B or owned object/control path.
- Any customer/non-owned data would be needed.
- Product surface maps to no practiced bundle.

## Evidence output

Write compact outputs under:

```text
programs/<program-slug>/notes/surface_map_20260529.md
<artifact-output-dir>/browser_state/<profile>_<timestamp>/
```

Do not promote runtime screenshots to repo unless reviewed/redacted.
