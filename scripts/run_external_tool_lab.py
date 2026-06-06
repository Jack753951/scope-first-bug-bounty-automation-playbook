#!/usr/bin/env python3
"""Controlled local-lab external tool runner plan generator.

This script preserves bounded httpx/katana/nuclei/ffuf lab execution patterns learned in
Phase 4A as reusable project capability. By default it only prints a JSON plan.
It writes an executable bash script only with --execute-lab-approved, and it
never supports public targets, random exploit scripts, callbacks, raw body
capture, or status promotion.
"""

from __future__ import annotations

import argparse
import ipaddress
import json
import shlex
import stat
import sys
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

SUPPORTED_TOOLS = {"httpx", "katana", "nuclei", "ffuf"}
SCHEMA_VERSION = "external_tool_lab_plan/0.1-trial"


def _err(code: str, message: str) -> dict[str, Any]:
    return {"schema_version": SCHEMA_VERSION, "status": "error", "run_mode": "none", "steps": [], "errors": [{"code": code, "message": message}]}


def _is_local_lab_url(target_url: str) -> bool:
    parsed = urlparse(target_url)
    if parsed.scheme not in {"http", "https"} or not parsed.hostname:
        return False
    host = parsed.hostname
    if host in {"localhost"} or host.endswith(".local"):
        return True
    try:
        ip = ipaddress.ip_address(host)
    except ValueError:
        return False
    return ip.is_private or ip.is_loopback or ip.is_link_local


def _validate_limits(rate_limit: int, timeout: int, depth: int) -> dict[str, Any] | None:
    if not (1 <= rate_limit <= 10):
        return _err("RATE_LIMIT_OUT_OF_RANGE", "rate_limit must be between 1 and 10 requests/sec for lab runner")
    if not (1 <= timeout <= 30):
        return _err("TIMEOUT_OUT_OF_RANGE", "timeout must be between 1 and 30 seconds")
    if not (0 <= depth <= 2):
        return _err("DEPTH_OUT_OF_RANGE", "katana depth must be between 0 and 2 for this bounded runner")
    return None


def _scope_regex(target_url: str) -> str:
    parsed = urlparse(target_url)
    host = parsed.hostname or ""
    port = f":{parsed.port}" if parsed.port else ""
    escaped = host.replace(".", "[.]")
    return f"^{parsed.scheme}://{escaped}{port}(/|$)"


def build_plan(
    *,
    target_url: str,
    tools: list[str],
    rate_limit: int = 2,
    timeout: int = 5,
    depth: int = 1,
    output_dir: str,
    execute_lab_approved: bool = False,
) -> dict[str, Any]:
    if not _is_local_lab_url(target_url):
        return _err("TARGET_NOT_LOCAL_LAB", "target_url must be localhost/private/local-lab only")
    unsupported = [tool for tool in tools if tool not in SUPPORTED_TOOLS]
    if unsupported:
        return _err("TOOL_NOT_SUPPORTED", f"unsupported tools: {', '.join(unsupported)}; supported: {', '.join(sorted(SUPPORTED_TOOLS))}")
    limit_error = _validate_limits(rate_limit, timeout, depth)
    if limit_error:
        return limit_error
    if not tools:
        return _err("NO_TOOLS_SELECTED", "select at least one supported tool")

    q_target = shlex.quote(target_url)
    q_out = shlex.quote(output_dir)
    steps: list[dict[str, Any]] = [
        {
            "id": "pre_health",
            "tool": "pre_health",
            "network_touching": True,
            "command": f"curl -sS -I --max-time {timeout} {q_target} | sed -n '1,12p' > {q_out}/pre_health.txt",
        }
    ]
    if "httpx" in tools:
        steps.append(
            {
                "id": "httpx_metadata",
                "tool": "httpx",
                "network_touching": True,
                "command": (
                    f"printf '%s\\n' {q_target} > {q_out}/targets.txt && "
                    f"$HOME/go/bin/httpx -l {q_out}/targets.txt -status-code -title -tech-detect -content-length "
                    f"-response-time -json -timeout {timeout} -retries 0 -rate-limit {rate_limit} -silent -no-color "
                    f"> {q_out}/httpx.jsonl 2> {q_out}/httpx.stderr"
                ),
            }
        )
    if "katana" in tools:
        scope = shlex.quote(_scope_regex(target_url))
        steps.append(
            {
                "id": "katana_depth_limited_crawl",
                "tool": "katana",
                "network_touching": True,
                "command": (
                    f"$HOME/go/bin/katana -u {q_target} -depth {depth} -rate-limit {rate_limit} -timeout {timeout} "
                    f"-crawl-scope {scope} -jsonl -omit-raw -omit-body -silent -no-color "
                    f"-output {q_out}/katana.jsonl > {q_out}/katana.stdout 2> {q_out}/katana.stderr"
                ),
            }
        )
    if "nuclei" in tools:
        template_path = f"{q_out}/nuclei-local-header-observer.yaml"
        steps.append(
            {
                "id": "nuclei_local_header_observer",
                "tool": "nuclei",
                "network_touching": True,
                "command": (
                    f"cat > {template_path} <<'YAML'\n"
                    "id: local-juice-shop-security-headers\n"
                    "info:\n"
                    "  name: Local lab security header observation\n"
                    "  author: hermes\n"
                    "  severity: info\n"
                    "  tags: local-lab,headers\n"
                    "http:\n"
                    "  - method: GET\n"
                    "    path:\n"
                    "      - '{{BaseURL}}/'\n"
                    "    matchers:\n"
                    "      - type: status\n"
                    "        status:\n"
                    "          - 200\n"
                    "YAML\n"
                    f"nuclei -u {q_target} -t {template_path} -jsonl -o {q_out}/nuclei.jsonl "
                    f"-timeout {timeout} -retries 0 -rl {rate_limit} -interactions-cache-size 1 -omit-raw "
                    f"-disable-update-check -silent -no-color > {q_out}/nuclei.stdout 2> {q_out}/nuclei.stderr"
                ),
            }
        )
    if "ffuf" in tools:
        steps.append(
            {
                "id": "ffuf_tiny_content_discovery",
                "tool": "ffuf",
                "network_touching": True,
                "command": (
                    f"printf 'ftp\\nassets\\nrest\\napi\\nadministration\\nrobots.txt\\nsecurity.txt\\n' > {q_out}/phase4a_tiny_wordlist.txt && "
                    f"ffuf -w {q_out}/phase4a_tiny_wordlist.txt -u {q_target}/FUZZ -of json -o {q_out}/ffuf.json "
                    f"-rate {rate_limit} -timeout {timeout} -maxtime 30 -s > {q_out}/ffuf.stdout 2> {q_out}/ffuf.stderr"
                ),
            }
        )
    steps.append(
        {
            "id": "post_health",
            "tool": "post_health",
            "network_touching": True,
            "command": f"curl -sS -I --max-time {timeout} {q_target} | sed -n '1,12p' > {q_out}/post_health.txt",
        }
    )
    return {
        "schema_version": SCHEMA_VERSION,
        "status": "ok",
        "run_mode": "execute_script_allowed" if execute_lab_approved else "plan_only",
        "target_url": target_url,
        "tools": tools,
        "limits": {"rate_limit": rate_limit, "timeout": timeout, "depth": depth},
        "output_dir": output_dir,
        "safety": {
            "local_lab_only": True,
            "requires_execute_lab_approved_for_script_write": True,
            "raw_body_capture": False,
            "callbacks": False,
            "promotes_findings": False,
            "supported_tools_only": sorted(SUPPORTED_TOOLS),
        },
        "steps": steps,
        "errors": [],
    }


def render_bash(plan: dict[str, Any]) -> str:
    lines = [
        "#!/usr/bin/env bash",
        "set -euo pipefail",
        "export PATH=\"$HOME/go/bin:$PATH\"",
        f"OUT={shlex.quote(plan['output_dir'])}",
        "mkdir -p \"$OUT\"",
        "date -u +%Y-%m-%dT%H:%M:%SZ > \"$OUT/generated_at.txt\"",
        "",
    ]
    for step in plan["steps"]:
        lines.append(f"# {step['id']}")
        lines.append(step["command"])
        lines.append("")
    lines.append("find \"$OUT\" -maxdepth 1 -type f -printf '%f\\n' | sort > \"$OUT/artifact_manifest.txt\"")
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Generate bounded httpx/katana/nuclei/ffuf local-lab execution plan or script")
    parser.add_argument("--target-url", required=True)
    parser.add_argument("--tool", action="append", dest="tools", required=True, choices=sorted(SUPPORTED_TOOLS))
    parser.add_argument("--rate-limit", type=int, default=2)
    parser.add_argument("--timeout", type=int, default=5)
    parser.add_argument("--depth", type=int, default=1)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--write-script")
    parser.add_argument("--execute-lab-approved", action="store_true")
    args = parser.parse_args(argv)

    plan = build_plan(
        target_url=args.target_url,
        tools=args.tools,
        rate_limit=args.rate_limit,
        timeout=args.timeout,
        depth=args.depth,
        output_dir=args.output_dir,
        execute_lab_approved=args.execute_lab_approved,
    )
    if plan["status"] != "ok":
        print(json.dumps(plan, indent=2, sort_keys=True))
        return 2
    if args.write_script:
        if not args.execute_lab_approved:
            print(json.dumps(_err("EXECUTE_APPROVAL_REQUIRED", "--write-script requires --execute-lab-approved"), indent=2, sort_keys=True))
            return 2
        path = Path(args.write_script)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(render_bash(plan), encoding="utf-8")
        path.chmod(path.stat().st_mode | stat.S_IXUSR)
    print(json.dumps(plan, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
