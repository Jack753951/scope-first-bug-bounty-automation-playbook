> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Current Navigation

Status: active compact navigation
Updated: 2026-05-29 (<program-slug> scoped lane → operator password gate)

## Project shape

Authorized bug-bounty platform. **Hermes (GPT-5.5) is the primary autonomous driver**; Claude Code CLI and Codex CLI are on-demand consults. Operator clears human gates. See `/INDEX.md` for full ownership map and `/.hermes.md` for Hermes role; `/SAFETY.md` for hard stops.

## North star

**First report-ready draft / submission within 30 days of restructure (target: 2026-06-27).** Each week must end with a lane state change or KILL — no week of zero motion. Infrastructure elegance is a support task; first-bounty outcome outranks it.

## Current route

- Repo: `<private-workspace>` — **current main/primary workspace** for Cybersec Lab work.
- Old repo `<private-workspace>` is **not active authority for this workspace**; treat it as an archived/reference snapshot only. Do not import or reconcile its old lanes unless the operator explicitly asks.
- Attacker VM: `<attacker-vm>` (host-only, NAT closed by default).
- Victim/lab VM: `<victim-vm>`.

## Active Tier A live lanes

**<program-slug>** — exact-host scope approved 2026-05-29 for `us.identity.<program-redacted>.com`, `app.<program-redacted>`, and `cloud.<program-redacted>.com`; owned-account signup advanced past the password gate and is now blocked at `A2_EMAIL_VERIFICATION_GATE`. Next operator action: verify the <program-slug> Konnect signup email for the owned H1 alias or manually continue in noVNC. OTP/CAPTCHA/final submit remain human-gated. No proof testing, scanners/fuzzers/DAST, API-token/OAuth/webhook/integration creation, customer/non-owned data access, or report submission is authorized by this lane state.

## Recently closed (KILL, 2026-05-28)

`<program-redacted>`, `<program-slug>`, `<program-redacted>`, `<program-slug>` — see each lane_state for closure reasons. Do not auto-reopen.

## Highest-priority operator action

**Clear <program-slug> Konnect email-verification gate or park the lane.** Scope packet, `programs/<program-slug>/scope.json`, global exact-host allowlist entries, run card, and first-contact surface map are in place. The active lane is blocked at Konnect owned-account email verification after signup succeeded. Operator must verify the email/link/code or continue manually in noVNC. If not clearing the gate, keep <program-redacted>/<program-slug>/Intigriti/<program-redacted> in passive candidate triage from `handoff/operator_inbox_20260529.md`.

## What is allowed now

- File organization, docs, scripts, schemas, tests, lab proofs against disposable targets.
- Public/passive reading: program policy, advisories, vendor docs, CVE/PoC sources.
- In-scope owned-account browser/manual work within each lane's stop-before rules.
- `dry-run` policy and recon (offline computation only).

See `/SAFETY.md` "Allowed by default" for full list.

## What is NOT allowed without explicit operator approval

See `/SAFETY.md` "Hard stops".

## Latest-vulnerability research lane

Source/local/passive review only. No live action. Live attempt requires intersection with an in-scope program.

- **2026-05-28 three-latest local lab batch** — verified in `<victim-vm>`: LiquidJS `<specific-cve-id>` strip_html ReDoS, @hapi/content `<specific-cve-id>` duplicate-parameter smuggling, and tmp `<specific-cve-id>` path traversal with patched control. Artifacts: `<artifact-output-dir>/three_latest_npm_vulns_20260528T110251Z/evidence/`; proof packets under `labs/proofs/`; bundles under `modules/bundles/`.
- **Dify** — auth/tenant/path-traversal cluster (<specific-cve-id> / 41948).
- **Langflow** — RCE / origin validation (KEV-listed).
- **LiteLLM** — SQLi (KEV).
- **Open WebUI** — upload path traversal.
- **LiquidJS** — RCE (GHSA fresh); local marker-only proof verified 2026-05-28 for `<specific-cve-id>` / `<specific-ghsa-id>` in `<victim-vm>`.
- **2026-05-29 realistic SaaS/API local lab** — installed/ran `modern-realistic-api` on `<victim-vm>` at `<victim-vm>:18080`; verified 7 high-value classes (BOLA/IDOR, authz role separation, path traversal, SSRF loopback surrogate, XXE, unsafe deserialization, upload retrieval) plus XSS sink candidate. Artifacts: `<artifact-output-dir>/realistic_saas_api_20260529T063059Z/`; proof packet `labs/proofs/realistic_saas_api_multi_class_kali_victim_20260529.md`; bundle `modules/bundles/verified_lab_flow_realistic_saas_api_multi_class.md`; note `notes/cybersec_lab_realistic_saas_api_tactics_20260529.md`.

## Recurring engineering cadence

Minute: CT/scope alerts. Hourly: diff recon on changed assets. Daily: passive inventory + KEV/NVD diff. Weekly: deep discovery + disclosed-report mining. Monthly: asset re-inventory.

Scheduler remains intentionally inactive until the operator enables it; `scripts/build_operator_inbox.py` now has a proved consumer path for lane and pending-candidate decisions. Disclosed-report mining now has the first offline/TDD slice in place: `schemas/disclosed_report.schema.json`, `scripts/ingest_disclosed_reports.py`, `scripts/score_disclosed_report_patterns.py`, `fixtures/disclosed_reports/sample_public_reports.jsonl`, and `scripts/test_disclosed_report_mining.py`. The slice is file-input only, sanitized, candidate-pattern only, and does not authorize live target contact.

## Memory routing

- Hermes durable memory: compact cross-session/profile signposts only.
- Repo handoff/INDEX/current_navigation: active engineering truth and validation state.
- Obsidian Cybersec Lab namespace: long-term strategy, methodology, rationale, and review synthesis.
- Old `<private-workspace>` references in historical Obsidian/lab notes are legacy pointers, not active authority.

## Authority order (when sources disagree)

See `/SAFETY.md` § "Authority order".
