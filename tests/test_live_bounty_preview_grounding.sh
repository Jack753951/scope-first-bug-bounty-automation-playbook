#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
TMPDIR="$(mktemp -d)"
trap 'rm -rf "$TMPDIR"' EXIT

cat > "$TMPDIR/ready_state.json" <<'JSON'
{
  "schema_version": "1.0",
  "program_slug": "fixture_program",
  "lane_id": "auth_session_profile_empty_state",
  "lane_title": "Auth/session/profile/workspace empty-state first flow",
  "autonomy_level": "A2",
  "state": "A3_PREVIEW_REQUIRED",
  "status": "ready",
  "authorization": {
    "program_url": "https://<bug-bounty-platform>.com/fixture_program",
    "scope_file": "programs/fixture_program/scope.json",
    "global_scope_entries": ["fixture.example"],
    "dry_run_gate": "passed",
    "out_of_scope_control": "failed_closed"
  },
  "lane_boundary": {
    "allowed_actions": ["local_preview_generation", "surface_map_template_preparation", "owned_account_surface_map"],
    "blocked_actions": ["scanner", "fuzzer", "DAST", "callbacks_or_webhooks", "workflow_execution", "report_submission"],
    "identity_strategy": "fixture_no_live_identity"
  },
  "operator_gates": [],
  "stop_conditions": ["candidate_could_be_report_ready", "stronger_technique_needed", "unexpected_third_party_data"],
  "next_autonomous_action": "prepare_local_preview_packet_only",
  "next_operator_action": "none",
  "artifacts": {
    "dry_run_packet": "handoff/fixture_dry_run.md",
    "evidence_dir": "handoff/live_bounty_evidence/fixture_program/auth_session_profile_empty_state"
  },
  "learning": {
    "preview_references": ["OWASP WSTG authentication/session management references", "PortSwigger authentication/access-control labs reference-only"],
    "next_preview_seed": "Map owned-account auth/session/profile/workspace empty states without executing workflows.",
    "reusable_capability": "reference-grounded local preview packet"
  },
  "updated_at": "2026-05-25"
}
JSON

cat > "$TMPDIR/ready_queue.json" <<JSON
{
  "schema_version": "1.0",
  "updated_at": "2026-05-25",
  "lanes": [
    {
      "program_slug": "fixture_program",
      "lane_id": "auth_session_profile_empty_state",
      "state_file": "$TMPDIR/ready_state.json",
      "priority": 1,
      "status": "ready"
    }
  ]
}
JSON

python scripts/live-bounty-preview-grounding.py \
  --queue "$TMPDIR/ready_queue.json" \
  --output-dir "$TMPDIR/references" \
  --date 2026-05-25 \
  --status-out "$TMPDIR/grounding_status.json" \
  > "$TMPDIR/grounding_stdout.json"

python - <<'PY' "$TMPDIR/grounding_stdout.json" "$TMPDIR/grounding_status.json" "$TMPDIR/references/fixture_program_auth_session_profile_empty_state_grounding_20260525.md"
import json, sys
stdout = json.load(open(sys.argv[1], encoding='utf-8'))
status = json.load(open(sys.argv[2], encoding='utf-8'))
path = sys.argv[3]
assert stdout == status, (stdout, status)
for doc in [stdout, status]:
    assert doc['decision'] == 'grounding_written', doc
    assert doc['target_touching'] is False, doc
    assert doc['runner_mode'] == 'local_reference_generation_only', doc
    assert doc['program_slug'] == 'fixture_program', doc
    assert doc['lane_id'] == 'auth_session_profile_empty_state', doc
    assert doc['output_path'].endswith('fixture_program_auth_session_profile_empty_state_grounding_20260525.md'), doc
text = open(path, encoding='utf-8').read()
required = [
    '# Live bounty preview grounding: fixture_program / auth_session_profile_empty_state',
    'Boundary: local reference generation only',
    'No target request, browser automation, scanner, fuzzer, DAST, callback, exploit, workflow execution, or report submission is authorized by this file.',
    'OWASP WSTG',
    'OWASP ASVS',
    'PortSwigger Web Security Academy',
    'Reference-only scanner/template metadata',
    'Positive controls',
    'Negative controls',
    'Evidence thresholds',
    'report_ready',
    'no_finding',
    'Blocked techniques',
    'scanner',
    'fuzzer',
    'DAST',
    'Next safe local action',
]
for needle in required:
    assert needle in text, needle
for forbidden in ['verified_reportable', 'confirmed vulnerability', 'run nuclei', 'run sqlmap', 'execute scanner']:
    assert forbidden not in text, forbidden
PY

cat > "$TMPDIR/blocked_state.json" <<'JSON'
{
  "schema_version": "1.0",
  "program_slug": "fixture_blocked",
  "lane_id": "auth_session_profile_empty_state",
  "lane_title": "Auth/session/profile/workspace empty-state blocked fixture",
  "autonomy_level": "A2",
  "state": "A2_PENDING_OPERATOR_AUTH",
  "status": "blocked_operator_action",
  "authorization": {
    "program_url": "https://<bug-bounty-platform>.com/fixture_blocked",
    "scope_file": "programs/fixture_blocked/scope.json",
    "global_scope_entries": ["blocked.fixture.example"],
    "dry_run_gate": "not_run",
    "out_of_scope_control": "not_applicable"
  },
  "lane_boundary": {
    "allowed_actions": ["local_preview_generation"],
    "blocked_actions": ["target_touching", "scanner", "fuzzer", "DAST", "report_submission"],
    "identity_strategy": "operator must complete auth outside repo/chat"
  },
  "operator_gates": ["complete <bug-bounty-platform>-alias signup/login"],
  "stop_conditions": ["operator gate incomplete", "unexpected target touch requested"],
  "next_autonomous_action": "none_until_operator_auth_gate",
  "next_operator_action": "complete <bug-bounty-platform>-alias signup/login",
  "artifacts": {
    "dry_run_packet": "handoff/fixture_blocked_dry_run.md",
    "evidence_dir": "handoff/live_bounty_evidence/fixture_blocked/auth_session_profile_empty_state"
  },
  "learning": {
    "preview_references": ["blocked fixture reference"],
    "next_preview_seed": "blocked fixture should preserve operator gate"
  },
  "updated_at": "2026-05-25"
}
JSON
cat > "$TMPDIR/blocked_queue.json" <<JSON
{
  "schema_version": "1.0",
  "updated_at": "2026-05-25",
  "lanes": [
    {
      "program_slug": "fixture_blocked",
      "lane_id": "auth_session_profile_empty_state",
      "state_file": "$TMPDIR/blocked_state.json",
      "priority": 1,
      "status": "blocked_operator_action"
    }
  ]
}
JSON

python scripts/live-bounty-preview-grounding.py --queue "$TMPDIR/blocked_queue.json" --output-dir "$TMPDIR/blocked_refs" --date 2026-05-25 > "$TMPDIR/blocked_stdout.json"
python - <<'PY' "$TMPDIR/blocked_stdout.json" "$TMPDIR/blocked_refs/fixture_blocked_auth_session_profile_empty_state_grounding_20260525.md"
import json, sys
r = json.load(open(sys.argv[1], encoding='utf-8'))
assert r['decision'] == 'grounding_written', r
text = open(sys.argv[2], encoding='utf-8').read()
assert 'Current lane status: `blocked_operator_action`' in text, text
assert 'Next operator gate' in text, text
assert 'complete <bug-bounty-platform>-alias signup/login' in text, text
assert 'Do not treat this grounding packet as permission to touch the target.' in text, text
PY

set +e
python scripts/live-bounty-preview-grounding.py --queue "$TMPDIR/ready_queue.json" --target > "$TMPDIR/target_stdout.json"
target_rc=$?
set -e
if [[ "$target_rc" -ne 30 ]]; then
    echo "grounding generator returned $target_rc for bare --target, expected 30" >&2
    exit 1
fi
python - <<'PY' "$TMPDIR/target_stdout.json"
import json, sys
r = json.load(open(sys.argv[1], encoding='utf-8'))
assert r['decision'] == 'invalid_queue_or_state', r
assert r['exit_code'] == 30, r
assert r['target_touching'] is False, r
assert any('target-touching arguments are not supported' in e for e in r['errors']), r
PY

echo PASS test_live_bounty_preview_grounding
