#!/usr/bin/env python3
"""Bounded /ftp/ filename content-class verifier for local lab use.

This adapter turns the Phase 4B directory-listing lead into a small reusable
script combination: health check, one GET for /ftp/, local filename parsing, and
candidate-only JSONL output. It does not bulk download listed files, crawl, keep
raw bodies, or promote findings.
"""

from __future__ import annotations

import argparse
import html.parser
import ipaddress
import json
import posixpath
import re
import shlex
import stat
from pathlib import Path
from typing import Any
from urllib.parse import unquote, urljoin, urlparse

SCHEMA_VERSION = "ftp_filename_content_class_verifier/0.1-trial"
DEFAULT_REQUEST_CAP = 20
MIN_REQUEST_CAP = 3
MAX_REQUEST_CAP = 40
DEFAULT_TIMEOUT = 5
DEFAULT_RATE_LIMIT = 2
MAX_BODY_BYTES = 65536
SNIPPET_BYTES = 220
ALLOWED_PATHS = {"/ftp/"}


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


def _normalize_candidate_path(candidate_path: str) -> str:
    if not candidate_path.startswith("/"):
        candidate_path = "/" + candidate_path
    if not candidate_path.endswith("/"):
        candidate_path += "/"
    return candidate_path


def _validate_limits(request_cap: int, timeout: int, rate_limit: int) -> dict[str, Any] | None:
    if not (MIN_REQUEST_CAP <= request_cap <= MAX_REQUEST_CAP):
        return _err("REQUEST_CAP_OUT_OF_RANGE", f"request_cap must be between {MIN_REQUEST_CAP} and {MAX_REQUEST_CAP}")
    if not (1 <= timeout <= 5):
        return _err("TIMEOUT_OUT_OF_RANGE", "fast-lane timeout must be between 1 and 5 seconds")
    if not (1 <= rate_limit <= 2):
        return _err("RATE_LIMIT_OUT_OF_RANGE", "fast-lane rate_limit must be between 1 and 2 requests/sec")
    planned = 3
    if planned > request_cap:
        return _err("REQUEST_CAP_TOO_LOW", f"request_cap {request_cap} is below planned request count {planned}")
    return None


def classify_filename(filename: str) -> str:
    lower = filename.lower()
    suffixes = Path(lower).suffixes
    ext = suffixes[-1] if suffixes else ""
    if lower.endswith(('.bak', '.backup', '.old', '.orig', '.tmp', '.swp')) or any(s in {'.bak', '.backup', '.old', '.orig', '.tmp'} for s in suffixes):
        return "backup_or_temporary_candidate"
    if ext == '.kdbx':
        return "password_database_candidate"
    if ext in {'.key', '.pem', '.p12', '.pfx', '.jks'}:
        return "sensitive_container_candidate"
    if 'pass' in lower or 'secret' in lower or 'credential' in lower or 'token' in lower:
        return "sensitive_name_candidate"
    if ext in {'.md', '.txt', '.csv', '.log'}:
        return "text_or_markdown"
    if ext in {'.pdf', '.doc', '.docx', '.xls', '.xlsx'}:
        return "document"
    if ext in {'.zip', '.7z', '.tar', '.gz', '.tgz', '.rar'}:
        return "archive"
    if ext in {'.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp'}:
        return "image"
    return "unknown_or_other"


class _HrefParser(html.parser.HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.hrefs: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.lower() != "a":
            return
        for key, value in attrs:
            if key.lower() == "href" and value:
                self.hrefs.append(value.strip())


def extract_ftp_entries(html_text: str, listing_url: str) -> list[dict[str, Any]]:
    parser = _HrefParser()
    parser.feed(html_text)
    listing = urlparse(listing_url)
    entries: list[dict[str, Any]] = []
    seen: set[str] = set()
    for raw_href in parser.hrefs:
        if raw_href.startswith(("#", "?", "mailto:", "javascript:")):
            continue
        absolute = urljoin(listing_url, raw_href)
        parsed = urlparse(absolute)
        if parsed.scheme not in {"http", "https"}:
            continue
        if parsed.netloc != listing.netloc:
            continue
        if not parsed.path.startswith(listing.path):
            continue
        if parsed.path.rstrip("/") == listing.path.rstrip("/"):
            continue
        basename = unquote(posixpath.basename(parsed.path.rstrip("/")))
        if not basename or basename in {".", ".."}:
            continue
        if basename in seen:
            continue
        seen.add(basename)
        entries.append({
            "filename": basename,
            "href": raw_href,
            "normalized_path": parsed.path,
            "extension": "".join(Path(basename.lower()).suffixes[-1:]),
            "content_class": classify_filename(basename),
            "status": "needs_manual_review",
            "manual_verification_required": True,
        })
    return entries


def build_plan(
    *,
    target_url: str,
    output_dir: str,
    candidate_path: str = "/ftp/",
    request_cap: int = DEFAULT_REQUEST_CAP,
    timeout: int = DEFAULT_TIMEOUT,
    rate_limit: int = DEFAULT_RATE_LIMIT,
    lab_approved: bool = False,
) -> dict[str, Any]:
    if not _is_fast_lane_lab_url(target_url):
        return _err("TARGET_NOT_FAST_LANE_LAB", "target_url must be localhost/private host-only lab target")
    candidate_path = _normalize_candidate_path(candidate_path)
    if candidate_path not in ALLOWED_PATHS:
        return _err("UNSUPPORTED_CANDIDATE_PATH", "fast-lane filename verifier currently only supports /ftp/")
    limit_error = _validate_limits(request_cap, timeout, rate_limit)
    if limit_error:
        return limit_error

    base = _base_url(target_url)
    listing_url = urljoin(base, candidate_path.lstrip("/"))
    steps = [
        {"id": "pre_health", "kind": "health", "method": "GET", "url": base, "output": "pre_health.txt"},
        {
            "id": "ftp_listing_parse",
            "kind": "directory_listing_filename_parse",
            "method": "GET",
            "module_id": "level1.directory_listing_metadata.filename_content_class",
            "path": candidate_path,
            "url": listing_url,
            "note": "parse listing anchors into filename/content-class candidates without downloading listed files",
        },
        {"id": "post_health", "kind": "health", "method": "GET", "url": base, "output": "post_health.txt"},
    ]
    return {
        "schema_version": SCHEMA_VERSION,
        "status": "ok",
        "run_mode": "execute_script_allowed" if lab_approved else "plan_only",
        "target_url": base,
        "candidate_path": candidate_path,
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
            "directory_listing_only": True,
            "fixed_path_only": True,
            "bulk_download": False,
            "recursive_crawl": False,
            "scanner_execution": False,
            "exploit_payloads": False,
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
    max_body = int(plan["limits"]["max_body_bytes"])
    out = _sq(plan["output_dir"])
    target = _sq(plan["target_url"])
    listing_step = next(step for step in plan["steps"] if step["kind"] == "directory_listing_filename_parse")
    listing_url = _sq(listing_step["url"])
    logical_path = _sq(listing_step["path"])
    module_id = _sq(listing_step["module_id"])

    lines = [
        "#!/usr/bin/env bash",
        "set -euo pipefail",
        f"OUT={out}",
        f"TARGET={target}",
        f"LISTING_URL={listing_url}",
        f"LOGICAL_PATH={logical_path}",
        f"MODULE_ID={module_id}",
        f"TIMEOUT={timeout}",
        f"MAX_BODY_BYTES={max_body}",
        "mkdir -p \"$OUT\"",
        ": > \"$OUT/observations.jsonl\"",
        ": > \"$OUT/health.txt\"",
        ": > \"$OUT/pre_health.txt\"",
        ": > \"$OUT/post_health.txt\"",
        "REQ_COUNT=0",
        f"record_health(){{ local label=$1; local code file; file=\"$OUT/${{label}}.txt\"; code=$(curl -sS --max-time {timeout} --max-filesize $MAX_BODY_BYTES -o /dev/null -w '%{{http_code}}' \"$TARGET\" || true); echo \"${{label}}=${{code}}\" >> \"$OUT/health.txt\"; echo \"${{label}}=${{code}}\" > \"$file\"; }}",
        "record_ftp_listing(){",
        "  REQ_COUNT=$((REQ_COUNT+1))",
        "  local hdr=\"$OUT/ftp_listing_parse.headers\" body=\"$OUT/ftp_listing_parse.tmp_body\"",
        "  local code",
        f"  code=$(curl -sS --max-time {timeout} --max-filesize $MAX_BODY_BYTES --max-redirs 0 -D \"$hdr\" -o \"$body\" -w '%{{http_code}}' \"$LISTING_URL\" || true)",
        "  python3 - \"$MODULE_ID\" \"$LISTING_URL\" \"$LOGICAL_PATH\" \"$code\" \"$hdr\" \"$body\" >> \"$OUT/observations.jsonl\" <<'PY'",
        "import datetime, hashlib, html.parser, json, pathlib, posixpath, re, sys, urllib.parse",
        "module_id, listing_url, logical_path, curl_code, hdr_path, body_path = sys.argv[1:7]",
        "headers_text = pathlib.Path(hdr_path).read_text(encoding='utf-8', errors='replace') if pathlib.Path(hdr_path).exists() else ''",
        "body = pathlib.Path(body_path).read_bytes() if pathlib.Path(body_path).exists() else b''",
        "body_text = body[:20000].decode('utf-8', errors='replace')",
        "status_code = None",
        "for line in headers_text.splitlines():",
        "    m = re.search(r'HTTP/[^ ]+ ([0-9]{3})', line)",
        "    if m: status_code = int(m.group(1))",
        "headers = {}",
        "for line in headers_text.splitlines():",
        "    if ':' in line:",
        "        key, value = line.split(':', 1); headers[key.lower()] = value.strip()",
        "class HrefParser(html.parser.HTMLParser):",
        "    def __init__(self): super().__init__(); self.hrefs=[]",
        "    def handle_starttag(self, tag, attrs):",
        "        if tag.lower() == 'a':",
        "            for key, value in attrs:",
        "                if key.lower() == 'href' and value: self.hrefs.append(value.strip())",
        "def classify_filename(filename):",
        "    lower=filename.lower(); suffixes=pathlib.Path(lower).suffixes; ext=suffixes[-1] if suffixes else ''",
        "    if lower.endswith(('.bak','.backup','.old','.orig','.tmp','.swp')) or any(s in {'.bak','.backup','.old','.orig','.tmp'} for s in suffixes): return 'backup_or_temporary_candidate'",
        "    if ext == '.kdbx': return 'password_database_candidate'",
        "    if ext in {'.key','.pem','.p12','.pfx','.jks'}: return 'sensitive_container_candidate'",
        "    if 'pass' in lower or 'secret' in lower or 'credential' in lower or 'token' in lower: return 'sensitive_name_candidate'",
        "    if ext in {'.md','.txt','.csv','.log'}: return 'text_or_markdown'",
        "    if ext in {'.pdf','.doc','.docx','.xls','.xlsx'}: return 'document'",
        "    if ext in {'.zip','.7z','.tar','.gz','.tgz','.rar'}: return 'archive'",
        "    if ext in {'.png','.jpg','.jpeg','.gif','.svg','.webp'}: return 'image'",
        "    return 'unknown_or_other'",
        "def extract_ftp_entries(html_text, listing_url):",
        "    parser=HrefParser(); parser.feed(html_text); listing=urllib.parse.urlparse(listing_url); entries=[]; seen=set()",
        "    for raw_href in parser.hrefs:",
        "        if raw_href.startswith(('#','?','mailto:','javascript:')): continue",
        "        absolute=urllib.parse.urljoin(listing_url, raw_href); parsed=urllib.parse.urlparse(absolute)",
        "        if parsed.scheme not in {'http','https'} or parsed.netloc != listing.netloc: continue",
        "        if not parsed.path.startswith(listing.path): continue",
        "        if parsed.path.rstrip('/') == listing.path.rstrip('/'): continue",
        "        basename=urllib.parse.unquote(posixpath.basename(parsed.path.rstrip('/')))",
        "        if not basename or basename in {'.','..'} or basename in seen: continue",
        "        seen.add(basename)",
        "        entries.append({'filename':basename,'href':raw_href,'normalized_path':parsed.path,'extension':''.join(pathlib.Path(basename.lower()).suffixes[-1:]),'content_class':classify_filename(basename),'status':'needs_manual_review','manual_verification_required':True})",
        "    return entries",
        "title = None",
        "m = re.search(r'<title[^>]*>(.*?)</title>', body_text, flags=re.I|re.S)",
        "if m: title = re.sub(r'\\s+', ' ', m.group(1)).strip()[:120]",
        "entries = extract_ftp_entries(body_text, listing_url)",
        "obs = {'schema_version':'ftp_filename_content_class_observation/0.1-trial','ts_utc':datetime.datetime.now(datetime.UTC).replace(microsecond=0).isoformat().replace('+00:00','Z'),'status':'candidate','kind':'directory_listing_filename_parse','module_id':module_id,'step_id':'ftp_listing_parse','url':listing_url,'path':logical_path,'http_status':status_code,'curl_code':curl_code,'content_type':headers.get('content-type'),'title':title,'body_sha256':hashlib.sha256(body).hexdigest(),'body_size':len(body),'directory_listing_candidate': logical_path == '/ftp/' and status_code == 200,'entries':entries,'entry_count':len(entries),'manual_verification_required':True,'promotes_findings':False}",
        "print(json.dumps(obs, sort_keys=True, ensure_ascii=False))",
        "PY",
        "  rm -f \"$body\"",
        "}",
        "record_health pre_health",
        "record_ftp_listing",
        "record_health post_health",
        "echo \"requests_sent=$REQ_COUNT\" >> \"$OUT/health.txt\"",
        "python3 - \"$OUT/observations.jsonl\" \"$OUT/summary.txt\" <<'PY'",
        "import json, sys",
        "rows=[json.loads(line) for line in open(sys.argv[1], encoding='utf-8') if line.strip()]",
        "with open(sys.argv[2], 'w', encoding='utf-8') as out:",
        "    out.write(f'observations={len(rows)}\\n')",
        "    for r in rows:",
        "        out.write(f\"GET {r.get('path')} -> {r.get('http_status')} entries={r.get('entry_count')} title={r.get('title')!r}\\n\")",
        "        for e in r.get('entries', []): out.write(f\"- {e.get('filename')} [{e.get('content_class')}] {e.get('status')}\\n\")",
        "PY",
        "find \"$OUT\" -maxdepth 1 -type f -printf '%f\\n' | sort > \"$OUT/artifact_manifest.txt\"",
    ]
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target-url", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--candidate-path", default="/ftp/")
    parser.add_argument("--request-cap", type=int, default=DEFAULT_REQUEST_CAP)
    parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT)
    parser.add_argument("--rate-limit", type=int, default=DEFAULT_RATE_LIMIT)
    parser.add_argument("--lab-approved", action="store_true")
    parser.add_argument("--write-script")
    args = parser.parse_args(argv)

    plan = build_plan(
        target_url=args.target_url,
        output_dir=args.output_dir,
        candidate_path=args.candidate_path,
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
