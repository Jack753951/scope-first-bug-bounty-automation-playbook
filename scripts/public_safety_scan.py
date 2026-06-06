#!/usr/bin/env python3
from __future__ import annotations
import re, sys
from pathlib import Path

PATTERNS = {
  "private_owner_path": re.compile(r"C:\\\\Users\\\\Owner|/c/Users/Owner|Desktop\\\\hacking2?|Desktop/hacking2?|C:/Users/Owner", re.I),
  "host_only_ip": re.compile(r"\b192\.168\.\d+\.\d+\b"),
  "private_vm_name": re.compile(r"\bkali-(aggressive|victim)[A-Za-z0-9_-]*\b", re.I),
  "researcher_alias": re.compile(r"\bOcro\b|wearehackerone\.com", re.I),
  "github_token": re.compile(r"gh[pousr]_[A-Za-z0-9_]+"),
  "api_key": re.compile(r"(?<![A-Za-z0-9])sk-[A-Za-z0-9_-]{20,}"),
  "private_key": re.compile(r"BEGIN (RSA |OPENSSH |EC |DSA )?PRIVATE KEY"),
  "program_or_domain": re.compile(r"\b(konghq|insomnia\.rest|coupang|fronthq|front\.com|tines|braze|gocardless|coveo|randstad|hubspot|indrive)\b", re.I),
  "advisory_id": re.compile(r"\bCVE-20\d{2}-\d{4,7}\b|\bGHSA-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{4}\b", re.I),
}
TEXT_SUFFIXES={".md",".py",".json",".jsonl",".yml",".yaml",".txt",".sh",".ps1",".csv",".xml",".html"}
SELF={"scripts/public_safety_scan.py"}

def main(root='.'):
    base=Path(root); hits=[]
    for path in sorted(base.rglob('*')):
        if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES: continue
        if '.git' in path.parts or '__pycache__' in path.parts: continue
        rel=path.relative_to(base).as_posix()
        if rel in SELF: continue
        for name,rx in PATTERNS.items():
            if rx.search(rel): hits.append((rel,0,name,'<path>'))
        text=path.read_text(encoding='utf-8', errors='ignore')
        for i,line in enumerate(text.splitlines(),1):
            for name,rx in PATTERNS.items():
                if rx.search(line): hits.append((rel,i,name,line.strip()[:220]))
    if hits:
        print('PUBLIC SAFETY SCAN FAILED')
        for h in hits[:500]: print(f'{h[0]}:{h[1]}: {h[2]}: {h[3]}')
        if len(hits)>500: print(f'... {len(hits)-500} more hits')
        return 1
    print('PUBLIC SAFETY SCAN PASS')
    return 0
if __name__=='__main__': raise SystemExit(main(sys.argv[1] if len(sys.argv)>1 else '.'))
