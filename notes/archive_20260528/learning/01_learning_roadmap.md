> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Cybersecurity 學習路線（中階向滲透測試）

> 前提：所有實作練習只在自己擁有或有授權的系統 / 合法靶場（HTB、THM、VulnHub、PortSwigger Web Security Academy）進行。

---

## 階段一：底層基礎（2–4 週）

| 領域 | 關鍵主題 | 推薦資源 |
|------|----------|----------|
| Linux | 檔案系統、權限、bash、systemd、cron、iptables | OverTheWire Bandit、Linux Journey |
| 網路 | TCP/IP、三向交握、DNS、HTTP/HTTPS、TLS、ARP、子網路 | Practical Networking、Wireshark 實作 |
| 程式 | Python 標準庫、socket、requests、subprocess、argparse | Automate the Boring Stuff |
| 加解密 | 雜湊 vs 加密、對稱/非對稱、PKI、JWT 結構 | Cryptopals Set 1–2 |

**檢核點**：能用 Python 寫一個多執行緒 TCP port scanner、能讀懂 Wireshark 抓到的 HTTPS 握手。

---

## 階段二：偵察與情資（1–2 週）

- 被動偵察：whois、DNS 紀錄、ASN、Shodan、censys、crt.sh、Wayback Machine
- 主動偵察：Nmap（-sS / -sV / -sC / -O / NSE）、masscan、subdomain enumeration
- OSINT：Google Dorks、theHarvester、SpiderFoot

**實作**：對自己擁有的網域跑一次完整偵察，把結果寫進報告範本的 §3「資訊蒐集」。

---

## 階段三：Web 應用滲透（4–6 週）— 大宗

依照 **OWASP Top 10 (2021)** 逐一打靶：

1. Broken Access Control（IDOR、強制瀏覽）
2. Cryptographic Failures
3. **Injection（SQLi、Command Injection、SSTI）**
4. Insecure Design
5. Security Misconfiguration
6. Vulnerable Components
7. Identification & Auth Failures（JWT、Session、暴力破解）
8. Software & Data Integrity（反序列化）
9. Logging Failures
10. **SSRF**

**主力工具**：Burp Suite Community（必學）、ffuf、sqlmap、nuclei

**最佳練習場**：PortSwigger Web Security Academy（免費、官方、課程式排版）

---

## 階段四：網路與系統滲透（4–6 週）

- 服務枚舉：SMB、SMTP、RDP、SSH、SNMP、LDAP、Kerberos
- 漏洞利用：searchsploit、Metasploit Framework、手寫 PoC
- 提權：LinPEAS、WinPEAS、GTFOBins、SUID/Capabilities、Kernel exploits
- 後滲透：pivoting（chisel、ligolo-ng）、credential dumping、persistence 概念
- AD：Kerberoasting、ASREPRoast、DCSync 概念（用 BloodHound 視覺化）

**靶場**：HackTheBox（從 Easy 起步）、TryHackMe Offensive Pathway。

---

## 階段五：報告與專業化（持續）

- CVSS 3.1 計分（自己手算過幾題再用 calculator）
- MITRE ATT&CK 對應戰術技巧
- 認證準備：eJPT → PNPT → OSCP（依預算與目標）
- 專業領域：雲端安全（AWS/GCP/Azure）、行動安全、ICS/OT、Red Team Ops

---

## 每週節奏（可剪貼）

- 週一/三/五：90 分鐘技術學習（一個主題）
- 週二/四：60 分鐘打 PortSwigger 或 THM 房
- 週六：3 小時打 HTB 一台機器，全程錄筆記
- 週日：整理本週筆記、把學到的東西寫成自動化片段

---

## 重要原則

1. **不要跳過筆記**——每打完一個靶就照「實驗筆記模板」記一份。
2. **報告比攻擊更重要**——能讓客戶理解風險的人才有商業價值。
3. **法律先行**——`nmap` 一個沒授權的目標就足以惹官司。
4. **理解優於工具**——sqlmap 點兩下能打的東西，要先能用 Burp Repeater 手做。
