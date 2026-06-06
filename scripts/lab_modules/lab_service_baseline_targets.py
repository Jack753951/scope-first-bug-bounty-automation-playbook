#!/usr/bin/env python3
"""Generate a bounded local-lab service baseline scanner runner.

This is a bundle-first adapter for common infrastructure/service surfaces:
Apache, Tomcat, OpenSSL/TLS, HAProxy, Envoy, and Traefik. It is intended for
authorized disposable labs and emits candidate-only observations.
"""
from __future__ import annotations

import argparse
import json
import os
import shlex
import sys
from pathlib import Path

from tool_wrapper_common import is_private_lab_url, normalize_target, parsed_target_bits

SERVICE_TARGETS = {
    "apache": {
        "paths": ["/server-status", "/server-info", "/icons/", "/manual/"],
        "candidate": "Apache httpd status/info/default path is reachable or advertises sensitive metadata",
        "control": "Apache-specific paths are absent, forbidden, or only expose generic web metadata",
    },
    "tomcat": {
        "paths": ["/manager/html", "/host-manager/html", "/docs/", "/examples/"],
        "candidate": "Tomcat manager/default docs/examples surface is reachable or advertises app-server metadata",
        "control": "Tomcat management/default paths are absent, forbidden, or unactionable metadata only",
    },
    "openssl": {
        "paths": [],
        "candidate": "TLS handshake/certificate/protocol metadata needs manual cryptographic review",
        "control": "TLS check unavailable or no actionable TLS candidate from the bounded probe",
    },
    "haproxy": {
        "paths": ["/haproxy?stats", "/haproxy_stats", "/stats", "/;csv"],
        "candidate": "HAProxy stats/status surface appears reachable or leaks proxy metadata",
        "control": "HAProxy stats/status paths are absent, forbidden, or unactionable metadata only",
    },
    "envoy": {
        "paths": [":9901/server_info", ":9901/config_dump", ":9901/stats", "/stats/prometheus"],
        "candidate": "Envoy admin/metrics/config surface appears reachable or leaks service-mesh metadata",
        "control": "Envoy admin/metrics paths are absent, forbidden, or unactionable metadata only",
    },
    "traefik": {
        "paths": ["/dashboard/", "/api/rawdata", "/api/http/routers", "/metrics"],
        "candidate": "Traefik dashboard/API/metrics surface appears reachable or leaks routing metadata",
        "control": "Traefik dashboard/API/metrics paths are absent, forbidden, or unactionable metadata only",
    },
}


def build_plan(args: argparse.Namespace) -> dict:
    target = normalize_target(args.target)
    return {
        "schema": "lab_service_baseline_targets_plan/0.1",
        "bundle_id": "lab_service_baseline_targets",
        "mode": "runnable-script" if args.lab_approved else "plan-only",
        "target": target,
        "target_bits": parsed_target_bits(target),
        "output_dir": args.output_dir,
        "tool_timeout_seconds": args.tool_timeout,
        "health_timeout_seconds": args.health_timeout,
        "semantics": "candidate-only",
        "lane": "local-learning-lab / authorized disposable lab only",
        "service_targets": sorted(SERVICE_TARGETS),
        "service_profiles": SERVICE_TARGETS,
        "owasp_classes": [
            "A05:2021 Security Misconfiguration",
            "A02:2021 Cryptographic Failures",
            "A06:2021 Vulnerable and Outdated Components",
        ],
        "release_mapping": {
            "2017": ["A03:2017 Sensitive Data Exposure", "A06:2017 Security Misconfiguration", "A09:2017 Using Components with Known Vulnerabilities"],
            "2021": ["A02:2021 Cryptographic Failures", "A05:2021 Security Misconfiguration", "A06:2021 Vulnerable and Outdated Components"],
            "2025_migration_track": ["crypto / misconfiguration / supply-chain or outdated component leads"],
        },
        "oss_recon_decision": {
            "decision": "wrap",
            "candidates_considered": ["curl", "nmap http/ssl NSE", "openssl s_client", "testssl.sh", "sslyze", "whatweb", "nikto", "nuclei allowlisted templates"],
            "reason": "Use mature low-impact metadata probes first; keep service-specific results candidate-only and promote later only if stable.",
        },
        "candidate_signals": [
            "reachable status/admin/metrics/default path for Apache, Tomcat, HAProxy, Envoy, or Traefik",
            "TLS/certificate/protocol metadata that needs manual OpenSSL/TLS review",
            "server/proxy/app-server header or route metadata worth manual misconfiguration review",
        ],
        "control_signals": [
            "404/403/401 on management/default paths may be normal control behavior",
            "generic SPA fallback or proxy response is not a finding by itself",
            "service not detected by this bounded baseline is not proof the service is absent",
        ],
        "missing_evidence_to_confirm": [
            "manual verification that the surface belongs to the suspected service",
            "redacted evidence packet and impact analysis",
            "version/outdatedness confirmation from primary sources",
            "report-readiness gate before confirmed/reportable/submission language",
        ],
        "disallowed": [
            "public/third-party targets without separate scope rules",
            "credential attempts or Tomcat manager brute force",
            "config dump retention beyond sanitized local lab artifacts",
            "real exfiltration or loot retention",
            "automatic confirmed-finding promotion",
            "report submission",
        ],
    }


def render_bash(plan: dict) -> str:
    target = plan["target"].rstrip("/")
    outdir = plan["output_dir"]
    bits = plan["target_bits"]
    scheme = bits["scheme"]
    host = bits["host"]
    port = str(bits["port"])
    tool_timeout = int(plan["tool_timeout_seconds"])
    health_timeout = int(plan["health_timeout_seconds"])
    profiles_json = json.dumps(SERVICE_TARGETS, sort_keys=True)
    return rf'''#!/usr/bin/env bash
set -euo pipefail
# lab_service_baseline_targets: Apache, Tomcat, OpenSSL, HAProxy, Envoy, Traefik
# Semantics: candidate-only / needs_manual_review. No credential attempts, brute force, config exfiltration, or finding promotion.
target={shlex.quote(target)}
scheme={shlex.quote(scheme)}
host={shlex.quote(host)}
port={shlex.quote(port)}
outdir={shlex.quote(outdir)}
tool_timeout={tool_timeout}
health_timeout={health_timeout}
mkdir -p "$outdir"
: > "$outdir/observations.jsonl"
: > "$outdir/http_probe_results.tsv"
: > "$outdir/tool_stdout.txt"
: > "$outdir/tool_stderr.txt"
root_hash=$(curl -k -sS --max-time 8 "$target/" 2>>"$outdir/tool_stderr.txt" | sha256sum | awk '{{print $1}}' || true)
printf '%s\n' "$root_hash" > "$outdir/root_body.sha256"

health() {{
  local label="$1"
  local code
  code=$(curl -k -sS -o /dev/null -w '%{{http_code}}' --max-time "$health_timeout" "$target/" || true)
  printf '%s_health=%s\n' "$label" "$code" >> "$outdir/health.txt"
}}

probe_path() {{
  local service="$1"
  local path="$2"
  local url
  if [[ "$path" == :* ]]; then
    url="$scheme://$host$path"
  else
    url="$target$path"
  fi
  local code server ctype location body_hash
  code=$(curl -k -sS -o /dev/null -w '%{{http_code}}' --max-time 8 "$url" 2>>"$outdir/tool_stderr.txt" || true)
  server=$(curl -k -sSI --max-time 8 "$url" 2>>"$outdir/tool_stderr.txt" | tr -d '\r' | awk 'BEGIN{{IGNORECASE=1}} /^server:/{{sub(/^[^:]+:[ ]*/, ""); print; exit}}' || true)
  ctype=$(curl -k -sSI --max-time 8 "$url" 2>>"$outdir/tool_stderr.txt" | tr -d '\r' | awk 'BEGIN{{IGNORECASE=1}} /^content-type:/{{sub(/^[^:]+:[ ]*/, ""); print; exit}}' || true)
  location=$(curl -k -sSI --max-time 8 "$url" 2>>"$outdir/tool_stderr.txt" | tr -d '\r' | awk 'BEGIN{{IGNORECASE=1}} /^location:/{{sub(/^[^:]+:[ ]*/, ""); print; exit}}' || true)
  body_hash=$(curl -k -sS --max-time 8 "$url" 2>>"$outdir/tool_stderr.txt" | sha256sum | awk '{{print $1}}' || true)
  printf '%s\t%s\t%s\t%s\t%s\t%s\t%s\n' "$service" "$path" "$code" "$server" "$ctype" "$location" "$body_hash" >> "$outdir/http_probe_results.tsv"
}}

health pre
# Apache safe metadata/default probes
probe_path apache '/server-status'
probe_path apache '/server-info'
probe_path apache '/icons/'
probe_path apache '/manual/'
# Tomcat safe management/default probes; no credential attempts or brute force
probe_path tomcat '/manager/html'
probe_path tomcat '/host-manager/html'
probe_path tomcat '/docs/'
probe_path tomcat '/examples/'
# HAProxy safe stats/status probes
probe_path haproxy '/haproxy?stats'
probe_path haproxy '/haproxy_stats'
probe_path haproxy '/stats'
probe_path haproxy '/;csv'
# Envoy safe admin/metrics probes; :9901 paths intentionally target common local admin port only inside approved lab
probe_path envoy ':9901/server_info'
probe_path envoy ':9901/config_dump'
probe_path envoy ':9901/stats'
probe_path envoy '/stats/prometheus'
# Traefik safe dashboard/API/metrics probes
probe_path traefik '/dashboard/'
probe_path traefik '/api/rawdata'
probe_path traefik '/api/http/routers'
probe_path traefik '/metrics'

# OpenSSL/TLS bounded metadata. Store handshake summary only; no secrets or keys.
if command -v openssl >/dev/null 2>&1; then
  timeout "$tool_timeout"s openssl s_client -connect "$host:$port" -servername "$host" -showcerts </dev/null >"$outdir/openssl_s_client.txt" 2>>"$outdir/tool_stderr.txt" || true
else
  printf 'missing tool: openssl\n' >>"$outdir/tool_stderr.txt"
  : > "$outdir/openssl_s_client.txt"
fi

if command -v nmap >/dev/null 2>&1; then
  timeout "$tool_timeout"s nmap -Pn -n -p "$port" --script http-title,http-headers,ssl-cert,ssl-enum-ciphers -oX "$outdir/tool_raw.xml" "$host" >>"$outdir/tool_stdout.txt" 2>>"$outdir/tool_stderr.txt" || true
else
  printf 'missing tool: nmap\n' >>"$outdir/tool_stderr.txt"
  : > "$outdir/tool_raw.xml"
fi

python - "$outdir" <<'PY'
import json, pathlib, sys, xml.etree.ElementTree as ET
outdir = pathlib.Path(sys.argv[1])
profiles = {profiles_json!r}
profiles = json.loads(profiles)
rows = []

def add(service, path, status, signal, title='', detail='', source='service_baseline'):
    rows.append({{
        'schema': 'service_baseline_lab_observation/0.1',
        'module': 'lab_service_baseline_targets',
        'bundle_id': 'lab_service_baseline_targets',
        'service': service,
        'path': path,
        'status': status,
        'signal': signal,
        'title': title[:160],
        'detail': detail[:260],
        'source': source,
        'semantics': 'candidate-only',
    }})

results = outdir / 'http_probe_results.tsv'
root_hash = (outdir / 'root_body.sha256').read_text(encoding='utf-8', errors='ignore').strip() if (outdir / 'root_body.sha256').exists() else ''
if results.exists():
    for line in results.read_text(encoding='utf-8', errors='ignore').splitlines():
        parts = line.split('\t')
        if len(parts) < 6:
            continue
        service, path, code, server, ctype, location = parts[:6]
        body_hash = parts[6] if len(parts) > 6 else ''
        try:
            status = int(code or 0)
        except ValueError:
            status = 0
        detail = f'server={{server}} content_type={{ctype}} location={{location}}'.strip()
        candidate_codes = {{200, 204, 301, 302, 307, 308}}
        auth_control_codes = {{401, 403}}
        generic_root_fallback = bool(root_hash and body_hash and body_hash == root_hash and not server and not location and path != '/')
        if status in candidate_codes and generic_root_fallback:
            add(service, path, status, f'{{service}}_generic_root_fallback_control', title='path returns same body as application root; likely generic SPA/router fallback, not service-specific evidence', detail=detail)
        elif status in candidate_codes:
            add(service, path, status, f'{{service}}_service_baseline_candidate', title=profiles[service]['candidate'], detail=detail)
        elif status in auth_control_codes:
            add(service, path, status, f'{{service}}_access_control_observed', title='management/default path not public but surface exists or is gated', detail=detail)
        else:
            add(service, path, status, f'{{service}}_service_baseline_control', title=profiles[service]['control'], detail=detail)

openssl_text = (outdir / 'openssl_s_client.txt').read_text(encoding='utf-8', errors='ignore') if (outdir / 'openssl_s_client.txt').exists() else ''
openssl_failed = 'no peer certificate available' in openssl_text.lower() or 'cipher is (none)' in openssl_text.lower()
if (not openssl_failed) and ('BEGIN CERTIFICATE' in openssl_text or 'SSL-Session:' in openssl_text):
    add('openssl', 'tls-handshake', 0, 'openssl_tls_metadata_candidate', title=profiles['openssl']['candidate'], detail='openssl s_client produced TLS/certificate metadata; manual crypto review required', source='openssl')
else:
    add('openssl', 'tls-handshake', 0, 'openssl_tls_metadata_control', title=profiles['openssl']['control'], detail='TLS handshake unavailable, plaintext service, or no peer certificate from bounded probe', source='openssl')

raw_xml = outdir / 'tool_raw.xml'
if raw_xml.exists() and raw_xml.read_text(encoding='utf-8', errors='ignore').strip():
    try:
        root = ET.fromstring(raw_xml.read_text(encoding='utf-8', errors='ignore'))
        for script in root.findall('.//script'):
            sid = script.get('id') or ''
            output = script.get('output') or ''
            if sid.startswith('ssl-'):
                add('openssl', f'nmap:{{sid}}', 0, 'openssl_nmap_tls_metadata_candidate', title=f'nmap {{sid}} TLS metadata', detail=output, source='nmap')
            elif sid.startswith('http-') and output:
                add('generic-http', f'nmap:{{sid}}', 0, 'http_service_metadata_candidate', title=f'nmap {{sid}} HTTP metadata', detail=output, source='nmap')
    except Exception as exc:
        add('generic-http', 'nmap-xml', 0, 'nmap_parse_control', title='nmap XML parse error', detail=str(exc), source='nmap')

with open(outdir / 'observations.jsonl', 'w', encoding='utf-8') as f:
    for row in rows:
        f.write(json.dumps(row, sort_keys=True) + '\n')

candidates = [r for r in rows if str(r.get('signal','')).endswith('_candidate')]
controls = [r for r in rows if r not in candidates]
with open(outdir / 'possible_vulnerabilities.md', 'w', encoding='utf-8') as f:
    f.write('# Possible service baseline vulnerabilities\n\n')
    f.write('Status: candidate-only / needs_manual_review\n\n')
    f.write('## possible_manual_review_candidates\n\n')
    if candidates:
        for r in candidates:
            f.write(f"- {{r['service']}} {{r['path']}} status={{r['status']}} signal `{{r['signal']}}`: {{r.get('title','')}}; {{r.get('detail','')}}\n")
    else:
        f.write('- None from this bounded service baseline run.\n')
    f.write('\n## non_findings_or_controls\n\n')
    if controls:
        for r in controls:
            f.write(f"- {{r['service']}} {{r['path']}} status={{r['status']}} signal `{{r['signal']}}`: {{r.get('title','')}}\n")
    else:
        f.write('- None recorded.\n')
    f.write('\n## missing_evidence_to_confirm\n\n')
    f.write('- Manual verification that any candidate path belongs to the suspected service.\n')
    f.write('- Redacted reproduction/evidence packet.\n')
    f.write('- Version/outdatedness confirmation from primary sources.\n')
    f.write('- Impact analysis beyond scanner/tool wording.\n')
    f.write('- Report-readiness gate before confirmed/reportable/submission language.\n')
PY

sleep 5
health post
printf 'target=%s\nbundle=lab_service_baseline_targets\nservices=apache,tomcat,openssl,haproxy,envoy,traefik\nsemantics=candidate-only\n' "$target" > "$outdir/summary.txt"
printf 'observations.jsonl\npossible_vulnerabilities.md\nhealth.txt\nsummary.txt\nhttp_probe_results.tsv\nopenssl_s_client.txt\ntool_stdout.txt\ntool_stderr.txt\ntool_raw.xml\n' > "$outdir/artifact_manifest.txt"
# Raw outputs are local-lab artifacts only; scanner wording stays candidate-only.
'''


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Generate local-lab service baseline scanner for Apache/Tomcat/OpenSSL/HAProxy/Envoy/Traefik")
    parser.add_argument("--target", required=True)
    parser.add_argument("--output-dir", default="/tmp/lab_service_baseline_targets")
    parser.add_argument("--out-script", default="setting/local/lab_service_baseline_targets_run.sh")
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
