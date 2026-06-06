#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TMP="$ROOT/.n/tmp/bundle_freshness_delta_test"
rm -rf "$TMP"
mkdir -p "$TMP/bundles" "$TMP/vuln_intel" "$TMP/out"

cat > "$TMP/bundles/verified_lab_flow_modern_api_ssrf_isolated_callback.md" <<'EOF'
# Verified SSRF callback proof

Status: verified_lab_flow
vuln_classes: ssrf, callback
cve_refs: <specific-cve-id>
product_refs: modern_vuln_api
last_verified: 2026-05-23
safe_proof_posture: local_lab_marker_callback_only

Uses a one-shot attacker callback marker in a disposable local lab.
EOF

cat > "$TMP/bundles/valuable_candidate_path_traversal.md" <<'EOF'
# Valuable candidate path traversal

Status: valuable_candidate
vuln_classes: file-read/path-traversal
product_refs: generic web file handlers
last_verified: 2026-05-22
safe_proof_posture: lab_owned_marker_file_only
EOF

cat > "$TMP/bundles/README.md" <<'EOF'
# Ignore me
vuln_classes: ignored
EOF

cat > "$TMP/vuln_intel/vuln_intel_candidates_20260527T010000Z.json" <<'EOF'
[
  {
    "source": "CISA KEV",
    "id": "<specific-cve-id>",
    "published": "2026-05-27",
    "vendor_project": "Example",
    "product": "SSRF Product",
    "title": "Server-side request forgery",
    "summary": "An SSRF issue allows callback style proof.",
    "vuln_classes": ["ssrf"],
    "routing": "local_bootstrap_review",
    "safe_proof_hint": "Use callback only in local lab."
  },
  {
    "source": "NVD recent",
    "id": "<specific-cve-id>",
    "published": "2026-05-27",
    "vendor_project": "Example",
    "product": "Files Product",
    "title": "Path traversal file read",
    "summary": "A path traversal file read issue.",
    "vuln_classes": ["file-read/path-traversal"],
    "routing": "local_bootstrap_review",
    "safe_proof_hint": "Use lab-owned marker."
  },
  {
    "source": "GitHub Advisory",
    "id": "<specific-ghsa-id>",
    "published": "2026-05-27",
    "vendor_project": "Example",
    "product": "Deserializer",
    "title": "Unsafe deserialization",
    "summary": "Unsafe deserialization with marker-only local proof potential.",
    "vuln_classes": ["deserialization"],
    "routing": "local_bootstrap_review",
    "safe_proof_hint": "Bounded marker only."
  },
  {
    "source": "GitHub Advisory",
    "id": "GHSA-live-target-only",
    "published": "2026-05-27",
    "vendor_project": "SaaS",
    "product": "Tenant App",
    "title": "Authorization bypass in tenant workspace",
    "summary": "Workspace authorization bypass needing a real authorized target.",
    "vuln_classes": ["auth/access-control"],
    "routing": "needs_authorized_live_target",
    "safe_proof_hint": "Requires explicit scope."
  },
  {
    "source": "NVD recent",
    "id": "<specific-cve-id>",
    "published": "2026-05-27",
    "vendor_project": "Example",
    "product": "Low Signal",
    "title": "Unclassified issue",
    "summary": "No useful proof class.",
    "vuln_classes": ["unknown/review"],
    "routing": "reference_only_review",
    "safe_proof_hint": "Review manually."
  }
]
EOF

python "$ROOT/tools/bundle_index.py" --bundle-dir "$TMP/bundles" --out "$TMP/out/bundle_index.json"
python - <<'PY' "$TMP/out/bundle_index.json"
import json, sys
items = json.load(open(sys.argv[1], encoding='utf-8'))
assert len(items) == 2, items
by_title = {item['title']: item for item in items}
assert by_title['Verified SSRF callback proof']['maturity'] == 'verified'
assert by_title['Verified SSRF callback proof']['vuln_classes'] == ['ssrf', 'callback']
assert by_title['Verified SSRF callback proof']['cve_refs'] == ['<specific-cve-id>']
assert by_title['Valuable candidate path traversal']['maturity'] == 'candidate'
assert 'README.md' not in '\n'.join(item['path'] for item in items)
PY

python "$ROOT/tools/vuln_intel_to_bundle_index.py" \
  --vuln-intel-dir "$TMP/vuln_intel" \
  --bundle-dir "$TMP/bundles" \
  --out-prefix "$TMP/out/bundle_freshness_delta_20260527T010000Z" \
  --stamp 20260527T010000Z

python - <<'PY' "$TMP/out/bundle_freshness_delta_20260527T010000Z.json" "$TMP/out/bundle_freshness_delta_20260527T010000Z.md"
import json, sys, pathlib
payload = json.load(open(sys.argv[1], encoding='utf-8'))
items = {item['id']: item for item in payload['items']}
assert payload['status'] == 'ok'
assert payload['source_vuln_intel'].endswith('vuln_intel_candidates_20260527T010000Z.json')
assert items['<specific-cve-id>']['classification'] == 'covered_by_existing_bundle'
assert items['<specific-cve-id>']['matched_bundles'][0]['maturity'] == 'verified'
assert items['<specific-cve-id>']['classification'] == 'needs_bundle_update'
assert items['<specific-ghsa-id>']['classification'] == 'new_local_bootstrap_candidate'
assert items['GHSA-live-target-only']['classification'] == 'needs_authorized_live_target'
assert items['<specific-cve-id>']['classification'] == 'reference_only'
assert len(payload['top_recommendations']) <= 3
assert payload['top_recommendations'][0]['classification'] in {'new_local_bootstrap_candidate', 'needs_bundle_update', 'needs_authorized_live_target'}
md = pathlib.Path(sys.argv[2]).read_text(encoding='utf-8')
assert 'Status: metadata-only bundle freshness delta / no target touched' in md
assert 'No scanners, PoCs, browser/noVNC, recon, account actions, or live targets were executed.' in md
assert '<specific-ghsa-id>' in md
PY

set +e
python "$ROOT/tools/vuln_intel_to_bundle_index.py" --target https://example.org > "$TMP/out/forbidden.json" 2>/dev/null
code=$?
set -e
[ "$code" -eq 30 ]
python - <<'PY' "$TMP/out/forbidden.json"
import json, sys
payload = json.load(open(sys.argv[1], encoding='utf-8'))
assert payload['status'] == 'error'
assert payload['error'] == 'target_like_argument_rejected'
assert payload['target_touching'] is False
PY

python "$ROOT/tools/vuln_to_proof_loop.py" \
  --delta-json "$TMP/out/bundle_freshness_delta_20260527T010000Z.json" \
  --out-dir "$TMP/out/proof_loop" \
  --stamp 20260527T010000Z

python - <<'PY' "$TMP/out/proof_loop/proof_loop_20260527T010000Z.json" "$TMP/out/proof_loop/proof_loop_20260527T010000Z.md"
import json, sys, pathlib
payload = json.load(open(sys.argv[1], encoding='utf-8'))
stages = payload['stages']
assert payload['status'] == 'ok'
assert payload['target_touching'] is False
assert stages['latest_vulnerability_intake']['status'] == 'consumed_existing_delta'
assert stages['local_target_test']['status'] == 'run_card_only_operator_gate'
assert stages['proof_pattern_library']['status'] == 'draft_only_until_local_proof_verified'
assert stages['live_target_selection']['status'] == 'prerequisite_mapping_only_no_live_touch'
assert payload['selected_candidate']['classification'] == 'new_local_bootstrap_candidate'
run_card = pathlib.Path(payload['artifacts']['local_run_card'])
draft = pathlib.Path(payload['artifacts']['proof_pattern_draft'])
assert run_card.exists(), run_card
assert draft.exists(), draft
assert 'Do not run against live targets' in run_card.read_text(encoding='utf-8')
assert 'Status: draft / not verified / do not add to proof library yet' in draft.read_text(encoding='utf-8')
md = pathlib.Path(sys.argv[2]).read_text(encoding='utf-8')
assert 'latest漏洞 -> local靶機 run-card -> proof pattern draft -> live-target prerequisites' in md
assert 'No local lab, scanner, PoC, browser/noVNC, account, or live target was executed.' in md
PY

echo "PASS test_bundle_freshness_delta"
