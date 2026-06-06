#!/usr/bin/env bash
set -Eeuo pipefail
TARGET_HOST="${TARGET_HOST:-<lab-ip>}"
WEBGOAT="${WEBGOAT:-http://${TARGET_HOST}:8080/WebGoat}"
RUN_ID="webgoat_jwt_wave3_$(date -u +%Y%m%dT%H%M%SZ)"
OUT_DIR="${OUT_DIR:-$HOME/<artifact-output-dir>/${RUN_ID}}"
SHORT_TS="$(date -u +%H%M%S)"
WG_USER="${WG_USER:-jwt${SHORT_TS}}"
PASS="${PASS:-webgoat}"
mkdir -p "$OUT_DIR/http" "$OUT_DIR/html" "$OUT_DIR/js" "$OUT_DIR/jwt_probe"
OBS="$OUT_DIR/observations.jsonl"
: > "$OBS"
json_escape(){ python -c 'import json,sys; print(json.dumps(sys.stdin.read())[1:-1])'; }
obs(){ local typ="$1" name="$2" val="$3"; printf '{"type":"%s","name":"%s","value":"%s"}\n' "$typ" "$name" "$(printf '%s' "$val" | json_escape)" >> "$OBS"; }
http_code(){ curl -sS -m 10 -o /dev/null -w '%{http_code}' "$1" || true; }
pre=$(http_code "$WEBGOAT/login")
obs health pre_webgoat_login "$pre"
if [[ "$pre" != "200" ]]; then echo "pre health failed: $pre" >&2; exit 2; fi
JAR="$OUT_DIR/cookies.jar"
curl -sS -m 10 -c "$JAR" -D "$OUT_DIR/http/register_get.headers" -o "$OUT_DIR/html/register_get.html" "$WEBGOAT/registration" >/dev/null
reg=$(curl -sS -m 12 -b "$JAR" -c "$JAR" -D "$OUT_DIR/http/register_post.headers" -o "$OUT_DIR/html/register_post.html" -w '%{http_code}' \
  -X POST "$WEBGOAT/register.mvc" \
  --data-urlencode "username=$WG_USER" \
  --data-urlencode "password=$PASS" \
  --data-urlencode "matchingPassword=$PASS" \
  --data-urlencode 'agree=agree' || true)
obs register_status throwaway "$reg"
login=$(curl -sS -m 12 -b "$JAR" -c "$JAR" -D "$OUT_DIR/http/login.headers" -o "$OUT_DIR/html/start.html" -w '%{http_code}' \
  -X POST "$WEBGOAT/login" \
  --data-urlencode "username=$WG_USER" \
  --data-urlencode "password=$PASS" || true)
obs login_status throwaway "$login"
if grep -q 'JSESSIONID' "$JAR"; then obs session_cookie throwaway present; else obs session_cookie throwaway missing; fi
# Authenticated fetch of JWT lesson material and client scripts.
for p in JWT.lesson lesson_js/jwt-voting.js lesson_js/jwt-weak-keys.js lesson_js/jwt-refresh.js lesson_js/jwt-jku.js lesson_js/jwt-kid.js lesson_js/jwt-buy.js images/logs.txt; do
  safe="${p//\//_}"
  out="$OUT_DIR/${safe}"
  code=$(curl -sS -m 12 -b "$JAR" -D "$OUT_DIR/http/${safe}.headers" -o "$out" -w '%{http_code}' "$WEBGOAT/$p" || true)
  bytes=$(wc -c < "$out" | tr -d ' ')
  obs authenticated_fetch "$p" "status=$code bytes=$bytes"
done
python - <<PY > "$OUT_DIR/endpoint_extract.txt"
from pathlib import Path
import re
root=Path('$OUT_DIR')
texts=[]
for p in [root/'JWT.lesson', *root.glob('lesson_js_*.js')]:
    if p.exists(): texts.append((p.name,p.read_text(errors='ignore')))
seen=set()
for name,s in texts:
    for m in re.finditer(r'(?:action="|url:\s*["\']?|["\'])(/?WebGoat/)?JWT/[A-Za-z0-9_./?=&:%+-]+', s):
        seen.add(m.group(0).strip('"\''))
    for m in re.finditer(r'/WebGoat/JWT/[A-Za-z0-9_./?=&:%+-]+', s):
        seen.add(m.group(0))
for item in sorted(seen): print(item)
PY
# Low-risk decode assignment proof first: submit known decoded user if possible.
for candidate_user in WebGoat Tom user Jerry; do
  decode_body=$(curl -sS -m 10 -b "$JAR" -D "$OUT_DIR/http/jwt_decode_${candidate_user}.headers" -o "$OUT_DIR/jwt_probe/jwt_decode_${candidate_user}.json" -w '%{http_code}' \
    -X POST "$WEBGOAT/JWT/decode" \
    --data-urlencode "jwt-encode-user=$candidate_user" || true)
  if grep -q '"lessonCompleted" : true' "$OUT_DIR/jwt_probe/jwt_decode_${candidate_user}.json"; then
    obs jwt_decode_verified "$candidate_user" "status=$decode_body lessonCompleted=true"
  else
    obs jwt_decode_submit "$candidate_user" "status=$decode_body lessonCompleted=false"
  fi
done
# Probe voting login/token endpoints without brute force. Use lesson-visible users only.
for u in Tom Jerry; do
  code=$(curl -sS -m 10 -b "$JAR" -D "$OUT_DIR/http/votings_login_${u}.headers" -o "$OUT_DIR/jwt_probe/votings_login_${u}.json" -w '%{http_code}' "$WEBGOAT/JWT/votings/login?user=$u" || true)
  obs jwt_votings_login "$u" "$code"
done
# Extract any bearer-like JWTs from response artifacts and decode locally without external services.
python - <<PY > "$OUT_DIR/jwt_probe/decoded_tokens.jsonl"
from pathlib import Path
import re, base64, json
root=Path('$OUT_DIR')
seen=[]
for p in list((root/'jwt_probe').glob('*'))+list(root.glob('*')):
    if p.is_file():
        s=p.read_text(errors='ignore')
        for m in re.finditer(r'eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+', s):
            tok=m.group(0)
            if tok not in seen: seen.append(tok)
def dec(part):
    part += '='*((4-len(part)%4)%4)
    return json.loads(base64.urlsafe_b64decode(part.encode()).decode())
for tok in seen:
    h,p,_=tok.split('.',2)
    try: out={'token_prefix':tok[:24], 'header':dec(h), 'payload':dec(p)}
    except Exception as e: out={'token_prefix':tok[:24], 'error':str(e)}
    print(json.dumps(out, sort_keys=True))
PY
obs decoded_token_count count "$(wc -l < "$OUT_DIR/jwt_probe/decoded_tokens.jsonl" | tr -d ' ')"
post=$(http_code "$WEBGOAT/login")
obs health post_webgoat_login "$post"
cat > "$OUT_DIR/summary.md" <<EOF
# WebGoat JWT wave 3

Target: $WEBGOAT
Run ID: $RUN_ID
Pre health: $pre
Registration status: $reg
Login status: $login
Post health: $post

## Scope
- local authorized WebGoat lab only
- JWT/token lesson only
- no public targets
- no brute force/dictionary cracking
- no credential theft
- no external callbacks
- no destructive writes

## Outputs
- JWT lesson page and JavaScript fetched for local review
- endpoint_extract.txt lists JWT lesson endpoints/actions
- jwt_probe/ contains bounded decode/voting login probes
- decoded_tokens.jsonl contains local offline JWT header/payload decoding only
EOF
echo "$OUT_DIR"
