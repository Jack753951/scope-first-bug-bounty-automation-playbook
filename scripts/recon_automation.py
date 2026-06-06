#!/usr/bin/env python3
"""
recon_automation.py — 偵察自動化骨架

整合 whois / DNS / Nmap / 子網域列舉，輸出 JSON + Markdown 摘要。

合法使用提醒
============
本工具僅可用於：
  1. 你自己擁有的資產
  2. 已取得書面授權的目標
  3. 合法靶場（HackTheBox / TryHackMe / VulnHub / 公司 CTF）

對未授權目標執行掃描（即使只是 nmap）在多數司法管轄區屬違法行為。

使用方式
========
    python3 recon_automation.py example.com -o ./recon_out
    python3 recon_automation.py 10.10.10.5 --skip-subdomains

需要的外部工具（系統需先安裝）：
    nmap, whois, dig, subfinder（選用），amass（選用）

只用 Python 標準庫，沒有額外 pip 依賴。
"""

from __future__ import annotations

import argparse
import datetime as dt
import ipaddress
import json
import re
import shutil
import subprocess
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Optional


# ------------------------------------------------------------------
# 結果資料結構
# ------------------------------------------------------------------

@dataclass
class ReconResult:
    target: str
    target_type: str  # "ip" | "domain"
    timestamp: str
    whois: Optional[str] = None
    dns_records: dict = field(default_factory=dict)  # type: dict[str, list[str]]
    subdomains: list = field(default_factory=list)
    nmap_summary: list = field(default_factory=list)  # list of {"port", "proto", "service", "version"}
    nmap_raw: Optional[str] = None
    errors: list = field(default_factory=list)


# ------------------------------------------------------------------
# 小工具
# ------------------------------------------------------------------

def have(tool: str) -> bool:
    """檢查 PATH 中是否有該工具"""
    return shutil.which(tool) is not None


def run(cmd: list[str], timeout: int = 600) -> tuple[int, str, str]:
    """安全地呼叫子程序：回傳 (returncode, stdout, stderr)。永遠用 list 傳，避免 shell injection。"""
    try:
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
        return proc.returncode, proc.stdout, proc.stderr
    except subprocess.TimeoutExpired:
        return -1, "", f"Timeout after {timeout}s: {' '.join(cmd)}"
    except FileNotFoundError as e:
        return -1, "", f"Not found: {e}"


def is_ip(target: str) -> bool:
    try:
        ipaddress.ip_address(target)
        return True
    except ValueError:
        return False


# ------------------------------------------------------------------
# 各個偵察模組
# ------------------------------------------------------------------

def gather_whois(target: str, result: ReconResult) -> None:
    if not have("whois"):
        result.errors.append("whois 未安裝，跳過")
        return
    rc, out, err = run(["whois", target], timeout=60)
    if rc == 0 and out:
        # 取前 60 行避免太長
        result.whois = "\n".join(out.splitlines()[:60])
    else:
        result.errors.append(f"whois failed: {err.strip()[:200]}")


def gather_dns(target: str, result: ReconResult) -> None:
    if is_ip(target):
        return  # IP 不查 DNS

    if not have("dig"):
        result.errors.append("dig 未安裝，跳過 DNS")
        return

    record_types = ["A", "AAAA", "MX", "NS", "TXT", "SOA", "CNAME"]
    for rtype in record_types:
        rc, out, _ = run(["dig", "+short", target, rtype], timeout=15)
        if rc == 0 and out.strip():
            records = [line.strip() for line in out.splitlines() if line.strip()]
            if records:
                result.dns_records[rtype] = records


def gather_subdomains(target: str, result: ReconResult) -> None:
    if is_ip(target):
        return

    found: set[str] = set()

    # 1) crt.sh 經由 dig 反查 — 不需要外部工具但較粗糙；這裡示範用 subfinder
    if have("subfinder"):
        rc, out, err = run(["subfinder", "-d", target, "-silent"], timeout=180)
        if rc == 0:
            for line in out.splitlines():
                line = line.strip().lower()
                if line.endswith(target.lower()):
                    found.add(line)
        else:
            result.errors.append(f"subfinder failed: {err.strip()[:200]}")
    else:
        result.errors.append("subfinder 未安裝；建議：go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest")

    # 2) amass passive（如果裝了）
    if have("amass"):
        rc, out, _ = run(["amass", "enum", "-passive", "-d", target], timeout=300)
        if rc == 0:
            for line in out.splitlines():
                line = line.strip().lower()
                if line.endswith(target.lower()):
                    found.add(line)

    result.subdomains = sorted(found)


# nmap -oX 的最小解析（不依賴第三方套件）
NMAP_PORT_RE = re.compile(
    r'<port\s+protocol="(?P<proto>[^"]+)"\s+portid="(?P<port>\d+)">'
    r'.*?<state\s+state="(?P<state>[^"]+)"'
    r'(?:.*?<service\s+name="(?P<service>[^"]*)"'
    r'(?:[^/]*?product="(?P<product>[^"]*)")?'
    r'(?:[^/]*?version="(?P<version>[^"]*)")?'
    r')?',
    re.DOTALL,
)


def gather_nmap(target: str, result: ReconResult, mode: str = "default") -> None:
    if not have("nmap"):
        result.errors.append("nmap 未安裝，跳過 port scan")
        return

    out_xml = f"/tmp/recon_{target.replace('/', '_')}_{dt.datetime.now().strftime('%H%M%S')}.xml"
    if mode == "fast":
        cmd = ["nmap", "-T4", "-F", "-sV", "-oX", out_xml, target]
    elif mode == "full":
        cmd = ["nmap", "-T4", "-p-", "-sC", "-sV", "-oX", out_xml, target]
    else:  # default — 前 1000 + 服務指紋 + 預設腳本
        cmd = ["nmap", "-T4", "-sC", "-sV", "-oX", out_xml, target]

    rc, out, err = run(cmd, timeout=1800)
    if rc != 0:
        result.errors.append(f"nmap rc={rc}: {err.strip()[:200]}")
        return

    result.nmap_raw = out

    try:
        xml = Path(out_xml).read_text(errors="ignore")
    except FileNotFoundError:
        return

    for m in NMAP_PORT_RE.finditer(xml):
        if m.group("state") != "open":
            continue
        result.nmap_summary.append({
            "port": int(m.group("port")),
            "proto": m.group("proto"),
            "service": m.group("service") or "",
            "product": m.group("product") or "",
            "version": m.group("version") or "",
        })


# ------------------------------------------------------------------
# 報告輸出
# ------------------------------------------------------------------

def to_markdown(r: ReconResult) -> str:
    lines: list[str] = []
    lines.append(f"# Recon Report — {r.target}")
    lines.append(f"_Generated: {r.timestamp}_  Target type: `{r.target_type}`\n")

    lines.append("## 1. Open Ports / Services\n")
    if r.nmap_summary:
        lines.append("| Port | Proto | Service | Product | Version |")
        lines.append("|------|-------|---------|---------|---------|")
        for p in r.nmap_summary:
            lines.append(
                f"| {p['port']} | {p['proto']} | {p['service']} | {p['product']} | {p['version']} |"
            )
    else:
        lines.append("_(no open ports detected or nmap not run)_")
    lines.append("")

    if r.dns_records:
        lines.append("## 2. DNS Records\n")
        for rtype, records in r.dns_records.items():
            lines.append(f"**{rtype}**")
            for rec in records:
                lines.append(f"- `{rec}`")
            lines.append("")

    if r.subdomains:
        lines.append(f"## 3. Subdomains ({len(r.subdomains)})\n")
        for s in r.subdomains:
            lines.append(f"- `{s}`")
        lines.append("")

    if r.whois:
        lines.append("## 4. WHOIS (truncated)\n")
        lines.append("```")
        lines.append(r.whois)
        lines.append("```\n")

    if r.errors:
        lines.append("## 5. Errors / Warnings\n")
        for e in r.errors:
            lines.append(f"- {e}")
        lines.append("")

    lines.append("---")
    lines.append("_Reminder: only run on authorized targets._")
    return "\n".join(lines)


# ------------------------------------------------------------------
# CLI
# ------------------------------------------------------------------

LEGAL_NOTICE = """\
================ LEGAL NOTICE ================
This tool actively probes the target. By proceeding you confirm that you
have explicit written authorization to test the target, OR the target is
your own asset / a legal practice range (HTB, THM, VulnHub).
==============================================
"""


def main() -> int:
    parser = argparse.ArgumentParser(description="Reconnaissance automation")
    parser.add_argument("target", help="Domain or IP")
    parser.add_argument("-o", "--out", default="./recon_out", help="Output directory")
    parser.add_argument(
        "--nmap-mode",
        choices=["fast", "default", "full"],
        default="default",
        help="fast=top100, default=top1000+sc+sv, full=all 65535 (slow)",
    )
    parser.add_argument("--skip-subdomains", action="store_true")
    parser.add_argument("--skip-whois", action="store_true")
    parser.add_argument("--yes", action="store_true", help="跳過互動式法律確認")
    args = parser.parse_args()

    print(LEGAL_NOTICE)
    if not args.yes:
        ans = input("Proceed? (yes/N) ").strip().lower()
        if ans != "yes":
            print("Aborted.")
            return 1

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    result = ReconResult(
        target=args.target,
        target_type="ip" if is_ip(args.target) else "domain",
        timestamp=dt.datetime.utcnow().isoformat() + "Z",
    )

    print(f"[+] Target: {args.target} ({result.target_type})")

    if not args.skip_whois:
        print("[*] WHOIS ...")
        gather_whois(args.target, result)

    print("[*] DNS ...")
    gather_dns(args.target, result)

    if not args.skip_subdomains:
        print("[*] Subdomains ...")
        gather_subdomains(args.target, result)

    print(f"[*] Nmap ({args.nmap_mode}) ...")
    gather_nmap(args.target, result, mode=args.nmap_mode)

    # JSON
    json_path = out_dir / f"{args.target}.json"
    json_path.write_text(json.dumps(asdict(result), indent=2, ensure_ascii=False))
    # Markdown
    md_path = out_dir / f"{args.target}.md"
    md_path.write_text(to_markdown(result))

    print(f"[+] Done.")
    print(f"    JSON     : {json_path}")
    print(f"    Markdown : {md_path}")
    print(f"    Open ports: {len(result.nmap_summary)}, Subdomains: {len(result.subdomains)}")
    if result.errors:
        print(f"    Warnings : {len(result.errors)} (見 markdown §5)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
