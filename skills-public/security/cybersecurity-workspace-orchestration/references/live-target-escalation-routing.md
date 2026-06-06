> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Live-target escalation routing

Use this when vulnerability-intelligence or proof-wave triage finds a valuable candidate that cannot be faithfully reproduced in the local lab.

## Core rule

Local/recoverable lab remains the preferred first route, but local-lab fit is a prioritization signal, not a hard exclusion filter.

Do not discard a vulnerability class or product-specific candidate solely because it needs a live/real target. Keep it as `needs_authorized_live_target` or `blocked-awaiting-scope` and ask the operator for legal target/scope/rules.

## Three-way candidate triage

1. `local_bootstrap_ready`
   - The vulnerable product/version or a faithful fixture can be launched in the recoverable lab.
   - Proceed with local target bootstrap, pre/post health, artifact path, cleanup, and evidence packet shape.

2. `local_simulation_possible_but_not_faithful`
   - A local lab can teach the pattern, but cannot honestly prove the real-world candidate.
   - Use local simulation only as methodology training; do not claim equivalence or report-readiness.

3. `needs_authorized_live_target`
   - The proof depends on live SaaS/cloud/workflow/payment/auth/mobile/API/product behavior, provider integration, real program scope, or a version that cannot be reproduced locally.
   - Retain the candidate, preserve source/proof notes, and request scope from the operator.

## Minimum scope package to request

Ask for only what is needed for that lane:

- target URL/app/API/product/version and environment type;
- written authorization or program/scope link;
- in-scope and out-of-scope assets/actions;
- allowed test classes, rate limits, time windows, and notification/reporting rules;
- test accounts/test data and whether destructive or state-changing tests are allowed;
- redaction/evidence handling requirements;
- whether external callbacks, OAST, tunnels, webhooks, or public listeners are allowed.

## Pitfalls

- Do not silently convert a candidate into public-target testing.
- Do not treat `needs live target` as `drop candidate`.
- Do not over-simulate locally when the local fixture no longer proves the vulnerability behavior truthfully.
- Do not let scope-request routing become governance-first busywork; keep it focused on enabling a legal proof wave.
