> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Cowork Direction Review Request — P2-15 offline preview ledger / archive index

You are Claude/Cowork performing a design-only direction review for the authorized cybersec lab repository.

Repository context:
- This is an authorized cybersecurity lab / bug bounty automation platform.
- Current phase completed: P2-14 `preview_manifest/1.0` schema + read-only validator for already-persisted dry-run preview bundles.
- The platform goal is extensible, update-friendly, modular, policy-gated, agent-assisted authorized testing.
- Safety boundary is binding: no live scans, no external target interaction, no module execution, no scanner invocation, no subprocess/network/callback behavior, no findings/evidence/report emission, no loot, no credentials, no `config/scope.txt` changes.

Proposed next phase:
- P2-15: an offline preview ledger / archive index for persisted preview bundles.
- Goal: create a small repo-local contract and validator that can index already-existing `runs/<run_id>/preview/preview_manifest.json` records for later agent-assisted triage and archive review.
- This must remain offline/data-only and must not trigger module execution or target-touching.

Candidate scope options to evaluate:
1. Minimal ledger schema only:
   - `modules/_schema/preview_ledger.schema.json`
   - records list run_id, preview_manifest_relative_path, preview_manifest_sha256, created_at_utc, validation status, and optional notes.
2. Validator only:
   - `scripts/validate_preview_ledger.py` reads a ledger JSON and validates path/hash references against committed/local preview manifests.
3. Builder/indexer optional but risky:
   - `scripts/build_preview_ledger.py` scans only repo-local `runs/*/preview/preview_manifest.json` and writes a ledger by explicit opt-in.
   - If you think this is too much for P2-15, recommend deferring builder to P2-16.

Review tier:
- Classify as T3 contract/platform boundary unless you find a higher tier trigger.
- Apply OSS Recon Gate design-only comparison.

OSS Recon Gate references to compare conceptually:
- SARIF `runs[]` and result artifact references.
- DefectDojo import/test metadata.
- CycloneDX/BOM-style component index metadata.
- OSV/vulnerability feed metadata for stable IDs and timestamps.
- Nuclei output/template metadata for scan-result indexing pitfalls.

Required decisions:
- Adopt/adapt/ignore decisions from the OSS comparison.
- Recommended P2-15 boundary: schema only, validator only, or schema+validator, and whether to defer builder/indexer.
- Required fields and default-deny semantics.
- How ledger records bind to `preview_manifest/1.0` without becoming a generic file index.
- Path, hash, timestamp, duplicate-run, unknown-field, and symlink posture.
- Test strategy with focused valid/invalid fixtures.
- Safety risks and blockers.

Please write only this file:
- `handoff/claude_p2_15_direction_review.json`

Required JSON shape:
{
  "phase": "P2-15 offline preview ledger / archive index",
  "verdict": "APPROVE_DIRECTION" | "ROUTE_BACK",
  "review_tier": "T3" | "T4",
  "recommended_boundary": "schema_only" | "schema_plus_validator" | "schema_validator_builder" | "defer",
  "oss_recon_gate": [
    {"reference": "...", "decision": "adopt|adapt|ignore", "reason": "..."}
  ],
  "approved_scope": ["..."],
  "out_of_scope": ["..."],
  "required_contract_fields": ["..."],
  "validator_requirements": ["..."],
  "test_requirements": ["..."],
  "safety_boundary": ["..."],
  "blocking_concerns": [],
  "non_blocking_recommendations": ["..."]
}
