> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Media Pipeline Proof-Card TDD Pattern

Use this reference when a media automation pipeline has a visual/metadata regression that must be fixed without immediately rerendering or uploading.

## Situation captured

A YouTube Shorts automation flow produced a technically valid local draft, but visual QA found that the promised proof object was not readable on-screen. The fix needed a safe code rung before any rerender/upload gate.

## Durable pattern

1. Keep the phase boundary explicit:
   - planning/review only,
   - TDD code implementation only,
   - rerender only,
   - upload/canary only,
   - publish only.
   Do not silently combine these gates.

2. Write RED tests against deterministic specs, not against a full video render:
   - generated proof-card objects contain required labels/text,
   - generic fallback does not contain template placeholders,
   - overlay text survives the renderer's escaping helper,
   - card start times are monotonic and `end <= total`,
   - metadata profile labels are attached as review context only.

3. If the module imports optional provider/render dependencies at import time, keep tests local by stubbing only the optional imports needed for collection. The RED should then be the missing behavior, not missing local packages.

4. Implement the smallest GREEN path:
   - helper returning deterministic proof-card specs,
   - renderer loop over those specs,
   - remove placeholder footer text,
   - attach review-only media/profile labels before metadata writing.

5. Verify before committing the code rung:
   - focused pytest for the new regression tests,
   - adjacent existing tests around the touched surface,
   - `py_compile` for touched Python modules,
   - project validate command,
   - `.agent.lock` clear if the project uses a lock,
   - scoped `git diff --check`.

6. Treat the rerender as its own separate gate after the code rung:
   - run exactly one controlled local/private rerender from the constrained topic or approved input,
   - build a contact sheet plus `ffprobe` JSON,
   - inspect the visual result directly before claiming the proof object is fixed,
   - run a read-only creative/vision review when available, with no file-write or upload permissions,
   - record the local video path, metadata path, subtitles path, contact sheet, `ffprobe`, render QA verdict, visual verdict, and blocked actions in handoff.

7. If the rerender becomes `PRIVATE_CANARY_READY`, do not treat that as upload authorization. Create a separate preflight/approval packet first, including destination/OAuth channel verification, default privacy confirmation, and an explicit user upload/canary gate.

## Pitfalls

- Do not call a successful code fix a successful visual fix until a separately gated rerender and visual QA confirms it.
- Do not let `PRIVATE_CANARY_READY` collapse into an upload step. Private canary readiness means the next artifact is a preflight/approval packet; actual upload still needs explicit authorization and destination/OAuth verification.
- Do not encode upload/publish/schedule/privacy behavior into review-only metadata labels.
- Do not use real names, emails, addresses, companies, or screenshots for synthetic evidence cards.
- Do not preserve placeholder copy like `real story detail` in rendered overlays.
