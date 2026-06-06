> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# tools/

Reserved for safe helper wrappers and local developer utilities.

This directory is not a dumping ground for arbitrary offensive tooling. Any helper placed here should be documented, testable, and should not bypass Hermes policy/scope gates.

Preferred structure for future reusable execution code is `scripts/core/`; preferred structure for vulnerability/check content is `modules/`.

Current metadata-only vulnerability-to-proof helpers:

- `vuln_intel_refresh.py` — fetches public advisory metadata and writes `handoff/vuln_intel/vuln_intel_candidates_<stamp>.*`; no target touch.
- `bundle_index.py` — indexes local `modules/bundles/*.md` proof-pattern coverage; no target touch.
- `vuln_intel_to_bundle_index.py` — compares newest vuln-intel candidates to proof bundles and emits bundle freshness delta JSON/Markdown; rejects target-like CLI flags.
- `vuln_to_proof_loop.py` — turns a freshness delta into non-executing local-lab run-card, proof-pattern draft, and live-target prerequisite map artifacts; rejects target/execution-like CLI flags.
