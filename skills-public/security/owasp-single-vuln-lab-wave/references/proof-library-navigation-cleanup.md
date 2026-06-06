> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Proof library navigation cleanup after verified lab waves

Use this reference after a session accumulates multiple verified/candidate local-lab proof waves and the handoff/bundle/artifact layer starts to become hard to navigate. The goal is not to delete history; it is to add a short, current map that future agents can use before starting the next vulnerability wave.

## Trigger signals

Run this cleanup when any of these are true:

- Several proof waves are now verified in one session or day.
- The operator says navigation/handoffs/bundles are getting too large or hard to follow.
- A previously blocked/deferred lane has been upgraded to verified, so old navigation now points to stale status.
- `active_strategy_queue.md` or current navigation still says a lane is next even though the lane was just completed.
- There are multiple bundles for related evidence classes such as callback, XSS runtime, file read/path traversal/XXE, auth/session, injection, upload, and exposure triage.

## Cleanup outputs

Prefer a small index file in the repo handoff layer, for example:

```text
handoff/proof_library_index_<date>.md
```

It should group proof patterns by evidence class, not by chronology. Useful groups:

1. true attacker callback evidence;
2. browser runtime XSS safe-marker proof;
3. file read / path traversal / XXE safe-marker proof;
4. auth/session/JWT/access-control proof;
5. injection and server-side execution proof;
6. upload and exposure triage;
7. candidate / attempted-not-verified shelf.

For each row, include:

```text
Pattern
Status
Target
Bundle / handoff
Artifact root
Minimum evidence shape
```

Also include a `What not to do next` section so future sessions do not jump to public targets, broad scanners, or governance/importer work just because several local proofs are now verified.

## Navigation files to update

After writing the proof index, update the current navigation layer so future agents find it first:

- `handoff/current_navigation.md`
- `handoff/active_strategy_queue.md`
- `handoff/vulnerability_test_inventory_<date>.md` when present
- `handoff/accepted_changes.md`
- Obsidian project note/index for Cybersec Lab

Do not rely on chat memory alone. Repo handoff is the engineering truth; Obsidian is strategy/methodology memory; global memory should stay compact and cross-project only.

## Next-lane reprioritization

After a high-value proof such as SSRF true-attacker callback is verified, remove it from the "next lane" list. Prefer this order:

1. evidence packet consolidation / report-readiness rehearsal for one already verified proof;
2. dedicated rerun for any important proof still buried inside a multi-vulnerability artifact family;
3. one second-surface safe-marker target to generalize a proof pattern.

Do not keep running new vulnerabilities just because the lab is working. A proof library that is hard to navigate causes future agents to duplicate work or mislabel stale candidates.

## Verification

Use a lightweight consistency check after writing the index: confirm the new index and every updated navigation file mentions the index path, the reprioritized next lanes, and any lane status change from blocked/deferred to verified. This is documentation verification only; do not run target-touching commands for a navigation cleanup.
