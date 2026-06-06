#!/usr/bin/env bash
set -Eeuo pipefail
TARGET_HOST="${TARGET_HOST:-<lab-ip>}"
WEBGOAT="${WEBGOAT:-http://${TARGET_HOST}:8080/WebGoat}"
WEBWOLF="${WEBWOLF:-http://${TARGET_HOST}:9090/WebWolf}"
RUN_ID="webgoat_docker_wave1_$(date -u +%Y%m%dT%H%M%SZ)"
OUT="$HOME/codex-output/$RUN_ID"
mkdir -p "$OUT/http" "$OUT/nmap" "$OUT/browser"
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
status(){ curl -k -sS -o /dev/null -w '%{http_code}' --max-time 12 "$1" 2>/dev/null || echo 000; }
wait_for(){ local url="$1" name="$2"; local s=000; for i in $(seq 1 60); do s=$(status "$url"); if [ "$s" != 000 ] && [ "$s" != 502 ] && [ "$s" != 503 ]; then echo "$s"; return 0; fi; sleep 3; done; echo "$s"; return 1; }
WG_STATUS=$(wait_for "$WEBGOAT" webgoat || true)
WW_STATUS=$(wait_for "$WEBWOLF" webwolf || true)
json_obs category=health service=webgoat url="$WEBGOAT" status="$WG_STATUS"
json_obs category=health service=webwolf url="$WEBWOLF" status="$WW_STATUS"
{
  echo "# WebGoat Docker Wave 1"
  echo "target_host: $TARGET_HOST"
  echo "webgoat: $WEBGOAT status=$WG_STATUS"
  echo "webwolf: $WEBWOLF status=$WW_STATUS"
  echo "route: <attacker-vm> -> <victim-vm> host-only"
  echo
} > "$SUMMARY"

# Bounded HTTP surface collection: no fuzzing beyond known WebGoat/WebWolf paths.
paths=(
  "/WebGoat"
  "/WebGoat/login"
  "/WebGoat/registration"
  "/WebGoat/logout"
  "/WebGoat/actuator"
  "/WebGoat/swagger-ui.html"
  "/WebWolf"
  "/WebWolf/login"
)
for p in "${paths[@]}"; do
  port=8080
  [[ "$p" == /WebWolf* ]] && port=9090
  url="http://${TARGET_HOST}:${port}${p}"
  safe=$(echo "$p" | tr '/?' '__')
  hdr="$OUT/http/${safe}.headers.txt"
  body="$OUT/http/${safe}.body.txt"
  code=$(curl -k -sS --max-time 15 -D "$hdr" -o "$body" -w '%{http_code}' "$url" || echo 000)
  title=$(python3 - "$body" <<'PY'
import re,sys
try: data=open(sys.argv[1],errors='ignore').read(20000)
except Exception: data=''
m=re.search(r'<title[^>]*>(.*?)</title>', data, re.I|re.S)
print(re.sub(r'\s+',' ',m.group(1)).strip()[:120] if m else '')
PY
)
  json_obs category=http path="$p" url="$url" status="$code" title="$title" headers="$hdr" body="$body"
done

# Minimal nmap service fingerprint on known WebGoat/WebWolf ports only.
if command -v nmap >/dev/null 2>&1; then
  nmap -Pn -sV --version-light -p 8080,9090 "$TARGET_HOST" -oN "$OUT/nmap/webgoat_ports.nmap" -oX "$OUT/nmap/webgoat_ports.xml" >/dev/null || true
  json_obs category=nmap target="$TARGET_HOST" ports="8080,9090" artifact="$OUT/nmap/webgoat_ports.nmap"
fi

# Browser title/DOM proof, no credential capture.
CHROMIUM=$(command -v chromium || command -v chromium-browser || true)
if [ -n "$CHROMIUM" ]; then
  "$CHROMIUM" --headless --disable-gpu --no-sandbox --virtual-time-budget=3000 --dump-dom "$WEBGOAT" > "$OUT/browser/webgoat_dom.txt" 2>"$OUT/browser/webgoat_chromium.err" || true
  "$CHROMIUM" --headless --disable-gpu --no-sandbox --virtual-time-budget=3000 --dump-dom "$WEBWOLF" > "$OUT/browser/webwolf_dom.txt" 2>"$OUT/browser/webwolf_chromium.err" || true
  wg_marker=$(grep -Eio 'WebGoat|OWASP|login|registration' "$OUT/browser/webgoat_dom.txt" | head -5 | tr '\n' ',' | sed 's/,$//' || true)
  ww_marker=$(grep -Eio 'WebWolf|OWASP|login' "$OUT/browser/webwolf_dom.txt" | head -5 | tr '\n' ',' | sed 's/,$//' || true)
  json_obs category=browser service=webgoat markers="$wg_marker" artifact="$OUT/browser/webgoat_dom.txt"
  json_obs category=browser service=webwolf markers="$ww_marker" artifact="$OUT/browser/webwolf_dom.txt"
fi

# Summarize key observations.
{
  echo "## Key observations"
  python3 - "$OBS" <<'PY'
import json,sys
for line in open(sys.argv[1],encoding='utf-8'):
    d=json.loads(line)
    if d.get('category') in {'health','http','browser','nmap'}:
        bits=[f"{k}={v}" for k,v in d.items() if k not in {'ts','headers','body','artifact'}]
        print('- ' + ' '.join(bits))
PY
} >> "$SUMMARY"

echo "$OUT" > "$HOME/codex-output/latest_webgoat_docker_wave1.txt"
echo "$OUT"
