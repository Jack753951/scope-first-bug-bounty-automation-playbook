> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Cowork Direction Review — SOC Evidence-Bucket Fixture / Reviewer Alignment

Date: 2026-05-20
Reviewer: Claude / Cowork (direction review only)
Source prompt: `handoff/cowork_soc_evidence_bucket_direction_prompt.md`
Source lessons: `handoff/trygovme_soc_sim_lessons_20260520.md`, `notes/daily/2026-05-20.md`
Repo truth consulted: `.hermes.md`, `handoff/active_strategy_queue.md`, `handoff/review_tiering_policy.md`, `handoff/multi_party_review_decision_policy.md`, `handoff/oss_recon_gate.md`, `templates/report_readiness_reviewer_prompts.json`, `programs/_examples/sample-lab/scope.json`

Posture: design-only. No implementation. No code, scope, schema, module, runner, report, scheduler, credential, OAuth, or production change is approved by this review.

---

## 1. Final verdict

`PROCEED_FIXTURE_ONLY` — accepted as a narrowed, non-contractual variant.

The smallest useful slice that converts the simulator lesson into project capability is a synthetic/redacted offline fixture set plus the small amount of documentation and tests needed to make the fixture meaningful for future review. The reviewer-gap catalog (Option 2) and the trial-consumer design plan (Option 3) are explicitly deferred to separate future direction reviews. They are not folded into this slice.

Rationale:

- Fixtures ground the lesson in concrete, inspectable data without touching any workflow contract.
- A reviewer-gap catalog (Option 2), while useful and parallel in spirit to `templates/report_readiness_reviewer_prompts.json`, is best evaluated *after* the fixture exists, because the catalog vocabulary should be calibrated against real synthetic examples rather than against a CTF anecdote.
- A trial-consumer plan (Option 3) prematurely shapes future executable behavior. Per `.hermes.md`, a no-code plan that materially defines a future consumer surface is still a contract preview and should not be approved before the fixture phase shows what is actually needed.
- `DEFER` (Option 4) loses too much of the freshly-captured lesson before any durable artifact exists.
- `BLOCK` (Option 5) is not warranted — the proposed boundary stays offline, synthetic, and non-executable.

Recommended slice name: `P3.11 — SOC evidence-bucket synthetic fixture (offline, non-contractual)`.

---

## 2. Recommended review tier and why

Tier: **T2** (standard implementation: offline fixtures, docs, tests).

Why T2 and not T3:

- The slice adds no new schema under `modules/_schema/`, no module manifest, no runner surface, no report contract, no consumer, no candidate-workflow field, and no validator that becomes a runtime gate.
- The fixture's field names are descriptive *examples*; they do not define a contract the rest of the codebase must honor.
- Tests assert the *fixture's own well-formedness* (loads as JSON/YAML, has the documented fields, gap codes match the in-fixture vocabulary) — not a system contract.

Escalation triggers that would force T3 (and must therefore be avoided in this slice):

- introducing a Python module / validator under `scripts/` that other code imports as a vocabulary source of truth
- wiring fixture field names into existing candidate workflow consumers
- promoting any field set under `modules/_schema/` or any `*/0.1-trial` schema location
- creating a reviewer-prompt JSON loaded by an existing consumer
- adding tests that assert a *production* contract uses these field names

If during implementation any of those triggers appears unavoidable, the slice must stop and re-enter a fresh T3 direction review.

---

## 3. OSS Recon Gate adopt/adapt/ignore notes

Strictly speaking, the OSS Recon Gate is mandatory at T3+. This slice is T2. However, because the fixture's field choices could influence a future T3 evidence/finding-contract slice, this review records light adopt/adapt/ignore notes now so the future contract review does not re-derive them from scratch.

Review tier: T2 (gate not formally required, attached as informational baseline).
Milestone: Post-P3.10 project workflow calibration.

Relevant references:

- **MITRE ATT&CK (Enterprise) tactic / technique / sub-technique**
  - Useful pattern: tactic and sub-technique IDs as the canonical labeling vocabulary; sub-technique preference over parent.
  - Adopt/adapt/ignore: **Adopt** as fixture vocabulary for `attack_tactic`, `attack_technique`, `attack_subtechnique` fields and the `PARENT_TECHNIQUE_TOO_BROAD` gap code.
  - Safety concern: ATT&CK strings must remain *labels for review*, never automatic findings. The fixture must not embed a "confirmed technique" boolean. Do not import or vendor any ATT&CK STIX bundle into the runtime path.
  - Contract impact (future): a later T3 contract slice could add an `attack_taxonomy` evidence sub-object with confidence; this review does not approve that.

- **Sigma rule / Elastic detection rule evidence fields**
  - Useful pattern: per-event context (host, user, process image, command line, source/destination addresses, timestamps).
  - Adopt/adapt/ignore: **Adapt.** Reuse the event-context *concept* (host, user, process, command line, source/destination) as fixture fields. Do not adopt Sigma's detection rule semantics, log-source naming conventions, or matching language. The fixture is an evidence-bucket fixture, not a detection rule.
  - Safety concern: Sigma examples often assume an active SIEM pipeline. Strip any wording that implies live ingestion.
  - Contract impact (future): event-context field naming may inform a future evidence-record schema slice.

- **STIX 2.1 / OpenCTI observables and relationships**
  - Useful pattern: observable types (file, process, network-traffic, user-account), relationship verbs, confidence scoring, marking/source refs.
  - Adopt/adapt/ignore: **Adapt** the *concept* of typed observables and a confidence value (`evidence_confidence: low | medium | high`). **Ignore** the full STIX object/relationship graph for this slice — it is overweight for a fixture. **Ignore** STIX marking definitions; redaction posture in this repo is set elsewhere.
  - Safety concern: STIX bundles commonly include indicator-of-compromise lists that look like live targets. The synthetic fixture must use clearly non-real values (e.g., RFC 5737 / RFC 2606 / RFC 3849 reserved ranges and example.tld names) and must not look like a real IOC feed.
  - Contract impact (future): typed-observable concept may inform a later evidence-schema review.

- **SARIF (Static Analysis Results Interchange Format) `result.locations` / `result.message`**
  - Useful pattern: a result object that carries a message, location-style context, severity, and rule identifier; explicit separation of `level` (severity) from `kind` (status).
  - Adopt/adapt/ignore: **Adapt** the *shape* — each fixture stage carries `description`, `evidence_records[]`, a `gap_codes[]` field, and a non-promotional `status` enum. **Ignore** SARIF's code-location-centric `physicalLocation` model; an incident timeline is not source-code analysis.
  - Safety concern: SARIF tooling tends to surface results as "findings." The fixture must keep its `status` strictly in the non-promotional vocabulary (`needs_more_evidence`, `needs_mapping_review`, `needs_asset_reconciliation`, `needs_second_pass_hunt`, `not_report_ready`) and must not include a `confirmed_finding` boolean.
  - Contract impact (future): the `result + rule` separation could inform a future report-readiness gate's result-record shape.

- **DefectDojo / <bug-bounty-platform> / Bugcrowd reviewer-workflow concepts**
  - Useful pattern: reviewer feedback as structured gap categories rather than free-text; explicit non-report-ready states.
  - Adopt/adapt/ignore: **Adapt** the *concept* of structured reviewer gap codes as fixture metadata (mirroring the existing `templates/report_readiness_reviewer_prompts.json` data-only pattern). **Ignore** anything related to submission automation, platform adapters, ticket sync, or external-side-effect workflows. No <bug-bounty-platform>/Bugcrowd/DefectDojo API client, library, importer, or exporter is approved by this slice.
  - Safety concern: these platforms exist to *publish* findings. Importing their reviewer-state vocabulary uncritically risks giving fixture stages a "ready to submit" connotation. Keep all states in the deliberately non-promotional vocabulary.
  - Contract impact (future): a separate, later catalog slice may codify gap-code metadata akin to `templates/report_readiness_reviewer_prompts.json`.

Contract impact summary (informational, fixture slice does not change any contract):

- Program scope: unchanged.
- Policy decisions: unchanged.
- Finding schema: unchanged.
- Evidence schema: unchanged.
- Run manifest: unchanged.
- Module manifest / profile / I/O preview: unchanged.
- Dry-run runner: unchanged.

Safety decision:

- Offline-only preview possible: yes.
- Requires active behavior: no.
- Requires new policy gate: no.
- Requires schema migration: no.

Re-review trigger if assumptions change: any attempt to wire fixture field names into a runtime consumer, a candidate-workflow contract, a schema under `modules/_schema/`, a report-readiness gate, or a reviewer-prompt JSON loaded by existing code requires a fresh T3 direction review with a full OSS Recon Gate.

---

## 4. Exact allowed implementation boundary

The implementation slice that may follow this review may:

- Add one or more synthetic incident-timeline fixture files under a new offline fixture path (suggested: `fixtures/soc_evidence_bucket/` — to be confirmed by the next implementation task). The fixture must contain at least one multi-stage incident timeline using deliberately synthetic, redacted, reserved-range values.
- Use the evidence-bucket field names listed in §6 below as the fixture's *internal* vocabulary.
- Use the non-promotional gap-code and status vocabulary listed in the prompt and reproduced in §6 below as the fixture's *internal* labels.
- Add a `README.md` (or equivalent) inside the fixture directory that:
  - states the fixture is synthetic and non-promotional
  - states it is not a real finding, not a real IOC list, and not target-touching
  - states the fixture is not a contract: other code must not depend on these field names
  - explains the non-promotional state vocabulary
  - explicitly forbids substituting real lab credentials, real TryHackMe data, real screenshots, or real captured logs into the fixture
- Add `scripts/test_soc_evidence_bucket_fixture.py` (or equivalent test) that:
  - parses the fixture
  - asserts each stage carries the documented fields
  - asserts every `gap_codes[]` value comes from the documented in-fixture vocabulary
  - asserts every `status` value comes from the documented non-promotional vocabulary
  - asserts host/network values fall inside reserved/synthetic ranges (RFC 5737 / RFC 2606 / RFC 3849 / `example.tld`) — this is the unsafe-defaults negative test
  - asserts no `confirmed_finding`, `submit_ready`, `report_ready`, `live_target`, or equivalent promotional field is present
- Update `handoff/accepted_changes.md` (append-only) with the slice summary, files added, validation performed, and safety boundary.
- Update `handoff/active_strategy_queue.md` to reflect P3.11 acceptance and re-list the two deferred catalog/consumer slices.

The implementation may **not**:

- import the fixture from any existing runtime path (`scripts/module_runner.py`, `scripts/validate_run_manifest.py`, `recon.sh`, any module, any report generator, any policy helper)
- introduce a Python module that *defines* the gap-code vocabulary as a constant other code imports (the vocabulary lives only inside the fixture and the fixture-local test for now)
- promote any field name into `modules/_schema/`, any `*/0.1-trial` schema location, any module manifest, or any run-manifest field
- create a reviewer-prompt JSON file under `templates/` that an existing consumer would load
- write to `loot/`, `scans/`, `runs/`, or `reports/`
- consult any real SIEM, Elasticsearch, Kibana, TryHackMe, or external service

---

## 5. Exact forbidden surfaces

The following surfaces are explicitly out of scope for this slice and any T2 follow-up. Touching any of them requires returning to direction review:

- Live SIEM / Elastic / Kibana / Splunk / any log-aggregation integration.
- Target-touching behavior of any kind: scan, probe, fuzz, brute force, exploit, callback, OAST, proxy, pivot, tunnel, beacon, relay, reverse listener, DNS exfil, webhook to external host.
- Scanner or module execution (nuclei, httpx, subfinder, naabu, katana, ffuf, etc.).
- `recon.sh` runtime, `safe_target`, `--skip-scope-check`, or any scope/policy gate change.
- `config/scope.txt` change.
- Any change under `programs/*/scope.json` or `programs/*/rules*.json` other than `programs/_examples/` synthetic fixtures, and even those are out of scope for this slice.
- Module runner change (`scripts/module_runner.py`).
- Run manifest change (`scripts/validate_run_manifest.py`, `scripts/test_run_manifest_schema.py`).
- Schema promotion or addition under `modules/_schema/` or any trial schema directory.
- Report drafting, report rendering, report submission, HTML/Markdown finding output, platform adapter (<bug-bounty-platform>, Bugcrowd, DefectDojo, etc.).
- Reviewer-prompt JSON wiring into existing consumers, including any change to `templates/report_readiness_reviewer_prompts.json` consumers or its sibling test `scripts/test_report_readiness_reviewer_prompts.py`.
- Credentials, cookies, OAuth, tokens, API keys, private keys, .env, lab secrets, password hashes, or any loot-class data.
- Loot/, logs/, `*.pcap`, `*.cap`, `*.kdbx`, `*.key`, `*.pem`, `creds*` — none may be committed, referenced, or substituted into the fixture.
- Real TryHackMe / TryGovMe screenshots, log exports, simulator hashes, or simulator-specific IOCs that could reveal lab answers.
- Scheduler, CI activation, cron, systemd, deployment, billing, publishing, or any persistent automation.
- Production-side settings, repo permissions, Git ignore weakening, branch protection.
- Subagent or model-route changes.
- Live mode flags or anything that flips dry-run defaults.

---

## 6. Recommended files to create/modify if proceeding

The following is a guide for the *next* implementation task. The next task must independently re-confirm scope before changing anything.

### To create

- `fixtures/soc_evidence_bucket/README.md`
  - Purpose, non-promotional posture, synthetic-only requirement, field vocabulary, gap-code vocabulary, status vocabulary, explicit "this is not a contract" notice, explicit "no real lab data" notice.
- `fixtures/soc_evidence_bucket/sample_timeline_01.json` (synthetic, redacted, multi-stage)
  - Top-level keys: `case_id` (synthetic), `description`, `stages[]`, `notes`.
  - Each stage carries the field set described below.
- `scripts/test_soc_evidence_bucket_fixture.py`
  - Schema-shape assertions (loads as JSON, required fields present per stage).
  - Vocabulary assertions (gap codes ⊂ allowed set; status ⊂ allowed set).
  - Synthetic-value assertions (IPs in 192.0.2.0/24, 198.51.100.0/24, 203.0.113.0/24, 2001:db8::/32; hostnames in `*.example`, `*.invalid`, `*.test`, `*.localhost`; user accounts using `synthetic.*` or `example\\*` style).
  - Negative assertions (no `confirmed_finding`, `submit_ready`, `report_ready`, `live_target`, `production`, `real_target`, `real_credential`, or analogous promotional/live keys anywhere in the document).
  - No filesystem writes outside the test's own tmpdir; no network; no subprocess.

### To modify

- `handoff/accepted_changes.md` — append-only entry for P3.11 with files, validation, and safety boundary.
- `handoff/active_strategy_queue.md` — mark P3.11 accepted; re-record the two deferred lanes (reviewer-gap catalog, trial-consumer design) with their re-trigger conditions; update the "Current Lane" pointer.
- `notes/daily/2026-05-20.md` or the date of acceptance — short note (boundary line preserved).

### Suggested fixture field set (per stage)

Adopt these as the fixture's *internal* names. They are not promoted to any contract by this slice.

- `stage_index` (integer; ordering only, not a final stage number)
- `stage_label` (human description, short)
- `timestamps`: object with `event_observed` and `event_role` (e.g., `download`, `execution`, `persistence`, `lateral_movement`, `impact`)
- `assets`: object with `source_asset`, `execution_asset`, `target_asset`, `affected_asset`, `destination_asset` (each optional; null when not applicable)
- `user_account`
- `process_image`
- `command_line`
- `host_ioc[]` (synthetic only)
- `network_ioc[]` (synthetic only; reserved ranges)
- `file_hashes[]` (synthetic SHA-256 values clearly marked as fixture-only, e.g., leading `0000...` or `dead...` pattern documented in the README)
- `source_uri` (optional; `example.invalid` etc.)
- `destination_path` (optional)
- `attack_tactic` (label, optional)
- `attack_technique` (label, optional)
- `attack_subtechnique` (label, optional)
- `evidence_confidence` ∈ {`low`, `medium`, `high`}
- `description` (finding + implication + follow-on result)
- `gap_codes[]` (subset of the gap-code vocabulary)
- `status` (subset of the non-promotional status vocabulary)
- `next_pivot_query` (optional; a human-readable hunt prompt, not an executable query)

### Allowed gap-code vocabulary (in-fixture only)

`MISSING_HOST_IOC`, `MISSING_NETWORK_IOC`, `MISSING_HASH`, `MISSING_SOURCE_URL`, `MISSING_DESTINATION_PATH`, `MISSING_COMMAND_LINE`, `MISSING_FOLLOW_ON_IMPLICATION`, `PARENT_TECHNIQUE_TOO_BROAD`, `TACTIC_MISMATCH`, `ASSET_ROLE_AMBIGUOUS`, `TIMESTAMP_EVENT_ROLE_MISMATCH`, `NEEDS_SECOND_PASS_HUNT`.

### Allowed non-promotional status vocabulary (in-fixture only)

`needs_more_evidence`, `needs_mapping_review`, `needs_asset_reconciliation`, `needs_second_pass_hunt`, `not_report_ready`.

The README must state that these vocabularies live inside the fixture and its sibling test for now, and are *not* an authoritative contract for any other code.

---

## 7. Tests or validation that must pass

The implementation task must record all of the following as having passed before the slice is accepted:

- `python -m unittest scripts.test_soc_evidence_bucket_fixture` (new test) — green.
- Adjacent suite sanity: `python -m unittest discover scripts` — green (no regression in candidate workflow, runner, bridge, run-manifest, or report-readiness tests).
- `HACKLAB=$(pwd) ./bin/hermes review` — Python compile OK, shell scripts OK, lock clear, scope entries unchanged, no new accepted-changes truncation, no new secrets-style strings introduced.
- `git diff --check` — clean (line-ending warnings tolerated as elsewhere in repo).
- Added-line scan for target-touching or live-mode strings — zero hits for: `http://`, `https://`, real public domain references, `nuclei`, `httpx`, `subprocess`, `requests.`, `urllib`, `socket.`, `loot/`, real credential-like patterns, real SIEM endpoints, real TryHackMe URLs, real Bugcrowd/<bug-bounty-platform> URLs.
- Synthetic-range assertion in the new test must explicitly fail when the fixture is intentionally mutated to contain a non-reserved IP (e.g., `8.8.8.8`); document this in the test docstring or README.
- No new files under `loot/`, `logs/`, `scans/`, `runs/`, `reports/`, `config/`, `programs/<real-slug>/`, `modules/`, `modules/_schema/`, `templates/`, or the runtime path.

---

## 8. Whether P2.24 helper extraction or any existing candidate workflow contract is implicated

**Not implicated.**

- The deferred shared helper `scripts/core/offline_consumer.py` (listed in `handoff/active_strategy_queue.md` under deferred lanes) is *not* touched by this slice. The new test imports nothing from a shared offline-consumer helper; it stands alone.
- The candidate-workflow contracts — candidate review packets, gap reports, verification plans, report-readiness gates, and `templates/report_readiness_reviewer_prompts.json` plus its consumer — are *not* extended, modified, or wired to in this slice. The fixture's gap-code vocabulary is intentionally kept inside the fixture/test only so that a future T3 review can decide deliberately whether and how to harmonize the SOC gap codes with the report-readiness reviewer-prompt vocabulary.
- The current `programs/_examples/sample-lab/scope.json` synthetic fixture pattern is the closest precedent for this kind of offline, synthetic, non-promotional artifact. The fixture in this slice follows the same posture but lives under `fixtures/soc_evidence_bucket/` so it cannot be confused with a program scope file.

A future direction review may decide to:

- promote a subset of the gap-code vocabulary into a `templates/`-style reviewer-prompt catalog (parallel to `templates/report_readiness_reviewer_prompts.json`), and/or
- extract a shared `scripts/core/offline_consumer.py` helper that several stdin-only consumers can reuse.

Both are explicitly out of scope here.

---

## 9. Multi-Party Review Decision final block

```text
Decision: APPROVE_WITH_CHANGES
Tier: T2
Milestone: Post-P3.10 project workflow calibration — P3.11 SOC evidence-bucket synthetic fixture (offline, non-contractual)
Hermes authority: direct
Reviewers consulted:
- Claude / Cowork direction review (this document); visible model/runtime: not exposed by Cowork harness — recorded as limitation
- Implementation review required at slice completion: a fresh-context implementation reviewer (Codex or Claude Code implementation review, route to be chosen by Hermes); visible model/runtime to be recorded at that time
- Safety reviewer: Hermes safety gate (the slice has no target-touching surface, so a separate safety reviewer is not required beyond Hermes synthesis; if implementation drifts toward any runtime wiring, a Cowork safety re-review must be triggered)
- Architecture/roadmap reviewer: this direction review (Cowork)
Validation performed (at direction review):
- Read .hermes.md, review_tiering_policy.md, multi_party_review_decision_policy.md, oss_recon_gate.md
- Read trygovme_soc_sim_lessons_20260520.md, notes/daily/2026-05-20.md, active_strategy_queue.md
- Inspected templates/report_readiness_reviewer_prompts.json and programs/_examples/sample-lab/scope.json as precedent patterns
- Confirmed no current runtime touches the proposed fixture path
Blocking findings:
- None at direction-review stage. The slice is APPROVE_WITH_CHANGES because the narrowed scope (fixture-only, gap-catalog and trial-consumer explicitly deferred) and the non-promotional vocabulary lock are required modifications relative to Option 1 as written.
Non-blocking recommendations:
- After P3.11 acceptance, consider a separate T2 direction review for PROCEED_REVIEWER_GAP_CATALOG_ONLY, calibrated against the now-existing fixture.
- A later T3 direction review may evaluate whether dual-asset / multi-role asset semantics (source/execution/target/affected/destination) should be promoted into any candidate evidence schema. Defer until concrete pressure exists.
- README in the fixture directory should cross-link to templates/report_readiness_reviewer_prompts.json as a *parallel-pattern* reference, not a contract dependency.
- The fixture's synthetic-hash convention (e.g., leading 0000... or dead...) should be documented in the README and asserted in the test so reviewers do not accidentally substitute real lab hashes.
Safety boundary:
- Offline, synthetic, redacted only. No SIEM/Elastic/Kibana, no scanner/module execution, no target-touching, no scope/config changes, no schema promotion, no report drafting/submission, no credentials/loot, no scheduler/CI activation, no proxy/pivot/transport. RFC reserved ranges and example.tld only.
OSS Recon Gate: attached as informational baseline (not formally required at T2); adopt/adapt/ignore notes recorded in §3 so a future T3 contract review does not start from zero.
User approval required: no.
- Reason: the slice is offline fixture/docs/tests only, introduces no contract, no runtime path, no safety-boundary change, no external side effect, and no scope/policy change. Hermes has direct authority at T2.
- Operator approval becomes required if any of the forbidden surfaces in §5 is later in play, if any reviewer disagrees materially on safety, or if drift toward a runtime consumer / schema / report path is observed during implementation.
Accepted changes updated: not applicable at direction-review stage; required at implementation acceptance.
Next action:
- Hermes synthesizes this verdict, prepares a narrow implementation task at handoff/claude_code_task.md (or handoff/codex_task.md depending on routing) restricted to §4 and §6, runs hermes review pre- and post-implementation, requests a fresh-context implementation review at slice completion, then records acceptance in handoff/accepted_changes.md and handoff/active_strategy_queue.md.
```

---

## Reviewer self-disclosure (multi-party policy add-on)

- Reviewer route/tool: Claude / Cowork direction-review session invoked via the Hermes cowork task path.
- Visible model/runtime: not exposed to this reviewer by the harness. Recorded as a limitation in line with the multi-party review decision policy.
- This reviewer did not execute any scan, probe, scanner, module, callback, exploit attempt, brute force, fuzz, OAST, or target-touching action. No edits were made to `config/scope.txt`, program scope files, runtime behavior, schemas, modules, reports, credentials, scheduler, deployment, billing, OAuth, or production settings during this review.
