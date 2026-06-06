> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# <program-name> multi-agent review synthesis — practical test run

Status: completed / BLOCK for proof beyond passive mapping
Date: 2026-05-26
Scope: <program-name> `<program-redacted>`, candidate `<program-name>-shared-inbox-object-permission`
Boundary: local read-only multi-agent review only. No target touched, no browser/VM/account action, no scanner/fuzzer/DAST, no exploit, no token/credential handling, no customer/non-owned data, no report submission.

## Worker routes actually invoked

- Claude Code tactical/boundary/evidence review
  - Artifact: `handoff/claude_program-redacted_tactical_boundary_evidence_review_20260526.json`
  - Raw preserved: `handoff/claude_program-redacted_tactical_boundary_evidence_review_20260526.raw.txt`
  - Version observed earlier: `claude --version` -> `2.1.146 (Claude Code)`
  - Session id: `492bcccb-a97e-4fd8-82c9-a3f85a1503ae`
  - Terminal reason: `max_turns`
  - Verdict extracted from generated content: `REQUEST_CHANGES`
  - Caveat: wrapper returned `error_max_turns`, but the file contains useful role-specific findings. Count it as one Claude/Cowork perspective, not three independent agents.

- Codex deterministic review
  - Artifact: `handoff/codex_program-redacted_deterministic_review_20260526.md`
  - Version observed earlier: `codex --version` -> `codex-cli 0.130.0`
  - Session id: `019e6421-4e56-7c30-b6dc-57773f5b3cee`
  - Verdict: `BLOCK`

## Cross-agent agreement

Both routes agree on the important result: the candidate is useful, but not ready for anything beyond passive UI/docs mapping.

Shared conclusions:

- `<program-name>-shared-inbox-object-permission` is strategically high-value because shared inbox permissions are core to <program-name> and match the policy interest in cross-company / cross-tenant / low-privilege boundary issues.
- Current evidence is not enough for a proof. We only have the post-signup/channel-connect gate and broad candidate packet, not a shared-inbox UI inventory, role matrix, owned-object plan, or redaction-safe proof protocol.
- No Account B / teammate identity and no second tenant exist, so role/tenant permission claims cannot be tested.
- API token/API calls, external channel connection, workflow activation, invites, object creation, and customer/non-owned data remain blocked.
- The existing workflow-rule reviews do not count as <program-name> proof-specific review; this run is the first <program-name>-specific multi-agent review and it returns BLOCK/REQUEST_CHANGES.

## Tactical value found

Claude preserved several attacker hypotheses for future bounded/lab planning:

- inbox object ID reuse/enumeration across workspaces;
- teammate reads inboxes outside membership;
- deleted/archived inbox or comment/draft reappearance;
- shareable/guest-link boundary bypass;
- attachment signed-URL replay across roles;
- message metadata/snippet leak in topics/team feeds;
- draft/scheduled message visibility across teammates;
- workflow/rule copy or routing causing unintended permission upgrade.

These are preserved as hypotheses only. They are not authorization to test.

## Required changes before any bounded proof

1. Keep candidate state as `needs_multi_agent_review` / passive-only; do not promote to `bounded_executable`.
2. Tighten candidate language: remove conditional object creation from `allowed_state_changes`; make it an explicit operator gate with named owned object label, redaction plan, and blocked outbound actions.
3. Add/record a passive shared-inbox/settings/role UI inventory first; no object creation unless later approved.
4. Define a positive/negative control protocol and expected permission matrix before any proof.
5. Decide whether Account B / second tenant is available through the operator action card. If not, keep this lane passive-only and preserve alternatives.
6. If later considering object creation, require explicit operator approval and keep it owned, non-sensitive, non-outbound, non-integrated, and reversible.
7. Re-check <bug-bounty-platform> policy/scope freshness before any bounded proof if near `scope.json` expiry.

## Hermes decision

Decision: `BLOCK_BEYOND_PASSIVE_MAPPING`.

Allowed next action, if we continue: passive UI/docs mapping only, preferably mapping settings/shared-inbox/role surfaces without creating objects, sending invites, connecting channels, generating tokens, calling APIs, saving/activating workflows, or touching non-owned/customer data.

This practical test was useful: the new workflow did what it should — it prevented a superficially plausible candidate from being promoted just because it looked promising, while preserving attacker hypotheses for future bounded planning.
