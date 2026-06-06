> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# P2.18 Direction Review — CTF Verifier Metadata Trial Consumers

Date: 2026-05-18
Reviewer route: Claude Code MAX/OAuth (read-only direction review)
Target output path (for Hermes to persist): `handoff/cowork_p2_18_direction_review.md`

## Decision

**ACCEPT_WITH_CHANGES**

The slice is well-motivated, narrowly scoped, and discharges the P2.17 deferral exactly as recorded (`handoff/cowork_p2_17_direction_review.md` line 15: "Promote to a versioned JSON Schema only after two real verifiers consume it"). Accept the slice with the bounded changes below: tighten the linter contract, expand forbidden fields, lock booleans-as-booleans, and require fixture parity with the P2.17 trigger vocabulary.

Do **NOT** promote `templates/ctf_verifier_metadata.yaml` to a schema, registry entry, or runner consumer in this slice. The whole point of two trial descriptors is to discover gaps before contract lock-in.

## Tier and Boundary Confirmation

- **Tier: T3 (Contract/platform boundary, design-only).** Correct as proposed. Even though the artifacts are fixture-shaped, the linter codifies a vocabulary that is one step from becoming a contract. T3 direction-review-before-implementation is the right gate.
- **Boundary: offline/local only.** Confirmed. The slice must not import from `scripts/module_runner.py`, `scripts/validate_module_io_*`, recon paths, scanner adapters, or program policy. Linter must be standard-library + a minimal YAML loader (or hand-rolled flat parser — see Worker Route below).
- **No schema promotion.** Confirmed. The linter is intentionally weaker than a JSON Schema. Promotion to `modules/_schema/ctf_verifier_metadata.schema.json` is deferred to P2.19+ after this trial reports gaps.
- **No runtime coupling.** Linter must not be invoked by any runner, hook, or CI in this slice. It is an operator-run utility only.

## OSS References Considered (Recon Gate)

Five mature references compared design-only. None copied wholesale.

| Reference | Decision | Why |
|---|---|---|
| **Nuclei template metadata** (`id`, `info.{name,author,severity,tags,classification}`) | **Adapt** | Flat, string-valued, category/tag style is the right shape for trial descriptors. **Explicitly do NOT adopt Nuclei `severity` (info/low/medium/high/critical) or CVSS classification.** P2.17 deliberately keeps severity out of the verifier axis. Borrow the `id` + `category` + flat-tag pattern only. |
| **SARIF result `kind`/`level` separation** | **Adapt** | Already reflected in `ctf_review_decision.py` (status vs confidence as separate axes). The linter must not introduce a `level`-like severity field on the verifier descriptor; verifier metadata describes the verifier, not the finding. Reinforces the no-severity rule. |
| **Semgrep rule metadata + `metadata.confidence`** | **Adapt** | Confidence axis (low/medium/high) is already adopted in `ctf_review_decision.py`. For verifier descriptors, allow a `confidence: candidate` advisory field (per the P2.17 template) but the linter must treat it as advisory only — the runtime decision uses `ctf_review_decision.py`'s axis, not the descriptor's. |
| **DefectDojo finding-state vocabulary** (`active`, `verified`, `false_positive`, `out_of_scope`, `inactive`) | **Ignore for this slice** | Finding-state semantics belong on findings, not on verifier descriptors. Mixing them here would create a parallel finding-state vocabulary and risk silent drift from the future `finding/1.0` contract. The linter must explicitly reject `finding_state`, `verification_state`, or similar fields. |
| **OWASP ZAP add-on manifest / alert metadata** | **Ignore** | ZAP add-on manifests are tightly coupled to ZAP plugin loading and alert ID registries. The trial is the wrong vehicle for that level of platform coupling. |

Optional sixth reference noted but not adopted: **OSCAL component definitions** — too heavyweight for a two-fixture trial. Revisit only if P2.19+ schema promotion needs a control-mapping axis.

## Answers to Required Review Questions

**1. Should P2.18 add a linter now, or only sample descriptors?**
Add the linter. Without it, two descriptors can drift from the template vocabulary and the trial loses its signal value. The linter is the instrument that makes the trial measurable. Keep it intentionally weaker than a schema (no `$schema`, no `$id`, no `additionalProperties` enforcement beyond a flat allowlist).

**2. Should sample descriptors live under `tests/fixtures/` rather than `templates/` or runtime dirs?**
Yes — `tests/fixtures/ctf_verifier_metadata/`. `templates/` connotes authority; placing real descriptors there would suggest the vocabulary is settled. Runtime dirs (`modules/`, `runs/`) would imply registration. `tests/fixtures/` correctly signals "trial input, not a contract."

**3. Should `mode: active-service` be allowed in examples if it is clearly marked as Kali-required and not host-executable?**
Yes, with linter enforcement. The linter must require: if `mode == "active-service"` OR `uses_external_service == true` OR `oracle_required == true`, then `kali_required` field must be present and `true`, AND the descriptor must not include any host-execution affordance (no `command`, `exec`, `cmd`, `callback_url`, `target_url`, etc.). This is consistent with `handoff/ctf_workflow_validation_and_escalation.md` Operating Model: Windows = control plane, Kali = external interaction.

Note that the P2.17 template (`templates/ctf_verifier_metadata.yaml`) currently has no `kali_required` field — it only states the Kali rule in a comment. **Recommend adding `kali_required: <bool>` as an explicit top-level field in the P2.18 fixtures and in the linter's required-when-active-service rule.** Update the template comment to reflect this in the same patch.

**4. Should unknown fields be denied in the linter, or should the template stay open for forward compatibility?**
**Deny unknown top-level fields in this slice.** The trial's purpose is to discover which fields are genuinely needed by real verifiers. If unknown fields are tolerated, drift goes silent. Future-compatibility belongs to the schema promotion step (P2.19+), where versioning provides the proper escape valve. Document this explicitly in the linter help text: "Unknown fields are denied during the trial; promotion to a versioned schema in P2.19+ may revisit."

**5. What are the exact forbidden fields for this slice?**
The linter must deny (return non-zero exit + structured error code per field) ANY of the following at any nesting depth:

- Network/target overrides: `target_url`, `target_host`, `target_ip`, `endpoint`, `base_url`, `host`, `port` (when not part of allowed fields), `scope_override`, `live_target`, `allow_cidr`
- Execution affordances: `command`, `cmd`, `exec`, `args`, `argv`, `shell`, `entrypoint`, `script`, `run`, `binary_path`
- Callback / out-of-band: `callback_url`, `webhook_url`, `oast_domain`, `oast_callback`, `interactsh`, `sink_url`
- Exploit / payload: `exploit_payload`, `payload`, `shellcode`, `rop_chain`, `cve_exploit`
- Promotion / finding-state leaks: `force_verified`, `asserted_status`, `override_status`, `finding_state`, `verification_state`, `evidence_promotion`, `report_promotion`, `severity`, `cvss`, `cvss_vector`, `cwe`
- Credential / loot leaks: `credentials`, `secret`, `token`, `api_key`, `private_key`, `wordlist_path`, `loot_path`
- Scope/config bypasses: `disable_scope`, `bypass_policy`, `skip_authorization`

Mirror the `OVERRIDE_FIELD_NAMES` set from `scripts/ctf_review_decision.py` (lines 90–102) so the two enforcement points share vocabulary. Add a comment in the linter pointing to that constant; the test suite must assert parity (or a documented superset).

**6. What acceptance tests are mandatory before implementation?**
Mandatory minimum set. Each test should pin a deterministic expected linter exit code + structured error code where applicable.

1. **Happy path × 2**: Both `source_transform_inversion.yaml` and `parser_validation_checksum.yaml` lint clean (exit 0, no errors, no warnings).
2. **`destructive: true` denied** → exit non-zero, error code `DESTRUCTIVE_NOT_ALLOWED`.
3. **`mode: "active-service"` with `uses_external_service: true` and `kali_required: true`** → accepted (and recorded as advisory) — this is the legitimate Kali-required descriptor case.
4. **`mode: "active-service"` without `kali_required: true`** → denied, code `ACTIVE_SERVICE_REQUIRES_KALI`.
5. **`mode: "active-service"` with a host-execution field (e.g., `command`)** → denied, code `HOST_EXECUTION_NOT_ALLOWED`.
6. **Unknown `second_review_triggers` value** (e.g., `"never_review"`) → denied, code `UNKNOWN_TRIGGER`. Allowed set must equal `ctf_review_decision.ALLOWED_TRIGGERS` exactly.
7. **Unknown top-level field** (e.g., `severity: high`) → denied, code `UNKNOWN_FIELD`. Test at least three: a benign-looking one (`description`), a severity leak (`severity`), and a network leak (`target_url`).
8. **Boolean fields as strings** (e.g., `destructive: "false"`) → denied, code `BOOL_TYPE_MISMATCH`. Test for each of `destructive`, `requires_scope`, `uses_external_service`, `oracle_required`, `kali_required`.
9. **Invalid `mode`** (e.g., `mode: "live"`) → denied, code `UNKNOWN_MODE`. Allowed: `offline|oracle|active-service|reconstruction`.
10. **Invalid `category`** (e.g., `category: "unknown_class"`) → denied, code `UNKNOWN_CATEGORY`. Allowed set must equal `ctf_prepare_challenge.ALLOWED_CATEGORIES`.
11. **Each forbidden field, individually** → denied. Parameterize this test so adding a new forbidden field requires updating one list. Use the question-5 list verbatim.
12. **Determinism**: running the linter twice on the same file produces byte-identical structured JSON output (no timestamps, no nondeterministic ordering).
13. **Idempotent multi-file run**: linting both fixtures in a single invocation produces the same output as linting them separately, concatenated and sorted.
14. **Empty / missing required keys**: missing `id`, `category`, `mode`, `requires_scope`, `destructive`, `uses_external_service`, `oracle_required`, `second_review_triggers`, `evidence_outputs` each → denied, code `MISSING_REQUIRED_FIELD`.
15. **YAML anchor / merge / `!!python/object` rejection**: if a YAML loader is used, it MUST be a safe loader. Add a test that a YAML file containing `!!python/object/apply:os.system ["echo pwned"]` is rejected at parse time and never executed. Prefer `yaml.safe_load`; if the project avoids `PyYAML`, write a minimal flat-key parser instead.
16. **Schema-promotion negative test**: assert no file under `modules/_schema/` references `ctf_verifier_metadata` and that the linter source contains a `# TRIAL ONLY — do not promote without P2.19+ review` comment near the top.

Tests 3, 4, 5 directly answer Required Question 3 and must not be skipped.

## Recommended Deliverables (Final)

1. `tests/fixtures/ctf_verifier_metadata/source_transform_inversion.yaml`
   - Models the vault-door-8 lesson: source-reverse / inversion verifier, `mode: offline`, no external service, `kali_required: false`.
2. `tests/fixtures/ctf_verifier_metadata/parser_validation_checksum.yaml`
   - Models the Java Script Kiddie lesson: parser/checksum verifier, `mode: offline`, no external service, `kali_required: false`.
3. *(Optional but recommended)* `tests/fixtures/ctf_verifier_metadata/oracle_replay_kali.yaml`
   - Models the Clouds lesson: `mode: active-service`, `uses_external_service: true`, `oracle_required: true`, `kali_required: true`. Including this third fixture proves the linter's Kali-required rule on a realistic example rather than a synthetic test stub. If the operator prefers to keep the trial at exactly two, move this case fully into `scripts/test_ctf_verifier_metadata.py` as inline test data.
4. `scripts/lint_ctf_verifier_metadata.py`
   - Standard-library + safe YAML loading only. `argparse`-driven. Reads one or more `--input` paths (or stdin). Emits one deterministic JSON object per file with `{file, status, errors[], warnings[]}` sorted. Exit 0 only if all inputs pass.
   - Must include header comment: trial-only, non-binding, no runtime consumers, deferred schema promotion.
5. `scripts/test_ctf_verifier_metadata.py` — covers tests 1–16 above.
6. Minor update to `templates/ctf_verifier_metadata.yaml`:
   - Add `kali_required: false` as an explicit field (with comment: required `true` when `mode: active-service` or `uses_external_service: true`).
   - Tighten the existing header comment to point readers at the linter and at `tests/fixtures/ctf_verifier_metadata/` for the trial fixtures.
   - Do **not** version the template, do **not** add a `schema_hint`, do **not** add `$schema` / `$id`.
7. `scripts/README.md` — add an entry for `lint_ctf_verifier_metadata.py` noting trial-only status.
8. `handoff/accepted_changes.md` — record worker route, verification result, and the fact that schema promotion is explicitly deferred to P2.19+.

## Forbidden Changes (Confirmed)

- No live scans, HTTP, sockets, callbacks, exploit attempts, fuzzing, brute force, OAST, or any target-touching behavior.
- No imports from `scripts/module_runner.py`, `scripts/validate_module_io_bundle.py`, `scripts/validate_module_io_contract.py`, `scripts/program_policy_boundary.py`, `recon.sh`, or any scanner/module runtime path. The linter must be standalone.
- No JSON Schema file under `modules/_schema/`. No registry entry, no runner wiring, no recon wiring, no CI/hook/scheduler/pre-commit wiring, no `bin/hermes` integration, no `.github/` workflow changes.
- No promotion of any field to `finding/1.0`, `evidence/1.0`, or `run/1.0` contracts.
- No changes to `config/scope.txt`, `loot/`, `.env`, credentials, tokens, OAuth, scheduler, deployment, billing, or production settings.
- No changes to `setting/local/ctf/` runtime layout (P2.17's prepare path stays untouched).
- No use of `ANTHROPIC_API_KEY`-backed Claude/Cowork; this slice does not justify it. P2.17's successful Claude Code MAX/OAuth route applies.
- No invocation of the new linter by any existing script, runner, or hook in this slice.
- No catch-all `unknown_field: tolerated` escape valve. The trial is meaningful only if drift is denied.

## Suggested Worker Route

**Primary: Claude Code MAX/OAuth implementation + Hermes verification.**

Rationale:
- Identical shape to P2.17, where this route succeeded (`accepted_changes.md` 2026-05-18 entry: focused tests 4 OK + 10 OK, full suite 218 OK / 8 skipped, no Codex fallback needed).
- Pure standard-library work with deterministic fixtures — ideal for Claude Code's plan-backed capacity.
- No `ANTHROPIC_API_KEY` consumption, which respects the active model-routing policy (`handoff/model_usage_routing_policy.md` lines 86–97: prefer Claude Code MAX/OAuth; API-backed Claude only for high-value cases).

**Fallback: Codex/GPT for surgical fixes if Claude Code is blocked on YAML loader choice or fixture content.**

**YAML loader note for the implementer.** If `PyYAML` is not already a dependency, prefer either (a) `yaml.safe_load` only after confirming PyYAML is already a transitive dep, or (b) a minimal hand-rolled flat-key parser limited to the allowed field set. **Do not add a new third-party dependency for this trial.** A flat parser is small (~50 LOC) and removes the YAML-anchor attack surface entirely; this is the recommended choice. Test 15 above must pass either way.

**Hermes verification contract** (per `model_usage_routing_policy.md` lines 56–63):
1. `git status --short` + targeted diff review on `scripts/lint_ctf_verifier_metadata.py`, `scripts/test_ctf_verifier_metadata.py`, the two fixtures, the template tweak, and the README entry.
2. `git diff --check` on all touched files (CRLF-only warnings tolerated per recent history).
3. `python -m py_compile` on the new linter and test files.
4. `python -m unittest scripts.test_ctf_verifier_metadata` — focused tests must pass.
5. `python -m unittest discover -s scripts` — full suite must remain green (current baseline: 218 OK, 8 skipped).
6. AST/grep verification that the new linter does NOT import `socket`, `http`, `urllib`, `requests`, `subprocess`, `asyncio`, `selectors`, or anything from `scripts/module_runner.py` / `scripts/program_policy_boundary.py` / `recon.sh`.
7. Confirm no new file under `modules/_schema/` was added.
8. Update `handoff/accepted_changes.md` with worker route + verification result.

## Promotion Criteria for P2.19+ (Out of Scope for This Slice)

Record but do not act on:
- If both fixtures lint clean AND no field had to be added beyond the current template vocabulary AND no forbidden-field collision arose during authoring, the template is a candidate for schema promotion in P2.19.
- If either fixture required vocabulary not in the template, the gap report (saved to `handoff/`) is the deliverable, and schema promotion is deferred again.
- Schema promotion requires a separate T3+ direction review with its own OSS Recon Gate (re-check SARIF/Nuclei/Semgrep evolution at that time).

---

**End of P2.18 direction review.** Hermes: please persist the above content verbatim to `handoff/cowork_p2_18_direction_review.md`. No file writes were performed by the reviewer; no `ANTHROPIC_API_KEY` was consumed.
