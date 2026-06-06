#!/usr/bin/env python3
"""
recon_pipeline.py — subdomain recon → liveness probe → ready-to-scan target list.

Pipeline
--------
  1. Pull subdomains for a root domain from public Certificate Transparency
     logs via crt.sh (and optionally hackertarget.com as a fallback).
  2. Deduplicate + filter against an optional scope file (one pattern per line,
     supports wildcards like *.api.example.com).
  3. Async DNS resolution + HTTP(S) liveness check on port 80 / 443.
  4. Emit a plain target list (one URL per line) and a JSON report.
  5. Optional: pipe the live list straight into nginx_rift_scanner.py.

This script only enumerates and pokes for liveness. It does not exploit
anything. Even so — confirm every root domain you scan is in a program you
have written authorization for. CT-log enumeration is legal, but mass-probing
hosts you have no relationship with can still get you blocklisted.

Usage
-----
  python recon_pipeline.py -d example.com -o live.txt
  python recon_pipeline.py -d example.com --scope scope.txt --chain
  python recon_pipeline.py -d example.com --json recon.json -c 30

Dependencies
------------
  pip install aiohttp
"""

import argparse
import asyncio
import fnmatch
import json
import socket
import subprocess
import sys
from dataclasses import dataclass, asdict, field
from datetime import datetime, timezone
from typing import Optional

try:
    import aiohttp
except ImportError:
    sys.stderr.write("Missing dependency. Install with:  pip install aiohttp\n")
    sys.exit(1)


CRTSH_URL = "https://crt.sh/?q=%25.{domain}&output=json"
HACKERTARGET_URL = "https://api.hackertarget.com/hostsearch/?q={domain}"


@dataclass
class Host:
    hostname: str
    resolves: bool = False
    ip: Optional[str] = None
    http: Optional[int] = None        # status code on :80
    https: Optional[int] = None       # status code on :443
    server: Optional[str] = None      # Server header (https preferred)
    in_scope: bool = True
    sources: list = field(default_factory=list)


# ---------- Subdomain sources -------------------------------------------------

async def fetch_crtsh(session, domain):
    url = CRTSH_URL.format(domain=domain)
    try:
        async with session.get(url, timeout=aiohttp.ClientTimeout(total=30)) as r:
            if r.status != 200:
                return []
            data = await r.json(content_type=None)
            names = set()
            for entry in data:
                for n in (entry.get("name_value") or "").split("\n"):
                    n = n.strip().lower().lstrip("*.")
                    if n and "@" not in n:
                        names.add(n)
            return sorted(names)
    except Exception as e:
        sys.stderr.write(f"[crt.sh] {type(e).__name__}: {e}\n")
        return []


async def fetch_hackertarget(session, domain):
    url = HACKERTARGET_URL.format(domain=domain)
    try:
        async with session.get(url, timeout=aiohttp.ClientTimeout(total=20)) as r:
            if r.status != 200:
                return []
            text = await r.text()
            names = set()
            for line in text.splitlines():
                parts = line.split(",")
                if parts and "." in parts[0]:
                    names.add(parts[0].strip().lower())
            return sorted(names)
    except Exception as e:
        sys.stderr.write(f"[hackertarget] {type(e).__name__}: {e}\n")
        return []


# ---------- Scope filtering ---------------------------------------------------

def load_scope(path):
    if not path:
        return None
    with open(path) as f:
        return [ln.strip().lower() for ln in f if ln.strip() and not ln.lstrip().startswith("#")]


def in_scope(hostname, patterns):
    if patterns is None:
        return True
    return any(fnmatch.fnmatch(hostname, p) for p in patterns)


# ---------- DNS + liveness ----------------------------------------------------

async def resolve(hostname, loop):
    try:
        infos = await loop.getaddrinfo(hostname, None, type=socket.SOCK_STREAM)
        return infos[0][4][0] if infos else None
    except Exception:
        return None


async def probe_port(session, hostname, scheme):
    url = f"{scheme}://{hostname}/"
    try:
        async with session.get(
            url,
            timeout=aiohttp.ClientTimeout(total=8),
            allow_redirects=False,
            ssl=False,
        ) as r:
            return r.status, r.headers.get("Server")
    except Exception:
        return None, None


async def check_host(host, session, loop, sem):
    async with sem:
        host.ip = await resolve(host.hostname, loop)
        host.resolves = host.ip is not None
        if not host.resolves:
            return host
        https_status, https_server = await probe_port(session, host.hostname, "https")
        http_status, http_server = await probe_port(session, host.hostname, "http")
        host.https = https_status
        host.http = http_status
        host.server = https_server or http_server
        return host


# ---------- Main pipeline -----------------------------------------------------

async def run(domain, scope_patterns, concurrency, no_hackertarget):
    connector = aiohttp.TCPConnector(ssl=False, limit=concurrency)
    headers = {"User-Agent": "recon-pipeline/1.0 (+bug-bounty-research)"}
    loop = asyncio.get_running_loop()

    sys.stderr.write(f"[*] Enumerating subdomains for {domain}...\n")
    async with aiohttp.ClientSession(connector=connector, headers=headers) as session:
        crt = await fetch_crtsh(session, domain)
        ht = [] if no_hackertarget else await fetch_hackertarget(session, domain)

        all_names = {}
        for n in crt:
            all_names.setdefault(n, []).append("crt.sh")
        for n in ht:
            all_names.setdefault(n, []).append("hackertarget")

        sys.stderr.write(f"    crt.sh:       {len(crt)} unique names\n")
        sys.stderr.write(f"    hackertarget: {len(ht)} unique names\n")
        sys.stderr.write(f"    combined:     {len(all_names)} unique names\n")

        hosts = [
            Host(hostname=name,
                 in_scope=in_scope(name, scope_patterns),
                 sources=src)
            for name, src in all_names.items()
        ]

        in_scope_hosts = [h for h in hosts if h.in_scope]
        sys.stderr.write(f"    in scope:     {len(in_scope_hosts)}\n")

        sys.stderr.write(f"[*] Resolving + probing liveness (concurrency={concurrency})...\n")
        sem = asyncio.Semaphore(concurrency)
        await asyncio.gather(*(check_host(h, session, loop, sem) for h in in_scope_hosts))

    return hosts


def main():
    p = argparse.ArgumentParser(description="Subdomain recon + liveness pipeline for bug-bounty workflows.")
    p.add_argument("-d", "--domain", required=True, help="Root domain (e.g. example.com)")
    p.add_argument("-o", "--output", default="live_targets.txt",
                   help="Plain list of live URLs (default: live_targets.txt)")
    p.add_argument("--json", help="JSON report path")
    p.add_argument("--scope", help="Scope file: one pattern per line, supports * wildcards")
    p.add_argument("-c", "--concurrency", type=int, default=20)
    p.add_argument("--no-hackertarget", action="store_true",
                   help="Skip the hackertarget.com source (use only crt.sh)")
    p.add_argument("--chain", action="store_true",
                   help="After recon, pipe the live target list into nginx_rift_scanner.py")
    args = p.parse_args()

    scope = load_scope(args.scope)
    hosts = asyncio.run(run(args.domain, scope, args.concurrency, args.no_hackertarget))

    live = [h for h in hosts if h.in_scope and h.resolves and (h.http or h.https)]
    sys.stderr.write(f"[+] {len(live)} live hosts (resolved + responding on 80/443)\n")

    # Plain target list — prefer https where available
    with open(args.output, "w") as f:
        for h in live:
            scheme = "https" if h.https else "http"
            f.write(f"{scheme}://{h.hostname}\n")
    sys.stderr.write(f"[+] Live URL list -> {args.output}\n")

    if args.json:
        report = {
            "domain": args.domain,
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "scope_patterns": scope,
            "total_names": len(hosts),
            "in_scope": sum(1 for h in hosts if h.in_scope),
            "resolves": sum(1 for h in hosts if h.resolves),
            "live": len(live),
            "hosts": [asdict(h) for h in hosts],
        }
        with open(args.json, "w") as f:
            json.dump(report, f, indent=2)
        sys.stderr.write(f"[+] JSON report  -> {args.json}\n")

    if args.chain:
        scanner = (sys.path[0] or ".") + "/nginx_rift_scanner.py"
        sys.stderr.write(f"[*] Chaining into {scanner}...\n")
        try:
            subprocess.run(
                [sys.executable, scanner, "-f", args.output, "--vuln-only",
                 "-o", "rift_findings.json"],
                check=False,
            )
            sys.stderr.write("[+] Scanner findings -> rift_findings.json\n")
        except FileNotFoundError:
            sys.stderr.write("[!] nginx_rift_scanner.py not found next to this script.\n")


if __name__ == "__main__":
    main()
