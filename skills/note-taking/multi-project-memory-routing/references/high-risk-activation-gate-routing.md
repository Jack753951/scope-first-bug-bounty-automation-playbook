> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# High-Risk Activation Gate Routing

Use this pattern when a project asks to move from offline/internal readiness into live activation, scheduling, upload, publication, OAuth, destination, default-privacy, or other production-affecting behavior.

## Core distinction

Treat the user's question as opening an activation gate, not as implicit permission to execute the side effect.

Examples:

- "Can we put this channel on schedule today?" means: run safe preflight, identify blockers, write the approval gate, and ask for exact confirmation before mutation/upload/scheduling.
- "Is this ready to upload?" means: verify readiness and list remaining gates; do not upload unless the user explicitly approves the exact artifact, destination, privacy, and scope.
- "After Claude visionreview, upload/schedule these channels more aggressively so we get learning data" means: update cadence strategy and make positive-reviewed candidates flow toward exact-artifact canary gates, but still do not mutate upload/schedule/privacy without the project’s exact-scope approval step. See `ri<api-key-redacted>.md`.

## Risk-tier note

For media automation projects, do not apply publication-grade process to every local-only experiment. Local batches can be fast and lightly logged; high-risk actions remain strict. The practical goal is to gather enough live learning data without weakening OAuth, destination, privacy, scheduler, or exact-artifact gates.

## Where records belong

- Repo handoff: live preflight evidence, blockers, exact artifacts, approved/blocked actions, validation results.
- Obsidian: longer-term strategy or decision rationale if the activation changes project direction.
- Hermes durable memory: only compact cross-project preferences or stable pointers, not dated activation state.
- Skill references: reusable gate pattern and session-specific examples without secrets.

## Safe activation-gate flow

1. Inspect the project-local authority files first (`.hermes.md`, active queue, accepted changes, existing gate packets).
2. Run only safe/read-only preflight checks needed to answer feasibility.
3. If an auth/destination check may refresh a token, say so and never print/copy token contents.
4. Distinguish technical feasibility from authorization.
5. Write a repo-local gate packet with:
   - requested live action,
   - current gate evidence,
   - hard blockers,
   - feasible routes,
   - exact approval wording,
   - explicit list of actions not performed.
6. Update the active routing index and accepted changes so future workers do not mistake discussion readiness for execution approval.
7. Validate the docs/config state according to project norm.
8. Final response should give a concise yes/no/conditional answer plus the exact next approval needed.

## Pitfalls

- Do not treat "today can we..." as approval to schedule/upload/publish.
- Do not use a generic create/loop path as a shortcut when a reviewed artifact exists; it may generate a different output.
- Do not silently mutate scheduler/default privacy/destination/render-ack/engine defaults while preparing a gate.
- Do not store dated gate status in global memory.
- Do not copy secrets or token contents into handoff, Obsidian, or chat.
