> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Live bounty high-hit-rate target filter — 2026-05-26

Status: active / passive-selection filter
Source: Hermes A0 passive OSINT policy + <bug-bounty-platform> program-directory search
Date: 2026-05-26
Boundary: passive selection only. No target asset navigation, no account creation, no scope expansion, no scan/fuzz/exploit, no credential handling, no report submission.

## Reviewer identity

- Reviewer route/tool: Hermes coordinator + terminal Python HTTPS requests to public <bug-bounty-platform> program-directory search endpoints
- Visible runtime model: gpt-5.5
- Provider / CLI version if visible: openai-codex provider; exact backend deployment not exposed
- Review focus: strategy / high-hit-rate target selection / live-bounty safety tiering
- Limitation: scoring uses public directory metadata/snippets and should be treated as triage, not authorization or final policy truth

## Purpose

The first two live/VDP runs proved the legal workflow, redaction discipline, noVNC route, and no-finding closeout. This filter changes the default from `flow-practice target` to `vulnerability-hit-rate target`.

Use this before selecting a live target. The goal is to quickly reject low-fit programs and prioritize programs that can support controlled, reportable evidence without risky techniques.

Important: this is a triage lens, not a tactical cage. It must not be used as a rigid whitelist of only five bug classes or as a reason to avoid creative preview. The preview stage should expand the tactical option set first, then use this filter to choose which option is safest, highest-fit, and best-evidenced for the current program.

## Scoring model

Score each candidate 0-2 for each high-value property:

| Criterion | Why it matters |
|---|---|
| Self-service signup | Reduces operator/program friction and enables owned-account testing |
| Two accounts / two tenants possible | Required for IDOR/BOLA, tenant isolation, and negative controls |
| Workspace / org / team boundary | Good SaaS authorization surface |
| Roles / members / invites | Enables role-confusion and permission tests |
| Free owned objects | Provides object IDs without payment/KYC/order/support state |
| API docs / API tokens | Enables UI-vs-API authorization mismatch checks |
| Access-control testing appears allowed | Needed before A/B or authz proof |
| No payment/KYC/phone/order dependency | Avoids high-risk or blocked evidence creation |
| Share/public-private boundary | Useful for unauth/auth and revocation checks |
| Public reports/docs/SDKs exist | Improves OSINT grounding and test design |

Recommended interpretation:

```text
16+  high-hit-rate candidate; suitable for main live lane after exact policy intake
12-15 viable; confirm prerequisites before target-touching
8-11  short viability check only; likely surface/no-finding
<8    park unless the operator specifically wants this program
```

## Fast reject rules

Park or defer when any of these are true:

- No second account/tenant path and the intended bug class needs A/B controls.
- No safe owned object can be created or naturally observed.
- Useful evidence requires payment, KYC, real order/booking, refund, support contact, or phone-gated state.
- Program rules forbid the needed class or are ambiguous.
- Only visible state is an empty dashboard with no object/role/API path.
- The likely useful area is A4: scanner/fuzzer/DAST, callback/OAST, upload/parser, workflow execution, run-script, integration, API-key/secret, payment/KYC, or report submission.

## Preferred bug-class order

Default high-hit-rate starting points:

1. IDOR / BOLA / object ownership
2. Tenant / workspace isolation
3. Role / permission confusion
4. API authorization mismatch
5. Share link / public-private boundary

This order is a starting bias, not a lock. Preview may propose additional or adjacent lanes when the product shape, public methodology, disclosed reports, or policy facts make them higher-value and still safe. Examples: OAuth/OIDC flow confusion, webhook misbinding, business-logic state confusion, import/export privacy boundary, audit-log/invite lifecycle flaws, cache or indexing disclosure, GraphQL/object graph authorization, mobile/API parity mismatch, or configuration exposure. Treat those as candidate lanes and map them to the same requirements: exact policy allowance, owned data, positive/negative controls, redacted evidence, stop conditions, and report-readiness thresholds.

Use XSS, SSRF/OAST, upload/parser, workflow execution, run-script, and integration testing only under separate A4 plans when the program explicitly permits them.

## Process change

A0 OSINT and program scoring are now the default first step for more live vulnerability investigation. A0 is safe to run autonomously because it reads public program metadata, policy, docs, disclosed reports, OWASP/PortSwigger references, and OSS/test-case material only.

A2 surface mapping should be timeboxed to 20-30 minutes and should answer only viability questions: object, ID, API, role, tenant, Account B feasibility, and policy blockers. If no viable controlled proof path appears, park the target quickly.

## Preview tactical-freedom rule

Preview exists to widen tactical vision before execution. Each preview should list at least:

1. the default high-hit-rate lane;
2. 2-4 adjacent creative lanes suggested by the product shape or public methodology;
3. what extra permission/control would unlock each adjacent lane;
4. which lanes are safe now, later-only, or blocked.

Do not collapse preview into a checklist that only asks “can we do IDOR?”. The correct pattern is:

```text
expand options -> classify risk/prerequisites -> choose one bounded lane -> preserve the rejected/blocked ideas as next-preview seeds
```

That keeps tactical freedom while preventing live-target overreach.
