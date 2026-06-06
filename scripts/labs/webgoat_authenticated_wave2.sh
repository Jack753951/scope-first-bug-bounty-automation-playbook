#!/usr/bin/env bash
set -Eeuo pipefail
TARGET_HOST="${TARGET_HOST:-<lab-ip>}"
WEBGOAT="${WEBGOAT:-http://${TARGET_HOST}:8080/WebGoat}"
WEBWOLF="${WEBWOLF:-http://${TARGET_HOST}:9090/WebWolf}"
RUN_ID="webgoat_authenticated_wave2_$(date -u +%Y%m%dT%H%M%SZ)"
OUT_DIR="${OUT_DIR:-$HOME/<artifact-output-dir>/${RUN_ID}}"
SHORT_TS="$(date -u +%H%M%S)"
USER_A="${USER_A:-hga${SHORT_TS}}"
USER_B="${USER_B:-hgb${SHORT_TS}}"
PASS="${PASS:-webgoat}"
mkdir -p "$OUT_DIR" "$OUT_DIR/http" "$OUT_DIR/html" "$OUT_DIR/browser"
OBS="$OUT_DIR/observations.jsonl"
: > "$OBS"
log(){ printf '[%s] %s\n' "$(date -u +%H:%M:%S)" "$*" | tee -a "$OUT_DIR/run.log" >&2; }
json_escape(){ python -c 'import json,sys; print(json.dumps(sys.stdin.read())[1:-1])'; }
obs(){ local typ="$1" name="$2" val="$3"; printf '{"type":"%s","name":"%s","value":"%s"}\n' "$typ" "$name" "$(printf '%s' "$val" | json_escape)" >> "$OBS"; }
http_code(){ curl -sS -m 10 -o /dev/null -w '%{http_code}' "$1" || true; }
pre=$(http_code "$WEBGOAT/login")
obs health pre_webgoat_login "$pre"
log "pre WebGoat login status=$pre"
if [[ "$pre" != "200" ]]; then log "pre health failed"; exit 2; fi
register_user(){
  local user="$1" jar="$2" prefix="$3"
  curl -sS -m 10 -c "$jar" -D "$OUT_DIR/http/${prefix}_registration_get.headers" -o "$OUT_DIR/html/${prefix}_registration_get.html" "$WEBGOAT/registration" >/dev/null
  local code
  code=$(curl -sS -m 12 -b "$jar" -c "$jar" -D "$OUT_DIR/http/${prefix}_register.headers" -o "$OUT_DIR/html/${prefix}_register.html" -w '%{http_code}' \
    -X POST "$WEBGOAT/register.mvc" \
    --data-urlencode "username=$user" \
    --data-urlencode "password=$PASS" \
    --data-urlencode "matchingPassword=$PASS" \
    --data-urlencode 'agree=agree' || true)
  obs register_status "$prefix" "$code"
  log "register $prefix user=$user status=$code"
}
login_user(){
  local user="$1" jar="$2" prefix="$3"
  local code
  code=$(curl -sS -m 12 -b "$jar" -c "$jar" -D "$OUT_DIR/http/${prefix}_login.headers" -o "$OUT_DIR/html/${prefix}_start.html" -w '%{http_code}' \
    -X POST "$WEBGOAT/login" \
    --data-urlencode "username=$user" \
    --data-urlencode "password=$PASS" || true)
  obs login_status "$prefix" "$code"
  if grep -q 'JSESSIONID' "$jar"; then obs session_cookie "$prefix" present; else obs session_cookie "$prefix" missing; fi
  log "login $prefix user=$user status=$code"
}
JAR_A="$OUT_DIR/user_a.cookies"; JAR_B="$OUT_DIR/user_b.cookies"
register_user "$USER_A" "$JAR_A" user_a
register_user "$USER_B" "$JAR_B" user_b
login_user "$USER_A" "$JAR_A" user_a
login_user "$USER_B" "$JAR_B" user_b
# Authenticated endpoint enumeration: fixed low-risk GET list only.
paths=(
  /start.mvc
  /service/lessonmenu.mvc
  /service/restartlesson.mvc
  /service/lessonoverview.mvc
  /service/progress.mvc
  /WebGoatContent/css/webgoat.css
  /lesson/IDOR.lesson
  /lesson/JWT.lesson
  /lesson/CrossSiteScripting.lesson
  /lesson/PathTraversal.lesson
  /lesson/AccessControl.lesson
)
printf 'path,status,bytes,title_or_marker\n' > "$OUT_DIR/authenticated_gets.csv"
for p in "${paths[@]}"; do
  safe=$(printf '%s' "$p" | tr '/?' '__')
  code=$(curl -sS -m 10 -b "$JAR_A" -D "$OUT_DIR/http/get_${safe}.headers" -o "$OUT_DIR/html/get_${safe}.html" -w '%{http_code}' "$WEBGOAT$p" || true)
  bytes=$(wc -c < "$OUT_DIR/html/get_${safe}.html" | tr -d ' ')
  marker=$(python - <<PY
from pathlib import Path
import re
s=Path('$OUT_DIR/html/get_${safe}.html').read_text(errors='ignore')
for pat in [r'<title>(.*?)</title>', r'lesson-title[^>]*>(.*?)<', r'(IDOR|JWT|Cross Site Scripting|Path Traversal|Access Control|WebGoat)']:
 m=re.search(pat,s,re.I|re.S)
 if m:
  print(re.sub(r'\\s+',' ',m.group(1) if m.lastindex else m.group(0)).strip()[:120]); break
else: print('')
PY
)
  printf '%s,%s,%s,%s\n' "$p" "$code" "$bytes" "${marker//,/ }" >> "$OUT_DIR/authenticated_gets.csv"
  obs authenticated_get "$p" "status=$code bytes=$bytes marker=$marker"
done
# Pull lesson JS / page references from authenticated start page and lesson menu outputs.
python - <<PY > "$OUT_DIR/discovered_references.txt"
from pathlib import Path
import re
root=Path('$OUT_DIR/html')
seen=set()
for p in root.glob('*.html'):
 s=p.read_text(errors='ignore')
 for m in re.finditer(r'(?i)(?:href|src)=["\']([^"\']+)["\']', s):
  u=m.group(1)
  if any(k.lower() in u.lower() for k in ['idor','jwt','xss','cross','path','lesson','service','webgoat']): seen.add(u)
 for m in re.finditer(r'(?i)(/WebGoat/[^"\' <]+|/lesson/[^"\' <]+|/service/[^"\' <]+)', s):
  if any(k.lower() in m.group(1).lower() for k in ['idor','jwt','xss','cross','path','lesson','service','webgoat']): seen.add(m.group(1))
for u in sorted(seen): print(u)
PY
obs discovered_references_count count "$(wc -l < "$OUT_DIR/discovered_references.txt" | tr -d ' ')"
# Browser evidence intentionally deferred: Kali Playwright driver is currently broken/missing.
# This wave keeps HTTP/session evidence only and records the browser blocker for the next XSS-runtime lane.
obs browser_logged_in proof deferred_playwright_driver_missing
post=$(http_code "$WEBGOAT/login")
obs health post_webgoat_login "$post"
log "post WebGoat login status=$post"
cat > "$OUT_DIR/summary.md" <<EOF
# WebGoat authenticated wave 2

Target: $WEBGOAT
Run ID: $RUN_ID
Users: throwaway user_a/user_b stored only as generated names in this artifact
Pre health: $pre
Post health: $post

## Auth results

- user_a registration/login artifacts captured
- user_b registration/login artifacts captured
- session cookies captured in local artifact jar files for lab-only replay

## Authenticated enumeration

See authenticated_gets.csv and discovered_references.txt.

## Boundaries

- local authorized lab only
- no credential theft
- no external callbacks
- no destructive writes
- no brute force
- no real secret reads
- no lesson exploit payloads yet; this wave is auth/session/enumeration readiness
EOF
log "artifacts $OUT_DIR"
