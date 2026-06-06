> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# P3.9 Direction Review Prompt — Dry-Run Recon-to-Runner Bridge

Status: READY_FOR_CLAUDE_COWORK_DIRECTION_REVIEW
Date: 2026-05-19
Prepared by: Hermes
Review tier: T3 design-only direction review
Milestone: Gate C — dry-run recon-to-runner bridge direction

## Context

The cybersec lab has closed the P3.7/P3.8 program-policy dry-run hardening lane enough to ask for the next mainline direction.

Recent source-of-truth artifacts:

- `handoff/program_policy_dry_run_closeout_20260519.md`
- `handoff/active_strategy_queue.md`
- `handoff/project_launch_estimate_20260519.md`
- `handoff/cowork_p3_7_direction_review.md`
- `handoff/third_party_p3_7_implementation_review.md`
- `handoff/review_tiering_policy.md`
- `handoff/multi_party_review_decision_policy.md`
- `handoff/oss_recon_gate.md`
- `.hermes.md`

Relevant current code surfaces to inspect read-only:

- `recon.sh`
- `scripts/test_recon_program_policy_dry_run.py`
- `scripts/module_runner.py`
- `scripts/test_module_runner.py`
- `scripts/validate_module_io_bundle.py`
- `scripts/validate_preview_manifest.py`
- `scripts/validate_preview_ledger.py`
- `scripts/README.md`

## Review request

Perform a T3 design-only direction review for the next safe mainline slice: a possible dry-run recon-to-runner bridge.

The central question:

Should the project now implement a narrow offline-only bridge exercise where a policy artifact produced or represented by the recon/program-policy side is consumed by the existing dry-run-only module runner preview path, or should that bridge remain deferred while another lane is handled first?

Return one of:

- `APPROVE`: approve a narrow implementation slice as specified by you.
- `APPROVE_WITH_CHANGES`: approve only after applying explicit scope reductions / safety assertions / test requirements.
- `DEFER`: do not implement yet; explain what should happen first.
- `BLOCK`: unsafe or premature; explain blockers.

## Required analysis

Please answer these questions explicitly:

1. Review tier and milestone boundary
   - Is this correctly T3 design-only, or does it escalate to T4 because of recon/runner policy boundary proximity?
   - If T4, can implementation still be limited to offline tests/docs only without operator approval?

2. Whether to bridge now
   - Is a dry-run recon-to-runner bridge the best next step after Gate B?
   - Or should the project first do another closeout/review/docs/test-only lane?

3. Approved implementation shape if proceeding
   - Propose the smallest safe implementation slice.
   - Prefer tests/fixtures/docs only if possible.
   - State a maximum file list.
   - State whether runtime files may be edited. Default should be no unless strictly justified.

4. Safety boundary
   - Confirm no target-touching, scanner/module execution, live lab activation, real program scope, config scope change, schema promotion, report drafting/submission, scheduler, credentials/OAuth, deployment, billing, or production changes.
   - Confirm whether `module_runner.py` may be invoked only in its existing dry-run preview mode.
   - Confirm whether `recon.sh` may be invoked only with `--dry-run` against synthetic temporary HACKLAB fixtures.

5. OSS Recon Gate
   - Run the OSS Recon Gate design comparison before recommending implementation.
   - Compare with 2-5 relevant open-source projects/tools/formats, likely including SARIF, Nuclei workflows, OWASP ZAP context/scan policy, DefectDojo engagement/test/finding linkage, and/or ProjectDiscovery pipeline patterns.
   - For each reference, state useful pattern, adopt/adapt/ignore, safety concern, and impact on current contracts.

6. Required tests / safety assertions
   - Define exact focused tests needed if implementation proceeds.
   - Include negative assertions for no scanner execution, no module execution, no target touching, no real `config/scope.txt` mutation, no report/finding/evidence promotion, and fail-closed behavior on policy mismatch.

7. Deferred items and re-review triggers
   - Name what must remain deferred.
   - Name the triggers that require a fresh T3/T4 review.

## Non-negotiable constraints

This review itself must be read-only/design-only except writing its review artifact.

Do not:

- run live scans, probes, scanner execution, module execution, exploit attempts, fuzzing, brute force, callbacks, OAST, proxy/pivot/tunnel, or target-touching automation;
- contact any external target;
- modify `config/scope.txt`;
- create or modify real `programs/<program-slug>/scope.json` authorization files;
- change `recon.sh`, `module_runner.py`, policy helpers, schemas, modules, report surfaces, scheduler, deployment, credentials, OAuth, billing, or production settings;
- promote schemas or create a new contract without explicitly requiring separate implementation approval;
- treat automated output as confirmed findings;
- create a public report/submission adapter.

If you believe implementation should proceed, define a bounded implementation task but do not implement it in this review.

## Expected output file

Write the direction review to:

`handoff/cowork_p3_9_direction_review.md`

Also write/update a concise worker summary in:

`handoff/claude_code_result.md`

Use this final decision block:

```text
Decision: APPROVE / APPROVE_WITH_CHANGES / DEFER / BLOCK
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
```
