> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Cybersec Lab Current Navigation Cleanup Pattern

Use this reference when a cybersecurity workspace has accumulated long handoffs, many bundles/artifacts, or route drift, and the user wants the project to become easier to navigate before starting another vulnerability wave.

## Trigger signals

- The user says the project is getting hard to navigate, handoffs are too long, or agents may not know the real current route.
- The active strategy queue has become a history dump instead of a short navigation layer.
- A lab route changed recently, such as replacing a broken attacker VM with a clean clone/snapshot.
- The user wants proof quality and local-lab capability fixed before moving to public/real bug bounty targets.
- A previous session misread another project’s handoff because the working directory was wrong.

## Safety boundary

Treat this as documentation/handoff cleanup only unless the user explicitly asks for a proof wave.

Do not:

- change VM networking or snapshots;
- open NAT;
- run scanners, exploits, callbacks, fuzzers, or target-touching scripts;
- edit scope/config to authorize public targets;
- handle credentials, loot, tokens, or private scope;
- submit reports or activate scheduler/CI.

## Workflow

1. Confirm the correct project root first.
   - On Windows, verify the repo path explicitly, e.g. `<user-home>`.
   - Do not infer Cybersec Lab state from a different project’s cwd or handoff.

2. Inspect current authority layers.
   - `.hermes.md` / `AGENTS.md` for binding project rules.
   - `handoff/active_strategy_queue.md` for current lane/navigation.
   - `handoff/accepted_changes.md` for accepted route and engineering truth.
   - project Obsidian namespace/index for long-term strategy/rationale.
   - `session_search` only as recall; verify against files before acting.

3. Archive the old long queue before replacing it.
   - Example archive path: `handoff/archive/active_strategy_queue_pre_navigation_cleanup_<YYYYMMDD>.md`.
   - Do not delete history; make the active queue short and navigational.

4. Create or refresh `handoff/current_navigation.md`.
   Include:
   - current default route;
   - current active lab targets;
   - top 3 next valuable vulnerability lanes;
   - parked/deprecated lanes;
   - recovery/snapshot rules;
   - artifact location convention;
   - evidence packet minimum shape;
   - memory/Obsidian routing rule;
   - freshness/authority rule.

5. Create or refresh `handoff/lab_safety_contract.md`.
   Include:
   - default attacker/victim route;
   - local-lab-only default scope;
   - host-only/NAT rules;
   - local-lab learning allowance;
   - proof quality rules;
   - evidence hygiene;
   - recovery rules;
   - promotion/activation gates.

6. Rewrite `handoff/active_strategy_queue.md` as a short current map.
   Keep only:
   - long-term goal;
   - current phase;
   - current default route;
   - active lab targets;
   - top 3 next lanes;
   - secondary lanes;
   - parked/deprecated lanes;
   - hard boundary;
   - pointers to current navigation/safety/accepted changes.

7. Record the change append/prepend-style in `handoff/accepted_changes.md`.
   State explicitly that the slice was documentation/handoff-only and did not touch VM/network/scanner/exploit/scope/credential/submission/scheduler surfaces.

8. Update the Cybersec Lab Obsidian project note/index with a short strategy/navigation summary.
   Keep raw sensitive evidence, raw scans, credentials, loot, tokens, private scope, exploit dumps, and hashes out of broad Obsidian notes.

9. Verify without target-touching.
   Useful checks:
   - markdown files exist and are readable;
   - archive exists;
   - `.agent.lock` is absent;
   - `git diff --check` has no new whitespace errors;
   - status output distinguishes new cleanup files from pre-existing dirty/untracked project state.

## Recommended navigation content

Default next valuable lanes for a local-lab proof-quality phase:

1. Attacker callback proof pattern hardening.
   - Reuse an already verified true attacker-side callback as the quality bar.
   - Require truthful source/context labeling, unique marker, listener log, pre/post health, and cleanup.

2. Browser runtime XSS proof pattern.
   - Prove execution in the correct browser/origin/session context, not just reflection.
   - Prefer safe markers, DOM/console evidence, and session/context labels.

3. File read / path traversal / XXE safe-marker proof pattern.
   - Use lab-owned marker files or bounded fixtures.
   - Avoid unnecessary habits around sensitive system-file proof.

## Evidence packet minimum shape

Use this for one-vulnerability proof waves after navigation cleanup:

```text
Target:
Vulnerability class:
Authorized scope:
Route/tool:
Preconditions:
Exploit/probe path:
Evidence:
Impact:
Controls / false-positive boundary:
Cleanup:
Rerun commands:
Report-readiness:
Project benefit:
New/changed artifacts:
```

## Pitfalls

- Do not let `active_strategy_queue.md` become a full historical ledger. Archive history and keep the active queue short.
- Do not treat navigation cleanup as permission to run a new proof wave.
- Do not promote project-specific route/IP/snapshot facts into global Hermes memory except as compact signposts.
- Do not collapse local-lab learning gates into public-target authorization. Public/real targets still require explicit program scope/rules and operator approval.
