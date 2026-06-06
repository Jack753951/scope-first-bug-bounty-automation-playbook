> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Sibling Project Structure Sync Routing

Use this when the user asks to inspect a cleaned clone/sibling repo and optimize the main repo from its structure.

## Pattern

1. Treat the sibling repo as a reference implementation, not authority.
2. Read the sibling's active authority layers first: root safety/README, handoff index, current navigation, active queue, artifact index, strategy/current direction, and policy index.
3. Read the main repo's matching authority layers and live machine-readable state before editing.
4. Extract reusable structure patterns, not raw project decisions:
   - compact root safety/hard-stop contract;
   - short README/read order;
   - one handoff index;
   - compact current navigation;
   - compact active strategy queue;
   - compact artifact index;
   - one `docs/strategy/CURRENT.md` active direction;
   - explicit archive/reference boundary.
5. Preserve the main repo's active direction, driver model, and live lane state unless the user explicitly asks to adopt the sibling's decisions.
6. When sibling and main lane states differ, document the discrepancy and create a separate reconciliation follow-up instead of silently mutating machine-readable lane JSON.
7. Update accepted-change/audit logs with the structural adoption boundary and state that no target-touching work was performed.
8. Validate locally with focused checks: path existence, Markdown/read-order coherence, JSON validation for machine state, `git diff --check`, and syntax checks for scripts if touched.

## Do not copy

- Sibling repo-specific target decisions, KILL/PARK/no-finding dispositions, operator actions, credentials, private scope, or evidence.
- A different driver model (for example single-agent vs Hermes-led multi-agent) unless it is explicitly the new desired project shape.
- Archived/historical files as active policy.

## Good outcome

The main repo gains a leaner active-truth surface while preserving its own authority layers and machine-readable state. Any substantive lane/state decision becomes an explicit separate task, not a side effect of cleanup.
