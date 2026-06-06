> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Proof library and evidence-packet closeout — Cybersec Lab pattern

Use this reference after several local-lab proof waves have produced verified/candidate bundles and artifacts. The goal is to prevent handoff/navigation sprawl and convert the strongest proof into a reusable one-vulnerability evidence packet without running new target-touching tests.

## Trigger signals

Run this closeout when any of these are true:

- Multiple verified local-lab proof patterns now exist and future agents may not know which route to use.
- `handoff/active_strategy_queue.md`, bundles, artifacts, or Obsidian notes have grown enough that navigation is harder than execution.
- A strong proof has complete artifacts but is not yet in the standard evidence-packet shape.
- The next best step is evidence quality/report-readiness rehearsal rather than another vulnerability trigger.

## Preferred sequence

1. Create or update a short proof-library index in repo handoff, for example `handoff/proof_library_index_<date>.md`.
2. Group proof patterns by evidence type rather than by run date:
   - true attacker callback;
   - browser-runtime XSS;
   - file read / path traversal / XXE safe-marker;
   - auth/session/JWT/access control;
   - injection / server-side execution;
   - upload/exposure triage;
   - candidate and attempted-not-verified shelves.
3. For each pattern, record the target, status, bundle/handoff path, artifact root, and minimum evidence shape.
4. Update the current navigation files (`current_navigation`, active queue/inventory, accepted changes) so future agents start from the index rather than old long queues.
5. Choose one strong verified proof and convert it into a one-vulnerability evidence packet using the existing template or equivalent headings.
6. After packetization, move that lane out of “next action” and promote the next highest-value lane.
7. Update Obsidian with strategy/navigation synthesis only; keep raw evidence, payloads, callbacks, and sensitive details in repo artifacts/handoff.
8. Verify by checking that every updated navigation file points to the new packet/index and that the old next-lane recommendation no longer says to do already-completed work.

## Evidence packet minimum sections

Use these headings for a polished one-vulnerability local-lab packet:

- Reviewer identity
- Target
- Vulnerability class
- Authorized scope
- Route/tool
- Preconditions
- Exploit/probe path
- Evidence
- Impact
- Controls / false-positive boundary
- Cleanup
- Rerun commands
- Report-readiness
- 對專案有什麼幫助
- 新增/更新了什麼

## Callback-proof packet notes

For SSRF/XXE/deserialization/command-injection callback packets, explicitly separate:

- listener reachability precheck, and
- actual vulnerability-trigger callback.

Do not count a precheck as impact. A verified callback claim needs a unique marker, source IP/context, trigger response or equivalent, authoritative listener log, pre/post health, cleanup, and a report-readiness decision.

## Common pitfall

Do not keep “evidence packet consolidation” as the top next lane after the packet is completed. Update the proof library, active queue, inventory, and Obsidian so the next lane advances, for example to a dedicated rerun or a second safe-marker target.
