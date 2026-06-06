> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Script Acquisition Wave 2

Date: 2026-05-22T01:59:41.128337+00:00
Root: `setting\local\tool_acquisition\wave2_20260522`

## Policy

- Download/acquisition only by default.
- Unknown exploit scripts are not executed until reviewed and bounded to authorized local lab.
- Target-touching execution stays on `<attacker-vm>`.

## Exploit-DB selected scripts

- ok: `setting\local\tool_acquisition\wave2_20260522\scripts\exploitdb\path_traversal\edb_37223.txt` from https://gitlab.com/exploit-database/exploitdb/-/raw/main/exploits/asp/webapps/37223.txt
  - Exploit-DB reference; desc=Acuity CMS 2.6.2 - '/admin/file_manager/browse.asp?path' Traversal Arbitrary File Access; date=; platform=asp; type=webapps
- ok: `setting\local\tool_acquisition\wave2_20260522\scripts\exploitdb\path_traversal\edb_35168.txt` from https://gitlab.com/exploit-database/exploitdb/-/raw/main/exploits/asp/webapps/35168.txt
  - Exploit-DB reference; desc=BlogEngine.NET 1.6 - Directory Traversal / Information Disclosure; date=; platform=asp; type=webapps
- ok: `setting\local\tool_acquisition\wave2_20260522\scripts\exploitdb\path_traversal\edb_47666.txt` from https://gitlab.com/exploit-database/exploitdb/-/raw/main/exploits/asp/webapps/47666.txt
  - Exploit-DB reference; desc=Crystal Live HTTP Server 6.01 - Directory Traversal; date=; platform=asp; type=webapps
- ok: `setting\local\tool_acquisition\wave2_20260522\scripts\exploitdb\path_traversal\edb_33700.txt` from https://gitlab.com/exploit-database/exploitdb/-/raw/main/exploits/asp/webapps/33700.txt
  - Exploit-DB reference; desc=DevExpress ASPxFileManager 10.2 < 13.2.8 - Directory Traversal; date=; platform=asp; type=webapps
- ok: `setting\local\tool_acquisition\wave2_20260522\scripts\exploitdb\path_traversal\edb_11212.txt` from https://gitlab.com/exploit-database/exploitdb/-/raw/main/exploits/asp/webapps/11212.txt
  - Exploit-DB reference; desc=eWebeditor - Directory Traversal; date=; platform=asp; type=webapps
- ok: `setting\local\tool_acquisition\wave2_20260522\scripts\exploitdb\file_upload\edb_14058.html` from https://gitlab.com/exploit-database/exploitdb/-/raw/main/exploits/aix/webapps/14058.html
  - Exploit-DB reference; desc=PHP-Nuke 8.2 - Arbitrary File Upload; date=; platform=aix; type=webapps
- ok: `setting\local\tool_acquisition\wave2_20260522\scripts\exploitdb\file_upload\edb_37504.py` from https://gitlab.com/exploit-database/exploitdb/-/raw/main/exploits/android/webapps/37504.py
  - Exploit-DB reference; desc=AirDroid - Arbitrary File Upload; date=; platform=android; type=webapps
- ok: `setting\local\tool_acquisition\wave2_20260522\scripts\exploitdb\file_upload\edb_51355.txt` from https://gitlab.com/exploit-database/exploitdb/-/raw/main/exploits/ashx/webapps/51355.txt
  - Exploit-DB reference; desc=Roxy Fileman 1.4.5 -  Arbitrary File Upload; date=; platform=ashx; type=webapps
- ok: `setting\local\tool_acquisition\wave2_20260522\scripts\exploitdb\file_upload\edb_8132.txt` from https://gitlab.com/exploit-database/exploitdb/-/raw/main/exploits/asp/webapps/8132.txt
  - Exploit-DB reference; desc=Access2asp - 'imageLibrar' Arbitrary File Upload; date=; platform=asp; type=webapps
- ok: `setting\local\tool_acquisition\wave2_20260522\scripts\exploitdb\file_upload\edb_15597.txt` from https://gitlab.com/exploit-database/exploitdb/-/raw/main/exploits/asp/webapps/15597.txt
  - Exploit-DB reference; desc=Acidcat CMS 3.3 - 'FCKeditor' Arbitrary File Upload; date=; platform=asp; type=webapps
- ok: `setting\local\tool_acquisition\wave2_20260522\scripts\exploitdb\xss\edb_43815.txt` from https://gitlab.com/exploit-database/exploitdb/-/raw/main/exploits/asp/webapps/43815.txt
  - Exploit-DB reference; desc=LiveWorld Multiple Products - Cross Site Scripting; date=; platform=asp; type=webapps
- ok: `setting\local\tool_acquisition\wave2_20260522\scripts\exploitdb\xss\edb_51055.txt` from https://gitlab.com/exploit-database/exploitdb/-/raw/main/exploits/asp/webapps/51055.txt
  - Exploit-DB reference; desc=Password Manager for IIS v2.0 - XSS; date=; platform=asp; type=webapps
- ok: `setting\local\tool_acquisition\wave2_20260522\scripts\exploitdb\xss\edb_48999.txt` from https://gitlab.com/exploit-database/exploitdb/-/raw/main/exploits/aspx/webapps/48999.txt
  - Exploit-DB reference; desc=BlogEngine 3.3.8 - 'Content' Stored XSS; date=; platform=aspx; type=webapps
- ok: `setting\local\tool_acquisition\wave2_20260522\scripts\exploitdb\xss\edb_51200.txt` from https://gitlab.com/exploit-database/exploitdb/-/raw/main/exploits/aspx/webapps/51200.txt
  - Exploit-DB reference; desc=ELSI Smart Floor V3.3.3 - Stored Cross-Site Scripting (XSS); date=; platform=aspx; type=webapps
- ok: `setting\local\tool_acquisition\wave2_20260522\scripts\exploitdb\xss\edb_51118.txt` from https://gitlab.com/exploit-database/exploitdb/-/raw/main/exploits/aspx/webapps/51118.txt
  - Exploit-DB reference; desc=ReQlogic v11.3 - Reflected Cross-Site Scripting (XSS); date=; platform=aspx; type=webapps
- ok: `setting\local\tool_acquisition\wave2_20260522\scripts\exploitdb\idor_auth\edb_47633.txt` from https://gitlab.com/exploit-database/exploitdb/-/raw/main/exploits/alpha/webapps/47633.txt
  - Exploit-DB reference; desc=Prima Access Control 2.3.35 - 'HwName' Persistent Cross-Site Scripting; date=; platform=alpha; type=webapps
- ok: `setting\local\tool_acquisition\wave2_20260522\scripts\exploitdb\idor_auth\edb_49266.py` from https://gitlab.com/exploit-database/exploitdb/-/raw/main/exploits/android/webapps/49266.py
  - Exploit-DB reference; desc=Magic Home Pro 1.5.1 - Authentication Bypass; date=; platform=android; type=webapps
- ok: `setting\local\tool_acquisition\wave2_20260522\scripts\exploitdb\idor_auth\edb_925.txt` from https://gitlab.com/exploit-database/exploitdb/-/raw/main/exploits/asp/webapps/925.txt
  - Exploit-DB reference; desc=ACNews 1.0 - Authentication Bypass; date=; platform=asp; type=webapps
- ok: `setting\local\tool_acquisition\wave2_20260522\scripts\exploitdb\idor_auth\edb_7273.txt` from https://gitlab.com/exploit-database/exploitdb/-/raw/main/exploits/asp/webapps/7273.txt
  - Exploit-DB reference; desc=Active Force Matrix 2 - Authentication Bypass; date=; platform=asp; type=webapps
- ok: `setting\local\tool_acquisition\wave2_20260522\scripts\exploitdb\idor_auth\edb_7278.txt` from https://gitlab.com/exploit-database/exploitdb/-/raw/main/exploits/asp/webapps/7278.txt
  - Exploit-DB reference; desc=Active Membership 2 - Authentication Bypass; date=; platform=asp; type=webapps
- ok: `setting\local\tool_acquisition\wave2_20260522\scripts\exploitdb\ssrf_xxe_deser\edb_46987.txt` from https://gitlab.com/exploit-database/exploitdb/-/raw/main/exploits/aspx/webapps/46987.txt
  - Exploit-DB reference; desc=Sitecore 8.x - Deserialization Remote Code Execution; date=; platform=aspx; type=webapps
- ok: `setting\local\tool_acquisition\wave2_20260522\scripts\exploitdb\ssrf_xxe_deser\edb_47793.txt` from https://gitlab.com/exploit-database/exploitdb/-/raw/main/exploits/aspx/webapps/47793.txt
  - Exploit-DB reference; desc=Telerik UI - Remote Code Execution via Insecure Deserialization; date=; platform=aspx; type=webapps
- ok: `setting\local\tool_acquisition\wave2_20260522\scripts\exploitdb\ssrf_xxe_deser\edb_50462.txt` from https://gitlab.com/exploit-database/exploitdb/-/raw/main/exploits/aspx/webapps/50462.txt
  - Exploit-DB reference; desc=Umbraco v8.14.1 - 'baseUrl' SSRF; date=; platform=aspx; type=webapps
- ok: `setting\local\tool_acquisition\wave2_20260522\scripts\exploitdb\ssrf_xxe_deser\edb_51869.txt` from https://gitlab.com/exploit-database/exploitdb/-/raw/main/exploits/go/webapps/51869.txt
  - Exploit-DB reference; desc=Ladder v0.0.21 - Server-side request forgery (SSRF); date=; platform=go; type=webapps
- ok: `setting\local\tool_acquisition\wave2_20260522\scripts\exploitdb\ssrf_xxe_deser\edb_51582.txt` from https://gitlab.com/exploit-database/exploitdb/-/raw/main/exploits/hardware/webapps/51582.txt
  - Exploit-DB reference; desc=Ateme TITAN File 3.9 - SSRF File Enumeration; date=; platform=hardware; type=webapps

## GitHub repositories

- ok: `setting\local\tool_acquisition\wave2_20260522\repos\ffuf` from https://github.com/ffuf/ffuf.git
  - purpose: content discovery / fuzzing baseline; already installed on Kali but source docs useful
- ok: `setting\local\tool_acquisition\wave2_20260522\repos\dalfox` from https://github.com/hahwul/dalfox.git
  - purpose: XSS scanner workflow/reference; run only against authorized lab
- ok: `setting\local\tool_acquisition\wave2_20260522\repos\Arjun` from https://github.com/s0md3v/Arjun.git
  - purpose: HTTP parameter discovery for API/XSS/access-control leads
- ok: `setting\local\tool_acquisition\wave2_20260522\repos\XSStrike` from https://github.com/s0md3v/XSStrike.git
  - purpose: XSS payload/workflow reference; review before execution
- ok: `setting\local\tool_acquisition\wave2_20260522\repos\jwt_tool` from https://github.com/ticarpi/jwt_tool.git
  - purpose: JWT analysis/tamper workflow for lab tokens only
- ok: `setting\local\tool_acquisition\wave2_20260522\repos\PayloadsAllTheThings` from https://github.com/swisskyrepo/PayloadsAllTheThings.git
  - purpose: payload reference; not executable target-touching by itself
- error: `setting\local\tool_acquisition\wave2_20260522\repos\SecLists` from https://github.com/danielmiessler/SecLists.git
  - purpose: wordlist/reference; use bounded subsets only

## Next usage

Prioritize these for the next Kali lab wave:

1. Arjun for bounded parameter discovery.
2. Dalfox/XSStrike only after browser/runtime proof criteria are scripted.
3. jwt_tool for local JWT analysis, not live abuse without a clear oracle.
4. Exploit-DB scripts as reference patterns; port safe pieces into lab-specific runners rather than running raw exploit code.
