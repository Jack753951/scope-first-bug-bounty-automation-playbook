> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Risk-Tiered Local Learning and Post-Visionreview Canary Cadence

Use this pattern when a media/automation project is becoming over-gated: low-risk local experiments are being treated with the same process weight as upload/publication/scheduler/OAuth actions, slowing learning.

## Trigger

Signals include:

- User says safety gates are slowing project learning.
- User says the project needs real learning data before it can optimize.
- User wants `redditstories`, `redditscary`, or equivalent channels to upload/schedule after Claude/vision review rather than looping in local polish.
- Handoff shows many local-only review/policy rungs but too little live canary data.

## Rule

Split work by risk tier:

1. **Local-only learning: fast**
   - Generate/render small batches, commonly 3-5 drafts.
   - Use lightweight QA and compact table logging.
   - Do not require long per-artifact handoff or multi-agent review for every local draft.
   - Mark artifacts clearly as `LOCAL_LEARNING_ONLY` when they are not candidates.

2. **Post-visionreview canary candidate: decisive**
   - If Claude/Claude Code/visionreview gives a positive canary-candidate verdict and hard blockers are absent, default to preparing exact-artifact upload/scheduled canary.
   - Avoid adding another local polish rung unless the blocker is concrete and likely to materially affect public learning.

3. **Upload/scheduled/public/OAuth/scheduler: strict**
   - Keep exact artifact, exact channel, exact privacy/schedule, destination/auth checks, `DEFAULT_PRIVACY`, OAuth/token/client_secret, Windows Task Scheduler, and runtime deletion gates strict.
   - Do not treat a cadence preference as blanket upload approval; still require exact-scope approval or the project’s established approval phrase before mutation.

## Practical flow

```text
read-only canary observation
→ fast local batch, e.g. 3-5 drafts
→ lightweight QA table
→ Claude/Claude Code visionreview batch ranking
→ top positive candidate enters exact-artifact upload/scheduled-canary gate
→ read-only observation after release
→ feed live data into the next batch
```

## Hard blockers that still stop promotion

- Wrong channel/destination or OAuth mismatch.
- Failed render QA.
- Major subtitle/audio/readability failure.
- Obvious third-party/competitor/provenance/copyright risk.
- Wrong or privacy-unsafe setting.
- User explicitly rejected that artifact/content direction.
- Secrets/token/client_secret exposure would be required.

## Handoff updates

When the user adopts this correction:

- Update the active strategy queue / roadmap overlay, not just chat.
- Add a short accepted-change entry.
- If the project uses Obsidian, update the active strategy note so future status answers include the risk-tiered cadence.
- Keep global memory as a compact pointer only, e.g. “consult project-local strategy for risk-tiered fast local learning and post-visionreview canary cadence.”

## Pitfalls

1. Do not let safety become the product.
   - The goal of local learning is content signal, not gate perfection.

2. Do not remove hard gates.
   - The correction is to move gates to the correct risk tier, not to allow uncontrolled upload/publication.

3. Do not over-interpret early canary stats.
   - A zero-view snapshot within the first hour is not a creative failure. Record public/processed status and wait for exposure.

4. Do not ignore weak live data.
   - Moderate views with zero engagement is still useful: it shows exposure is possible but hook/retention/engagement may need work.

5. Do not create session-log-shaped global memories.
   - Store exact video IDs, counts, and timestamps in repo handoff; only compact project direction belongs in Hermes memory.
