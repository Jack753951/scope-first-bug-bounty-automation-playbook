> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Multi-Party Review Decision Gate

Use this reference for safety-gated, long-lived projects where a single third-party review is not enough to decide whether a change should proceed.

## Core model

- Multi-party review informs the decision.
- Hermes synthesizes review outputs and gates the next action.
- The operator remains the final authority for high-risk activation.
- No agent should be the only reviewer of its own implementation.

## Review roles

1. Implementation reviewer
   - Correctness, regressions, tests, maintainability, deterministic behavior, and slice-scope compliance.

2. Safety/security reviewer
   - Authorization, scope gates, live-target behavior, scanner/callback/proxy/pivot/transport risk, secrets/loot/report handling, and fail-closed tests.

3. Architecture/roadmap reviewer
   - Modularity, updateability, contract boundaries, artifact sprawl, OSS Recon Gate alignment, and long-term platform fit.

4. Hermes decision layer
   - Assign/confirm tier, separate blocking vs advisory findings, verify validation, decide authority level, and record accepted outcomes.

5. Operator
   - Final approval for target-touching activation, scanner/recon behavior, scope changes, scheduler/deployment/production, credentials/OAuth/billing, public submission/publication, and unresolved safety disagreements.

## Authority by tier

| Tier | Hermes authority | Operator approval |
|---|---|---|
| T0 trivial docs/bookkeeping | direct | not required |
| T1 docs/data-only fixtures/prompt catalogs | direct | usually not required |
| T2 local tests/validators/offline helpers | direct if reviewers agree; conditional for minor non-blocking recommendations | only for material disagreement or side-effect risk |
| T3 runtime workflow/contract/schema/module/report/plugin boundaries | conditional only when reviewers align and activation remains deferred | required for major disagreement or boundary expansion |
| T4 scanner/recon/scope/target-touching/callback/proxy/pivot/transport | escalation-only for activation; Hermes may accept docs/tests-only prep | required before activation |
| T5 deployment/scheduler/credentials/OAuth/billing/public submission | escalation-only | always required |

## Final decision block

```text
Decision: PASS / PASS_WITH_CONDITIONS / REQUEST_CHANGES / DEFER / ESCALATE_TO_OPERATOR
Tier: T0/T1/T2/T3/T4/T5
Milestone:
Hermes authority: direct / conditional / escalation-only
Reviewers consulted:
- <route/tool>; visible model/runtime: <model if exposed, otherwise limitation>
Validation performed:
Blocking findings:
Non-blocking recommendations:
Safety boundary:
OSS Recon Gate: not applicable / attached / required before implementation
User approval required: yes/no; reason:
Accepted changes updated: yes/no/not applicable
Next action:
```

## Reviewer prompt add-on

```text
Review this change as part of the multi-party review decision policy.

Separate your findings into:
1. Blocking defects
2. Non-blocking improvements
3. Safety/security concerns
4. Architecture/roadmap fit
5. Deferred recommendations

State the review tier you believe applies: T0/T1/T2/T3/T4/T5.
State whether Hermes may decide directly, conditionally, or must escalate to the operator.
State whether operator approval is required before any activation.
Label your reviewer route/tool and visible model/runtime if exposed; if not exposed, state that limitation.
```

## Pitfalls

- Do not treat one positive third-party review as approval for all risk levels.
- Do not let review artifacts become the work; synthesize a decision and next action.
- Do not let advisory recommendations silently expand the current slice.
- Do not approve T4/T5 activation without explicit operator approval, even if reviewers are positive.
- Do not copy OSS tool defaults that assume live target interaction into an authorized-testing platform.
