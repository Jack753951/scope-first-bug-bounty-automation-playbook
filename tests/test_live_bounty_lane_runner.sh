#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
TMPDIR="$(mktemp -d)"
trap 'rm -rf "$TMPDIR"' EXIT

cat > "$TMPDIR/blocked_state.json" <<'JSON'
{
  "schema_version": "1.0",
  "program_slug": "fixture_program",
  "lane_id": "fixture_blocked_lane",
  "lane_title": "Fixture blocked lane",
  "autonomy_level": "A2",
  "state": "A2_PENDING_OPERATOR_AUTH",
  "status": "blocked_operator_action",
  "authorization": {
    "program_url": "https://<bug-bounty-platform>.com/fixture_program",
    "scope_file": "programs/fixture_program/scope.json",
    "global_scope_entries": ["fixture.example"],
    "dry_run_gate": "passed",
    "out_of_scope_control": "failed_closed"
  },
  "lane_boundary": {
    "allowed_actions": ["manual_noVNC_signup_login", "owned_account_surface_map"],
    "blocked_actions": ["scanner", "fuzzer", "DAST", "report_submission"],
    "identity_strategy": "fixture_alias_required"
  },
  "operator_gates": ["complete_fixture_login_locally"],
  "stop_conditions": ["captcha", "otp_or_email_verification", "lane_complete_or_exhausted"],
  "next_autonomous_action": "after_operator_identity_gate_prepare_fixture_surface_map",
  "next_operator_action": "complete fixture alias signup/login locally",
  "artifacts": {
    "dry_run_packet": "handoff/fixture_dry_run.md",
    "evidence_dir": "handoff/live_bounty_evidence/fixture_program/fixture_blocked_lane"
  },
  "learning": {
    "preview_references": ["OWASP WSTG reference-only"],
    "next_preview_seed": "blocked fixture"
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
      "program_slug": "fixture_program",
      "lane_id": "fixture_blocked_lane",
      "state_file": "$TMPDIR/blocked_state.json",
      "priority": 1,
      "status": "blocked_operator_action"
    }
  ]
}
JSON

set +e
python scripts/live-bounty-lane-runner.py --queue "$TMPDIR/blocked_queue.json" --status-out "$TMPDIR/blocked_status.json" > "$TMPDIR/blocked_stdout.json"
blocked_rc=$?
set -e
if [[ "$blocked_rc" -eq 0 ]]; then
    echo 'runner unexpectedly returned success for blocked_operator_action lane' >&2
    exit 1
fi
if [[ "$blocked_rc" -ne 10 ]]; then
    echo "runner returned $blocked_rc for blocked_operator_action, expected 10" >&2
    exit 1
fi
python - <<'PY' "$TMPDIR/blocked_stdout.json" "$TMPDIR/blocked_status.json"
import json, sys
stdout = json.load(open(sys.argv[1], encoding='utf-8'))
status = json.load(open(sys.argv[2], encoding='utf-8'))
for doc in [stdout, status]:
    assert doc['decision'] == 'blocked_operator_action', doc
    assert doc['exit_code'] == 10, doc
    assert doc['program_slug'] == 'fixture_program', doc
    assert doc['lane_id'] == 'fixture_blocked_lane', doc
    assert doc['next_operator_action'].startswith('complete fixture alias'), doc
    assert doc['next_autonomous_action'].startswith('after_operator_identity_gate'), doc
    assert doc['target_touching'] is False, doc
    assert doc['runner_mode'] == 'local_orchestration_only', doc
assert stdout == status, (stdout, status)
PY

cat > "$TMPDIR/ready_state.json" <<'JSON'
{
  "schema_version": "1.0",
  "program_slug": "fixture_program",
  "lane_id": "fixture_ready_lane",
  "lane_title": "Fixture ready lane",
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
    "allowed_actions": ["local_preview_generation", "surface_map_template_preparation"],
    "blocked_actions": ["scanner", "fuzzer", "DAST", "report_submission"],
    "identity_strategy": "fixture_no_live_identity"
  },
  "operator_gates": [],
  "stop_conditions": ["candidate_could_be_report_ready", "stronger_technique_needed"],
  "next_autonomous_action": "prepare_local_preview_packet_only",
  "next_operator_action": "none",
  "artifacts": {
    "dry_run_packet": "handoff/fixture_dry_run.md",
    "evidence_dir": "handoff/live_bounty_evidence/fixture_program/fixture_ready_lane"
  },
  "learning": {
    "preview_references": ["OWASP WSTG reference-only"],
    "next_preview_seed": "generate local preview checklist"
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
      "lane_id": "fixture_ready_lane",
      "state_file": "$TMPDIR/ready_state.json",
      "priority": 1,
      "status": "ready"
    }
  ]
}
JSON
python scripts/live-bounty-lane-runner.py --queue "$TMPDIR/ready_queue.json" --status-out "$TMPDIR/ready_status.json" > "$TMPDIR/ready_stdout.json"
python - <<'PY' "$TMPDIR/ready_stdout.json" "$TMPDIR/ready_status.json"
import json, sys
stdout = json.load(open(sys.argv[1], encoding='utf-8'))
status = json.load(open(sys.argv[2], encoding='utf-8'))
for doc in [stdout, status]:
    assert doc['decision'] == 'autonomous_local_action_available', doc
    assert doc['exit_code'] == 0, doc
    assert doc['next_autonomous_action'] == 'prepare_local_preview_packet_only', doc
    assert doc['target_touching'] is False, doc
    assert doc['blocked_actions'] == ['scanner', 'fuzzer', 'DAST', 'report_submission'], doc
assert stdout == status, (stdout, status)
PY

cat > "$TMPDIR/closed_state.json" <<'JSON'
{
  "schema_version": "1.0",
  "program_slug": "fixture_program",
  "lane_id": "fixture_closed_lane",
  "lane_title": "Fixture closed lane",
  "autonomy_level": "A2",
  "state": "NO_FINDING_CLOSEOUT",
  "status": "no_finding",
  "authorization": {
    "program_url": "https://<bug-bounty-platform>.com/fixture_program",
    "scope_file": "programs/fixture_program/scope.json",
    "global_scope_entries": ["fixture.example"],
    "dry_run_gate": "passed",
    "out_of_scope_control": "failed_closed"
  },
  "lane_boundary": {
    "allowed_actions": ["surface_map_closeout"],
    "blocked_actions": ["scanner", "fuzzer", "DAST", "report_submission"],
    "identity_strategy": "fixture_identity_completed"
  },
  "operator_gates": ["future_lanes_require_new_approval"],
  "stop_conditions": ["lane_complete_or_exhausted"],
  "next_autonomous_action": "none_lane_closed",
  "next_operator_action": "review checkpoint",
  "artifacts": {
    "dry_run_packet": "handoff/fixture_dry_run.md",
    "evidence_dir": "handoff/live_bounty_evidence/fixture_program/fixture_closed_lane",
    "latest_evidence": "handoff/live_bounty_evidence/fixture_program/fixture_closed_lane/evidence.json"
  },
  "learning": {
    "preview_references": ["OWASP WSTG reference-only"],
    "next_preview_seed": "closed no-finding lane"
  },
  "updated_at": "2026-05-25"
}
JSON
cat > "$TMPDIR/closed_queue.json" <<JSON
{
  "schema_version": "1.0",
  "updated_at": "2026-05-25",
  "lanes": [
    {
      "program_slug": "fixture_program",
      "lane_id": "fixture_closed_lane",
      "state_file": "$TMPDIR/closed_state.json",
      "priority": 1,
      "status": "no_finding"
    }
  ]
}
JSON
python scripts/live-bounty-lane-runner.py --queue "$TMPDIR/closed_queue.json" --status-out "$TMPDIR/closed_status.json" > "$TMPDIR/closed_stdout.json"
python - <<'PY' "$TMPDIR/closed_stdout.json" "$TMPDIR/closed_status.json"
import json, sys
stdout = json.load(open(sys.argv[1], encoding='utf-8'))
status = json.load(open(sys.argv[2], encoding='utf-8'))
for doc in [stdout, status]:
    assert doc['decision'] == 'lane_closed_or_parked', doc
    assert doc['exit_code'] == 0, doc
    assert doc['status'] == 'no_finding', doc
    assert doc['next_autonomous_action'] == 'none_lane_closed', doc
    assert doc['target_touching'] is False, doc
assert stdout == status, (stdout, status)
PY

cat > "$TMPDIR/bad_queue.json" <<'JSON'
{
  "schema_version": "1.0",
  "updated_at": "2026-05-25",
  "lanes": [
    {
      "program_slug": "missing_program",
      "lane_id": "missing_lane",
      "state_file": "programs/missing_program/missing_lane_state.json",
      "priority": 1,
      "status": "ready"
    }
  ]
}
JSON
set +e
python scripts/live-bounty-lane-runner.py --queue "$TMPDIR/bad_queue.json" --status-out "$TMPDIR/bad_status.json" > "$TMPDIR/bad_stdout.json"
bad_rc=$?
set -e
if [[ "$bad_rc" -eq 0 ]]; then
    echo 'runner unexpectedly accepted invalid queue' >&2
    exit 1
fi
if [[ "$bad_rc" -ne 30 ]]; then
    echo "runner returned $bad_rc for invalid queue, expected 30" >&2
    exit 1
fi
python - <<'PY' "$TMPDIR/bad_stdout.json" "$TMPDIR/bad_status.json"
import json, sys
stdout = json.load(open(sys.argv[1], encoding='utf-8'))
status = json.load(open(sys.argv[2], encoding='utf-8'))
for doc in [stdout, status]:
    assert doc['decision'] == 'invalid_queue_or_state', doc
    assert doc['exit_code'] == 30, doc
    assert doc['target_touching'] is False, doc
    assert any('state_file does not exist' in e for e in doc['errors']), doc
assert stdout == status, (stdout, status)
PY

set +e
python scripts/live-bounty-lane-runner.py --queue "$TMPDIR/ready_queue.json" --target https://fixture.example > "$TMPDIR/target_stdout.json"
target_rc=$?
set -e
if [[ "$target_rc" -eq 0 ]]; then
    echo 'runner unexpectedly accepted target-touching argument' >&2
    exit 1
fi
if [[ "$target_rc" -ne 30 ]]; then
    echo "runner returned $target_rc for target argument, expected 30" >&2
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

set +e
python scripts/live-bounty-lane-runner.py --queue "$TMPDIR/ready_queue.json" --target > "$TMPDIR/bare_target_stdout.json"
bare_target_rc=$?
set -e
if [[ "$bare_target_rc" -ne 30 ]]; then
    echo "runner returned $bare_target_rc for bare --target, expected 30 structured fail-closed" >&2
    exit 1
fi
python - <<'PY' "$TMPDIR/bare_target_stdout.json"
import json, sys
r = json.load(open(sys.argv[1], encoding='utf-8'))
assert r['decision'] == 'invalid_queue_or_state', r
assert r['exit_code'] == 30, r
assert r['target_touching'] is False, r
assert any('target-touching arguments are not supported' in e for e in r['errors']), r
PY

echo PASS test_live_bounty_lane_runner
