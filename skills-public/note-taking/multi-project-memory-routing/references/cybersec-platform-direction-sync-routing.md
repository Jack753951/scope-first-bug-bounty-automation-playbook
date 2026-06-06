> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Cybersec Platform Direction Sync Routing

Use when the Cybersec Lab operator states or corrects the project’s future direction, especially when they ask to adjust policy, global memory, Obsidian/project memory, long-term goals, or engineering truth.

## Trigger

The operator says the next message is the project future direction, north star, long-term goal, structural direction, multi-agent policy, recurring engineering cadence, or says that similar memories/policies should be superseded by the current conversation.

## Critical pitfall

Do not start writing memory or editing files while the operator is still saying “等等”, “還沒說完”, or otherwise indicating the direction is incomplete. Acknowledge and wait. Only act after the full direction is delivered or the operator clearly authorizes applying it.

## Routing pattern

1. Treat the latest explicit operator direction as authority over older global memories, repo handoff, and Obsidian strategy notes.
2. First update only compact global Hermes memory signposts. Do not store long strategy, target details, scan output, secrets, private scope/rules, or run logs in global memory.
3. Put detailed durable project direction in the project authority layers:
   - `.hermes.md` for binding project/worker operating contract.
   - `handoff/current_navigation.md` for current operational truth and safety boundaries.
   - `handoff/active_strategy_queue.md` for active priorities and next engineering lanes.
   - `notes/obsidian_projects/Cybersec Lab.md` for long-term rationale/strategy synthesis.
   - `handoff/accepted_changes.md` as a short append/prepend-only record of the governance change.
4. Preserve safety semantics when translating user authorization:
   - In-scope testing may include aggressive or attack-shaped scripts only after exact bug bounty scope and program rules allow the target and technique.
   - Execution remains bounded proof-only.
   - Stop before internal/customer/non-owned data browsing, download, modification, or exfiltration.
   - Keep OTP/CAPTCHA/email/SMS verification and final submission human-gated unless explicitly changed.
5. If the direction requires external strong-agent participation, encode a context-sync requirement before invocation: `.hermes.md`, current navigation, active queue, artifact index, Obsidian bridge, accepted changes, relevant program state, and stop-before rules.
6. Run a lightweight consistency check after edits: search active authority files for superseded phrases such as `first-bounty-only`, `first reportable`, or old passive-only language that conflicts with the new direction. Mark historical notes as superseded/reference rather than deleting them unless the operator asked for deletion.

## Cybersec-specific direction shape captured 2026-05-28

- Active goal: automated, multi-agent collaborative bug bounty platform and capability library.
- Hermes role: project owner, task decomposer, scheduler, worker router, verifier, and safety gate.
- Multi-agent policy: external strong agents should be used frequently for unclear direction, dissent, architecture, tactic selection, recurring automation, target-pattern fit, evidence/reporting, implementation review, and safety-boundary analysis.
- Practical dual track:
  1. Recurring latest-vulnerability/intel/recon work → local lab proof → reusable bundle/library.
  2. Multi-agent matching of proven patterns to suitable in-scope targets → bounded proof-only testing.
- Recurring cadence target: minute-level CT/scope/CVE-PoC alerts; hourly differential recon; daily passive inventory/NVD/CISA/nuclei sweeps; weekly deep discovery/JS/params/version/policy/disclosed mining; monthly inventory/strategy/metrics review.
- Structural priorities: contract alignment, platform core migration, evidence-to-report pipeline, detector harness, artifact/path integrity, repo hygiene, environment validation profiles, reporting automation, auth/session state, submission tracking, hourly diff recon, disclosed-report mining, mobile static analysis, vendor advisory diffing.
- Avoid: web UI, SaaS/multi-tenant, distributed scanner, custom vulnerability DB, custom ML, and reimplementing mature tools unless strategy changes.
