#!/usr/bin/env python3
"""Phase 4B Wave2 benign parameter lab adapter.

This is the fast-lane replacement for directly running open-redirect/XSS helper
scripts. It uses fixed local-lab URLs, inert text canaries, no redirect following,
no executable browser payloads, no crawlers/scanners, capped requests, and
candidate-only JSONL observations.
"""

from __future__ import annotations

import argparse
import ipaddress
import json
import shlex
import stat
from pathlib import Path
from typing import Any
from urllib.parse import quote, urljoin, urlparse

SCHEMA_VERSION = "phase4b_wave2_benign_params/0.1-trial"
DEFAULT_REQUEST_CAP = 40
MAX_REQUEST_CAP = 100
MIN_REQUEST_CAP = 10
DEFAULT_TIMEOUT = 5
DEFAULT_RATE_LIMIT = 2
MAX_BODY_BYTES = 65536
SNIPPET_BYTES = 300
REFLECT_CANARY = "PHASE4B_REFLECT_CANARY"
EXTERNAL_REDIRECT_CANARY = "https://phase4b-canary.invalid/"


def _param_paths() -> list[tuple[str, str, str, str, str]]:
    encoded_reflect = quote(REFLECT_CANARY, safe="")
    encoded_external = quote(EXTERNAL_REDIRECT_CANARY, safe="")
    return [
        (
            "api_search_reflect_canary",
            "level2.benign_reflection_candidate",
            f"/rest/products/search?q={encoded_reflect}",
            REFLECT_CANARY,
            "API search inert text canary",
        ),
        (
            "spa_search_reflect_canary",
            "level2.benign_reflection_candidate",
            f"/search?q={encoded_reflect}",
            REFLECT_CANARY,
            "SPA search inert text canary / fallback control",
        ),
        (
            "redirect_external_canary",
            "level2.open_redirect_candidate",
            f"/redirect?to={encoded_external}",
            EXTERNAL_REDIRECT_CANARY,
            "external redirect inert canary; do not follow",
        ),
        (
            "redirect_root_canary",
            "level2.open_redirect_candidate",
            "/redirect?to=/",
            "/",
            "relative redirect canary; do not follow",
        ),
        (
            "redirect_scoreboard_canary",
            "level2.open_redirect_candidate",
            "/redirect?to=/#/score-board",
            "/#/score-board",
            "relative fragment redirect canary; do not follow",
        ),
    ]


def _err(code: str, message: str) -> dict[str, Any]:
    return {
        "schema_version": SCHEMA_VERSION,
        "status": "error",
        "run_mode": "none",
        "steps": [],
        "outputs": [],
        "errors": [{"code": code, "message": message}],
    }


def _is_fast_lane_lab_url(target_url: str) -> bool:
    parsed = urlparse(target_url)
    if parsed.scheme not in {"http", "https"} or not parsed.hostname:
        return False
    host = parsed.hostname
    if host in {"localhost", "127.0.0.1", "::1"}:
        return True
    try:
        ip = ipaddress.ip_address(host)
    except ValueError:
        return host.endswith(".local")
    return ip.is_private or ip.is_loopback or ip.is_link_local


def _base_url(target_url: str) -> str:
    parsed = urlparse(target_url)
    clean = parsed._replace(path="", params="", query="", fragment="")
    return clean.geturl().rstrip("/") + "/"


def _validate_limits(request_cap: int, timeout: int, rate_limit: int) -> dict[str, Any] | None:
    if not (MIN_REQUEST_CAP <= request_cap <= MAX_REQUEST_CAP):
        return _err("REQUEST_CAP_OUT_OF_RANGE", f"request_cap must be between {MIN_REQUEST_CAP} and {MAX_REQUEST_CAP}")
    if not (1 <= timeout <= 5):
        return _err("TIMEOUT_OUT_OF_RANGE", "fast-lane timeout must be between 1 and 5 seconds")
    if not (1 <= rate_limit <= 2):
        return _err("RATE_LIMIT_OUT_OF_RANGE", "fast-lane rate_limit must be between 1 and 2 requests/sec")
    planned = 2 + len(_param_paths())
    if planned > request_cap:
        return _err("REQUEST_CAP_TOO_LOW", f"request_cap {request_cap} is below planned request count {planned}")
    return None


def build_plan(
    *,
    target_url: str,
    output_dir: str,
    request_cap: int = DEFAULT_REQUEST_CAP,
    timeout: int = DEFAULT_TIMEOUT,
    rate_limit: int = DEFAULT_RATE_LIMIT,
    lab_approved: bool = False,
) -> dict[str, Any]:
    if not _is_fast_lane_lab_url(target_url):
        return _err("TARGET_NOT_FAST_LANE_LAB", "target_url must be localhost/private host-only lab target")
    limit_error = _validate_limits(request_cap, timeout, rate_limit)
    if limit_error:
        return limit_error

    base = _base_url(target_url)
    steps: list[dict[str, Any]] = [
        {"id": "pre_health", "kind": "health", "method": "GET", "url": base, "output": "pre_health.txt"}
    ]
    for step_id, module_id, path, canary, note in _param_paths():
        steps.append({
            "id": step_id,
            "kind": "benign_parameter_probe",
            "method": "GET",
            "module_id": module_id,
            "path": path,
            "url": urljoin(base, path.lstrip("/")),
            "canary": canary,
            "note": note,
        })
    steps.append({"id": "post_health", "kind": "health", "method": "GET", "url": base, "output": "post_health.txt"})

    return {
        "schema_version": SCHEMA_VERSION,
        "status": "ok",
        "run_mode": "execute_script_allowed" if lab_approved else "plan_only",
        "target_url": base,
        "limits": {
            "request_cap": request_cap,
            "planned_requests": len(steps),
            "timeout": timeout,
            "rate_limit": rate_limit,
            "max_body_bytes": MAX_BODY_BYTES,
            "snippet_bytes": SNIPPET_BYTES,
        },
        "outputs": ["observations.jsonl", "summary.txt", "health.txt", "artifact_manifest.txt"],
        "output_dir": output_dir,
        "safety": {
            "lab_fast_lane": True,
            "local_lab_only": True,
            "get_only": True,
            "fixed_urls_only": True,
            "inert_canaries_only": True,
            "executable_payloads": False,
            "redirect_following": False,
            "crawler_execution": False,
            "scanner_execution": False,
            "callbacks": False,
            "credential_flows": False,
            "raw_body_persistence": False,
            "promotes_findings": False,
        },
        "steps": steps,
        "errors": [],
    }


def _sq(value: str) -> str:
    return shlex.quote(value)


def render_bash(plan: dict[str, Any]) -> str:
    timeout = int(plan["limits"]["timeout"])
    rate_limit = int(plan["limits"]["rate_limit"])
    delay = max(0.0, 1.0 / rate_limit)
    max_body = int(plan["limits"]["max_body_bytes"])
    snippet = int(plan["limits"]["snippet_bytes"])
    out = _sq(plan["output_dir"])
    target = _sq(plan["target_url"])

    lines = [
        "#!/usr/bin/env bash",
        "set -euo pipefail",
        f"OUT={out}",
        f"TARGET={target}",
        f"TIMEOUT={timeout}",
        f"MAX_BODY_BYTES={max_body}",
        f"SNIPPET_BYTES={snippet}",
        "mkdir -p \"$OUT\"",
        ": > \"$OUT/observations.jsonl\"",
        ": > \"$OUT/health.txt\"",
        ": > \"$OUT/pre_health.txt\"",
        ": > \"$OUT/post_health.txt\"",
        "REQ_COUNT=0",
        f"record_health(){{ local label=$1; local code file; file=\"$OUT/${{label}}.txt\"; code=$(curl -sS --max-time {timeout} --max-filesize $MAX_BODY_BYTES -o /dev/null -w '%{{http_code}}' \"$TARGET\" || true); echo \"${{label}}=${{code}}\" >> \"$OUT/health.txt\"; echo \"${{label}}=${{code}}\" > \"$file\"; }}",
        "record_probe(){",
        "  local id=$1 module_id=$2 url=$3 logical_path=$4 canary=$5 note=$6",
        "  REQ_COUNT=$((REQ_COUNT+1))",
        "  local hdr=\"$OUT/${id}.headers\" body=\"$OUT/${id}.tmp_body\"",
        "  local code",
        f"  code=$(curl -sS --max-time {timeout} --max-filesize $MAX_BODY_BYTES --max-redirs 0 -D \"$hdr\" -o \"$body\" -w '%{{http_code}}' \"$url\" || true)",
        "  python3 - \"$id\" \"$module_id\" \"$url\" \"$logical_path\" \"$canary\" \"$note\" \"$code\" \"$hdr\" \"$body\" \"$SNIPPET_BYTES\" \"$TARGET\" >> \"$OUT/observations.jsonl\" <<'PY'",
        "import hashlib, json, pathlib, re, sys, datetime, urllib.parse",
        "step_id, module_id, url, logical_path, canary, note, curl_code, hdr_path, body_path, snippet_bytes, target = sys.argv[1:12]",
        "headers_text = pathlib.Path(hdr_path).read_text(encoding='utf-8', errors='replace') if pathlib.Path(hdr_path).exists() else ''",
        "body = pathlib.Path(body_path).read_bytes() if pathlib.Path(body_path).exists() else b''",
        "body_text = body[:20000].decode('utf-8', errors='replace')",
        "status = None",
        "for line in headers_text.splitlines():",
        "    m = re.search(r'HTTP/[^ ]+ ([0-9]{3})', line)",
        "    if m: status = int(m.group(1))",
        "headers = {}",
        "for line in headers_text.splitlines():",
        "    if ':' in line:",
        "        key, value = line.split(':', 1); headers[key.lower()] = value.strip()",
        "location = headers.get('location')",
        "target_host = urllib.parse.urlparse(target).hostname",
        "location_host = urllib.parse.urlparse(urllib.parse.urljoin(target, location or '')).hostname if location else None",
        "is_reflection_step = module_id.endswith('benign_reflection_candidate')",
        "canary_in_body = bool(is_reflection_step and canary and canary in body_text)",
        "canary_echoed_in_error_body = bool((not is_reflection_step) and canary and len(canary) > 3 and canary in body_text)",
        "canary_in_location = bool(canary and location and canary in location)",
        "external_redirect_candidate = bool(status in {301,302,303,307,308} and location and location_host and target_host and location_host != target_host)",
        "title = None",
        "m = re.search(r'<title[^>]*>(.*?)</title>', body_text, flags=re.I|re.S)",
        "if m: title = re.sub(r'\\s+', ' ', m.group(1)).strip()[:120]",
        "snippet = body[:int(snippet_bytes)].decode('utf-8', errors='replace')",
        "snippet = re.sub(r'(?i)(token|secret|password|api[_-]?key|session|cookie)[^\\s<>&]{0,80}', '[REDACTED]', snippet)",
        "snippet = re.sub(r'\\s+', ' ', snippet).strip()[:300]",
        "obs = {'schema_version':'phase4b_wave2_observation/0.1-trial','ts_utc':datetime.datetime.now(datetime.UTC).replace(microsecond=0).isoformat().replace('+00:00','Z'),'status':'candidate','kind':'benign_parameter_probe','module_id':module_id,'step_id':step_id,'url':url,'path':logical_path,'note':note,'http_status':status,'curl_code':curl_code,'content_type':headers.get('content-type'),'location_header':location,'location_host':location_host,'title':title,'body_sha256':hashlib.sha256(body).hexdigest(),'body_size':len(body),'short_redacted_snippet':snippet,'canary':canary,'canary_in_body':canary_in_body,'canary_echoed_in_error_body':canary_echoed_in_error_body,'canary_in_location':canary_in_location,'external_redirect_candidate':external_redirect_candidate,'manual_verification_required':True,'promotes_findings':False}",
        "print(json.dumps(obs, sort_keys=True, ensure_ascii=False))",
        "PY",
        "  rm -f \"$body\"",
        "}",
        "record_health pre_health",
    ]
    for step in plan["steps"]:
        if step["kind"] != "benign_parameter_probe":
            continue
        lines.append(
            "record_probe "
            f"{_sq(step['id'])} {_sq(step['module_id'])} {_sq(step['url'])} {_sq(step['path'])} {_sq(step['canary'])} {_sq(step['note'])}"
        )
        if delay:
            lines.append(f"sleep {delay:g}")
    lines.extend([
        "record_health post_health",
        "echo \"requests_sent=$REQ_COUNT\" >> \"$OUT/health.txt\"",
        "python3 - \"$OUT/observations.jsonl\" \"$OUT/summary.txt\" <<'PY'",
        "import collections, json, sys",
        "rows=[json.loads(line) for line in open(sys.argv[1], encoding='utf-8') if line.strip()]",
        "by=collections.Counter((r.get('module_id'), str(r.get('http_status')), r.get('content_type') or '') for r in rows)",
        "with open(sys.argv[2], 'w', encoding='utf-8') as out:",
        "    out.write(f'observations={len(rows)}\\n')",
        "    for key, count in sorted(by.items()): out.write(f'{count} x {key}\\n')",
        "    out.write('\\nnotable_params\\n')",
        "    for r in rows: out.write(f\"GET {r.get('path')} -> {r.get('http_status')} body_canary={r.get('canary_in_body')} loc_canary={r.get('canary_in_location')} ext_redirect={r.get('external_redirect_candidate')} loc={r.get('location_header')!r} title={r.get('title')!r}\\n\")",
        "PY",
        "find \"$OUT\" -maxdepth 1 -type f -printf '%f\\n' | sort > \"$OUT/artifact_manifest.txt\"",
    ])
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target-url", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--request-cap", type=int, default=DEFAULT_REQUEST_CAP)
    parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT)
    parser.add_argument("--rate-limit", type=int, default=DEFAULT_RATE_LIMIT)
    parser.add_argument("--lab-approved", action="store_true")
    parser.add_argument("--write-script")
    args = parser.parse_args(argv)

    plan = build_plan(
        target_url=args.target_url,
        output_dir=args.output_dir,
        request_cap=args.request_cap,
        timeout=args.timeout,
        rate_limit=args.rate_limit,
        lab_approved=args.lab_approved,
    )
    if plan["status"] != "ok":
        print(json.dumps(plan, indent=2, sort_keys=True))
        return 2
    if args.write_script and not args.lab_approved:
        print(json.dumps(_err("LAB_APPROVAL_REQUIRED", "--write-script requires --lab-approved"), indent=2, sort_keys=True))
        return 2
    if args.write_script:
        path = Path(args.write_script)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(render_bash(plan), encoding="utf-8", newline="\n")
        path.chmod(path.stat().st_mode | stat.S_IXUSR)
    print(json.dumps(plan, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
