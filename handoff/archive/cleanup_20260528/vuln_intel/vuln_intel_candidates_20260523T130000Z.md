> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Vulnerability Intelligence Candidates — 20260523T130000Z

Status: one-shot intake / no target touched
Source: CISA KEV, NVD recent, GitHub Security Advisories when reachable
Boundary: metadata-only; no scanning, exploit execution, target bootstrap, live-target probing, or report submission.

## Routing meanings

- `local_bootstrap_review`: likely worth reviewing for a faithful local target or fixture.
- `local_or_live_review_high_impact`: high-impact class; review for local reproduction first, otherwise ask operator for legal scope.
- `needs_authorized_live_target`: do not drop; ask operator for legal target/scope/rules if chosen.
- `reference_only_review`: keep as reference unless it maps to current scope or a clear local target.

## Top candidates

| # | Source | ID | Product | Classes | Routing | Safe proof hint |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | CISA KEV | <specific-cve-id> | Zoho / ManageEngine | rce/command-execution,auth/access-control | local_bootstrap_review | Use throwaway accounts, role/account matrix, positive + negative controls, and no real data retention. |
| 2 | GitHub Advisory | <specific-ghsa-id> |  | unknown/review | local_bootstrap_review | Review manually; do not touch targets until scope and safe proof plan are explicit. |
| 3 | GitHub Advisory | <specific-ghsa-id> |  | unknown/review | local_bootstrap_review | Review manually; do not touch targets until scope and safe proof plan are explicit. |
| 4 | GitHub Advisory | <specific-ghsa-id> |  | rce/command-execution,redirect | local_bootstrap_review | Requires explicit authorization; use marker-only bounded action, pre/post health, and human confirmation gate. |
| 5 | GitHub Advisory | <specific-ghsa-id> |  | unknown/review | local_bootstrap_review | Review manually; do not touch targets until scope and safe proof plan are explicit. |
| 6 | CISA KEV | <specific-cve-id> | Zoho / ManageEngine | rce/command-execution,upload/archive | local_or_live_review_high_impact | Requires explicit authorization; use marker-only bounded action, pre/post health, and human confirmation gate. |
| 7 | CISA KEV | <specific-cve-id> | Yealink / Device Management | ssrf,rce/command-execution | local_or_live_review_high_impact | Use callback/OAST only if explicitly allowed; prefer DNS-only marker; no metadata/internal scanning. |
| 8 | GitHub Advisory | <specific-ghsa-id> |  | ssrf,rce/command-execution | needs_authorized_live_target | Use callback/OAST only if explicitly allowed; prefer DNS-only marker; no metadata/internal scanning. |
| 9 | CISA KEV | <specific-cve-id> | Zyxel / Multiple Products | unknown/review | reference_only_review | Review manually; do not touch targets until scope and safe proof plan are explicit. |
| 10 | CISA KEV | <specific-cve-id> | Zoho / ManageEngine | upload/archive | reference_only_review | Review manually; do not touch targets until scope and safe proof plan are explicit. |
| 11 | NVD recent | <specific-cve-id> |  | unknown/review | reference_only_review | Review manually; do not touch targets until scope and safe proof plan are explicit. |
| 12 | NVD recent | <specific-cve-id> |  | xss | reference_only_review | Use browser/runtime safe marker only; no cookie theft, keylogging, or victim interaction. |
| 13 | NVD recent | <specific-cve-id> |  | auth/access-control | reference_only_review | Use throwaway accounts, role/account matrix, positive + negative controls, and no real data retention. |
| 14 | NVD recent | <specific-cve-id> |  | auth/access-control | reference_only_review | Use throwaway accounts, role/account matrix, positive + negative controls, and no real data retention. |
| 15 | NVD recent | <specific-cve-id> |  | auth/access-control,redirect | reference_only_review | Use throwaway accounts, role/account matrix, positive + negative controls, and no real data retention. |

## Next operator decision

Pick at most one candidate. If routing is `needs_authorized_live_target`, provide the Phase 5A scope package before any target-touching work. If routing is local, create a bounded local bootstrap plan first.

JSON: `<private-workspace>/handoff/vuln_intel/vuln_intel_candidates_20260523T130000Z.json`
CSV: `<private-workspace>/handoff/vuln_intel/vuln_intel_candidates_20260523T130000Z.csv`
