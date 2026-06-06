> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Upstream planning gates: Claude Code review + bounded implementation

Use this when working in an upstream topic-intelligence repo that feeds a downstream media generator/publisher, especially when the user explicitly says Claude Code usage is plentiful or asks to use Claude Code more.

## Pattern

1. Verify Claude Code routing without exposing secrets:
   - `claude auth status --text 2>&1 | sed -E 's/(sk-ant-[A-Za-z0-9_-]+)/[REDACTED]/g'`
   - Prefer Pro/Max OAuth Claude Code for heavy review/implementation work when available.
2. Run two independent read-only Claude Code reviews before implementation:
   - Engineering review: changed/new modules, CLI, tests, fail-closed logic, validation gaps.
   - Product/content/safety review: whether the current planning gate is the right next gate, missing human-review inputs, no-go boundaries, strongest next artifact.
3. Ask Claude Code to implement only one bounded planning-only rung using strict TDD:
   - Write tests first and verify RED.
   - Implement minimal code.
   - Run focused tests and full suite.
   - Do not commit unless explicitly requested.
4. Hermes must verify locally after Claude Code self-report:
   - Run the full test suite and compile/lint commands relevant to the repo.
   - Inspect generated JSON/Markdown artifacts when a CLI produced them.
   - Confirm no downstream runtime/publish actions occurred.
5. Report route/model transparently:
   - State `Claude Code CLI` as route/tool.
   - Include visible Claude model from JSON output (for example `claude-opus-4-7`) when available.
   - If the main Hermes runtime model is not exposed in an artifact, say so instead of inventing it.

## Good next-rung examples

For a chain ending at a downstream concept-review gate, the next bounded implementation can be a `concept_review_decision` recorder with enumerated decisions:

- approve only for the next named local/planning packet, e.g. `user_gated_local_only_concept_packet = YES_SEPARATE_GATE_ONLY`.
- request revision of the current gate.
- reject/return to topic discovery.

The decision recorder should fail closed on source-status mismatch, channel mismatch, unknown decision, and missing provenance/main-project alignment. It should generate JSON + Markdown only.

## No-go boundaries to repeat in prompts

For media-generator downstream projects, every Claude Code prompt must explicitly forbid:

- calling downstream runtime commands such as create/draft/loop/remake.
- render, upload, schedule, destination/privacy changes.
- OAuth/token/client-secret access or edits.
- channel config edits.
- competitor/social asset reuse or frame/thumbnail downloads as source media.
- copying Reddit/Shorts/social posts verbatim into hooks, premise, or scripts.

## Pitfalls

- Do not accept Claude Code's self-reported success without Hermes rerunning tests and checking artifacts.
- Do not broaden a planning-gate approval into script/render/upload authorization; approval should open only the next named gate.
- Do not bury reviewer identity/model metadata only in chat; put it in decision artifacts when the generator supports it.
- If Claude Code hits max turns, inspect the actual workspace state and continue with a narrower task instead of rerunning the same broad prompt.
