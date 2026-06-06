> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Cybersec phase/status routing note

Use this when the user asks questions like "目前的長期目標是什麼？", "現在在什麼階段？", "Phase N 還要幾步？", or asks what a review decision means in the cybersec/hacking workspace.

## Durable pattern

- Treat this as a project-state/status task, not a reason to save transient progress in global memory.
- Answer from the project handoff/state artifacts when available: `.hermes.md`, `handoff/current_navigation.md`, `handoff/active_strategy_queue.md`, recent phase/review notes, current review/decision documents, `targets/catalog/*.md`, and relevant `modules/bundles/` status files. If context compaction or a previous chat summary mentions project status, treat it only as a lead and verify against project-local artifacts before presenting it as current.
- Frame the response in concise Traditional Chinese around:
  1. long-term goal;
  2. current phase/maturity level;
  3. what is already accepted vs. what is explicitly not authorized yet;
  4. which vulnerability/bundle classes are `verified-impact`, `valuable-candidate`, `attempted-not-verified`, `blocked/deferred`, or `reference-only`;
  5. remaining sub-phases or gates;
  6. next safest action.
- For advisory/CVE candidates, distinguish `source/install feasibility reviewed` from `local proof verified` and from `live-target authorized`. Do not describe a candidate as exploitable or report-ready merely because source diff, GHSA metadata, image tags, or install feasibility checks line up.
- Preserve security boundaries: distinguish offline/dry-run platform hardening, controlled local-lab activation, disposable target expansion, and real bug-bounty/private-beta execution.
- If the project has accumulated many handoffs, bundles, queues, or untracked artifacts, recommend a short navigation cleanup before opening another vulnerability lane: current default route, active lab targets, top 3 next valuable vuln lanes, deprecated lanes, recovery/snapshot rules, artifact location convention, and Obsidian memory-routing rule. This is project-local navigation, not a reason to delete data or create global memory.
- Do not treat improved local-lab capability as approval to move to real bug bounty/public targets. For this user, prefer stabilizing local proof primitives first: attacker callback proof pattern, browser-runtime XSS proof, file-read/path-traversal safe-marker proof, auth/session handling, evidence packet format, and report-readiness gate.
- If review terms are discussed, translate them into operational meaning: e.g. `APPROVE_WITH_CHANGES`, `PASS_WITH_RECOMMENDATIONS`, `REQUEST_CHANGES`, and `DEFER` should be tied to what can or cannot be done next.
- When the user asks whether old vulnerabilities were retested, do not answer from memory alone: inspect handoff/bundle state, distinguish “rerun/classified” from “verified exploit,” and explicitly name any remaining proof gaps.
- When the user asks how much of the vulnerability library has been tested, split the answer into family-touch coverage versus individual material-entry coverage; broad family coverage is not the same as corpus completion. See `references/cybersec-vulnerability-material-coverage-routing.md`.

## Memory routing

Save only stable user expectations, such as preferring phase/gate/status clarity. Do not save PR numbers, phase artifacts, completed slices, issue IDs, or "we finished X" facts to global memory; those belong in handoff files or session history.
