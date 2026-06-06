#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
WORK="$ROOT/tmp/agent_capability_substrate_test"
rm -rf "$WORK"
mkdir -p "$WORK"

python - "$WORK" <<'PY'
import json
import sys
from pathlib import Path

work = Path(sys.argv[1])

def write(name, data):
    (work / name).write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")

stop = {
    "unauthorized_access": "stop before unauthorized access",
    "non_owned_data": "stop before non-owned data",
    "destructive_impact": "stop before destructive impact",
    "dos_or_resource_exhaustion": "stop before resource exhaustion",
    "credential_or_token_access": "stop before credentials/tokens",
    "malware_persistence_evasion": "stop before malware/persistence/evasion",
    "scope_expansion": "stop before scope expansion",
    "report_submission": "stop before report submission"
}
boundary = {
    "in_scope_assets": ["pending logged-in asset confirmation"],
    "owned_accounts_or_objects": ["owned synthetic object only"],
    "request_budget": "offline fixture only",
    "allowed_state_changes": ["none in fixture"],
    "blocked_state_changes": ["no customer/message send"],
    "data_contact_boundary": "owned synthetic data only",
    "callback_oast_tunnel_allowance": "not_allowed"
}
surrogate = {
    "method": "compare owned positive/negative controls",
    "why_it_proves_impact_without_harm": "no non-owned data or live side effect",
    "positive_control": "owner sees own object",
    "negative_control": "lower role denied"
}
def cand(i, status="blocked_preserve"):
    return {
        "candidate_id": f"cand_{i}",
        "title": f"Candidate {i}",
        "attacker_path": ["model path only"],
        "impact_hypothesis": "authz mismatch would matter if proven",
        "required_prerequisites": ["scope confirmation"],
        "proof_boundary": boundary,
        "proof_surrogate": surrogate,
        "stop_before": stop,
        "evidence_requirements": ["redacted A/B control evidence"],
        "execution_status": status,
        "impact_potential": 3,
        "surrogate_feasibility": 3,
        "authorization_readiness": 2
    }
packet = {
    "schema_version": "1.0",
    "program_slug": "<program-redacted>",
    "packet_id": "program-redacted_fixture_packet",
    "authorization_source": "offline fixture only",
    "product_model": {
        "actors": ["owner", "lower role"],
        "tenants_or_workspaces": ["owned workspace"],
        "roles": ["admin", "member"],
        "objects": ["synthetic object"],
        "api_surfaces": ["api docs reference only"],
        "state_transitions": ["role downgrade"]
    },
    "candidates": [cand(1, "bounded_executable"), cand(2), cand(3), cand(4), cand(5)],
    "decision": {"selected_candidate_id": "cand_1", "decision": "select_bounded_lane", "reason": "fixture selects bounded lane"}
}
write("candidate.json", packet)
write("planner.json", {"role": "adversarial-planner", "artifact": "fixture/planner", "verdict": "PASS", "candidate_ids": ["cand_1"], "claims": ["impact plausible"], "blockers": []})
write("critic_block.json", {"role": "evidence-critic", "artifact": "fixture/critic", "verdict": "REQUEST_CHANGES", "candidate_ids": ["cand_1"], "claims": [], "blockers": ["evidence too weak"]})
write("critic_pass.json", {"role": "evidence-critic", "artifact": "fixture/critic", "verdict": "PASS", "candidate_ids": ["cand_1"], "claims": ["controls defined"], "blockers": []})
ready = {
    "schema_version": "1.0",
    "profile": "<attacker-vm>",
    "checked_at": "2026-05-26",
    "readiness": "ready",
    "target_touching_allowed": False,
    "checks": [
        {"name": "project_mount", "status": "pass", "evidence": "fixture", "command_safe_to_rerun": True},
        {"name": "host_only_network", "status": "pass", "evidence": "fixture", "command_safe_to_rerun": True},
        {"name": "nat_closed", "status": "pass", "evidence": "fixture", "command_safe_to_rerun": True}
    ],
    "conditions": [{"type": "KaliReady", "status": "True", "reason": "Fixture", "message": "fixture ready", "last_transition_time": "2026-05-26"}],
    "blockers": [],
    "warnings": [],
    "next_action": "none"
}
write("kali_ready.json", ready)
bad = dict(ready)
bad["checks"] = [dict(c) for c in ready["checks"]]
bad["checks"][2]["status"] = "fail"
write("kali_bad_nat.json", bad)
evidence = {
    "schema_version": "1.0",
    "program_slug": "<program-slug>",
    "lane_id": "auth_session_profile_empty_state",
    "status": "surface_only",
    "request_budget": {"planned": 10, "used": 4},
    "observations": [{"type": "ui", "label": "empty workspace", "value": "redacted", "sensitive": False}],
    "positive_evidence": [],
    "negative_controls": ["no owned object family available"],
    "redactions": ["alias redacted"],
    "candidate_signals": [],
    "blocked_states": ["needs_second_account", "needs_owned_object"],
    "next_learning_seed": "prefer lanes with A/B account and owned object controls",
    "updated_at": "2026-05-26"
}
write("surface_evidence.json", evidence)
candidate_evidence = dict(evidence)
candidate_evidence["status"] = "candidate"
write("candidate_evidence.json", candidate_evidence)
report_ready_evidence = dict(evidence)
report_ready_evidence["status"] = "report_ready"
write("report_ready_evidence.json", report_ready_evidence)
PY

python "$ROOT/scripts/attack-path-role-synthesize.py" synthesize --candidate-packet "$WORK/candidate.json" --role-artifact "$WORK/planner.json" --role-artifact "$WORK/critic_pass.json" --out "$WORK/synthesis_pass.json" >"$WORK/role_synth_pass.out"
python "$ROOT/scripts/attack-path-role-synthesize.py" validate --input "$WORK/synthesis_pass.json" >"$WORK/role_synth_validate.out"
python "$ROOT/scripts/attack-path-role-synthesize.py" synthesize --candidate-packet "$WORK/candidate.json" --role-artifact "$WORK/planner.json" --role-artifact "$WORK/critic_block.json" --out "$WORK/synthesis_block.json" >"$WORK/role_synth_block.out"
python - "$WORK/synthesis_block.json" <<'PY'
import json, sys
s = json.load(open(sys.argv[1], encoding='utf-8'))
assert s["decision"]["decision"] == "park_preserve", s
assert s["decision"]["learning_seed_if_blocked"] == "required", s
PY
if python "$ROOT/scripts/attack-path-role-synthesize.py" validate --input "$WORK/synthesis_bad.json" --target example.org >"$WORK/role_forbidden.out" 2>&1; then
  echo "expected forbidden target-like arg to fail" >&2
  exit 1
fi
if python "$ROOT/scripts/attack-path-role-synthesize.py" validate --input "$WORK/synthesis_bad.json" --target=example.org >"$WORK/role_forbidden_equals.out" 2>&1; then
  echo "expected forbidden target-like arg=value to fail" >&2
  exit 1
fi
python - "$WORK/role_forbidden.out" "$WORK/role_forbidden_equals.out" <<'PY'
import json, sys
for path in sys.argv[1:]:
    j=json.load(open(path, encoding='utf-8'))
    assert j['exit_code'] == 30, (path, j)
PY

python "$ROOT/scripts/kali-readiness-state.py" validate --input "$WORK/kali_ready.json" >"$WORK/kali_ready.out"
if python "$ROOT/scripts/kali-readiness-state.py" validate --input "$WORK/kali_bad_nat.json" >"$WORK/kali_bad.out"; then
  echo "expected ready+nAT fail semantic error" >&2
  exit 1
fi
python "$ROOT/scripts/kali-readiness-state.py" seed --profile <attacker-vm> --out "$WORK/kali_seed.json" >"$WORK/kali_seed.out"
python "$ROOT/scripts/kali-readiness-state.py" summarize --input "$WORK/kali_seed.json" >"$WORK/kali_seed_summary.out"
if python "$ROOT/scripts/kali-readiness-state.py" summarize --input "$WORK/kali_ready.json" --url https://example.org >"$WORK/kali_forbidden.out" 2>&1; then
  echo "expected kali forbidden target-like arg to fail" >&2
  exit 1
fi
if python "$ROOT/scripts/kali-readiness-state.py" summarize --input "$WORK/kali_ready.json" --host=example.org >"$WORK/kali_forbidden_equals.out" 2>&1; then
  echo "expected kali forbidden target-like arg=value to fail" >&2
  exit 1
fi

python "$ROOT/scripts/no-finding-learning-seed.py" from-evidence --evidence "$WORK/surface_evidence.json" --out "$WORK/learning_seed.json" >"$WORK/learning_seed.out"
python "$ROOT/scripts/no-finding-learning-seed.py" validate --input "$WORK/learning_seed.json" >"$WORK/learning_validate.out"
python "$ROOT/scripts/no-finding-learning-seed.py" summarize --input "$WORK/learning_seed.json" >"$WORK/learning_summary.out"
if python "$ROOT/scripts/no-finding-learning-seed.py" from-evidence --evidence "$WORK/candidate_evidence.json" >"$WORK/learning_candidate_fail.out"; then
  echo "expected candidate evidence to fail no-finding seed" >&2
  exit 1
fi
if python "$ROOT/scripts/no-finding-learning-seed.py" from-evidence --evidence "$WORK/report_ready_evidence.json" >"$WORK/learning_report_ready_fail.out"; then
  echo "expected report_ready evidence to fail no-finding seed" >&2
  exit 1
fi
if python "$ROOT/scripts/no-finding-learning-seed.py" validate --input "$WORK/learning_seed.json" --live >"$WORK/learning_forbidden.out" 2>&1; then
  echo "expected learning forbidden target-like arg to fail" >&2
  exit 1
fi
if python "$ROOT/scripts/no-finding-learning-seed.py" validate --input "$WORK/learning_seed.json" --scope=<program-redacted> >"$WORK/learning_forbidden_equals.out" 2>&1; then
  echo "expected learning forbidden target-like arg=value to fail" >&2
  exit 1
fi
python - "$WORK/learning_seed.json" "$WORK/learning_log.jsonl" <<'PY'
import json, sys
seed = json.load(open(sys.argv[1], encoding='utf-8'))
open(sys.argv[2], 'w', encoding='utf-8').write(json.dumps(seed, separators=(',', ':')) + '\n')
for line in open(sys.argv[2], encoding='utf-8'):
    if line.strip():
        json.loads(line)
PY

echo "agent capability substrate tests passed"
