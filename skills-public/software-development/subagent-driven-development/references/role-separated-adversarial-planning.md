> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Role-separated adversarial planning reviews

Use this reference when delegating review for security research, bug-bounty planning, tactical preview, or other adversarial workflows where creativity and safety boundaries must both improve.

Core lesson

Multi-agent review is only useful if each reviewer has a distinct job. Do not ask three agents to produce the same broad review. Split the work so disagreements are meaningful and Hermes can synthesize them.

Recommended role split

1. Adversarial planner
   - Expands realistic attacker-like paths.
   - Preserves high-impact ideas even if they cannot be executed now.
   - Does not decide authorization or safety approval.

2. Boundary engineer
   - Converts each path into proof boundary, proof surrogate, and stop-before rules.
   - Marks candidates as bounded executable, blocked/preserve, needs scope, needs operator control, needs local simulation, or reference-only.
   - Treats missing owned controls, callback/OAST/tunnel allowance, data-contact boundary, or state-change boundary as blockers.

3. Evidence critic
   - Checks whether evidence would actually prove impact.
   - Rejects overclaims, non-owned data contact, sensitive artifacts, weak controls, and report-readiness gaps.

4. Hermes synthesis
   - Reads all role outputs.
   - Fixes concrete REQUEST_CHANGES before completion.
   - Selects at most one bounded lane, parks/preserves blocked candidates, or escalates to operator/scope gate.
   - Does not treat a reviewer recommendation as execution authorization.

Prompt pattern

Include in every delegated role context:

- exact project context entrypoints to read
- exact files under review
- explicit allowed actions and forbidden side effects
- expected verdict format: `PASS` or `REQUEST_CHANGES`
- instruction to return concrete blockers only, not generic concerns
- instruction to preserve realistic but currently unsafe ideas as parked candidates rather than deleting them

For side-effect-sensitive/security repos, forbidden side effects usually include:

- live target requests
- browser automation
- scans/fuzzers/DAST
- exploit execution
- callbacks/OAST/tunnels
- account actions
- credential handling
- scope edits
- report submission

Common pitfall

If the same reviewer is asked to be creative, safety gate, and evidence critic at once, they often either over-block creative tactics or under-specify boundaries. Keep creativity and boundary compilation separate, then have Hermes synthesize.
