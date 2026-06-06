#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
TMPDIR="$(mktemp -d)"
trap 'rm -rf "$TMPDIR"' EXIT

python - <<'PY'
import json
from pathlib import Path
from jsonschema import Draft202012Validator

schema_paths = [
    Path('schemas/live_bounty_lane_state.schema.json'),
    Path('schemas/live_bounty_evidence.schema.json'),
]
for path in schema_paths:
    if not path.exists():
        raise SystemExit(f'missing schema: {path}')
    schema = json.loads(path.read_text(encoding='utf-8'))
    Draft202012Validator.check_schema(schema)

state_schema = json.loads(Path('schemas/live_bounty_lane_state.schema.json').read_text(encoding='utf-8'))
evidence_schema = json.loads(Path('schemas/live_bounty_evidence.schema.json').read_text(encoding='utf-8'))

valid_state = {
    'schema_version': '1.0',
    'program_slug': '<program-slug>',
    'lane_id': 'auth_session_profile_empty_state',
    'lane_title': 'Auth/session/profile/workspace empty-state first flow',
    'autonomy_level': 'A2',
    'state': 'A2_PENDING_OPERATOR_AUTH',
    'status': 'blocked_operator_action',
    'authorization': {
        'program_url': 'https://<bug-bounty-platform>.com/<program-slug>',
        'scope_file': 'programs/<program-slug>/scope.json',
        'global_scope_entries': ['login.<program-redacted>.com'],
        'dry_run_gate': 'passed',
        'out_of_scope_control': 'failed_closed'
    },
    'lane_boundary': {
        'allowed_actions': ['manual_noVNC_signup_login', 'owned_account_surface_map'],
        'blocked_actions': ['scanner', 'fuzzer', 'DAST', 'report_submission'],
        'identity_strategy': 'hackerone_alias_preferred'
    },
    'operator_gates': ['hackerone_alias_signup_login'],
    'stop_conditions': ['captcha', 'otp', 'unexpected_third_party_data', 'candidate_report_ready'],
    'next_autonomous_action': 'prepare_noVNC_surface_map_after_operator_auth',
    'next_operator_action': 'complete <bug-bounty-platform>-alias signup/login or choose proxy header strategy',
    'artifacts': {
        'dry_run_packet': 'handoff/tines_automation_vdp_phase5a_dry_run_packet_20260525.md',
        'evidence_dir': 'evidence/live_bounty/<program-slug>/auth_session_profile_empty_state'
    },
    'learning': {
        'preview_references': ['OWASP WSTG ATHN', 'PortSwigger authentication labs'],
        'next_preview_seed': 'session/profile empty-state map after login'
    },
    'updated_at': '2026-05-25'
}
Draft202012Validator(state_schema).validate(valid_state)

invalid_state = dict(valid_state)
invalid_state.pop('next_autonomous_action')
errors = list(Draft202012Validator(state_schema).iter_errors(invalid_state))
if not errors:
    raise SystemExit('invalid lane state without next_autonomous_action unexpectedly validated')

valid_evidence = {
    'schema_version': '1.0',
    'program_slug': '<program-slug>',
    'lane_id': 'auth_session_profile_empty_state',
    'status': 'blocked_operator_action',
    'request_budget': {'planned': 0, 'used': 0},
    'observations': [
        {'type': 'gate', 'label': 'dry_run_gate', 'value': 'in_scope_pass_out_of_scope_fail', 'sensitive': False}
    ],
    'positive_evidence': ['login.<program-redacted>.com dry-run safe_target PASS'],
    'negative_controls': ['example.org dry-run safe_target FAIL'],
    'redactions': ['no secrets captured'],
    'candidate_signals': [],
    'blocked_states': ['operator_identity_strategy_required'],
    'next_learning_seed': 'surface-map owned workspace after alias login',
    'updated_at': '2026-05-25'
}
Draft202012Validator(evidence_schema).validate(valid_evidence)

invalid_evidence = dict(valid_evidence)
invalid_evidence['status'] = 'verified_reportable'
errors = list(Draft202012Validator(evidence_schema).iter_errors(invalid_evidence))
if not errors:
    raise SystemExit('invalid promotional evidence status unexpectedly validated')
PY

cat > "$TMPDIR/clean.md" <<'EOF'
Account A reached login page on 2026-05-25. Status: blocked_operator_action. No secrets captured.
EOF
python scripts/evidence-redaction-check.py "$TMPDIR/clean.md" --json > "$TMPDIR/clean.json"
python - <<'PY' "$TMPDIR/clean.json"
import json, sys
r = json.load(open(sys.argv[1], encoding='utf-8'))
assert r['status'] == 'clean', r
assert r['findings'] == [], r
PY

cat > "$TMPDIR/leaky.md" <<'EOF'
Authorization: Bearer eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxMjMifQ.sig
Set-Cookie: sessionid=abc123
contact test@example.com
EOF
if python scripts/evidence-redaction-check.py "$TMPDIR/leaky.md" --json > "$TMPDIR/leaky.json"; then
    echo 'redaction checker unexpectedly accepted leaky evidence' >&2
    exit 1
fi
python - <<'PY' "$TMPDIR/leaky.json"
import json, sys
text = open(sys.argv[1], encoding='utf-8').read()
assert 'eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxMjMifQ.sig' not in text, text
assert 'sessionid=abc123' not in text, text
assert 'test@example.com' not in text, text
r = json.loads(text)
assert r['status'] == 'blocked', r
kinds = {f['kind'] for f in r['findings']}
assert {'authorization_header', 'set_cookie', 'email_address'} <= kinds, kinds
for finding in r['findings']:
    assert '<REDACTED' in finding['excerpt'], finding
PY

cat > "$TMPDIR/bad_queue.json" <<'EOF'
{
  "schema_version": "1.0",
  "updated_at": "2026-05-25",
  "lanes": [
    {
      "program_slug": "missing_program",
      "lane_id": "missing_lane",
      "state_file": "programs/missing_program/missing_lane_state.json",
      "priority": 1,
      "status": "blocked_operator_action"
    }
  ]
}
EOF
if python scripts/live-bounty-lane-status.py queue --queue "$TMPDIR/bad_queue.json" > "$TMPDIR/bad_queue_result.json"; then
    echo 'lane status helper unexpectedly accepted queue with missing state_file' >&2
    exit 1
fi
python - <<'PY' "$TMPDIR/bad_queue_result.json"
import json, sys
r = json.load(open(sys.argv[1], encoding='utf-8'))
assert r['status'] == 'error', r
assert any('state_file does not exist' in e for e in r['errors']), r
PY

cat > "$TMPDIR/queue.json" <<'EOF'
{
  "schema_version": "1.0",
  "updated_at": "2026-05-25",
  "lanes": [
    {
      "program_slug": "<program-slug>",
      "lane_id": "auth_session_profile_empty_state",
      "state_file": "programs/<program-slug>/lane_state.json",
      "priority": 1,
      "status": "blocked_operator_action"
    }
  ]
}
EOF
python scripts/live-bounty-lane-status.py validate \
  --queue "$TMPDIR/queue.json" \
  --state-json - <<'JSON' > "$TMPDIR/status.json"
{
  "schema_version": "1.0",
  "program_slug": "<program-slug>",
  "lane_id": "auth_session_profile_empty_state",
  "lane_title": "Auth/session/profile/workspace empty-state first flow",
  "autonomy_level": "A2",
  "state": "A2_PENDING_OPERATOR_AUTH",
  "status": "blocked_operator_action",
  "authorization": {
    "program_url": "https://<bug-bounty-platform>.com/<program-slug>",
    "scope_file": "programs/<program-slug>/scope.json",
    "global_scope_entries": ["login.<program-redacted>.com"],
    "dry_run_gate": "passed",
    "out_of_scope_control": "failed_closed"
  },
  "lane_boundary": {
    "allowed_actions": ["manual_noVNC_signup_login", "owned_account_surface_map"],
    "blocked_actions": ["scanner", "fuzzer", "DAST", "report_submission"],
    "identity_strategy": "hackerone_alias_preferred"
  },
  "operator_gates": ["hackerone_alias_signup_login"],
  "stop_conditions": ["captcha", "otp", "unexpected_third_party_data", "candidate_report_ready"],
  "next_autonomous_action": "prepare_noVNC_surface_map_after_operator_auth",
  "next_operator_action": "complete <bug-bounty-platform>-alias signup/login or choose proxy header strategy",
  "artifacts": {
    "dry_run_packet": "handoff/tines_automation_vdp_phase5a_dry_run_packet_20260525.md",
    "evidence_dir": "evidence/live_bounty/<program-slug>/auth_session_profile_empty_state"
  },
  "learning": {
    "preview_references": ["OWASP WSTG ATHN", "PortSwigger authentication labs"],
    "next_preview_seed": "session/profile empty-state map after login"
  },
  "updated_at": "2026-05-25"
}
JSON
python - <<'PY' "$TMPDIR/status.json"
import json, sys
r = json.load(open(sys.argv[1], encoding='utf-8'))
assert r['status'] == 'ok', r
assert r['lane']['state'] == 'A2_PENDING_OPERATOR_AUTH', r
assert r['lane']['next_operator_action'].startswith('complete <bug-bounty-platform>-alias'), r
PY

echo PASS test_live_bounty_state_and_redaction
