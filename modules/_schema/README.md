> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Module and Finding Schemas

This directory contains the P2 contract layer for future policy-gated modules.

Current files:

- `module_manifest.schema.json` — module/plugin metadata. A module manifest declares module id/version, risk level, target types, approved technique tags, dry-run support, network posture, output contracts, external tools, and safety gates before a runner may execute the module.
- `module_profile.schema.json` — data-driven module selection profile metadata. A profile declares allowed modes, risk levels, target types, technique tags, execution/output constraints, and required safety gates before discovery may select matching manifests.
- `module_input.schema.json` — P2-10 preview-only normalized invocation envelope for future modules. It is built only after manifest/profile/policy checks pass and currently allows only dry-run, no-network, non-target-touching, no-finding/evidence preview data.
- `module_result.schema.json` — P2-10 constrained future output envelope. Current valid results are `not_executed`, `planned`, `skipped`, or `error`; they remain dry-run-only and cannot contain findings, evidence, raw observations, scanner output, reports, callbacks, secrets, or loot paths.
- `run.schema.json` — execution ledger metadata. A run manifest binds `run_id`, program/global scope hashes, target, policy decision artifact/hash, profile id/hash, execution mode, modules, findings, evidence, and review state.
- `finding.schema.json` — candidate finding metadata. Automated tools may emit only conservative statuses such as `candidate`, `needs_verification`, `no_observation`, `not_applicable`, or `error`. They must not emit `confirmed` findings.
- `evidence.schema.json` — local evidence metadata. Evidence references must point to redacted artifacts under `runs/<run_id>/evidence/` and include canonical SHA-256 hashes.
- `preview_ledger.schema.json` - P2-15 offline-only manifest-of-manifests index for already-persisted `preview_manifest/1.0` files. Each ledger entry binds exactly one `runs/<run_id>/preview/preview_manifest.json` by path, SHA-256, byte size, and observed schema version.

Safety boundaries:

- Scanner/module output remains triage only.
- Manual verification is required before anything becomes a reportable finding.
- Raw secrets, credentials, tokens, private client data, and unredacted evidence must not be committed.
- Future modules should depend on policy decisions from the central gate instead of re-reading scope files directly.

Module layout:

- `modules/checks/<level-or-category>/<module_id>/module.json` stores committed module manifests.
- `modules/profiles/<profile_id>.json` stores committed data-driven profile contracts. `modules/profiles/audit-baseline.json` is the first conservative offline dry-run profile.
- `modules/checks/level1/policy_decision_metadata_audit/module.json` is the first Level 1 audit fixture. It is intentionally offline-only, non-target-touching, and emits no findings/evidence; it exists to prove manifest validation and runner planning before real execution exists.

Module discovery/profile selection:

- `scripts/module_runner.py --discover-root <repo>` scans only repository-local `modules/checks/**/module.json` paths; discovery mode is mutually exclusive with explicit `--manifest` paths so selected modules all pass the same repo-local profile gate.
- Discovery loads exactly one repo-local profile from `modules/profiles/<profile_id>.json`, validates it with `scripts/validate_module_profile.py`, and fails closed if the profile is missing, malformed, unsupported, path-escaping, or unsafe.
- Runner/discovery JSON payloads preserve human-readable `errors`/`warnings` and add deterministic `error_codes`, `warning_codes`, `error_details`, and `warning_details` for profile loader/selection failures such as `PROFILE_NOT_FOUND`, `PROFILE_MALFORMED_JSON`, `PROFILE_SCHEMA_INVALID`, `PROFILE_ID_MISMATCH`, `PROFILE_CONSTRAINT_EXECUTION`, and `PROFILE_EMPTY_SELECTION`.
- Discovery validates every discovered manifest with the strict manifest validator and fails closed on malformed manifests or duplicate `module_id` values.
- The only current profile is `audit-baseline`; it is data-driven from `modules/profiles/audit-baseline.json` and selects dry-run-safe manifests whose `execution.default_profile` is `audit-baseline`, whose risk/target/technique values are allowlisted, and whose execution/output/safety gates satisfy the profile contract.
- Planned `run/1.0` previews now bind both policy integrity and profile integrity via `execution.profile_id` and `execution.profile_sha256`.
- Discovery is still offline planning infrastructure only: it reads JSON as data and does not import module code, run subprocesses, open network connections, touch targets, or emit findings/evidence.
- `module_input/1.0` and `module_result/1.0` are P2-10 contract previews, not an execution API. The runner emits them only when `--include-module-io-preview` is requested; generated result previews use `status: not_executed`, `dry_run: true`, `target_touching: false`, and empty `findings`/`evidence` arrays.
- P2-11 adds an offline module I/O bundle consistency layer. `scripts/validate_module_io_bundle.py` validates a planned `run/1.0` document together with matching `module_input/1.0` and `module_result/1.0` previews, fails closed on missing/duplicate/extra preview pairs or cross-document mismatches, and remains in-memory/stdout-only with no module execution or persisted ledger.
- Future live/active support, non-empty findings/evidence, reports, scanner execution, module imports, callbacks, or target-touching behavior require separate explicit phases, scope gates, tests, and independent review.

Validation helpers:

```bash
python scripts/validate_module_manifest.py \
  --manifest modules/checks/level1/policy_decision_metadata_audit/module.json \
  --json

python scripts/validate_module_profile.py \
  modules/profiles/audit-baseline.json \
  --json

python scripts/validate_run_manifest.py \
  --run runs/<run_id>/run.json \
  --finding runs/<run_id>/findings/<finding>.json \
  --evidence runs/<run_id>/evidence/<evidence>.json \
  --json

python scripts/validate_finding_evidence.py \
  --finding runs/<run_id>/findings/<finding>.json \
  --evidence runs/<run_id>/evidence/<evidence>.json \
  --json

python scripts/validate_module_io_contract.py \
  --input runs/<run_id>/modules/<module_id>/module_input.json \
  --json

python scripts/validate_module_io_contract.py \
  --result runs/<run_id>/modules/<module_id>/module_result.json \
  --json

python scripts/validate_module_io_bundle.py \
  --run runs/<run_id>/run.json \
  --input runs/<run_id>/modules/<module_id>/module_input.json \
  --result runs/<run_id>/modules/<module_id>/module_result.json \
  --json

python scripts/module_runner.py \
  --manifest modules/checks/level1/policy_decision_metadata_audit/module.json \
  --policy-artifact runs/<run_id>/policy/decision.json \
  --run-id <run_id> \
  --target-type url \
  --target https://authorized.example/ \
  --json

python scripts/module_runner.py \
  --discover-root . \
  --profile audit-baseline \
  --policy-artifact runs/<run_id>/policy/decision.json \
  --run-id <run_id> \
  --target-type url \
  --target https://authorized.example/ \
  --json
```

The helpers are standard-library only and default-deny on malformed, unsupported, ambiguous, unredacted, over-trusting, or cross-document-inconsistent documents. The P2-7 module runner/discovery path is a dry-run-only skeleton: it validates discovered or explicit manifests, an existing policy allow artifact, and the selected repo-local profile, emits a planned `run/1.0` preview with profile hash binding, and refuses target-touching or network-requiring modules instead of executing checks.

Open-source design notes:

- Nuclei templates influenced the simple `id` + `info/severity/tags` style, but Hacklab keeps a smaller allowlisted `technique_tags` vocabulary and does not accept arbitrary template behavior as executable authority.
- OWASP ZAP add-on manifests influenced explicit dependency and extension metadata, but Hacklab keeps execution safety separate from package/build metadata.
- NIST OSCAL component definitions influenced the idea that security components should declare their control/output contracts, but Hacklab uses a lightweight local contract tied to run/finding/evidence schemas rather than adopting full OSCAL.

P2-14 preview manifest:

- `preview_manifest.schema.json` defines the offline-only `preview_manifest/1.0` contract for already-persisted dry-run preview bundles.
- Compatibility is strict-equal: consumers must accept only `schema_version: "preview_manifest/1.0"`. Additive optional fields, removed fields, or semantic changes require a separately reviewed future schema version rather than silent 1.0 drift.
- The manifest binds exactly `run.json`, `module_inputs.json`, `module_results.json`, and `bundle_consistency.json` by safe relative path, SHA-256, byte size, and `application/json` content type. `preview_manifest.json` is not listed as an artifact.
- `scripts/validate_preview_manifest.py runs/<run_id>/preview --json` is a standalone read-only validator. It rejects malformed or duplicate-key JSON, unknown fields, unsafe run IDs/paths, symlinks, missing/extra artifacts, hash/size drift, and non-allow bundle consistency data. It does not repair files, execute modules, launch tools, open network clients, touch targets, or emit findings/evidence/reports.
- Reusable contract fixtures live under `tests/fixtures/preview_manifest/1.0/`; `valid_minimal/` is the committed golden bundle for future ledger/archive/agent-review consumers.

P2-15 preview ledger:

- `preview_ledger.schema.json` defines the offline-only `preview_ledger/1.0` contract for a curated manifest-of-manifests index.
- Compatibility is strict-equal: consumers must accept only `schema_version: "preview_ledger/1.0"` and per-entry `schema_version_observed: "preview_manifest/1.0"`. Additive optional fields, removed fields, or semantic changes require a separately reviewed future schema version rather than silent 1.0 drift.
- The ledger is not a builder, importer, scanner index, finding format, or report surface. It binds only `runs/<run_id>/preview/preview_manifest.json` records by exact relative path, SHA-256, byte size, and duplicate-free `run_id`.
- `scripts/validate_preview_ledger.py preview_ledger.json --repo-root <repo> --json` is a standalone read-only validator. It rejects malformed or duplicate-key JSON, unknown fields, unsafe IDs/paths, symlinks, duplicate run IDs, hash/size drift, missing manifests, timestamp drift, unsafe notes, and schema-version drift. It hashes only the referenced `preview_manifest.json` file and does not parse or hash the four inner artifacts.
- P2-15 does not add `scripts/build_preview_ledger.py` and does not wire the ledger or validator into `module_runner.py`, recon, CI, hooks, schedulers, or scan/module execution paths.
