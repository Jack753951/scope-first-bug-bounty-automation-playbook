> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Cybersec Lab Navigation Cleanup Routing

Use this pattern when a cybersecurity lab has gained capability quickly but navigation artifacts are expanding faster than the active direction is staying legible.

## Trigger signals

- The user says the lab is now recoverable/re-runnable but handoff, bundles, queues, or artifacts are becoming hard to navigate.
- `active_strategy_queue.md`, handoff files, proof bundles, or untracked artifacts are long enough that future agents may not know the next default lane.
- The user explicitly dissents against moving too quickly from local lab proof waves to public bug bounty / real targets.
- The project has new stable infrastructure, snapshots, or default attack-machine route and needs that baseline reflected in navigation before more vuln work.

## Routing rule

Treat the cleanup as project-local governance and navigation, not global memory and not a new one-off skill.

- Repo handoff/navigation: current route, active targets, next lanes, deprecated lanes, snapshot/recovery rules, artifact conventions, validation state.
- Obsidian project namespace: long-term rationale, methodology direction, and why local proof patterns remain the current focus.
- Hermes global memory: at most a compact pointer if the routing principle affects future cross-session behavior.
- Skills: only the reusable pattern for preventing lab-navigation drift belongs here.

## Cleanup shape

Create or update a short current-navigation artifact before starting another vulnerability lane. It should answer:

1. Current default route / attack machine.
2. Current active local lab targets.
3. Top 3 next valuable vulnerability lanes.
4. Deprecated or paused lanes and why.
5. Recovery/snapshot rules.
6. Artifact location and naming convention.
7. Obsidian memory-routing rule.
8. Public-target readiness gate.

Keep the artifact compact. Link to long proof bundles instead of copying them.

## Cybersecurity-specific gate

Do not treat a stable local lab as approval to pivot to public targets. First stabilize local evidence patterns such as:

- attacker callback proof pattern;
- browser-runtime XSS proof;
- file-read/path-traversal safe-marker proof;
- auth/session handling;
- evidence packet format;
- report-readiness gate.

When these are not yet fixed, recommend one or two high-quality local single-vulnerability proof waves plus navigation cleanup, not broad public recon.

## Verification

- The active navigation file has a single obvious default path.
- Old lanes are marked `deprecated`, `paused`, `reference`, or `superseded` rather than deleted silently.
- Artifact conventions distinguish committed proof libraries from ignored runtime/raw cache.
- Obsidian index points to the active cybersec lab direction and not only historical notes.
- Chat summary labels uncertainty and states that no public-target authorization was inferred.
