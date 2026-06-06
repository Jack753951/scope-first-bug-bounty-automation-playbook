# 05 — Authorized Live-Target Dry Run

Status: planning template / does not authorize testing

## Dry-run objective

Before touching a real target, prove that the lane has enough policy, scope,
account, data, rate, evidence, and cleanup detail to execute safely.

## Required scope package

```text
Program / engagement name:
Authorization source:
In-scope assets:
Out-of-scope assets:
Allowed vulnerability classes:
Forbidden actions:
Rate/request limits:
Automation allowance:
Allowed accounts/data:
Allowed callbacks/OAST/tunnels:
Allowed state changes:
Testing window:
Disclosure/submission rules:
Evidence redaction requirements:
```

Unknown safety-critical fields fail closed.

## Candidate lane table

| Candidate | Class | Value | Scope status | Risk | Proof plan | Decision |
| --- | --- | --- | --- | --- | --- | --- |
| Example | access control | high | unknown | medium | role matrix | blocked |

## Proof plan fields

```text
Hypothesis:
Security boundary:
Attacker preconditions:
Accounts/roles used:
Exact endpoints/actions:
Positive proof:
Negative controls:
Safe marker/data:
Request budget:
Rollback/cleanup:
Stop conditions:
```

## Operator gates

- signup/login/verification;
- scope broadening;
- first target contact beyond passive reading;
- callbacks/OAST/tunnels;
- API token, OAuth, webhook, integration, billing, KYC, payment;
- customer/non-owned data risk;
- report-ready promotion or final submission.
