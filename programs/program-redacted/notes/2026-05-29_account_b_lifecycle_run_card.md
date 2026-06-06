> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# <program-redacted> Account B lifecycle run card

Date: 2026-05-29
Decision: EXECUTE after operator authorization.

Program: <program-redacted> BBP
Scope: sandbox-only assets listed in `programs/<program-slug>/scope.json` and `config/scope.txt`.

Bundle: invite-membership-lifecycle + auth-role-separation, with API/UI mismatch follow-on.

Hypothesis:
- A low-privilege, pending, removed, or downgraded owned teammate may retain access to admin/team/security/settings surfaces or metadata that should be denied.

Report-title shapes if true:
- Low-privilege teammate can access admin-only team/security settings via direct URL.
- Removed or downgraded teammate retains access to organization/team metadata.
- UI denies an action but direct navigation/API-backed UI route still exposes/administers team state.

Positive control:
- Account A (admin) can access Team/settings/admin surfaces.

Negative control:
- Account B, operator-owned, invited/accepted/pending/removed/downgraded as applicable.

Owned object/resource:
- Sandbox organization/team membership only.

Allowed actions:
- Manual or wrapper-assisted browser actions on in-scope sandbox pages.
- Low-count, scope fail-closed script-assisted checks when they reduce noise or improve evidence.
- Send/use owned Account B team invite as explicitly authorized by operator.
- Direct URL checks to already-observed in-scope admin/team/settings pages using Account B.

Blocked actions / stop-before:
- Production assets.
- Customer/internal/non-owned data.
- Secrets, cookies, tokens, API keys, OTPs, passwords, phone numbers in artifacts.
- API token creation/storage, OAuth/integration/webhook setup, payment/bank/KYC unless separately approved.
- Destructive/resource-exhaustive/evasive/persistent behavior.
- Final report submission or report-ready promotion without operator approval.

Evidence required:
- Role/provenance matrix using labels only.
- Expected vs observed access results.
- Minimal redacted screenshots or sanitized visible-text snippets.
- Cleanup note: Account B role/removal state and no customer/internal data touched.

Time box: 45-60 minutes.


## Execution checkpoint — invite sent

- Account A admin opened Team -> Invite a team member.
- Account B was invited with Read-only permissions for the sandbox organization.
- The page confirmed: invitation sent to Account B, and Account B account permissions updated.
- No API tokens, OAuth, webhooks, payment/bank/KYC, customer data, or internal/non-owned data were touched.
- Current blocker: operator must complete Account B invitation acceptance / account setup from email. Hermes should resume after Account B can sign in, or if CAPTCHA/OTP/phone/payment/KYC/API-token/OAuth/integration appears.


## Checkpoint — Account B setup reported, Account A session still visible

- Operator reported clicking Account B verification email and setting a password.
- Current Kali/noVNC Chromium session still appears to be Account A admin: Team page marks Account A as `You` / Admin, and Account B is still shown as Invited / Read-only.
- No Account B negative-control checks have been executed yet.
- Next action requires Account B session in the browser, or a separate Account B browser profile, without exposing/storing the password.

## Checkpoint — Account B read-only negative controls

Timestamp: 2026-05-29T03:25:15Z

Session confirmation:
- Operator reported one Kali/noVNC browser window is signed in as Account B.
- User settings page rendered `User settings for Account B`, confirming the checked session is Account B without recording email/password/cookies/tokens.

Route checks performed with Account B / Read-only:

| Route | Expected | Observed |
|---|---|---|
| `/company/team` | Read-only should not administer team membership. | Redirect/rendered <program-redacted> 404; no team table or invite controls visible. |
| `/company/team/users/invite` | Read-only should not invite users. | Redirect/rendered <program-redacted> 404; no invite form visible. |
| `/company/settings` | Read-only should not administer company settings. | Redirect/rendered <program-redacted> 404. |
| `/settings` | User can manage own personal settings only. | Rendered Account B user settings/personal preferences, password and 2FA setup controls; no organization-admin controls observed on this page. |
| `/developers` | Needs role-boundary review because API/webhook surfaces are sensitive. | Rendered API settings and Events navigation. Page showed no existing webhook endpoints and a `Create a webhook endpoint` link. No webhook setup was opened or submitted due stop-before. |
| `/events?limit=25` | Read-only may be allowed to audit sandbox events, but exposure should be assessed. | Rendered events list containing sandbox creditor event rows with truncated IDs. No customer/internal/non-owned data observed. |

Assessment:
- Team/invite/company-settings direct URL checks are negative controls, not findings.
- Account B read-only access to `/developers` and `/events` is a candidate follow-on only. It is not yet report-ready because the lane stopped before webhook/API-token/integration setup and before any token/cookie/API-key handling.
- Next decision: ask operator whether to approve a strictly bounded webhook-creation-form inspection/submission-negative-control, or park this candidate and continue non-webhook owned-account role checks.

Stop-before maintained:
- No API token, OAuth, integration, webhook endpoint, payment/bank/KYC, customer data, credentials, cookies, OTPs, phone numbers, or non-owned data were stored or used.

## Checkpoint — Account B webhook route form-only negative control

Timestamp: 2026-05-29T03:25:15Z+follow-up

Operator approval:
- Operator approved only `webhook creation form inspection / negative-control`.
- Boundary: no submit, no endpoint creation, no external callback URL, no token/API-key handling.

Route checked:
- `/developers/webhook-endpoints?action=create`

Observed:
- Page rendered `Webhook endpoints` for Account B.
- Instead of a creation form, the page stated: `No webhook endpoints have been created yet` and `An admin on your account can create a webhook endpoint. You'll see it here once it's been added.`
- No URL field, secret/token field, or submit/create endpoint control was visible to Account B.

Assessment:
- This is a clean negative control: Account B read-only cannot open/create the webhook endpoint form via the direct `action=create` URL.
- Combined with Team/invite/company-settings 404s, the current invite-membership-lifecycle + webhook/admin role-boundary lane has no reportable finding from these checks.
- Decision: PARK/KILL this specific candidate as `no_finding_current_controls`; resume broader target search or a different <program-redacted> owned-account lane only if a new high-signal hypothesis appears.

Stop-before maintained:
- No webhook endpoint was created, no callback was provided, no submit action was taken, and no secrets/tokens/cookies were stored.
