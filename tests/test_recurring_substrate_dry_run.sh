#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
TMPDIR="$(mktemp -d)"
trap 'rm -rf "$TMPDIR"' EXIT

cat > "$TMPDIR/passive_intel.json" <<'JSON'
{
  "schema_version": "1.0",
  "generated_at": "2026-05-28T00:00:00Z",
  "items": [
    {
      "id": "overclaim_execute_input",
      "source_type": "cve_advisory",
      "title": "Overclaim input must be downgraded",
      "summary": "Fixture proves dry-run passive intake cannot emit EXECUTE even when upstream input recommends it.",
      "affected_technology": "test-only",
      "recommended_decision": "EXECUTE",
      "references": ["https://example.invalid/overclaim"]
    }
  ]
}
JSON

python platform/pipeline/recurring_substrate_dry_run.py \
  --input "$TMPDIR/passive_intel.json" \
  --out "$TMPDIR/candidates.json" \
  --schema schemas/operator_inbox_candidate.schema.json > "$TMPDIR/stdout.json"

python - <<'PY' "$TMPDIR/stdout.json" "$TMPDIR/candidates.json"
import json, sys
stdout = json.load(open(sys.argv[1], encoding='utf-8'))
out = json.load(open(sys.argv[2], encoding='utf-8'))
assert stdout == out, (stdout, out)
assert out['status'] == 'ok', out
assert out['mode'] == 'dry_run_no_target', out
assert out['target_touching'] is False, out
assert out['candidate_count'] == 1, out
candidate = out['candidates'][0]
assert candidate['operator_decision'] == 'PASSIVE_ONLY', candidate
assert candidate['machine_state'] == 'CANDIDATE_REVIEW', candidate
assert candidate['source_kind'] == 'offline_passive_intel', candidate
assert candidate['safety']['target_touching'] is False, candidate
assert candidate['safety']['live_activation_allowed'] is False, candidate
assert 'exploit' not in json.dumps(candidate).lower(), candidate
PY

if python platform/pipeline/recurring_substrate_dry_run.py --live --input "$TMPDIR/passive_intel.json" --out "$TMPDIR/live.json" > "$TMPDIR/live_stdout.json"; then
  echo 'dry-run substrate unexpectedly accepted --live' >&2
  exit 1
fi
python - <<'PY' "$TMPDIR/live_stdout.json"
import json, sys
r = json.load(open(sys.argv[1], encoding='utf-8'))
assert r['status'] == 'error', r
assert r['target_touching'] is False, r
assert any('--live is not supported' in e for e in r['errors']), r
PY

echo PASS test_recurring_substrate_dry_run
