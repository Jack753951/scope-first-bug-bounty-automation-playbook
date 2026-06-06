> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Dual-track first-bounty synthesis — 2026-05-27

## Operator instruction

Run both tracks autonomously until an operator gate appears:

1. Multi-agent freshness/control target funnel.
2. One latest-vulnerability local-lab/detector lane.

Operator gates remain: auth/OTP/CAPTCHA/email verification/phone/payment/KYC/control setup requiring human action/final report submit.

## Multi-agent target funnel result

Top candidates from role-separated agent work:

1. <program-redacted> — EXECUTE first
   - Freshness: launched May 2025; active and high-signal.
   - H1 page reportedly permits trial portal creation with @researcher-alias.example alias.
   - Strong CRM/web/API object model; likely portals/users/records/API tokens.
   - Expected operator cost: 0-1 until email/CAPTCHA/OTP gate.
   - Bundle fit: auth-role-separation, object-ownership IDOR, API/UI permission mismatch, removed/downgraded stale access.

2. <program-slug> — EXECUTE second
   - Freshness: launched Oct 2025; updated May 2026.
   - Strong API-management SaaS model; org/team/API/service/token objects.
   - Expected operator cost: 1; possible Auth0/email gate.
   - Bundle fit: tenant isolation, org/team privilege, API/UI mismatch.

3. Notion — EXECUTE third
   - Freshness: launched Nov 2025; active bounty.
   - Explicit self-signup; excellent workspace/page/database/integration controls.
   - Expected operator cost: 0.
   - Caveat: very crowded/high volume.

4. <program-redacted> — PARK for standard authz bundle
   - Good staging/account setup, but access-control permission issues reportedly out of scope as of 2026-02-06.
   - Keep only for non-authz/API/XSS/session lane.

5. Anthropic — PARK unless clean account/API access exists
   - Very fresh but high crowding; API/console may require phone/payment/credits.

6. Vercel OSS — offline fallback
   - Good zero-cost local/repro lane, but not the SaaS A/B control path.

7. Whatnot / Twilio family — PARK until clean no-phone/no-payment path confirmed.

<program-redacted> note: good sandbox/control model but public page appears External VDP/no bounty; only resume if a bounty-eligible H1 opportunity view is confirmed.

## Control/setup gate to apply to each EXECUTE candidate

10-minute gate:

- Can create/sign in with H1 alias without phone/payment/KYC/company OAuth?
- Can reach dashboard before email verification blocks everything?
- Can create workspace/org/project/object?
- Can invite or create second owned user / role / member?
- Can establish clean lower-priv/removed/different-workspace negative control?
- Can map to one practiced bundle without non-owned data?

Immediate PARK if blocked by CAPTCHA/OTP/email verification before any dashboard/object access, phone, payment, KYC, company OAuth, real third-party integration, support contact, or no negative control.

## Latest-vulnerability lab/detector lane

Selected lane: <specific-cve-id> — Next.js Middleware authorization bypass via `x-middleware-subrequest`.

Why:

- Recent and high-signal.
- Common in modern bounty scopes.
- Non-destructive differential detector possible.
- Can be validated on a disposable local Next.js app with protected canary route.
- Live transfer can be GET-only, path-limited, candidate-only, and scope-gated.

Next lab artifacts to create:

- local disposable Next.js vulnerable app or minimal equivalent proof target;
- bounded detector that compares baseline protected-route behavior against `x-middleware-subrequest` probes;
- false-positive controls: Next.js fingerprint + stable baseline/probe differential + inert-header control + no body retention for live targets;
- live transfer gate: explicit program scope/rules, operator-supplied small path list, GET/HEAD only, no data extraction.

## Hermes decision

Proceed now with <program-redacted> precondition/signup-control gate as the live mainline. In parallel, create the Next.js CVE detector/lab plan artifacts locally. Stop only if <program-redacted> reaches human verification/CAPTCHA/OTP/phone/payment/KYC/final-submit/control-setup requiring operator action.
