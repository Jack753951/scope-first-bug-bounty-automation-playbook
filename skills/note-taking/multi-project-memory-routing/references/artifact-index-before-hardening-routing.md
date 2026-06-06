> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Artifact Index Before Engineering Hardening Routing

Use this pattern when a repo has many handoff, worker, evidence, schema, queue, and debug artifacts and the user wants to know whether it is ready for the next engineering-hardening slice.

## Trigger signals

- Git status or handoff inventory is noisy, but many files are legitimate project artifacts rather than trash.
- The next proposed work depends on workers reliably finding current navigation, strategy, schemas, queues, evidence, and validation artifacts.
- The user prefers recoverable cleanup and audit-backed role division rather than aggressive deletion.
- A context-compacted session leaves only a final cleanup summary, so future agents need a compact repo-local index before continuing.

## Routing rule

Treat the work as project-local governance, not global Hermes memory and not a new narrow skill.

- Repo handoff/navigation: create or update a compact artifact index that classifies active, reference, superseded, local-only, ignored, operator-owned, and unverified/quarantined files.
- Obsidian project namespace: store long-term rationale if the classification changes strategy or review behavior.
- Hermes memory: at most a compact signpost about the project's memory location; do not save file lists or validation snapshots globally.
- Skills: keep only this reusable pattern here.

## Recommended sequence

1. Re-anchor on the latest user request if a compaction summary is present; do not replay stale side-effect tasks.
2. Inspect existing project navigation/handoff policy before deleting or moving anything.
3. Separate artifacts into at least these classes:
   - active-entrypoint / active-navigation
   - active-engineering substrate
   - active-lane-state or machine state
   - local-evidence-reference
   - target-lane-reference
   - historical-reference
   - cleanup-record
   - ignored-local or transient debug
   - operator-owned / never mutate without approval
   - unverified-current-intel / quarantine until primary-source checked
4. Prefer moving or quarantining over deletion unless the file is clearly transient/debug/cache; use recoverable deletion for local-only trash when available.
5. Add the new index to the main navigation and active strategy queue so workers have an obvious entrypoint.
6. Update the accepted-change log append/prepend-only with the classification and cleanup boundary.
7. Only after the index is wired in, run the project's focused validation/review checks needed to justify the next hardening slice.

## Verification

- Main navigation points to the artifact index.
- Active queue or equivalent project route includes the artifact index as a required context read.
- Accepted changes records what moved, what was quarantined, and what was intentionally not touched.
- Validation passes for affected scripts/schemas/review, and whitespace/diff checks are clean where applicable.
- Chat summary says whether the repo is ready for the next engineering-hardening slice and distinguishes remaining uncommitted artifacts from garbage.

## Pitfalls

- Do not equate a large git status with junk; many files may be active engineering substrate.
- Do not put raw targets, scans, loot, evidence payloads, or private scope into global memory or this skill.
- Do not let an artifact index become a full project database; it should point to project truth, not duplicate it.
- Do not treat unverified CVE/advisory/current-intel drafts as operational truth; quarantine and require fresh primary-source verification before use.
