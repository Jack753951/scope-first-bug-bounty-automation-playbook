> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Cybersec Fixture Review Fallback After Claude Code Max-Turn

Use when a Hermes-style cybersec wrapper (`hermes claude-impl`) is asked to perform a read-only/design or implementation review, exits with `error_max_turns`, and does not produce the requested review artifact.

## Recovery pattern

1. Preserve the raw run metadata/log paths in the handoff. Do not treat the wrapper exit as a project verdict.
2. Inspect whether the requested artifact exists and whether it contains a real verdict. If it is missing/empty, mark the Claude Code review attempt as inconclusive, not failed implementation.
3. Create a narrower review packet:
   - exact verdict vocabulary expected;
   - exact files in scope;
   - explicit forbidden behaviors;
   - observed validation commands/results;
   - prior blocker(s), if this is follow-up.
4. Run an independent read-only follow-up review with a small packet and no code modification authority.
5. If the review returns `REQUEST_CHANGES`, convert each blocker into a focused regression test before patching, then run a follow-up review or record the resolved blocker in a separate review artifact.
6. Final handoff should distinguish:
   - wrapper-level `error_max_turns` metadata;
   - independent review verdict;
   - local Hermes verification result.

## Pitfalls

- Do not re-run the same broad Claude Code review prompt repeatedly. Broad repo context can burn turns without producing the requested artifact.
- Do not accept a missing `handoff/*review.md` just because raw JSON exists. The raw JSON is usage metadata, not an implementation review.
- In noisy working trees, final acceptance should attribute the slice by an explicit file list rather than raw `git status` alone.
