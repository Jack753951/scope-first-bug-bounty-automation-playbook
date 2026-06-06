> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# <program-redacted> Taiwan First-Bounty Run Card — 2026-05-28

Status: prepared, not executed
Program: <program-redacted> Taiwan
Platform: <bug-bounty-platform>
Program URL: `https://<bug-bounty-platform>.com/<program-slug>`
Target-touching allowed now: false
Boundary: run-card only. No live target requests beyond already completed H1 policy/scope reads.

## Authorization basis

- H1 program policy is visible in logged-in browser.
- Program launched May 2026.
- Scope CSV parsed: 47 rows, all eligible for bounty and submission, max severity critical.
- Repo `config/scope.txt` already contains a <program-redacted> Taiwan H1 section from earlier operator confirmation.
- Latest H1 CSV vs `config/scope.txt` alignment check completed on 2026-05-28:
  - H1 CSV URL assets: 45.
  - Current `config/scope.txt` <program-redacted> hosts: 10.
  - Live execution is restricted to the 10 hosts already present in `config/scope.txt` unless the operator updates the whitelist.

Currently whitelisted <program-redacted> subset:

```text
www.tw.<program-redacted>.com
tw.<program-redacted>.com
member.tw.<program-redacted>.com
id.tw.<program-redacted>.com
my.tw.<program-redacted>.com
myself.tw.<program-redacted>.com
review.tw.<program-redacted>.com
cart.tw.<program-redacted>.com
cart-<program-name>-api.tw.<program-redacted>.com
mc.tw.<program-redacted>.com
```

## Report-title-first hypotheses

Candidate title A:

```text
Low-privileged/other owned account can access or modify another owned account's cart/review/member object via direct API request
```

Candidate title B:

```text
API allows action on owned account object that the UI blocks after account/session state change
```

Candidate title C:

```text
Search, review, cart, or account metadata for another owned account is exposed through direct URL/API access
```

Do not execute any title unless controls exist.

## Bundle

Primary bundle:

```text
api-ui-permission-mismatch
```

Secondary bundles:

```text
object-ownership-idor
metadata-only-leak
auth-role-separation
```

IDOR caution:

- <program-redacted> has a platform standards deviation for unpredictable IDs.
- Any IDOR-like report must show how the ID/object reference was obtained easily through an owned flow.
- Do not guess/brute force IDs.

## Candidate assets

Prioritized from H1 scope CSV:

```text
member.tw.<program-redacted>.com
id.tw.<program-redacted>.com
my.tw.<program-redacted>.com
myself.tw.<program-redacted>.com
cart.tw.<program-redacted>.com
review.tw.<program-redacted>.com
cart-<program-name>-api.tw.<program-redacted>.com
www.tw.<program-redacted>.com
tw.<program-redacted>.com
mc.tw.<program-redacted>.com
```

These are the only <program-redacted> hosts currently allowed by both H1 CSV and repo `config/scope.txt`.

Additional high-interest H1 CSV assets that are not currently in `config/scope.txt` and therefore cannot be touched until operator whitelist update:

```text
checkout.tw.<program-redacted>.com
pay.tw.<program-redacted>.com
payment.tw.<program-redacted>.com
cash.tw.<program-redacted>.com
rs-open-api.tw.<program-redacted>.com
fileupload.tw.<program-redacted>.com
fileupload-video.tw.<program-redacted>.com
partners.tw.<program-redacted>.com
marketplace.tw.coupangcorp.com
helpseller.tw.coupangcorp.com
```

High-risk / park unless explicitly bounded:

```text
pay.tw.<program-redacted>.com
payment.tw.<program-redacted>.com
cash.tw.<program-redacted>.com
fileupload.tw.<program-redacted>.com
fileupload-video.tw.<program-redacted>.com
partners.tw.<program-redacted>.com
ads-partners.tw.<program-redacted>.com
logs-partners.tw.<program-redacted>.com
marketplace.tw.coupangcorp.com
helpseller.tw.coupangcorp.com
```

Reason:

- Payment/order/seller/upload/partner flows can create payment, business, non-owned data, or destructive-risk boundaries.
- Use only after stronger policy/control clarity.

## Preconditions before EXECUTE

```text
Program: <program-redacted> Taiwan
Scope: latest H1 CSV + current config/scope.txt whitelisted subset only
Bundle: api-ui-permission-mismatch / object-ownership-idor / metadata-only-leak
Hypothesis: owned A object should not be accessible/actionable by owned B or unauthenticated context
Report title if true: low-priv/other owned account can access/modify another owned account's cart/review/member object via direct API

Positive control:
  Account A can create or view owned object through normal UI.

Negative control:
  Account B, or logged-out context, should not access Account A object.

Owned object/resource:
  Non-payment, non-order, non-customer object only: cart item, review draft/test item, profile/member metadata, saved item, notification preference, or similar.

Expected matrix:
  A -> A object: allowed
  B -> A object: denied
  logged-out -> A object: denied
  A after logout/session clear -> denied

Allowed actions:
  normal browser use
  account signup/login if no OTP/CAPTCHA/phone/payment/KYC beyond operator gate
  create owned low-risk object
  inspect browser DevTools/network manually
  replay only same owned request with controlled Account A/B session
  add `X-<bug-bounty-platform>-Researcher: [H1 username]` header if using a tool/proxy for requests

Blocked actions:
  scans/fuzzers/DAST
  brute force / ID guessing
  rate-limit testing
  DoS/resource exhaustion
  social engineering/phishing/redirection abuse
  non-owned/customer/seller data
  real purchase/payment/refund/order flows
  destructive modification or deletion
  upload/path traversal unless separately approved and marker-only
  leaked credentials/token/cookie/OTP storage
  final report submission

Operator cost:
  Unknown; likely H1 alias/account signup and maybe email verification. Stop for OTP/CAPTCHA/phone/payment/KYC.

Kill criteria:
  signup requires phone/payment/KYC before owned object exists
  no non-payment owned object can be created
  only one account/control possible
  object IDs are not obtainable through normal owned flow
  behavior is intended/benign product logic
  evidence would require non-owned/customer data

Evidence required:
  scope reference
  account/control matrix
  owned object labels only
  request/response snippets with secrets/cookies redacted
  expected vs observed
  proof boundary and no-customer-data statement
  cleanup note

Time box:
  60-90 minutes after operator/safe gate permits live execution

Decision:
  PREPARED_NOT_EXECUTED
```

## Internal multi-role lens

Adversarial planner:

- Best path is account/object API mismatch on cart/member/review/profile surfaces.
- Highest-value adjacent path is metadata-only leak or stale session after logout/downgrade if account controls exist.

Boundary engineer:

- Need A/B owned accounts or A/logged-out negative control.
- Need to avoid payments, orders, refunds, seller data, customer data, real purchases, and uploads unless separately bounded.
- Need `X-<bug-bounty-platform>-Researcher` header if moving beyond browser-only to request tooling.

Evidence critic:

- IDOR proof must show how object ID/reference was obtained easily.
- No claim without clean negative control.
- Screenshots/request snippets must redact cookies, auth headers, phone/email details, order/customer data.

Deterministic reviewer:

- Most likely benign explanations: anonymous public product/review/cart endpoints, intended shared state, anti-CSRF/session behavior, account-specific but non-sensitive metadata.
- Kill if object is intentionally public, no impact, or only missing security header/version/error info.

Final synthesizer:

```text
Decision: PREPARE; ask operator only for live-target safe gate / signup verification gates.
Next action: verify latest scope alignment and then request safe phrase before any target-touching browser work.
```

## Next gate

Operator/safe phrase is required before live target execution against <program-redacted> assets.

No action should be taken against <program-redacted> target hosts until that gate is satisfied.
