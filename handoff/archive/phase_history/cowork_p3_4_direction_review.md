> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# P3.4 Direction Review — Manifest-Only Third Level 1 Module Candidate

Date: 2026-05-19
Reviewer: Claude/Cowork via `hermes claude-impl` (design-only direction review)
Review tier: T3 direction review + OSS Recon Gate, design-only
Milestone: Phase 3, candidate fourth slice after P3.3 two-module runner discovery coverage
Source prompt: `handoff/cowork_p3_4_direction_prompt.md`
Predecessors: `handoff/cowork_p3_3_direction_review.md`, P3.3 entry in `handoff/accepted_changes.md` (2026-05-19), `modules/profiles/audit-baseline.json`, `modules/checks/level1/policy_decision_metadata_audit/module.json`, `modules/checks/level1/security_headers_baseline/module.json`, `scripts/module_runner.py`, `scripts/test_module_runner.py`.

## Verdict

DEFER_P3_4_MANIFEST_ONLY

The proposed slice should not proceed as a third-module addition. The contract claim that motivates it — "the module registry can represent metadata-only audit checks without colocated evaluator code" — is **already physically satisfied** in the committed repo by `modules/checks/level1/policy_decision_metadata_audit/`, whose directory contains exactly one file (`module.json`) and no `check.py`, no README, no fixtures, no evaluator artifact of any kind. The peer module `modules/checks/level1/security_headers_baseline/` contains `module.json` + `check.py` + `README.md`. The repo therefore already exhibits both shapes side by side. Adding a third manifest-only module would not unlock a contract claim that is not already observable; it would only repeat an existing datapoint and force a coordinated update of the exact-two-module assertions landed in P3.3.

If the operator still wants stronger evidence that the manifest-only shape is a *deliberate, runner-observed* contract (not an accident of which evaluator happens to have been authored yet), the correct next slice is a small docs + test-only pass that asserts `module_runner.py` is indifferent to `check.py` presence — i.e., discovery, planning, module I/O preview, and bundle consistency behave identically across the manifest-only and manifest+evaluator shapes, using the two existing modules as the natural A/B case. See "Recommended Redirect (P3.4-alt)" below.

If the operator overrides this verdict and still wants to land a third manifest-only module under P3.4, the strict implementation boundary that would be acceptable is in "Conditional Approved Module Scope (override path)" and "Conditional TDD / Validation Gates (override path)" below. Those sections are gated; they are not approved unless the operator explicitly overrides DEFER.

## Rationale

Five reasons drive DEFER rather than PROCEED.

1. **The contract claim is already observable on disk.** A directory listing of `modules/checks/level1/policy_decision_metadata_audit/` shows `module.json` and nothing else (no `check.py`, no README, no fixtures). The runner discovers this manifest, the profile selects it, the in-process and CLI discovery paths return it, the module I/O preview path emits a `not_executed` row for it, and the bundle consistency layer returns `allow` over it — all without any evaluator file ever being present, and all already asserted by the P3.3 test suite (`scripts/test_module_runner.py` lines 533-630). The repo therefore already proves "the registry holds at least one metadata-only audit check, and every runner pathway treats it as a first-class module". A third manifest would not strengthen that claim; it would restate it.

2. **The actual unobserved property is runner indifference to `check.py`, not module count.** What the repo does *not* currently assert with a test is the stronger and more useful claim: `module_runner.py` does not import, execute, reference, or condition on the presence of a `check.py` file in any module directory. That claim is true today (the runner only imports the sibling script `profile_issues` via `_load_script_module` at lines 28-37 of `scripts/module_runner.py`; no codepath walks module directories for executable artifacts), but it is not pinned by a test. Adding a third manifest-only module would not pin it either. A targeted test that (a) demonstrates discovery succeeds when `check.py` is absent and (b) demonstrates discovery is byte-identical when `check.py` is present but contains code that would crash if imported is the smaller, sharper assertion. It can be added without any new module manifest at all.

3. **Adding a third module forces a coordinated edit of three landed P3.3 assertions and gains nothing in return.** The P3.3 tests `test_p3_3_live_repo_audit_baseline_has_exact_two_level1_modules` (line 619), the CLI plan-length assertion `self.assertEqual(len(payload["plan"]["modules"]), 2)` (line 581), and the `expected_ids = {two ids}` assertions (lines 546, 607, 629) all currently lock the live-repo profile-membership set to exactly two ids. A third profile-selected manifest would deliberately break each of them. That is recoverable — the right answer is to update them in the same slice — but it raises the bar: the slice now has to touch test code, the exact-two-module guarantee that was the *output* of P3.3 is being discarded by P3.4, and the rationale for breaking that guarantee has to be more compelling than "we wanted a third instance of a shape we already have". It is not.

4. **The proposed module id `level1.policy_decision_trace_audit` evokes runtime semantics that the prompt asks the module to disclaim.** "Trace" in security-tooling vocabulary commonly denotes runtime tracing, instrumentation hooks, callgraphs, or replay — exactly the kind of execution-flavored affordance that a manifest-only fixture should not advertise. The P3.3 review's non-blocking recommendation 1 named `policy_decision_trace_audit` as one option *or* a deliberately neutral alternative such as `manifest_contract_audit_b`. Re-reading the two against the project's "no runtime affordance in module identity" posture, `policy_decision_trace_audit` is the weaker choice. If the operator overrides DEFER, the safer name is `manifest_contract_audit_b` or a similarly neutral fixture-flavored id. The conditional scope section below assumes that override choice.

5. **Runtime-creep pressure is the real risk, not authoring cost.** The slice as proposed is small, but its main risk is not the manifest itself — it is the directional signal it sends. "We added a third Level 1 module" is read by future slices as license to add more, and the next slice may not be manifest-only. The P3.3 review's non-blocking recommendation 3 already flagged that `security_headers_baseline/check.py` is a real evaluator some future slice might be tempted to wire into the runner for "consistency". Adding a third Level 1 module under P3.4 is structurally compatible with that creep; closing the runner-indifference assertion instead makes that creep *harder*, because any future slice that adds `check.py` import paths to the runner would have to break a green test that explicitly says "the runner does not import or condition on check.py".

The recommendation is therefore not "never add a third manifest-only module"; it is "do the runner-indifference assertion first, then re-evaluate whether a third manifest still has any signal value". After that assertion lands, the answer may well be no.

## Recommended Redirect (P3.4-alt)

If the operator agrees with DEFER, the suggested replacement slice (label it P3.4-alt or P3.4-runner-indifference; Hermes can choose) is:

- **No new module manifest.** The two existing Level 1 modules remain the entire module surface.
- **No edits to any existing manifest, profile, schema, or runner runtime.**
- **Test-only changes to `scripts/test_module_runner.py`** that assert:
  1. Discovery on the live repo succeeds and selects `level1.policy_decision_metadata_audit` (which has no `check.py`) and `level1.security_headers_baseline` (which has a `check.py`) under `audit-baseline` — already asserted by P3.3, retained as a regression baseline.
  2. In a fresh fixture root containing both committed manifests, *placing* a deliberately-broken `check.py` (e.g., `raise RuntimeError("module check should never be imported by the runner")`) into `policy_decision_metadata_audit/` does **not** change any runner output: discovery still returns the same two ids, CLI plan still has length 2, module I/O preview still returns two `not_executed` rows, bundle consistency still returns `allow`, no error/warning code is emitted that references the broken file. The test proves by construction that the runner did not import the file.
  3. The symmetric case: *removing* `check.py` from a fixture copy of `security_headers_baseline/` does not change any runner output either. (`check.py` is only consumed by `scripts/test_security_headers_baseline.py`, never by the runner.)
- **Docs**: one short note in `scripts/README.md` extending the existing P3.3 paragraph to state that the runner-indifference property is now pinned by tests, and one optional one-liner in `modules/_schema/README.md` clarifying that "module manifest" is the runner's only contract surface for a Level 1 module.
- **`handoff/accepted_changes.md`**: one append-only entry summarizing the verdict and test additions.

This alternative is strictly smaller than the prompt's P3.4, requires no new module authoring decision, breaks no existing assertion, and pins the property that actually matters. It would inherit the OSS Recon Gate decision below unchanged (no new field, vocabulary, or contract surface is introduced) and would not require a fresh direction review beyond this one if the operator accepts the redirect inline.

## Conditional Approved Module Scope (override path)

This section is **gated**: it is the implementation boundary only if the operator overrides DEFER and explicitly authorizes a manifest-only third module. Otherwise it does not apply.

- Module id: `level1.manifest_contract_audit_b`
  - Not `policy_decision_trace_audit` (see rationale 4 above). Not `scope_match_audit` (rejected by P3.3 review). The chosen id must not contain `trace`, `scope`, `eval`, `exec`, `run`, `probe`, or `scan`.
- Path: `modules/checks/level1/manifest_contract_audit_b/module.json` (one file, exactly)
- Required manifest fields and values (literal):
  - `schema_version`: `module_manifest/1.0`
  - `module_id`: `level1.manifest_contract_audit_b`
  - `version`: `0.1.0`
  - `name`: a neutral phrase such as `Level 1 Manifest Contract Audit Fixture B`
  - `description`: must say it is a manifest-only fixture, performs no execution, has no colocated evaluator code, opens no network connections, does not touch targets, and emits no findings/evidence
  - `risk_level`: `info`
  - `target_types`: one of `["url", "domain"]` or `["url", "domain", "ip", "cidr"]`; do not introduce a new target type
  - `technique_tags`: a single tag drawn from the existing allowlist in `audit-baseline.json` (`passive.http_headers`, `passive.tls_metadata`, `passive.dns_metadata`, `passive.content_metadata`); do not introduce a new tag
  - `execution.supports_dry_run`: `true`
  - `execution.requires_network`: `false`
  - `execution.network_access`: `"none"`
  - `execution.target_touching`: `false`
  - `execution.destructive`: `false`
  - `execution.intrusive`: `false`
  - `execution.default_profile`: `"audit-baseline"`
  - `external_tools`: identical shape to the existing two manifests (`python-stdlib`, `required: true`, `>=3.11`)
  - `output_contracts.run_schema`: `run/1.0`
  - `output_contracts.finding_schema`: `finding/1.0`
  - `output_contracts.evidence_schema`: `evidence/1.0`
  - `output_contracts.emits_findings`: `false`
  - `output_contracts.emits_evidence`: `false`
  - `safety_gates`: byte-identical to the existing two manifests' `safety_gates` block (all five `true` gates true, all four `false` gates false)
  - `references`: 1-3 publicly accessible documentation URLs only, no scanner-engine references and no URLs that imply active scanning, exploitation, or import-database lifecycles; prefer OWASP ASVS / NIST SP 800-115 style references that describe audit methodology
- Profile membership: the new manifest's `execution.default_profile: audit-baseline` makes it automatically selectable by the profile; no edit to `modules/profiles/audit-baseline.json` is approved.
- Test posture: assertions on `selected_manifests` must move from `==` against a two-id set to `==` against a three-id set. **Partial-match / `assertIn`-only assertions are not acceptable** — that would silently allow any future module to slip into the profile undetected. The exact-set guarantee P3.3 landed must be preserved at the new cardinality.
- Documentation must explicitly state that "manifest-only" in this slice means no `check.py`, no evaluator, no fixtures, and no README in the new module directory. The directory must contain exactly one file: `module.json`.

If any of these constraints cannot be satisfied, the override path is itself off the table and the slice must route back to Hermes for a re-issue.

## OSS Recon Gate Notes

Review tier: T3 (proposed change is a third manifest under the existing `module_manifest/1.0` contract — no new schema, no new field, no new vocabulary, no new execution surface). Milestone: Phase 3, candidate slice 4.

The five references named in the prompt were compared at the design level only. No third-party code was imported, no live target was touched, no scanner shape was adopted. The decision below holds for *both* the deferred path (no module added) and the override path (one manifest-only module added under the constraints above).

### 1. Nuclei templates / ProjectDiscovery metadata + matcher separation

- Useful pattern: Nuclei templates separate `id` / `info` / `severity` / `tags` / `classification` metadata from `requests` / `network` / `headless` / `code` runtime sections. A template can in principle ship metadata that names a class of check while declaring no matcher block — though in practice this is rare in upstream templates. Templates are loaded as data; the engine interprets them. The discovery layer never imports template Python.
- Adopt / adapt / ignore: **affirm current shape; adopt nothing new under P3.4 or P3.4-alt.** Our `module.json` already mirrors the metadata-side cleanly. The manifest-only configuration our `policy_decision_metadata_audit` already exhibits is structurally identical to a Nuclei template that ships `id`/`info`/`tags` only.
- Safety concerns to reject: Nuclei's `tags: dos`, `intrusive`, `fuzz`, `oast`, `network`, `default-login`, and `cve` flagging carry execution semantics (e.g., `network`, `oast`) or import-database lifecycle (`cve`). Our `technique_tags` allowlist must not absorb any of these. The new manifest (override path) must reuse an already-approved tag from `audit-baseline.json`.
- Contract impact: none. No new field is required. The override-path manifest must not introduce a Nuclei-style `matcher` or `extractor` field — those would imply runtime evaluation.

### 2. OWASP ZAP passive scanner add-ons / alert metadata separation

- Useful pattern: ZAP add-ons register alert templates (`alertId`, `risk`, `confidence`, `description`, `solution`, `reference`, `cweId`, `wascId`) declaratively; the alert metadata is data, the passive scanner code is engine-side. Add-on registration is separate from rule execution.
- Adopt / adapt / ignore: **affirm current shape; adopt nothing new.** Our `references`, `safety_gates`, and `output_contracts` fields cover the equivalent surface for a fixture-only manifest. ZAP's `risk`/`confidence`/`cwe` fields are findings-shaped; copying them into a Level 1 manifest would conflate "this is an audit check definition" with "this is an alert template", which the contract intentionally keeps apart.
- Safety concerns to reject: ZAP add-ons can declare active-scan behavior; the framing "passive scanner add-on" must not leak into P3.4 documentation as implying that future Level 1 modules can be active. Override-path docs must explicitly say that Level 1 stays dry-run-only and that `audit-baseline.json`'s `network_access: none` is non-negotiable.
- Contract impact: none.

### 3. Semgrep rule metadata / fixture separation

- Useful pattern: Semgrep rules live in YAML/JSON with `id`/`severity`/`languages`/`message`/`metadata`; rule *fixtures* (input/expected output pairs) sit alongside but are loaded only by tests, not the engine. Crucially, a Semgrep rule directory may contain a rule file with no test fixtures and still be loaded as a valid rule definition — the "manifest-only" shape is normalized in Semgrep's ecosystem.
- Adopt / adapt / ignore: **closest structural match; affirm and adopt nothing new.** The shape `policy_decision_metadata_audit/` already exhibits (one `module.json`, no peer files) is directly analogous to a Semgrep rule with no fixtures. Adding `manifest_contract_audit_b/` in the override path would be a second instance of the same Semgrep-analogous shape; it would not unlock a new Semgrep-side property.
- Safety concerns to reject: do not promote Semgrep's notion of a confirmed rule match into our `finding/1.0`. Semgrep's `match` is a positive signal from a static analyzer; our `finding/1.0` `status` must remain `candidate` for triage-only emission and never appear in any P3.4 docs or test strings.
- Contract impact: none.

### 4. SARIF run / result / toolComponent separation

- Useful pattern: SARIF separates `runs[]` (one per tool invocation), `results[]` (one per finding), and `runs[].tool.driver` + `runs[].tool.extensions[]` (`toolComponent` objects) describing the tool and its rule set. A `toolComponent` may declare rules without any corresponding `result` ever having been emitted by it — the metadata-only shape is first-class.
- Adopt / adapt / ignore: **affirm current `run/1.0` vs `finding/1.0` split; adopt nothing new under P3.4 or P3.4-alt.** The SARIF `toolComponent`-without-results pattern is precisely what our manifest-only modules represent, and the existing `policy_decision_metadata_audit` already demonstrates it.
- Safety concerns to reject: SARIF's `kind: fail` / `pass` / `notApplicable` is promotion-flavored and must not appear in P3.4 manifest field values, test assertion strings, payload keys, or log strings. Use `verdict: allow` / `deny` (already used by the runner) instead. SARIF's `level: error` / `warning` / `note` should not be conflated with our `risk_level: info` / `low` — the override-path manifest must keep `risk_level: info` and must not introduce a SARIF-flavored `level` field.
- Contract impact: none.

### 5. DefectDojo importer / engagement / test / product lifecycle

- Useful pattern: DefectDojo's import pipeline lands findings into a `product -> engagement -> test` hierarchy and applies lifecycle states (`active`, `verified`, `false_p`, `risk_accepted`, `out_of_scope`, `mitigated`). The model formalizes how third-party scanner output gets reviewed.
- Adopt / adapt / ignore: **ignore for P3.4 and P3.4-alt.** DefectDojo's separation is import-database shaped; our manifest-only module slice does not need it. The lifecycle vocabulary remains explicitly **rejected** in fixtures, tests, and docs; `finding/1.0` chain stays at `candidate`-only.
- Safety concerns to reject: introducing DefectDojo's lifecycle vocabulary (`verified`, `risk_accepted`, `mitigated`) into the new manifest, into test assertion strings, or into the P3.4 docs would invite a path toward "automated verification" semantics that the safety model explicitly bans. Hard reject. Likewise, no `severity` field shaped after CVSS should appear in the new manifest — `risk_level` is the only severity surface and must remain `info`.
- Contract impact: none.

### Net OSS Recon Gate decision

**APPROVE the design boundary; no new field, vocabulary, contract, behavior, or runtime is adopted from any reference.** The decision is consistent with the OSS Recon Gates already applied in `handoff/cowork_p3_1_direction_review.md` and `handoff/cowork_p3_3_direction_review.md`. Nothing has shifted that would warrant fresh adoption.

Tier / milestone impact:

- Escalation required: **no.** Stays at T3.
- Can this gate cover later slices: **no.** A fresh OSS Recon Gate must run for any subsequent slice that (a) adds a *fourth* Level 1 module manifest, (b) introduces any evaluator-import path into the runner, (c) proposes promoting `module_input/1.0` / `module_result/1.0` / `module_manifest/1.0` / `module_profile/1.0` / `preview_manifest/1.0` / `preview_ledger/1.0` toward a 1.1 or later version, or (d) introduces any importer/exporter/platform adapter.
- Re-review triggers if assumptions change: any proposal to load `check.py` from `module_runner.py`; any proposal to relax `audit-baseline.json` constraints (risk allowlist, technique tags, execution flags); any proposal to add a new technique tag or target type; any proposal to add an `enabled` / `feature_flag` field to manifests; any proposal to add finding/evidence emission to a Level 1 module.

## Conditional TDD / Validation Gates (override path)

This section applies only if the operator overrides DEFER. Under the redirect (P3.4-alt), the TDD shape is the runner-indifference test described in "Recommended Redirect" above, and the file-allowed/file-forbidden lists are even tighter (no `modules/**` writes at all).

If the override is exercised, the implementer should follow this sequence:

1. **RED first.** Add the three-module discovery assertion against the live repo before adding the new manifest. The assertion `set(...) == {policy_decision_metadata_audit, security_headers_baseline, manifest_contract_audit_b}` should fail with `manifest_contract_audit_b` absent. This RED step proves the test is actually pinned to the new cardinality and not silently passing.
2. **GREEN by manifest creation only.** Add `modules/checks/level1/manifest_contract_audit_b/module.json` with exactly the fields and values in "Conditional Approved Module Scope" above. Do not add `check.py`, README, fixtures, or any other file in the new directory. Do not edit any other manifest, profile, schema, runner, or validator.
3. **Update P3.3 exact-two-module assertions to exact-three.** Specifically: `test_p3_3_live_repo_audit_baseline_has_exact_two_level1_modules` (line 619) becomes `..._exact_three_..._modules` with the expanded `expected_ids`; the CLI plan-length assertion `self.assertEqual(len(payload["plan"]["modules"]), 2)` (line 581) becomes `... 3)`; the `expected_ids = {two ids}` assertions at lines 546 and 607 become `{three ids}`. Each updated assertion must remain an exact-set assertion (`==`), not a containment assertion (`assertIn`).
4. **Two-module fixture tests stay two-module.** The P3.3 fixture-based tests in `TwoModuleDiscoveryTests` (and equivalents) intentionally exercise the two-module discovery contract by *copying only two manifests into a fresh fixture root*. They must remain two-module — do not retrofit them to three-module by also copying the new manifest. The new live-repo assertion is the only assertion that pins the new cardinality. This preserves the two-module discovery regression separately from the three-module live-repo regression.
5. **Manifest schema validation.** Run `python scripts/validate_module_manifest.py modules/checks/level1/manifest_contract_audit_b/module.json` (or the test that covers it) and confirm it passes against `modules/_schema/module_manifest.schema.json` without warnings. Run the equivalent profile-membership validation against `audit-baseline.json` and confirm the new manifest is selected.
6. **Module I/O preview / bundle consistency over three modules.** Run the CLI with `--include-module-io-preview` against the live repo and confirm `module_input_previews` and `module_result_previews` each have length 3, with `status: not_executed`, `dry_run: true`, `target_touching: false`, empty `findings`, and empty `evidence` for the new module. Confirm `bundle_consistency` (or the equivalent payload signal) is `allow`.
7. **Determinism gate.** Call `runner.discover_profile_manifests` twice against the live repo and assert the `selected_manifests` lists are element-by-element equal. The deterministic-ordering claim must hold at the new cardinality.
8. **Negative-path coverage at the new cardinality.** Extend (do not replace) the existing P3.3 malformed-second-manifest fail-closed test so that malforming the *third* manifest also produces `verdict: deny` with no partial selection. Add this as a new test method; do not edit the existing one.
9. **Full-suite gate.** Run `python -m unittest discover -s scripts -p 'test_*.py'`. The suite must remain green and the test count must increase (or at minimum stay equal if the P3.3 two-module fail-closed test was generalized). Any newly-skipped test must be justified in the worker summary.
10. **Hermes review gate.** Run `hermes review`. Resolve any JSON or `bash -n` failures by fixing the offending file, not by skipping the check.
11. **Independent implementation review.** Per `handoff/review_tiering_policy.md` T3 row, request a separate Claude/Cowork or third-party implementation review against this direction boundary before final acceptance.

### Focused test commands (override path)

```bash
python -m unittest scripts.test_module_runner.TwoModuleDiscoveryTests -v
python -m unittest scripts.test_module_runner -v
```

### Full suite command

```bash
python -m unittest discover -s scripts -p 'test_*.py'
```

### Hermes review command

```bash
bin/hermes review
```

### Independent review requirement

T3 per `handoff/review_tiering_policy.md`: independent Claude/Cowork or third-party implementation review required before the slice is closed in `handoff/accepted_changes.md`.

## Forbidden Changes (binding for both the deferred and override paths)

The implementer must not touch any of the following:

- `config/scope.txt`
- `recon.sh`
- `config/recon.conf`
- `scripts/module_runner.py` runtime behavior (no new import path, no new discovery branch, no new field handling, no new error code, no new warning code; this slice does not adjust the runner)
- `scripts/validate_module_manifest.py`, `scripts/validate_module_profile.py`, `scripts/validate_module_io_contract.py`, `scripts/validate_module_io_bundle.py`, `scripts/validate_preview_manifest.py`, `scripts/validate_preview_ledger.py`, `scripts/validate_finding_evidence.py`, `scripts/validate_run_manifest.py`
- `scripts/program_policy_boundary.py`, `scripts/profile_issues.py`, `scripts/build_candidate_review_packet.py`, `scripts/review_candidate_packet_gaps.py`, `scripts/build_candidate_verification_plan.py`, `scripts/build_report_readiness_gate.py`, `scripts/build_candidate_workflow_fixture.py`
- `modules/profiles/audit-baseline.json` (no profile edit is approved; the new manifest's `execution.default_profile: audit-baseline` is the only profile-membership mechanism allowed under the override path)
- `modules/profiles/*.json` other than membership-by-manifest (no profile authoring or constraint change)
- `modules/_schema/**` (no schema bump, no field add, no constraint relaxation, no version promotion; trial schemas at `*/0.1-trial` remain locked)
- Any candidate workflow `*/0.1-trial` schema or script
- `modules/checks/level1/policy_decision_metadata_audit/module.json` (existing manifest must remain byte-identical)
- `modules/checks/level1/security_headers_baseline/module.json` (existing manifest must remain byte-identical)
- `modules/checks/level1/security_headers_baseline/check.py` (existing evaluator must remain byte-identical; no parallel evaluator may be added to the new module)
- `modules/checks/level1/security_headers_baseline/README.md` (no parallel README; the new module must contain *only* `module.json`)
- `tests/fixtures/**`
- `loot/**`, `scans/**`, `reports/**`, `runs/**`
- `.env`, credentials, OAuth, scheduler, deployment, billing, production settings, persistent automation, external services
- Any addition of network access, subprocess spawning, scanner integration, importer/exporter, platform adapter, OAST/callback infrastructure, proxy/pivot/transport, or live-target affordance, at any layer

Any deviation from these constraints is a scope escalation and must route back through Hermes for a direction-review re-issue. The implementer must not "fix" a manifest field, "tighten" a profile constraint, "harden" a validator, or "extract" a runner helper inside this slice.

## Safety Boundary Confirmation

This review is design-only. The reviewer did not:

- run live scans, probes, scanners, fuzzers, exploit tooling, callbacks, OAST / relay infrastructure, proxy / pivot tooling, or any target-touching automation
- import, vendor, or invoke any third-party scanning code
- execute any module `check.py` file
- modify `config/scope.txt`, `config/recon.conf`, `recon.sh`, anything under `modules/**`, `scripts/*.py`, `tests/**`, `loot/**`, `scans/**`, `reports/**`, `runs/**`, `.env`, credentials, OAuth, scheduler, billing, deployment, or production-side settings
- promote any `*/0.1-trial` schema, draft any report, add any platform adapter, change any candidate-chain status to `confirmed` / `verified`, or add any runner runtime / recon wiring / module execution surface
- authorize any active scan, target interaction, module execution, scanner import, report drafting/submission, schema promotion, or platform adapter under this review

Files this review reads (read-only):
`handoff/cowork_p3_4_direction_prompt.md` (delivered inline),
`handoff/cowork_p3_3_direction_review.md`,
`handoff/oss_recon_gate.md` (excerpt),
`handoff/review_tiering_policy.md` (excerpt),
`handoff/accepted_changes.md` (P3.3 entry),
`modules/profiles/audit-baseline.json`,
`modules/checks/level1/policy_decision_metadata_audit/module.json`,
`modules/checks/level1/security_headers_baseline/module.json`,
directory listings of `modules/checks/level1/policy_decision_metadata_audit/` and `modules/checks/level1/security_headers_baseline/`,
`modules/_schema/` listing,
`scripts/module_runner.py` (selected ranges),
`scripts/test_module_runner.py` (selected ranges).

Files this review writes:
`handoff/cowork_p3_4_direction_review.md` (this file, only).

Binding rules from `.hermes.md` preserved: authorization-first, no exfiltration, no destructive defaults, no silent overwrites, lock discipline, secrets out of git, report integrity (`accepted_changes.md` treated as append-only), no production-side changes. None of these were touched.

The implementation slice that follows this review — whether the deferred P3.4-alt redirect or, on operator override, the manifest-only P3.4 — must preserve the same posture and is bound by the explicit "Forbidden Changes" list above. No live-target affordance is added, no scope semantics are changed, no schema is promoted, no runner runtime is wired, no scanner importer is created, no evaluator is imported from the runner, no existing manifest is edited, and no status above `needs_manual_review` is emitted by any stage (this slice does not emit any candidate-chain status at all; it only asserts manifest registration shape).

## Blocking Issues

None for the deferred path (P3.4-alt redirect).

One conditional concern on the override path: the proposed module id `level1.policy_decision_trace_audit` should be rejected in favor of a neutral fixture-flavored id such as `level1.manifest_contract_audit_b` (see rationale 4 and "Conditional Approved Module Scope"). Proceeding with the `trace`-flavored name would be a low but avoidable runtime-creep signal in the module identity surface.

## Non-Blocking Recommendations

1. **Treat the redirect as the default and the override as the exception.** If the operator accepts DEFER, run the P3.4-alt runner-indifference slice next. It is strictly smaller than the prompt's P3.4, breaks no existing assertions, and pins the property that actually distinguishes manifest-only modules from manifest+evaluator modules at the runner contract level.

2. **If the override is taken, land the test updates (exact-three assertions) in the same commit as the manifest addition.** Splitting them would leave the suite red on the manifest commit; bundling them keeps `accepted_changes.md` honest about what the slice did.

3. **Do not chain a fourth Level 1 module proposal off the back of P3.4.** Whether the deferred or override path is taken, the next slice that proposes a *fourth* Level 1 module must trigger a fresh direction review and OSS Recon Gate. Cardinality drift is the kind of change that looks small in any single slice and large only across a few of them.

4. **Reaffirm the `0.1-trial` lock at implementation review.** Per `handoff/cowork_p2_25_closeout_review.md`, nothing in P3.4 (either path) may promote any `*/0.1-trial` schema. Implementation review should spot-check this by grepping the diff for any `0.1-trial` or `1.0` string appearing in a non-test, non-manifest path.

5. **Do not extract `module_runner.py` discovery helpers under P3.4 (either path).** The P2.24 deferral remains correct. If the runner-indifference test reveals the discovery path is hard to test without a shared helper, that is a separate slice with its own direction review; do not absorb it into P3.4 as "while we're here".

6. **Hermes should record the redirect explicitly when scheduling the next slice.** If the operator accepts DEFER and Hermes proceeds with the P3.4-alt redirect, the converted `handoff/claude_code_task.md` (or codex task) should explicitly restate the redirect ("do not add a third module; pin runner-indifference to `check.py` presence using the two existing modules") so the implementer cannot read the original P3.4 prompt and infer a different scope.

7. **If the override is taken, the worker summary in `handoff/claude_code_result.md` must list the four updated P3.3 assertions by line number and confirm each remains an exact-set assertion.** This is the smallest tripwire for the failure mode "exact-two-module guarantee silently relaxed to containment".
