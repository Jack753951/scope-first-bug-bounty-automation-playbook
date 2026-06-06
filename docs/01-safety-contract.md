# 01 — Safety Contract

Status: public methodology / non-authorizing template

## One-sentence rule

Proceed only when the target, technique, account/data boundary, request budget,
and cleanup plan are explicitly authorized; otherwise stop, record the blocker,
and ask the operator.

## Default allowed work

- Read public docs, public advisories, disclosed reports, and vendor guidance.
- Build local disposable labs and intentionally vulnerable training targets.
- Run bounded scripts against owned local lab services with pre/post health checks.
- Draft candidate packets, templates, run cards, and report-readiness reviews.
- Normalize scanner/tool output into candidate-only observations.

## Default blocked work

- Any live target contact outside an explicit scope package.
- Broad scanning, fuzzing, DAST, stress testing, or rate-limit testing.
- Credential theft, token capture, cookie handling, OTP/CAPTCHA bypass, or secret storage.
- Accessing, copying, modifying, or retaining customer/non-owned data.
- External callback/OAST/tunnel/listener use unless explicitly allowed.
- Payment, abuse, KYC, billing, webhook, OAuth, integration, or API-token flows without a lane-specific gate.
- Public disclosure, report promotion, or final submission without human approval.

## Execution posture

Think aggressively; execute conservatively.

The planning model is:

```text
attack path -> proof boundary -> safe proof surrogate -> stop conditions -> evidence packet
```

This keeps realistic bug-hunting creativity while preventing unauthorized impact.

## Stop-before list

Stop before any step that would require:

- new target or scope interpretation;
- login/signup/verification that was not already approved;
- private data inspection;
- destructive change outside disposable owned state;
- persistence, stealth, malware-like behavior, or uncontrolled propagation;
- unapproved callbacks or internal network enumeration;
- report-ready claim or submission.
