#!/usr/bin/env python3
"""Shared helpers for bounded single-vulnerability OWASP lab modules."""
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


def build_plan(args: argparse.Namespace, spec: dict) -> dict:
    return {
        "schema": f"{spec['slug']}_plan/0.1",
        "mode": "runnable-script" if args.lab_approved else "plan-only",
        "target": normalize_target(args.target),
        "output_dir": args.output_dir,
        "request_cap": args.request_cap,
        "planned_requests_including_health": len(spec["probes"]) + 2,
        "timeout_seconds": args.timeout,
        "rate_limit_note": "sequential curl requests only; fixed path list; no scanner/crawler/fuzzer",
        "semantics": "candidate-only",
        "module_granularity": "one-vulnerability-one-module",
        "owasp_classes": spec["owasp_classes"],
        "release_mapping": spec["release_mapping"],
        "risk_lane": spec["risk_lane"],
        "oss_recon_decision": spec["oss_recon_decision"],
        "probes": [{"path": p["path"], "purpose": p["purpose"]} for p in spec["probes"]],
        "possible_vulnerability_summary": {
            "possible_manual_review_candidates": spec["candidate_signals"],
            "non_findings_or_controls": spec["control_signals"],
            "missing_evidence_to_confirm": spec["missing_evidence_to_confirm"],
        },
        "disallowed": [
            "public targets",
            "credential theft",
            "brute force",
            "callbacks/OAST",
            "crawler/scanner broad run",
            "raw secret/loot retention",
            "status promotion",
            "report submission",
        ],
    }


def _bash_case_lines(spec: dict) -> str:
    return "\n".join(
        f"    {shlex.quote(probe['path'])}) signal={shlex.quote(probe['signal'])} ;;"
        for probe in spec["probes"]
    )


def _probe_lines(spec: dict) -> str:
    return "\n".join(
        f"probe {shlex.quote(p['path'])} {shlex.quote(p['purpose'])}" for p in spec["probes"]
    )


def render_bash(plan: dict, spec: dict) -> str:
    target = plan["target"].rstrip("/")
    outdir = plan["output_dir"]
    request_cap = int(plan["request_cap"])
    timeout = int(plan["timeout_seconds"])
    case_lines = _bash_case_lines(spec)
    probe_lines = _probe_lines(spec)
    class_name = spec["owasp_classes"][0]
    slug = spec["slug"]
    return rf'''#!/usr/bin/env bash
set -euo pipefail

target={shlex.quote(target)}
outdir={shlex.quote(outdir)}
timeout={timeout}
request_cap={request_cap}
requests_sent=0
module_slug={shlex.quote(slug)}
owasp_class={shlex.quote(class_name)}
mkdir -p "$outdir"
: > "$outdir/observations.jsonl"
: > "$outdir/possible_vulnerabilities.md"

health() {{
  # writes pre_health/post_health lines to health.txt
  local label="$1"
  local code
  code=$(curl -k -sS -o /dev/null -w '%{{http_code}}' --max-time "$timeout" "$target/" || true)
  printf '%s_health=%s\n' "$label" "$code" >> "$outdir/health.txt"
}}

json_escape() {{ python3 -c 'import json,sys; print(json.dumps(sys.stdin.read())[1:-1])'; }}

probe() {{
  local path="$1"
  local purpose="$2"
  if [ "$requests_sent" -ge "$request_cap" ]; then
    printf 'request cap reached before %s\n' "$path" >> "$outdir/summary.txt"
    return 0
  fi
  requests_sent=$((requests_sent + 1))
  local url="$target$path"
  local hdr body code ctype loc title body_hash set_cookie signal
  hdr="$outdir/headers_${{requests_sent}}.tmp"
  body="$outdir/body_${{requests_sent}}.tmp"
  code=$(curl -k -sS -D "$hdr" -o "$body" -w '%{{http_code}}' --max-time "$timeout" "$url" || true)
  [ -f "$hdr" ] || : > "$hdr"
  [ -f "$body" ] || : > "$body"
  ctype=$(grep -i '^content-type:' "$hdr" | head -n1 | tr -d '\r' | cut -d' ' -f2- || true)
  loc=$(grep -i '^location:' "$hdr" | head -n1 | tr -d '\r' | cut -d' ' -f2- || true)
  set_cookie=$(grep -i '^set-cookie:' "$hdr" | sed -E 's/=[^;]*/=<redacted>/g' | tr -d '\r' | paste -sd '|' - || true)
  title=$(python3 - "$body" <<'PY' || true
import re, sys
p=sys.argv[1]
data=open(p,'rb').read(4096).decode('utf-8','ignore')
m=re.search(r'<title[^>]*>(.*?)</title>', data, re.I|re.S)
print(re.sub(r'\\s+',' ',m.group(1)).strip()[:120] if m else '')
PY
)
  body_hash=$(python3 - "$body" <<'PY'
import hashlib, sys
print(hashlib.sha256(open(sys.argv[1],'rb').read()).hexdigest())
PY
)
  signal="observation"
  case "$path" in
{case_lines}
  esac
  rm -f "$body"
  printf '{{"schema":"single_vuln_lab_observation/0.1","module":"%s","class":"%s","path":"%s","purpose":"%s","status":%s,"content_type":"%s","location":"%s","title":"%s","set_cookie_metadata":"%s","body_sha256":"%s","signal":"%s","semantics":"candidate-only"}}\n' \
    "$module_slug" \
    "$(printf '%s' "$owasp_class" | json_escape)" \
    "$(printf '%s' "$path" | json_escape)" \
    "$(printf '%s' "$purpose" | json_escape)" \
    "${{code:-0}}" \
    "$(printf '%s' "$ctype" | json_escape)" \
    "$(printf '%s' "$loc" | json_escape)" \
    "$(printf '%s' "$title" | json_escape)" \
    "$(printf '%s' "$set_cookie" | json_escape)" \
    "$body_hash" \
    "$signal" >> "$outdir/observations.jsonl"
}}

write_possible_vulnerabilities() {{
  python3 - "$outdir/observations.jsonl" "$outdir/possible_vulnerabilities.md" <<'PY'
import json, sys
obs_path, out_path = sys.argv[1], sys.argv[2]
rows=[]
for line in open(obs_path, encoding='utf-8'):
    if line.strip(): rows.append(json.loads(line))
candidates=[r for r in rows if r.get('signal','').endswith('_candidate')]
controls=[r for r in rows if r.get('signal','') and not r.get('signal','').endswith('_candidate')]
with open(out_path,'w',encoding='utf-8') as f:
    f.write('# Possible vulnerabilities\n\n')
    f.write('Status: candidate-only / needs_manual_review\n\n')
    f.write('## possible_manual_review_candidates\n\n')
    if candidates:
        for r in candidates:
            f.write(f"- {{r['class']}} {{r['path']}} -> status {{r['status']}}, signal `{{r['signal']}}`, title `{{r.get('title','')}}`\n")
    else:
        f.write('- None from this bounded run.\n')
    f.write('\n## non_findings_or_controls\n\n')
    if controls:
        for r in controls:
            f.write(f"- {{r['path']}} -> status {{r['status']}}, signal `{{r['signal']}}`\n")
    else:
        f.write('- None recorded.\n')
    f.write('\n## missing_evidence_to_confirm\n\n')
    f.write('- Intent/publicness check for each endpoint.\n')
    f.write('- Authenticated versus unauthenticated comparison where applicable.\n')
    f.write('- Redacted evidence packet and manual impact analysis.\n')
    f.write('- Report-readiness gate result before any finding/submission language.\n')
PY
}}

health pre
{probe_lines}
health post
write_possible_vulnerabilities
printf 'requests_sent=%s\n' "$requests_sent" >> "$outdir/health.txt"
printf 'target=%s\nmodule=%s\nrequests_sent=%s\nsemantics=candidate-only\n' "$target" "$module_slug" "$requests_sent" > "$outdir/summary.txt"
printf 'observations.jsonl\npossible_vulnerabilities.md\nhealth.txt\nsummary.txt\n' > "$outdir/artifact_manifest.txt"
find "$outdir" -name '*.tmp' -delete
'''


def main_for_spec(spec: dict, argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=f"Generate bounded {spec['slug']} local-lab probe")
    parser.add_argument("--target", required=True)
    parser.add_argument("--output-dir", default=f"/tmp/{spec['slug']}")
    parser.add_argument("--out-script", default=f"setting/local/{spec['slug']}_run.sh")
    parser.add_argument("--request-cap", type=int, default=max(6, len(spec["probes"]) + 3))
    parser.add_argument("--timeout", type=int, default=5)
    parser.add_argument("--lab-approved", action="store_true")
    args = parser.parse_args(argv)

    if not is_private_lab_url(args.target):
        print("public targets are not allowed for this local-lab adapter", file=sys.stderr)
        return 2
    min_cap = len(spec["probes"]) + 2
    if args.request_cap < min_cap or args.request_cap > 30:
        print(f"request cap must be between {min_cap} and 30", file=sys.stderr)
        return 2
    if args.timeout < 1 or args.timeout > 10:
        print("timeout must be between 1 and 10 seconds", file=sys.stderr)
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
