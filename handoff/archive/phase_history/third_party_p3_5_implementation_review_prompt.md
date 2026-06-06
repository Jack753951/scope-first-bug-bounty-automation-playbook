> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Third-Party P3.5 Implementation Review Prompt

Date: 2026-05-19
Reviewer route requested: Claude/Cowork via local Hermes cowork / Claude Code CLI. Record route/tool and visible model/runtime; if exact model is not exposed, state that limitation.
Review tier: T3 implementation review
Milestone: Phase 3 P3.5 report-readiness reviewer prompt catalog

## Review Goal

Independently review the implemented P3.5 slice against `handoff/cowork_p3_5_direction_review.md`.

Expected implemented files:

- `templates/report_readiness_reviewer_prompts.json`
- `scripts/test_report_readiness_reviewer_prompts.py`
- `scripts/README.md`
- `handoff/cowork_p3_5_direction_prompt.md`
- `handoff/cowork_p3_5_direction_review.md`

Review constraints:

- Do not run live scans, probes, exploit tools, callbacks, OAST, network, scanner imports, or target-touching automation.
- Do not modify files except writing your review to `handoff/third_party_p3_5_implementation_review.md`.
- Treat `config/scope.txt`, `recon.sh`, module runner runtime, workflow consumers, schemas, manifests, profiles, reports, loot, credentials, OAuth, scheduler, deployment, billing, and production settings as forbidden.

## What to Check

1. Confirm the implementation obeys the approved P3.5 scope:
   - static JSON prompt catalog only
   - tests-only catalog validation
   - README note only
   - no reviewer-notes artifact
   - no schema promotion
   - no new consumer
   - no chain script behavior change
   - no renderer, platform adapter, report drafting, or submission surface

2. Spot-check the catalog:
   - keys entries by existing `GATE_*`, `BLOCK_*`, and `CHECK_*` codes
   - has closed allowed response postures only: `still_blocked`, `still_needs_manual_review`, `needs_more_evidence`, `defer`
   - avoids forbidden lifecycle/promotion/platform/scanner/drafting/live-target vocabulary
   - has no URLs or network/callback references
   - contains no field names that imply drafting, platform lifecycle, severity-axis reclassification, scanner output import, or report submission

3. Review tests:
   - catalog parses and canonical JSON is enforced
   - marker is flat and not slash-shaped like a schema
   - gate/block/check coverage is exact
   - postures are closed
   - ids are stable and sorted
   - forbidden vocabulary locks exist
   - chain vocabulary sources are scanned as text only
   - tests do not import workflow consumers just to read constants

4. Review validation results already run by Hermes:
   - `python -m unittest scripts.test_report_readiness_reviewer_prompts scripts.test_report_readiness_gate -v` => 28 OK
   - `python -m unittest discover -s scripts -p 'test_*.py'` => 375 OK, 8 skipped
   - `HACKLAB=<private-workspace> ./bin/hermes review` => PASS; Python compile OK 74 files; shell scripts OK; lock clear

5. Decide: PASS / PASS_WITH_RECOMMENDATIONS / REQUEST_CHANGES / BLOCK.

## Required Output

Write `handoff/third_party_p3_5_implementation_review.md` with:

```text
# Third-Party P3.5 Implementation Review

Date:
Reviewer route/tool:
Visible model/runtime model:
Review tier:
Milestone:
Decision:

## Diff / File Summary
## Scope Compliance
## Safety Assertions Verified
## Catalog Review
## Test Review
## Validation Reviewed
## Blocking Issues
## Non-Blocking Recommendations
## Deferred Follow-ups
## Acceptance Notes
```
