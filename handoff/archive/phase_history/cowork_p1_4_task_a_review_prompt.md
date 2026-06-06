> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

Read `.hermes.md`, `handoff/cowork_p1_4_proposal.md`, `handoff/codex_p1_4_proposal_review.md`, `handoff/codex_review.md`, and the current git diff.

Task:
Independently review Codex's Phase 1 P1-4 Task A implementation (CLI surface only) for the cybersec lab.

Check specifically:
- Does the implementation stay within Task A only?
- Does it correctly implement `--program`, `--policy-mode`, and `--allow-cidr` parsing/validation?
- Is no-`--program` behavior zero-side-effect except ordinary existing behavior?
- Are path/slug restrictions strong enough, including symlink/path escape behavior?
- Are dry-run/planned/live constraints safe?
- Are tests meaningful and offline-only?
- Are there maintainability or roadmap issues before Task B?
- Did Codex avoid target-touching behavior, `config/scope.txt`, secrets, logs, scheduler/deployment, reports, and `accepted_changes.md` edits?

Constraints:
- Offline-only review.
- Do not modify files.
- Do not run active scans/probes/network target-touching commands.
- If you run commands, restrict to read-only git diff and offline syntax/unit tests.

Output format:
# Cowork Review — P1-4 Task A CLI Surface

Verdict: ACCEPT / ROUTE_BACK

Blocking issues:

Non-blocking recommendations:

Testing gaps:

Safety/authorization assessment:

Architecture/roadmap assessment:

Recommended next step:
