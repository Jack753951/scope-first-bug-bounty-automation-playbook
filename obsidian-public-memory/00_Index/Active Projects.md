> Public filtered Obsidian memory export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# Active Projects

## Cybersec Lab

Repo:

- `<user-home>` — current main/primary workspace.
- `<user-home>` — legacy/reference-only unless explicitly reactivated.

目前重點：

- 長期目標：在 `hacking2` 建立 Hermes-as-primary 的授權 bug-bounty 平台；第一優先是 2026-06-27 前拿到 first report-ready draft/submission candidate。自動化、模組化 proof-library、evidence、review、report pipeline 是支援這個目標的能力，必須被 scope/program policy/hard stops 約束。
- 當前階段：2026-05-28 restructure → hermes-as-primary clean slate；所有舊 active Tier A live lanes 已 archived，current route 以 `handoff/current_navigation.md` 為準。
- 目前實作重點：保持 `INDEX.md` / `SAFETY.md` / `.hermes.md` / `handoff/current_navigation.md` 作為 active truth；使用 local lab 最新漏洞 proof→bundle/library，再把可用模式映射到新選定的 in-scope bounty target。
- 目前下一步：挑一個新 first-bounty target；同時維持 latest-vulnerability research lane（例如 LiquidJS <advisory-redacted> 已在 `<lab-vm>` 完成 marker-only local proof）。
- 目前不做：public/real bug bounty target activation、scanner confirmed finding promotion、credential theft/brute-force against real accounts、callback/pivot outside isolated lab、loot retention、destructive behavior outside disposable lab snapshot/recovery gate。

相關筆記：

- [[../06_Project_Cybersec_Lab/Architecture|Architecture]]
- [[../06_Project_Cybersec_Lab/Phase 1 Program Scope System|Phase 1 Program Scope System]]
- [[../01_Methodology/OWASP Top 10 Release Coverage and Lab Testing Plan|OWASP Top 10 Release Coverage and Lab Testing Plan]]
- [[../01_Methodology/OWASP Top 10 2003-2025 Traceability Matrix|OWASP Top 10 2003-2025 Traceability Matrix]]
- [[../01_Methodology/OWASP 2025 Migration and Automation Modularization Review|OWASP 2025 Migration and Automation Modularization Review]]
- [[../01_Methodology/Phase 4B Script-first Architecture Reset 2026-05-21|Phase 4B Script-first Architecture Reset 2026-05-21]]
- [[../01_Methodology/Module Bundle Distinction and Service Scanner Direction 2026-05-21|Module Bundle Distinction and Service Scanner Direction 2026-05-21]]
- [[../02_Lab Runs/Phase 4B OWASP Local-Lab Probe Result 2026-05-21|Phase 4B OWASP Local-Lab Probe Result 2026-05-21]]
- [[../02_Lab Runs/Phase 4B Fast-Lane GET-only Adapter Result 2026-05-21|Phase 4B Fast-Lane GET-only Adapter Result 2026-05-21]]
- [[../02_Lab Runs/Phase 4B Wave2 Benign Params Adapter Result 2026-05-21|Phase 4B Wave2 Benign Params Adapter Result 2026-05-21]]
- [[../02_Lab Runs/Phase 4B Three Exposure Bundles 2026-05-21|Phase 4B Three Exposure Bundles 2026-05-21]]
- [[../02_Lab Runs/Phase 4B OWASP CVE Continuation 2026-05-22|Phase 4B OWASP CVE Continuation 2026-05-22]]
- [[../02_Lab Runs/DVWA Command Injection Impact Wave 1 2026-05-22|DVWA Command Injection Impact Wave 1 2026-05-22]]
- [[../02_Lab Runs/DVWA Command Injection Callback-Control Wave 2 2026-05-22|DVWA Command Injection Callback-Control Wave 2 2026-05-22]]
- [[../02_Lab Runs/DVWA Command Injection True Attacker Callback 2026-05-22|DVWA Command Injection True Attacker Callback 2026-05-22]]
- [[../02_Lab Runs/<advisory-redacted> Kernel Lane Triage 2026-05-22|<advisory-redacted> Kernel Lane Triage 2026-05-22]]
- [[../02_Lab Runs/Work Record 2026-05-21|Work Record 2026-05-21]]
