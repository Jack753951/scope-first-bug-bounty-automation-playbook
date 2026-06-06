#!/usr/bin/env python3
"""Bounded/offline-safe detector for Next.js <specific-cve-id> indicators.

This artifact is intentionally conservative: it defaults to plan-only mode,
uses GET/HEAD only, stores no response bodies, and reports only candidate
indicators based on baseline-vs-probe response deltas.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Iterable
from urllib.parse import urljoin, urlparse
from urllib.request import Request, urlopen

SCHEMA_VERSION = "nextjs_cve_2025_29927_detector/0.1"
PROBE_HEADER_NAME = "x-middleware-subrequest"
PROBE_HEADER_VALUE = "middleware:middleware:middleware:middleware:middleware"
ALLOWED_METHODS = {"GET", "HEAD"}
MAX_TIMEOUT_SECONDS = 5.0
MAX_PATHS = 25


@dataclass(frozen=True)
class HttpObservation:
    """Small response observation; body content is never serialized."""

    status: int
    headers: dict[str, str]
    body: bytes = b""


def _normalize_method(method: str) -> str:
    normalized = method.upper().strip()
    if normalized not in ALLOWED_METHODS:
        raise ValueError("Only GET/HEAD methods are supported")
    return normalized


def _normalize_timeout(timeout: float) -> float:
    value = float(timeout)
    if value <= 0 or value > MAX_TIMEOUT_SECONDS:
        raise ValueError(f"timeout must be > 0 and <= {MAX_TIMEOUT_SECONDS:g} seconds")
    return value


def _undo_git_bash_path_conversion(path: str) -> str:
    """Recover `/foo` arguments that Git-Bash may pass as `C:/Program Files/Git/foo`."""

    marker = ":/Program Files/Git/"
    if marker in path:
        return "/" + path.split(marker, 1)[1].lstrip("/")
    return path


def normalize_paths(paths: Iterable[str]) -> list[str]:
    """Keep same-origin relative paths only, de-duplicated, capped."""

    normalized: list[str] = []
    seen: set[str] = set()
    for raw in paths:
        path = _undo_git_bash_path_conversion((raw or "").strip())
        if not path:
            continue
        parsed = urlparse(path)
        if parsed.scheme or parsed.netloc:
            continue
        if not path.startswith("/"):
            path = "/" + path
        if path not in seen:
            normalized.append(path)
            seen.add(path)
        if len(normalized) >= MAX_PATHS:
            break
    return normalized


def build_plan(
    base_url: str,
    paths: Iterable[str],
    *,
    method: str = "GET",
    timeout: float = 3.0,
) -> dict:
    """Build an offline plan. This performs no network activity."""

    parsed_base = urlparse(base_url)
    if parsed_base.scheme not in {"http", "https"} or not parsed_base.netloc:
        raise ValueError("base_url must be an http(s) URL")
    safe_method = _normalize_method(method)
    safe_timeout = _normalize_timeout(timeout)
    safe_paths = normalize_paths(paths)
    if not safe_paths:
        raise ValueError("at least one relative path is required")

    return {
        "schema_version": SCHEMA_VERSION,
        "cve": "<specific-cve-id>",
        "run_mode": "plan_only",
        "network_enabled": False,
        "base_url": base_url.rstrip("/"),
        "method": safe_method,
        "timeout_seconds": safe_timeout,
        "paths": safe_paths,
        "requests_planned": len(safe_paths) * 2,
        "limits": {
            "max_paths": MAX_PATHS,
            "max_timeout_seconds": MAX_TIMEOUT_SECONDS,
            "methods": sorted(ALLOWED_METHODS),
        },
        "probe_header": {PROBE_HEADER_NAME: PROBE_HEADER_VALUE},
        "comparison": "baseline response vs probe response with x-middleware-subrequest header",
        "classification_language": "candidate indicators only; manual authorization and review required",
        "retains_response_bodies": False,
        "notes": [
            "No requests are sent unless --execute, --allow-network, and --authorized-target are all supplied.",
            "Response bodies are not written to output; only status, selected headers, and body_length are retained.",
        ],
    }


def _target_url(base_url: str, path: str) -> str:
    return urljoin(base_url.rstrip("/") + "/", path.lstrip("/"))


def default_fetcher(url: str, *, method: str, headers: dict[str, str], timeout: float) -> HttpObservation:
    request = Request(url, method=method, headers=headers)
    with urlopen(request, timeout=timeout) as response:  # noqa: S310 - explicit opt-in CLI path only
        body = response.read(1024)
        return HttpObservation(
            status=int(response.status),
            headers={str(k).lower(): str(v) for k, v in response.headers.items()},
            body=body,
        )


def _safe_observation(obs: HttpObservation) -> dict:
    selected_headers = {}
    for name in ("location", "content-type", "x-middleware-rewrite", "x-middleware-redirect"):
        if name in {k.lower() for k in obs.headers}:
            for key, value in obs.headers.items():
                if key.lower() == name:
                    selected_headers[name] = value[:200]
                    break
    return {
        "status": int(obs.status),
        "headers": selected_headers,
        "body_length": len(obs.body or b""),
    }


def _is_candidate_delta(baseline: HttpObservation, probe: HttpObservation) -> bool:
    baseline_status = int(baseline.status)
    probe_status = int(probe.status)
    guarded_baseline = baseline_status in {301, 302, 303, 307, 308, 401, 403}
    probe_allows = 200 <= probe_status < 300
    if guarded_baseline and probe_allows:
        return True

    baseline_location = next((v for k, v in baseline.headers.items() if k.lower() == "location"), "")
    probe_location = next((v for k, v in probe.headers.items() if k.lower() == "location"), "")
    if guarded_baseline and baseline_location and baseline_location != probe_location:
        return True
    return False


def detect(
    base_url: str,
    paths: Iterable[str],
    *,
    method: str = "GET",
    timeout: float = 3.0,
    fetcher: Callable[..., HttpObservation] | None = None,
    network_enabled: bool = False,
) -> dict:
    """Compare baseline and x-middleware-subrequest probe responses."""

    plan = build_plan(base_url, paths, method=method, timeout=timeout)
    active_fetcher = fetcher or default_fetcher
    findings: list[dict] = []
    observations: list[dict] = []

    for path in plan["paths"]:
        url = _target_url(plan["base_url"], path)
        baseline = active_fetcher(url, method=plan["method"], headers={}, timeout=plan["timeout_seconds"])
        probe = active_fetcher(
            url,
            method=plan["method"],
            headers={PROBE_HEADER_NAME: PROBE_HEADER_VALUE},
            timeout=plan["timeout_seconds"],
        )
        pair = {
            "path": path,
            "baseline": _safe_observation(baseline),
            "probe": _safe_observation(probe),
        }
        observations.append(pair)
        if _is_candidate_delta(baseline, probe):
            findings.append({
                "path": path,
                "classification": "candidate_middleware_bypass_indicator",
                "reason": "guarded baseline response changed to allowed or materially different probe response",
                "baseline": pair["baseline"],
                "probe": pair["probe"],
            })

    return {
        "schema_version": SCHEMA_VERSION,
        "cve": "<specific-cve-id>",
        "run_mode": "network_execute" if network_enabled else "offline_fixture",
        "network_enabled": bool(network_enabled),
        "base_url": plan["base_url"],
        "method": plan["method"],
        "timeout_seconds": plan["timeout_seconds"],
        "retains_response_bodies": False,
        "summary": {
            "paths_tested": len(plan["paths"]),
            "candidate_count": len(findings),
            "classification_language": "candidate only",
        },
        "findings": findings,
        "observations": observations,
    }


def _read_paths(args: argparse.Namespace) -> list[str]:
    values = list(args.path or [])
    if args.paths_file:
        values.extend(Path(args.paths_file).read_text(encoding="utf-8").splitlines())
    return values


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Offline-safe <specific-cve-id> candidate detector")
    parser.add_argument("--base-url", required=True)
    parser.add_argument("--path", action="append", default=[])
    parser.add_argument("--paths-file")
    parser.add_argument("--method", default="GET", choices=sorted(ALLOWED_METHODS))
    parser.add_argument("--timeout", type=float, default=3.0)
    parser.add_argument("--output", help="Write JSON result/plan to this path")
    parser.add_argument("--execute", action="store_true", help="Send requests; requires both safety flags")
    parser.add_argument("--allow-network", action="store_true", help="Explicit network opt-in")
    parser.add_argument("--authorized-target", action="store_true", help="Affirm target authorization")
    args = parser.parse_args(argv)

    try:
        paths = _read_paths(args)
        if args.execute:
            if not (args.allow_network and args.authorized_target):
                print(
                    "Refusing network execution: --execute requires --allow-network and --authorized-target.",
                    file=sys.stderr,
                )
                return 2
            result = detect(
                args.base_url,
                paths,
                method=args.method,
                timeout=args.timeout,
                network_enabled=True,
            )
        else:
            result = build_plan(args.base_url, paths, method=args.method, timeout=args.timeout)
    except Exception as exc:  # compact CLI artifact: report validation failures without traceback
        print(f"error: {exc}", file=sys.stderr)
        return 2

    rendered = json.dumps(result, indent=2, sort_keys=True)
    if args.output:
        Path(args.output).write_text(rendered + "\n", encoding="utf-8")
    else:
        print(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
