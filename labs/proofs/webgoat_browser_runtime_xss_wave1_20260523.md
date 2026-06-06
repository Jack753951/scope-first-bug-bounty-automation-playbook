> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# WebGoat Browser Runtime XSS Wave 1

Status: completed / local-lab browser runtime safe-marker proof
Date: 2026-05-23
Route/tool: Windows Hermes control plane -> `<attacker-vm>` (`<lab-ip>`) -> Docker-backed WebGoat on `<victim-vm>` (`<lab-ip>:8080`) using Kali `chromium` through a minimal Chrome DevTools Protocol helper
Target: `http://<lab-ip>:8080/WebGoat`
OWASP mapping: A03:2021 Injection / Cross-Site Scripting; 2025 migration track: injection/XSS proof capability
Artifacts:
- remote: `/home/kali/<artifact-output-dir>/webgoat_browser_runtime_xss_20260523T030746Z/`
- pulled: `<artifact-output-dir>/webgoat_browser_runtime_xss_20260523T030746Z/`
Scripts:
- `scripts/labs/webgoat_browser_runtime_xss_wave1.sh`
- `scripts/labs/cdp_runtime_xss.py`

## Scope and boundaries

- Authorized local lab only.
- Target was Docker-backed WebGoat on the local `<victim-vm>` VM.
- The wave used a throwaway WebGoat account and a unique marker only.
- No public/third-party target, no credential theft, no token/cookie exfiltration, no external callback/OAST, no persistence, no shell, no destructive write, and no report/finding promotion.
- This is a browser-runtime safe-marker proof. The evidence proves a WebGoat XSS training endpoint can return attacker-controlled HTML which, when rendered in a browser DOM sink on the WebGoat origin, mutates the DOM with the expected marker. It does not claim a real-world reportable finding outside the lab.

## Route and recovery posture

Pre/post route checks:

- `<attacker-vm>`: running, NIC1 host-only, NIC2/NAT null/off, snapshot label `clean-attacker-v2-tools-4096m-4cpu-20260522`.
- `<victim-vm>`: running, NIC1 host-only, NIC2/NAT null/off, snapshot label `setup-complete-with-tools`.
- Attacker guest route after the wave: only `<lab-ip>/24` plus Docker bridge; no default Internet route.
- Attacker guest Internet test after the wave: `Network is unreachable` / `internet_closed`.
- WebGoat post-health after the wave: `/WebGoat/login` returned HTTP 200.
- Snapshot restore was not required.

## Proof summary

The runner registered/logged in a short throwaway WebGoat user, fetched the CrossSiteScripting lesson, then used Chromium/CDP to:

1. set the lab `JSESSIONID` cookie in a headless browser context;
2. navigate to `/WebGoat/CrossSiteScripting/attack5a` with a bounded `field1` payload;
3. render the endpoint's JSON `output` into a same-origin browser DOM sink for runtime validation;
4. verify the payload mutated `document.body` with a unique marker;
5. repeat a control request whose reflected marker text did not create `data-xss`.

Unique marker:

```text
WG_XSS_RUNTIME_webgoat_browser_runtime_xss_20260523T030746Z
```

Verified browser result from `xss/browser_result.json`:

```json
{
  "attrs": {
    "xss": "WG_XSS_RUNTIME_webgoat_browser_runtime_xss_20260523T030746Z",
    "origin": "http://<lab-ip>:8080",
    "path": "/WebGoat/CrossSiteScripting/attack5a"
  },
  "control_attrs": {
    "xss": null,
    "origin": "http://<lab-ip>:8080",
    "path": "/WebGoat/CrossSiteScripting/attack5a"
  }
}
```

Runner summary:

```text
pre_health: 200
post_health: 200
register_status: 302
login_status: 302
lesson_status: 200
runtime_marker: yes
```

## Evidence files

Primary evidence:

- `<artifact-output-dir>/webgoat_browser_runtime_xss_20260523T030746Z/summary.md`
- `<artifact-output-dir>/webgoat_browser_runtime_xss_20260523T030746Z/observations.jsonl`
- `<artifact-output-dir>/webgoat_browser_runtime_xss_20260523T030746Z/xss/browser_result.json`
- `<artifact-output-dir>/webgoat_browser_runtime_xss_20260523T030746Z/xss/dom.html`
- `<artifact-output-dir>/webgoat_browser_runtime_xss_20260523T030746Z/xss/control_dom.html`
- `<artifact-output-dir>/webgoat_browser_runtime_xss_20260523T030746Z/xss/payload.html`
- `<artifact-output-dir>/webgoat_browser_runtime_xss_20260523T030746Z/xss/xss_url.txt`
- `<artifact-output-dir>/webgoat_browser_runtime_xss_20260523T030746Z/xss/control_url.txt`
- `<artifact-output-dir>/webgoat_browser_runtime_xss_20260523T030746Z/browser/xss_page.png`

Supporting session artifacts:

- `http/registration.html`
- `http/register_post.html`
- `http/start.html`
- `http/CrossSiteScripting.lesson.html`
- `http/cookies.txt` (lab-only throwaway session artifact; do not publish)

## Controls / false-positive boundary

- Control request reflected marker-like text but did not set `document.body[data-xss]`.
- The proof checks browser runtime state, not just raw text reflection.
- The proof labels origin/path so future review can detect wrong-context execution.
- This wave intentionally avoids `alert(document.cookie)`, cookie reads, credential prompts, token exfiltration, redirects, persistence, and external callbacks.
- Important limitation: because direct `/attack5a` returns JSON, the CDP helper renders the JSON `output` into a browser DOM sink for validation instead of relying on a manual lesson-page UI click. Treat this as a verified local-lab runtime-sink proof and a reusable browser-proof pattern, not as a public-target report by itself.

## Rerun commands

From Windows/Git-Bash at `<private-workspace>`:

```bash
powershell.exe -NoProfile -ExecutionPolicy Bypass -File ./scripts/kali-run.ps1 -Command 'cd /mnt/hacking && bash scripts/labs/webgoat_browser_runtime_xss_wave1.sh'
MSYS2_ARG_CONV_EXCL='*' powershell.exe -NoProfile -ExecutionPolicy Bypass -File ./scripts/kali-pull.ps1 -RemotePath '/home/kali/<artifact-output-dir>/<run_id>'
```

Validation used in this wave:

```bash
python -m py_compile scripts/labs/cdp_runtime_xss.py
bash -n scripts/labs/webgoat_browser_runtime_xss_wave1.sh
powershell.exe -NoProfile -ExecutionPolicy Bypass -File ./scripts/kali-run.ps1 -Command 'cd /mnt/hacking && bash scripts/labs/webgoat_browser_runtime_xss_wave1.sh'
MSYS2_ARG_CONV_EXCL='*' powershell.exe -NoProfile -ExecutionPolicy Bypass -File ./scripts/kali-pull.ps1 -RemotePath '/home/kali/<artifact-output-dir>/webgoat_browser_runtime_xss_20260523T030746Z'
```

## Report-readiness

Decision: `local_learning` / `reusable_methodology`.

This is useful as a local proof-pattern and evidence-packet building block. It is not report-ready for any real program until scope/rules, rate limits, manual browser proof on the actual in-scope application, safe payload policy, redaction, and report-readiness gates are satisfied.

## 對專案有什麼幫助

- 把「XSS 不是只有反射字串」固定成可重跑的 browser-runtime marker 證據：DOM state、origin、path、positive/control 都保存。
- 補上先前 WebGoat authenticated wave 中「browser evidence deferred」的缺口，並把 Kali Playwright driver 壞掉的問題繞成較小、可維護的 CDP helper。
- 強化 one-vuln proof packet 的形狀：有 pre/post health、route/NAT posture、runtime evidence、control、artifact pullback、limitation wording。
- 給後續 Juice Shop / modern_vuln_api / 真實授權範圍前的 browser proof lane 一個較穩定的校準基準。

## 新增/更新了什麼

- Added `scripts/labs/webgoat_browser_runtime_xss_wave1.sh`.
- Added `scripts/labs/cdp_runtime_xss.py`.
- Added pulled artifacts under `<artifact-output-dir>/webgoat_browser_runtime_xss_20260523T030746Z/`.
- Added this handoff: `handoff/webgoat_browser_runtime_xss_wave1_20260523.md`.
- Added reusable bundle: `modules/bundles/verified_lab_flow_webgoat_browser_runtime_xss_safe_marker.md`.
- Updated `scripts/SCRIPT_INVENTORY.md`, `handoff/accepted_changes.md`, `handoff/current_navigation.md`, and Obsidian Cybersec Lab note.

## Next lanes

1. File read / path traversal / XXE safe-marker proof packet, using lab-owned marker files only.
2. If continuing XSS, improve this from CDP-rendered output to full WebGoat lesson-page UI interaction or repeat the same proof against a target whose vulnerable endpoint directly renders HTML in-app.
3. Keep public/real bug bounty activation parked until local proof packets and report-readiness gates are stable.
