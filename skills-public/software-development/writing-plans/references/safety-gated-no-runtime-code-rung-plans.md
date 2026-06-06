> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Safety-Gated No-Runtime Code-Rung Plans

Use this pattern when a project phase is ready to move from architecture/design notes toward implementation, but actual code execution is not yet authorized or would risk crossing production/runtime boundaries.

## Trigger

- The user says to continue a project phase, but the active queue or project policy says the next code rung needs explicit selection.
- The next workstream touches media generation, upload, scheduler, OAuth, privacy, channel routing, external side effects, or other activation surfaces.
- A design-only artifact exists and needs to become an actionable implementation plan without changing runtime behavior.

## Procedure

1. Read the project-local active queue / accepted changes / relevant design note first.
2. Inspect narrow code surfaces only enough to make the future plan concrete: file paths, function names, existing tests, validation commands.
3. Write a plan artifact, not implementation code, unless the user explicitly chooses the code rung.
4. Put a prominent safety boundary near the top:
   - no generation / create / loop / remake,
   - no upload / publish / schedule,
   - no OAuth/token/client-secret/destination/privacy change,
   - no channel config switch,
   - no DB/runtime media mutation,
   - no broad renderer/platform rewrite.
5. Break the future code rung into TDD phases:
   - RED test with exact file path and expected failure,
   - minimal implementation,
   - focused GREEN command,
   - integration/regression command,
   - handoff update requirements.
6. Identify explicit deferrals so the plan does not smuggle in extra scope.
7. Update repo handoff to say the plan exists but implementation remains unexecuted.
8. Run project-local docs/safety validation if available; do not run unrelated generation or activation commands.

## Shape of a good plan

- Goal and architecture in 1-3 paragraphs.
- Exact future files to create/modify.
- Copy-pasteable test skeletons when useful.
- Exact commands in the user's native shell style.
- Expected RED/GREEN outcomes.
- Review tier/approval boundary for the future implementation.
- Handoff notes required after implementation.

## Pitfalls

- Do not treat "continue project work" as permission to cross a previously documented activation gate.
- Do not implement code just because the plan is obvious when the project queue says a concrete code rung must be chosen first.
- Do not let QA/profile/readiness labels imply upload/publication approval.
- Do not put source project facts into a class-level skill; put only the reusable planning pattern here.

## Example mapping

For a media automation project with a design-only asset/render/QA profile note, a safe next-phase plan can define:

- a future closed, versioned data-only profile registry,
- metadata label passthrough,
- optional read-only QA report labels,
- tests proving no render/generation/upload behavior changes,
- deferrals for profile-driven asset search, renderer branching, canary scoring, upload-readiness contracts, and channel JSON edits.
