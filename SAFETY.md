> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# SAFETY — Single Source of Hard Stops

Status: active, binding

This file is the single binding safety/authorization contract for the project. Other docs may define workflow hygiene, file ownership, schemas, or stop-condition mechanics, but they do not add target-testing authorization gates beyond this rule.

## One-sentence rule

Proceed only when the target and action are explicitly in `config/scope.txt` and `programs/<slug>/scope.json`, stay inside an operator-approved owned-data proof boundary, and are low-volume, reversible, and evidence-safe. Bounded low-speed active recon is allowed by default for exact in-scope assets only when program rules and the per-program scope file permit the specific technique, with fail-closed scope checks, conservative rate limits, no customer/non-owned data, no secrets/tokens/cookies/OTP/passwords/verification links, no destructive or stealthy behavior, and redacted evidence handling. A3 is the standing lane-approved proof tier: bounded API-token creation, owned-object fuzz/discovery, SSRF/callback/OAST surrogates, and exploit-chain steps may proceed as A3 capabilities when the per-program scope file permits the technique, the proof uses operator-owned accounts/objects or operator-controlled callbacks, request/action caps and cleanup are defined, and the stop-before list excludes customer data, secret capture, credential extraction, uncontrolled internal enumeration, persistence, destructive impact outside recoverable owned test state, and final submission. Otherwise stop and ask before scope changes, credentials/secrets, non-owned/customer data, fuzzing beyond the approved profile, DAST beyond approved templates, SSRF/OAST/exploit-chain steps beyond the approved capability, high-volume automation, integrations/webhooks/payment/KYC/external side effects, report-ready promotion, public disclosure, or final submission.

## Authority

Current explicit operator instruction overrides this file only by narrowing or approving a named hard-stop action for the current bounded task; missing or ambiguous scope, policy, ownership, or evidence boundary fails closed.
