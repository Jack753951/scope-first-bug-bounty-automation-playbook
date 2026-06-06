> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Active Testing Policy

Status: active simplified policy
Owner: Hermes safety gate
Scope: authorized bug-bounty work, local labs, CTF/training calibration, and reusable module/plugin execution

## Purpose

This file removes the old module-risk-tier machinery from active decision-making. The project should not spend energy classifying every action into tiers. Use the hard-stop list and capability-growth rule instead.

## Default Learning Rule

For disposable/recoverable local靶機, intentionally vulnerable apps, and offline/local capability work:

```text
Use the tool, cap obvious runaway behavior, keep artifacts local, recover if needed, validate, and record candidate/verified lessons honestly.
```

Mature offensive/security tools and aggressive local scripts are allowed when the target is authorized and recoverable. Temporary NAT/package pulls are allowed when needed for local lab setup, but close and verify network posture afterward.

## Hard Stops

Do not proceed without explicit operator approval when an action would involve:

- public/unknown/live target interaction outside exact authorized scope;
- scanner/fuzzer/DAST/exploit/callback/OAST/tunnel/proxy/pivot automation against a live target;
- OAuth, integrations, webhooks, mailbox/channel connection, API-token creation, billing/payment/KYC, scheduler/deployment/publishing, or external persistent services;
- invite/team/role/account mutation outside an approved owned-account proof boundary;
- credentials, cookies, tokens, OTPs, passwords, phone numbers, API keys, verification links, loot, customer/non-owned data, or proprietary data;
- malware, stealth persistence, evasion, unauthorized pivoting/relay, brute force/password guessing, resource exhaustion, destructive payloads, or uncontrolled propagation;
- report-ready promotion, public disclosure, or report submission.

## Live / Bug-Bounty Work

For live bounty or client-like work:

- exact scope and program rules must be known;
- `config/scope.txt` and `programs/<slug>/scope.json` remain authoritative where used;
- program rules can only narrow what is allowed;
- owned accounts/objects/test data are required for proof;
- stop before customer/non-owned data, secrets, external communication, destructive state, or final submission;
- automation output remains triage/candidate until evidence is reviewed.

If an in-scope owned-account browser/manual lane is already established, Hermes should move to a reportable / no-finding / blocked checkpoint without asking for extra review approvals. Ask only for real operator gates: auth, OTP, CAPTCHA, phone, Account B/session identity, ambiguous scope/rules, secret handling, external side effect, or final submit.

## Evidence and Validation

- Keep evidence minimal and redacted.
- Use labels for accounts/objects; do not store secrets or PII.
- Record what was tested, what was not tested, and why.
- For local lab execution, capture pre/post health, cleanup, and network posture.
- For scripts/contracts, run focused parse/compile/tests instead of ceremony.

## Capability-Growth Bias

Do not let review vocabulary, historical tiers, or generic caution block authorized local learning or capability-library growth. Preserve useful hypotheses and blocked lanes with clear reasons; do not delete them simply because they are not executable yet.
