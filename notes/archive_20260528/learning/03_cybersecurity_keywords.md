> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Cybersecurity 關鍵字總覽（Cheat Sheet）

> 每一條都是一個值得花時間 Google / 動手實作的關鍵字。  
> 建議用法：每週挑 5–10 個還不熟的，逐一打開查、做筆記、找對應靶場練。

---

## 一、協議 Protocols

### 網路 / 傳輸層
`Ethernet` `ARP` `ICMP` `IPv4` `IPv6` `NAT` `PAT`  
`TCP (3-way handshake, RST, SYN flood, sequence prediction)` `UDP` `QUIC`  
`Routing` `BGP` `OSPF` `VLAN` `802.1Q` `STP` `LACP`

### 應用層
`HTTP/1.1` `HTTP/2` `HTTP/3` `HTTPS` `TLS 1.2` `TLS 1.3` `mTLS` `Certificate Transparency`  
`DNS` `A / AAAA / MX / TXT / CNAME / NS / SOA / SRV` `DNSSEC` `DoH` `DoT` `Zone transfer (AXFR)`  
`SSH` `SCP` `SFTP` `FTP / FTPS` `SMTP` `IMAP` `POP3` `DKIM` `SPF` `DMARC`  
`SMB / CIFS` `NetBIOS` `LDAP / LDAPS` `Kerberos (TGT, TGS, S4U)` `NTLM` `MS-RPC` `WMI` `WinRM`  
`SNMP v1/v2c/v3` `RDP` `VNC` `Telnet` `DHCP` `TFTP` `NTP` `RADIUS` `TACACS+` `IPMI`  
`MQTT` `AMQP` `Modbus` `S7comm` `BACnet`（OT/IoT）

### Web / API
`REST` `GraphQL` `WebSocket` `gRPC` `Webhook`  
`OAuth 2.0` `OIDC` `SAML 2.0` `JWT` `JWS` `JWE` `PASETO`  
`CORS` `CSP` `HSTS` `SameSite` `SubResource Integrity (SRI)` `Trusted Types`

### Active Directory / Windows
`Kerberos` `LDAP` `SMB` `LSASS` `SAM` `NTDS.dit` `GPO` `Trust relationships` `ADCS`  
`Pass-the-Hash` `Pass-the-Ticket` `Overpass-the-Hash` `Unconstrained / Constrained Delegation` `RBCD`

### 加密 / PKI
`AES (CBC, GCM, CTR)` `ChaCha20-Poly1305` `RSA` `ECC (P-256, Curve25519)` `Ed25519`  
`SHA-2` `SHA-3` `BLAKE2/3` `HMAC` `bcrypt` `scrypt` `Argon2id` `PBKDF2`  
`Diffie-Hellman` `ECDH` `X.509` `PKI` `OCSP` `CRL` `HSM` `KMS`

---

## 二、網站 Websites

### 學習 / 靶場
`TryHackMe` `HackTheBox` `HTB Academy` `PortSwigger Web Security Academy` `OffSec PWK / Proving Grounds`  
`PentesterLab` `RangeForce` `LetsDefend` `CyberDefenders` `Hack The Box CWEE` `RastaLabs` `Immersive Labs`

### CTF
`picoCTF` `CTFtime.org` `OverTheWire (Bandit / Natas / Narnia / Leviathan)` `Root-Me`  
`HackThisSite` `Cryptopals` `pwn.college` `Microcorruption` `Reversing.kr` `crackmes.one`

### 漏洞 / 情資
`cve.mitre.org` `nvd.nist.gov` `exploit-db.com` `vulners.com` `vuldb.com`  
`CISA KEV (known-exploited-vulnerabilities)` `GitHub Security Advisories` `Snyk Vulnerability DB`  
`Packet Storm` `0day.today`（謹慎）

### Cheat Sheets / 攻擊知識庫
`HackTricks` `book.hacktricks.xyz` `PayloadsAllTheThings` `GTFOBins` `LOLBAS` `LOLDrivers`  
`OWASP Cheat Sheet Series` `OWASP WSTG` `OWASP MASTG` `OWASP ASVS`  
`WADComs` `Internal All The Things` `Active Directory Exploitation Cheat Sheet` `revshells.com`

### 框架 / 標準
`OWASP Top 10 (Web / API / LLM / Mobile / IoT)` `MITRE ATT&CK` `MITRE D3FEND`  
`NIST CSF` `NIST 800-53 / 800-171` `CIS Controls v8` `ISO 27001 / 27002` `PCI-DSS` `SOC 2`  
`Cyber Kill Chain (Lockheed)` `Diamond Model`

### OSINT / 偵察搜尋引擎
`Shodan` `Censys` `ZoomEye` `FOFA` `BinaryEdge` `GreyNoise` `urlscan.io`  
`crt.sh` `DNSDumpster` `securitytrails.com` `viewdns.info` `Wayback Machine` `Google Dorks (GHDB)`  
`Hunter.io` `Have I Been Pwned`

### 工具線上版
`CyberChef` `dcode.fr` `regex101` `JWT.io` `crackstation.net` `hashes.com` `VirusTotal` `Joe Sandbox` `ANY.RUN`

### 新聞 / 研究
`Krebs on Security` `The Hacker News` `BleepingComputer` `Dark Reading` `The Record (Recorded Future)`  
`Google Project Zero blog` `PortSwigger Research` `NCC Group blog` `Trail of Bits blog`  
`Mandiant blog` `Microsoft MSRC` `IppSec YouTube` `John Hammond YouTube` `LiveOverflow`

### 賞金獵人 / 漏洞披露
`<bug-bounty-platform>` `Bugcrowd` `Intigriti` `YesWeHack` `Synack Red Team` `Open Bug Bounty`

---

## 三、技能 Skills

### 程式
`Python (sockets, requests, scapy, asyncio)` `Bash` `PowerShell` `JavaScript / TypeScript`  
`Go` `Rust 基礎` `C / C++（讀懂為主）` `Assembly x86 / x64 / ARM` `SQL` `Regex` `YAML` `JSON`

### 作業系統
**Linux**: `proc / sys filesystems` `systemd` `cron` `iptables / nftables` `LD_PRELOAD`  
`namespaces / cgroups (容器底層)` `capabilities` `SELinux / AppArmor` `auditd`  
**Windows**: `Registry` `Services` `Scheduled Tasks` `Tokens / SIDs` `Event Logs` `ETW`  
`PowerShell remoting` `WMI` `Sysmon`  
**macOS**: `launchd` `TCC` `Gatekeeper` `XProtect`

### 網路 / 抓包
`Wireshark` `tcpdump` `tshark` `Zeek (Bro)` `nmap NSE 撰寫` `scapy 封包工程` `mitmproxy`  
`Burp Suite (Pro)` `Caido` `OWASP ZAP`

### 容器 / 雲
`Docker (escape, --privileged 風險)` `Kubernetes (RBAC, etcd, kubelet API)` `Helm`  
`AWS IAM, S3, VPC, GuardDuty, CloudTrail` `Azure Entra ID, Sentinel` `GCP IAM, Asset Inventory`  
`Terraform / IaC scanning (tfsec, Checkov)`

### 反向 / 二進位
`Ghidra` `IDA Free / Pro` `Binary Ninja` `Cutter / radare2` `x64dbg` `gdb + pwndbg / GEF`  
`pwntools` `angr` `frida` `Hopper`（mac）

### 鑑識 / 事件回應
`Volatility 3` `Autopsy` `FTK Imager` `plaso / log2timeline` `KAPE` `Velociraptor`  
`Sigma rules` `YARA` `MITRE Caldera` `Atomic Red Team`

### 防禦 / 監控
`Splunk SPL` `Elastic / ELK / OpenSearch` `Wazuh` `Suricata` `Snort` `Zeek`  
`Falco` `osquery` `EDR concepts (CrowdStrike / SentinelOne / Defender for Endpoint)`  
`SOAR` `Threat Hunting`

---

## 四、技巧 Techniques

### Web 漏洞
`SQL Injection (Boolean, Time-based, UNION, Error-based, Blind, 2nd-order, NoSQLi)`  
`XSS (Reflected, Stored, DOM, mXSS, CSP bypass)`  
`CSRF` `SSRF (cloud metadata 169.254.169.254, gopher://, dict://)`  
`XXE (in-band, OOB, blind)` `LFI / RFI` `Path traversal` `File upload bypass`  
`SSTI (Jinja2, Twig, Freemarker, Velocity)` `Prototype Pollution`  
`IDOR / BOLA` `Mass Assignment` `Race Condition` `TOCTOU`  
`HTTP Request Smuggling (CL.TE, TE.CL, TE.TE, H2.CL)` `HTTP/2 desync` `Cache Poisoning`  
`JWT (alg=none, kid injection, jwk header, weak secret)` `OAuth (open redirect, state CSRF, PKCE downgrade)`  
`GraphQL (introspection, batching, alias DoS, field suggestion)`  
`CORS misconfig` `DNS Rebinding` `Web Cache Deception` `CRLF Injection` `Host Header Injection`

### 網路 / AD
`Port scanning evasion (-sS / -sU / -sN / -sF / -sX, decoys, fragmentation)`  
`ARP spoofing` `LLMNR / NBT-NS / mDNS poisoning (Responder)` `SMB Relay`  
`Kerberoasting` `ASREPRoast` `Silver / Golden / Diamond / Sapphire Ticket` `Skeleton Key`  
`Pass-the-Hash` `Pass-the-Ticket` `Overpass-the-Hash` `DCSync` `DCShadow`  
`AD CS abuse (ESC1–ESC15)` `BloodHound paths` `RBCD` `Constrained delegation abuse`  
`SOCKS pivoting (chisel, ligolo-ng, sshuttle, ssf)` `Port forwarding (ssh -L/-R/-D)`

### 提權
**Linux**: `SUID / SGID` `Capabilities (CAP_SYS_ADMIN, CAP_DAC_READ_SEARCH)`  
`sudo (env_keep, sudoedit, LD_PRELOAD, runas)` `cron job hijack` `Writable PATH` `Wildcard injection`  
`Kernel exploits (DirtyCow, DirtyPipe, OverlayFS, PwnKit)`  
**Windows**: `Token impersonation` `JuicyPotato / RoguePotato / GodPotato` `PrintNightmare`  
`Unquoted service path` `DLL Hijacking` `AlwaysInstallElevated` `Stored credentials`  
`UAC bypass (fodhelper, eventvwr, sdclt)`

### 二進位 / Pwn
`Stack buffer overflow` `ret2win` `ret2libc` `ROP / SROP / JOP` `Format String`  
`Heap (UAF, double free, tcache poisoning, fastbin attack, House of *)`  
`Integer overflow` `Race condition` `Side channel (timing, cache, Spectre/Meltdown 概念)`  
`ASLR / PIE / NX / RELRO / Stack Canary 與其繞過`

### 加密 / 協議攻擊
`Padding Oracle (POODLE, BEAST, Lucky13)` `Bleichenbacher` `Hash length extension`  
`ECB pattern leak` `IV reuse (GCM nonce reuse)` `Weak RNG` `LSB oracle`

### 紅隊 / OPSEC
`AMSI bypass` `ETW patching` `In-memory execution (reflective DLL, PEzor)`  
`C2 frameworks: Cobalt Strike, Sliver, Mythic, Havoc, Brute Ratel`  
`OPSEC: indicators (PID parent, named pipes, process injection IOCs)` `BOFs`

### 無線 / 行動
`WPA2 4-way handshake capture / hashcat -m 22000` `WPA3 Dragonblood`  
`Evil Twin` `KARMA` `Krack` `Bluetooth (BlueBorne, BLE pairing)`  
`Frida hooking (iOS/Android)` `Objection` `MobSF`

### 防禦面（Blue Team）
`Threat hunting hypotheses` `Sigma 規則撰寫` `YARA 規則撰寫`  
`Detection-as-Code` `Purple teaming` `Atomic Red Team replay`  
`Memory forensics (Volatility plugins: pslist, malfind, netscan, hivelist)`  
`Log correlation (Sysmon → Splunk / ELK)` `EDR evasion 偵測指標`

---

## 五、課程 / 認證 Courses & Certifications

### 完全免費 / 高 CP 入門
- `Google Cybersecurity Professional Certificate`（Coursera）
- `TryHackMe — Pre Security / Cyber Security 101`
- `TCM Security — Practical Ethical Hacker (PEH)`（雖付費但極便宜）
- `PortSwigger Web Security Academy`（免費完整 Web 課）
- `Cybrary Free Career Path`

### 入門認證
`CompTIA Security+` `Network+` `Linux+` `Cybersecurity Analyst (CySA+)` `(ISC)² CC`  
`eJPT v2 (INE)` `Microsoft SC-900`

### 中階滲透 / 紅隊
`OSCP (OffSec PEN-200)` `eCPPT / eWPT (INE)` `TCM PNPT` `HTB CPTS / CBBH`  
`PentesterLab Pro` `OSWP (wireless)` `CRTP (AD - Altered Security)` `CRTE`

### 進階紅隊 / Web / Exploit
`OSWE (OffSec WEB-300)` `OSEP (OffSec PEN-300)` `OSED (OffSec EXP-301)` `OSCE3`  
`CRTO / CRTO II (Zero-Point Security)` `HTB CWEE` `OSEE` `SANS SEC660 / SEC760`

### 防禦 / SOC / DFIR
`Blue Team Level 1 / 2 (Security Blue Team)` `LetsDefend Pro` `SANS SEC401 / SEC504`  
`SANS GCIH` `GCIA` `GCFA` `GREM (Reverse Engineering Malware)` `GNFA` `GCFE`

### 雲端
`AWS Security Specialty` `Azure SC-100 / SC-200 / SC-300 / AZ-500`  
`GCP Professional Cloud Security Engineer` `Certified Kubernetes Security Specialist (CKS)`  
`SANS SEC488 (Cloud)` `SANS SEC588 (Cloud Pentest)`

### 治理 / 管理 / 合規
`CISSP (8 domains)` `CISM` `CISA` `CRISC` `CCSP` `ISO 27001 Lead Implementer / Auditor`

### 必看書單（精選）
- `The Web Application Hacker's Handbook` (Stuttard & Pinto)
- `The Hacker Playbook 3` (Peter Kim)
- `RTFM: Red Team Field Manual` / `BTFM: Blue Team Field Manual`
- `The Tangled Web` (Michał Zalewski)
- `Practical Malware Analysis` (Sikorski & Honig)
- `Hacking: The Art of Exploitation` (Erickson)
- `Real-World Cryptography` (David Wong)
- `Tribe of Hackers Red/Blue Team` 系列

---

## 六、建議學習路徑（依關鍵字 milestone）

```
新手起步:
    Linux 基礎 → TCP/IP → Python → OWASP Top 10 → Burp Suite → TryHackMe
        ↓
入門認證:
    Security+ 或 eJPT
        ↓
打靶練習:
    PortSwigger Academy 全破 → HTB Easy → HTB Medium → CTF
        ↓
中階認證:
    OSCP 或 PNPT
        ↓
分流選擇:
    Web → OSWE / CWEE
    AD/Red Team → CRTP → CRTO → OSEP
    Cloud → AWS Security / Azure SC-200
    Blue/DFIR → BTL1 → GCFA / GCIH
    Exploit Dev → OSED → OSEE
```

---

## 七、每日習慣（建議）

`讀一篇 The Hacker News / BleepingComputer`  
`刷一題 PortSwigger Lab 或 HTB Challenge`  
`查一個 CVE 看它怎麼被利用`  
`記一份筆記到 Obsidian / Notion`  
`每週寫一支自動化小腳本`

---

> 完整掌握以上所有關鍵字大概需要 3–5 年。**不要焦慮**——選一條路線深耕，遇到不熟的就標記下來，週末補。能在一個領域做到深的人，比每個領域都半懂的人值錢得多。
