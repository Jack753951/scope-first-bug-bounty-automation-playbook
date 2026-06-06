> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Cybersec Phase Direction / Closeout Reviews with Claude Code

Use this pattern for Hermes-style cybersecurity workspaces when a phase is at a boundary and the next choice is architectural, safety-related, or roadmap sequencing rather than implementation.

## When to use

- A completed offline/local milestone needs a closeout verdict before the next phase.
- A refactor looks attractive, but could centralize or hide safety gates.
- The next step may cross into schema promotion, runtime wiring, report drafting, platform adapters, or target-touching behavior.
- The user asks to continue project progress but the safest useful action is a design-only review.

## Pattern

1. Create a focused direction/closeout prompt under `handoff/`, e.g.:
   - `handoff/cowork_pX_direction_prompt.md`
   - `handoff/cowork_pX_closeout_prompt.md`
2. Convert it into `handoff/claude_code_task.md` for `hermes claude-impl`.
3. Make the task explicitly design-only / read-mostly.
4. Allow writing only the review result and wrapper result file, e.g.:
   - `handoff/cowork_pX_direction_review.md`
   - `handoff/cowork_pX_closeout_review.md`
   - `handoff/claude_code_result.md`
5. Require a small finite verdict vocabulary, such as:
   - `DEFER_REFACTOR_AND_CLOSE_PHASE_2`
   - `EXTRACT_MINIMAL_CORE_HELPER`
   - `ROUTE_BACK_FOR_SCOPE_CLARIFICATION`
   - `CLOSE_PHASE_2`
   - `CLOSE_WITH_CONDITIONS`
   - `DO_NOT_CLOSE_PHASE_2`
6. Run:
   - `HACKLAB=<user-home> ./bin/hermes claude-impl`
7. Read the review, wrapper summary, and usage JSON. Record useful run metadata (`num_turns`, `total_cost_usd`, run JSON path) in `accepted_changes.md` if the review is accepted.
8. Run local Hermes verification afterward:
   - `HACKLAB=<user-home> ./bin/hermes review`

## Safety boundary to include in prompts

The prompt should explicitly forbid:

- live scans, probes, scanners, fuzzers, exploit tooling, callbacks, OAST, proxy/pivot/tunnel behavior, and target-touching automation;
- network clients or target interaction;
- module execution, runner runtime wiring, recon integration, scheduler/CI hooks, platform adapters;
- schema promotion from trial schemas to stable contracts;
- confirmed/verified finding status promotion;
- report generation, report drafting, or report submission adapters;
- edits to `config/scope.txt`, loot, credentials, OAuth, scheduler/deployment/billing/production settings.

## Refactor-at-boundary pitfall

In safety-sensitive cybersec workflows, duplication can be safer than premature centralization. In the P2.24 review, repeated `LIVE_TARGET_FLAGS`, argument rejection, error payloads, and compact JSON emitters across offline consumers were deliberately left duplicated because each script's local safety posture was easy to review. A helper extraction should be deferred until a concrete trigger exists, such as:

- schema promotion;
- cross-consumer drift;
- a fifth stdin-only consumer;
- a third file-reading consumer;
- operator-approved live-target flag vocabulary changes.

If extraction is later approved, keep the helper narrow and pure. For example, `scripts/core/offline_consumer.py` may contain constants and pure payload/emit/argument-rejection helpers only. It must not add file I/O, subprocess, network, target fields, status promotion, report drafting, runner/recon integration, or any `ignore_live_flags` / `permissive_argv` parameter.

## Closeout review output shape

A closeout review should answer:

- whether the phase is ready to close;
- what value was demonstrated;
- safety boundary status;
- test/fixture quality;
- first next-phase slice;
- explicit deferrals / what not to build next;
- boundary locks requiring operator approval;
- revisit triggers for deferred refactors.

For Phase 2 of the cybersec workspace, the successful closeout verdict was `CLOSE_PHASE_2`; the first Phase 3 slice was curated near-real offline fixtures, not live scanning, report drafting, schema promotion, or platform integration.