> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Live bounty Account A/B operator action card — 2026-05-26

Status: active / reusable operator-local gate card
Source: Hermes synthesis for first live A/B controlled testing attempt
Date: 2026-05-26
Boundary: operator-local account/session actions only. Do not share or store passwords, OTPs, phone numbers, cookies, tokens, API keys, verification links, raw aliases, raw email addresses, screenshots with PII, payment/KYC/order/support data, or third-party data.

## Purpose

Use this card when a live-bounty lane needs a second operator-owned account, second tenant, second role, or owned object visibility before Hermes can safely run an A/B controlled authorization matrix.

This card is meant to make the operator gate simple and secret-safe.

## Safe reply phrases

The operator should reply with only one of these safe phrases unless Hermes asks for a non-secret label:

```text
Account B ready
Tenant B ready
Role matrix ready
Object visible
No safe object
blocked_auth
blocked_captcha
blocked_email_verification
blocked_phone_verification
blocked_warning
blocked_policy
blocked_no_object
stop
```

Do not paste secrets, phone numbers, OTPs, passwords, cookies, full emails, verification links, API tokens, or screenshots containing identifiers.

## Generic Account B setup card

Operator-local steps:

1. Use the authorized/program-allowed signup or account-creation path only.
2. Create or verify Account B locally. Do not share the password, OTP, phone number, verification link, cookie, token, or email contents.
3. If the site shows CAPTCHA, phone verification, email verification, account warning, lockout, anti-abuse message, payment/KYC/order/support prompt, or anything unexpected, stop and reply with the matching safe phrase above.
4. After Account B is ready, check whether a harmless owned object exists or can be created without payment/KYC/order/support/upload/seller/admin/integration/workflow/run-script/callback behavior.
5. Reply only with:
   - `Account B ready` if the account exists but object viability is unknown;
   - `Object visible` if a safe owned object exists or can be created normally;
   - `No safe object` if there is no safe object path;
   - a `blocked_*` phrase if blocked.

## Generic Tenant B / workspace B setup card

Operator-local steps:

1. Use only program-allowed self-service workspace/tenant creation.
2. Do not invite third parties. Use only operator-owned accounts or program-provided test users.
3. Do not connect integrations, mailboxes, webhooks, API credentials, databases, payment methods, cloud accounts, or external services unless a separate plan explicitly allows it.
4. Do not create public shares or publish externally unless a separate plan allows it.
5. Reply with:
   - `Tenant B ready`
   - `Object visible`
   - `No safe object`
   - or the matching `blocked_*` phrase.

## Object viability checklist

A safe owned object should satisfy all of these:

```text
belongs only to operator/test accounts:
created or visible through normal UI/API:
ID/path/link provenance is normal and explainable:
does not require payment/order/KYC/support:
does not involve third-party/customer data:
does not require upload/parser testing:
does not trigger workflow/run-script/integration/callback:
can be harmlessly marked or observed:
can be cleaned up or left benign:
```

Examples that are often safer if policy allows:

- private project/note/document/folder/task/story;
- test workspace resource with harmless name/description marker;
- private table/base/list/board;
- profile metadata field with harmless value;
- draft-only item visible only to the owner;
- private share/revoke test object.

Examples that are usually not first-lane safe:

- payment/order/refund/coupon/cash/KYC state;
- customer-support ticket or message to real staff;
- mailbox/integration/webhook/API key/secret/resource connection;
- uploaded active file/parser test;
- seller/admin/partner/internal surfaces;
- any object containing third-party or real customer data.

## Hermes next step after safe phrase

If operator replies `Account B ready` or `Object visible`, Hermes should:

1. confirm exact program policy/scope artifact exists;
2. confirm `config/scope.txt` has only explicitly approved minimal assets before target-touching automation;
3. produce or update a tactical preview using `docs/strategy/live_bounty/live_bounty_tactical_preview_template_20260526.md`;
4. build a minimal Account A/B matrix for exactly one object family;
5. use Account A positive / Account B negative controls;
6. record only redacted paths/status/body excerpts and Account A/B labels;
7. stop if any third-party data, policy ambiguity, stronger technique, or report-ready candidate appears.

If operator replies `No safe object` or `blocked_no_object`, Hermes should park the target and update `docs/strategy/live_bounty/live_bounty_no_finding_feedback_log.md` instead of browsing longer.

## <program-redacted>-specific current use

Current status: <program-redacted> Taiwan is `needs_second_account` and `blocked_no_owned_object` until proven otherwise.

Operator-safe next replies after second phone/account gate:

```text
Account B ready
Object visible
No safe object
blocked_phone_verification
blocked_auth
blocked_warning
stop
```

Do not test or create state involving payment, checkout, order, refund, KYC, coupon redemption, customer support, seller/admin, upload, password/ID recovery, or third-party data.
