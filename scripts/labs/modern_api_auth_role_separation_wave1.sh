#!/usr/bin/env bash
set -euo pipefail

TARGET="${TARGET:-http://127.0.0.1:18084}"
RUN_ID="${RUN_ID:-modern_api_auth_role_separation_$(date -u +%Y%m%dT%H%M%SZ)}"
OUT="${OUT:-<artifact-output-dir>/${RUN_ID}}"
START_LOCAL="${START_LOCAL:-1}"
SERVER_PID=""

mkdir -p "$OUT/requests" "$OUT/responses"
OBS="$OUT/observations.jsonl"
: > "$OBS"

json_obs() {
  python - "$@" >> "$OBS" <<'PY'
import json, sys, time
obj = {"ts": time.time()}
for arg in sys.argv[1:]:
    if "=" in arg:
        k, v = arg.split("=", 1)
        obj[k] = v
print(json.dumps(obj, sort_keys=True))
PY
}

cleanup() {
  if [ -n "${SERVER_PID:-}" ]; then
    kill "$SERVER_PID" >/dev/null 2>&1 || true
    wait "$SERVER_PID" >/dev/null 2>&1 || true
  fi
}
trap cleanup EXIT

if [ "$START_LOCAL" = "1" ]; then
  python labs/modern_vuln_api/modern_vuln_api.py --host 127.0.0.1 --port 18084 > "$OUT/server.log" 2>&1 &
  SERVER_PID="$!"
fi

for i in $(seq 1 30); do
  PRE=$(curl -sS -o "$OUT/responses/health_pre.json" -w '%{http_code}' "$TARGET/health" || true)
  [ "$PRE" = "200" ] && break
  sleep 0.2
done
json_obs category=health name=pre_health status="$PRE" target="$TARGET"
[ "$PRE" = "200" ] || { echo "target_unhealthy pre=$PRE" >&2; exit 2; }

login() {
  local user="$1" pass="$2" out="$3"
  local status
  status=$(curl -sS -o "$out" -w '%{http_code}' \
    -H 'Content-Type: application/json' \
    --data "{\"username\":\"$user\",\"password\":\"$pass\"}" \
    "$TARGET/api/login")
  json_obs category=auth name="login_${user}" status="$status" artifact="$out"
  [ "$status" = "200" ] || return 1
  python - "$out" <<'PY'
import json, sys
print(json.load(open(sys.argv[1], encoding='utf-8'))['token'])
PY
}

ALICE_TOKEN=$(login alice alicepass "$OUT/responses/login_alice.json")
ADMIN_TOKEN=$(login admin adminpass "$OUT/responses/login_admin.json")

request() {
  local name="$1" token="$2" path="$3" out="$4"
  local status
  if [ -n "$token" ]; then
    status=$(curl -sS -o "$out" -w '%{http_code}' -H "Authorization: Bearer $token" "$TARGET$path" || true)
  else
    status=$(curl -sS -o "$out" -w '%{http_code}' "$TARGET$path" || true)
  fi
  json_obs category=request name="$name" path="$path" status="$status" artifact="$out"
  printf '%s' "$status"
}

NOAUTH_AUDIT=$(request noauth_admin_audit "" /api/admin/audit-log "$OUT/responses/noauth_admin_audit.json")
ALICE_ME=$(request alice_me "$ALICE_TOKEN" /api/me "$OUT/responses/alice_me.json")
ALICE_AUDIT=$(request alice_admin_audit "$ALICE_TOKEN" /api/admin/audit-log "$OUT/responses/alice_admin_audit.json")
ADMIN_AUDIT=$(request admin_admin_audit "$ADMIN_TOKEN" /api/admin/audit-log "$OUT/responses/admin_admin_audit.json")
ALICE_SETTINGS=$(request alice_admin_settings_control "$ALICE_TOKEN" /api/admin/settings "$OUT/responses/alice_admin_settings_control.json")
ADMIN_SETTINGS=$(request admin_admin_settings_control "$ADMIN_TOKEN" /api/admin/settings "$OUT/responses/admin_admin_settings_control.json")
POST=$(curl -sS -o "$OUT/responses/health_post.json" -w '%{http_code}' "$TARGET/health" || true)
json_obs category=health name=post_health status="$POST" target="$TARGET"

python - "$OUT" "$NOAUTH_AUDIT" "$ALICE_ME" "$ALICE_AUDIT" "$ADMIN_AUDIT" "$ALICE_SETTINGS" "$ADMIN_SETTINGS" "$POST" > "$OUT/summary_values.json" <<'PY'
import json, pathlib, sys
out = pathlib.Path(sys.argv[1])
statuses = {
    "noauth_audit": sys.argv[2],
    "alice_me": sys.argv[3],
    "alice_audit": sys.argv[4],
    "admin_audit": sys.argv[5],
    "alice_settings_control": sys.argv[6],
    "admin_settings_control": sys.argv[7],
    "post_health": sys.argv[8],
}
def load(name):
    return json.loads((out / 'responses' / name).read_text(encoding='utf-8'))
alice_audit = load('alice_admin_audit.json') if statuses['alice_audit'] == '200' else {}
admin_audit = load('admin_admin_audit.json') if statuses['admin_audit'] == '200' else {}
alice_settings = load('alice_admin_settings_control.json') if statuses['alice_settings_control'] in {'200','403'} else {}
admin_settings = load('admin_admin_settings_control.json') if statuses['admin_settings_control'] == '200' else {}
marker = 'ADMIN_AUDIT_MARKER_HERMES_LOCAL_LAB'
result = {
    'statuses': statuses,
    'alice_audit_marker_found': marker in json.dumps(alice_audit),
    'admin_audit_marker_found': marker in json.dumps(admin_audit),
    'alice_audit_requested_role': alice_audit.get('requested_role'),
    'alice_settings_control_error': alice_settings.get('error'),
    'admin_settings_control_marker_found': 'ADMIN_SETTINGS_CONTROL_HERMES_LOCAL_LAB' in json.dumps(admin_settings),
}
result['verdict'] = 'verified_role_separation_bypass_lab_only' if (
    statuses['noauth_audit'] == '401' and
    statuses['alice_me'] == '200' and
    statuses['alice_audit'] == '200' and result['alice_audit_marker_found'] and result['alice_audit_requested_role'] == 'user' and
    statuses['admin_audit'] == '200' and result['admin_audit_marker_found'] and
    statuses['alice_settings_control'] == '403' and
    statuses['admin_settings_control'] == '200' and result['admin_settings_control_marker_found'] and
    statuses['post_health'] == '200'
) else 'attempted_not_verified'
print(json.dumps(result, indent=2, sort_keys=True))
PY
VERDICT=$(python - "$OUT/summary_values.json" <<'PY'
import json, sys
print(json.load(open(sys.argv[1], encoding='utf-8'))['verdict'])
PY
)
json_obs category=verdict name=auth_role_separation verdict="$VERDICT" artifact="$OUT/summary_values.json"

cat > "$OUT/summary.md" <<EOF
# Modern API Auth/Session Role-Separation Wave 1

Run: $RUN_ID
Target: $TARGET
Verdict: $VERDICT

## Purpose

Phase 4 ability-gap proof for real-target-style auth/session role separation: two roles, explicit unauthenticated control, normal-user positive access to an admin-only audit marker, and secure admin-settings control that rejects the normal user.

## Evidence shape

- Unauthenticated /api/admin/audit-log control: $NOAUTH_AUDIT, expected 401.
- Alice /api/me: $ALICE_ME, expected 200 normal user session.
- Alice /api/admin/audit-log: $ALICE_AUDIT, expected vulnerable 200 with ADMIN_AUDIT_MARKER_HERMES_LOCAL_LAB despite role=user.
- Admin /api/admin/audit-log: $ADMIN_AUDIT, expected 200 baseline admin access.
- Alice /api/admin/settings: $ALICE_SETTINGS, expected 403 secure-role control.
- Admin /api/admin/settings: $ADMIN_SETTINGS, expected 200 secure-role control.
- Post-health: $POST.

## Boundary

Authorized local lab only. Lab-owned marker data only. No public target, brute force, credential theft, sensitive data, persistence, exfiltration, destructive write, or automatic report/finding promotion.

## Artifacts

- observations: observations.jsonl
- summary values: summary_values.json
- responses: responses/*.json
- server log when START_LOCAL=1: server.log
EOF

echo "OUT=$OUT"
echo "VERDICT=$VERDICT"
[ "$VERDICT" = "verified_role_separation_bypass_lab_only" ]
