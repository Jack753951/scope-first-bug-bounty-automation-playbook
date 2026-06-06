> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Cowork Direction Review Request — P2-14 preview_manifest/1.0 schema + validator

You are Claude/Cowork performing a design-only direction review for the authorized cybersec lab repository.

Repository context:
- Project: cybersec lab / hacking workspace.
- Long-term goal: extensible, update-friendly, systematized authorized bug bounty platform with modular vulnerability scripts/plugins, scope/rule gates, triage, verification, and reporting workflows.
- Security boundary: DO NOT run scans, touch external targets, execute modules, invoke scanners, perform exploit/fuzz/brute-force/callback behavior, change config/scope.txt, access loot/secrets, or publish/deploy anything.
- This review is offline architecture/design only.

Recent completed phase:
- P2-13 added opt-in dry-run preview bundle persistence to scripts/module_runner.py.
- It writes already-validated dry-run preview artifacts under repo-local runs/<run_id>/preview/:
  - run.json
  - module_inputs.json
  - module_results.json
  - bundle_consistency.json
  - preview_manifest.json
- Persistence requires --persist-preview-bundle + --include-module-io-preview + explicit repo root.
- It rejects unsafe run IDs, symlinked roots/parents, path escapes, existing preview dirs, bundle non-allow, and filesystem failures.
- No module execution, subprocess, network, target touching, findings/evidence, callbacks, scanners, or reports were added.

Proposed next phase:
- P2-14: add a versioned preview_manifest/1.0 schema and standard-library semantic validator for persisted preview_manifest.json.
- Purpose: make preview_manifest.json a stable contract before later preview ledger/archive/agent-review consumers rely on it.
- Must remain offline-only and data-only.

Required review tier:
- Classify this phase under handoff/review_tiering_policy.md.
- Expected default: T3 contract/platform boundary, unless you justify lower/higher.

OSS Recon Gate requirement:
Compare 2-5 relevant open-source formats/projects and decide adopt/adapt/ignore. Good candidates include:
- SARIF run/result metadata
- DefectDojo importer/test metadata concepts
- CycloneDX metadata/provenance ideas
- OSV advisory/versioned schema style
- Nuclei result/template metadata conventions
Use only design ideas. Do not inherit unsafe live-scanning or target-touching defaults.

Please write the result to:
- handoff/claude_p2_14_direction_review.json

Required JSON shape:
{
  "phase": "P2-14 preview_manifest schema and validator",
  "verdict": "ACCEPT_FOR_IMPLEMENTATION" | "ROUTE_BACK_FOR_DESIGN_FIXES",
  "review_tier": "T0" | "T1" | "T2" | "T3" | "T4" | "T5",
  "milestone_boundary": "...",
  "oss_recon_gate": {
    "applied": true,
    "references": [
      {"name": "...", "decision": "adopt" | "adapt" | "ignore", "reason": "...", "safety_notes": "..."}
    ]
  },
  "recommended_contract": {
    "schema_path": "...",
    "validator_path": "...",
    "required_fields": ["..."],
    "semantic_checks": ["..."],
    "failure_mode": "..."
  },
  "implementation_constraints": ["..."],
  "tests_required": ["..."],
  "blocking_issues": ["..."],
  "non_blocking_recommendations": ["..."],
  "safety_boundary": ["..."]
}

Focus questions:
1. What fields must preview_manifest/1.0 contain to safely bind the persisted artifacts to the validated run/bundle?
2. Which checks belong in JSON Schema vs stricter Python semantic validator?
3. How should artifact path/hash/size consistency be represented without becoming a generic file-write/output mechanism?
4. What tests should Codex implement before any future ledger or executor work?
5. What should explicitly remain out of scope for P2-14?
