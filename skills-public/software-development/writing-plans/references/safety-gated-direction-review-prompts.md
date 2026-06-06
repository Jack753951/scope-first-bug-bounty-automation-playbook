> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Safety-Gated Direction Review Prompt Pattern

Use this when a project is at a boundary decision point and implementation could prematurely expand safety/runtime scope.

Session-derived example: a cybersecurity workspace had completed a sequence of offline trial-only consumers and needed to decide whether to extract shared core helpers or close the phase. Instead of immediately refactoring, create a design-only direction-review prompt that forces an explicit verdict and preserves boundaries.

## Pattern

1. State the completed chain and current decision point.
2. Ask for one explicit verdict from a small enum, such as:
   - `DEFER_REFACTOR_AND_CLOSE_PHASE`
   - `EXTRACT_MINIMAL_CORE_HELPER`
   - `ROUTE_BACK_FOR_SCOPE_CLARIFICATION`
3. Separate observed duplication from approved implementation.
4. Include a strict "design-only constraints" section that forbids runtime expansion.
5. If extraction is recommended, define the smallest acceptable helper scope and compatibility tests.
6. If deferring, ask for closeout-review inputs and next-phase questions.
7. Require OSS/prior-art comparison when the change touches platform contracts or boundaries.
8. Require a concrete output file path and required headings.
9. Run only local/static validation after writing the prompt; do not trigger target-touching behavior.

## Guardrails to include for security-sensitive projects

- No live scans, target interaction, fuzzing, callbacks, OAST, proxy/pivot behavior.
- No schema promotion, runtime/recon wiring, scheduler/CI hooks, platform adapters, report submission, credentials, scope-file edits, deployment, billing, or production settings.
- Prefer read-only review via the project’s established worker route before any code change.
- Treat helper extraction as a separate future implementation task requiring TDD and compatibility checks.

## Minimal output contract for the reviewer

```text
# Direction Review

## Verdict
<ONE_OF_THE_ALLOWED_VERDICTS>

## Rationale
## Duplication / Boundary Assessment
## OSS / Prior-Art Notes
## If Proceeding: Minimal Task Boundary
## If Deferring: Closeout Questions
## Safety Boundary Confirmation
## Blocking Issues
## Non-Blocking Recommendations
```
