> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Security dry-run bridge follow-up TDD pattern

Use when an independent safety/implementation review returns non-blocking recommendations for an offline cybersec bridge or handoff-only slice, especially recommendations like hash drift/tampered copied artifact coverage or explicit test-only helper documentation.

## Trigger

- Existing slice is offline/local or dry-run only.
- Review verdict is PASS_WITH_RECOMMENDATIONS or similar.
- Follow-up must stay inside tests/comments/handoff and must not introduce runtime coupling.
- The code under test copies, translates, stages, or references policy/evidence artifacts only inside a test harness.

## Pattern

1. Keep the scope narrow.
   - Only tests, comments, and handoff updates unless a fresh direction review approves broader implementation.
   - Do not modify runtime bridge code, scanner/module execution, scope/config, schemas, modules, report adapters, credentials, scheduler, deployment, billing, or production settings.

2. Turn the recommendation into a RED regression.
   - For tampered copied artifacts, copy/stage the artifact exactly as the harness does, record its hash, mutate bytes directly, then assert the hash changed.
   - Invoke the existing consumer/runner through its current explicit CLI/API path.
   - Assert fail-closed behavior: non-zero return, deny/error verdict, no plan/output artifact promotion, and no execution-leakage markers.

3. For documentation/comment recommendations, make the comment testable.
   - Add a source-level regression that extracts the helper block and asserts phrases like `test-harness-only path translation` and `must not be mirrored into runtime code`.
   - Run it before adding the comment so RED is real.
   - Add only the minimal comment needed to pass.

4. Verify adjacent safety boundaries.
   - Run focused new tests.
   - Run the full suite for the touched harness.
   - Run adjacent suites that cover the producer, consumer, and policy boundary.
   - Run full project unittest discovery when affordable.
   - Run static diff checks and an added-line scan for sensitive or target-touching vocabulary.
   - Run the project review wrapper if present.

5. Update handoff compactly.
   - Record the review recommendation closure in accepted changes.
   - Update the active strategy queue so the completed follow-up is no longer listed as pending.
   - Preserve explicit boundary language: tests/comment/handoff only; no live target, scanner/module execution, runtime bridge, scope/config, credentials, scheduler, deployment, billing, or production changes.

## Pitfalls

- Do not treat a copied artifact path helper as permission to build an auto-bridge. The helper is a test harness convenience only.
- Do not only assert that a displayed hash equals the current copied file. Add a negative mutation case that proves tampered bytes are denied.
- Do not leave completed review recommendations queued as future work in the active strategy file.
- Avoid adding runtime hash-pinning logic in a T2 follow-up unless the approved scope explicitly allows runtime changes.
