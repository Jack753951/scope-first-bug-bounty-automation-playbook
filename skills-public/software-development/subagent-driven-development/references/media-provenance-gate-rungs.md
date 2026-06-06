> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Media provenance gate rungs

Use this reference when a side-effect-sensitive media/channel repo generates local-only videos or other visible artifacts from stock/search assets.

## Pattern

1. Render exactly one local-only artifact for the candidate gate.
2. Inspect the machine-readable provenance/relevance report before spending reviewer budget on visual QA.
   - Accepted assets: URL/id/query/reason.
   - Rejected assets: URL/id/query/matched deny term or rejection reason.
3. If provenance already shows a blocker, do not promote the artifact to visual review/canary review. Treat it as a failed rung and fix the policy first.
4. Patch the policy with TDD:
   - Add a regression fixture for the exact asset/id/URL pattern that slipped through.
   - Add a safe counterexample that must remain accepted.
   - Add/adjust tests that prove the channel/profile emits the new deny terms or scoring rule.
5. Re-run targeted tests, compile checks, and the repo validate command.
6. Re-render exactly one post-fix local-only artifact.
7. Re-inspect provenance to prove the formerly accepted bad asset is now rejected.
8. Only then run a read-only visual/domain QA packet and record the verdict in handoff files.

## Useful gate semantics

- `LOCAL_ONLY_LEARNING_ARTIFACT_NOT_PRIVATE_CANARY_READY`: technically generated, useful for learning, but not eligible for upload/canary.
- `LOCAL_LEARNING_ONLY`: visual/domain reviewer agrees the artifact is only evidence for the next local rung.
- `PRIVATE_CANARY_CANDIDATE`: only after provenance, render QA, visual QA, and safety gates all pass; this is still not publication permission.

## Pitfalls

- Do not rely on broad deny phrases only. Real stock URLs often use adjacent wording (`counting money` vs `cash counting`, singular/plural variants, direct nouns such as `cash`/`money`). Regression tests should use the real escaped asset/id/URL that slipped through.
- Do not send an artifact to creative/vision review when provenance has already failed. Save reviewer budget and fix the gate.
- Do not call a worker run failed just because it ended with max-turns or no polished final report. Inspect workspace changes and validate them locally; useful TDD changes may already be present.
- Do not let a passing local render imply channel readiness. Keep the verdict local-only until the post-fix artifact passes provenance and visual/domain review.

## Handoff record checklist

Record in the repo handoff files:

- local artifact path and metadata/report paths
- exact accepted bad asset(s), if any
- policy/test files changed
- worker route/tool and visible model/runtime when available
- raw worker artifact path if available
- targeted tests/compile/validate commands and results
- post-fix artifact path
- evidence that the previously bad asset is now rejected
- remaining blockers and next safe rung
