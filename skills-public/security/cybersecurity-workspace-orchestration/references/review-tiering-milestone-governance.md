> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Review Tiering and Milestone Governance

Use this pattern when a cybersecurity workspace's multi-agent review loop becomes too fragmented or when the user asks whether reviews are too heavy. The goal is not to weaken safety; it is to concentrate deep review on contract/runtime/safety boundaries while batching related low-risk slices.

## Core Policy

Assign a review tier before routing work:

| Tier | Use for | Required review |
|---|---|---|
| T0 Trivial/offline docs | Typos, formatting, comments, non-policy notes | Hermes static/context check |
| T1 Local docs/fixtures | Offline examples, README updates, non-sensitive fixtures that do not alter contracts or execution | Hermes + Codex if files change |
| T2 Standard implementation | Internal refactors, schema-compatible helpers, validators, tests, offline adapters | Codex implementation + Hermes review |
| T3 Contract/platform boundary | New/changed schema, manifest, module/profile/runner/report boundary, importer/exporter, finding/evidence lifecycle, external-tool integration | Claude/Cowork direction review with OSS Recon Gate + Codex + Hermes + Claude/Cowork implementation review |
| T4 Safety/runtime boundary | Scope enforcement, `safe_target`, program policy, recon/scanner/module execution, callbacks, notifications, live-mode gating, authz decisions | Operator approval where needed + full direction/implementation/re-review; prove fail-closed behavior |
| T5 Production/release boundary | Scheduler, deployment, billing, publishing, external services, persistent automation, secret-handling changes | Explicit operator approval + full T4 if cyber-relevant |

If safety impact is ambiguous, choose the higher tier and keep review offline until the boundary is clear.

## Escalation Triggers

Escalate to the highest matching tier if the change touches:

- authorization, scope, `safe_target`, policy decisions, run manifests, or dry-run/live-mode decisions
- `recon.sh`, module runner behavior, scanner adapters, external tool invocation, callbacks, webhooks, notifications, or target selection
- schemas, module manifests/profiles, reports, finding/evidence contracts, importers/exporters, or agent/tool boundaries
- external scanner output, templates, rules, or OSS conventions
- persistence, redaction, hashing, deduplication, reports, generated artifacts, `loot/`, secrets, credentials, logs, or `.gitignore`
- concurrency, locks, scheduling, background automation, update mechanisms, or hard-to-revert cross-cutting changes

## OSS Recon Gate Linkage

- T0-T2 normally skip OSS Recon Gate unless an escalation trigger applies.
- T3 requires OSS Recon Gate before Codex implementation when introducing/changing platform contracts, modules, runners, reports, evidence/finding lifecycle, external-tool integrations, or update mechanisms.
- T4/T5 require OSS Recon Gate when they also change contracts, execution boundaries, external tooling, proxy/pivot/transport design, update mechanisms, or finding/evidence/report lifecycles.
- One milestone-level OSS Recon Gate can cover multiple small slices only while the approved boundary and assumptions remain unchanged.

## Milestone Batching

When related slices are being over-reviewed, create a milestone rather than independent full reviews for each patch.

Template:

```text
Milestone: <name>
Tier: T2/T3/T4/T5
Goal:
Safety boundary:
In scope:
Out of scope:
OSS Recon Gate required: yes/no; references:
Planned slices:
1. <slice> - files/contracts/tests
2. <slice> - files/contracts/tests
Acceptance checks:
Rollback/defer notes:
```

Rules:

- One milestone should have one primary boundary: policy/scope, contract/schema, module runner, reporting, importer, or docs.
- Prefer small vertical slices with tests over broad rewrites.
- Do not mix T4 safety/runtime work with unrelated cleanup; split cleanup into T1/T2.
- Record deferred items so non-blocking recommendations do not become hidden blockers.
- Close only after Hermes verification, required independent review, and accepted-changes/handoff summary.

## Proxy / Pivot / Transport Defaults

Treat proxy, pivot, and transport features as high-risk because they can create unintended network reachability.

- Offline docs/diagrams: T1, escalate if they imply execution defaults.
- Offline proxy/pivot/transport schema or validators: T3 + OSS Recon Gate.
- Any code that can open sockets, forward traffic, tunnel, proxy, pivot, callback, beacon, invoke external network tools, or create relay chains: T4 minimum, even for lab use.
- Persistent, scheduled, production-like, credentialed, or secret-bearing transport: T4/T5 depending on side effects and operator approval.

Default posture: design offline first; implement validators/previews before execution; live transport last and only after explicit operator approval plus scope/policy allow.

## Worker Prompt Fields

Direction/implementation reviews should include:

```text
Review tier: T0/T1/T2/T3/T4/T5
Milestone:
OSS Recon Gate: not applicable / attached / required before implementation
Escalation required: yes/no; reason:
Blocking issues:
Non-blocking improvements:
Required tests/safety assertions:
Out-of-scope/deferred items:
```

Codex prompts should say: honor the assigned review tier and milestone boundary; if implementation reveals an escalation trigger, stop and route back instead of broadening scope silently.

Hermes final arbitration should confirm the tier/milestone still matches the final diff before accepting the change.
