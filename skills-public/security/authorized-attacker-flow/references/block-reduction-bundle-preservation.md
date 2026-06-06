> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# BLOCK reduction + bundle preservation pattern

Use when a multi-agent review blocks proof execution but the user wants to keep testing safely and explicitly says not to exclude useful bundles.

## Pattern

1. Split the BLOCK into two buckets:
   - Non-target-touching blockers: can be resolved now with boundary tightening, docs/reference mapping, evidence plans, expected matrices, and lane-state cleanup.
   - Operator-gated proof blockers: remain blocked until explicit approval or new owned resources exist.
2. Do not convert a BLOCK directly into `bounded_executable` just because some paperwork improved. Prefer a middle state such as `passive_mapping_extended_not_proof_ready`.
3. Create a bundle map that preserves related hypothesis families. Each bundle should have:
   - stable bundle id;
   - hypothesis family;
   - expected boundary;
   - future proof gate;
   - current state (`passive-only`, `operator-gated`, `blocked-preserve`, etc.).
4. Keep all potentially useful bundles unless there is an explicit evidence/scope/safety reason to park them. Parking is not deletion: record rationale and future unlock condition.
5. Continue only the least-active allowed work: passive UI/docs mapping, redacted empty-state screenshots, and public reference review.
6. Stop before Save/Create/Invite/Connect/Generate token/API call/Activate/Send/Import/Upload/Delete or any non-owned/customer data.
7. Sync non-sensitive results into lane state, accepted changes, artifact index/active queue when relevant, and the project note/Obsidian bridge.

## Example status transition

`front_specific_multi_agent_review_completed_blocked` -> `block_reduced_passive_mapping_allowed_not_proof_ready`

This means:

- proof is still blocked;
- passive mapping is allowed;
- bundle preservation is explicit;
- remaining proof blockers are listed separately.
