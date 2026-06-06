> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Cybersecurity Learning Paths — by Goal

Choose the path that matches the user's stated goal. Don't recommend across paths unless asked.

---

## Path A — Web Application Security (Bug Bounty / AppSec)

**0→3 months** (foundations)
- Linux + bash + HTTP fundamentals
- Burp Suite Community: proxy, repeater, intruder
- Read PortSwigger Web Security Academy theory pages

**3→9 months** (core)
- Complete every PortSwigger Academy lab — by far the highest-density free resource
- Books: *The Web Application Hacker's Handbook*, *Real-World Bug Hunting*
- Side reading: PortSwigger Research blog, <bug-bounty-platform> Hacktivity public reports

**9→18 months** (specialization)
- HackTheBox web challenges + boxes tagged "web"
- HTB CWEE or PortSwigger Burp Practitioner cert
- Submit on <bug-bounty-platform> / Bugcrowd / Intigriti — start with VDP programs (no bounty pressure)
- OSWE if budget allows

**Tools to master**: Burp Suite Pro, ffuf, sqlmap, nuclei (write your own templates), Caido.

---

## Path B — Internal Pentest / Red Team

**0→3 months**
- Linux + Windows fundamentals; AD basics; Active Directory home lab (DC + 2 hosts)
- Networking: TCP/IP, AD authentication flows (Kerberos, NTLM)

**3→9 months**
- TryHackMe Offensive Pathway → HackTheBox Easy boxes
- Watch IppSec writeups for retired boxes you got stuck on
- Cert: Security+ (foundational) or eJPT (cheap practical)

**9→18 months**
- HTB Medium/Hard; pro-labs (Dante, RastaLabs)
- TCM PNPT (cheap, AD focus, real report)
- OSCP

**18→36 months**
- CRTP → CRTE → CRTO (Zero-Point Security) for AD-heavy red team
- OSEP for evasion, OSEE for exploit dev (very advanced)

**Tools to master**: Nmap, Burp, BloodHound, NetExec/CrackMapExec, Mimikatz, Rubeus, Impacket, Sliver, Cobalt Strike (commercial).

---

## Path C — Blue Team / SOC / DFIR

**0→3 months**
- Networking + Linux + Windows internals (Sysmon, Event Logs, ETW)
- LetsDefend free; Blue Team Labs Online

**3→9 months**
- Splunk Fundamentals + Boss of the SOC dataset
- Sigma rule writing; YARA basics
- Cert: BTL1 (Security Blue Team)

**9→18 months**
- DFIR fundamentals: Volatility memory analysis, KAPE/Plaso for triage
- SANS SEC504 / GCIH (incident handling) — expensive but gold standard if employer pays
- Threat hunting: practice on Atomic Red Team replays

**18→36 months**
- SANS GCFA / FOR508 (advanced forensics)
- Detection engineering: Sigma → Splunk SPL / Elastic EQL

**Tools to master**: Splunk SPL, Elastic/Kibana, Sigma, YARA, Volatility 3, Velociraptor, Sysmon.

---

## Path D — Cloud Security

**0→3 months**
- Pick one cloud (start with AWS for breadth of jobs)
- AWS Solutions Architect Associate or Cloud Practitioner first — you can't secure what you don't understand

**3→9 months**
- AWS Security Specialty
- IAM deep dive: trust policies, permission boundaries, SCPs
- Practice: flaws.cloud, flaws2.cloud, CloudGoat

**9→18 months**
- Multi-cloud: Azure SC-200/300, GCP PSE
- Kubernetes security: CKS, kube-hunter, kube-bench
- IaC scanning: Checkov, tfsec, Trivy

**Tools**: Prowler, ScoutSuite, Pacu, Stratus Red Team (cloud attack emulation), kube-bench.

---

## Path E — Reverse Engineering / Exploit Dev

Niche. Only attempt after solid Linux + C + assembly basics.

**0→6 months**
- C programming + x86/x64 assembly
- *Hacking: The Art of Exploitation* (Erickson)
- pwn.college early modules; Microcorruption

**6→18 months**
- pwn.college full pwn track
- ROP, heap exploitation, kernel basics
- crackmes.one for reversing practice

**18+ months**
- OSED (Windows usermode exploit dev)
- OSEE (the hardest OffSec cert)
- Zero2Automated for malware analysis

---

## Universal recommendations (any path)

- **Notes are the moat**: Obsidian or Notion. Future you will thank you.
- **Public writing**: blog or GitHub writeups force clarity. Recruiters read these.
- **One CTF per month minimum**: keeps your skills honest.
- **Read CVE write-ups weekly**: GitHub Advisories, Project Zero.

---

## Time/cost reality check

| Cert | Approx. cost (USD) | Hours to prepare (with full-time job) |
|------|---------------------|--------------------------------------|
| Security+ | 400 | 80–120 |
| eJPT v2 | 250 | 60–100 |
| PNPT (TCM) | 400 | 100–150 |
| OSCP | 1600 | 400–800 |
| OSWE | 1700 | 300–500 |
| OSEP | 1700 | 300–500 |
| CRTP | 250 | 80–120 |
| CISSP | 750 | 200+ |

If money is tight: PortSwigger Academy + TryHackMe sub + HackTheBox sub + one cheap practical cert (eJPT or PNPT) gets you 80% of the way at <10% of OffSec cost.
