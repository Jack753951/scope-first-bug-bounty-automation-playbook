> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# P2.19 Direction Review — Bug-Bounty Candidate Review Packet

Date: 2026-05-18
Reviewer route: Claude Code MAX/OAuth (read-only direction review)
Target output path (for Hermes to persist): `handoff/cowork_p2_19_direction_review.md`
API-backed Claude/Cowork: not used; no `ANTHROPIC_API_KEY` consumed.

## Decision

**ACCEPT_WITH_CHANGES**

The strategic redirection back to bug-bounty after P2.18 is correct and overdue: CTF calibration (P2.17/P2.18) has converged and should not keep claiming roadmap. The proposed candidate review packet is a low-risk, high-leverage offline projection of the already-stable `finding/1.0` contract: it converts the committed P2.16 candidate-finding fixtures into a deterministic review bundle without touching live targets, schemas, or runtime. Accept Option A (builder now) with the bounded changes below — primarily a tightened input allowlist, a deterministic `review_questions` generator, a deterministic `report_readiness` rubric, and tests that pin all of the above.

Do **NOT** promote the packet to a versioned `modules/_schema/` file in this slice. The whole point of the `-trial` suffix is to discover gaps before contract lock-in, matching the P2.18 precedent.

## Tier and Boundary Confirmation

- **Tier: T3 (Contract/platform boundary, design-with-implementation).** Correct as proposed. Even though the packet is a projection rather than a new artifact contract, it codifies the interface that future report-drafting steps will consume. T3 direction-review-before-implementation is the right gate.
- **Boundary: offline/local only.** Confirmed. The builder must not import from `scripts/module_runner.py`, `scripts/validate_module_io_*`, `scripts/program_policy_boundary.py`, `recon.sh`, scanner adapters, or any runtime path. Standard library only.
- **No schema promotion.** Confirmed. `candidate_review_packet/0.1-trial` is intentionally weaker than a JSON Schema (no `$schema`, no `$id`, no `additionalProperties`-style closure beyond the builder's flat allowlist). Promotion to `modules/_schema/candidate_review_packet.schema.json` is deferred to P2.20+ after two real consumers exist.
- **No runtime coupling.** Builder must not be invoked by any runner, hook, CI, recon path, or scheduler in this slice. It is an operator-run utility only.
- **No status escalation.** Builder MUST NOT promote `status` from `candidate`/`needs_verification` to `confirmed`/`verified`/`accepted` anywhere in its emitted JSON, summary counters, or `report_readiness` field. Reuse the `FORBIDDEN_STATUSES` constant from `scripts/validate_finding_evidence.py` (lines 70-71) for parity.

## OSS References Considered (Recon Gate)

Five mature references compared. None copied wholesale.

| Reference | Decision | Why |
|---|---|---|
| **DefectDojo import/review lifecycle** (`active`, `verified`, `false_positive`, `out_of_scope`, `inactive`, plus engagement → test → finding hierarchy) | **Adapt narrowly** | Adopt only the *concept* of a review-state envelope distinct from the finding itself. **Explicitly reject** the `verified` state name (already a `FORBIDDEN_STATUSES` member) and the `false_positive` shortcut — both would let a builder make a triage decision. The packet must remain a *view* over `finding/1.0`, not a parallel state machine. Borrow the engagement→test→finding nesting only insofar as the packet groups findings by `source.module_id` + `source.run_id`. |
| **SARIF `result.kind` / `result.level` separation** (kind: pass/fail/open/informational; level: error/warning/note/none) | **Adapt** | The kind-vs-level split is already mirrored in `finding/1.0` (`status` vs `severity_hint`) plus `confidence` as a third axis. The packet must preserve all three axes verbatim — no merging into a single "priority" score, no synthesized fields. Reinforces the no-new-axes rule. |
| **<bug-bounty-platform> / Bugcrowd report quality conventions** (publicly documented: title, summary, impact, reproduction steps, suggested fix, severity rubric per program) | **Adapt — read-only checklist only** | The reviewer-checklist concept (does the finding have title, scope, evidence, CWE, repro steps?) is the right *shape* for the packet's `review_questions` list. **Do NOT** copy platform-specific severity rubrics, program rules, or report templates. The packet must remain platform-neutral; <bug-bounty-platform>/Bugcrowd platform adapters are a later slice and are explicitly forbidden here. Do NOT name either platform in the source or fixtures. |
| **Semgrep finding metadata + `metadata.confidence`** | **Already adopted; ignore for new fields** | `confidence: low/medium/high` already exists in `finding/1.0` and is preserved verbatim. Do not add a `dev_metadata` vs `user_metadata` split — premature for this slice. |
| **Nuclei template info metadata** (`info.severity`, `info.classification.{cve, cwe, cvss}`, `info.tags`, `info.reference`) | **Already adopted; ignore for severity reuse** | Nuclei doesn't have a packet concept. Severity/CWE/references are already on `finding/1.0`. **Explicitly do NOT** introduce a Nuclei-style `info.severity` shadow on the packet — keep `severity_hint` only. |

Optional sixth reference noted but not adopted: **OWASP DefectDojo `import-scan` JSON schema** — useful as a future export target for a later adapter slice, but mixing import-schema vocabulary here would prematurely commit to DefectDojo coupling. Revisit only if P2.20+ adds a platform adapter.

Optional seventh reference noted but not adopted: **GitLab Secure JSON report format** — fixed `vulnerabilities[]`/`scan` shape is closer to a scanner output than a review packet; wrong layer for this slice.

## Answers to Required Review Questions

**1. Is this the right next bug-bounty-focused slice after P2.18?**
Yes. The P2.16 module already produces committed `expected_findings.json` candidate fixtures (six under `tests/fixtures/security_headers_baseline/*/expected_findings.json` — verified). Without a packet layer those fixtures have no downstream consumer that exercises the manual-verification + scanner-output-only contract end-to-end. The packet is the smallest offline step that gives reviewers a single artifact to look at before any future drafting. Alternatives considered and deferred:
- A scope-coverage report — depends on program scope contract not yet built.
- A confirmed-finding promotion helper — explicitly out of bounds; promotion is a human step.
- A program scope schema slice (`program/1.0`) — bigger T3+ scope; do after the packet has proven shape.

**2. Should this be a builder now, or design-only first?**
**Builder now (Option A).** Rationale:
- Inputs already exist and are stable (6 fixtures × `finding/1.0`).
- `scripts/validate_finding_evidence.py` provides the semantic guard; reuse rather than redesign.
- The `-trial` schema-version suffix gives the same escape valve P2.18 used for the verifier metadata template — no contract lock-in.
- Design-only would defer a measurable artifact for no concrete information gain; the unknowns (review-question vocabulary, readiness rubric) are best discovered by writing tests against real fixtures.

**3. Should the packet be a trial `candidate_review_packet/0.1-trial` document or reuse an existing schema?**
**Trial `candidate_review_packet/0.1-trial`.** Reasons:
- The packet is a *projection* of `finding/1.0`, not a new artifact contract — reusing `finding/1.0` would silently expand that schema's semantics.
- The `-trial` suffix matches the P2.18 precedent and signals "do not consume as a stable contract."
- No file under `modules/_schema/` in this slice. The builder source must contain a header comment: `# TRIAL ONLY — schema promotion deferred to P2.20+ after two real consumers exist`.
- The packet `schema_version` string MUST be literally `candidate_review_packet/0.1-trial` (pinned by test 11 below). No `0.1`, no `1.0`, no `0.2-trial`.

**4. Which input fixture paths should be allowed initially?**
Initial allowlist (enforced by the builder, not just by convention):
- `tests/fixtures/security_headers_baseline/*/expected_findings.json` (the six P2.16 committed outputs)
- *Optionally* `tests/fixtures/candidate_review_packet/**/expected_findings.json` for builder-self-test fixtures.

Builder must REJECT (with structured error codes):
- Any path under `runs/`, `scans/`, `loot/`, `evidence/`, `programs/`, `config/`, `.env`, `setting/local/` → code `INPUT_PATH_NOT_ALLOWED`
- Absolute paths → code `INPUT_PATH_MUST_BE_RELATIVE`
- Paths containing `..` segments → code `INPUT_PATH_TRAVERSAL`
- Paths containing `\`, `://`, NUL → code `INPUT_PATH_UNSUPPORTED_CHARS`
- Paths whose canonical realpath escapes `--repo-root` → code `INPUT_PATH_OUTSIDE_REPO`
- Paths under symlinked directories (resolved-vs-declared mismatch) → code `INPUT_PATH_SYMLINK_REFUSED`

Builder must REQUIRE an explicit `--repo-root` flag (mirroring `scripts/validate_preview_ledger.py`'s pattern) and must not fall back to cwd.

**5. What review questions should be generated per finding?**
Deterministic, derived from the finding shape — no freeform text generation, no LLM, no environment lookups. Each question is a fixed template populated with finding fields. Required minimum set (each emitted only when applicable; sorted, deduplicated):

1. `scope_in_authorized_scope` — `"Confirm target.value '{target.value}' (type={target.type}) is within the program's authorized scope at the run window."`
2. `policy_decision_freshness` — `"Confirm source.policy_decision_sha256 '{sha}' is still the current allow artifact for module_id '{module_id}'."`
3. `manual_verification_executed` — `"Confirm an authorized response has been manually inspected per verification_guidance before drafting."`
4. `evidence_sufficiency` — when `evidence_ref_count == 0`: `"No evidence refs are attached. Capture a manual evidence file before drafting, or leave as candidate-only."` When `> 0`: `"Confirm the {n} attached evidence refs are redacted and sufficient for the report kind."`
5. `severity_calibration` — `"Compare severity_hint='{severity}' against the program's severity rubric (program-specific, not platform-defined)."`
6. `cwe_classification_check` — emitted only when `classifications.cwe` is non-empty: `"Confirm CWE classifications {cwes} accurately describe the observed condition."`
7. `confidence_floor` — emitted only when `confidence == "low"`: `"Confidence is low; either raise it with additional verification or keep this finding off the draft."`
8. `status_guardrail` — always emitted, **last in the list**: `"This packet does NOT promote status from '{status}'. Promotion to confirmed/verified is a separate human step."`

Builder must NOT generate questions that:
- Mention <bug-bounty-platform>, Bugcrowd, or any specific platform
- Suggest a status transition or score
- Reference live network state, DNS, or third-party services
- Embed remediation rewrites or templated report prose

The `review_questions` array is sorted alphabetically by question key for determinism. Each entry is `{key, text}` — flat, no nesting.

**6. What tests are mandatory before implementation?**
Mandatory minimum set. Each test pins deterministic expected output (or expected structured error code where applicable).

1. **Happy path × multiple fixtures**: invoke the builder on `tests/fixtures/security_headers_baseline/all_headers_absent/expected_findings.json` plus one other P2.16 fixture → exit 0, deterministic JSON, `summary.candidate_count` matches manually-counted findings.
2. **Single-file happy path**: invoke on one fixture only → identical packet shape, single-module summary, sorted findings.
3. **Empty inputs (zero findings)**: invoke on a builder-self-test fixture with `[]` → `status: ok`, empty `findings` array, `summary.candidate_count: 0`, no errors.
4. **Determinism**: running the builder twice on the same inputs produces byte-identical stdout (no timestamps, no random ordering, JSON keys sorted, `findings[]` sorted by `id` then by `target.value`).
5. **Order-independent multi-file run**: linting `A B` vs `B A` produces identical JSON (because both are sorted).
6. **Validation reuse**: each input finding is checked through `scripts/validate_finding_evidence.py`'s `validate_data(finding, "finding")` path; invalid findings appear in `errors[]` with code `FINDING_VALIDATION_FAILED` and do NOT appear in `findings[]`. Test with a deliberately broken builder-self-test fixture.
7. **Forbidden status detection**: a builder-self-test fixture containing `status: "confirmed"` → rejected with code `FORBIDDEN_STATUS`, finding excluded from `findings[]`. Mirror the `FORBIDDEN_STATUSES` constant exactly.
8. **Input path allowlist**: pass `runs/x/y.json` or an absolute path or `../etc/passwd` → rejected with the appropriate `INPUT_PATH_*` code, exit non-zero.
9. **Repo root required**: invoke without `--repo-root` → argparse error, no traceback to user. Invoke with `--repo-root` pointing at a directory that doesn't contain the input → `INPUT_PATH_OUTSIDE_REPO`.
10. **No filesystem writes**: assert that running the builder creates no new files under cwd, the temp dir, or `--repo-root` (parametrize across both happy and deny paths).
11. **Schema-version pin**: assert the literal string `"candidate_review_packet/0.1-trial"` appears in source exactly once (the constant), and the emitted packet's `schema_version` matches. Assert no occurrence of `candidate_review_packet/0.1` (unsuffixed), `candidate_review_packet/1.0`, or `candidate_review_packet/0.2` anywhere.
12. **Manual-verification gate preserved**: each finding's `triage.manual_verification_required` and `triage.scanner_output_only` carry through to the packet's `manual_verification_required` and `scanner_output_only` flags unchanged. A finding whose triage flags are not both `true` is rejected (consistent with `finding/1.0` schema).
13. **Report-readiness rubric**: deterministic mapping pinned by tests. Recommended rubric (open to operator adjustment):
    - `report_readiness: "not_ready"` if `evidence_ref_count == 0` OR `confidence == "low"` OR `severity_hint == "info"`
    - `report_readiness: "reviewer_decision_required"` otherwise
    - **Never** emit `report_readiness: "ready"`, `"approved"`, or `"draft"` in this slice — those would imply promotion authority the packet does not have.
14. **Aggregation determinism**: `summary.targets[]` and `summary.modules[]` are sorted, deduplicated, and exactly equal to the distinct values seen in inputs.
15. **Review-questions determinism**: each finding's `review_questions[]` is generated deterministically from the finding fields; running twice on the same fixture produces identical question lists. Test each conditional (evidence_ref_count == 0, confidence == low, classifications.cwe non-empty) individually.
16. **Network/subprocess/file-write AST guard**: the builder source must not import `socket`, `http`, `http.client`, `urllib`, `urllib.request`, `urllib3`, `requests`, `httpx`, `subprocess`, `asyncio`, `selectors`, `ssl`, `pathlib.Path.write_*` calls, `open(..., "w")` patterns, or `os.system`/`os.popen`. Assert via AST walk in the test file (mirror the approach used by `scripts/test_security_headers_baseline.py` — verified pattern from P2.16).
17. **No runtime imports**: builder must not import from `scripts.module_runner`, `scripts.validate_module_io_bundle`, `scripts.validate_module_io_contract`, `scripts.program_policy_boundary`, `scripts.module_input_contract`, `scripts.module_result_contract`, or any module under `modules/checks/`. Allowed: `scripts.validate_finding_evidence` (read-only validation reuse), and only its `validate_data` function — not `validate_bundle`, not the CLI `main`.
18. **No platform name leak**: assert that the literal strings `<bug-bounty-platform>`, `Bugcrowd`, `Synack`, `Intigriti`, `YesWeHack` do not appear in source, tests, fixtures, or emitted packets (case-insensitive grep).
19. **Trial-only header comment present**: assert the builder source contains a `# TRIAL ONLY — schema promotion deferred to P2.20+` comment within the first 20 lines.
20. **No schema files added**: assert no new file under `modules/_schema/` was created in this slice.

**7. How should this packet support later report drafting without becoming a report generator yet?**
The packet is the *input contract* for any future report-drafting step, not the report itself. Specifically:
- **What the packet provides**: deterministic, validated, redacted-evidence-only, candidate-status-only JSON keyed by finding `id`, with a reviewer checklist (`review_questions`) and an advisory `report_readiness` field. This is what a future drafter would consume.
- **What the packet does NOT do**: no Markdown, no HTML, no PDF, no template strings, no remediation rephrasing, no severity-to-score translation, no platform-specific shaping, no auto-population of report titles or impact statements, no status promotion.
- **What protects the boundary**: tests 7, 11, 13, 18, 20 above. In particular, `report_readiness` never has a value that implies authority to draft; the worst the packet can say is "reviewer decision required."
- **What a future drafter slice would need**: a separate T3+ direction review covering (a) program-scope contract, (b) platform adapter, (c) human-gated promotion step, (d) report template registry. None of those exist yet; the packet must not anticipate their shape.

## Recommended Deliverables (Final)

1. `scripts/build_candidate_review_packet.py`
   - Standard-library only. `argparse`-driven: `--repo-root <path>` (required), `--input <path>` (repeatable, required at least once), and `--json` (advisory; output is always JSON).
   - Reads one or more allowlisted `expected_findings.json` files, validates each finding via `scripts.validate_finding_evidence.validate_data`, derives `review_questions` and `report_readiness` deterministically, emits one packet to stdout, exits 0 only if `status == "ok"` and no `errors[]`.
   - Header comment: `# TRIAL ONLY — schema promotion deferred to P2.20+; do not consume as a stable contract.`
2. `scripts/test_candidate_review_packet.py` — covers tests 1–20 above.
3. `tests/fixtures/candidate_review_packet/` — minimal builder-self-test fixtures for the negative-path tests (forbidden status, invalid finding, empty findings). **Do NOT** duplicate the P2.16 fixtures; consume them in place from `tests/fixtures/security_headers_baseline/`.
4. `scripts/README.md` — add an entry for `build_candidate_review_packet.py` noting trial-only status, offline-only, stdout-only.
5. `handoff/accepted_changes.md` — record worker route, verification result, and that schema promotion is explicitly deferred to P2.20+ after two real consumers exist.

Explicitly **NOT** in this slice:
- No `modules/_schema/candidate_review_packet.schema.json` (deferred).
- No registry/profile/manifest entry, no `module.json` for the builder (it is not a module).
- No update to `finding/1.0`, `evidence/1.0`, `run/1.0`, `preview_manifest/1.0`, or `preview_ledger/1.0`.
- No new fixtures under `runs/`, `scans/`, `loot/`, `evidence/`, `programs/`.
- No platform adapter, no Markdown emitter, no PDF emitter, no GitHub issue/PR helper.

## Forbidden Changes (Confirmed)

- No live scans, HTTP, sockets, DNS, callbacks, exploit attempts, fuzzing, brute force, OAST, or any target-touching behavior.
- No subprocess execution. No `os.system`, `os.popen`, `subprocess.*`, `asyncio.create_subprocess_*`.
- No filesystem writes by the builder anywhere — stdout only. A separate direction review (P2.20+) may authorize output paths under `runs/<run_id>/review_packet/`.
- No imports from `scripts/module_runner.py`, `scripts/validate_module_io_bundle.py`, `scripts/validate_module_io_contract.py`, `scripts/program_policy_boundary.py`, `scripts/module_input_contract.py`, `scripts/module_result_contract.py`, `recon.sh`, or any scanner/module runtime path. Allowed only: `scripts.validate_finding_evidence.validate_data`.
- No new JSON Schema file under `modules/_schema/`. No registry entry, no runner wiring, no recon wiring, no CI/hook/scheduler/pre-commit wiring, no `bin/hermes` integration, no `.github/` workflow changes.
- No promotion of any field to `finding/1.0`, `evidence/1.0`, `run/1.0`, `preview_manifest/1.0`, or `preview_ledger/1.0` contracts.
- No status escalation: builder must never emit `confirmed`, `verified`, or `accepted` in any field, summary counter, or `report_readiness` value.
- No platform adapters, no platform-name strings, no platform-specific severity rubrics, no report templates, no Markdown/HTML emission.
- No reading from `runs/`, `scans/`, `loot/`, `evidence/`, `programs/`, `config/`, `.env`, `setting/local/`, absolute paths, or `..`-containing paths.
- No notifications, no GitHub issue/PR creation, no Slack, no webhooks, no OAuth, no credentials, no tokens.
- No changes to `config/scope.txt`, `loot/`, `.env`, credentials, scheduler, deployment, billing, or production settings.
- No CTF tooling changes — `setting/local/ctf/`, `templates/ctf_verifier_metadata.yaml`, `tests/fixtures/ctf_*`, and the P2.17/P2.18 helpers stay untouched.
- No use of `ANTHROPIC_API_KEY`-backed Claude/Cowork. This slice does not justify it — the work is pure standard-library + deterministic fixtures, ideal for Claude Code MAX/OAuth plan-backed capacity (`handoff/model_usage_routing_policy.md` lines 86–97).
- No invocation of the new builder by any existing script, runner, hook, or CI step in this slice.
- No tolerance for unknown packet fields. If the builder discovers a future-compat need, that is a P2.20+ schema-promotion conversation, not a silent expansion.

## Suggested Worker Route

**Primary: Claude Code MAX/OAuth implementation + Hermes verification.**

Rationale:
- Identical shape to P2.17 and P2.18, where this route succeeded twice in succession (`handoff/accepted_changes.md` 2026-05-18 entries: 218 OK then 254 OK / 8 skipped, no Codex fallback needed).
- Pure standard-library work with deterministic fixtures and a closed input contract — ideal for Claude Code's plan-backed capacity.
- No `ANTHROPIC_API_KEY` consumption, which respects the active model-routing policy (prefer Claude Code MAX/OAuth; API-backed Claude only for high-value cases).
- The validation reuse (`validate_finding_evidence.validate_data`) is a single, well-documented function — no need for cross-module reasoning that would push the implementer toward API-backed Claude.

**Fallback: Codex/GPT for surgical fixes** if Claude Code is blocked on (a) the review-questions vocabulary, (b) the readiness rubric branches, or (c) AST-guard test wiring.

**Hermes verification contract** (per `model_usage_routing_policy.md` lines 56–63):
1. `git status --short` + targeted diff review on `scripts/build_candidate_review_packet.py`, `scripts/test_candidate_review_packet.py`, any new fixtures under `tests/fixtures/candidate_review_packet/`, and the `scripts/README.md` entry.
2. `git diff --check` on all touched files (CRLF-only warnings tolerated per recent history).
3. `python -m py_compile` on the new builder and test files.
4. `python -m unittest scripts.test_candidate_review_packet` — focused tests must pass.
5. `python -m unittest discover -s scripts` — full suite must remain green (current baseline: 254 OK, 8 skipped per the 2026-05-18 entry).
6. AST/grep verification that the new builder does NOT import `socket`, `http`, `urllib`, `requests`, `httpx`, `subprocess`, `asyncio`, `selectors`, `ssl`, or anything from the forbidden runtime modules listed above.
7. Grep verification that no `<bug-bounty-platform>`/`Bugcrowd`/`Synack`/`Intigriti`/`YesWeHack` string leaks into source, tests, fixtures, or expected outputs.
8. Confirm no new file under `modules/_schema/` was added.
9. Smoke run: `python -m scripts.build_candidate_review_packet --repo-root . --input tests/fixtures/security_headers_baseline/all_headers_absent/expected_findings.json` and verify deterministic JSON.
10. Update `handoff/accepted_changes.md` with worker route + verification result + the fact that schema promotion is explicitly deferred to P2.20+.

## Promotion Criteria for P2.20+ (Out of Scope for This Slice)

Record but do not act on:
- If two distinct downstream consumers (e.g., a future report-draft helper AND a triage-summary helper) successfully consume `candidate_review_packet/0.1-trial` without requiring vocabulary changes, the packet is a candidate for schema promotion in P2.20+.
- If either consumer requires vocabulary not in this trial, the gap report (saved to `handoff/`) is the deliverable, and schema promotion is deferred again.
- Schema promotion requires a separate T3+ direction review with its own OSS Recon Gate (re-check SARIF/DefectDojo/<bug-bounty-platform> evolution at that time).
- A future "write the packet to `runs/<run_id>/review_packet/`" step is a separate slice that requires its own direction review covering run-id provenance, evidence-path containment, ledger entries, and overwrite policy. **Do not preempt that design here.**
- A future platform adapter (<bug-bounty-platform>/Bugcrowd/etc.) is a separate slice that requires a program-scope contract, severity-rubric source, and platform credentials handling. **Explicitly out of scope for the packet.**

---

**End of P2.19 direction review.** Hermes: please persist the above content verbatim to `handoff/cowork_p2_19_direction_review.md`. No file writes were performed by the reviewer; no `ANTHROPIC_API_KEY` was consumed; route was Claude Code MAX/OAuth read-only.
