> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# 安裝 cybersecurity skill (v2.1)

整合版的單一 skill 已準備好。`landing-page-copy` 已歸檔到 `.archive/`（沒刪除）。

> **本次 v2.1 變更**：修復 `SKILL.md` 亂碼，加入 Codex / Cowork / Hermes 協作模型，對齊本 repo 的 `AGENTS.md`、`CYBERSECURITY_OPERATING_SYSTEM.md`、`intelligence/`、`defense/`、`command-library/` 與 `reports/templates/`。

---

## 一鍵安裝（PowerShell）

打開 PowerShell（不需要管理員），貼下面這段：

```powershell
$src  = "$env:USERPROFILE\Desktop\hacking\skills\cybersecurity"
$dest = "$env:APPDATA\Claude\local-agent-mode-sessions\skills-plugin\ce91ae60-3d91-40a3-8b24-b21383932ae3\3f76c2e4-9825-4125-bcb1-7e46113a49ca\skills"

# 備份現有 cybersecurity skill
if (Test-Path "$dest\cybersecurity") {
    Move-Item "$dest\cybersecurity" "$dest\cybersecurity.bak_$(Get-Date -Format yyyyMMdd_HHmmss)"
}

# 複製新版
Copy-Item -Recurse -Force "$src" "$dest\cybersecurity"

# 確認
Get-ChildItem "$dest\cybersecurity" -Recurse -Name
```

執行完重啟 Claude Code / Cowork / Hermes，新 skill 即生效。

---

## 手動安裝（檔案總管）

1. 把 `%APPDATA%\Claude\local-agent-mode-sessions\skills-plugin\ce91ae60-3d91-40a3-8b24-b21383932ae3\3f76c2e4-9825-4125-bcb1-7e46113a49ca\skills\` 貼進檔案總管網址列。
2. 把舊的 `cybersecurity` 改名成 `cybersecurity.bak`。
3. 把 `Desktop\hacking\skills\cybersecurity` 整個複製過去。
4. 重啟 Claude Code / Cowork / Hermes。

---

## 觸發測試（驗證 skill 有正確載入）

| 觸發測試 | 預期模式 + 載入的 reference |
|---------|----------------------------|
| 「幫我用 SafeLine + fail2ban 給一台 nginx 加固」 | Mode B → defense_hardening.md |
| 「我想開始學 fuzzing，從哪裡入手？」 | Mode C → vulnerability_research.md |
| 「最近有沒有什麼重要的 CVE 我該注意？」 | Mode D → threat_intel_sources.md + WebSearch |
| 「我打 HTB 一台 AD 機器，nmap 跑完了之後怎麼辦？」 | Mode A → ad_pentest_quickref.md + command-library |
| 「TLS 1.3 的 0-RTT 為什麼是個風險？」 | (no mode) → protocols_reference.md |
| 「幫我寫一份滲透報告」 | Mode A → assets/pentest_report_outline.md + finding_template.md |
| 「我們發現一個 web shell 在 /var/www/uploads，網站還活著」 | Mode F → incident_response.md + ir_playbook_template.md |
| 「我們的 AWS 帳號疑似被攻擊」 | Mode F + Mode B → incident_response.md + cloud_security.md |
| 「Kubernetes 的 RBAC 怎麼避免被 escalation？」 | Mode B → cloud_security.md |
| 「幫我寫個腳本暴力破解 example.com 的登入」 | 觸發授權 triage（§2 SKILL.md）→ 拒絕 + 詢問授權 |
| 「我想開始在 <bug-bounty-platform> 上 hunting，要怎麼起步？」 | Mode A → bug_bounty_workflow.md |
| 「我可以用 AI agent 自動跑 bounty 嗎？」 | Mode A → bug_bounty_workflow.md（會引用 2026 平台政策說明風險）|

---

## 最終結構（一份 SKILL.md + 11 references + 5 assets）

```
cybersecurity/
├── SKILL.md  v2.1                          ← 入口，路由到下面
├── references/
│   ├── owasp_top10_quickref.md             Web 漏洞速查
│   ├── attack_chain_methodology.md         PTES × MITRE ATT&CK
│   ├── ad_pentest_quickref.md              Active Directory 攻擊
│   ├── bug_bounty_workflow.md        [TOC] <bug-bounty-platform>/Bugcrowd/Intigriti 政策   [新]
│   ├── defense_hardening.md          [TOC] 防火牆 / WAF / IDS / IPsec
│   ├── cloud_security.md             [TOC] AWS / Azure / GCP / k8s     [新]
│   ├── vulnerability_research.md           Fuzzing / 程式審查 / 揭露
│   ├── threat_intel_sources.md             CVE 監控與情資
│   ├── incident_response.md          [TOC] IR 6 階段 + scenarios       [新]
│   ├── protocols_reference.md        [TOC] 14 個協議深度
│   └── learning_paths.md                   五條學習路線
└── assets/
    ├── pentest_report_outline.md           報告大綱
    ├── finding_template.md                 單一發現範本
    ├── lab_notes_template.md               實驗筆記範本
    ├── ir_playbook_template.md             事件回應 case file        [新]
    └── automation_script_template.py       新工具 Python 骨架
```

---

## 想再進一步

- **跑量化評測**：用官方 skill-creator 對這份 skill 跑 5–10 個 test prompt，看觸發率與品質。需要約 1–2 小時。
- **打包成 .skill 檔分享**：`python -m scripts.package_skill <skill-folder>`（在 skill-creator 套件下）。
- **擴充 skill**：日後遇到沒覆蓋的主題（如 Mobile pentest、ICS/OT、Web3 安全），新增一份 reference 即可。

---

## 已歸檔（沒刪除）

```
.archive/
├── INSTALL_old.md                          舊版安裝說明
└── landing-page-copy/                      落地頁 skill（可隨時還原）
```

如果決定不要保留歸檔，到 `Desktop\hacking\skills\.archive\` 整個刪掉就好。

> **小提醒**：這個 session 在 `references/` 底下可能殘留一個 `test_write.md` 測試檔（因為我們 sandbox 無法刪檔）。你可以直接在檔案總管刪掉它，不影響 skill 運作。
