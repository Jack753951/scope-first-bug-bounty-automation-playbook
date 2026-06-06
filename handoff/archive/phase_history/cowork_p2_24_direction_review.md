> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# P2.24 Direction Review

Date: 2026-05-19
Reviewer: Claude Code MAX/OAuth via `hermes claude-impl` (design-only direction review)
Review tier: T3 direction review, design-only
Milestone: Phase 2 bug-bounty candidate review workflow closeout
Source prompt: `handoff/cowork_p2_24_direction_prompt.md`
Scope note: `handoff/p2_24_core_extraction_scope.md`

## Verdict

DEFER_REFACTOR_AND_CLOSE_PHASE_2

## Rationale

The Phase 2 candidate workflow chain (P2.19 -> P2.23) has reached the intended
trial-only end state. The five consumers each fail closed, reject live-target
flags explicitly, emit compact deterministic JSON, hold their schemas at
`0.1-trial`, and do not promote any item above `blocked` / `needs_manual_review`.
The chain has already proved out the candidate -> review -> gap -> verification
checklist -> report-readiness flow without schema promotion, runtime wiring, or
target interaction.

A pre-closeout helper extraction is not justified at this point because:

1. The duplication is real but bounded. It is concentrated in five places:
   `LIVE_TARGET_FLAGS`, a `*_Error` dataclass-style object, an `_error_payload`,
   a `_compact_emit`, and an `_argv_errors`-style all-args rejection. Combined,
   that is roughly twenty to thirty repeated lines per consumer across at most
   four scripts. None of it is currently causing maintenance pain because no
   consumer has had to change shape after merge.

2. The duplication is load-bearing for safety review. Today each consumer
   declares its own `LIVE_TARGET_FLAGS` and its own argument-rejection posture
   in-file. A reviewer scanning any one script can verify the binding cyber
   safety contract locally, without crossing a `scripts/core/...` import. Moving
   `LIVE_TARGET_FLAGS` and `reject_all_args(...)` into a shared helper would
   silently centralize the denylist for every present and future consumer. That
   is exactly the kind of centralization that becomes an "attractive nuisance"
   when Phase 3 introduces program policy or live-mode work: a single
   parameterized helper that quietly relaxes one flag would weaken all four
   consumers at once. The current pattern forces a deliberate, per-script
   review for any boundary change, which is the conservative posture this
   project has chosen elsewhere.

3. P2.19 and P2.23 are intentionally non-uniform with the P2.20-P2.22 pattern.
   P2.19 reads allowlisted committed fixtures under `--repo-root` and is the
   only consumer with positional flag values; P2.23 chains the helpers in
   memory and accepts `--repo-root` / `--input` / `--json`. A "minimal" helper
   that only fits stdin-only consumers would still leave both file-reading
   consumers managing their own argv parsing. The shared surface is therefore
   smaller than it looks at first glance.

4. The natural moment for a core helper is Phase 3 schema promotion, not now.
   When any `*/0.1-trial` schema graduates to a stable `modules/_schema/...`
   contract, the matching error/payload/emit primitives should be promoted at
   the same time, in the same review, with the same OSS Recon Gate. Extracting
   them before that point risks fixing the helper's shape too early and then
   needing to rewrite it once a real schema appears.

5. Closing Phase 2 cleanly is worth more than a small refactor. P2.25 should
   ask which Phase 3 direction is highest value (real fixture quality, second
   Level 1 module, candidate/evidence UX, report-readiness reviewer prompts),
   and which boundaries must stay locked. That conversation drives the next
   six to ten phases; a "minimal core helper" PR drives one.

This is therefore a defer, not a block. The duplication remains on the radar
and will be revisited when Phase 3 raises a schema, a second policy boundary,
or a third file-reading consumer.

## Duplication Assessment

Confirmed duplicated shapes across P2.19-P2.23 (verified by reading each
script):

- `LIVE_TARGET_FLAGS = frozenset({"--target", "--url", "--host", "--scope", "--live"})`
  appears verbatim in `review_candidate_packet_gaps.py`,
  `build_candidate_verification_plan.py`, `build_report_readiness_gate.py`,
  and `build_candidate_workflow_fixture.py`. P2.19 does not need it because it
  is a file-reader, not a stdin consumer.

- Error-record dataclass-shaped object with `code`, `path`, `message` and an
  `as_dict()` method appears as `PacketError` (P2.19, frozen dataclass),
  `GapError` (P2.20), `PlanError` (P2.21), `GateError` (P2.22), and
  `WorkflowError` (P2.23, additionally carries optional `stage`). These are
  near-identical except for the P2.23 stage tag.

- `_error_payload(errors)` building a `{schema_version, status: "error",
  source_schema_version, summary: <empty>, <items>: [], errors: [...]}`
  envelope appears in P2.20-P2.23 with per-stage `summary` schemas.

- `_compact_emit(payload)` writing `json.dumps(payload, sort_keys=True,
  separators=(",", ":")) + "\n"` to stdout appears in P2.20-P2.23 byte-for-byte
  identical.

- Live-flag rejection that splits `arg.split("=", 1)[0]` before checking the
  denylist appears as `_live_flag_errors` (P2.20), `_argv_errors` (P2.21),
  `_argv_errors` (P2.22), and is woven into `_parse_args` (P2.23).

- Status vocabulary (`blocked`, `needs_manual_review`, `not_ready`,
  `reviewer_decision_required`) is shared but is intentionally specific to
  each stage and should not be centralized prematurely.

- Trial-only README and TRIAL ONLY top-of-file banners are duplicated in
  intent but slightly different in wording; this is acceptable and even
  desirable for review visibility.

Severity of duplication: **moderate but stable**. No consumer has needed an
edit-once-update-all change since the chain landed; the duplication has not
caused a real maintenance event.

Rule-of-three check: barely satisfied for `_compact_emit` and
`_error_payload`; for `LIVE_TARGET_FLAGS` it is satisfied four times but the
safety argument for keeping it duplicated (above) outweighs the DRY argument.

## OSS Recon Gate Notes

Comparisons (design-only, no targets touched, no third-party code imported):

- SARIF (`runs[].results[].level`, `kind`, `properties`).
  Useful pattern: separation between a tool's `level`/`kind` (informational,
  warning, error) and a finding's later promotion state; rich `properties`
  bag for tool-specific data.
  Adopt/adapt/ignore: **adapt later** when a Phase 3 schema is promoted.
  Safety concern: SARIF's `kind` includes promotion-flavored values
  (`fail`/`pass`) that should not leak into trial vocabularies. We must keep
  candidate/triage status (`blocked`, `needs_manual_review`,
  `reviewer_decision_required`, `not_ready`) firmly below confirmed/verified.
  Contract impact for P2.24: none. The current trial vocabulary is already
  non-promotional and aligns with SARIF's "level" philosophy without coupling
  to its shape.

- Nuclei templates / helpers.
  Useful pattern: clean separation between template metadata (tags, severity,
  references) and runtime execution. Helper libraries focused on parsing and
  shaping data, not on driving network behavior.
  Adopt/adapt/ignore: **ignore the runtime**, design only on the helper
  separation idea. Do not adopt anything that makes target interaction easier.
  Safety concern: Nuclei's defaults are target-touching; we explicitly will
  not import or mirror its execution surface.
  Contract impact for P2.24: none. The proposed minimal helper would only
  cover constants and pure payload-shaping primitives, with no execution.

- Semgrep / generic JSON CLI error shapes.
  Useful pattern: stable `{code, path, message}` triple and stable
  `status: "ok" | "error"` envelopes.
  Adopt/adapt/ignore: **already adopted in spirit** by all five consumers.
  Safety concern: none.
  Contract impact for P2.24: confirms the existing per-consumer shape is the
  right shape; promotion to a shared helper does not change the shape.

- DefectDojo / OWASP ZAP finding lifecycles.
  Useful pattern: explicit lifecycle vocabularies (`new`, `under_review`,
  `confirmed`, `false_positive`, `risk_accepted`) and the discipline of not
  letting tool output autopromote.
  Adopt/adapt/ignore: **adapt at the Phase 3 schema-promotion boundary**.
  Safety concern: importing these lifecycles now would invite a confirmed
  status into the trial vocabulary. We must preserve the explicit gap
  between "candidate" and "confirmed" until manual verification policy is
  drafted in a later phase.
  Contract impact for P2.24: none.

Net OSS Recon Gate decision for P2.24: **APPROVE deferral**. None of the
mature references support refactoring before the schemas promote. They all
suggest the same shape we already have, and they would only be worth
re-running at the Phase 3 boundary.

Tier/milestone impact:

- Escalation required: no.
- Can this gate cover later slices: yes, until Phase 3 changes assumptions
  (schema promotion, new consumer category, or live-mode boundary).
- Re-review trigger if assumptions change: a second file-reading consumer
  joining the chain, a fifth stdin consumer joining the chain, a Phase 3
  schema promoting to `modules/_schema/...`, or any new live-target flag
  proposal.

## If Proceeding: Minimal Task Boundary

This section is informational because the verdict is to defer. If a future
phase decides to extract a helper, the boundary should be:

- New file: `scripts/core/offline_consumer.py` only.
- Public surface, in order:
  - `LIVE_TARGET_FLAGS: frozenset[str]` -- exact current value, no additions.
  - `@dataclass(frozen=True) class ConsumerError` with `code: str`,
    `path: str`, `message: str`, and `as_dict()` returning `{"code", "path",
    "message"}` in that order.
  - `def error_payload(*, schema_version: str, errors: list[ConsumerError],
    source_schema_version: str | None = None, summary: dict[str, Any] | None
    = None, extra: dict[str, Any] | None = None) -> dict[str, Any]` returning
    the existing envelope shape byte-for-byte for every existing consumer.
  - `def compact_emit(payload: dict[str, Any], stream=sys.stdout) -> None`
    using `json.dumps(payload, sort_keys=True, separators=(",", ":"))` plus a
    trailing newline.
  - `def reject_all_args(argv: list[str], *, live_message: str,
    arg_message: str) -> list[ConsumerError]` preserving today's
    `arg.split("=", 1)[0]` denylist behavior. No parameter may relax the
    denylist; the helper must hardcode `LIVE_TARGET_FLAGS` membership.

- Forbidden surface (must not exist in this helper, ever, even behind a flag):
  - any file I/O, subprocess, network, socket, target field, schema
    validation, business logic, status promotion, report drafting, runner
    runtime, or recon integration;
  - any "ignore_live_flags", "extra_allowed_flags", or "permissive_argv"
    parameter;
  - any helper for accepting `--repo-root` / `--input` / `--json`, because
    P2.19 and P2.23 must continue to declare their own argument grammars.

- Required guardrails before any consumer migrates:
  1. RED tests in `scripts/test_core_offline_consumer.py` before the helper
     module exists.
  2. Compatibility tests asserting byte-for-byte equality of every existing
     error envelope and every `--target=value` rejection path before and
     after migration. Capture representative payloads from current tests as
     golden fixtures, then assert equality.
  3. Migrate exactly one consumer (suggested: P2.21
     `build_candidate_verification_plan.py`) and run the full
     `python -m unittest discover -s scripts -p 'test_*.py'` suite.
  4. Only after that suite is green, migrate the remaining stdin consumers
     in separate slices.
  5. P2.19 must not be migrated; its file-reading and validator-loading
     paths are out of scope.
  6. P2.23 may keep its custom `_parse_args` and only adopt
     `compact_emit`, `error_payload`, and `ConsumerError`. Its `--repo-root`
     / `--input` parsing must not move into the helper.
  7. Every existing schema version, status value, error code, field name,
     summary counter, and exit code must be preserved exactly.

- Review tier if this is ever pursued: T3 (contract/platform boundary). It is
  not T2 because `LIVE_TARGET_FLAGS` centralization is safety-relevant.

## If Deferring: P2.25 Closeout Questions

Hermes should route P2.25 as a periodic Phase 2 closeout review with the
following questions:

1. **Workflow value.** Did the P2.19 -> P2.23 chain demonstrate enough of the
   intended candidate -> review -> gap -> verification -> readiness flow to
   justify moving on, or are any stages missing a primitive a future Phase 3
   consumer will need (for example, an evidence-locator stage, a redaction
   gate, or a reviewer-notes scaffold)?

2. **Phase 3 priority ranking.** Which of the following should Phase 3
   tackle first, and which should be explicitly deferred?
   - Real offline fixture quality (replace the synthetic
     `expected_findings.json` fixtures with curated, near-real cases that
     stress the full chain).
   - A second Level 1 module fixture (so a second module's
     `validate_finding_evidence` path is exercised end to end).
   - Candidate/evidence UX (operator-facing surfaces for moving a candidate
     toward manual verification without leaving the trial-only boundary).
   - Report-readiness reviewer prompts (structured prompts that a human
     reviewer or Claude/Cowork can answer per gate result, still without
     drafting submission prose).

3. **What not to build next.** Confirm that none of the following will be
   pursued until a separate review explicitly approves them:
   - report generation, report drafting, or report submission adapters;
   - schema promotion of any `*/0.1-trial` document to a stable
     `modules/_schema/...` contract;
   - confirmed/verified status promotion;
   - module-runner / recon / scanner runtime wiring or platform adapters;
   - any live-target flag, callback, OAST, proxy/pivot/transport, or
     network-touching feature, even in lab mode;
   - any helper that parameterizes the live-target denylist.

4. **Boundary locks until operator approval.**
   - `config/scope.txt` remains operator-only.
   - Program policy boundary work (P1.4 stream) remains design-only until
     program-scope contract review.
   - `recon.sh` and `safe_target` semantics remain unchanged.
   - `accepted_changes.md` remains append-only.

5. **Trigger conditions for revisiting P2.24.**
   - Any new file-reading consumer joins the chain (third such consumer).
   - Any new stdin-only consumer joins the chain (fifth such consumer).
   - Any schema promotes out of `0.1-trial`.
   - Any operator-approved change to `LIVE_TARGET_FLAGS` is proposed.
   - Any cross-consumer drift in `_compact_emit`, `_error_payload`, or
     argument-rejection behavior is observed during review.

6. **Independent review cadence.** Should Phase 3 keep the same routing
   (Hermes direction -> Claude/Cowork direction review -> Codex or
   Claude-Code-Impl -> independent implementation review), or should
   T3-and-above slices in Phase 3 always require Claude/Cowork plus a Codex
   secondary review by default? P2.24's lightweight design-only routing
   confirms the current cadence is adequate for narrow direction work.

## Safety Boundary Confirmation

This review is design-only. The reviewer did not:

- run live scans, probes, scanners, fuzzers, exploit tooling, callbacks,
  OAST/relay infrastructure, proxy/pivot tooling, or target-touching
  automation;
- import, vendor, or invoke any third-party scanning code;
- modify `config/scope.txt`, `config/recon.conf`, `recon.sh`, anything under
  `modules/**`, `scripts/*.py`, `tests/**`, `loot/**`, `scans/**`,
  `reports/**`, `.env`, credentials, OAuth, scheduler, billing, deployment,
  or production-side settings;
- promote any `*/0.1-trial` schema, draft any report, add any platform
  adapter, or change any status to `confirmed`/`verified`.

Files this review reads (read-only): `handoff/cowork_p2_24_direction_prompt.md`,
`handoff/p2_24_core_extraction_scope.md`, `handoff/codex_review.md`,
`handoff/review_tiering_policy.md`, `handoff/oss_recon_gate.md`,
`scripts/build_candidate_review_packet.py`,
`scripts/review_candidate_packet_gaps.py`,
`scripts/build_candidate_verification_plan.py`,
`scripts/build_report_readiness_gate.py`,
`scripts/build_candidate_workflow_fixture.py`.

Files this review writes: `handoff/cowork_p2_24_direction_review.md` (this
file) and `handoff/claude_code_result.md` (worker summary stub).

Binding rules from `.hermes.md` preserved: authorization-first, no
exfiltration, no destructive defaults, no silent overwrites, lock discipline,
secrets out of git, report integrity, no production-side changes. None of
these were touched.

## Blocking Issues

None. The verdict is a clean defer; no code, schema, or safety surface is
proposed to change as part of P2.24.

## Non-Blocking Recommendations

1. Add a short "duplication watchlist" note to `scripts/README.md` (or to a
   new `handoff/p2_25_closeout_inputs.md`) capturing the five duplicated
   shapes identified above plus the rationale for not extracting them yet.
   This keeps the deferred decision visible without creating a hidden TODO.

2. When P2.25 closeout completes, write its result to
   `handoff/cowork_p2_25_closeout_review.md` and link it from
   `handoff/accepted_changes.md` so the Phase 2 chain has a single,
   discoverable closing record.

3. Treat any future temptation to add a new stdin-only consumer as a trigger
   to re-run P2.24 rather than to add a fifth `_compact_emit` clone. A
   fifth clone would tip the maintenance argument in favor of extraction.

4. If a P2.24-style helper is eventually written, name it
   `scripts/core/offline_consumer.py` rather than something generic like
   `scripts/core/util.py`. The narrow name discourages drift into general
   utility code that could later host risky helpers.

5. Keep the `_argv_errors` / `_live_flag_errors` differences in P2.20-P2.23
   on the radar. Today they are functionally equivalent and only differ by
   error names and messages. Consolidate the error vocabulary names
   (`LIVE_TARGET_FLAG_NOT_ALLOWED`, `ARGUMENT_NOT_ALLOWED`) as a documented
   convention in `scripts/README.md` even while keeping the implementations
   per-script.

6. Capture, as part of P2.25, an explicit "what Phase 3 must not pull in
   from OSS without an OSS Recon Gate" list. The references in this review
   (SARIF, Nuclei, DefectDojo, ZAP) are appealing but each carries a
   target-touching or promotion-flavored default that must remain rejected
   until a Phase 3 direction review explicitly accepts a narrow piece.
