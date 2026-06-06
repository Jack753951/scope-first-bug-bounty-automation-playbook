> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Phase-Closeout Milestone Checkpoints

Use this pattern when a long offline/design/review phase needs to be closed or advanced without accidentally granting runtime, production, or target-touching approval.

## When to use

- The user asks to continue after a sequence of policy/docs/tests-only slices.
- A phase has accumulated many micro-slices and needs a clear checkpoint.
- The next phase may introduce a higher-risk boundary such as lab/live execution, scheduler, external services, uploads, credentials, or production activation.
- The safest answer may be "close the offline phase and move to a planning gate" rather than "write more code".

## Closeout artifact shape

Create a single handoff/checkpoint document with these sections:

1. `Decision`
   - Use an explicit verdict such as `PASS_WITH_CONDITIONS / CLOSE_<PHASE>_<MILESTONE>`.
   - State exactly what is accepted and what is not approved.

2. `What the phase achieved`
   - Summarize capabilities by class, not by every commit.
   - Name important artifacts only when they are decision-relevant.

3. `Current capability statement`
   - Split into `can currently support` and `still cannot support`.
   - Be especially explicit about runtime, external-side-effect, target-touching, publication/submission, credential, and scheduler boundaries.

4. `Exit conditions`
   - Table: `condition | status | evidence / note`.
   - Mark incomplete validation or cleanup as `Conditional`, not silently complete.

5. `Local demo / validation checklist`
   - Provide copy-pasteable commands only for already-approved local/offline validation.
   - Include expected posture, not just expected pass/fail.
   - If final validation was not run or was denied, say so in the final report and do not claim it passed.

6. `Remaining gaps carried forward`
   - These are not blockers to closing the current phase, but they block the next activation boundary.

7. `Next phase entry criteria`
   - List exactly what must happen before the next higher-risk boundary can activate.
   - Include operator approval when needed.

8. `Default next slice`
   - Prefer a planning/direction slice before any activation.
   - State its boundary in negative terms too: no target, no scope/config activation, no runtime execution, etc.

9. `Final decision block`
   - Include tier, milestone, authority, reviewers consulted/model visibility, validation performed, blockers, recommendations, safety boundary, OSS-gate status, and user approval requirement.

## Updating navigation files

After writing the checkpoint:

- Update the compact strategy/current-navigation document so the new current lane is the closeout decision and the next default lane is explicit.
- Update the append-only acceptance history with a concise boundary summary.
- Do not overwrite or weaken older accepted-change entries; add a new top entry.

## Pitfalls

- Do not let a closeout checkpoint become hidden activation approval.
- Do not mix `phase is closed as offline MVP` with `lab/live is authorized`.
- Do not claim validation passed if a tool call was denied, skipped, or not run.
- Do not expand schemas, runners, validators, profiles, manifests, adapters, or production settings inside a documentation closeout unless the user explicitly asked for an implementation rung and the review tier permits it.
- Do not turn unrun demo commands into proof; label them as a checklist.
