> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Template / Review Packet TDD

Use this when the code change is a docs/template generator, periodic-review packet builder, prompt generator, or fallback template path.

## What to test first

Write RED tests against generated output, not just helper internals:

- Snapshot contains freshness/authority metadata.
- Snapshot contains project-specific review tiers or safety classes.
- Prompts include reviewer identity/model/runtime fields.
- Prompts include the final decision block or required output schema.
- Blank reviewer-output templates also include the same required blocks.
- Fallback generator output stays aligned with the primary generator when practical.

## Cycle

1. Build a tiny temporary project fixture with only safe files needed by the generator.
2. Monkeypatch filesystem/git helper calls only when necessary to avoid depending on local repo state.
3. Run the focused test and verify RED for the missing generated block/schema.
4. Implement the smallest generator/template change.
5. Run the focused test to GREEN.
6. Smoke-run the real packet builder with a non-production review date.
7. Read back representative generated files to verify the blocks appear in actual output.
8. Run project validation / diff hygiene if this is inside a repo workflow.

## Pitfalls

- Do not only test source strings if the generator has interpolation, fallback paths, or file-writing behavior. Verify generated output.
- Do not update the primary generator and forget fallback builders; future sessions may hit the fallback when a runtime is unavailable.
- Do not hardcode session-specific paths or dates except in isolated test fixtures.
- A review packet is frozen input. Tests should encourage explicit freshness and authority rules so stale packets do not override live handoff or code.
