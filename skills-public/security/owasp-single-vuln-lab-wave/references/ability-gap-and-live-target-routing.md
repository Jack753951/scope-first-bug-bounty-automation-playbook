> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Ability-Gap-Only Lab Closeout and Live-Target Routing

Use this reference when a local lab already has several verified proof primitives and the operator asks whether to keep testing new漏洞類型, move toward bug bounty readiness, or add latest-vulnerability intake.

## Core lesson

Do not keep adding lab waves just to increase the count. Once the proof library has stable primitives, new vulnerability testing should be limited to explicit capability gaps.

Good reasons to add one more local proof wave:

- it adds a proof shape needed for real authorized assessments;
- it trains multi-account / multi-role / tenant-boundary evidence;
- it improves report-readiness or false-positive control;
- it turns a recurring blocker into a reusable operator-run or safe-marker pattern;
- it creates a capability that existing bundles cannot approximate.

Poor reasons:

- another similar XSS/path traversal/SSRF/SQLi lab just because it is available;
- a scanner lead with no reusable proof/evidence pattern;
- expanding governance/importer/schema work before proof value is known.

## Local-first, not local-lab-only

Default to recoverable local lab proof when faithful reproduction is possible, but do not use local-lab fit as a hard exclusion filter.

Route candidates as:

- `local_bootstrap_ready`: can be faithfully reproduced in a local disposable target; bootstrap and prove locally.
- `local_simulation_possible_but_not_faithful`: useful for learning the pattern, but do not claim equivalence to the product-specific/live vulnerability.
- `needs_authorized_live_target`: valuable candidate genuinely needs a live/real target; keep it and ask the operator for legal target/scope/rules instead of dropping it.
- `reference_only`: useful background, but not enough for a target-touching wave.

## When a candidate needs a live target

Ask the operator for a legal scope package before any target-touching work:

```text
target URL / app / API / product / version
authorization or program/scope link
in-scope and out-of-scope assets/actions
allowed vulnerability classes and payload boundaries
rate limits / time window / notification rules
test accounts / roles / test data availability
destructive/state-changing permission
evidence redaction/minimization rules
external callback / OAST / tunnel allowance
```

Until supplied, keep the candidate as `needs_authorized_live_target` / `blocked-awaiting-scope`. Do not silently discard it, and do not let Hermes authorize the target by itself.

## Phase boundary pattern

If the current phase is a local proof-platform phase, close it after the last clear ability gap. Move periodic latest-vulnerability refresh to the next phase instead of letting closeout expand indefinitely.

Recommended split:

- Phase 4-style closeout: one or two ability-gap proof waves, proof-library cleanup, evidence packet/readiness template, current navigation cleanup.
- Phase 5-style intake: one-shot vulnerability-intelligence refresh MVP first; candidate triage; local/live target routing; only later optional weekly schedule if output stays compact.

Do not start with scheduler/automation. Start with a one-shot refresh and a small top-candidate queue.

## Auth/session role-separation proof as a high-value gap

When the lab already has injection, callback, file-read, XSS, and deserialization primitives, a strong next gap is often auth/session role separation:

- normal user vs admin or member vs owner;
- unauthenticated control;
- positive role-boundary bypass;
- admin/owner baseline;
- separate secure-control endpoint that correctly denies the lower role;
- post-health and lab-owned markers only.

This proof shape prepares for Phase 5 live-target dry runs because real bug bounty reports often succeed or fail on role/account matrix quality, not payload cleverness.

## Closeout wording

After completing an ability-gap wave, say explicitly:

- whether the result is `verified_*_lab_only`, `reusable_methodology`, `attempted_not_verified`, or `needs_authorized_live_target`;
- what project capability it adds;
- why no more similar lab variants are needed by default;
- that periodic vulnerability-intelligence refresh belongs to the next phase if that was the agreed boundary;
- that live-target candidates should request legal scope instead of being filtered out.
