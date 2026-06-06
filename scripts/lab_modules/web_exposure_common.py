#!/usr/bin/env python3
"""Shared generator for bounded local-lab web exposure triage bundles."""
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


def build_plan(config: dict, target: str, output_dir: str, mode: str) -> dict:
    bits = parse_target(target)
    return {
        "schema": "phase4b_web_exposure_plan/0.1",
        "bundle_id": config["bundle_id"],
        "mode": mode,
        "target": bits["base"],
        "target_bits": bits,
        "semantics": "candidate-only",
        "owasp_mapping": config["owasp_mapping"],
        "cve_mapping": config.get("cve_mapping", []),
        "probe_paths": config["probe_paths"],
        "keywords": config["keywords"],
        "candidate_signal": config["candidate_signal"],
        "control_signals": [
            "404/401/403/timeout can be normal controls",
            "HTTP 200 with body identical to application root is generic SPA/router fallback",
            "status-code-only observations are not findings",
        ],
        "disallowed": [
            "public targets without separate written scope/rules",
            "credential attempts or brute force",
            "secret/loot retention or raw sensitive body capture",
            "automatic confirmed finding promotion",
            "report submission",
        ],
        "oss_recon_decision": config["oss_recon_decision"],
        "output_dir": output_dir,
        "missing_evidence_to_confirm": [
            "manual verification that the endpoint belongs to the suspected exposure class",
            "redacted evidence packet",
            "impact analysis beyond scanner wording",
            "version/config/context confirmation from primary sources when relevant",
            "report-readiness gate before confirmed/reportable language",
        ],
    }


def render_runner(config: dict, plan: dict) -> str:
    plan_json = json.dumps(plan, sort_keys=True)
    output_dir = shlex.quote(plan["output_dir"])
    bundle = config["bundle_id"]
    return rf'''#!/usr/bin/env bash
set -euo pipefail
# {bundle}: bounded local-lab web exposure triage
# Semantics: candidate-only / needs_manual_review. No credentials, brute force, loot retention, or finding promotion.

outdir={output_dir}
mkdir -p "$outdir"
: > "$outdir/tool_stderr.txt"
: > "$outdir/tool_stdout.txt"

python - "$outdir" <<'PY'
import hashlib, html, json, re, sys, urllib.error, urllib.parse, urllib.request
from pathlib import Path

outdir = Path(sys.argv[1])
plan = json.loads({plan_json!r})
base = plan['target'].rstrip('/')
bundle = plan['bundle_id']
keywords = [k.lower() for k in plan['keywords']]
max_body = 262144
observations = []
fetch_log = []

def fetch(path):
    if path.startswith('http://') or path.startswith('https://'):
        url = path
    else:
        url = base + ('/' + path.lstrip('/'))
    try:
        req = urllib.request.Request(url, method='GET', headers={{'User-Agent': 'HermesPhase4BLocalLab/1.0'}})
        with urllib.request.urlopen(req, timeout=8) as resp:
            body = resp.read(max_body)
            ctype = resp.headers.get('content-type', '')
            status = int(resp.status)
            loc = resp.headers.get('location', '')
    except urllib.error.HTTPError as e:
        body = e.read(8192)
        status = int(e.code)
        ctype = e.headers.get('content-type', '') if e.headers else ''
        loc = e.headers.get('location', '') if e.headers else ''
    except Exception as e:
        body = b''
        status = 0
        ctype = ''
        loc = ''
        print(f'fetch_error {{url}} {{type(e).__name__}}: {{e}}', file=sys.stderr)
    text = body.decode('utf-8', errors='ignore')
    digest = hashlib.sha256(body).hexdigest()
    fetch_log.append({{'url': url, 'path': urllib.parse.urlparse(url).path or '/', 'status': status, 'content_type': ctype, 'location': loc, 'sha256': digest, 'bytes': len(body)}})
    return url, status, ctype, loc, text, digest, len(body)

def add(path, status, signal, title, detail='', source='bounded_probe'):
    observations.append({{
        'schema': 'phase4b_web_exposure_observation/0.1',
        'bundle_id': bundle,
        'module': bundle,
        'path': path,
        'status': status,
        'signal': signal,
        'title': title[:180],
        'detail': detail[:300],
        'source': source,
        'semantics': 'candidate-only',
    }})

_, root_status, root_ctype, root_loc, root_text, root_hash, root_len = fetch('/')
probe_paths = list(plan['probe_paths'])
if bundle == 'lab_source_map_disclosure_triage':
    for m in re.finditer(r'(?:src|href)=["\']([^"\']+\.js(?:\?[^"\']*)?)["\']', root_text, re.I):
        src = html.unescape(m.group(1))
        parsed = urllib.parse.urljoin(base + '/', src)
        path = urllib.parse.urlparse(parsed).path
        probe_paths.append(path + '.map' if not path.endswith('.map') else path)
        probe_paths.append(path.replace('.js', '.js.map'))
    probe_paths.extend(['/main.js.map', '/runtime.js.map', '/vendor.js.map', '/polyfills.js.map'])

seen = set()
for path in probe_paths:
    if path in seen:
        continue
    seen.add(path)
    url, status, ctype, loc, text, digest, size = fetch(path)
    lower = text[:8192].lower()
    root_fallback = bool(status in {{200, 204, 301, 302, 307, 308}} and digest == root_hash and path != '/')
    kw = [k for k in keywords if k in lower]
    if root_fallback:
        add(path, status, f'{{bundle}}_generic_root_fallback_control', 'path returns same body as application root; likely SPA/router fallback', f'content_type={{ctype}} bytes={{size}}')
    elif status in {{200, 204, 301, 302, 307, 308}} and kw:
        extra = f'keywords={{kw[:5]}} content_type={{ctype}} bytes={{size}}'
        if bundle == 'lab_source_map_disclosure_triage':
            try:
                data = json.loads(text)
                extra += f" sources={{len(data.get('sources', []))}} sourcesContent={{len(data.get('sourcesContent', []) or [])}}"
            except Exception:
                extra += ' sourcemap_parse=failed'
        add(path, status, plan['candidate_signal'], plan['candidate_signal'].replace('_', ' '), extra)
    elif status in {{401, 403}}:
        add(path, status, f'{{bundle}}_access_control_observed', 'endpoint exists but is access-controlled', f'content_type={{ctype}}')
    else:
        add(path, status, f'{{bundle}}_control', 'no actionable candidate from bounded probe', f'content_type={{ctype}} bytes={{size}}')

with open(outdir / 'observations.jsonl', 'w', encoding='utf-8') as f:
    for row in observations:
        f.write(json.dumps(row, sort_keys=True) + '\n')
with open(outdir / 'http_probe_results.jsonl', 'w', encoding='utf-8') as f:
    for row in fetch_log:
        f.write(json.dumps(row, sort_keys=True) + '\n')

candidates = [r for r in observations if r['signal'] == plan['candidate_signal']]
controls = [r for r in observations if r not in candidates]
with open(outdir / 'possible_vulnerabilities.md', 'w', encoding='utf-8') as f:
    f.write(f'# {{bundle}} possible vulnerabilities\n\n')
    f.write('Status: candidate-only / needs_manual_review\n\n')
    f.write('## possible_manual_review_candidates\n\n')
    if candidates:
        for r in candidates:
            f.write(f"- {{r['path']}} status={{r['status']}} signal `{{r['signal']}}`: {{r['detail']}}\n")
    else:
        f.write('- None from this bounded local-lab run.\n')
    f.write('\n## non_findings_or_controls\n\n')
    for r in controls:
        f.write(f"- {{r['path']}} status={{r['status']}} signal `{{r['signal']}}`: {{r['title']}}\n")
    f.write('\n## missing_evidence_to_confirm\n\n')
    for item in plan['missing_evidence_to_confirm']:
        f.write(f'- {{item}}\n')

with open(outdir / 'summary.txt', 'w', encoding='utf-8') as f:
    f.write(f"target={{base}}\n")
    f.write(f"bundle={{bundle}}\n")
    f.write('semantics=candidate-only\n')
    f.write(f"candidates={{len(candidates)}}\n")
with open(outdir / 'artifact_manifest.txt', 'w', encoding='utf-8') as f:
    for name in ['observations.jsonl','http_probe_results.jsonl','possible_vulnerabilities.md','summary.txt','tool_stdout.txt','tool_stderr.txt']:
        p = outdir / name
        f.write(f"{{name}}\t{{p.stat().st_size if p.exists() else 0}}\n")
PY
'''


def main(config: dict) -> int:
    ap = argparse.ArgumentParser(description=config["description"])
    ap.add_argument("--target", required=True)
    ap.add_argument("--lab-approved", action="store_true")
    ap.add_argument("--out-script", default=f"setting/local/{config['bundle_id']}_run.sh")
    ap.add_argument("--output-dir", default=f"/tmp/{config['bundle_id']}")
    args = ap.parse_args()

    try:
        mode = "runnable-script" if args.lab_approved else "plan-only"
        plan = build_plan(config, args.target, args.output_dir, mode)
    except SystemExit as exc:
        print(str(exc), file=sys.stderr)
        return 2

    if not args.lab_approved:
        print(json.dumps(plan, indent=2, sort_keys=True))
        return 0

    out_script = Path(args.out_script)
    out_script.parent.mkdir(parents=True, exist_ok=True)
    out_script.write_text(render_runner(config, plan), encoding="utf-8")
    try:
        os.chmod(out_script, 0o755)
    except OSError:
        pass
    print(json.dumps({"status": "script_written", "path": str(out_script), "plan": plan}, indent=2, sort_keys=True))
    return 0
