#!/usr/bin/env python3
"""Reusable bounded Wave 1A metadata local-lab adapter.

Default behavior is plan-only. Writing an executable bash script requires
--lab-approved and remains limited to local/private lab URLs, tiny fixed metadata
requests, health checks, and non-promotional JSONL observations.
"""

from __future__ import annotations

import argparse
import ipaddress
import json
import shlex
import stat
from pathlib import Path
from typing import Any
from urllib.parse import urljoin, urlparse

SCHEMA_VERSION = "wave1a_metadata_lab_plan/0.1-trial"
MODULE_IDS = [
    "level1.directory_listing_metadata",
    "level1.robots_securitytxt_metadata",
    "level1.api_docs_metadata",
    "level1.dependency_manifest_metadata",
    "level1.cors_metadata",
]
KNOWN_PATHS = [
    "/robots.txt",
    "/.well-known/security.txt",
    "/ftp/",
    "/api-docs/",
    "/rest/products/search",
]
CORS_PATHS = ["/", "/rest/products/search"]
CORS_ORIGINS = ["https://example.invalid", "null"]
MIN_REQUEST_CAP = 8
MAX_REQUEST_CAP = 30
DEFAULT_REQUEST_CAP = 24


def _err(code: str, message: str) -> dict[str, Any]:
    return {
        "schema_version": SCHEMA_VERSION,
        "status": "error",
        "run_mode": "none",
        "module_ids": [],
        "steps": [],
        "outputs": [],
        "errors": [{"code": code, "message": message}],
    }


def _is_local_lab_url(target_url: str) -> bool:
    parsed = urlparse(target_url)
    if parsed.scheme not in {"http", "https"} or not parsed.hostname:
        return False
    host = parsed.hostname
    if host in {"localhost", "127.0.0.1", "::1"} or host.endswith(".local"):
        return True
    try:
        ip = ipaddress.ip_address(host)
    except ValueError:
        return False
    return ip.is_private or ip.is_loopback or ip.is_link_local


def _normalized_base_url(target_url: str) -> str:
    parsed = urlparse(target_url)
    path = parsed.path if parsed.path and parsed.path != "/" else ""
    base = parsed._replace(path=path.rstrip("/"), params="", query="", fragment="")
    return base.geturl().rstrip("/") + "/"


def _validate_limits(*, request_cap: int, timeout: int, rate_limit: int) -> dict[str, Any] | None:
    if not (MIN_REQUEST_CAP <= request_cap <= MAX_REQUEST_CAP):
        return _err("REQUEST_CAP_OUT_OF_RANGE", f"request_cap must be between {MIN_REQUEST_CAP} and {MAX_REQUEST_CAP}")
    if not (1 <= timeout <= 15):
        return _err("TIMEOUT_OUT_OF_RANGE", "timeout must be between 1 and 15 seconds")
    if not (1 <= rate_limit <= 5):
        return _err("RATE_LIMIT_OUT_OF_RANGE", "rate_limit must be between 1 and 5 requests/sec")
    planned_requests = 2 + len(KNOWN_PATHS) + len(CORS_PATHS) * len(CORS_ORIGINS)
    if planned_requests > request_cap:
        return _err("REQUEST_CAP_TOO_LOW", f"request_cap {request_cap} is below planned request count {planned_requests}")
    return None


def _target_url_for_path(base_url: str, path: str) -> str:
    return urljoin(base_url, path.lstrip("/"))


def build_plan(
    *,
    target_url: str,
    output_dir: str,
    request_cap: int = DEFAULT_REQUEST_CAP,
    timeout: int = 5,
    rate_limit: int = 2,
    lab_approved: bool = False,
) -> dict[str, Any]:
    if not _is_local_lab_url(target_url):
        return _err("TARGET_NOT_LOCAL_LAB", "target_url must be localhost/private/local-lab only")
    limit_error = _validate_limits(request_cap=request_cap, timeout=timeout, rate_limit=rate_limit)
    if limit_error:
        return limit_error

    base_url = _normalized_base_url(target_url)
    steps: list[dict[str, Any]] = [
        {
            "id": "pre_health",
            "kind": "health",
            "network_touching": True,
            "url": base_url,
            "output": "pre_health.txt",
        }
    ]
    for path in KNOWN_PATHS:
        module_id = (
            "level1.directory_listing_metadata" if path == "/ftp/" else
            "level1.robots_securitytxt_metadata" if "robots.txt" in path or "security.txt" in path else
            "level1.api_docs_metadata" if path == "/api-docs/" else
            "level1.dependency_manifest_metadata"
        )
        steps.append(
            {
                "id": f"known_path_{path.strip('/').replace('/', '_').replace('.', '_') or 'root'}",
                "kind": "known_path_metadata",
                "module_id": module_id,
                "network_touching": True,
                "path": path,
                "url": _target_url_for_path(base_url, path),
            }
        )
    for origin in CORS_ORIGINS:
        for path in CORS_PATHS:
            steps.append(
                {
                    "id": f"cors_{origin.replace(':', '_').replace('/', '_').replace('.', '_')}_{path.strip('/').replace('/', '_') or 'root'}",
                    "kind": "cors_metadata",
                    "module_id": "level1.cors_metadata",
                    "network_touching": True,
                    "path": path,
                    "origin": origin,
                    "url": _target_url_for_path(base_url, path),
                }
            )
    steps.append(
        {
            "id": "post_health",
            "kind": "health",
            "network_touching": True,
            "url": base_url,
            "output": "post_health.txt",
        }
    )

    return {
        "schema_version": SCHEMA_VERSION,
        "status": "ok",
        "run_mode": "execute_script_allowed" if lab_approved else "plan_only",
        "target_url": base_url,
        "module_ids": MODULE_IDS,
        "limits": {
            "request_cap": request_cap,
            "planned_requests": len(steps),
            "timeout": timeout,
            "rate_limit": rate_limit,
        },
        "output_dir": output_dir,
        "outputs": ["observations.jsonl", "pre_health.txt", "post_health.txt", "artifact_manifest.txt"],
        "safety": {
            "local_lab_only": True,
            "requires_lab_approved_for_script_write": True,
            "fixed_known_paths_only": True,
            "recursive_crawl": False,
            "file_transfer": False,
            "exploit_payloads": False,
            "callbacks": False,
            "promotes_findings": False,
            "raw_body_persistence": False,
        },
        "steps": steps,
        "errors": [],
    }


def _json_for_bash(value: Any) -> str:
    return shlex.quote(json.dumps(value, sort_keys=True))


def render_bash(plan: dict[str, Any]) -> str:
    timeout = int(plan["limits"]["timeout"])
    rate_limit = int(plan["limits"]["rate_limit"])
    delay = max(0.0, 1.0 / rate_limit)
    output_dir = shlex.quote(plan["output_dir"])
    lines = [
        "#!/usr/bin/env bash",
        "set -euo pipefail",
        f"OUT={output_dir}",
        f"TIMEOUT={timeout}",
        "mkdir -p \"$OUT\"",
        ": > \"$OUT/observations.jsonl\"",
        "date -u +%Y-%m-%dT%H:%M:%SZ > \"$OUT/generated_at.txt\"",
        "append_json(){ printf '%s\\n' \"$1\" >> \"$OUT/observations.jsonl\"; }",
        "record_head(){ local id=$1 url=$2 file=$3; curl -sS -I --max-time $TIMEOUT \"$url\" | sed -n '1,20p' > \"$OUT/$file\"; python3 - \"$id\" \"$url\" \"$OUT/$file\" >> \"$OUT/observations.jsonl\" <<'PY'",
        "import json, pathlib, re, sys",
        "step_id, url, path = sys.argv[1:4]",
        "text = pathlib.Path(path).read_text(encoding='utf-8', errors='replace')",
        "status = None",
        "first = text.splitlines()[0] if text.splitlines() else ''",
        "match = re.search(r'HTTP/[^ ]+ ([0-9]{3})', first)",
        "if match: status = int(match.group(1))",
        "headers = {}",
        "for line in text.splitlines()[1:]:",
        "    if ':' in line:",
        "        key, value = line.split(':', 1)",
        "        headers[key.lower()] = value.strip()",
        "print(json.dumps({'schema_version':'observation/0.1-trial','status':'candidate','kind':'health_metadata','step_id':step_id,'url':url,'http_status':status,'content_type':headers.get('content-type'),'promotes_findings':False}, sort_keys=True))",
        "PY",
        "}",
        "record_get(){ local id=$1 module_id=$2 url=$3 logical_path=$4; local hdr=\"$OUT/${id}.headers\"; local body=\"$OUT/${id}.tmp_body\"; curl -sS -L --max-time $TIMEOUT -D \"$hdr\" \"$url\" > \"$body\"; python3 - \"$id\" \"$module_id\" \"$url\" \"$logical_path\" \"$hdr\" \"$body\" >> \"$OUT/observations.jsonl\" <<'PY'",
        "import hashlib, json, pathlib, re, sys",
        "step_id, module_id, url, logical_path, hdr_path, body_path = sys.argv[1:7]",
        "headers_text = pathlib.Path(hdr_path).read_text(encoding='utf-8', errors='replace')",
        "body = pathlib.Path(body_path).read_bytes()",
        "body_text = body[:20000].decode('utf-8', errors='replace')",
        "status = None",
        "for line in headers_text.splitlines():",
        "    m = re.search(r'HTTP/[^ ]+ ([0-9]{3})', line)",
        "    if m: status = int(m.group(1))",
        "headers = {}",
        "for line in headers_text.splitlines():",
        "    if ':' in line:",
        "        key, value = line.split(':', 1)",
        "        headers[key.lower()] = value.strip()",
        "title = None",
        "m = re.search(r'<title[^>]*>(.*?)</title>', body_text, flags=re.I|re.S)",
        "if m: title = re.sub(r'\\s+', ' ', m.group(1)).strip()[:120]",
        "print(json.dumps({'schema_version':'observation/0.1-trial','status':'candidate','kind':'metadata_observation','module_id':module_id,'step_id':step_id,'url':url,'path':logical_path,'http_status':status,'content_type':headers.get('content-type'),'title':title,'body_sha256':hashlib.sha256(body).hexdigest(),'body_size':len(body),'directory_listing_candidate': logical_path == '/ftp/' and status == 200,'promotes_findings':False,'manual_verification_required':True}, sort_keys=True))",
        "PY",
        "rm -f \"$body\"",
        "}",
        "record_cors(){ local id=$1 url=$2 logical_path=$3 origin=$4; local hdr=\"$OUT/${id}.headers\"; curl -sS -I --max-time $TIMEOUT -H \"Origin: $origin\" \"$url\" > \"$hdr\"; python3 - \"$id\" \"$url\" \"$logical_path\" \"$origin\" \"$hdr\" >> \"$OUT/observations.jsonl\" <<'PY'",
        "import json, pathlib, re, sys",
        "step_id, url, logical_path, origin, hdr_path = sys.argv[1:6]",
        "text = pathlib.Path(hdr_path).read_text(encoding='utf-8', errors='replace')",
        "status = None",
        "headers = {}",
        "for line in text.splitlines():",
        "    m = re.search(r'HTTP/[^ ]+ ([0-9]{3})', line)",
        "    if m: status = int(m.group(1))",
        "    if ':' in line:",
        "        key, value = line.split(':', 1)",
        "        headers[key.lower()] = value.strip()",
        "print(json.dumps({'schema_version':'observation/0.1-trial','status':'candidate','kind':'cors_metadata','module_id':'level1.cors_metadata','step_id':step_id,'url':url,'path':logical_path,'origin':origin,'http_status':status,'access_control_allow_origin':headers.get('access-control-allow-origin'),'access_control_allow_credentials':headers.get('access-control-allow-credentials'),'promotes_findings':False,'manual_verification_required':True}, sort_keys=True))",
        "PY",
        "}",
        "",
    ]
    for step in plan["steps"]:
        lines.append(f"# {step['id']}")
        if step["kind"] == "health":
            lines.append(f"record_head {shlex.quote(step['id'])} {shlex.quote(step['url'])} {shlex.quote(step['output'])}")
        elif step["kind"] == "known_path_metadata":
            lines.append(
                "record_get "
                f"{shlex.quote(step['id'])} {shlex.quote(step['module_id'])} "
                f"{shlex.quote(step['url'])} {shlex.quote(step['path'])}"
            )
        elif step["kind"] == "cors_metadata":
            lines.append(f"# origin: {step['origin']}")
            lines.append(
                "record_cors "
                f"{shlex.quote(step['id'])} {shlex.quote(step['url'])} "
                f"{shlex.quote(step['path'])} {shlex.quote(step['origin'])}"
            )
        lines.append(f"sleep {delay:g}")
        lines.append("")
    lines.append("find \"$OUT\" -maxdepth 1 -type f -printf '%f\\n' | sort > \"$OUT/artifact_manifest.txt\"")
    script = "\n".join(lines) + "\n"
    return script.replace("--max-time $TIMEOUT", f"--max-time {timeout}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Generate a bounded Wave 1A metadata local-lab plan or executable script")
    parser.add_argument("--target-url", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--request-cap", type=int, default=DEFAULT_REQUEST_CAP)
    parser.add_argument("--timeout", type=int, default=5)
    parser.add_argument("--rate-limit", type=int, default=2)
    parser.add_argument("--write-script")
    parser.add_argument("--lab-approved", action="store_true")
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
    if args.write_script:
        if not args.lab_approved:
            print(json.dumps(_err("LAB_APPROVAL_REQUIRED", "--write-script requires --lab-approved"), indent=2, sort_keys=True))
            return 2
        path = Path(args.write_script)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(render_bash(plan), encoding="utf-8")
        path.chmod(path.stat().st_mode | stat.S_IXUSR)
    print(json.dumps(plan, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
