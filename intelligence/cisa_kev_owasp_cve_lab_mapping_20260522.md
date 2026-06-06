> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# CISA KEV to OWASP/local-lab candidate map

Generated: 2026-05-22 08:31:34
Source: https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json
Catalog title: CISA Catalog of Known Exploited Vulnerabilities; count: 1601

Purpose: use CISA KEV as an intelligence/backlog source for authorized local lab reproduction patterns. This does not mean the Juice Shop target has any specific product CVE. Product-specific CVEs are only used as pattern inspiration unless the matching component/version exists in the lab.

## Pattern buckets

### auth_access_control
| CVE | Vendor/Product | KEV name | Date added | Lab mapping |
|---|---|---|---|---|
| <specific-cve-id> | Cisco Catalyst SD-WAN | Cisco Catalyst SD-WAN Controller Authentication Bypass Vulnerability | 2026-05-14 | OWASP A01/A07 -> auth bypass/access control/privilege boundary bundles |
| <specific-cve-id> | Linux Kernel | Linux Kernel Incorrect Resource Transfer Between Spheres Vulnerability | 2026-05-01 | OWASP A01/A07 -> auth bypass/access control/privilege boundary bundles |
| <specific-cve-id> | WebPros cPanel & WHM and WP2 (WordPress Squared) | WebPros cPanel & WHM and WP2 (WordPress Squared) Missing Authentication for Critical Function Vulnerability | 2026-04-30 | OWASP A01/A07 -> auth bypass/access control/privilege boundary bundles |
| <specific-cve-id> | Microsoft Defender | Microsoft Defender Insufficient Granularity of Access Control Vulnerability | 2026-04-22 | OWASP A01/A07 -> auth bypass/access control/privilege boundary bundles |
| <specific-cve-id> | PaperCut NG/MF | PaperCut NG/MF Improper Authentication Vulnerability | 2026-04-20 | OWASP A01/A07 -> auth bypass/access control/privilege boundary bundles |
| <specific-cve-id> | Quest KACE Systems Management Appliance (SMA) | Quest KACE Systems Management Appliance (SMA) Improper Authentication Vulnerability | 2026-04-20 | OWASP A01/A07 -> auth bypass/access control/privilege boundary bundles |
| <specific-cve-id> | Microsoft Windows | Microsoft Windows Link Following Vulnerability | 2026-04-13 | OWASP A01/A07 -> auth bypass/access control/privilege boundary bundles |
| <specific-cve-id> | Fortinet FortiClient EMS | Fortinet FortiClient EMS Improper Access Control Vulnerability | 2026-04-06 | OWASP A01/A07 -> auth bypass/access control/privilege boundary bundles |

### deserialization
| CVE | Vendor/Product | KEV name | Date added | Lab mapping |
|---|---|---|---|---|
| <specific-cve-id> | Microsoft Exchange Server | Microsoft Exchange Server Deserialization of Untrusted Data Vulnerability | 2026-04-13 | OWASP A08 -> only if serialized-object input exists |
| <specific-cve-id> | Cisco Secure Firewall Management Center (FMC) | Cisco Secure Firewall Management Center (FMC) Software and Cisco Security Cloud Control (SCC) Firewall Management Deserialization of Untrusted Data Vulnerability | 2026-03-19 | OWASP A08 -> only if serialized-object input exists |
| <specific-cve-id> | Microsoft SharePoint | Microsoft SharePoint Deserialization of Untrusted Data Vulnerability | 2026-03-18 | OWASP A08 -> only if serialized-object input exists |
| <specific-cve-id> | SolarWinds Web Help Desk | SolarWinds Web Help Desk Deserialization of Untrusted Data Vulnerability | 2026-03-09 | OWASP A08 -> only if serialized-object input exists |
| <specific-cve-id> | Roundcube Webmail | RoundCube Webmail Deserialization of Untrusted Data Vulnerability | 2026-02-20 | OWASP A08 -> only if serialized-object input exists |
| <specific-cve-id> | SolarWinds Web Help Desk | SolarWinds Web Help Desk Deserialization of Untrusted Data Vulnerability | 2026-02-03 | OWASP A08 -> only if serialized-object input exists |
| <specific-cve-id> | Microsoft Windows | Microsoft Windows Server Update Service (WSUS) Deserialization of Untrusted Data Vulnerability | 2025-10-24 | OWASP A08 -> only if serialized-object input exists |
| <specific-cve-id> | Jenkins Jenkins | Jenkins Remote Code Execution Vulnerability | 2025-10-02 | OWASP A08 -> only if serialized-object input exists |

### exposed_admin_config
| CVE | Vendor/Product | KEV name | Date added | Lab mapping |
|---|---|---|---|---|
| <specific-cve-id> | Cisco Catalyst SD-WAN | Cisco Catalyst SD-WAN Controller Authentication Bypass Vulnerability | 2026-05-14 | OWASP A05 -> admin/config/docs/metrics exposure bundles |
| <specific-cve-id> | Cisco Catalyst SD-WAN Manger | Cisco Catalyst SD-WAN Manager Incorrect Use of Privileged APIs Vulnerability | 2026-04-20 | OWASP A05 -> admin/config/docs/metrics exposure bundles |
| <specific-cve-id> | Cisco Catalyst SD-WAN Manager | Cisco Catalyst SD-WAN Manager Exposure of Sensitive Information to an Unauthorized Actor Vulnerability | 2026-04-20 | OWASP A05 -> admin/config/docs/metrics exposure bundles |
| <specific-cve-id> | Cisco Catalyst SD-WAN Manager | Cisco Catalyst SD-WAN Manager Storing Passwords in a Recoverable Format Vulnerability | 2026-04-20 | OWASP A05 -> admin/config/docs/metrics exposure bundles |
| <specific-cve-id> | Wing FTP Server Wing FTP Server | Wing FTP Server Information Disclosure Vulnerability | 2026-03-16 | OWASP A05 -> admin/config/docs/metrics exposure bundles |
| <specific-cve-id> | Cisco SD-WAN | Cisco SD-WAN Path Traversal Vulnerability | 2026-02-25 | OWASP A05 -> admin/config/docs/metrics exposure bundles |
| <specific-cve-id> | Cisco Catalyst SD-WAN Controller and Manager | Cisco Catalyst SD-WAN Controller and Manager Authentication Bypass Vulnerability | 2026-02-25 | OWASP A05 -> admin/config/docs/metrics exposure bundles |
| <specific-cve-id> | Microsoft Windows | Microsoft Windows Information Disclosure Vulnerability | 2026-01-13 | OWASP A05 -> admin/config/docs/metrics exposure bundles |

### file_upload_file_write
| CVE | Vendor/Product | KEV name | Date added | Lab mapping |
|---|---|---|---|---|
| <specific-cve-id> | TeamT5 ThreatSonar Anti-Ransomware | TeamT5 ThreatSonar Anti-Ransomware Unrestricted Upload of File with Dangerous Type Vulnerability | 2026-02-17 | OWASP A01/A05/A08 -> upload marker/write/retrieval/extension validation bundles |
| <specific-cve-id> | SmarterTools SmarterMail | SmarterTools SmarterMail Unrestricted Upload of File with Dangerous Type Vulnerability | 2026-01-26 | OWASP A01/A05/A08 -> upload marker/write/retrieval/extension validation bundles |
| <specific-cve-id> | Sierra Wireless AirLink ALEOS | Sierra Wireless AirLink ALEOS Unrestricted Upload of File with Dangerous Type Vulnerability | 2025-12-12 | OWASP A01/A05/A08 -> upload marker/write/retrieval/extension validation bundles |
| <specific-cve-id> | OpenPLC ScadaBR | OpenPLC ScadaBR Unrestricted Upload of File with Dangerous Type Vulnerability | 2025-12-03 | OWASP A01/A05/A08 -> upload marker/write/retrieval/extension validation bundles |
| <specific-cve-id> | SAP NetWeaver | SAP NetWeaver Unrestricted File Upload Vulnerability | 2025-04-29 | OWASP A01/A05/A08 -> upload marker/write/retrieval/extension validation bundles |
| <specific-cve-id> | Advantive VeraCore | Advantive VeraCore Unrestricted File Upload Vulnerability | 2025-03-10 | OWASP A01/A05/A08 -> upload marker/write/retrieval/extension validation bundles |
| <specific-cve-id> | Cleo Multiple Products | Cleo Multiple Products Unauthenticated File Upload Vulnerability | 2024-12-17 | OWASP A01/A05/A08 -> upload marker/write/retrieval/extension validation bundles |
| <specific-cve-id> | Cleo Multiple Products | Cleo Multiple Products Unrestricted File Upload Vulnerability | 2024-12-13 | OWASP A01/A05/A08 -> upload marker/write/retrieval/extension validation bundles |

### injection_sqli_command_template
| CVE | Vendor/Product | KEV name | Date added | Lab mapping |
|---|---|---|---|---|
| <specific-cve-id> | BerriAI LiteLLM | BerriAI LiteLLM SQL Injection Vulnerability | 2026-05-08 | OWASP A03 Injection -> SQLi/auth-bypass, command/template injection labs if sink exists |
| <specific-cve-id> | D-Link DIR-823X | D-Link DIR-823X Command Injection Vulnerability | 2026-04-24 | OWASP A03 Injection -> SQLi/auth-bypass, command/template injection labs if sink exists |
| <specific-cve-id> | Apache ActiveMQ | Apache ActiveMQ Improper Input Validation Vulnerability | 2026-04-16 | OWASP A03 Injection -> SQLi/auth-bypass, command/template injection labs if sink exists |
| <specific-cve-id> | Fortinet FortiClient EMS | Fortinet FortiClient EMS SQL Injection Vulnerability | 2026-04-13 | OWASP A03 Injection -> SQLi/auth-bypass, command/template injection labs if sink exists |
| <specific-cve-id> | Ivanti Endpoint Manager Mobile (EPMM) | Ivanti Endpoint Manager Mobile (EPMM) Code Injection Vulnerability | 2026-04-08 | OWASP A03 Injection -> SQLi/auth-bypass, command/template injection labs if sink exists |
| <specific-cve-id> | Langflow Langflow | Langflow Code Injection Vulnerability | 2026-03-25 | OWASP A03 Injection -> SQLi/auth-bypass, command/template injection labs if sink exists |
| <specific-cve-id> | Craft CMS Craft CMS | Craft CMS Code Injection Vulnerability | 2026-03-20 | OWASP A03 Injection -> SQLi/auth-bypass, command/template injection labs if sink exists |
| <specific-cve-id> | Laravel Livewire | Laravel Livewire Code Injection Vulnerability | 2026-03-20 | OWASP A03 Injection -> SQLi/auth-bypass, command/template injection labs if sink exists |

### path_traversal_file_read
| CVE | Vendor/Product | KEV name | Date added | Lab mapping |
|---|---|---|---|---|
| <specific-cve-id> | Trend Micro Apex One | Trend Micro Apex One (On-Premise) Directory Traversal Vulnerability | 2026-05-21 | OWASP A01/A05 -> /ftp/file-read/path traversal/file exposure bundles |
| <specific-cve-id> | ConnectWise ScreenConnect | ConnectWise ScreenConnect Path Traversal Vulnerability | 2026-04-28 | OWASP A01/A05 -> /ftp/file-read/path traversal/file exposure bundles |
| <specific-cve-id> | Samsung MagicINFO 9 Server | Samsung MagicINFO 9 Server Path Traversal Vulnerability | 2026-04-24 | OWASP A01/A05 -> /ftp/file-read/path traversal/file exposure bundles |
| <specific-cve-id> | SimpleHelp  SimpleHelp | SimpleHelp Path Traversal Vulnerability | 2026-04-24 | OWASP A01/A05 -> /ftp/file-read/path traversal/file exposure bundles |
| <specific-cve-id> | Kentico Kentico Xperience | Kentico Xperience Path Traversal Vulnerability | 2026-04-20 | OWASP A01/A05 -> /ftp/file-read/path traversal/file exposure bundles |
| <specific-cve-id> | JetBrains TeamCity | JetBrains TeamCity Relative Path Traversal Vulnerability | 2026-04-20 | OWASP A01/A05 -> /ftp/file-read/path traversal/file exposure bundles |
| <specific-cve-id> | Wing FTP Server Wing FTP Server | Wing FTP Server Information Disclosure Vulnerability | 2026-03-16 | OWASP A01/A05 -> /ftp/file-read/path traversal/file exposure bundles |
| <specific-cve-id> | Cisco SD-WAN | Cisco SD-WAN Path Traversal Vulnerability | 2026-02-25 | OWASP A01/A05 -> /ftp/file-read/path traversal/file exposure bundles |

### rce
| CVE | Vendor/Product | KEV name | Date added | Lab mapping |
|---|---|---|---|---|
| <specific-cve-id> | Ivanti Endpoint Manager Mobile (EPMM) | Ivanti Endpoint Manager Mobile (EPMM) Improper Input Validation Vulnerability | 2026-05-07 | OWASP A03/A05/A06 -> only if lab has matching vulnerable component or execution sink |
| <specific-cve-id> | Marimo Marimo | Marimo Remote Code Execution Vulnerability | 2026-04-23 | OWASP A03/A05/A06 -> only if lab has matching vulnerable component or execution sink |
| <specific-cve-id> | Microsoft Office | Microsoft Office Remote Code Execution | 2026-04-14 | OWASP A03/A05/A06 -> only if lab has matching vulnerable component or execution sink |
| <specific-cve-id> | Microsoft Visual Basic for Applications (VBA) | Microsoft Visual Basic for Applications Insecure Library Loading Vulnerability | 2026-04-13 | OWASP A03/A05/A06 -> only if lab has matching vulnerable component or execution sink |
| <specific-cve-id> | Microsoft Exchange Server | Microsoft Exchange Server Deserialization of Untrusted Data Vulnerability | 2026-04-13 | OWASP A03/A05/A06 -> only if lab has matching vulnerable component or execution sink |
| <specific-cve-id> | Adobe Acrobat | Adobe Acrobat Use-After-Free Vulnerability | 2026-04-13 | OWASP A03/A05/A06 -> only if lab has matching vulnerable component or execution sink |
| <specific-cve-id> | Adobe Acrobat and Reader | Adobe Acrobat and Reader Prototype Pollution Vulnerability | 2026-04-13 | OWASP A03/A05/A06 -> only if lab has matching vulnerable component or execution sink |
| <specific-cve-id> | Ivanti Endpoint Manager Mobile (EPMM) | Ivanti Endpoint Manager Mobile (EPMM) Code Injection Vulnerability | 2026-04-08 | OWASP A03/A05/A06 -> only if lab has matching vulnerable component or execution sink |

### ssrf
| CVE | Vendor/Product | KEV name | Date added | Lab mapping |
|---|---|---|---|---|
| <specific-cve-id> | Omnissa Workspace One UEM | Omnissa Workspace ONE Server-Side Request Forgery | 2026-03-09 | OWASP A10:2021 -> blocked until isolated callback lab exists |
| <specific-cve-id> | GitLab GitLab | GitLab Server-Side Request Forgery (SSRF) Vulnerability | 2026-02-18 | OWASP A10:2021 -> blocked until isolated callback lab exists |
| <specific-cve-id> | Synacor Zimbra Collaboration Suite | Synacor Zimbra Collaboration Suite (ZCS) Server-Side Request Forgery Vulnerability | 2026-02-17 | OWASP A10:2021 -> blocked until isolated callback lab exists |
| <specific-cve-id> | GitLab Community and Enterprise Editions | GitLab Community and Enterprise Editions Server-Side Request Forgery (SSRF) Vulnerability | 2026-02-03 | OWASP A10:2021 -> blocked until isolated callback lab exists |
| <specific-cve-id> | Oracle E-Business Suite | Oracle E-Business Suite Server-Side Request Forgery (SSRF) Vulnerability | 2025-10-20 | OWASP A10:2021 -> blocked until isolated callback lab exists |
| <specific-cve-id> | Adminer Adminer | Adminer Server-Side Request Forgery Vulnerability | 2025-09-29 | OWASP A10:2021 -> blocked until isolated callback lab exists |
| <specific-cve-id> | Synacor Zimbra Collaboration Suite (ZCS) | Synacor Zimbra Collaboration Suite (ZCS) Server-Side Request Forgery (SSRF) Vulnerability | 2025-07-07 | OWASP A10:2021 -> blocked until isolated callback lab exists |
| <specific-cve-id> | Ivanti Connect Secure, Policy Secure, and Neurons | Ivanti Connect Secure, Policy Secure, and Neurons Server-Side Request Forgery (SSRF) Vulnerability | 2024-01-31 | OWASP A10:2021 -> blocked until isolated callback lab exists |

### xss
| CVE | Vendor/Product | KEV name | Date added | Lab mapping |
|---|---|---|---|---|
| <specific-cve-id> | Microsoft Microsoft | Microsoft Exchange Server Cross-Site Scripting Vulnerability | 2026-05-15 | OWASP A03/A05 -> browser-backed reflected/stored XSS runtime proof |
| <specific-cve-id> | Synacor Zimbra Collaboration Suite (ZCS) | Synacor Zimbra Collaboration Suite (ZCS) Cross-site Scripting Vulnerability | 2026-04-20 | OWASP A03/A05 -> browser-backed reflected/stored XSS runtime proof |
| <specific-cve-id> | Synacor Zimbra Collaboration Suite (ZCS) | Synacor Zimbra Collaboration Suite (ZCS) Cross-Site Scripting Vulnerability | 2026-03-18 | OWASP A03/A05 -> browser-backed reflected/stored XSS runtime proof |
| <specific-cve-id> | Roundcube Webmail | RoundCube Webmail Cross-site Scripting Vulnerability | 2026-02-20 | OWASP A03/A05 -> browser-backed reflected/stored XSS runtime proof |
| <specific-cve-id> | OpenPLC ScadaBR | OpenPLC ScadaBR Cross-site Scripting Vulnerability | 2025-11-28 | OWASP A03/A05 -> browser-backed reflected/stored XSS runtime proof |
| <specific-cve-id> | Synacor Zimbra Collaboration Suite (ZCS) | Synacor Zimbra Collaboration Suite (ZCS) Cross-site Scripting Vulnerability | 2025-10-07 | OWASP A03/A05 -> browser-backed reflected/stored XSS runtime proof |
| <specific-cve-id> | Roundcube Webmail | RoundCube Webmail Cross-Site Scripting Vulnerability | 2025-06-09 | OWASP A03/A05 -> browser-backed reflected/stored XSS runtime proof |
| <specific-cve-id> | Synacor Zimbra Collaboration Suite (ZCS) | Synacor Zimbra Collaboration Suite (ZCS) Cross-Site Scripting (XSS) Vulnerability | 2025-05-19 | OWASP A03/A05 -> browser-backed reflected/stored XSS runtime proof |

### xxe
| CVE | Vendor/Product | KEV name | Date added | Lab mapping |
|---|---|---|---|---|
| <specific-cve-id> | OSGeo GeoServer | OSGeo GeoServer Improper Restriction of XML External Entity Reference Vulnerability | 2025-12-11 | OWASP A05:2021 -> only if XML parser/input surface exists |
| <specific-cve-id> | SysAid SysAid On-Prem | SysAid On-Prem Improper Restriction of XML External Entity Reference Vulnerability | 2025-07-22 | OWASP A05:2021 -> only if XML parser/input surface exists |
| <specific-cve-id> | SysAid SysAid On-Prem | SysAid On-Prem Improper Restriction of XML External Entity Reference Vulnerability | 2025-07-22 | OWASP A05:2021 -> only if XML parser/input surface exists |
| <specific-cve-id> | North Grid Proself | North Grid Proself Improper Restriction of XML External Entity (XXE) Reference Vulnerability | 2024-12-03 | OWASP A05:2021 -> only if XML parser/input surface exists |
| <specific-cve-id> | Adobe Commerce and Magento Open Source | Adobe Commerce and Magento Open Source Improper Restriction of XML External Entity Reference (XXE) Vulnerability | 2024-07-17 | OWASP A05:2021 -> only if XML parser/input surface exists |
| <specific-cve-id> | Synacor Zimbra Collaboration Suite (ZCS) | Synacor Zimbra Collaboration Suite (ZCS) Improper Restriction of XML External Entity Reference | 2022-01-10 | OWASP A05:2021 -> only if XML parser/input surface exists |
| <specific-cve-id> | Citrix StoreFront Server | Citrix StoreFront Server XML External Entity (XXE) Processing Vulnerability | 2021-11-03 | OWASP A05:2021 -> only if XML parser/input surface exists |
| <specific-cve-id> | SAP NetWeaver | SAP NetWeaver XML External Entity (XXE) Vulnerability | 2021-11-03 | OWASP A05:2021 -> only if XML parser/input surface exists |

## Next lab-test queue
- KEV-pattern path/file read: Extend existing directory/file-read bundle: test traversal encodings and allowed/blocked file patterns from Kali; promote only if non-SPA proof and bounded file evidence exist.
- KEV-pattern upload/file write: Continue marker upload flow: discover retrieval/storage path and extension/content-type validation; no webshell claim unless execution proof exists.
- KEV-pattern browser XSS: Use Kali Chromium/Playwright-style instrumentation or known Juice Shop challenge route to capture runtime proof, not just reflected payload text.
- KEV-pattern auth/access-control: Use SQLi-derived admin and low/no-auth controls to test privilege boundary reads/state changes.
- KEV-pattern SSRF/XXE/deserialization: Record as blocked until matching input surface/callback lab/parser exists.
