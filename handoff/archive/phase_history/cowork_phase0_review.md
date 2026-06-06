> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Cowork Phase 0 Independent Review

Date:     2026-05-15
Reviewer: Cowork (Claude, independent reviewer pass)
Scope:    Phase 0 scope-hardening implemented by Codex
Inputs:   `.hermes.md`, `handoff/cowork_proposal.md` §1, `handoff/codex_review.md`,
          `handoff/accepted_changes.md`, `recon.sh`, `config/recon.conf`,
          `bin/hermes`, `handoff/latest_check.md`
Method:   Read-only inspection + reasoning. No network tools run.

---

## Verdict

**Phase 0 is substantively complete and ACCEPT-with-followups.** No blocking
implementation defects were found. The remaining gaps are validation-evidence
gaps and one minor scope-policy semantic. None require routing back to Codex
before Phase 1, provided the operator (or Codex, as a small follow-up) closes
the validation gaps listed below.

---

## Requirements Matrix

Requirement source: `cowork_proposal.md` §1.1 / §1.3.

| # | Requirement | Status | Evidence |
|---|---|---|---|
| 1 | Gate `--skip-scope-check` behind per-session token, force dry-run | MET | `recon.sh:234-247` (`validate_runtime_flags` requires `SCOPE_OVERRIDE_TOKEN` == `SCOPE_OVERRIDE_CONFIRM`, sets `DRY_RUN=true`). `safe_target` short-circuits with audit event `SAFE_TARGET_OVERRIDE_DRY_RUN` (`recon.sh:439-444`). |
| 2 | Refuse `REQUIRE_SCOPE_CHECK=false` as hard error | MET | `recon.sh:223-232` (`validate_config` exits non-zero on anything not exactly `true`). Comment updated at `config/recon.conf:69`. |
| 3 | Revalidate after domain expansion | MET | `enum_subdomains` calls `filter_safe_targets` on raw subfinder+crt.sh output (`recon.sh:564`); dropped hosts captured in `subdomains_dropped.txt` with reasons; surfaced in summary (`recon.sh:835-836`). |
| 4 | Single `safe_target` runtime guard, no per-stage scope logic | MET | One authoritative function (`recon.sh:431-466`). Called by `find_live_hosts`, `port_scan`, `service_fingerprint`, `web_probe`, `dir_bruteforce`, `vuln_scan`, and inline at `run_pipeline:899`. No competing scope logic found. |
| 5 | Default-deny on ambiguity (missing/unparseable scope, malformed target) | MET | `validate_scope_file` rejects missing/unreadable/empty/unparseable (`recon.sh:389-409`). `parse_target` rejects empty, leading `-`, whitespace/control, shell metachars, userinfo, malformed port, IPv6 literal, non-IP/CIDR/domain (`recon.sh:332-387`). |
| 6 | `bash -n recon.sh` clean | MET | `handoff/latest_check.md` reports "All shell scripts: bash -n OK". |
| 7 | Unit checks for scope/out-of-scope/malformed/IDN/wildcard | PARTIAL | Codex validated: authorized, unauthorized, `REQUIRE_SCOPE_CHECK=false`, missing token, matching token (dry-run forced), one malformed (`bad host`), one out-of-scope (`evil.example`). **IDN and wildcard positive-match cases not exercised.** |
| 8 | Audit log shows `safe_target` decisions for smoke run on `scanme.nmap.org` | NOT MET | `codex_review.md` only references synthetic local fakes (`authorized.local`). No `scanme.nmap.org` smoke artifact cited. |
| 9 | Operator sign-off in `accepted_changes.md` | AMBIGUOUS | `accepted_changes.md` contains a 2026-05-15 Phase 0 entry, but it was authored by Codex as part of the same session, not as a distinct operator approval. Procedurally weak but not an implementation defect. |
| 10 | Cowork-side: update `.hermes.md` Safety Gate to reference `safe_target` / program-scope pattern | NOT MET | `.hermes.md` Safety Gate still references only `config/scope.txt`; `safe_target` is not named. This is Cowork's (this reviewer's) own deliverable per §1.2 — flagging here, not routing to Codex. |
| 11 | Cowork-side: update `HERMES_WORKFLOW.md` routing for scope-touching tasks | NOT MET | Not verified in this pass; same owner caveat as #10. |

---

## Security Findings

Severity legend: **H** = high, **M** = medium, **L** = low/informational.

- **L — `SCOPE_OVERRIDE_TOKEN`/`SCOPE_OVERRIDE_CONFIRM` is "type twice", not two-factor.** Anything setting both env vars in the same shell satisfies the gate. Impact is bounded because acceptance forces `DRY_RUN=true` and every network stage is gated on `$DRY_RUN` (verified across `enum_subdomains`, `find_live_hosts` incl. the ICMP fallback at `recon.sh:596-606`, `port_scan`, `service_fingerprint`, `web_probe`, `dir_bruteforce`, `vuln_scan`, `send_notifications`). Net effect: the override only disables scope filtering for a dry-run-only invocation, which matches the proposal intent. Acceptable for Phase 0; tighten in a later phase if real two-party confirmation is wanted.

- **L — Wildcard scope `*.example.com` also matches the apex `example.com`.** `scope_match` (`recon.sh:421-423`) returns true when `host == base`. Some bug-bounty programs treat the apex as a distinct scope item. Operator-facing semantic, not an exploit. Worth deciding before Phase 1 scope.json work, since Phase 1's `in_scope[]` will need a consistent rule.

- **L — `source "$CONFIG_FILE"` executes `config/recon.conf` with full shell privileges.** Pre-existing, not in Phase 0 scope. Any write-access to that file is code execution at recon.sh launch. Mention here only so it does not get forgotten. Mitigation belongs in a later hardening phase (e.g., parse as key=value).

- **L — `nocasematch` is enabled globally (`recon.sh:14`).** All `[[ ... =~ ... ]]` matches are case-insensitive. `parse_target` already lowercases hosts via `${host,,}` before matching, and `scope_match` lowercases both sides, so no observed bypass. Flagging because future contributors editing regexes here may not realize the implicit case fold.

- **Informational — audit log field separator.** `audit_log` joins fields with `|`. Reason strings now look benign (they come from controlled constants or already-validated targets), but the convention is fragile if future reasons interpolate untrusted text. Consider switching to JSON lines when `logs/audit.log` is next touched.

No high or medium findings.

---

## Validation Gaps

These are the deltas vs. proposal §1.3 exit criteria. They are evidence gaps,
not code defects.

1. **No IDN / punycode case exercised.** `valid_domain` accepts `xn--*` punycode and rejects unicode bytes (which never reach the regex because `parse_target` rejects whitespace/control). Behavior looks correct; it just hasn't been demonstrated in the recorded test matrix.
2. **No wildcard positive-match case exercised.** `scope_match` wildcard logic (`recon.sh:421-423`) is the most subtle branch and has no recorded test row.
3. **No `scanme.nmap.org` smoke run / audit excerpt.** The proposal asks for an audit-log demonstration on this target. A dry-run is sufficient — the requirement is about audit entries, not network behavior. Codex satisfied the spirit (audit entries are produced for synthetic targets) but not the letter.
4. **No record of operator confirming `accepted_changes.md`.** Append by the implementing agent is fine for history; a one-line operator confirmation would close the loop.

---

## Route Back To Codex

**Nothing blocking.** Suggested follow-ups, in priority order, that the
operator may choose to route back as a small Phase 0.1 task rather than
holding Phase 1:

1. Append three test rows: IDN (`xn--bcher-kva.example` against a matching scope entry), wildcard positive (`a.b.example.com` against `*.example.com`), and trailing-dot rejection (`example.com.`). Capture in `codex_review.md` validation block.
2. Run `recon.sh --dry-run --domain scanme.nmap.org` against a scope file that contains `scanme.nmap.org`, and paste the resulting `logs/audit.log` slice into `codex_review.md`.
3. Decide and document the apex-vs-wildcard scope semantic (`*.x.y` includes `x.y`? yes/no) in a one-line note inside `config/scope.txt` header, so Phase 1's `scope.json` schema inherits a clear rule.

Each is <30 minutes of work and does not require any new Codex design.

---

## Recommendation

**Proceed to Phase 1 operator approval.** Phase 0 implementation meets the
hardening requirements; the residual items are validation evidence and a
minor semantic clarification, none of which block subsequent program-intake
work. This reviewer will, as a separate Cowork deliverable, update
`.hermes.md` Safety Gate language and `HERMES_WORKFLOW.md` routing to
reference `safe_target` and the upcoming `programs/<slug>/scope.json`
pattern (proposal §1.2) before Phase 1 routes to Codex.

If the operator prefers a strict reading of the exit criteria, route
items 1–2 above to Codex as a Phase 0.1 finalization pass before
opening Phase 1.
