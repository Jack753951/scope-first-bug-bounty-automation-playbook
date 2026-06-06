> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Active Strategy Queue / Phase-Closeout Pattern

Use this reference when a long-running project has many handoff files, one-off reviews, periodic review packets, and parallel workstreams.

## Trigger

Apply when any of these are true:

- A mini-phase is being closed out.
- A periodic/deep review produced broad recommendations.
- Review artifacts are accumulating faster than current-state summaries.
- The next step is ambiguous because multiple safe lanes exist.
- The user asks to close out a phase and then prompt for the next step.

## Pattern

1. Close the phase in repo handoff, not global memory.
   - Write a closeout note with accepted scope, validation evidence, safety boundaries, non-blocking notes, and next-decision options.
   - Update accepted changes and any rolling engineering review log.

2. Finish pending review artifacts before starting a new lane.
   - If a periodic packet has blank reviewer/synthesis files, complete recommendation-only reviews or mark blockers explicitly.
   - Synthesize into decisions, anti-actions, and owners.

3. If a reviewed implementation slice was actually completed, reconcile the active queue immediately.
   - Move the queue from "next design/review pending" to "implementation complete/verified" instead of leaving stale future-tense language.
   - Record the review verdicts, reviewer route/tool, visible model/runtime if exposed, and limitations when the exact child runtime is not exposed.
   - Summarize the precise changed boundary and the precise untouched/forbidden surfaces.
   - List the validation set that makes the slice accepted, but keep raw command output and run-specific details in repo handoff or logs.
   - Preserve unrelated untracked files as explicitly unrelated; do not silently fold them into the accepted slice.

4. Convert broad recommendations into a compact active strategy queue.
   - Use statuses such as `DO_NOW`, `NEXT`, `PAUSED`, `USER_GATED`, and `AVOID`.
   - Each lane should have: current verdict, next allowed action, blocked action, evidence file, and user approval requirement.
   - After an implementation lands, the first next candidate is often closeout/commit hygiene, not another feature slice.

5. Keep safety gates explicit.
   - Canary/readiness packets are discussion-ready only, not upload/publication approval.
   - Upload, publication, scheduler, OAuth/token/client-secret, privacy defaults, active channel switches, destination filling, and runtime data changes stay user-gated.
   - For security tooling, distinguish a narrow explicit/manual data-flow bridge from automated coupling: auto-discovery, auto-copy, scanner/module execution, finding/evidence promotion, reports/submission, CI/scheduler, and live target activation remain separately reviewed and operator-gated.

6. Prompt the user with ranked next-step choices only after the closeout and synthesis are recorded.

## Pitfalls

- Do not let review artifacts become the work; synthesize them into a short current-priority index.
- Do not store phase state in global Hermes memory unless it is a compact cross-project pointer.
- Do not create a new one-off review file when a rolling log or active strategy queue is the better entry point.
- Do not treat `CANARY`, `CANARY_READINESS`, or similar review labels as authorization to execute external side effects.
- Do not leave an active strategy queue saying "prepare direction review" after the direction review and implementation have both completed; stale future-tense queue entries misroute the next `continue`.
- Do not describe an explicit, user-supplied artifact path as an automated bridge. If there is no auto-discovery/copy/execution, name it as explicit direct-read and keep automation activation separately gated.
