#!/usr/bin/env python3
"""
vuln_scan_integration.py — 漏洞掃描整合器

把 nuclei / nikto / whatweb 的輸出統一收進一份 JSON + Markdown。
sqlmap 不在這裡自動跑——它應該由人在確認過注入點之後手動呼叫，
而不是亂噴大量請求。本腳本只會偵測「可能可注入」的點供你後續手測。

合法使用提醒
============
僅供你自己擁有 / 授權 / 合法靶場 (DVWA / Juice Shop / WebGoat / HTB Box)。

使用方式
========
    python3 vuln_scan_integration.py https://target.lab -o ./vuln_out
    python3 vuln_scan_integration.py https://target.lab --skip-nuclei

外部工具：nuclei (projectdiscovery), nikto, whatweb
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import shutil
import subprocess
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Optional


SEVERITY_ORDER = {"critical": 0, "high": 1, "medium": 2, "low": 3, "info": 4, "unknown": 5}


@dataclass
class Finding:
    source: str           # "nuclei" | "nikto" | "whatweb"
    severity: str         # critical/high/medium/low/info/unknown
    title: str
    target: str
    description: str = ""
    reference: str = ""
    raw: str = ""

    def cvss_hint(self) -> str:
        """給定 severity 一個粗估的 CVSS 範圍，方便寫報告時起步。仍需人工修正。"""
        return {
            "critical": "9.0–10.0",
            "high": "7.0–8.9",
            "medium": "4.0–6.9",
            "low": "0.1–3.9",
            "info": "N/A (informational)",
            "unknown": "TBD",
        }.get(self.severity, "TBD")


@dataclass
class ScanResult:
    target: str
    timestamp: str
    findings: list = field(default_factory=list)  # type: list[Finding]
    errors: list = field(default_factory=list)
    tools_used: list = field(default_factory=list)


# ------------------------------------------------------------------
# 工具偵測 / 子程序
# ------------------------------------------------------------------

def have(tool: str) -> bool:
    return shutil.which(tool) is not None


def run(cmd: list[str], timeout: int = 1800) -> tuple[int, str, str]:
    try:
        proc = subprocess.run(
            cmd, capture_output=True, text=True, timeout=timeout, check=False
        )
        return proc.returncode, proc.stdout, proc.stderr
    except subprocess.TimeoutExpired:
        return -1, "", f"Timeout: {' '.join(cmd)}"
    except FileNotFoundError as e:
        return -1, "", str(e)


# ------------------------------------------------------------------
# Nuclei
# ------------------------------------------------------------------

def scan_nuclei(target: str, result: ScanResult, severity: str = "low,medium,high,critical") -> None:
    if not have("nuclei"):
        result.errors.append("nuclei 未安裝；安裝：go install -v github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest")
        return
    result.tools_used.append("nuclei")

    cmd = [
        "nuclei",
        "-u", target,
        "-severity", severity,
        "-jsonl",
        "-silent",
        "-disable-update-check",
    ]
    rc, out, err = run(cmd, timeout=1800)
    if rc != 0 and not out:
        result.errors.append(f"nuclei rc={rc}: {err.strip()[:200]}")
        return

    for line in out.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            continue
        info = obj.get("info", {})
        result.findings.append(Finding(
            source="nuclei",
            severity=(info.get("severity") or "unknown").lower(),
            title=info.get("name") or obj.get("template-id", "unknown"),
            target=obj.get("matched-at") or obj.get("host") or target,
            description=info.get("description", ""),
            reference=", ".join(info.get("reference", []) or []),
            raw=line[:1000],
        ))


# ------------------------------------------------------------------
# Nikto
# ------------------------------------------------------------------

def scan_nikto(target: str, result: ScanResult) -> None:
    if not have("nikto"):
        result.errors.append("nikto 未安裝（apt install nikto）")
        return
    result.tools_used.append("nikto")

    out_json = f"/tmp/nikto_{dt.datetime.now().strftime('%H%M%S')}.json"
    cmd = ["nikto", "-h", target, "-Format", "json", "-o", out_json, "-ask", "no"]
    rc, _, err = run(cmd, timeout=1800)
    if rc != 0:
        result.errors.append(f"nikto rc={rc}: {err.strip()[:200]}")

    p = Path(out_json)
    if not p.exists():
        return
    try:
        data = json.loads(p.read_text(errors="ignore"))
    except json.JSONDecodeError:
        return

    vulns = data.get("vulnerabilities", []) if isinstance(data, dict) else []
    for v in vulns:
        # nikto 沒給 severity，這裡依關鍵字粗略對應，仍需人工調整
        msg = (v.get("msg") or "").lower()
        if any(k in msg for k in ["xss", "sql", "rce", "execute", "lfi", "rfi"]):
            sev = "high"
        elif any(k in msg for k in ["disclos", "leak", "default", "directory"]):
            sev = "medium"
        elif "header" in msg or "missing" in msg:
            sev = "low"
        else:
            sev = "info"

        result.findings.append(Finding(
            source="nikto",
            severity=sev,
            title=v.get("msg", "Nikto finding")[:120],
            target=v.get("url") or target,
            description=v.get("msg", ""),
            reference=v.get("references", "") or v.get("OSVDB", ""),
            raw=json.dumps(v)[:1000],
        ))


# ------------------------------------------------------------------
# WhatWeb（指紋識別，提供脈絡）
# ------------------------------------------------------------------

def scan_whatweb(target: str, result: ScanResult) -> None:
    if not have("whatweb"):
        return  # whatweb 是輔助性工具，沒裝就跳過
    result.tools_used.append("whatweb")

    cmd = ["whatweb", "-a", "3", "--log-json=-", target]
    rc, out, err = run(cmd, timeout=180)
    if rc != 0:
        result.errors.append(f"whatweb rc={rc}: {err.strip()[:120]}")
        return

    for line in out.splitlines():
        line = line.strip()
        if not line.startswith("{"):
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            continue
        plugins = obj.get("plugins", {})
        names = ", ".join(sorted(plugins.keys()))
        result.findings.append(Finding(
            source="whatweb",
            severity="info",
            title=f"Tech fingerprint: {names[:120]}",
            target=obj.get("target", target),
            description=f"WhatWeb 偵測到的技術堆疊。HTTP {obj.get('http_status', '')}",
            raw=json.dumps(plugins)[:1000],
        ))


# ------------------------------------------------------------------
# 報告
# ------------------------------------------------------------------

def to_markdown(r: ScanResult) -> str:
    sorted_findings = sorted(
        r.findings,
        key=lambda f: (SEVERITY_ORDER.get(f.severity, 99), f.source, f.title),
    )

    lines: list[str] = []
    lines.append(f"# Vulnerability Scan — {r.target}")
    lines.append(f"_Generated: {r.timestamp}_")
    lines.append(f"Tools: {', '.join(r.tools_used) or '(none)'}\n")

    # 嚴重度統計
    counts: dict[str, int] = {}
    for f in r.findings:
        counts[f.severity] = counts.get(f.severity, 0) + 1
    lines.append("## Summary by Severity\n")
    lines.append("| Severity | Count |")
    lines.append("|----------|-------|")
    for sev in ["critical", "high", "medium", "low", "info", "unknown"]:
        lines.append(f"| {sev} | {counts.get(sev, 0)} |")
    lines.append("")

    lines.append("## Findings\n")
    if not sorted_findings:
        lines.append("_(no findings)_\n")
    for i, f in enumerate(sorted_findings, 1):
        lines.append(f"### {i}. [{f.severity.upper()}] {f.title}")
        lines.append(f"- **Source**: {f.source}")
        lines.append(f"- **Target**: `{f.target}`")
        lines.append(f"- **CVSS hint**: {f.cvss_hint()}")
        if f.description:
            lines.append(f"- **Description**: {f.description}")
        if f.reference:
            lines.append(f"- **Reference**: {f.reference}")
        lines.append("")

    if r.errors:
        lines.append("## Errors\n")
        for e in r.errors:
            lines.append(f"- {e}")
        lines.append("")

    lines.append("---")
    lines.append("_All findings need human verification before being reported as confirmed vulnerabilities._")
    return "\n".join(lines)


# ------------------------------------------------------------------
# CLI
# ------------------------------------------------------------------

LEGAL_NOTICE = """\
================ LEGAL NOTICE ================
This script sends potentially intrusive HTTP requests. Run only against
targets you own or have explicit written authorization to test.
==============================================
"""


def main() -> int:
    parser = argparse.ArgumentParser(description="Vulnerability scan integrator")
    parser.add_argument("target", help="URL of the target, e.g. https://target.lab")
    parser.add_argument("-o", "--out", default="./vuln_out")
    parser.add_argument("--severity", default="low,medium,high,critical",
                        help="nuclei severity filter")
    parser.add_argument("--skip-nuclei", action="store_true")
    parser.add_argument("--skip-nikto", action="store_true")
    parser.add_argument("--skip-whatweb", action="store_true")
    parser.add_argument("--yes", action="store_true", help="跳過互動確認")
    args = parser.parse_args()

    print(LEGAL_NOTICE)
    if not args.yes:
        ans = input("Proceed? (yes/N) ").strip().lower()
        if ans != "yes":
            print("Aborted.")
            return 1

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    result = ScanResult(
        target=args.target,
        timestamp=dt.datetime.utcnow().isoformat() + "Z",
    )

    if not args.skip_whatweb:
        print("[*] WhatWeb fingerprinting ...")
        scan_whatweb(args.target, result)

    if not args.skip_nuclei:
        print(f"[*] Nuclei ({args.severity}) ...")
        scan_nuclei(args.target, result, severity=args.severity)

    if not args.skip_nikto:
        print("[*] Nikto ...")
        scan_nikto(args.target, result)

    json_path = out / "vuln_scan.json"
    json_path.write_text(json.dumps(
        {
            "target": result.target,
            "timestamp": result.timestamp,
            "tools_used": result.tools_used,
            "errors": result.errors,
            "findings": [asdict(f) for f in result.findings],
        },
        indent=2, ensure_ascii=False,
    ))

    md_path = out / "vuln_scan.md"
    md_path.write_text(to_markdown(result))

    print(f"[+] Done. Findings: {len(result.findings)}")
    print(f"    JSON     : {json_path}")
    print(f"    Markdown : {md_path}")
    if result.errors:
        print(f"    Warnings : {len(result.errors)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
