#!/usr/bin/env bash
set -Eeuo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PY="$SCRIPT_DIR/modern_vuln_api.py"
PORT="${1:-18080}"
PIDFILE="${TMPDIR:-/tmp}/hermes_modern_vuln_api_${PORT}.pid"
LOG="${TMPDIR:-/tmp}/hermes_modern_vuln_api_${PORT}.log"
if [ -f "$PIDFILE" ] && kill -0 "$(cat "$PIDFILE")" 2>/dev/null; then
  echo "already_running pid=$(cat "$PIDFILE") port=$PORT log=$LOG"
  exit 0
fi
nohup python3 "$PY" --host 0.0.0.0 --port "$PORT" >"$LOG" 2>&1 &
echo $! > "$PIDFILE"
for i in $(seq 1 30); do
  if curl -sS -o /dev/null -w '%{http_code}' --max-time 2 "http://127.0.0.1:$PORT/health" | grep -q '^200$'; then
    echo "started pid=$(cat "$PIDFILE") port=$PORT log=$LOG"
    exit 0
  fi
  sleep 0.5
done
echo "failed_to_start port=$PORT log=$LOG" >&2
cat "$LOG" >&2 || true
exit 1
