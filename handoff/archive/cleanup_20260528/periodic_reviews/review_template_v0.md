> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Periodic Project Review Template v0

Copy this template into a dated folder such as `handoff/periodic_reviews/YYYY-MM-DD/` when writing a periodic or direction-boundary review. Keep the filled artifact as Markdown. Do not add a schema header, machine-readable contract marker, or candidate-chain consumer surface.

## Review Metadata

- Review date:
- Review scope:
- Current branch / commit:
- Packet frozen at:
- Latest live handoff inspected:
- Latest commit inspected:
- Post-packet changes included:
- Post-packet changes excluded:
- Authority if stale: current explicit operator instruction, live repo state, `handoff/accepted_changes.md`, and `handoff/active_strategy_queue.md` override stale frozen packets.
- Reviewer route/tool summary:
- Visible model/runtime by reviewer route, if exposed:
- Explicitly out of scope:

## Reviewer Routes Consulted

Reviews are advisory unless they identify a concrete blocker. A route may be skipped when it would not materially improve quality; record the reason briefly.

### Hermes Local Validation / Decision Layer

- Status:
- Evidence reviewed:
- Hard-stop assessment:
- Concrete blockers:
- Notes:

### Implementation / Deterministic Reviewer

- Status:
- Route/tool:
- Visible model/runtime:
- Concrete blockers:
- Advisory improvements:
- Test/validation gaps:
- Verdict:

### Safety / Security Reviewer

- Status:
- Route/tool:
- Visible model/runtime:
- Authorization/scope notes:
- Target-touching / scanner / callback / proxy / pivot / scheduler / credential risk:
- Secret / loot / Git ignore posture:
- Operator approval required: yes/no; reason:
- Concrete blockers:
- Advisory improvements:
- Verdict:

### Architecture / Roadmap Reviewer

- Status:
- Route/tool:
- Visible model/runtime:
- Extensibility / updateability / modularity:
- Contract or artifact-boundary impact:
- Goal alignment with authorized bug-bounty automation platform:
- Artifact sprawl / consolidation notes:
- Concrete blockers:
- Advisory improvements:
- Verdict:

## Validation Performed

List concrete commands and outcomes. Avoid vague claims such as `all tests passed` without counts or exit status.

- `git status --short --branch`:
- `git log --oneline -5`:
- `HACKLAB=<private-workspace> ./bin/hermes review` if shared workflow/contracts/scripts changed:
- Focused tests, if applicable:
- Full/offline tests, if applicable:
- Git diff / whitespace checks:
- Secret/safety scan, if applicable:

### Not Validated

- Item:
- Reason:
- Risk / follow-up:

## Source / OSS Pattern Check

Choose one and explain:

- `not useful for this slice; reason: ...`
- `used; reference: ...`
- `recommended before implementation; reason: ...`

If used or recommended, summarize adopt / adapt / ignore decisions and rejected unsafe defaults.

## Long-Term Goal Alignment

- Does this review move the project toward an authorized, modular, update-friendly bug-bounty automation platform?
- What drift risks are visible?
- What should be paused, consolidated, or stopped because it slows capability growth?

## Workflow / Memory / Handoff Flow

- Which conclusions belong in `handoff/`?
- Which settled, reusable workflow lessons belong in skills or memory?
- Which details are temporary and should remain out of durable memory?
- Are periodic review artifacts aligned with the current policy documents?
- Memory drift check: does Hermes durable memory overstate, understate, or conflict with repo truth?
- Handoff drift check: do `accepted_changes.md`, rolling handoffs, named artifacts, and `active_strategy_queue.md` agree?
- Goal drift check: is the project still moving toward authorized bug-bounty automation rather than CTF-only, process-only, or artifact-only work?
- Capability-growth drift check: are process artifacts blocking runnable scripts, proof bundles, or useful bounty checkpoints?
- Structure drift check: are artifacts accumulating without a clear active queue or owner?
- Obsidian routing: should any strategy/review synthesis be mirrored to the project Obsidian namespace without sensitive operational data?

## Project Structure / System Health

- Structure health:
- Artifact sprawl / stale handoffs:
- Duplication watchlist status:
- Lock / temp / generated artifact posture:

## Safety Governance

- Scope / authorization posture unchanged: yes/no
- `config/scope.txt` touched: yes/no
- `recon.sh` / runtime scanner behavior touched: yes/no
- Live-target affordance check for `--target`, `--url`, `--host`, `--scope`, `--live`:
- Secrets / loot / credentials posture:
- Production / scheduler / OAuth / billing / repo-settings posture:
- Operator approval required: yes/no; reason:

## Test / Validation Quality

- Test coverage adequacy:
- Negative / fail-closed tests:
- Dry-run / offline-only guarantees:
- Known gaps:

## Roadmap / Next Phase

- Immediate next capability-building slice:
- Deferred items:
- Re-trigger conditions for each deferred item:
- Items to avoid for now:

## Disagreement Handling

A disagreement blocks only when it maps to a hard stop, failing validation, malformed consumed contract, or data/capability-loss risk. Generic caution is advisory.

### Blocking Disagreements

- Finding:
- Reviewer route:
- Concrete hard stop / validation failure:
- Required response:

### Non-Blocking Disagreements

- Recommendation:
- Reviewer route:
- Deferred trigger or narrow follow-up:

## Final Decision Block

```text
Decision: PASS / PASS_WITH_CONDITIONS / REQUEST_CHANGES / DEFER / ESCALATE_TO_OPERATOR
Concrete blockers:
Reviewers consulted:
- <route/tool>; visible model/runtime: <model if exposed, otherwise limitation>
Validation performed:
Advisory recommendations:
Safety boundary:
Source/OSS pattern check: not useful / used / recommended before implementation
User approval required: yes/no; reason:
Accepted changes updated: yes/no/not applicable
Next action:
```

## Operator Approval Line

User approval required: yes/no; reason:

## Accepted-Changes Pointer

- `handoff/accepted_changes.md` entry date / summary:
