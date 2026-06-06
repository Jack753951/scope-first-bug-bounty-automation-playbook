#!/usr/bin/env python3
"""Generate a bounded three-class OWASP local-lab probe.

Classes covered in this first trial:
- A01:2021 Broken Access Control: unauthenticated fixed-route access metadata.
- A02:2021 Cryptographic Failures: HTTP/cookie/security metadata only.
- A10:2025 Mishandling of Exceptional Conditions: benign malformed/unknown route responses.

The generator never executes target requests. It writes a runnable bash script only
when --lab-approved is supplied.
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

WAVES = [
    {
        "owasp_class": "A01:2021 Broken Access Control",
        "release_mapping": ["A05:2017 Broken Access Control", "A01:2025 Broken Access Control"],
        "risk_lane": "active bounded metadata",
        "paths": [
            "/rest/admin/application-configuration",
            "/api/Users",
            "/rest/user/whoami",
            "/administration",
        ],
        "signals": ["unauthenticated_200_candidate", "redirect_or_auth_gate_observed", "spa_fallback_control"],
    },
    {
        "owasp_class": "A02:2021 Cryptographic Failures",
        "release_mapping": ["A03:2017 Sensitive Data Exposure", "A04:2025 Cryptographic Failures"],
        "risk_lane": "metadata only",
        "paths": ["/", "/rest/user/whoami", "/api/SecurityQuestions"],
        "signals": ["set_cookie_flag_metadata", "transport_scheme_metadata", "sensitive_metadata_exposure_candidate"],
    },
    {
        "owasp_class": "A10:2025 Mishandling of Exceptional Conditions",
        "release_mapping": ["A05:2021 Security Misconfiguration", "A09:2021 Security Logging and Monitoring Failures"],
        "risk_lane": "benign malformed input metadata",
        "paths": [
            "/rest/products/search?q=%25",
            "/rest/products/search?q=%F0%9F%92%A9",
            "/rest/does-not-exist",
        ],
        "signals": ["server_error_candidate", "verbose_error_metadata", "stable_error_handling_observed"],
    },
]

OSS_RECON_DECISIONS = {
    "A01:2021 Broken Access Control": {
        "tools_checked": ["OWASP ZAP", "Autorize", "AuthMatrix"],
        "decision": "write-custom",
        "reason": "Mature tools exist, but available authz tools expect Burp/session workflows and credentials; ZAP is broad and not installed locally. For this first lab wave, a fixed unauthenticated route metadata adapter is safer and candidate-only.",
    },
    "A02:2021 Cryptographic Failures": {
        "tools_checked": ["testssl.sh", "SSLyze", "Mozilla HTTP Observatory"],
        "decision": "write-custom",
        "reason": "Mature TLS/HTTP observability tools exist, but the current Juice Shop lab target is plain HTTP on a host-only network and the tools are not installed on the host. First wave records transport/cookie metadata only.",
    },
    "A10:2025 Mishandling of Exceptional Conditions": {
        "tools_checked": ["OWASP ZAP", "ffuf", "nuclei templates"],
        "decision": "write-custom",
        "reason": "Broad fuzzing/scanning tools exist, but this wave needs only three fixed benign error-handling probes with no crawler/fuzzer behavior and candidate-only JSONL output.",
    },
}


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


def build_plan(args: argparse.Namespace) -> dict:
    target = normalize_target(args.target)
    planned_requests = sum(len(w["paths"]) for w in WAVES) + 2
    return {
        "schema": "owasp_three_class_probe_plan/0.1",
        "mode": "runnable-script" if args.lab_approved else "plan-only",
        "target": target,
        "output_dir": args.output_dir,
        "request_cap": args.request_cap,
        "planned_requests_including_health": planned_requests,
        "timeout_seconds": args.timeout,
        "rate_limit_note": "sequential curl requests; no scanner/crawler/fuzzer",
        "semantics": "candidate-only",
        "oss_recon_decisions": OSS_RECON_DECISIONS,
        "waves": WAVES,
        "disallowed": [
            "public targets",
            "credential theft",
            "brute force",
            "callbacks/OAST",
            "crawler/scanner broad run",
            "raw body retention",
            "confirmed finding promotion",
        ],
    }


def render_bash(plan: dict) -> str:
    target = plan["target"].rstrip("/")
    outdir = plan["output_dir"]
    request_cap = plan["request_cap"]
    timeout = plan["timeout_seconds"]
    probe_lines = []
    for wave in WAVES:
        cls = wave["owasp_class"]
        for path in wave["paths"]:
            probe_lines.append(f"probe {shlex.quote(cls)} {shlex.quote(path)}")
    probes = "\n".join(probe_lines)
    return f'''#!/usr/bin/env bash
set -euo pipefail

target={shlex.quote(target)}
outdir={shlex.quote(outdir)}
timeout={int(timeout)}
request_cap={int(request_cap)}
requests_sent=0
mkdir -p "$outdir"
: > "$outdir/observations.jsonl"

health() {{
  local label="$1"
  local code
  code=$(curl -k -sS -o /dev/null -w '%{{http_code}}' --max-time "$timeout" "$target/" || true)
  printf '%s_health=%s\n' "$label" "$code" >> "$outdir/health.txt"
}}

json_escape() {{ python3 -c 'import json,sys; print(json.dumps(sys.stdin.read())[1:-1])'; }}

probe() {{
  local cls="$1"
  local path="$2"
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
  case "$cls|$code|$path" in
    *"Broken Access Control"*"|200|/administration") signal="spa_fallback_control" ;;
    *"Broken Access Control"*"|200|/rest/user/whoami") signal="unauth_identity_metadata" ;;
    *"Broken Access Control"*"|200|"*) signal="unauthenticated_200_candidate" ;;
    *"Exceptional"*"|500|"*) signal="server_error_candidate" ;;
    *"Cryptographic"*) signal="crypto_transport_cookie_metadata" ;;
  esac
  rm -f "$body"
  printf '{{"schema":"owasp_three_class_observation/0.1","class":"%s","path":"%s","status":%s,"content_type":"%s","location":"%s","title":"%s","set_cookie_metadata":"%s","body_sha256":"%s","signal":"%s","semantics":"candidate-only"}}\n' \
    "$(printf '%s' "$cls" | json_escape)" \
    "$(printf '%s' "$path" | json_escape)" \
    "${{code:-0}}" \
    "$(printf '%s' "$ctype" | json_escape)" \
    "$(printf '%s' "$loc" | json_escape)" \
    "$(printf '%s' "$title" | json_escape)" \
    "$(printf '%s' "$set_cookie" | json_escape)" \
    "$body_hash" \
    "$signal" >> "$outdir/observations.jsonl"
}}

health pre
{probes}
health post
printf 'requests_sent=%s\n' "$requests_sent" >> "$outdir/health.txt"
printf 'target=%s\nrequests_sent=%s\nsemantics=candidate-only\n' "$target" "$requests_sent" > "$outdir/summary.txt"
printf 'observations.jsonl\nhealth.txt\nsummary.txt\n' > "$outdir/artifact_manifest.txt"
find "$outdir" -name '*.tmp' -delete
'''


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Generate bounded three-class OWASP local-lab probe")
    parser.add_argument("--target", required=True)
    parser.add_argument("--output-dir", default="/tmp/owasp-three-class-probe")
    parser.add_argument("--out-script", default="setting/local/owasp_three_class_probe_run.sh")
    parser.add_argument("--request-cap", type=int, default=16)
    parser.add_argument("--timeout", type=int, default=5)
    parser.add_argument("--lab-approved", action="store_true")
    args = parser.parse_args(argv)

    if not is_private_lab_url(args.target):
        print("public targets are not allowed for this local-lab adapter", file=sys.stderr)
        return 2
    if args.request_cap < 12 or args.request_cap > 40:
        print("request cap must be between 12 and 40", file=sys.stderr)
        return 2
    if args.timeout < 1 or args.timeout > 10:
        print("timeout must be between 1 and 10 seconds", file=sys.stderr)
        return 2

    plan = build_plan(args)
    if not args.lab_approved:
        print(json.dumps(plan, indent=2, sort_keys=True))
        return 0

    out_path = Path(args.out_script)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(render_bash(plan), encoding="utf-8", newline="\n")
    try:
        os.chmod(out_path, 0o755)
    except OSError:
        pass
    print(json.dumps({"status": "script_written", "path": str(out_path), "plan": plan}, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
