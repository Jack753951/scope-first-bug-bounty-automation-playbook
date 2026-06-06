> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# HackerOne Testing-Guidance Requests

Use this reference when the operator wants to ask a HackerOne program for permission, test accounts, sandbox/staging access, or rules clarification before performing a live-target test such as two-account IDOR/object-ownership checks.

## Preferred route

1. Prefer the program's official `Ask a question`, `Contact program`, program inbox, or discussion route when available.
2. Do not contact company employees, customer support, social media, or unrelated business channels for bug-bounty testing permission.
3. Do not ask the program to bypass phone verification, CAPTCHA, OTP, or anti-abuse controls. Ask for approved test accounts, sandbox/staging, or guidance on creating a second researcher-owned account.
4. If no official question/contact route exists and the operator considers using `Submit report`, treat it as a last resort and warn that HackerOne pre-submission review may block or down-rank it because it is not an actual vulnerability report.

## Submit-report fallback behavior

If using the report form as a guidance request:

- Title should clearly say `Testing guidance request`, not imply a confirmed finding.
- First sentence should say it is not a vulnerability report yet.
- Impact should explicitly say no vulnerability/impact is claimed yet.
- Do not include secrets, OTPs, phone numbers, cookies, tokens, or private user data.
- Fill fields only as much as required to draft/save; run checks before submission.
- Stop before final Submit and require operator approval.

Expected HackerOne/Hai checks may include:

- `Not a vulnerability report` / blocking issue because the content is a permission/guidance request.
- Missing required severity; if allowed, use `None`/informational, but some programs still require a conventional severity.
- No PoC / no demonstrated impact / no asset-weakness match.

These checks are a signal to prefer an official contact route instead of forcing submission.

## Safe guidance-request template

```text
Hi <Program> team,

This is not a vulnerability report yet; this is a testing-guidance request before I perform any cross-account testing.

I am preparing a low-speed, account-owned access-control test within your HackerOne scope.

The specific lane I would like to test is cross-account object ownership / IDOR between two normal customer accounts, using only objects created or visible through normal UI flows.

I currently have only one phone number available and do not want to bypass phone verification, use SMS rental services, or create accounts in a way that could violate anti-abuse controls.

Could you advise whether the program can provide any of the following?

1. Two normal customer test accounts;
2. A sandbox or staging environment for researcher testing;
3. Guidance on creating a second researcher-owned account without violating phone verification / anti-abuse rules;
4. Confirmation that this class of testing should be deferred unless I have two fully owned verified accounts.

I will keep testing manual, low-speed, account-owned only, avoid payment/checkout/KYC/upload/seller/admin flows unless explicitly approved, and include any required researcher header where tooling permits.

Thanks.
```

## Classification after response

- If the program provides approved accounts/environment/guidance: update the scope package and plan a low-speed owned-account lane.
- If the program declines or provides no safe way to test: mark the lane `blocked-needs-second-account / no finding yet` and switch to another low-risk surface or program.
- If there is no response: do not perform cross-account testing that requires a second account you cannot create without violating controls.
