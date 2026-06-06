> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Vulnerability Intelligence Candidates — 20260527T042644Z

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
| 2 | NVD recent | <specific-cve-id> |  | unknown/review | local_bootstrap_review | Review manually; do not touch targets until scope and safe proof plan are explicit. |
| 3 | NVD recent | <specific-cve-id> |  | rce/command-execution | local_bootstrap_review | Requires explicit authorization; use marker-only bounded action, pre/post health, and human confirmation gate. |
| 4 | NVD recent | <specific-cve-id> |  | xss | local_bootstrap_review | Use browser/runtime safe marker only; no cookie theft, keylogging, or victim interaction. |
| 5 | GitHub Advisory | <specific-ghsa-id> |  | file-read/path-traversal,auth/access-control | local_bootstrap_review | Use throwaway accounts, role/account matrix, positive + negative controls, and no real data retention. |
| 6 | GitHub Advisory | <specific-ghsa-id> |  | upload/archive | local_bootstrap_review | Review manually; do not touch targets until scope and safe proof plan are explicit. |
| 7 | GitHub Advisory | <specific-ghsa-id> |  | redirect | local_bootstrap_review | Review manually; do not touch targets until scope and safe proof plan are explicit. |
| 8 | CISA KEV | <specific-cve-id> | Zoho / ManageEngine | rce/command-execution,upload/archive | local_or_live_review_high_impact | Requires explicit authorization; use marker-only bounded action, pre/post health, and human confirmation gate. |
| 9 | CISA KEV | <specific-cve-id> | Yealink / Device Management | ssrf,rce/command-execution | local_or_live_review_high_impact | Use callback/OAST only if explicitly allowed; prefer DNS-only marker; no metadata/internal scanning. |
| 10 | CISA KEV | <specific-cve-id> | Zyxel / Multiple Products | unknown/review | reference_only_review | Review manually; do not touch targets until scope and safe proof plan are explicit. |
| 11 | CISA KEV | <specific-cve-id> | Zoho / ManageEngine | upload/archive | reference_only_review | Review manually; do not touch targets until scope and safe proof plan are explicit. |
| 12 | NVD recent | <specific-cve-id> |  | xss | reference_only_review | Use browser/runtime safe marker only; no cookie theft, keylogging, or victim interaction. |
| 13 | NVD recent | <specific-cve-id> |  | auth/access-control | reference_only_review | Use throwaway accounts, role/account matrix, positive + negative controls, and no real data retention. |
| 14 | GitHub Advisory | <specific-ghsa-id> |  | sqli | reference_only_review | Use bounded boolean/time-free controls or synthetic data only; no dumping or broad extraction. |
| 15 | GitHub Advisory | <specific-ghsa-id> |  | deserialization,rce/command-execution,sqli | reference_only_review | Requires explicit authorization; use marker-only bounded action, pre/post health, and human confirmation gate. |

## Next operator decision

Pick at most one candidate. If routing is `needs_authorized_live_target`, provide the Phase 5A scope package before any target-touching work. If routing is local, create a bounded local bootstrap plan first.

JSON: `<private-workspace>/handoff/vuln_intel/vuln_intel_candidates_20260527T042644Z.json`
CSV: `<private-workspace>/handoff/vuln_intel/vuln_intel_candidates_20260527T042644Z.csv`
