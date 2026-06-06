#!/usr/bin/env bash
set -Eeuo pipefail
PORT="${1:-18080}"
PIDFILE="${TMPDIR:-/tmp}/hermes_modern_vuln_api_${PORT}.pid"
if [ -f "$PIDFILE" ]; then
  pid=$(cat "$PIDFILE")
  if kill -0 "$pid" 2>/dev/null; then
    kill "$pid"
    echo "stopped pid=$pid port=$PORT"
  else
    echo "not_running stale_pid=$pid"
  fi
  rm -f "$PIDFILE"
else
  echo "not_running no_pidfile port=$PORT"
fi
