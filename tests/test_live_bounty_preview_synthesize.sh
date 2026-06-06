#!/usr/bin/env bash
set -euo pipefail
unset TMPDIR || true

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
TMPDIR="$(mktemp -d)"
trap 'rm -rf "$TMPDIR"' EXIT

python - <<'PY' "$TMPDIR/valid_packet.json"
import copy, json, sys

def candidate(cid, title, status, impact, feasibility, readiness, request_budget="max 4 manual replay requests"):
    return {
        "candidate_id": cid,
        "title": title,
        "attacker_path": [
            "Model the product boundary from owned controls.",
            "Compare positive and negative controls without guessing identifiers or reading non-owned content."
        ],
        "impact_hypothesis": f"{title} could expose an authorization or isolation failure if bounded controls disagree.",
        "required_prerequisites": ["Account A", "Account B", "owned object provenance"],
        "impact_potential": impact,
        "surrogate_feasibility": feasibility,
        "authorization_readiness": readiness,
        "proof_boundary": {
            "in_scope_assets": ["fixture.example"],
            "owned_accounts_or_objects": ["Account A", "Account B", "owned object label only"],
            "request_budget": request_budget,
            "allowed_state_changes": ["none"],
            "blocked_state_changes": ["delete", "purchase", "invite", "credential creation"],
            "callback_oast_tunnel_allowance": "not_allowed",
            "data_contact_boundary": "stop if response contains non-owned private content; record status/length only"
        },
        "proof_surrogate": {
            "method": "A positive / B negative status and redacted body-shape comparison",
            "why_it_proves_impact_without_harm": "Authorization behavior is demonstrated by status/body-shape deltas without reading third-party content.",
            "positive_control": "Account A can access its own object.",
            "negative_control": "Account B receives deny/not-found/redacted response."
        },
        "stop_before": {
            "unauthorized_access": "do not proceed past a response that appears to grant Account B access",
            "non_owned_data": "do not read or store private content if it appears",
            "destructive_impact": "no mutation requests in this lane",
            "dos_or_resource_exhaustion": "fixed request budget only",
            "credential_or_token_access": "do not create, view, copy, or store credentials/tokens",
            "malware_persistence_evasion": "not applicable; any such requirement blocks the lane",
            "scope_expansion": "do not follow hosts outside fixture.example",
            "report_submission": "no report submission from this helper"
        },
        "evidence_requirements": ["status codes", "redacted response shape", "Account A/B labels only"],
        "execution_status": status
    }

packet = {
  "schema_version": "1.0",
  "program_slug": "fixture_program",
  "packet_id": "fixture_attack_paths",
  "authorization_source": "fixture offline policy packet; no target touched",
  "product_model": {
    "actors": ["Account A", "Account B"],
    "tenants_or_workspaces": ["Tenant A", "Tenant B"],
    "roles": ["owner", "member"],
    "objects": ["owned project", "owned comment"],
    "api_surfaces": ["documented project API"],
    "state_transitions": ["create", "share", "revoke"]
  },
  "candidates": [
    candidate("owned_object_replay", "Owned object replay boundary check", "bounded_executable", 5, 5, 5),
    candidate("dangerous_raw_export_path", "Raw export path that would be harmful if completed", "blocked_preserve", 5, 2, 1, "zero live export requests until separate approval"),
    candidate("tenant_boundary_probe", "Tenant boundary permission confusion", "needs_operator_control", 4, 3, 2),
    candidate("role_downgrade_api_mismatch", "Role downgrade UI/API mismatch", "needs_local_simulation", 4, 4, 1),
    candidate("share_revoke_lifecycle", "Share revoke lifecycle stale access", "reference_only", 3, 3, 1)
  ],
  "decision": {
    "selected_candidate_id": "owned_object_replay",
    "decision": "select_bounded_lane",
    "reason": "Only this candidate has owned controls and a bounded proof surrogate.",
    "next_artifact": "handoff/live_bounty_evidence/fixture_program/owned_object_replay/run_card.md"
  }
}
json.dump(packet, open(sys.argv[1], 'w', encoding='utf-8'), indent=2)
PY

python scripts/live-bounty-preview-synthesize.py validate "$TMPDIR/valid_packet.json" > "$TMPDIR/validate.json"
python - <<'PY' "$TMPDIR/validate.json"
import json, sys
r = json.load(open(sys.argv[1], encoding='utf-8'))
assert r['status'] == 'ok', r
assert r['errors'] == [], r
PY

python scripts/live-bounty-preview-synthesize.py synthesize "$TMPDIR/valid_packet.json" > "$TMPDIR/synthesize.json"
python - <<'PY' "$TMPDIR/synthesize.json"
import json, sys
r = json.load(open(sys.argv[1], encoding='utf-8'))
assert r['status'] == 'ok', r
assert r['target_touching'] is False, r
assert r['runner_mode'] == 'offline_attack_path_synthesis_only', r
assert len(r['selected_rows']) == 1, r
row = r['selected_rows'][0]
assert row['candidate_id'] == 'owned_object_replay', row
assert row['execution_status'] == 'bounded_executable', row
assert row['composite_rank'] == 15, row
assert 'unauthorized_access' in row['stop_before_keys'], row
packet_rows = r['packets'][0]['rows']
assert len(packet_rows) == 5, packet_rows
assert packet_rows[0]['selected'] is True, packet_rows
assert any(x['candidate_id'] == 'dangerous_raw_export_path' and x['execution_status'] == 'blocked_preserve' for x in packet_rows), packet_rows
PY

python - <<'PY' "$TMPDIR/valid_packet.json" "$TMPDIR/missing_surrogate.json" "$TMPDIR/empty_boundary.json" "$TMPDIR/missing_callback.json"
import copy, json, sys
packet = json.load(open(sys.argv[1], encoding='utf-8'))
p = copy.deepcopy(packet)
p['candidates'][0]['proof_surrogate']['method'] = ''
json.dump(p, open(sys.argv[2], 'w', encoding='utf-8'), indent=2)
p = copy.deepcopy(packet)
p['candidates'][0]['proof_boundary']['in_scope_assets'] = []
p['candidates'][0]['proof_boundary']['owned_accounts_or_objects'] = []
p['candidates'][0]['proof_boundary']['blocked_state_changes'] = []
json.dump(p, open(sys.argv[3], 'w', encoding='utf-8'), indent=2)
p = copy.deepcopy(packet)
p['candidates'][0]['proof_boundary'].pop('callback_oast_tunnel_allowance')
json.dump(p, open(sys.argv[4], 'w', encoding='utf-8'), indent=2)
PY
for bad in missing_surrogate empty_boundary missing_callback; do
  set +e
  python scripts/live-bounty-preview-synthesize.py validate "$TMPDIR/${bad}.json" > "$TMPDIR/${bad}_result.json"
  rc=$?
  set -e
  if [[ "$rc" -eq 0 ]]; then
    echo "$bad unexpectedly passed" >&2
    exit 1
  fi
  python - <<'PY' "$TMPDIR/${bad}_result.json"
import json, sys
r = json.load(open(sys.argv[1], encoding='utf-8'))
assert r['status'] == 'error', r
assert r['errors'], r
PY
done

python - <<'PY' "$TMPDIR/valid_packet.json" "$TMPDIR/two_selected_a.json" "$TMPDIR/two_selected_b.json"
import copy, json, sys
base = json.load(open(sys.argv[1], encoding='utf-8'))
for out, packet_id in [(sys.argv[2], 'a'), (sys.argv[3], 'b')]:
    p = copy.deepcopy(base)
    p['packet_id'] = f'fixture_attack_paths_{packet_id}'
    json.dump(p, open(out, 'w', encoding='utf-8'), indent=2)
PY
set +e
python scripts/live-bounty-preview-synthesize.py synthesize "$TMPDIR/two_selected_a.json" "$TMPDIR/two_selected_b.json" > "$TMPDIR/two_selected_result.json"
rc=$?
set -e
if [[ "$rc" -eq 0 ]]; then
  echo "two selected executable lanes unexpectedly passed" >&2
  exit 1
fi
python - <<'PY' "$TMPDIR/two_selected_result.json"
import json, sys
r = json.load(open(sys.argv[1], encoding='utf-8'))
assert r['status'] == 'error', r
assert any('more than one bounded executable' in e for e in r['errors']), r
PY

echo PASS test_live_bounty_preview_synthesize
