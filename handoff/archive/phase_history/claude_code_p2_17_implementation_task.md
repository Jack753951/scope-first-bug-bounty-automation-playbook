> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Claude Code Implementation Task — P2.17 CTF Artifact + Review Decision Skeleton

Date: 2026-05-18
Worker route: Claude Code MAX/OAuth implementation
Verifier: Hermes
Fallback: Codex/GPT surgical fixes only if needed
Tier: T3 offline/local

## Source review

Read and follow:

- `handoff/cowork_p2_17_direction_review.md`
- `handoff/model_usage_routing_policy.md`
- `handoff/ctf_tooling_backlog.md`
- `handoff/ctf_workflow_validation_and_escalation.md`

## Goal

Implement the P2.17 offline/local CTF artifact and review-decision skeleton.

## Required deliverables

1. `scripts/ctf_prepare_challenge.py`
   - standalone stdlib-only Python script with `argparse`
   - creates `setting/local/ctf/<slug>/`
   - writes `challenge.json`
   - writes `solve_notes.md` with output-side review checklist
   - idempotent: refuse overwrite by default if files/dir already exist; support explicit `--force`
   - slug must be operator-supplied; do not derive slug from URL/host
   - no network, no sockets, no external target interaction

2. `scripts/ctf_review_decision.py`
   - standalone stdlib-only Python script with `argparse`
   - pure review decision over JSON input file or stdin
   - emits deterministic JSON with stable sorted keys and sorted triggers
   - status enum: `hint`, `candidate`, `verified`, `needs_second_review`
   - confidence enum: `low`, `medium`, `high`
   - output fields should include at least: `status`, `confidence`, `triggers`, `reasons`, `input_hash`
   - default to conservative status when ambiguity exists
   - do not infer high confidence unless input explicitly provides it

3. `templates/ctf_verifier_metadata.yaml`
   - non-binding, unversioned template
   - clear header comment says this is not a schema/contract yet

4. Test fixtures and tests
   - use repo style: `scripts/test_*.py` if no central test dir exists
   - include fixtures under `tests/fixtures/ctf_review_decision/` or another clearly local fixture path if repo convention requires
   - required fixture scenarios:
     - verified normal flag
     - no-wrapper flag triggers abnormal_format / second review
     - UI/checker-only candidate triggers second review
     - multiple candidates triggers second review
     - solver timeout triggers second review
     - external writeup only triggers second review
   - add idempotency test for prepare script
   - add determinism test for decision output
   - add boundary test showing target/scope override fields do not trigger network action and do not grant verification

5. Handoff
   - update `handoff/accepted_changes.md` with a concise P2.17 implementation entry including:
     - Worker route: Claude Code MAX/OAuth
     - Verifier: Hermes pending or Hermes to run after
     - Boundary: offline/local only
     - Tests run

## Forbidden changes

- No live scans, HTTP clients, sockets, exploit attempts, fuzzers, callbacks, brute force, or target-touching automation.
- No modification of `config/scope.txt`, `loot/`, credentials, `.env`, tokens, private keys, scheduler, deployment, billing, OAuth settings.
- No scanner/module runtime wiring.
- No promotion of metadata template to JSON Schema or registry.
- No CVSS/severity/exploitability finding state machine.
- No integration with existing program policy, preview ledger, preview manifest, or security headers runtime modules.
- No destructive cleanup.

## Validation to run if possible

- `python -m py_compile scripts/ctf_prepare_challenge.py scripts/ctf_review_decision.py scripts/test_ctf_prepare_challenge.py scripts/test_ctf_review_decision.py`
- `python scripts/test_ctf_prepare_challenge.py`
- `python scripts/test_ctf_review_decision.py`
- `git diff --check -- scripts/ctf_prepare_challenge.py scripts/ctf_review_decision.py scripts/test_ctf_prepare_challenge.py scripts/test_ctf_review_decision.py templates/ctf_verifier_metadata.yaml handoff/accepted_changes.md`

Stop and write a blocking note instead if any requirement appears to need target interaction or secrets.
