> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# <program-redacted> sandbox dashboard surface map

Status: dashboard reached after operator completed email/contact onboarding.
Date: 2026-05-29

Boundary:
- Sandbox-only H1 lane.
- In-scope sandbox hosts only: manage-sandbox, api-sandbox, pay-sandbox, payer-details-sandbox, oauth-sandbox, connect-sandbox.
- No scanners/fuzzers/DAST, no token/cookie/API-key storage, no API-token creation, no OAuth/integration/webhook setup, no real bank/payment/KYC/customer data, no final submission.

Observed owned-account dashboard surfaces via sanitized CDP visible text:
- Home: Payments, Customers, Success+, Protect+, Developers, Create payment, Settings.
- Team: current Account A is Admin; controls include Enforce 2FA, Invite a team member, Team search, Export.
- Developers/API settings: Access token, Publishable access token, Public token, Webhook endpoint, Send test webhook. These are mapped only and remain operator-gated / not activated.
- Customers: empty state, counts 0 active/inactive/pending; invite-customer route exists; page recommends adding yourself as customer for testing.
- Subscription templates: empty/list surface; create route exposes subscription/template flow and customer-facing preview; avoid payment/bank/customer-data activation.

Bundle decision:
- Primary candidate: invite-membership-lifecycle + auth-role-separation.
- Report-title shape if true: low-priv/removed/pending owned teammate can access admin-only team/security/settings surfaces or export metadata after expected denial.
- Positive control: Account A admin can view Team/settings/admin surfaces.
- Negative control required: owned Account B as pending/low-priv/removed/downgraded team member.
- Decision: PARK/OPERATOR_GATE until explicit approval for Account B invite/member lifecycle setup.

Secondary candidates:
- api-ui-permission-mismatch: follow-on only with Account B; manual direct URL checks to already-seen pages, no token/header extraction.
- object-ownership-idor: parked; no safe non-payment owned object yet. Subscription template may be revisited only if metadata-only and non-activating.
- metadata-only-leak: parked until Account B exists.
- upload-path-traversal-safe-marker: killed for this surface; no upload surface observed.

Next required operator decision:
- Approve or decline creating/inviting an owned Account B for the sandbox team-role lifecycle proof.
