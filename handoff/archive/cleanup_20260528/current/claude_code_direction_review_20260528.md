> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# 方向審查回覆 — Claude Code (Opus 4.7) Direction Reviewer

## 1. Worker identity

- Worker: Claude Code (Opus 4.7), 方向審查角色 (read-only direction reviewer)
- Boundary acknowledged: 不接觸 target、不掃描/fuzz/exploit/callback/OAST、不處理憑證、不修改檔案、不送 report。本回覆僅為 advisory。

## 2. Context read attestation

下列檔案已實際讀取（read-only）:

- `.hermes.md`
- `PROJECT_CHARTER.md`
- `docs/ENGINEERING_INDEX.md`
- `docs/policy/README.md`
- `docs/policy/repo_hygiene_policy.md`
- `docs/policy/memory_and_strategy_routing.md`
- `handoff/INDEX.md`
- `handoff/current_navigation.md`
- `handoff/active_strategy_queue.md`
- `handoff/current_artifact_index.md`
- `docs/strategy/platform/engineering_direction_20260527.md`
- `handoff/current/worktree_cleanup_index_20260528.md`

無缺檔。所有必讀檔案存在。

## 3. Verdict

**APPROVE_WITH_CHANGES**

理由總結：
- 願景一致且 coherent（authorized bug bounty automation platform、operator inbox、evidence → submission loop）。
- 本次 Hermes 提案的 48h / 7d 內容比 `engineering_direction_20260527.md` 已承諾的 P1–P5（4–6 + 2 + 1–2 + 3 小時可分配）**反而保守**。若此提案被當成最新方向，會悄悄 de-scope 一份還沒過期的 backlog。需明確說明：是 supersede engineering_direction，還是兩者並行。
- 7–14d「跑完一個完整 loop」未指出**所有 live lane 目前都卡在 operator-only gate**（<program-redacted> human-check、<program-name> Account B 角色變更、<program-slug> / <program-redacted> / <program-redacted> 缺 owned account）。純工程無法 unblock。必須把 operator gate 明列為前提，而非工程 deliverable。
- 30–90d「成熟為 bug bounty OS」缺 outcome metric。past 3 週「380+ handoff、20+ policy、0 submission」就是同個失敗模式重演的最大風險。需要綁定可量化指標。

## 4. 建議節奏（48h / 7d / 14d / 30d / 90d）

### 0–48 小時（工程，無 operator gate）

1. 完成 worktree commit split（依 `repo_hygiene_policy.md` 7 類拆分），重點先 land：policy archive、structure/index、worktree cleanup index。
2. 立刻交付 `scripts/build_operator_inbox.py`（engineering_direction P2，預估 2 小時）。即使下游 detector 還沒接，先讓「每天 18:00 產出 inbox」的骨架跑起來，content 從 `programs/<slug>/lane_state.json` + 既有 PARKED 列表直接 render。
3. 切換 Hermes 後端避開壞掉的 Codex adapter（P3，1–2 小時）— 但這條動 routing，需要 operator 確認後端選擇。
4. 凍結新 policy / strategy / navigation 變體（已在 engineering_direction「不可以做」列表中明文）。

### 3–7 天（工程 + 一個 operator 決定點）

1. P1 detector 批次：HAProxy 33555 / Apache httpd / Tomcat 11.0.21 / OpenSSL 3.0.18 + `daily_sweep.py` chainer。**全部 metadata-only / passive 模式 default**，live sweep 待 program scope 對齊。
2. 持續監控層 P4（disclose.io / chaos / CVE PoC diff）寫進 inbox。
3. **Operator 決定點**: <program-redacted> 是否繼續（human-check），或正式 PARK 改選 <program-name> Account B 啟動 role mutation 安全詞流程。沒有 operator 決定 → 7 天內 0 個 live lane 推進是必然，要正視這點。

### 7–14 天（完整 loop 但要分清誰負責哪段）

1. 工程段：`lane_state.json` → evidence packet 生成器 → `evidence-redaction-check.py` → report draft template，跑 dry-run。
2. Operator gate 段：選定一個 live lane（最可能是 <program-name> 或 <program-redacted>），operator 提供必要安全詞或 human-check，agent 推到 candidate 或 no-finding closeout。
3. 至少完成一次 **dry-run end-to-end**（用 PARKED lane 的歷史資料模擬），證明工程段在 operator gate 之外不會卡住。

### 14–30 天

1. 把 P4 + daily_sweep 變成 dry-run cron（仍可不對 live target 跑，先對 fixture / 已授權 lab）。
2. 完成 2–3 個 reusable bundle（access-control、lifecycle、metadata；對照 `live_bounty_attack_class_matrix_20260526.md`）。
3. 加入 submission tracking + 第一份正式 report submission（operator 最終批准）— 此為 30 天內最重要的單一 outcome。
4. Passive live check 啟用前，scheduler 必須能讀 program policy、scope、rate budget、stop-before。

### 30–90 天

1. 達到 **每月 ≥ N 個 candidate evidence packet 進 operator inbox** 與 **每月 ≥ 1 個 submission** 的可衡量輸出（具體 N 由 operator 設）。
2. 穩定 5–8 個 reusable detector / bundle。
3. 加入 vendor advisory diffing、disclosed-report mining、mobile static analysis（已在 ROI lane 清單）。
4. 每月做一次 capability-library cleanup（依 `repo_hygiene_policy.md`）。

## 5. Essential capabilities（必須有）

- `operator_inbox.md` daily renderer（無此一切自動化都看不到輸出）
- `daily_sweep.py` chainer + 4 個 fingerprint-only detector
- 持續監控 diff（disclose.io、chaos、CVE PoC GitHub）
- Evidence packet builder + redaction check（已存在 `scripts/evidence-redaction-check.py` 入口）
- Report draft template + CVSS/CWE mapping + submission tracking
- Lane state machine 嚴格化（EXECUTE / PASSIVE-ONLY / PARK / KILL / ARCHIVED）
- Hermes 後端可用（脫離壞 Codex adapter）
- `safe_target` scope gate + per-program policy intake JSON（已在 `.hermes.md`）

## 6. Non-goals（未來 30 天明確排除）

- Web UI / dashboard / SaaS multi-tenant
- 自製 vuln DB / 自製 ML 分類器 / 自製 distributed scanner
- 重造 nuclei / subfinder / httpx / arjun
- 新的 policy 變體 / tactical direction 變體 / multi-party review 變體
- 新 schema / contract（除非 ≤ 1 週內有具體 consumer）
- 新 governance / review tier 抽象層
- 任何 `handoff/` 根目錄的新 root-level 檔
- Stealth / persistence / 規避控制 / 非授權帳戶測試 / 任何 production-side 變更

## 7. Risks 與 hard stops

### Hard risks（會讓 repo 再次 chaotic）

1. **Operator gate 阻塞被誤當工程問題** — 所有 live lane 目前都需要 operator 介入。若把「7 天內推進一條 lane」當工程 KPI，agent 會傾向產更多 substrate 來「不卡住」，反而堆積。
2. **方向檔多源衝突** — 本提案、engineering_direction_20260527、active_strategy_queue 三份都聲稱是 active 方向。若不指定 single-source-of-truth 與 supersede 關係，舊問題重現。
3. **Capability-library 偷渡** — `active_strategy_queue.md` 已警告「library/index work 不可取代 evidence/report 進度」，但無自動防護。需要 metric：本週 evidence packet 數 = 0 時，禁止新 library/index commit。
4. **Hermes Codex adapter 壞掉** — engineering_direction P3 已記錄，每多 routing 一輪壞掉就多一次 silent payload drop。需在做任何 multi-agent review 流程前先修。
5. **Memory / handoff drift** — 雖然 `repo_hygiene_policy.md` 與 `memory_and_strategy_routing.md` 寫得很清楚，但 `handoff/` 根仍有 200+ 檔的歷史殘留。需設定強制：commit 進 `handoff/` 根 → CI fail（除已 allow-list 的 rolling IPC + INDEX 等）。
6. **Operator 注意力錯配** — 北極星寫「operator 每天 5 分鐘」，但實際每個 PARKED lane 都在等 operator 做高成本動作（owned account、OAuth、KYC、phone）。需重新評估哪些 lane 在現實的 operator 預算內可被 unblock。

### Hard stops（不變）

- 沒有 scope.txt + programs/<slug>/scope.json + program rules 允許 → 不對 live target 執行任何 active 動作
- 不存 secrets / OTPs / cookies / tokens / customer data
- 不做 OAuth / 帳號創建 / 付款 / KYC 自動化
- 不未經 operator 最終批准送 report

## 8. Hermes 應向 operator 確認的問題

1. **能力願景斷詞**：北極星是「每日 operator_inbox 含 ≥1 candidate」，還是「30 天內第一個 submission」？兩者導向不同的工程優先順序（前者重 detector + inbox，後者重 evidence packet + report tooling + 解一條 live lane）。
2. **方向檔權威**：本次審查包與 `engineering_direction_20260527.md`、`active_strategy_queue.md` 三者哪份為 single-source-of-truth？另兩份是否要 archive 或明文標記為 supersede chain？
3. **Operator gate 預算**：未來 30 天，operator 每週能投入多少分鐘做 owned account、OAuth、KYC、安全詞回覆、human-check？此數字決定有多少條 live lane 可被 unblock。
4. **目前的 Tier A live lane 選擇**：<program-redacted> 還是 <program-name>？或都 PARK，改新進 H1 fresh program（Discourse / Hex / Frontegg）？
5. **Hermes 後端授權**：是否同意切換到 `xai/grok-4.3` 或 `anthropic api key`（engineering_direction P3）？這影響 multi-agent 流程能否運作。
6. **Submission cadence 目標**：30 天內、90 天內期待達到的 informational/low/medium submission 數量？沒有數字 → 沒有「distracting」判準。
7. **`programs/` 收斂**：是否同意把已 PARKED 且短期不 reopen 的 program（<program-slug>、<program-redacted>、<program-redacted> TW）正式 `ARCHIVED`，停止在 navigation / queue 中佔位？
8. **可接受的 PASSIVE-ONLY 範圍**：對哪些 program、哪些 endpoint，passive fingerprint + version check 可在無逐次 operator 同意下執行（前提 scope/rules 允許）？

## 9. 與 Hermes 提案的 disagreement

| 項目 | Hermes 提案 | 我的看法 |
|---|---|---|
| 48h「清 worktree + 驗證」 | 偏輕，只做 commit 拆分 + 既有測試 | 應同時交付 `build_operator_inbox.py`（2 小時）與 Hermes 後端切換決定，否則 P2 與 P3 會持續延宕 |
| 7d「產出 inbox 3–5 件決定 + 推 1 條 lane」 | 把 inbox 與 live lane 推進綁在同 7 天 | 兩者性質不同：inbox 是純工程可控；live lane 推進完全受 operator gate 限制。應分開列，並明示後者前提 |
| 14d「跑完整 loop」 | 含「scope intake → 報告草稿」 | 現實是 evidence packet builder 與 report draft tooling 都還沒寫；先把 dry-run loop（用歷史 PARKED lane 資料）跑通比追求 live loop 更務實 |
| 30d「passive check 加 policy/scope gate 後啟用」 | 概念正確 | 缺：scheduler 必須能讀 per-program rate / technique budget / stop-before；否則 passive 啟用即逾界風險 |
| 90d「成熟為 bug bounty OS」 | 列出能力清單，無 outcome metric | 必綁可衡量輸出（candidates/月、submissions/月、redaction violations 數 = 0）。沒有 metric，3 個月後可能又是「能力齊備、submission = 0」 |
| 提案未提 | — | (a) `engineering_direction_20260527.md` 既有 P1–P5 backlog 的 supersede 關係；(b) Hermes 後端 adapter 壞掉的 routing 風險；(c) `handoff/` 根目錄歷史殘留的 CI-level 收斂機制；(d) 已 PARKED program 的 archive 紀律 |

---

**Summary**: 願景 coherent；提案方向正確但偏軟、未處理 operator-gate 阻塞與多份方向檔權威衝突。建議 Hermes 在採納本回覆後，**edit 既有的 `engineering_direction_20260527.md`**（依其自身規則）整合本次審查決議，而非再開新方向檔。