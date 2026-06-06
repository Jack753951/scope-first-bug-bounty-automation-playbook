> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Lightweight Follow-up Review De-escalation

Use this when a cybersecurity workspace has already completed a heavy direction/review slice for a specific boundary, and the operator wants less review overhead for small follow-ups.

## Trigger

- The operator says the review flow is too heavy, too fragmented, or agrees to a lighter tiered approach.
- A follow-up is inside an already-reviewed boundary and only adds tests, docs, fixtures, handoff updates, or narrow assertions.
- The work does not introduce a new runtime behavior, schema/contract, target-touching path, scanner/module execution, report/submission surface, credential/OAuth surface, scheduler, deployment, or production setting.

## Pattern

1. Classify the follow-up explicitly as T0/T1/T2 rather than defaulting to T3/T4.
2. Reuse the prior direction/review artifact as the governing boundary.
3. Do not create a fresh Cowork/Claude direction review for every small recommendation.
4. Implement the smallest local change, usually tests first.
5. Run focused tests, adjacent suite, `git diff --check`, and the project review wrapper.
6. Update compact handoff state and append-only accepted-changes history.
7. If the branch has an existing PR, stage only scoped files, commit, push, and post a PR comment using `--body-file`.
8. Escalate back to T3/T4 immediately if implementation requires changing the reviewed boundary.

## Example shape

A literal CIDR forced-deny follow-up after P3.7/P3.8 program-policy review stayed T2 because it only added dry-run regression coverage and handoff updates. The test asserted the already-existing behavior: global scope accepted a synthetic RFC 5737 CIDR, program policy denied without `--allow-cidr`, a deny artifact was emitted, no policy PASS occurred, and no scanner plan/execution markers appeared. No `recon.sh` runtime code, program-policy helpers, scope files, schemas, modules, runner, or live activation changed.

## Pitfalls

- Do not describe de-escalation as lowering safety. The safety boundary stays intact; only review overhead is reduced.
- Do not let a T2 label smuggle runtime behavior changes. If code changes target-touching behavior, policy semantics, schema contracts, module/runner behavior, or report/submission flow, reclassify upward before editing.
- Do not leave completed low-risk follow-ups as stale "fresh direction review" queue items; update the active queue so the next session starts from the real lane.
