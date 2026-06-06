> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Cowork Phase 0.1 Independent Review

Date:     2026-05-15
Reviewer: Cowork (Claude, independent reviewer pass)
Scope:    Phase 0.1 validation-evidence closure by Codex for the non-blocking
          follow-ups in `handoff/cowork_phase0_review.md` §"Route Back To Codex"
Inputs:   `handoff/sustained_review_loop.md`, `handoff/cowork_phase0_review.md`,
          `handoff/codex_review.md`, `handoff/phase0_1_validation_evidence.md`,
          `handoff/accepted_changes.md`, `recon.sh`, `bin/hermes`,
          `config/scope.txt`, `config/recon.conf`, `logs/audit.log`, and the
          on-disk temp lab `.tmp_phase0_1_validation_20260515_162146_329/`
Method:   Read-only inspection plus cross-check of claimed audit excerpts
          against the surviving temp lab artifacts. No network tools run.

---

## Verdict

**ACCEPT. No blocking issues. Phase 1 may start.** Codex closed the
non-blocking validation-evidence items from Phase 0 review (`cowork_phase0_review.md`
§"Route Back To Codex" items 1–2) using isolated temp lab roots; every claimed
audit excerpt is reproducible from the surviving on-disk artifacts.
Production `config/scope.txt` was not modified and production
`logs/audit.log` was not polluted by Phase 0.1.

---

## Evidence Matrix

Each row cross-checks an evidence claim in `handoff/phase0_1_validation_evidence.md`
against the actual artifacts on disk and the code path in `recon.sh`.

| # | Claim | Code path | Artifact | Result |
|---|---|---|---|---|
| 1 | `xn--bcher-kva.example` allowed under matching punycode scope | `parse_target` regex at `recon.sh:296` accepts `xn--*` (ASCII), `scope_match` exact-equal at `recon.sh:419` | `.tmp_phase0_1_validation_20260515_162146_329/punycode_allowed/lab/logs/audit.log` shows 4× `SAFE_TARGET_OK` rows for `xn--bcher-kva.example` at `2026-05-15T08:21:47Z` | MATCHES |
| 2 | Raw Unicode `bücher.example` rejected against punycode scope | `valid_domain` regex is ASCII-only (`recon.sh:296`); `parse_target` returns "target is not a supported IP, CIDR, domain, or HTTP(S) URL" | `unicode_idn_rejected/lab/logs/audit.log` shows 1× `SAFE_TARGET_FAIL` with the same reason; target text rendered as `b?cher.example` due to Git-Bash console encoding | MATCHES; rejection path verified |
| 3 | `a.b.example.com` allowed under `*.example.com` | `scope_match` wildcard branch at `recon.sh:421-423` (`host == *.$base`) | `wildcard_deep_allowed/lab/logs/audit.log` shows 4× `SAFE_TARGET_OK` rows at `2026-05-15T08:21:49Z` | MATCHES |
| 4 | `example.com` apex allowed under `*.example.com` (observed) | Same branch, `host == base` clause | `wildcard_apex_observed/lab/logs/audit.log` shows 4× `SAFE_TARGET_OK` rows at `2026-05-15T08:21:51Z` | MATCHES |
| 5 | `example.com.` (trailing dot) rejected | `valid_domain` regex requires non-empty final label | `trailing_dot_rejected/lab/logs/audit.log` shows 1× `SAFE_TARGET_FAIL` with the expected reason | MATCHES |
| 6 | `scanme.nmap.org` dry-run produces audit rows for `initial_target` / `domain_expansion` / `find_live_hosts.input` / `find_live_hosts.output` / `port_scan.input` | `run_pipeline:899` + `enum_subdomains:564` + `find_live_hosts:580,609` + `port_scan:618` | `scanme_dryrun/lab/logs/audit.log` shows exactly those 5 rows at `2026-05-15T08:21:53–54Z` | MATCHES; this is the smoke-evidence gap from Phase 0 review #8 closed |
| 7 | `bash -n recon.sh` exit 0 | — | `handoff/codex_review.md` §"Phase 0.1 Validation Evidence" + script content compiles by inspection | MATCHES |
| 8 | Hermes review exit 0 | `bin/hermes:338` writes `handoff/latest_check.md` | latest run noted in `phase0_1_validation_evidence.md`; warning about `<user-home>` mkdir is consistent with Git-Bash absolute-path handling and does not gate success | MATCHES; limitation is documented |
| 9 | `config/scope.txt` not modified, no live scans, no new recon features | — | `config/scope.txt` headers/entries unchanged; production `logs/audit.log` ends at `2026-05-15T08:05:17Z` (Phase 0 only) — none of the Phase 0.1 `08:21:*Z` rows appear there, confirming HACKLAB isolation worked | MATCHES |

All evidence is reproducible and consistent.

---

## Safety Review

- **HACKLAB isolation worked.** All Phase 0.1 audit rows landed in
  `.tmp_phase0_1_validation_*/lab/logs/audit.log` under the temp lab root.
  Production `logs/audit.log` was not appended to. This is the right pattern
  and should be preserved for future validation passes.
- **No live egress.** Every test case ran with `--dry-run`. `recon.sh` gates
  every network stage on `$DRY_RUN` and the `validate_runtime_flags` accepted
  path forces `DRY_RUN=true`. No `curl`/`subfinder`/`httpx`/`naabu`/`nmap` etc.
  invocation paths could have fired during these tests.
- **No production state touched.** `config/scope.txt`, `config/recon.conf`,
  `recon.sh`, and `bin/hermes` are unchanged for Phase 0.1.
- **IDN rejection is real.** The bash regex character class `[a-z0-9]` is
  ASCII-only regardless of `nocasematch`, so non-ASCII bytes cannot satisfy
  `valid_domain`. The console rendering of `ü` as `?` in audit text is a
  display artifact only — the decision path was rejection, and the audit row
  records `SAFE_TARGET_FAIL` with the unsupported-target reason. Acceptable
  in this sandbox; operators on UTF-8-capable shells will see the real
  glyph.
- **Apex-matches-wildcard is the documented, intended behavior.** `config/scope.txt:8`
  already states this rule in Chinese
  ("`*.example.com (會比對 *.example.com 與 example.com 本身)`"). The
  Phase 0 review treated this as a policy question worth deciding; the
  policy was in fact already declared in code. Phase 1's `scope.json` schema
  can either preserve this rule or break it intentionally with migration
  notes — but it is not undefined behavior today.

No new safety findings beyond those already recorded in `cowork_phase0_review.md`.

---

## Documentation Issues

Non-blocking accuracy notes for `handoff/phase0_1_validation_evidence.md`
and `handoff/codex_review.md` §"Phase 0.1 Validation Evidence":

1. **Audit excerpts are truncated to one row per case** (except `scanme`),
   even though the on-disk audit log holds 4–5 rows per pass case. Not
   wrong, but worth a single line such as "Full row set:
   `<temp>/<case>/lab/logs/audit.log`" so readers know the rest of the
   rows exist and were not omitted because they failed.
2. **Wildcard-semantics recommendation overstates the openness of the
   question.** `phase0_1_validation_evidence.md` §"Wildcard Semantics"
   ("`Recommendation for Phase 1: make this explicit in program-scope policy`")
   reads as if the rule is currently undocumented. It isn't — `config/scope.txt:8`
   already declares "`*.example.com` 會比對 `*.example.com` 與 `example.com`
   本身". Phase 1 is a *change* decision, not a *clarification* decision.
3. **`accepted_changes.md` Phase 0.1 entry is again self-authored** by
   Codex within the same session, not signed by the operator. This carries
   forward the same procedural weakness flagged in `cowork_phase0_review.md`
   gap #4. Not an implementation defect; flag here for completeness.
4. **No CIDR positive test row.** Not requested by `cowork_phase0_review.md`,
   so not a gap — noting only so reviewers don't ask later.
5. **Temp lab not cleaned up.** `.tmp_phase0_1_validation_20260515_162146_329/`
   is still on disk (~6 case dirs, harmless artifacts). Should be removed by
   the operator or by a Codex hygiene pass; the directory name is dotted so
   it won't show up in casual `ls`, but it is real bytes on disk.

None of these block acceptance.

---

## Route Back To Codex

**Nothing blocking.** Optional, low-priority cleanups the operator may bundle
into a Phase 1 prep pass — *not* required before Phase 1 starts:

1. In `handoff/phase0_1_validation_evidence.md` §"Wildcard Semantics",
   reword the recommendation to reference the existing rule in
   `config/scope.txt:8` and frame Phase 1 as a *preserve-or-change* decision.
2. Remove `.tmp_phase0_1_validation_20260515_162146_329/` (operator action;
   trivial `rm -rf` of the dotted dir).
3. Add a one-line "Full audit rows: see `<temp>/<case>/lab/logs/audit.log`"
   pointer under each excerpt block in `phase0_1_validation_evidence.md`.

Each is <5 minutes and pure documentation/hygiene.

---

## Recommendation

**Phase 0.1 is closed. Proceed to Phase 1 operator approval.**

The Phase 0 review's non-blocking follow-ups (IDN row, wildcard positive row,
trailing-dot row, `scanme.nmap.org` dry-run audit excerpt) are all backed by
reproducible on-disk artifacts. The apex-vs-wildcard semantic flagged in
Phase 0 review §3 of "Route Back To Codex" turns out to be already documented
in `config/scope.txt:8`; Phase 1 should pick this up as an explicit
preserve-or-change decision when defining `programs/<slug>/scope.json`
semantics, but it is not a defect today.

No route-back is required before Phase 1. The three optional cleanups above
can ride along with Phase 1's first Codex task.
