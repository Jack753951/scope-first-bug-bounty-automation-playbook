> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# External vulnerability intelligence sources for lab bundles

Generated: 2026-05-22 08:40:12

## Retention rule
Keep bundles when they are useful, not only when they achieve full target control or file read. Valid statuses: `verified-impact`, `valuable-candidate`, `attempted-not-verified`, `blocked/deferred`, and `reference-only` for intelligence that requires a different target/component.

## Sources added
- CISA KEV: already mirrored in `cves/cisa_kev_catalog_latest.json`.
- NVD recent modified API: `https://services.nvd.nist.gov/rest/json/cves/2.0?lastModStartDate=2026-05-15T00%3A40%3A12.000Z&lastModEndDate=2026-05-22T00%3A40%3A12.000Z&resultsPerPage=200` -> `cves/nvd_recent_modified_20260522.json`
- Exploit-DB files CSV: `https://gitlab.com/exploit-database/exploitdb/-/raw/main/files_exploits.csv` -> `cves/exploitdb_files_exploits_20260522.csv`
- GitHub repository search for PoC/lab/tooling patterns -> `cves/github_security_lab_repo_search_20260522.json`
- HTB/training labs: use as pattern taxonomy/training calibration; do not rely on public writeups unless explicitly in assisted mode.

## NVD recent pattern matches
Total NVD results fetched: 200; matched pattern rows: 142
| CVE | Patterns | Description |
|---|---|---|
| <specific-cve-id> | rce | Prototype pollution vulnerability in 'deephas' versions 1.0.0 through 1.0.5 allows attacker to cause a denial of service and may lead to remote code execution. |
| <specific-cve-id> | path_traversal_file_read | A path traversal vulnerability on Pardus Software Center's "extractArchive" function could allow anyone on the same network to do a man-in-the-middle and write files on the system. |
| <specific-cve-id> | rce | Microsoft Word Remote Code Execution Vulnerability |
| <specific-cve-id> | path_traversal_file_read | Visual Basic for Applications Information Disclosure Vulnerability |
| <specific-cve-id> | rce | Microsoft Excel Remote Code Execution Vulnerability |
| <specific-cve-id> | rce | Microsoft Office Graphics Remote Code Execution Vulnerability |
| <specific-cve-id> | rce | Microsoft Office Remote Code Execution Vulnerability |
| <specific-cve-id> | rce | Microsoft Excel Remote Code Execution Vulnerability |
| <specific-cve-id> | rce | Microsoft Office Visio Remote Code Execution Vulnerability |
| <specific-cve-id> | rce | Microsoft Office Visio Remote Code Execution Vulnerability |
| <specific-cve-id> | rce | Microsoft Office Visio Remote Code Execution Vulnerability |
| <specific-cve-id> | rce | Microsoft Excel Remote Code Execution Vulnerability |
| <specific-cve-id> | rce | Microsoft Excel Remote Code Execution Vulnerability |
| <specific-cve-id> | path_traversal_file_read | Windows Graphics Component Information Disclosure Vulnerability |
| <specific-cve-id> | rce | Microsoft Excel Remote Code Execution Vulnerability |
| <specific-cve-id> | xss | Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in NetDataSoft DivvyDrive allows Stored XSS.

This issue affects DivvyDrive: from unspecified before v.4.6.2.0. |
| <specific-cve-id> | injection_sqli_command_template | Inavitas Solar Log product has an unauthenticated SQL Injection vulnerability. |
| <specific-cve-id> | auth_access_control | Netmaker makes networks with WireGuard. Prior to version 0.15.1, Improper Authorization functions lead to non-privileged users running privileged API calls. If someone adds users to the Netmaker platform who do not have  |
| <specific-cve-id> | injection_sqli_command_template | Kayrasoft product before version 2 has an unauthenticated SQL Injection vulnerability. This is fixed in version 2. |
| <specific-cve-id> | injection_sqli_command_template | Database Software Accreditation Tracking/Presentation Module product before version 2 has an unauthenticated SQL Injection vulnerability. This is fixed in version 2. |
| <specific-cve-id> | injection_sqli_command_template | The library automation system product KOHA developed by Parantez Teknoloji before version 19.05.03 has an unauthenticated SQL Injection vulnerability. This has been fixed in the version 19.05.03.01. |
| <specific-cve-id> | path_traversal_file_read | The Identity and Directory Management System developed by Çekino Bilgi Teknolojileri before version 2.1.25 has an unauthenticated Path traversal vulnerability. This has been fixed in the version 2.1.25 |
| <specific-cve-id> | xss | University Library Automation System developed by Yordam Bilgi Teknolojileri before version 19.2 has an unauthenticated Reflected XSS vulnerability. This has been fixed in the version 19.2 |
| <specific-cve-id> | path_traversal_file_read | Yordam Library Information Document Automation product before version 19.02 has an unauthenticated Information disclosure vulnerability. |
| <specific-cve-id> | xss | Yordam Library Information Document Automation product before version 19.02 has an unauthenticated reflected XSS vulnerability. |
| <specific-cve-id> | path_traversal_file_read | Microsoft Word Information Disclosure Vulnerability |
| <specific-cve-id> | rce | Microsoft Word Remote Code Execution Vulnerability |
| <specific-cve-id> | rce | Microsoft Excel Remote Code Execution Vulnerability |
| <specific-cve-id> | path_traversal_file_read | Microsoft Word Information Disclosure Vulnerability |
| <specific-cve-id> | path_traversal_file_read | Microsoft Excel Information Disclosure Vulnerability |
| <specific-cve-id> | rce | Microsoft Excel Remote Code Execution Vulnerability |
| <specific-cve-id> | rce | Microsoft Office Graphics Remote Code Execution Vulnerability |
| <specific-cve-id> | injection_sqli_command_template | SQL Injection vulnerability in Algan Software Prens Student Information System allows SQL Injection.

This issue affects Prens Student Information System: before 2.1.11. |
| <specific-cve-id> | injection_sqli_command_template, auth_access_control | Authorization Bypass Through User-Controlled Key vulnerability in Algan Software Prens Student Information System allows Object Relational Mapping Injection.

This issue affects Prens Student Information System: before 2 |
| <specific-cve-id> | rce | Microsoft Office Visio Remote Code Execution Vulnerability |
| <specific-cve-id> | rce | Microsoft Office Visio Remote Code Execution Vulnerability |
| <specific-cve-id> | rce | Microsoft Office Visio Remote Code Execution Vulnerability |
| <specific-cve-id> | injection_sqli_command_template | Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection') vulnerability in GullsEye GullsEye terminal operating system allows SQL Injection.

This issue affects GullsEye terminal operating syst |
| <specific-cve-id> | injection_sqli_command_template | Call Center System developed by Bulutses Information Technologies before version 3.0 has an unauthenticated Sql Injection vulnerability. This has been fixed in the version 3.0 |
| <specific-cve-id> | path_traversal_file_read | Path Traversal vulnerability in Deytek Informatics FileOrbis File Management System allows Path Traversal.

This issue affects FileOrbis File Management System: from unspecified before 10.6.3. |

## Exploit-DB pattern rows sampled
Matched/sampled rows: 300
| EDB ID | Date | Platform | Type | Description |
|---|---|---|---|---|
| 10372 |  | aix | webapps | OPMANAGER - Blind SQL Injection / XPath Injection |
| 14058 |  | aix | webapps | PHP-Nuke 8.2 - Arbitrary File Upload |
| 35382 |  | android | dos | Android WAPPushManager - SQL Injection |
| 40876 |  | android | dos | Google Android - 'IOMXNodeInstance::enableNativeBuffers' Unchecked Index |
| 47157 |  | android | remote | Android 7 < 9 - Remote Code Execution |
| 42289 |  | android | remote | Australian Education App - Remote Code Execution |
| 42288 |  | android | remote | BestSafe Browser - Man In The Middle Remote Code Execution |
| 34088 |  | android | remote | Boat Browser 8.0/8.0.1 - Remote Code Execution |
| 42287 |  | android | remote | eVestigator Forensic PenTester - Man In The Middle Remote Code Execution |
| 40846 |  | android | remote | Google Android - 'BadKernel' Remote Code Execution |
| 38124 |  | android | remote | Google Android - 'Stagefright' Remote Code Execution |
| 38226 |  | android | remote | Google Android - libstagefright Integer Overflow Remote Code Execution |
| 15548 |  | android | remote | Google Android 2.0/2.1 - Use-After-Free Remote Code Execution on Webkit |
| 44415 |  | android | remote | LineageOS 14.1 Blueborne - Remote Code Execution |
| 35282 |  | android | remote | Samsung Galaxy KNOX Android Browser - Remote Code Execution (Metasploit) |
| 42349 |  | android | remote | SKILLS.com.au Industry App - Man In The Middle Remote Code Execution |
| 42350 |  | android | remote | Virtual Postage (VPA) - Man In The Middle Remote Code Execution |
| 47515 |  | android | remote | Whatsapp 2.19.216 - Remote Code Execution |
| 37504 |  | android | webapps | AirDroid - Arbitrary File Upload |
| 49266 |  | android | webapps | Magic Home Pro 1.5.1 - Authentication Bypass |
| 47722 |  | android | webapps | Mersive Solstice 2.8.0 - Remote Code Execution |
| 51355 |  | ashx | webapps | Roxy Fileman 1.4.5 -  Arbitrary File Upload |
| 12527 |  | asp | dos | Administrador de Contenidos - Admin Authentication Bypass |
| 29077 |  | asp | webapps | 20/20 Applications Data Shed 1.0 - 'f-email.asp?itemID' SQL Injection |
| 29078 |  | asp | webapps | 20/20 Applications Data Shed 1.0 - 'listings.asp' Multiple SQL Injections |
| 29075 |  | asp | webapps | 20/20 Auto Gallery 3.2 - Multiple SQL Injections |
| 28985 |  | asp | webapps | 20/20 Real Estate 3.2 - 'listings.asp' SQL Injection |
| 29074 |  | asp | webapps | 20/20 Real Estate 3.2 - Multiple SQL Injections |
| 29084 |  | asp | webapps | A-Cart Pro 2.0 - 'product.asp?ProductID' SQL Injection |
| 26747 |  | asp | webapps | A-FAQ 1.0 - 'faqDsp.asp?catcode' SQL Injection |
| 26746 |  | asp | webapps | A-FAQ 1.0 - 'faqDspItem.asp?faqid' SQL Injection |
| 32898 |  | asp | webapps | Absolute Form Processor XE 1.5 - 'login.asp' SQL Injection |
| 3493 |  | asp | webapps | Absolute Image Gallery 2.0 - 'gallery.asp?categoryId' SQL Injection |
| 30842 |  | asp | webapps | Absolute News Manager .NET 5.1 - 'xlaabsolutenm.aspx' Multiple SQL Injections |
| 6731 |  | asp | webapps | Absolute Poll Manager XE 4.1 - 'xlacomments.asp' SQL Injection |
| 10582 |  | asp | webapps | Absolute Shopping Cart - SQL Injection |
| 8132 |  | asp | webapps | Access2asp - 'imageLibrar' Arbitrary File Upload |
| 26873 |  | asp | webapps | Acidcat CMS 2.1.13 - 'ID' SQL Injection |
| 15597 |  | asp | webapps | Acidcat CMS 3.3 - 'FCKeditor' Arbitrary File Upload |
| 925 |  | asp | webapps | ACNews 1.0 - Authentication Bypass |

## GitHub repo search samples
| Query | Repo | Stars | Notes |
|---|---|---:|---|
| juice shop exploit lab | [cchopin/owasp-labs-juiceshop](https://github.com/cchopin/owasp-labs-juiceshop) | 3 | Educational portfolio demonstrating common web vulnerabilities using OWASP Juice Shop. Includes guided examples of OWASP Top 10 flaws (XSS, SQLi, IDOR, CSRF) wi |
| juice shop exploit lab | [ATK-007/advanced-web-exploitation-lab](https://github.com/ATK-007/advanced-web-exploitation-lab) | 1 | Automated Kali Linux and OWASP Juice Shop Web Exploitation Lab |
| juice shop exploit lab | [adremmy/Mega-hacking-lab](https://github.com/adremmy/Mega-hacking-lab) | 0 | Mega Hacking lab – Juice Shop SQLi and BeEF browser exploitation |
| juice shop exploit lab | [karirujoe/owasp-juice-shop-web-pentest-lab](https://github.com/karirujoe/owasp-juice-shop-web-pentest-lab) | 0 | Web penetration testing lab using OWASP Juice Shop. Includes exploitation of XSS, SQL Injection, IDOR, and LFI vulnerabilities with structured writeups. |
| juice shop exploit lab | [madihaazamahmed-droid/cybersecurity-owasp-juice-shop](https://github.com/madihaazamahmed-droid/cybersecurity-owasp-juice-shop) | 0 | Cybersecurity lab report and practice documentation for DVWA and OWASP Juice Shop including vulnerability testing, exploitation techniques, and security learnin |
| OWASP Juice Shop XSS | [ScottContini/juiceshop_xss_example](https://github.com/ScottContini/juiceshop_xss_example) | 8 | An example heroku server implementation for exploiting an XSS in the OWASP Juice Shop |
| OWASP Juice Shop XSS | [anurag708989/Owasp_Juice_Shop_Tryhackme](https://github.com/anurag708989/Owasp_Juice_Shop_Tryhackme) | 4 | owasp juice chop ctf tryhackme walkthrough |
| OWASP Juice Shop XSS | [cchopin/owasp-labs-juiceshop](https://github.com/cchopin/owasp-labs-juiceshop) | 3 | Educational portfolio demonstrating common web vulnerabilities using OWASP Juice Shop. Includes guided examples of OWASP Top 10 flaws (XSS, SQLi, IDOR, CSRF) wi |
| OWASP Juice Shop XSS | [Aksin528/CodeSentinel_JuiceShopVulnLab](https://github.com/Aksin528/CodeSentinel_JuiceShopVulnLab) | 2 | This repository contains reports and demos for Task 1 of the CodeSentinel Internship, covering SQL Injection and XSS vulnerabilities identified in OWASP Juice S |
| OWASP Juice Shop XSS | [Suerine/owasp-juice-shop-pentest](https://github.com/Suerine/owasp-juice-shop-pentest) | 1 | Web application penetration testing lab — SQL injection, XSS, broken access control, and privilege escalation using BurpSuite |
| OWASP Juice Shop SQL injection | [Aksin528/CodeSentinel_JuiceShopVulnLab](https://github.com/Aksin528/CodeSentinel_JuiceShopVulnLab) | 2 | This repository contains reports and demos for Task 1 of the CodeSentinel Internship, covering SQL Injection and XSS vulnerabilities identified in OWASP Juice S |
| OWASP Juice Shop SQL injection | [devwaseem/OWASP-Juiceshop-SQL-Injection](https://github.com/devwaseem/OWASP-Juiceshop-SQL-Injection) | 1 | Exfilterate whole database of OWASP Juice shop using Error and Boolean based SQL injection  |
| OWASP Juice Shop SQL injection | [Suerine/owasp-juice-shop-pentest](https://github.com/Suerine/owasp-juice-shop-pentest) | 1 | Web application penetration testing lab — SQL injection, XSS, broken access control, and privilege escalation using BurpSuite |
| OWASP Juice Shop SQL injection | [Vignesh942/SQL-Injection-using-OWASP-Juice-Shop-and-Burp-Suite](https://github.com/Vignesh942/SQL-Injection-using-OWASP-Juice-Shop-and-Burp-Suite) | 1 |  |
| OWASP Juice Shop SQL injection | [abk00804/OWASP-Juice-Shop-Security-Assessment](https://github.com/abk00804/OWASP-Juice-Shop-Security-Assessment) | 1 | Web Application Security Testing & Hardening Project 🔐 OWASP Juice Shop / XSS / SQL Injection / bcrypt / Helmet / JWT / Winsto |
| file upload vulnerability lab | [Sfedfcv/redesigned-pancake](https://github.com/Sfedfcv/redesigned-pancake) | 234 | Skip to content github / docs Code Issues 80 Pull requests 35 Discussions Actions Projects 2 Security Insights Merge branch 'main' into 1862-Add-Travis-CI-migra |
| file upload vulnerability lab | [Don-No7/Hack-SQL](https://github.com/Don-No7/Hack-SQL) | 131 | -- -- File generated with SQLiteStudio v3.2.1 on Sun Feb 7 14:58:28 2021 -- -- Text encoding used: System -- PRAGMA foreign_keys = off; BEGIN TRANSACTION;  -- T |
| file upload vulnerability lab | [LunaM00n/File-Upload-Lab](https://github.com/LunaM00n/File-Upload-Lab) | 102 | Damn Vulnerable File Upload V 1.1 |
| file upload vulnerability lab | [bookworm52/EthicalHackingFromScratch](https://github.com/bookworm52/EthicalHackingFromScratch) | 95 | Welcome to my comprehensive course on python programming and ethical hacking. The course assumes you have NO prior knowledge in any of these topics, and by the  |
| file upload vulnerability lab | [udinparla/aa.py](https://github.com/udinparla/aa.py) | 26 | #!/usr/bin/env python import re import hashlib import Queue from random import choice import threading import time import urllib2 import sys import socket  try: |
| ssrf lab vulnerable app | [j0rd1s3rr4n0/FinSecure_Bank](https://github.com/j0rd1s3rr4n0/FinSecure_Bank) | 3 | 🏦 FinSecure Bank — Educational SSRF Demo Lab simulating a vulnerable fintech app to teach secure development and ethical hacking. |
| ssrf lab vulnerable app | [vivek12112/vulnerable-node-app](https://github.com/vivek12112/vulnerable-node-app) | 1 | A vulnerable web application lab built with Node.js, Express, and PostgreSQL. This educational sandbox demonstrates common flaws like XSS, SQL Injection, CSRF,  |
| ssrf lab vulnerable app | [HairyAnkle/vulnlab-webapp](https://github.com/HairyAnkle/vulnlab-webapp) | 0 | A realistic web app security lab: intentionally vulnerable features with PoCs, patches, and pentest-style reports (IDOR, XSS, CSRF, uploads, SSRF). |

## Lab bundle intake policy
- `verified-impact`: exploit flow reproduced on the authorized lab with concrete impact evidence.
- `valuable-candidate`: useful tool/payload/false-positive workflow retained even without full exploitation.
- `attempted-not-verified`: attempted with artifacts, but no runtime/impact proof.
- `blocked/deferred`: missing component/version/input surface/callback lab/auth state/tooling.
- `reference-only`: modern vulnerability intelligence that does not apply to the current target but informs future lab modules or fixtures.

## Next integration queue
1. Build a `vuln_intel_to_lab_bundle` index that links CISA KEV/NVD/Exploit-DB/GitHub items to OWASP/CWE and local bundle status.
2. Run Kali-side wave focused on KEV/NVD/Exploit-DB-derived path traversal and upload validation patterns.
3. Add browser-backed XSS proof workflow informed by HTB/PortSwigger/Juice Shop training patterns, without relying on public writeups unless assisted mode is declared.
