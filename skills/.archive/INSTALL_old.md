> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# 兩份 Skill 安裝指南

我把兩個 skill 都建好了，各自獨立，不會互相打架。

```
hacking/skills/
├── cybersecurity/                ← 取代你原本壞掉那份
│   ├── SKILL.md
│   ├── references/
│   │   ├── owasp_top10_quickref.md
│   │   ├── attack_chain_methodology.md
│   │   ├── ad_pentest_quickref.md
│   │   └── learning_paths.md
│   └── assets/
│       ├── pentest_report_outline.md
│       ├── finding_template.md
│       └── lab_notes_template.md
│
└── landing-page-copy/            ← 全新獨立 skill
    ├── SKILL.md
    ├── references/
    │   ├── copywriting_frameworks.md
    │   ├── section_structure.md
    │   └── quality_checklist.md
    └── assets/
        ├── blank_template.md
        └── landing_page_template.md   ← 保留 AI Profit Boardroom 版本
```

---

## 安裝方式（PowerShell — 推薦）

打開 PowerShell（不需要管理員權限），貼下面這段：

```powershell
$src    = "$env:USERPROFILE\Desktop\jack\hacking\skills"
$dest   = "$env:APPDATA\Claude\local-agent-mode-sessions\skills-plugin\ce91ae60-3d91-40a3-8b24-b21383932ae3\3f76c2e4-9825-4125-bcb1-7e46113a49ca\skills"

# 備份舊的 cybersecurity skill（以防你還想留著）
if (Test-Path "$dest\cybersecurity") {
    Move-Item "$dest\cybersecurity" "$dest\cybersecurity.bak_$(Get-Date -Format yyyyMMdd_HHmmss)"
}

# 複製兩個新 skill 過去
Copy-Item -Recurse -Force "$src\cybersecurity"      "$dest\cybersecurity"
Copy-Item -Recurse -Force "$src\landing-page-copy"  "$dest\landing-page-copy"

# 列出結果確認
Get-ChildItem "$dest\cybersecurity", "$dest\landing-page-copy" -Recurse -Name
```

執行後重新啟動 Claude Code / Cowork，兩個 skill 就會自動被載入。

---

## 安裝方式（用檔案總管手動）

如果你不想用 PowerShell：

1. 開啟 `%APPDATA%\Claude\local-agent-mode-sessions\skills-plugin\ce91ae60-3d91-40a3-8b24-b21383932ae3\3f76c2e4-9825-4125-bcb1-7e46113a49ca\skills\`（直接把這串貼到檔案總管網址列）。
2. 把舊的 `cybersecurity` 資料夾改名 → `cybersecurity.bak`（保險）。
3. 從 `Desktop\jack\hacking\skills\` 把 `cybersecurity` 與 `landing-page-copy` 兩個資料夾**整個複製過去**。
4. 重啟 Claude Code / Cowork。

---

## 怎麼確認有效

重啟後，問我下面任一個問題：

- 觸發 cybersecurity skill：「**幫我整理一下 OWASP A03 Injection 的學習筆記**」、「**這個 HTB 機器我打不下去，nmap 結果是 …**」
- 觸發 landing-page-copy skill：「**幫我寫一個給 SaaS 的落地頁文案**」、「**用 PAS 框架幫我重寫 hero section**」

如果觸發成功，回應的開頭會看到 `<command-message>` 提示某個 skill 被載入。

---

## 兩份 skill 跟你原本那份的差別

| | 你原本那份 | 新的 cybersecurity | 新的 landing-page-copy |
|---|---|---|---|
| **名字 ↔ 內容** | ❌ 不符 | ✅ 一致 | ✅ 一致 |
| **description 是觸發詞** | ❌ 是說明文 | ✅ 是觸發條件 | ✅ 是觸發條件 |
| **有可重用資產** | ❌ 沒有 | ✅ 4 references + 3 assets | ✅ 3 references + 2 assets |
| **避免 prompt-injection 寫法** | ❌ 用 "Claude must execute" | ✅ 用描述性語氣 | ✅ 用描述性語氣 |
| **各自單一職責** | ❌ 名字錯位 | ✅ | ✅ |

---

## 想再進一步

如果你想：

1. **用官方 skill-creator 跑量化評測**：把這兩份 skill 各自跑 5–10 個 test prompt，看觸發率與品質。我可以引導你做，但需要你願意花一兩小時看評估結果。
2. **打包成 .skill 檔分享給別人**：用 `python -m scripts.package_skill <skill-folder>`（在 skill-creator 套件下），可以變成單一檔案分享。
3. **再建第三份 skill**（例如：bug bounty writeup 寫作 / cloud security audit / SOC alert triage），照同樣模式擴。

需要哪一條告訴我。
