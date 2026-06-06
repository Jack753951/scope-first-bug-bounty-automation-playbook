> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Phase 4A — 隔離式積極實驗室切片計畫 / 閘門文件

- 文件編號：phase4a_isolated_aggressive_lab_slice_20260521
- 建立日期：2026-05-21
- 建立工具：Claude Code CLI（本計畫由 CLI 撰寫；實際使用的模型 ID 與 JSON usage 數據由 Hermes 於另一份審計檔分開記錄，不在本文件內聲稱）
- 文件狀態：草案 / 待 Hermes 與多方審查通過後始得啟用
- 上層政策依據：本倉庫安全測試政策、bug bounty scope 限制、`handoff/active_testing_policy.md`
- 主要受眾：使用者本人、Hermes（守門人）、Cowork（審查/規劃輔助）、未來接手者

---

## 0. 緊要前置宣告（必讀）

1. **積極 / 破壞性測試在本計畫所有閘門通過、且經 Hermes 明確簽核之前，全程 BLOCKED。**
2. 本切片**不授權**對任何真實目標（網際網路服務、公開 bug bounty 資產、第三方 IP/網域、雲端租戶等）執行任何積極或破壞性動作；所有授權邊界僅止於本機 VirtualBox 內、明確列出的 victim 快照 VM。
3. 本切片**不變更現行 scope**，亦不取代既有 P3.x / P4 任何 ROE。任何欲擴張 scope 的請求，須走獨立的政策更新流程，不可由本切片夾帶。
4. 不允許「臨時把真實目標當作練習」。若實驗中觀察到任何流量離開虛擬 host-only 網段，立即觸發 Kill Switch（見 §10）。

---

## 1. 目的 (Purpose)

本切片的唯一目的，是在**完全隔離的快照實驗室**內，評估專案在「積極 / 破壞性腳本」面向的**能力上限與安全護欄**，以回答下列問題：

- 在本機可控環境下，現有 recon → review → script → review 流程能撐到多 aggressive 的層級？
- 哪些動作類別可以被安全地模組化、外掛化（pluginize）並納入未來標準工具庫？
- 哪些動作類別必須永久禁止、或僅能在隔離實驗室出現、絕不外推至真實 scope？
- 多方審查迴圈（人 / Hermes / Cowork / Claude Code）在面對高風險腳本時，是否仍能維持「先審後跑」的紀律？

非目的（Out of Scope）：

- 不在此切片內追求任何 bounty payload、不產生對外可投遞的 exploit。
- 不替任何真實 CVE 寫 PoC，除非該 CVE 已有公開且明確標示「安全沙盒可重現」的官方 lab 鏡像。
- 不在此切片內進行紅隊演練、不模擬內網橫向移動跨越本機 host-only 網段。

---

## 2. 真實目標的非授權聲明 (Non-Authorization)

- 本計畫**不授權**對下列任何對象進行任何形式的主動測試、流量發送或弱點驗證：
  - 任何網際網路上的網域、IP、API、雲端控制台。
  - 任何公開或私下 bug bounty 計畫的真實生產資產（即使該計畫已將該資產列入 in-scope，亦不在本切片授權範圍）。
  - 使用者所屬之第三方雇主、客戶、合作方、家庭網路、ISP 設備、路由器、IoT 裝置。
- 唯一被授權的「靶」是本機 VirtualBox 中、由使用者本人建立且已快照的 victim VM（目前唯一登錄者為 `<victim-vm>` 上的 Juice Shop，<lab-ip>:3000）。
- 若日後新增 victim VM，必須先在本文件 §A 附錄登錄、再經 Hermes 簽核，方可納入授權清單。

---

## 3. 必要的 VirtualBox 隔離條件 (Required Isolation)

3.1 **網路模式**

- victim VM 與攻擊 VM 之間僅允許使用 `Host-Only` 介面（目前為 `<lab-ip>/24`）。
- 禁止 `NAT`、`Bridged`、`NAT Network`、`Internal` 以外的任何介面對 victim VM 啟用。
- 攻擊 VM 在執行積極腳本期間，**必須關閉所有對外（NAT/Bridged）網卡**，僅保留 host-only。
- DNS / Proxy / VPN：實驗期間禁止在攻擊 VM 上掛載任何對外 VPN、Tor、proxy chain；若需 DNS，僅允許指向 host-only 內的本機 resolver 或 `127.0.0.1`。

3.2 **攻擊 VM 的選擇**

二擇一，並在 §13 Checklist 明確勾選：

- (A) **建立獨立的攻擊 VM**：自既有 red-team Kali 工作站匯出，於 VirtualBox 中匯入為新 VM（例如 `kali-attacker-lab`），完成後**立刻拍攝乾淨快照 `clean-baseline`**。此 VM 僅用於本切片之積極腳本實驗。
- (B) **明確聲明不使用現行 red-team Kali 工作站執行高風險腳本**：若暫不建立獨立 VM，則本切片**所有積極執行階段一律 BLOCKED**，僅允許在文件 / dry-run / 紙上推演層級進行。此選項不得作為「先跑了再說」的退路。

預設建議採 (A)。若採 (B)，必須在 Checklist 上以文字明示「本階段不執行任何積極腳本，僅進行規劃審查」。

3.3 **快照閘門 (Snapshot Gates)**

每一次積極腳本執行前後，皆須完成以下快照節點，缺一不可：

| 節點 | 快照名稱範例 | 觸發時機 |
|---|---|---|
| G0 | `attacker-clean-baseline` | 攻擊 VM 建立後、任何工具安裝前 |
| G1 | `attacker-tooling-ready` | 工具鏈安裝完成、實驗開始前 |
| G2 | `victim-clean-baseline` | victim VM 建立或重置後、任何攻擊腳本送出前 |
| G3 | `pre-run-<slice-id>` | 每一次切片執行前 5 分鐘內 |
| G4 | `post-run-<slice-id>` | 該切片執行結束、收集 artifacts 之後 |
| G5 | `recovery-checkpoint` | Kill Switch 觸發後或 victim 服務無法回復時，回滾至 G2 並重新拍攝 |

回滾規則：任何 post-run 觀察到非預期持久化（例：victim VM 在重啟後仍處於異常狀態、攻擊 VM 出現未知 outbound 連線殘留），立即回滾至最近一個乾淨快照，並補登事件記錄。

---

## 4. 允許的動作類別 (Allowed Action Classes)

下列動作類別在通過 §13 Checklist、且僅針對本機 host-only victim VM 時，得在本切片內執行：

- A1. 被動 recon：埠掃描（受 §6 速率限制）、服務指紋、HTTP 路徑列舉、目錄爆破（字典需事先審查）。
- A2. 主動但可逆的應用層測試：對 Juice Shop 等已知練習靶的 OWASP Top 10 類別測試（SQLi、XSS、IDOR、SSRF 限本機回環、auth bypass）。
- A3. 受控的 fuzzing：對單一 endpoint、有 request 上限、有 timeout、有輸出 redaction。
- A4. 受控的暴力測試：僅針對 victim VM 本身的測試帳號，須有單帳號最大嘗試次數上限。
- A5. 已知 CVE 的本機重現：僅當該 CVE 有官方/廣為認可的 vulnerable lab 容器或 image，且不需向外抓取執行檔。

---

## 5. 禁止的動作類別 (Forbidden Action Classes)

下列動作類別在本切片內**絕對禁止**，無論是否在隔離環境內：

- F1. 任何對非授權 IP / 網域 / 雲端帳號發出的封包（含「只是 ping 一下」「只是 nslookup」）。
- F2. 任何 DoS / DDoS / 資源耗盡腳本，即使對象是 victim VM；本切片不研究「打掛它」這類目標。
- F3. 任何 ransomware、wiper、persistent backdoor、rootkit、bootkit、firmware 類別 PoC，即使在隔離 VM 內也禁止落地執行。
- F4. 任何供應鏈攻擊模擬（投毒 npm/pypi、惡意 PR、CI 污染）。
- F5. 任何規避偵測 / EDR bypass / AV evasion 為主要目的之腳本（防禦研究用途請走獨立的 defensive 切片並另案審查）。
- F6. 任何針對真實人類的社交工程、釣魚、OSINT 深挖（含對使用者本人帳號之外的個人資料蒐集）。
- F7. 任何會自動向外回報、自動更新、自動下載額外 payload 的工具，未經逐行人審不得執行。
- F8. 任何「先跑後審」的腳本，包括「我只是想看看會發生什麼」這類請求。

---

## 6. 請求 / 時間 / 速率限制 (Quotas)

- 單一切片執行視窗：≤ 30 分鐘，含啟動、執行、收尾。
- 單一 target endpoint 請求上限：≤ 2,000 requests / 切片，且 ≤ 20 req/s。
- Fuzzing payload 集大小：≤ 5,000 條，需事先 commit 至 repo 並走審查。
- 暴力測試：單一帳號 ≤ 50 次嘗試 / 切片；超過視為觸發 Kill Switch。
- 同一 victim VM 每日累計切片執行：≤ 3 次；超過須隔日重排。
- 任一腳本若連續 60 秒無 stdout / 無進展，視為 hang，立即終止並記錄。

---

## 7. Kill Switch 與回復程序 (Kill Switch & Recovery)

7.1 Kill Switch 觸發條件（任一即觸發）：

- 偵測到攻擊 VM 有任何封包目的地不在 `<lab-ip>/24`。
- victim VM 服務（如 Juice Shop）非預期離線、或回應出現非該應用之內容。
- 腳本輸出含有疑似真實 PII、真實 credential、真實外部資產字串。
- 使用者或 Hermes 任一方喊停。
- 觀察到超出 §6 任一上限。

7.2 Kill Switch 動作（依序）：

1. 在攻擊 VM 上 `Ctrl-C` / `pkill` 終止正在執行的腳本。
2. 於 VirtualBox 介面 `ACPI Shutdown` 或必要時 `Power Off` 攻擊 VM 與 victim VM。
3. 攻擊 VM 回滾至 `attacker-tooling-ready` 或更早乾淨快照。
4. victim VM 回滾至 `victim-clean-baseline`。
5. 撰寫 `handoff/phase4a_killswitch_<timestamp>.md`，記錄觸發原因、時序、保留的 artifact、後續處置建議。
6. 在恢復下一輪實驗前，**必須**由 Hermes 重新核可 §13 Checklist。

---

## 8. 稽核與遮罩 Artifacts (Audit & Redaction)

每一次切片執行皆須產出下列檔案，集中存於 `handoff/phase4a_runs/<slice-id>/`：

- `plan.md`：本切片要做什麼、預期觀察、停止條件。
- `commands.log`：所有實際下達的指令（含時間戳、執行者、工作目錄）。
- `network.pcap` 或 `network_summary.md`：host-only 介面流量摘要；如含完整 pcap，須先確認其中無真實外部 IP。
- `tool_output.redacted.log`：工具原始輸出經遮罩（token、session id、cookie、密碼欄位以 `[REDACTED]` 取代）。
- `findings.md`：觀察到的弱點、可重現步驟、嚴重度自評（僅供內部學習，不對外）。
- `post_health.md`：見 §9。
- `review_trail.md`：多方審查每一輪意見（見 §11）。

遮罩規則：任何疑似真實使用者資料、真實 email、真實 API key 一律遮罩；若實驗中意外蒐集到，須於 `findings.md` 註明來源並安排刪除。

---

## 9. 執行前 / 執行後健檢 (Pre/Post Health)

9.1 Pre-Run Health（任一不通過則 BLOCKED）：

- 攻擊 VM 對外網卡為關閉狀態。
- `ip route` 僅見 host-only 與 loopback。
- victim VM 已回滾至 `victim-clean-baseline` 並重啟驗證服務可達。
- 系統時間正確（用於後續稽核時序比對）。
- 預定執行的腳本已 commit 至 repo，未含未審查之依賴下載步驟。

9.2 Post-Run Health：

- 比對攻擊 VM 進程清單與 G1 快照差異。
- 比對 victim VM 服務回應指紋與 G2 快照差異。
- 確認沒有遺留 listener / reverse shell / cron / systemd timer。
- 確認 artifacts 完整、遮罩通過。
- 若任一健檢失敗 → 觸發 §7 回復程序。

---

## 10. 多方審查迴圈 (Multi-Party Review Loop)

固定順序，任一步未完成不得跳到下一步：

1. **Recon 草案** — 由使用者或 Cowork 提出本次想探索的方向、目標 VM、預期手法。
2. **Review #1（規劃審查）** — Hermes 與另一審查者（人或 Cowork）對草案做風險分類、確認落在 §4 而非 §5、確認在 §6 上限內。產出 `cowork_phase4a_<slice-id>_direction_review.md`。
3. **Script 撰寫** — 由 Claude Code CLI 或使用者撰寫具體腳本/指令清單，commit 至 repo（不直接執行）。
4. **Review #2（腳本審查）** — 對腳本逐行審查：是否會打到非授權對象、是否會落地禁止類別、是否有 hard-coded credential、是否含對外回報行為。產出 `cowork_phase4a_<slice-id>_script_review.md`。
5. **Go/No-Go** — Hermes 在 `review_trail.md` 簽核 GO，且 §13 Checklist 全勾，方可進入執行階段。
6. **執行** — 依 §6 上限執行，全程錄 `commands.log`。
7. **Review #3（事後審查）** — 對 artifacts、findings、Kill Switch 是否觸發、健檢結果做覆盤；決定下一輪方向，回到步驟 1。

任一輪 review 出現「不確定」即視為 No-Go，回退一步。

---

## 11. 外掛化 / 模組化判準 (Pluginization Criteria)

某一動作經多次切片驗證後，若同時符合以下條件，方可考慮抽出成為標準外掛（plugin / tool module）：

- 至少在 3 個獨立切片中安全完成、且每次 Post-Run Health 全通過。
- 動作邊界可被靜態描述（輸入域、輸出域、副作用、最大資源用量）。
- 具備明確 dry-run 模式；dry-run 與實跑差異可被 diff。
- 預設 fail-closed：缺少授權檔、缺少 target 白名單即拒絕執行。
- 內建上限與遮罩，無需依賴外部呼叫者記得設參數。
- 通過 Hermes 對其文件、預設值、錯誤處理路徑的審查。

未達上述條件者，僅能以一次性腳本形式留在 `handoff/phase4a_runs/<slice-id>/`，不得提升為共用工具。

---

## 12. 停止條件 (Stop Conditions)

下列任一成立，整個 Phase 4A 切片計畫立即暫停，並重啟政策審查：

- 任一次 Kill Switch 在 7 日內被觸發 ≥ 2 次。
- 任一 artifact 出現未遮罩之真實外部資料。
- 使用者本人對隔離度、scope、責任歸屬有任何疑慮。
- Hermes 對本文件之假設前提（例如 host-only 隔離仍有效）失去信心。
- 法律 / 合約 / 雇主政策出現變動，影響本機實驗合法性判讀。
- Phase 4A 整體執行超過 14 個自然日仍未完成首輪 GO，須重新評估必要性。

---

## 13. Go / No-Go 啟用檢查表 (Activation Checklist)

> **此檢查表所有項目須由 Hermes 逐項核可後，積極執行階段方可解除 BLOCKED。**
> 在 Hermes 簽核前，本文件僅作為規劃 / 紙上推演依據。

- [ ] 已確認本切片不變更現行 bug bounty scope，亦不授權任何真實目標。
- [ ] 已在 §A 附錄登錄本切片允許的 victim VM 清單（含 IP、服務、快照名稱、建立日期）。
- [ ] 已二擇一並書面勾選：
  - [ ] (A) 已建立獨立攻擊 VM `kali-attacker-lab`，並完成 `attacker-clean-baseline`、`attacker-tooling-ready` 快照。
  - [ ] (B) 明確聲明：本階段不在 red-team Kali 正常工作站上執行任何積極腳本，僅進行規劃 / dry-run / 紙上推演。
- [ ] 攻擊 VM 與 victim VM 均僅啟用 host-only 介面，對外網卡關閉。
- [ ] 所有預定腳本已 commit 至 repo，未含外部下載執行步驟，未含 hard-coded 真實 credential。
- [ ] §4 / §5 動作分類已逐條對照本次切片計畫，無越界。
- [ ] §6 限額已寫入 `plan.md`，並於腳本內以技術手段強制（非靠人記得）。
- [ ] Kill Switch 程序（§7）已熟讀；快照 G3 / G4 名稱已預先填好。
- [ ] Pre-Run Health（§9.1）已逐項通過。
- [ ] 多方審查迴圈（§10）Review #1 與 Review #2 均已完成、皆為 GO。
- [ ] 已在 `review_trail.md` 留下 Hermes 的 GO 簽核字句與時間戳。
- [ ] Claude Code CLI 路由 / 工具 / 模型限制聲明：本計畫由 Claude Code CLI 撰寫，**本文件不自我聲稱使用何種具體模型 ID**；實際模型 ID 與 JSON usage 由 Hermes 於獨立稽核檔記錄，本文件不重複、不替代該記錄。
- [ ] 確認以上每一項皆為「是」之後，Hermes 方可在覆核紀錄中註明「Phase 4A 積極執行解除 BLOCKED — 限本切片」。

---

## §A 附錄：授權 victim VM 清單（隨切片更新）

| VM 名稱 | 介面 / IP | 服務 | 快照基線 | 登錄日期 | 備註 |
|---|---|---|---|---|---|
| <victim-vm> | host-only / <lab-ip>:3000 | Juice Shop | victim-clean-baseline（待補拍） | 2026-05-21 | 目前唯一登錄之 victim VM |

新增 victim VM 須以 PR / commit 形式追加本表，並重新跑一次 §13 Checklist。

---

## §B 附錄：Claude Code 路由 / 工具 / 模型限制聲明

- 本計畫由 Claude Code CLI 介面撰寫，受該介面之工具集與權限模式限制。
- 本文件**不自我聲稱**所使用的具體模型 ID 或版本；任何此類聲稱皆可能與實際 JSON usage 不符，故一律改由 Hermes 從 CLI 的 usage 記錄中事後比對、登錄於獨立稽核檔。
- 若未來需在合規 / 稽核情境下證明本計畫由何模型產出，請以 Hermes 的稽核檔為準，而非本文件之自述。

---

（本文件結束。在 §13 Checklist 未全數通過且 Hermes 未簽核之前，Phase 4A 積極執行階段保持 BLOCKED。）
