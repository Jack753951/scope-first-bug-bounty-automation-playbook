> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Security Scripts

這個資料夾放自動化腳本與安全輔助工具。它們的用途是協助合法授權的 recon、triage、defense audit 與 report evidence collection，而不是取代人工判斷。

執行前請先看 [INDEX.md](INDEX.md)，確認用途、依賴、輸出與風險。

## 安全使用規則

- 只對 lab、CTF、自己擁有的資產、或書面授權 scope 內的目標使用。
- 任何 scanner hit 都必須人工驗證。
- 對真實目標執行前先建立 scope 檔案，包含 allowlist、out-of-scope、速率限制與禁止行為。
- 不要把 token、cookie、API key、客戶資料或敏感證據存進 repo。
- 優先使用最小、非破壞性 proof。不要為了證明漏洞而擴大影響。

## 主要 Python 工作流

| Script | Purpose | Output |
| --- | --- | --- |
| `recon_automation.py` | 授權目標偵查：whois、DNS、subdomain、Nmap。 | JSON + Markdown recon summary。 |
| `vuln_scan_integration.py` | 整合 nuclei、nikto、whatweb 等掃描結果。 | JSON + Markdown vulnerability summary。 |
| `passive_target_search.py` | 產生 passive/public target-search queries 與 first-bounty triage template；不發網路請求、不開 browser、不碰 live target。 | JSON/Markdown query pack。 |
| `module_runner.py` | P2-4/P2-13 dry-run-only module runner skeleton：可手動指定 manifest，或以 `--discover-root <repo>` 離線枚舉 `modules/checks/**/module.json`；profile 由 repo-local `modules/profiles/<profile>.json` 資料檔驅動，目前保守 profile 為 `audit-baseline`。驗證 module manifest、module profile 與 policy allow artifact 後產生 `run/1.0` planned manifest preview；加上 `--include-module-io-preview` 時只額外輸出 P2-10 `module_input/1.0` / `module_result/1.0` preview envelopes，並在回傳 allow 前以 P2-11/P2-12 bundle consistency validator 檢查 run/input/result 交叉一致性；result 狀態保持 `not_executed`。加上 `--persist-preview-bundle` 時，必須同時啟用 module I/O preview 並提供 explicit repo root，且只有所有 gates allow 後才會寫入 repo-local `runs/<run_id>/preview/` 的資料型 JSON artifacts。profile loader/selection failures 會保留人類可讀 errors/warnings，並額外輸出穩定 `error_codes` / `warning_codes` / details；profile issue constants/detail helpers 集中於 `profile_issues.py`。 | JSON plan payload；選用 preview bundle artifacts；不執行 module、scanner、subprocess 或網路動作。 |
| `lab_modules/wave1a_metadata.py` | Phase 4B Wave 1A reusable bounded local-lab adapter：把 directory listing、robots/security.txt、api-docs、dependency/API metadata、CORS metadata 這批 Level 1 module manifests 接成可調用的 lab-only plan/script generator。預設只輸出 plan；必須加 `--lab-approved --write-script <path>` 才會產生 bash 腳本。 | JSON plan；選用 bash script；只允許 local/private lab URL、固定 known paths/CORS origins、request cap、timeout、rate limit、pre/post health、JSONL observations；不遞迴、不抓檔、不跑 exploit/callback、不升級 finding。 |
| `import_wave1a_metadata_observations.py` | Phase 4B Wave 1A offline observation importer：讀取已審查/fixture 化的 `wave1a_metadata.py` JSONL observations，正規化成 non-promotional observations 與 manual-review candidate seeds。 | JSON only；只允許 `tests/fixtures/wave1a_metadata/*.jsonl`；不網路、不 subprocess、不碰目標、不讀 raw body、不輸出 confirmed/verified/reportable/accepted。 |
| `build_wave1a_candidate_review_fixture.py` | Phase 4B Wave 1A candidate-review bridge：把 importer 產生的 manual-review candidate seeds 轉成 `finding/1.0` candidate fixture list，並用既有 P2.19 vocabulary 在記憶體中產生 `candidate_review_packet/0.1-trial`。 | JSON only；預設不寫檔；不網路、不 subprocess、不碰目標、不 draft/submit report、不輸出 confirmed/verified/reportable/accepted；CLI 拒絕 live target flags。 |
| `build_wave1a_review_chain.py` | Phase 4B Wave 1A offline review-chain builder：從 Wave1A observation fixture 走 importer → candidate-review bridge → `candidate_review_packet/0.1-trial` → gap report → verification plan → report-readiness gate。 | JSON only；預設不寫檔；不網路、不 subprocess、不碰目標、不 draft/submit report、不輸出 confirmed/verified/reportable/accepted/ready_for_submission；上游失敗時 fail-closed 且不產生後續 stage。 |
| `validate_module_io_contract.py` | P2-10 standard-library-only validator for offline `module_input/1.0` and `module_result/1.0` JSON contracts. It fails closed on non-dry-run, target-touching, network, unsafe constraints, path traversal, unknown fields, completed result status, or non-empty findings/evidence. | JSON validation verdict；不 import module code、不執行 subprocess、不開網路、不碰目標。 |
| `validate_module_io_bundle.py` | P2-11/P2-12 standard-library-only validator for offline module I/O preview bundles. It cross-checks a planned `run/1.0` document with parallel `module_input/1.0` and `module_result/1.0` previews, denying missing/duplicate/extra pairs, mismatched run/module/policy/profile/program/target/hash fields, malformed paths, unsafe result states, timestamp drift, or non-empty findings/evidence. P2-13 runner persistence consumes only an `allow` bundle report and stores that report as data. | JSON validation verdict；validator 本身不寫 ledger、不執行 module、不開網路、不碰目標。 |
| `validate_preview_manifest.py` | P2-14 standard-library-only, read-only validator for already-persisted `preview_manifest/1.0` bundles under `runs/<run_id>/preview/`. It rejects malformed or duplicate-key JSON, unknown fields, unsafe run IDs/relative paths, symlinks, missing or extra artifacts, hash/size drift, and non-allow bundle consistency output. | Single JSON validation verdict; no writes, repairs, module execution, scanner/network/process launch, target touching, findings, evidence, or reports. |
| `validate_preview_ledger.py` | P2-15 standard-library-only, read-only validator for offline `preview_ledger/1.0` manifest-of-manifests indexes. It requires an explicit `--repo-root`, rejects strict-version/path/hash/size/timestamp/duplicate/symlink drift, and hashes only referenced `preview_manifest.json` files. | Single-line JSON validation verdict; no writes, repairs, builder/indexer behavior, module execution, scanner/network/process launch, callbacks, target touching, findings, evidence, or reports. |
| `ctf_prepare_challenge.py` | P2.17 offline/local CTF artifact scaffold. Creates `setting/local/ctf/<slug>/challenge.json` and `solve_notes.md` with output-side review checklist. Slug must be operator-supplied; external service interaction remains Kali-first. | JSON status report; writes only local ignored CTF notes/artifacts; no network, subprocess, scanner/module execution, callbacks, or target touching. |
| `ctf_review_decision.py` | P2.17 pure CTF result classifier over a JSON solver/result payload. Separates `hint` / `candidate` / `verified` / `needs_second_review`, confidence, ignored override fields, and escalation triggers such as abnormal format, multiple candidates, solver timeout, external-source-only, and UI/checker-only. | Deterministic JSON decision; no network, subprocess, scanner/module imports, target touching, findings/evidence/report promotion, or schema/runtime wiring. |
| `lint_ctf_verifier_metadata.py` | P2.18 trial-only, non-binding linter for flat CTF verifier metadata descriptors under `tests/fixtures/ctf_verifier_metadata/`. It is a vocabulary trial before any P2.19+ schema/registry promotion and denies unknown/forbidden fields, unsafe YAML syntax, boolean-string drift, active-service descriptors without `kali_required: true` and `requires_scope: true`, and host-execution affordances. | Deterministic JSON to stdout only; read-only, standard-library-only, no output file writes, network, subprocess, scanner/module imports, runtime consumers, schema promotion, target touching, findings, evidence, or reports. |
| `build_candidate_review_packet.py` | P2.19 trial-only bug-bounty candidate review packet builder. It reads only allowlisted committed `expected_findings.json` fixtures, validates `finding/1.0` candidate data, preserves manual-verification/scanner-output guardrails, and emits deterministic review questions plus non-promotional `report_readiness` for human triage. | Deterministic JSON to stdout only; read-only, standard-library-only, no output file writes, network, subprocess, scanner/module runtime imports, live target access, schema promotion, platform adapter, report drafting, or status promotion. |
| `review_candidate_packet_gaps.py` | P2.20 trial-only bug-bounty candidate review packet gap/action consumer. It reads one `candidate_review_packet/0.1-trial` JSON document from stdin, validates the packet boundary, and emits deterministic per-finding triage gap/action codes for human review. | Deterministic JSON to stdout only; stdin-only, read-only, standard-library-only, no file input/output options, no output file writes, network, subprocess, scanner/module runtime imports, live target flags, schema promotion, platform adapter, report drafting, or status promotion. |
| `build_candidate_verification_plan.py` | P2.21 trial-only bug-bounty candidate verification checklist consumer. It reads one `candidate_review_gap_report/0.1-trial` JSON document from stdin, validates the gap-report boundary, and emits deterministic per-finding human checklist items while preserving `blocked` / `needs_manual_review` states below confirmation language. | Deterministic JSON to stdout only; stdin-only, read-only, standard-library-only, no file input/output options, no output file writes, network, subprocess, scanner/module runtime imports, live target flags, schema promotion, platform adapter, report drafting, or status promotion. |
| `build_report_readiness_gate.py` | P2.22 trial-only bug-bounty report-readiness gate consumer. It reads one `candidate_verification_plan/0.1-trial` JSON document from stdin, validates the checklist boundary, and emits deterministic per-finding gate actions while preserving only `blocked` / `needs_manual_review` states below report-confirmation language. | Deterministic JSON to stdout only; stdin-only, read-only, standard-library-only, no file input/output options, no output file writes, network, subprocess, scanner/module runtime imports, live target flags, schema promotion, platform adapter, report drafting, report submission adapter, or status promotion. |
| `build_candidate_workflow_fixture.py` | P2.23 trial-only offline end-to-end bug-bounty candidate workflow fixture builder. It chains committed finding fixtures through P2.19 review packet, P2.20 gap report, P2.21 verification plan, and P2.22 report-readiness gate helpers in memory to prove the deterministic triage workflow. P3.1 adds curated near-real synthetic cases under `tests/fixtures/candidate_review_packet/p3_1_curated_*` to stress vocabulary coverage while staying at `finding/1.0` / `0.1-trial`; these fixtures must not be promoted to importer, scanner-output, platform-adapter, or report-submission fixtures without a fresh OSS Recon Gate. | Deterministic JSON to stdout only; reads only P2.19-allowlisted committed fixtures, standard-library-only, no output file writes, network, subprocess, scanner/module runtime imports, live target flags, schema promotion, platform adapter, report drafting, report submission adapter, runtime wiring, or status promotion. |
| `profile_issues.py` | P2-9 standard-library-only shared profile issue vocabulary/helper layer for stable profile codes and `error_details` / `warning_details` object serialization. | Imported helper only；不讀寫檔案、不執行 module、不觸碰網路或目標。 |

P3.3 note: `modules/checks/level1/` contains two committed dry-run-safe modules selected by `audit-baseline` (`policy_decision_metadata_audit` and `security_headers_baseline`). `scripts/test_module_runner.py` exercises two-module discovery and module I/O bundle consistency; `module_runner.py` still loads module manifests as data only and does not import or execute module `check.py` files. P3.4-alt pins that runner-indifference property with tests that add a deliberately broken `check.py` beside the manifest-only module and remove `check.py` from the evaluator-backed module in fixture repos; discovery, CLI planning, and preview bundles remain unchanged.

P3.5 note: `templates/report_readiness_reviewer_prompts.json` is a data-only reviewer-prompt catalog keyed to existing report-readiness gate, block-reason, and check codes. The catalog is deliberately not a `*/0.1-trial` schema, has only a flat marker, and is not read by any workflow consumer, validator, runner, scanner, renderer, or report generator; tests only assert JSON shape, coverage, deterministic ordering, and forbidden vocabulary locks. No reviewer-notes artifact, report drafting, submission adapter, platform adapter, runtime wiring, live-target flag, or P2.24 helper-extraction trigger is introduced by the catalog.

## Kali SSH Helpers

| Script | Purpose | Note |
| --- | --- | --- |
| `kali-install-key.ps1` | 用一次密碼登入把專案公鑰裝進 Kali。 | 只對你的 Kali VM 使用，不保存密碼。 |
| `kali-check-tools.ps1` | 透過 SSH 檢查 Kali 裡常見 pentest 工具是否存在。 | 只做版本/路徑檢查，不掃描目標。 |
| `kali-run.ps1` | 從 Windows/Hermes/Codex 透過 SSH 呼叫 Kali 工具。 | 只對 lab、自有資產或授權 scope 使用。 |
| `kali-browser-ops.ps1` | Kali/noVNC browser remote-control primitives：status、open、browser-reset、screenshot、click、type、hotkey、downloads、CDP tab metadata/visible text。 | 只作 GUI/browser 操作輔助；不要用 `type` 傳密碼、OTP、token、cookie、phone；live target URL 仍需 scope/policy gate。 |
| `kali-passive-browse.ps1` | End-to-end passive browser helper：必要時啟動 Kali、確保 temporary NAT route、啟動 noVNC tunnel、開 URL、抽 sanitized visible text/gate flags；可用 `-CloseNatAfter` 結束後關 NAT。 | 只做 passive/public browsing；看到 OTP/CAPTCHA/login-secret/phone/payment/KYC/scarce-claim/live-test gate 就停。 |
| `kali-pull.ps1` | 把 Kali 的 `~/codex-output` 拉回 `<artifact-output-dir>/`。 | 先審查再移進正式 reports 或 notes。 |

## Shell Helpers

| Script | Purpose | Note |
| --- | --- | --- |
| `gen_report.sh` | Generate an offline Markdown draft report from an existing scan directory. | Does not scan targets or send network traffic; scanner output remains triage until manually verified; DOCX requires explicit format request plus local `pandoc`. |
| `subdomain_recon.sh` | 子網域與 HTTP probe。 | 僅限授權 domain，注意速率。 |
| `subdomain_takeover.sh` | dangling DNS / takeover 線索。 | 只做 triage，不接管第三方服務。 |
| `xss_finder.sh` | XSS 反射或行為線索。 | 需要 Burp 或人工 context 驗證。 |
| `sqli_triage.sh` | SQLi 線索 triage。 | 避免 heavy / destructive 測試。 |
| `ssrf_finder.sh` | SSRF OOB 線索。 | 只用核准的 callback infrastructure。 |
| `lfi_finder.sh` | LFI / path traversal 線索。 | 只收集最小證據。 |
| `open_redirect.sh` | open redirect 檢查。 | 避免使用惡意或品牌冒用 destination。 |
| `cors_audit.sh` | CORS header 行為檢查。 | CORS misconfig 需要確認 exploitability。 |
| `jwt_inspect.sh` | JWT 結構與弱設定檢查。 | 不儲存真實 secret，不未授權破解。 |
| `headers_audit.sh` | Security headers / cookie flags 檢查。 | 適合作為 defense baseline。 |
| `kali_audit.sh` | Kali 本機工具與環境盤點。 | 本機 defensive inventory。 |
| `setup_kali.sh` | 安裝或設定 Kali 工具。 | 執行前先審閱，因為會改變環境。 |

## 改進 Backlog

- 新增共用 `--scope scope.json`，讓會碰目標的腳本先檢查 allowlist。
- 新增 `--dry-run`，顯示將執行的工具與命令但不真正掃描。
- 統一輸出命名、timestamp、tool version、command provenance。
- 建立 sample outputs，讓 parser 與 report generator 可以離線測試。
- 為每個腳本加入清楚的 dependency check 與錯誤訊息。
