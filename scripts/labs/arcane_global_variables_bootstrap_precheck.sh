#!/usr/bin/env bash
# Arcane <specific-ghsa-id> local bootstrap PRECHECK/RENDER helper.
# Safe default: does not launch Arcane, does not mount any Docker socket, does not send proof requests.
set -Eeuo pipefail

MODE="precheck"
ALLOW_RENDER_COMPOSE="0"
for arg in "$@"; do
  case "$arg" in
    --precheck-only) MODE="precheck" ;;
    --render-compose) MODE="render"; ALLOW_RENDER_COMPOSE="1" ;;
    -h|--help)
      cat <<'HELP'
Usage: bash scripts/labs/arcane_global_variables_bootstrap_precheck.sh [--precheck-only|--render-compose]

Purpose:
  Fail-closed local-lab readiness helper for Arcane <specific-ghsa-id>.
  It prepares evidence directories and checks the Docker/socket posture before any later target launch.

Modes:
  --precheck-only   Default. Environment/posture checks only. No target launch, no proof request.
  --render-compose  Also writes a disposable-lab compose template under the artifact directory.
                    The template is not executed and still needs operator review.

Boundary:
  - local lab only; intended for <victim-vm> or equivalent disposable victim VM
  - no public/live targets
  - no Arcane launch in this script
  - no Docker socket mount in this script
  - no exploit/proof endpoint request in this script
  - no host/user Docker socket allowed
HELP
      exit 0
      ;;
    *) echo "Unknown argument: $arg" >&2; exit 2 ;;
  esac
done

RUN_ID="${RUN_ID:-arcane_global_variables_precheck_$(date -u +%Y%m%dT%H%M%SZ)}"
PROJECT_ROOT="${PROJECT_ROOT:-/mnt/hacking}"
OUT_ROOT="${OUT_ROOT:-$HOME/<artifact-output-dir>}"
OUT="$OUT_ROOT/$RUN_ID"
VICTIM_IP="${VICTIM_IP:-<lab-ip>}"
ARCANE_VULN_IMAGE="${ARCANE_VULN_IMAGE:-ghcr.io/getarcaneapp/arcane:v1.19.1}"
ARCANE_PATCHED_IMAGE="${ARCANE_PATCHED_IMAGE:-ghcr.io/getarcaneapp/arcane:v1.19.2}"
ARCANE_PORT="${ARCANE_PORT:-3552}"
DISPOSABLE_DOCKER_ENDPOINT="${DISPOSABLE_DOCKER_ENDPOINT:-tcp://arcane-dind:2375}"
ALLOW_HOST_DOCKER_SOCKET="${ALLOW_HOST_DOCKER_SOCKET:-0}"

mkdir -p "$OUT/diagnostics" "$OUT/templates" "$OUT/decision"
log(){ printf '[%s] %s\n' "$(date -u +%H:%M:%SZ)" "$*" | tee -a "$OUT/run.log"; }
fail(){ log "ERROR: $*"; echo "blocked" > "$OUT/decision/verdict.txt"; printf '%s\n' "$*" > "$OUT/decision/block_reason.txt"; exit 1; }

internet_state(){
  if timeout 3 bash -lc '</dev/tcp/1.1.1.1/80' 2>/dev/null; then
    echo internet_open
  else
    echo internet_closed
  fi
}

check_lab_boundary(){
  [[ "$VICTIM_IP" == 192.168.56.* ]] || fail "VICTIM_IP must stay on host-only lab range <lab-ip>/24; got $VICTIM_IP"
  [[ "$ARCANE_PORT" =~ ^[0-9]+$ ]] || fail "ARCANE_PORT must be numeric"
  [[ "$ARCANE_VULN_IMAGE" == "ghcr.io/getarcaneapp/arcane:v1.19.1" ]] || fail "ARCANE_VULN_IMAGE must stay pinned to ghcr.io/getarcaneapp/arcane:v1.19.1 for this candidate"
  [[ "$ARCANE_PATCHED_IMAGE" == "ghcr.io/getarcaneapp/arcane:v1.19.2" ]] || fail "ARCANE_PATCHED_IMAGE must stay pinned to ghcr.io/getarcaneapp/arcane:v1.19.2 for patched comparison"
}

check_docker_posture(){
  command -v docker >/dev/null || fail "docker CLI missing on this host/VM"
  docker version > "$OUT/diagnostics/docker_version.txt" 2>&1 || fail "docker CLI cannot talk to a daemon; do not continue until a disposable victim-lab daemon is selected"
  docker context inspect > "$OUT/diagnostics/docker_context_inspect.json" 2>&1 || true
  docker info > "$OUT/diagnostics/docker_info.txt" 2>&1 || true

  local docker_host="${DOCKER_HOST:-unix:///var/run/docker.sock}"
  printf '%s\n' "$docker_host" > "$OUT/diagnostics/effective_docker_host.txt"

  if [[ "$ALLOW_HOST_DOCKER_SOCKET" != "1" ]]; then
    case "$docker_host" in
      unix:///var/run/docker.sock|/var/run/docker.sock|"")
        fail "effective Docker endpoint is the default host/user socket ($docker_host). Arcane must use a disposable nested daemon/proxy, not the host Docker socket."
        ;;
    esac
  fi

  if [[ "$DISPOSABLE_DOCKER_ENDPOINT" =~ var/run/docker\.sock ]]; then
    fail "DISPOSABLE_DOCKER_ENDPOINT mentions /var/run/docker.sock; use an isolated TCP endpoint for this precheck template"
  fi
}

write_compose_template(){
  cat > "$OUT/templates/compose.arcane.disposable.template.yaml" <<EOF
# REVIEW-ONLY TEMPLATE. Do not run until Hermes/operator confirms disposable Docker posture.
# Safe objective: later local-lab Arcane role-boundary proof for <specific-ghsa-id>.
# This template intentionally avoids mounting /var/run/docker.sock from the host.
services:
  arcane-vulnerable:
    image: ${ARCANE_VULN_IMAGE}
    ports:
      - "127.0.0.1:${ARCANE_PORT}:3552"
    environment:
      PORT: "3552"
      DATABASE_URL: "sqlite:///data/arcane.db"
      DOCKER_HOST: "${DISPOSABLE_DOCKER_ENDPOINT}"
    volumes:
      - arcane-data:/data
    depends_on:
      - arcane-dind

  arcane-dind:
    image: docker:27-dind
    privileged: true
    environment:
      DOCKER_TLS_CERTDIR: ""
    command: ["dockerd", "--host=tcp://0.0.0.0:2375", "--host=unix:///var/run/docker.sock"]
    volumes:
      - arcane-dind-data:/var/lib/docker

volumes:
  arcane-data:
  arcane-dind-data:
EOF

  cat > "$OUT/templates/next_manual_steps.md" <<EOF
# Arcane disposable bootstrap next manual steps (not executed)

1. Review \\`compose.arcane.disposable.template.yaml\\`.
2. Confirm this is running only inside \\`<victim-vm>\\` or equivalent disposable VM.
3. Confirm no host/user Docker socket is mounted into Arcane.
4. If image pulls require NAT, open NAT temporarily, pull images, then close and verify Internet is closed before proof execution.
5. Only after separate approval, launch vulnerable Arcane and create throwaway admin/member accounts.
6. Proof objective remains marker-only config write/readback:
   - unauth control denied
   - admin baseline succeeds
   - non-admin write to \\`/api/environments/0/templates/variables\\` unexpectedly succeeds on v1.19.1
   - non-admin separate admin-only control denied
   - patched v1.19.2 denies non-admin if comparison is run
EOF
}

log "RUN_ID=$RUN_ID"
log "MODE=$MODE"
log "OUT=$OUT"
log "PROJECT_ROOT=$PROJECT_ROOT"
log "VICTIM_IP=$VICTIM_IP"
log "ARCANE_VULN_IMAGE=$ARCANE_VULN_IMAGE"
log "ARCANE_PATCHED_IMAGE=$ARCANE_PATCHED_IMAGE"
log "No target launch/proof request will be performed by this script."

check_lab_boundary
internet_state | tee "$OUT/diagnostics/internet_pre.txt" >/dev/null
check_docker_posture

if [[ "$ALLOW_RENDER_COMPOSE" == "1" ]]; then
  write_compose_template
fi

cat > "$OUT/summary.md" <<EOF
# Arcane <specific-ghsa-id> bootstrap precheck

run_id: $RUN_ID
mode: $MODE
verdict: precheck_passed_no_target_touched
victim_ip: $VICTIM_IP
vulnerable_image: $ARCANE_VULN_IMAGE
patched_image: $ARCANE_PATCHED_IMAGE
effective_docker_host: $(cat "$OUT/diagnostics/effective_docker_host.txt" 2>/dev/null || echo unknown)
internet_pre: $(cat "$OUT/diagnostics/internet_pre.txt" 2>/dev/null || echo unknown)

Boundary confirmed by script:
- no Arcane container launched
- no proof endpoint request sent
- no accounts created
- no public/live target touched
- default host/user Docker socket rejected unless explicitly overridden outside this script

Next gate:
- operator/Hermes must confirm disposable Docker daemon/proxy posture before any setup/proof run
EOF

echo "precheck_passed_no_target_touched" > "$OUT/decision/verdict.txt"
log "summary=$OUT/summary.md"
log "verdict=precheck_passed_no_target_touched"
