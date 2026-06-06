#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

python - <<'PY'
import json
from pathlib import Path
from jsonschema import Draft202012Validator

root = Path('.')
schema = json.loads(Path('schemas/live_bounty_lane_state.schema.json').read_text(encoding='utf-8'))
validator = Draft202012Validator(schema)
state_paths = sorted(root.glob('programs/*/lane_state*.json'))
if not state_paths:
    raise SystemExit('no live bounty lane_state files found')

errors = []
for path in state_paths:
    doc = json.loads(path.read_text(encoding='utf-8'))
    for err in sorted(validator.iter_errors(doc), key=lambda e: list(e.path)):
        where = '/'.join(str(p) for p in err.path) or '<root>'
        errors.append(f'{path}:{where}: {err.message}')
    if doc.get('operator_decision') not in {'EXECUTE', 'PASSIVE_ONLY', 'PARK', 'KILL'}:
        errors.append(f'{path}:operator_decision: missing valid operator decision vocabulary')
    if doc.get('machine_state') != doc.get('state'):
        errors.append(f'{path}:machine_state: must mirror state until runners migrate to the alias')

if errors:
    raise SystemExit('\n'.join(errors))
PY

echo PASS test_current_live_bounty_contracts
