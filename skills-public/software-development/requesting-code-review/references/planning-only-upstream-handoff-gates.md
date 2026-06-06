> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Planning-only upstream handoff gates

Use this when reviewing a helper/upstream project that produces recommendations, candidate packets, handoff manifests, or concept/design gates for a more sensitive runtime project.

## Core pattern

1. Keep the upstream tool planning-only by contract:
   - no runtime invocation of the downstream app,
   - no render/upload/publish/schedule action,
   - no OAuth/token/secret/channel/default-privacy edits,
   - no competitor/social asset reuse unless explicitly approved.
2. Validate both behavior and artifact wording. Handoff files should clearly say they do not authorize runtime/publication actions.
3. Treat identifiers used in filesystem paths as security-sensitive input even when they look like friendly labels such as `--channel`.
4. Validate labels against a known closed registry before path construction, scoring, market-pattern generation, handoff selection, or downstream routing.
5. Reject path-like labels fail-closed: absolute paths, `/`, `\`, `.`, `..`, or strings containing `..` should not be accepted as channel/profile names.
6. After constructing a path from a validated label, resolve it and assert it remains under the expected root before reading local history/database files.
7. Handoff selection should skip or reject unknown channels rather than forwarding them to the downstream project.
8. Add tests at both levels when practical:
   - unit/path helper tests for unknown and traversal-like labels,
   - CLI or integration negative tests proving bad labels fail before database/runtime access.

## Independent review prompts

Ask the reviewer to focus on:

- registry alignment with the downstream project,
- fail-closed unknown-channel behavior,
- path traversal via user-facing labels,
- planning-only boundary preservation,
- tests proving no runtime/upload/scheduler/OAuth side effects.

## Good verdict wording

Record both the first review and the follow-up if blockers were found:

- initial route/model/provider and `REQUEST_CHANGES` blockers,
- exact fixes applied,
- follow-up route/model/provider and `PASS`,
- validation commands and test counts,
- explicit safety boundary.
