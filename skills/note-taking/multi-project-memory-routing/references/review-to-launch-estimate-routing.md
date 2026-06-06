> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Review-to-Launch Estimate Routing

Use this pattern when a sensitive or multi-agent project finishes a review/implementation slice and the user asks what the next work goal, workflow, or launch timeline should be.

## Durable lesson

A launch estimate is usually a project-local planning artifact, not global memory. Keep exact branches, PRs, commits, dated validation output, and phase status in repo handoff. Capture only reusable routing/process in skills.

## Procedure

1. Anchor the answer in live project authority:
   - active strategy queue / roadmap
   - accepted changes / review artifacts
   - safety or activation policy
   - current validation status when available
2. Separate readiness tiers rather than giving one vague date:
   - offline / dry-run MVP
   - controlled lab beta
   - authorized private beta
   - production-like multi-program or broad rollout
3. For cybersecurity, finance, uploads/publication, OAuth, scheduler, or other activation-sensitive work, distinguish:
   - code completeness
   - safety-gate completeness
   - operator/client authorization
   - review/approval boundary
   - evidence/reporting maturity
4. Recommend the next safest slice, preferably one that reduces review friction or clarifies boundaries without crossing activation gates.
5. Write the detailed estimate and rationale into repo-local handoff/strategy files. Keep chat summaries concise and point to the artifact path.
6. Do not promote PR numbers, commit SHAs, exact issue links, or one-day validation status into Hermes memory or this skill.

## Good output shape

```text
Current recommendation: do not activate live automation yet.

Launch tiers:
- Dry-run/local MVP: <range> — <what it means>
- Controlled lab beta: <range> — <what it permits>
- Authorized private beta: <range> — <what approval/gates are required>
- Production-like rollout: <range> — <missing operational controls>

Next safe slice:
- <small task that improves docs/tests/review boundary without touching live targets or production>
```

## Pitfalls

- Do not equate many passing tests with authorization to touch live targets.
- Do not collapse dry-run readiness, lab readiness, and bug-bounty/private-beta readiness into one date.
- Do not store the resulting estimate as global memory; it will stale quickly.
- Do not let a max-turn worker result become accepted truth until Hermes has inspected artifacts and verified locally.
