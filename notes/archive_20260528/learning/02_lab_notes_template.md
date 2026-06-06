> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# 實驗筆記模板

> 每打完一個靶/做完一次實驗就用這份模板存一份，命名建議：`YYYY-MM-DD_平台_靶名.md`
> 例如 `2026-05-08_HTB_Lame.md`

---

## 1. 基本資訊

- **日期**：
- **平台 / 靶名**：（HTB / THM / VulnHub / 自架）
- **難度**：
- **目標 IP**：
- **預估時間 / 實際時間**：
- **OS / 主要服務**：
- **MITRE ATT&CK 戰術**：（Initial Access / Execution / Privilege Escalation / ...）

---

## 2. Recon 摘要

### Nmap 結果

```
（貼上 nmap -sC -sV -p- 的精簡輸出）
```

### 發現的端點

| Port | Service | Version | Notes |
|------|---------|---------|-------|
|      |         |         |       |

### 其他偵察

- 子網域：
- 目錄列舉（ffuf / dirsearch）：
- OSINT / 公開資訊：

---

## 3. 攻擊鏈（Kill Chain）

> 用條列把整條攻擊路徑寫清楚，每一步附上指令與證據。

### Step 1 — Initial Access

- **手法**：
- **指令**：
  ```bash
  ```
- **證據**：（截圖路徑或指令輸出）

### Step 2 — Foothold / User Shell

- **取得使用者**：
- **關鍵憑證/Token**：

### Step 3 — Privilege Escalation

- **錯誤組態 / CVE**：
- **指令**：
- **取得 root/SYSTEM 證據**：

---

## 4. Loot

- `user.txt`：
- `root.txt`：
- 其他發現的檔案 / 憑證 / 密鑰：

---

## 5. 我學到了什麼

> 這欄最重要。**沒寫這欄等於沒做這台**。

- 新工具 / 新技術：
- 卡關 30 分鐘以上的點：
- 可以重複利用的指令片段：
- 之後遇到 X 服務該怎麼想：

---

## 6. 自動化片段

> 這次實驗中可以抽出來、之後變成腳本的東西。

```python
# e.g. 一個自製 enum function
```

---

## 7. 參考資料

- 官方 writeup / 0xdf / IppSec：
- 相關 CVE：
- 推薦讀的延伸文章：

---

## 8. 相關 OWASP / CWE

- CWE-XXX：
- OWASP Top 10：
