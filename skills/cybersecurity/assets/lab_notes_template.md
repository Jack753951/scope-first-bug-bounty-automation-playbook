> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Lab / Engagement Notebook Template

Copy this file each time you start a new box, room, or engagement.  
Suggested filename: `YYYY-MM-DD_<platform>_<target>.md` — e.g. `2026-05-08_HTB_Lame.md`.

---

## 1. Metadata
- **Date**:
- **Platform / target**: (HTB / THM / VulnHub / self-host / authorized engagement)
- **Difficulty**:
- **Target IP / URL**:
- **OS / main services**:
- **Estimated time / actual time**:
- **MITRE ATT&CK tactics covered**:

## 2. Reconnaissance

### Nmap
```
(top-line nmap -sC -sV output, trimmed)
```

### Open ports
| Port | Service | Version | Notes |
|------|---------|---------|-------|

### Other recon
- Subdomains / vhosts:
- Content discovery (ffuf / dirsearch / feroxbuster):
- OSINT / public info:

## 3. Kill Chain

For each step: hypothesis → action → result → next thought.

### Step 1 — Initial Access
- **Hypothesis**:
- **Action**:
  ```bash
  ```
- **Evidence**: (screenshot path or output)

### Step 2 — Foothold / User
- **How obtained**:
- **Useful credentials / tokens**:

### Step 3 — Privilege Escalation
- **Misconfig / CVE**:
- **Action**:
- **Evidence**:

## 4. Loot
- `user.txt`:
- `root.txt`:
- Other interesting files / hashes / secrets:

## 5. Lessons Learned (most valuable section)
- New tools / techniques:
- Stuck points (anything ≥ 30 min):
- Reusable commands or one-liners:
- Heuristic for next time you see service X:

## 6. Reusable automation snippets
```python
# Anything from this lab worth promoting into your toolkit
```

## 7. References
- Official writeup / 0xdf / IppSec:
- Related CVE:
- Background reading:

## 8. OWASP / CWE mapping
- CWE-XXX:
- OWASP category:
