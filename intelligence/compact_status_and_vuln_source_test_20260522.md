> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Compact status and vulnerability-source test handoff

Generated: 2026-05-22 19:05 +0800
Route/tool: Hermes coordinator on Windows Git-Bash + Kali SSH. Exact model/runtime hidden by host; no Claude/Codex usage JSON for this slice.

## Testing宗旨 / 目標

目前專案不是為了堆很多掃描結果，而是建立一套可回收、可驗證、可轉成未來授權 bug-bounty/pentest 候選發現的 local-lab 工作流：

1. 只在授權 local lab / CTF / 自有或明確 scope 目標上執行 target-touching 測試。
2. 一次盡量證明一個漏洞行為或一個能力 lane，避免混成大雜燴。
3. 來源驅動：OWASP/lab、CISA KEV、NVD/CVE、Exploit-DB、GitHub 工具/PoC、HTB 模式都可作為 backlog/靈感，但不能把產品 CVE 套到不相符的 lab 元件上。
4. public exploit 預設只當參考，不 raw execute；把安全核心概念改寫成 bounded local-lab runner。
5. 產物要能留下：前置健康檢查、輸入、輸出、post-health、限制、下一步；confirmed finding 需要人工驗證、impact、remediation、retest，不能自動宣稱。

## 現況整理

- Repo branch: `feat/p1-4-program-policy-boundary`.
- `handoff/latest_check.md` 最近一次顯示 Python compile OK、bash -n OK、lock clear。
- 漏洞來源覆蓋 snapshot: `handoff/vulnerability_source_coverage_inventory_20260522.md`。
  - actively represented: 5/6 source families.
  - verified lab-flow bundles: 14 at snapshot time; current `modules/bundles/` now has 42 md files.
  - HTB remains the main untested source family.
- 標註漏洞庫/來源：
  - CISA KEV: `cves/cisa_kev_catalog_latest.json`, `handoff/cisa_kev_owasp_cve_lab_mapping_20260522.md`.
  - NVD/CVE: `cves/nvd_recent_modified_20260522.json`, `cves/CVE-2026-43494_candidate.md`.
  - Exploit-DB refs: `setting/local/tool_acquisition/wave2_20260522/scripts/exploitdb/...`.
  - GitHub tooling refs: `setting/local/tool_acquisition/wave2_20260522/repos/{ffuf,dalfox,Arjun,XSStrike,jwt_tool,PayloadsAllTheThings}`.

## VM / aggressive lab 狀態

VirtualBox currently shows:

- Working attacker VM: `kali-linux-2026.1-virtualbox-amd64`, path `<user-home>\Desktop\kali\kali-linux-2026.1-virtualbox-amd64.vbox`, state running, host-only IP `<lab-ip>`.
- Victim VM: `<victim-vm>`, path `<user-home>\Desktop\kali_terget\<victim-vm>\<victim-vm>.vbox`, state running after reset, host-only IP `<lab-ip>`.
- Stale/inaccessible registered VM entry: `<inaccessible>` UUID `{5764e0cc-bee0-404b-a8f6-3bd808744326}`, old path `<user-home>\VirtualBox VMs\<attacker-vm>\<attacker-vm>.vbox`; that config says `aborted="true"` and is not the VM we actually use now.

Interpretation:

- `AGGRESSIVE LAB 不可存取` was most likely confusion/VirtualBox stale registration: the old `<attacker-vm>` entry is inaccessible, while the actual active attacker VM is named `kali-linux-2026.1-virtualbox-amd64`.
- The attacker VM was started successfully; SSH initially timed out only while booting, then became reachable.
- The victim VM also needed a reset because SSH did not come up after start; after reset it was reachable.
- No evidence that installed tools were erased. No full redownload is needed right now.

## Tool state

On attacker VM:

- Present in PATH: `ffuf`, `nikto`, `nmap`, `sqlmap`, `nuclei`, `chromium`, `docker`, `python3`, `curl`, `git`.
- Not globally installed: `arjun`, `dalfox`, `jwt_tool` as commands.
- Source repos exist under the shared repo and can be invoked/reviewed from `/mnt/hacking/setting/local/tool_acquisition/wave2_20260522/repos/...`.
- Internet is intentionally closed/unreachable from the host-only attacker route; this is expected for lab isolation unless temporarily opening NAT for installs.

On victim VM:

- Docker images still present: `bkimminich/juice-shop:latest`, `webgoat/webgoat:latest`, `vulnerables/web-dvwa:latest`.
- `juice-shop-lab` was restarted and health from attacker is `http://<lab-ip>:3000/ -> 200`.
- `webgoat-lab` is reachable via redirect `http://<lab-ip>:8080/WebGoat/ -> 302` though Docker health reported unhealthy during warmup.
- DVWA image exists, but the DVWA container was not listed in the latest victim `docker ps -a` output; recreate/start only when returning to DVWA command-injection lane.

## Test run performed after整理

Lane: GitHub-source / Arjun-inspired bounded parameter discovery against authorized local Juice Shop.

Why this lane:

- `handoff/script_acquisition_wave2_20260522.md` explicitly recommended Arjun as next usage: bounded parameter discovery.
- It is lower-risk than kernel/<specific-cve-id> crash/LPE testing and avoids raw Exploit-DB execution.
- It helps find parameter surfaces that can later feed XSS/access-control/file/path lanes.

Attempt 1 and retry:

- Direct `python3 /mnt/hacking/.../Arjun/arjun/__main__.py` failed because Python package path was wrong.
- `cd Arjun && python3 -m arjun` loaded the package but failed because dependency `ratelimit` is missing.
- Because the attacker VM has no internet/DNS in host-only isolation, I did not install/download dependencies during this run.

Fallback actually executed:

- Bounded stdlib Python parameter probe using the same Arjun-style idea and a 20-param curated wordlist.
- Targets:
  - `http://<lab-ip>:3000/rest/products/search`
  - `http://<lab-ip>:3000/rest/user/login`
  - `http://<lab-ip>:3000/api/Products`
- Probe count: 3 targets x 20 params = 60 GET probes.
- Artifact: `<artifact-output-dir>/source_driven_param_discovery_fallback_retry_20260522T110522Z/`.
- Post-health:
  - Juice Shop: `200`
  - WebGoat: `302`

Result summary:

- `targets=3 params=20 probes=60 interesting=25`.
- Strongest useful lead: `q` on `/rest/products/search` changed body length `16563 -> 30`, consistent with known search parameter behavior.
- `/api/Products` showed possible params/effects:
  - `q`: `16011 -> 30`
  - `id`: `16011 -> 30`
  - `sort`: `200 -> 400`, `16011 -> 104`
  - `name`: `16011 -> 30`
- `/rest/user/login` returned baseline `500`; many params changed error body length slightly, but this is noisy and not a finding.

Interpretation:

- This is candidate/observation only, not a vulnerability proof.
- The useful output is a parameter-surface map that can seed the next bounded lane.
- It confirms the source-driven tool idea is usable, but the real Arjun command needs dependencies installed or vendored before proper use.

## Next recommended lane

1. Turn the parameter discovery fallback into a reusable `scripts/lab_modules/` module or install Arjun dependencies during a deliberate temporary NAT window.
2. Use discovered `q`, `id`, `sort`, `name` on Juice Shop for one of these bounded one-vuln lanes:
   - XSS runtime proof with Chromium if a reflected/runtime sink exists.
   - SQLi/search behavior proof if a safe known Juice Shop challenge route is selected.
   - Access-control/object-boundary proof only with explicit user/session setup.
3. Keep `<specific-cve-id>` in kernel/local candidate lane only; no crash/LPE/module-loading unless snapshot/recovery gate is explicitly approved.
4. HTB remains a source-family gap; schedule later as a separate CTF/training target lane.
