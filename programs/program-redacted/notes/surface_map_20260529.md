> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# <program-slug> Surface Map — 2026-05-29

Boundary: Exact hosts approved by operator for owned-account signup/login/surface mapping. This note records first-contact visible state only. No exploit, scanner/fuzzer/DAST, API-token/OAuth app/webhook/integration creation, customer/non-owned data access, or report submission was performed.

Run card: `programs/<program-slug>/notes/run_card_20260529_owned_account_surface_mapping.md`
Scope file: `programs/<program-slug>/scope.json`

## Host observations

### `cloud.<program-redacted>.com`

- Opened URL: `https://cloud.<program-redacted>.com/`
- Redirected visible URL host: `signin.cloud.<program-redacted>.com` login flow
- Page title: `Login | Konnect`
- Visible state: Konnect sign-in page
- Visible options:
  - Continue with a passkey
  - Continue with Google
  - Continue with GitHub
  - Continue with Microsoft
  - Continue with SSO
  - Email address + Continue with Email
  - Sign Up link
- Gate flags from sanitized CDP extraction:
  - login: true
  - captcha: false
  - otp: false
  - phone: false
  - payment/KYC: false
- Screenshot local runtime path:
  - `<artifact-output-dir>/browser_state/<program-slug>-surface-map_20260529T162249Z.png`
- Decision: EXECUTE candidate for owned-account signup path next, but stop at verification/CAPTCHA/OTP/password/passkey/SSO/OAuth token gates.

### `app.<program-redacted>`

- Opened URL: `https://app.<program-redacted>/`
- Redirected visible URL: `https://app.<program-redacted>/app/authorize`
- Page title: `Insomnia`
- Visible state: Insomnia auth/start page
- Visible options:
  - Continue with Google
  - Continue with GitHub
  - Continue with Email
  - Continue with Enterprise SSO
- Terms/privacy links visible.
- Gate flags from sanitized CDP extraction:
  - login: true
  - captcha: false
  - otp: false
  - phone: false
  - payment/KYC: false
- Screenshot local runtime path:
  - `<artifact-output-dir>/browser_state/<program-slug>-surface-map_20260529T162311Z.png`
- Decision: EXECUTE candidate for email signup mapping if Konnect blocks or if Insomnia workspace role surfaces appear lower-friction.

### `us.identity.<program-redacted>.com`

- Opened URL: `https://us.identity.<program-redacted>.com/`
- Page title: empty
- Visible state: JSON 404 response
- Sanitized visible text says resource not found.
- Gate flags from sanitized CDP extraction:
  - login: false
  - captcha: false
  - otp: false
  - phone: false
  - payment/KYC: false
- Screenshot local runtime path:
  - `<artifact-output-dir>/browser_state/<program-slug>-surface-map_20260529T162334Z.png`
- Decision: PARK as direct browser route. Keep as identity/OIDC endpoint only if later routed through owned Konnect login flow; do not probe endpoints directly.

## Bundle fit after first contact

Preferred live lane remains `cloud.<program-redacted>.com` / Konnect:

- `auth-role-separation`: likely if org/team/member roles are available after signup.
- `invite-membership-lifecycle`: likely if invite/removal/downgrade flows are available.
- `object-ownership-idor`: likely if services/routes/plugins/certs/runtime groups or workspaces expose direct identifiers.
- `api-ui-permission-mismatch`: possible only after approved API/direct URL surfaces are visible; no API token creation yet.

Fallback lane:

- `app.<program-redacted>` if it exposes low-friction workspace/team/project/collection role surfaces.

Parked:

- `us.identity.<program-redacted>.com` direct route because root returns 404 and identity/OIDC testing risks token/session boundary without a later specific proof card.

## Next gate / next action

Next action inside current approval: attempt the ordinary email signup path on `cloud.<program-redacted>.com` or `app.<program-redacted>` using the operator-approved H1 alias pattern and secret-safe fill path only. Stop if the app sends verification email/code, shows CAPTCHA/OTP, requires passkey/SSO/OAuth provider, asks for phone/payment/KYC, or requires API token/OAuth/webhook/integration setup.

Do not perform role/IDOR/API proof testing until Account A/B and owned object controls are confirmed and a separate bounded proof run card exists.

## Signup attempt status

- Email secret availability validated through `scripts/kali-fill-secret.ps1` dry-run: available without printing the value.
- CDP secret fill to `input[name="username"]` reported success.
- The visible page remained on the Konnect login identifier step after click/Return attempts; no verification email/CAPTCHA/OTP/password/passkey/phone/payment/KYC gate was reached during this run.
- Tooling note: direct coordinate clicks were unreliable in the stacked noVNC/Chromium window. Next efficient path is to add/reuse a reviewed CDP click/navigate helper for text links/buttons, then continue with the same stop gates.

## CDP helper + signup gate update

- Added and tested a reviewed CDP action helper for Kali/noVNC browser control:
  - `scripts/cdp_browser_action.py`
  - `scripts/kali-browser-ops.ps1 -Action cdp-click`
  - `scripts/kali-browser-ops.ps1 -Action cdp-fill` for non-secret text only
- CDP text click successfully clicked the Konnect `Sign Up` link without coordinate guessing.
- CDP non-secret fill successfully filled the name field without printing the value.
- Secret-safe email/password fill path was hardened to support base64-encoded selectors and page preference for signup/auth pages.
- Email and password fills reported success without printing secrets.
- Current hard gate: stored password values do not satisfy Konnect's 12-character password policy; page remains on signup with password-strength failure.
- No verification email/CAPTCHA/OTP/phone/payment/KYC step was reached.
- Stop condition: password/passkey secret gate with no currently valid secret-safe password value. Operator action required to update `setting/local/hacklab.secrets.env` with a compliant signup password or manually continue in noVNC.

Latest screenshot:

- `<artifact-output-dir>/browser_state/<program-slug>-surface-map_20260529T170403Z.png`

## Email verification gate update — 2026-05-29T18:10Z

- Resumed from `A2_SIGNUP_PASSWORD_GATE` after validating that the Windows active workspace secret file contains a Konnect-compliant signup password without printing it.
- Kali wrapper caveat: `/mnt/hacking/setting/local/hacklab.secrets.env` still exposed stale 10-character password values from the old mounted workspace, so the current active `hacking2` ignored secret file was copied to `/tmp/hermes_current_hacklab.secrets.env` on Kali for this one fill. No secret values were printed.
- Filled owned-account signup fields via CDP/secret-safe path and submitted the ordinary Konnect email signup form.
- Result: browser reached `https://cloud.<program-redacted>.com/org-switcher` with visible text indicating the owned H1 alias is unverified and must verify email.
- New stop condition: `A2_EMAIL_VERIFICATION_GATE`. Operator must handle the verification email/link/code or continue manually in noVNC.
- No CAPTCHA/OTP/phone/payment/KYC/API-token/OAuth/webhook/integration/customer-data/proof-testing step was reached.
- Latest screenshot: `<artifact-output-dir>/browser_state/<program-slug>-email-verification-gate_20260529T181037Z.png`.
