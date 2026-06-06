#!/usr/bin/env python3
"""Shared helpers for mature-tool local-lab wrappers.

These generators create approval-gated bash runners for disposable lab targets.
Outputs are candidate-only observations; scanner/tool output never becomes a
confirmed finding.
"""
from __future__ import annotations

import argparse
import ipaddress
import json
import os
import shlex
import sys
from pathlib import Path
from urllib.parse import urlparse


def is_private_lab_url(target: str) -> bool:
    parsed = urlparse(target)
    if parsed.scheme not in {"http", "https"} or not parsed.hostname:
        return False
    host = parsed.hostname.lower()
    if host in {"localhost"} or host.endswith(".local"):
        return True
    try:
        ip = ipaddress.ip_address(host)
    except ValueError:
        return False
    return ip.is_private or ip.is_loopback


def normalize_target(target: str) -> str:
    return target.rstrip("/") + "/"


def parsed_target_bits(target: str) -> dict:
    parsed = urlparse(normalize_target(target))
    port = parsed.port or (443 if parsed.scheme == "https" else 80)
    return {"scheme": parsed.scheme, "host": parsed.hostname or "", "port": port}


def build_plan(args: argparse.Namespace, spec: dict) -> dict:
    target = normalize_target(args.target)
    return {
        "schema": f"{spec['slug']}_tool_wrapper_plan/0.1",
        "mode": "runnable-script" if args.lab_approved else "plan-only",
        "target": target,
        "target_bits": parsed_target_bits(target),
        "output_dir": args.output_dir,
        "tool_timeout_seconds": args.tool_timeout,
        "health_timeout_seconds": args.health_timeout,
        "semantics": "candidate-only",
        "module_granularity": "one-vulnerability-one-module",
        "owasp_classes": spec["owasp_classes"],
        "release_mapping": spec["release_mapping"],
        "risk_lane": spec["risk_lane"],
        "tool": spec["tool"],
        "oss_recon_decision": spec["oss_recon_decision"],
        "possible_vulnerability_summary": {
            "possible_manual_review_candidates": spec["candidate_signals"],
            "non_findings_or_controls": spec["control_signals"],
            "missing_evidence_to_confirm": spec["missing_evidence_to_confirm"],
        },
        "lab_tooling_authorization": {
            "scope": "authorized disposable local lab only",
            "broad_tool_category_ban": False,
            "scanner_output_semantics": "candidate-only",
            "nat_policy": "NAT allowed only for download/update, then return to host-only execution when feasible",
        },
        "disallowed": [
            "public/third-party targets without separate scope rules",
            "credential theft",
            "real exfiltration or loot retention",
            "uncontrolled propagation",
            "automatic confirmed-finding promotion",
            "report submission",
        ],
    }


def _render_parser_py(spec: dict) -> str:
    signals = json.dumps(spec["parser_signals"], sort_keys=True)
    return f"""import json, pathlib, re, sys, xml.etree.ElementTree as ET
outdir = pathlib.Path(sys.argv[1])
module = {spec['slug']!r}
owasp_class = {spec['owasp_classes'][0]!r}
tool_name = {spec['tool']['name']!r}
signals = {signals}
rows = []

def add(path, status, signal, title='', detail='', source='tool'):
    rows.append({{
        'schema': 'tool_wrapper_lab_observation/0.1',
        'module': module,
        'class': owasp_class,
        'tool': tool_name,
        'path': path,
        'status': status,
        'signal': signal,
        'title': title[:160],
        'detail': detail[:240],
        'source': source,
        'semantics': 'candidate-only',
    }})

raw_text = ''
raw_json = outdir / 'tool_raw.json'
raw_txt = outdir / 'tool_raw.txt'
raw_xml = outdir / 'tool_raw.xml'
if raw_json.exists():
    raw_text = raw_json.read_text(encoding='utf-8', errors='ignore')
elif raw_txt.exists():
    raw_text = raw_txt.read_text(encoding='utf-8', errors='ignore')
elif raw_xml.exists():
    raw_text = raw_xml.read_text(encoding='utf-8', errors='ignore')

if tool_name == 'ffuf':
    try:
        data = json.loads(raw_text or '{{}}')
    except json.JSONDecodeError:
        data = {{}}
    results = data.get('results') or []
    lengths = [int(r.get('length') or 0) for r in results]
    default_len = max(set(lengths), key=lengths.count) if lengths else None
    for r in results:
        path = '/' + str(r.get('input', {{}}).get('FUZZ', '')).lstrip('/')
        status = int(r.get('status') or 0)
        words = int(r.get('words') or 0)
        length = int(r.get('length') or 0)
        is_default_spa = status == 200 and default_len is not None and length == default_len and lengths.count(default_len) > 1
        if status in {{200, 204, 301, 302, 307, 308, 401, 403}} and not is_default_spa:
            add(path, status, signals['candidate'], detail=f'ffuf discovered non-default path; words={{words}} length={{length}}')
        elif status in {{200, 204, 301, 302, 307, 308, 401, 403}}:
            add(path, status, signals['control'], title='likely SPA/default fallback suppressed', detail=f'ffuf repeated default length; words={{words}} length={{length}}')
    if not results:
        add('/', 0, signals['control'], title='ffuf completed with no parsed discoveries')
elif tool_name == 'nikto':
    # Nikto JSON varies by distro/version. Keep parser tolerant and fall back to text regex.
    parsed = False
    try:
        data = json.loads(raw_text or '{{}}')
        vulns = []
        if isinstance(data, dict):
            for key in ('vulnerabilities', 'items'):
                if isinstance(data.get(key), list):
                    vulns.extend(data[key])
            for host in data.get('host', []) if isinstance(data.get('host'), list) else []:
                if isinstance(host, dict) and isinstance(host.get('vulnerabilities'), list):
                    vulns.extend(host['vulnerabilities'])
        for v in vulns:
            if isinstance(v, dict):
                msg = str(v.get('msg') or v.get('message') or v.get('description') or v)
                uri = str(v.get('url') or v.get('uri') or '/')
                add(uri, 0, signals['candidate'], title='nikto server misconfiguration lead', detail=msg)
                parsed = True
    except Exception:
        pass
    if not parsed:
        for line in raw_text.splitlines():
            clean = line.strip('+ ').strip()
            lower = clean.lower()
            has_plugin_id = bool(re.search(r'\[[0-9]{{6}}\]', clean))
            is_metadata = lower.startswith(('target ip:', 'target hostname:', 'target port:', 'platform:', 'start time:', 'end time:', '1 host(s) tested', 'scan terminated:'))
            if clean and ('+ ' in line or line.startswith('+')):
                if has_plugin_id:
                    add('/', 0, signals['candidate'], title='nikto observation', detail=clean)
                elif not is_metadata:
                    add('/', 0, signals['control'], title='nikto informational output', detail=clean)
                parsed = True
        if not parsed:
            add('/', 0, signals['control'], title='nikto completed with no parsed observations')
elif tool_name == 'nmap':
    parsed = False
    if raw_xml.exists():
        try:
            root = ET.fromstring(raw_xml.read_text(encoding='utf-8', errors='ignore'))
            for port in root.findall('.//port'):
                state = port.find('state')
                state_text = state.get('state') if state is not None else ''
                service = port.find('service')
                product = service.get('product') if service is not None else ''
                version = service.get('version') if service is not None else ''
                portid = port.get('portid') or ''
                add(f':{{portid}}', 0, signals['control'], title=f'nmap service {{state_text}}', detail=f'{{product}} {{version}}'.strip())
                parsed = True
                for script in port.findall('script'):
                    sid = script.get('id') or ''
                    output = script.get('output') or ''
                    sig = signals['candidate'] if any(x in output.lower() for x in ['express', 'x-powered-by', 'server:', 'set-cookie']) else signals['control']
                    add(f':{{portid}}', 0, sig, title=f'nmap {{sid}}', detail=output)
                    parsed = True
        except Exception as exc:
            add('/', 0, signals['control'], title='nmap XML parse error', detail=str(exc))
            parsed = True
    if not parsed:
        add('/', 0, signals['control'], title='nmap completed with no parsed observations')

with open(outdir / 'observations.jsonl', 'w', encoding='utf-8') as f:
    for row in rows:
        f.write(json.dumps(row, sort_keys=True) + '\\n')

candidates = [r for r in rows if str(r.get('signal','')).endswith('_candidate')]
controls = [r for r in rows if r not in candidates]
with open(outdir / 'possible_vulnerabilities.md', 'w', encoding='utf-8') as f:
    f.write('# Possible vulnerabilities\\n\\n')
    f.write('Status: candidate-only / needs_manual_review\\n\\n')
    f.write('## possible_manual_review_candidates\\n\\n')
    if candidates:
        for r in candidates:
            f.write(f"- {{r['tool']}} {{r['path']}} -> signal `{{r['signal']}}`, title `{{r.get('title','')}}`, detail `{{r.get('detail','')}}`\\n")
    else:
        f.write('- None from this tool run.\\n')
    f.write('\\n## non_findings_or_controls\\n\\n')
    if controls:
        for r in controls:
            f.write(f"- {{r['tool']}} {{r['path']}} -> signal `{{r['signal']}}`, title `{{r.get('title','')}}`\\n")
    else:
        f.write('- None recorded.\\n')
    f.write('\\n## missing_evidence_to_confirm\\n\\n')
    f.write('- Manual review of tool output against intended lab app behavior.\\n')
    f.write('- Redacted reproduction/evidence packet.\\n')
    f.write('- Impact analysis beyond scanner/tool wording.\\n')
    f.write('- Report-readiness gate before any confirmed/reportable/submission language.\\n')
"""


def render_tool_command(spec: dict, plan: dict) -> str:
    target = shlex.quote(plan["target"].rstrip("/"))
    tool_timeout = int(plan["tool_timeout_seconds"])
    bits = plan["target_bits"]
    host = shlex.quote(bits["host"])
    port = shlex.quote(str(bits["port"]))
    name = spec["tool"]["name"]
    if name == "ffuf":
        words = " ".join(shlex.quote(w) for w in spec["wordlist"])
        return f"""printf '%s\\n' {words} > \"$outdir/wordlist.txt\"
if command -v ffuf >/dev/null 2>&1; then
  timeout {tool_timeout}s ffuf -u \"$target/FUZZ\" -w \"$outdir/wordlist.txt\" -of json -o \"$outdir/tool_raw.json\" -t 5 -rate 25 -maxtime {tool_timeout} -noninteractive >/dev/null 2>\"$outdir/tool_stderr.txt\" || true
else
  printf 'missing tool: ffuf\\n' > \"$outdir/tool_stderr.txt\"
  printf '{{"results":[]}}' > \"$outdir/tool_raw.json\"
fi"""
    if name == "nikto":
        return f"""if command -v nikto >/dev/null 2>&1; then
  timeout {tool_timeout}s nikto -h \"$target\" -nointeractive -maxtime 30s -Format json -output \"$outdir/tool_raw.json\" >\"$outdir/tool_stdout.txt\" 2>\"$outdir/tool_stderr.txt\" || true
  [ -s \"$outdir/tool_raw.json\" ] || cp \"$outdir/tool_stdout.txt\" \"$outdir/tool_raw.txt\"
else
  printf 'missing tool: nikto\\n' > \"$outdir/tool_stderr.txt\"
  : > \"$outdir/tool_raw.txt\"
fi"""
    if name == "nmap":
        return f"""if command -v nmap >/dev/null 2>&1; then
  timeout {tool_timeout}s nmap -Pn -n -p {port} --script http-title,http-headers -oX \"$outdir/tool_raw.xml\" {host} >\"$outdir/tool_stdout.txt\" 2>\"$outdir/tool_stderr.txt\" || true
else
  printf 'missing tool: nmap\\n' > \"$outdir/tool_stderr.txt\"
  : > \"$outdir/tool_raw.xml\"
fi"""
    raise ValueError(f"unsupported tool: {name}")


def render_bash(plan: dict, spec: dict) -> str:
    target = plan["target"].rstrip("/")
    outdir = plan["output_dir"]
    health_timeout = int(plan["health_timeout_seconds"])
    command = render_tool_command(spec, plan)
    parser = _render_parser_py(spec)
    slug = spec["slug"]
    tool = spec["tool"]["name"]
    return f'''#!/usr/bin/env bash
set -euo pipefail
target={shlex.quote(target)}
outdir={shlex.quote(outdir)}
health_timeout={health_timeout}
module_slug={shlex.quote(slug)}
tool_name={shlex.quote(tool)}
mkdir -p "$outdir"
: > "$outdir/observations.jsonl"
: > "$outdir/possible_vulnerabilities.md"

health() {{
  # emits pre_health/post_health lines into health.txt
  local label="$1"
  local code
  code=$(curl -k -sS -o /dev/null -w '%{{http_code}}' --max-time "$health_timeout" "$target/" || true)
  printf '%s_health=%s\n' "$label" "$code" >> "$outdir/health.txt"
}}

health pre
{command}
python3 - "$outdir" <<'PY'
{parser}
PY
# brief cooldown before post-health; scanners can leave the lab service busy for a moment
sleep 5
health post
printf 'target=%s\nmodule=%s\ntool=%s\nsemantics=candidate-only\n' "$target" "$module_slug" "$tool_name" > "$outdir/summary.txt"
printf 'observations.jsonl\npossible_vulnerabilities.md\nhealth.txt\nsummary.txt\ntool_stdout.txt\ntool_stderr.txt\ntool_raw.json\ntool_raw.txt\ntool_raw.xml\n' > "$outdir/artifact_manifest.txt"
# Raw tool outputs are retained only as local lab artifacts; no raw response bodies or secrets are intentionally collected.
'''


def main_for_spec(spec: dict, argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=f"Generate {spec['tool']['name']} local-lab wrapper for {spec['slug']}")
    parser.add_argument("--target", required=True)
    parser.add_argument("--output-dir", default=f"/tmp/{spec['slug']}")
    parser.add_argument("--out-script", default=f"setting/local/{spec['slug']}_run.sh")
    parser.add_argument("--tool-timeout", type=int, default=90)
    parser.add_argument("--health-timeout", type=int, default=5)
    parser.add_argument("--lab-approved", action="store_true")
    args = parser.parse_args(argv)

    if not is_private_lab_url(args.target):
        print("public targets are not allowed for this local-lab adapter", file=sys.stderr)
        return 2
    if args.tool_timeout < 10 or args.tool_timeout > 300:
        print("tool timeout must be between 10 and 300 seconds", file=sys.stderr)
        return 2
    if args.health_timeout < 1 or args.health_timeout > 15:
        print("health timeout must be between 1 and 15 seconds", file=sys.stderr)
        return 2

    plan = build_plan(args, spec)
    if not args.lab_approved:
        print(json.dumps(plan, indent=2, sort_keys=True))
        return 0

    out_path = Path(args.out_script)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(render_bash(plan, spec), encoding="utf-8", newline="\n")
    try:
        os.chmod(out_path, 0o755)
    except OSError:
        pass
    print(json.dumps({"status": "script_written", "path": str(out_path), "plan": plan}, indent=2, sort_keys=True))
    return 0
