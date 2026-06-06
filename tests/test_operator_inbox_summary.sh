#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
TMPDIR="$(mktemp -d)"
trap 'rm -rf "$TMPDIR"' EXIT

cat > "$TMPDIR/candidates.json" <<'JSON'
{
  "schema_version": "1.0",
  "status": "ok",
  "mode": "dry_run_no_target",
  "target_touching": false,
  "candidate_count": 1,
  "candidates": [
    {
      "candidate_id": "cve_2026_6279_avada",
      "title": "Avada Builder passive exposure candidate",
      "summary": "Public advisory indicates exposed Fusion Builder versions may need passive version/fingerprint review.",
      "source_kind": "offline_passive_intel",
      "source_id": "cve_2026_6279_avada",
      "affected_technology": "wordpress-avada-fusion-builder",
      "operator_decision": "PASSIVE_ONLY",
      "machine_state": "CANDIDATE_REVIEW",
      "recommended_next_step": "Review in operator inbox; require program policy/scope gate before any live or target-touching action.",
      "references": ["https://example.invalid/advisory/<specific-cve-id>"],
      "safety": {
        "target_touching": false,
        "live_activation_allowed": false,
        "requires_policy_scope_gate": true,
        "blocked_actions": ["live_target_contact", "active_scanning", "fuzzing"]
      }
    }
  ]
}
JSON

python platform/inbox/operator_inbox_summary.py \
  --input "$TMPDIR/candidates.json" \
  --out "$TMPDIR/inbox.md" \
  --schema schemas/operator_inbox_candidate.schema.json > "$TMPDIR/stdout.json"

python - <<'PY' "$TMPDIR/stdout.json" "$TMPDIR/inbox.md"
import json, sys
status = json.load(open(sys.argv[1], encoding='utf-8'))
text = open(sys.argv[2], encoding='utf-8').read()
assert status['status'] == 'ok', status
assert status['candidate_count'] == 1, status
assert status['target_touching'] is False, status
assert '# Operator Inbox' in text, text
assert 'PASSIVE_ONLY' in text, text
assert 'Avada Builder passive exposure candidate' in text, text
assert 'Target touching: false' in text, text
assert 'Live activation allowed: false' in text, text
assert 'Requires policy/scope gate: true' in text, text
assert 'https://example.invalid/advisory/<specific-cve-id>' in text, text
assert 'Bearer ' not in text and 'Set-Cookie' not in text, text
PY

cat > "$TMPDIR/bad.json" <<'JSON'
{"schema_version":"1.0","status":"ok","mode":"dry_run_no_target","target_touching":true,"candidate_count":0,"candidates":[]}
JSON
if python platform/inbox/operator_inbox_summary.py --input "$TMPDIR/bad.json" --out "$TMPDIR/bad.md" --schema schemas/operator_inbox_candidate.schema.json > "$TMPDIR/bad_stdout.json"; then
  echo 'operator inbox summary unexpectedly accepted target_touching=true batch' >&2
  exit 1
fi
python - <<'PY' "$TMPDIR/bad_stdout.json"
import json, sys
r=json.load(open(sys.argv[1], encoding='utf-8'))
assert r['status']=='error', r
assert r['target_touching'] is False, r
assert r['errors'], r
PY

echo PASS test_operator_inbox_summary
