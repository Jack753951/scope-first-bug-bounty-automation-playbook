> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Review Tiering and Anti-Fragmentation Pattern

Use this when a project has multiple reviewers (e.g. implementation reviewer, domain/strategy reviewer, orchestrator) and review files are becoming noisy.

## Goal

Keep independent review for meaningful risk while avoiding one-session-one-review-file sprawl.

## Tiers

### Tier 0 — Local check only

Use for:
- trivial docs/bookkeeping/typos,
- rolling-log updates,
- non-runtime process notes,
- changes that do not alter user-visible behavior, security posture, public readiness, or product direction.

Output:
- no one-off review file,
- update a rolling log or accepted-changes file only if the decision must persist,
- run local validation if available.

### Tier 1 — Lightweight domain/strategy review

Use for:
- visible artifacts,
- creative/strategy decisions,
- candidate/public-readiness previews,
- source/story/topic selection,
- decision artifacts for experimental channels/products.

Output:
- domain reviewer verdict (e.g. ACCEPT/CANARY/REVISE/REJECT),
- prefer rolling logs over one-off files,
- one-off review files only for public-readiness gates, major decision artifacts, or non-trivial phase gates.

### Tier 2 — Engineering + domain review

Use for:
- runtime code,
- safety gates,
- prompt systems that materially alter output,
- rendering/subtitle/QA logic,
- worker orchestration or reusable workflow contracts.

Output:
- engineering review notes,
- domain/strategy review when output/product direction is affected,
- orchestrator acceptance summary.

### Tier 3 — User-approved activation/public gate

Use for:
- upload, publish, deploy, scheduler, OAuth/token/credentials,
- active channel/product activation,
- privacy/default-public behavior,
- any externally visible irreversible action.

Output:
- local validation,
- independent engineering/safety review,
- domain/strategy review when relevant,
- explicit user approval for the exact action/artifact/visibility.

## Anti-fragmentation rules

- Prefer rolling decision logs for repeated review loops.
- Keep one-off review files for important gates only.
- Summarize reviewer findings into the authoritative log after the review.
- If a user asks whether review is becoming too fragmented, introduce/refresh tier rules immediately.
- If the user expected a specific reviewer (e.g. Claude for strategy/creative review), encode that reviewer into the relevant tier instead of relying on ad hoc judgment.
