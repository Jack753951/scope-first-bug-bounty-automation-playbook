> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Exact-Artifact Scheduled Canary Routing

Use this pattern when a media/automation project moves from local/internal review into a single scheduled private/public-eligible canary for a specific already-rendered artifact.

## Trigger

- User asks to schedule or advance the current best candidate after review.
- A prior worker/review has identified an exact local artifact as the strongest candidate.
- The action touches YouTube or another production platform, scheduler state, OAuth destination, privacy/publication timing, or channel identity.

## Routing

- Store exact artifact path, platform ID/URL, schedule time, validation outputs, and follow-up observation plan in repo handoff / accepted-change logs.
- Keep only the reusable procedure in skills.
- Do not save per-video IDs, titles, dates, or candidate rankings in global memory.
- Do not treat a canary scheduling request as approval for generic generation loops, broader uploads, public publication, cron/scheduler changes, OAuth changes, default privacy changes, deletions, or channel config rewrites.

## Procedure

1. Identify the exact already-rendered artifact from current project authority layers, not from memory alone.
2. Verify local safety/environment gates before touching the platform.
3. Verify exact-artifact QA for the same file that will be scheduled; do not substitute a similar render or rerun generic creation.
4. Verify destination/auth/channel identity immediately before the platform action.
5. Confirm privacy semantics and schedule time conversion in both local timezone and platform UTC format.
6. Execute the narrow scheduling/upload action only for the exact artifact.
7. Read back from the platform API after the action:
   - destination/channel identity;
   - title or artifact identity;
   - privacy state;
   - publish/schedule timestamp;
   - processing/upload status;
   - audience flags such as made-for-kids if relevant;
   - duration or other exact-artifact invariants.
8. Write a named repo-local handoff artifact and append/prepend the durable accepted-change entry.
9. State in the user reply what was explicitly not done: no generic create/loop, no immediate public publish unless requested, no unrelated scheduler/default-privacy/OAuth/config changes, no deletion.
10. Recommend read-only observation after an exposure window rather than immediate conclusions.

## Pitfalls

- Do not let a positive candidate review become broad permission to generate or publish multiple items.
- Do not rely on local DB state alone after a platform action; use read-back from the platform when available.
- Do not bury channel/destination verification. For multi-channel automation, wrong OAuth destination is a higher-risk failure than most content-quality issues.
- Do not store exact platform IDs or dated schedules in Hermes durable memory; those are repo handoff facts.
