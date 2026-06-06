#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SCRIPT="$ROOT/scripts/labs/tmp_path_traversal_safe_marker_wave1.sh"

[ -f "$SCRIPT" ]
bash -n "$SCRIPT"

grep -q 'RUN_TMP_PATH_TRAVERSAL_ON_LOCAL_LAB' "$SCRIPT"
grep -q 'tmp@0.2.5' "$SCRIPT"
grep -q 'verified_tmp_path_traversal_arbitrary_file_creation_lab_only' "$SCRIPT"
grep -q 'No live targets' "$SCRIPT"

set +e
bash "$SCRIPT" --target https://example.org > "$ROOT/.n/tmp/tmp_path_traversal_forbidden.json" 2>/dev/null
code=$?
set -e
[ "$code" -eq 30 ]
python - <<'PY' "$ROOT/.n/tmp/tmp_path_traversal_forbidden.json"
import json, sys
payload=json.load(open(sys.argv[1], encoding='utf-8'))
assert payload['status']=='error'
assert payload['error']=='target_like_argument_rejected'
assert payload['target_touching'] is False
PY

echo "PASS test_tmp_path_traversal_safe_marker"
