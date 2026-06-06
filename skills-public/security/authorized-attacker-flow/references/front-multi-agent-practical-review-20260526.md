> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Front multi-agent practical review pattern (2026-05-26)

Use this as a concrete reference when a live-bounty candidate has become tempting but still needs the hard role-separated gate before anything beyond passive UI/docs mapping.

## Scenario

- Program/lane: Front / `front-shared-inbox-object-permission`.
- Candidate looked high-value because shared inbox permissions are core product surface and map to tenant/user/data-boundary impact.
- Current state was post-auth passive mapping paused at external channel-connect gate.
- The operator asked to test the new multi-agent workflow in practice.

## Route pattern that worked

1. Build a compact memory-sync packet for workers.
   - Include `.hermes.md`, current navigation/queue/artifact index, recent accepted changes, Obsidian bridge, program scope, lane state, candidate packet, exact safety boundary, and stop-before list.
   - Exclude secrets, OTPs, phone numbers, cookies, tokens, API keys, verification links, customer data, and raw loot.
2. Invoke Claude Code/Cowork for tactical/boundary/evidence roles.
   - Treat one Claude process that covers several roles as one Claude perspective, not three independent agents.
   - If the CLI wrapper returns `error_max_turns` but still streams useful findings, preserve raw output and record the caveat; do not count it as a clean PASS.
3. Invoke Codex for deterministic/skeptical review.
   - Require it to check candidate status, lane-state `worker_route_status`, scope/safety boundary, and evidence gaps.
4. Hermes synthesis decides; workers do not grant authorization.
5. Update lane state with structured route evidence and keep `passive_only_until_complete: true` unless the synthesis explicitly approves a bounded next step.
6. Run validation: JSON parser, diff check, and `bash ./bin/hermes review` when repo files changed.

## Output-normalization lesson

Claude Code JSON output can contain a valid result header followed by streamed text if the process times out or hits max turns. When that happens:

- Preserve the original file as `*.raw.txt`.
- Normalize the advertised JSON artifact into valid JSON with fields such as:
  - `source_raw_artifact`
  - `normalization_reason`
  - `cli_result_header`
  - `worker_identity`
  - `verdict`
  - `caveat`
  - `key_findings`
  - `raw_output_tail`
- Record the wrapper error (`error_max_turns`, `terminal_reason`, session id) as evidence, not as a hard tool failure.
- Do not advance execution on a normalized/partial artifact unless the synthesis and the other worker route support it.

## Practical synthesis outcome

Both routes agreed the candidate was useful but not ready:

- Claude: `REQUEST_CHANGES`.
- Codex: `BLOCK`.
- Hermes decision: `BLOCK_BEYOND_PASSIVE_MAPPING`.

Allowed next action remained passive UI/docs mapping only. Blocked actions included object creation, invites, role changes, token/API calls, workflow activation, channel connection, customer/non-owned data, scanner/fuzzer/DAST, exploit steps, and report submission.

## Evidence gaps to look for on similar SaaS lanes

- No Account B / teammate identity.
- No second tenant.
- No shared-inbox UI inventory or role/permission matrix.
- No expected-vs-observed positive/negative control protocol.
- No named owned test object label before creation.
- No redaction plan for screenshots and request snippets.
- No explicit operator approval for state-changing owned test objects.
- No scope freshness check if program scope expiry is near.

## Durable rule of thumb

A strong attacker hypothesis is not enough. The multi-agent gate is doing its job when it preserves the hypothesis while blocking premature proof execution until owned controls, redaction, scope, and operator approval exist.
