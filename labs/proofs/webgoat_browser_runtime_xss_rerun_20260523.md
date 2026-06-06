> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# WebGoat Browser Runtime XSS Rerun — 2026-05-23

Status: completed / verified local-lab runtime proof rerun
Date: 2026-05-23
Route/tool: Windows Hermes control plane -> `scripts/kali-run.ps1` -> `<attacker-vm>` (`<lab-ip>`) -> Kali Chromium/CDP helper -> Docker-backed WebGoat on `<victim-vm>` (`<lab-ip>:8080`)
Target: `http://<lab-ip>:8080/WebGoat/CrossSiteScripting/attack5a`
OWASP mapping: A03:2021 Injection / Cross-Site Scripting; 2025 migration track: browser-runtime XSS proof capability
Artifacts:
- remote: `/home/kali/<artifact-output-dir>/webgoat_browser_runtime_xss_20260523T105506Z/`
- pulled: `<artifact-output-dir>/webgoat_browser_runtime_xss_20260523T105506Z/`
Scripts:
- `scripts/labs/webgoat_browser_runtime_xss_wave1.sh`
- `scripts/labs/cdp_runtime_xss.py`

## Scope and boundaries

- Authorized local lab only.
- Target was Docker-backed WebGoat on the local `<victim-vm>` VM.
- The wave used a throwaway WebGoat account and a unique safe DOM marker only.
- No public/third-party target, no credential theft, no token/cookie exfiltration, no external callback/OAST, no persistence, no shell, no destructive write, and no report/finding promotion.
- This rerun validates the existing WebGoat browser-runtime safe-marker pattern; it does not expand scope to real programs.

## Pre/post route and recovery posture

Pre-route audit from `<attacker-vm>` before target-touching work:

```text
hostname: kali
attacker_ip: <lab-ip>/24
routes: <lab-ip>/24 plus Docker bridge only
internet: internet_closed
```

Post-route audit after artifact pullback:

```text
routes: <lab-ip>/24 plus Docker bridge only
internet: internet_closed
WebGoat login health: HTTP/1.1 200
```

Snapshot restore was not required.

## Proof summary

Runner result from `summary.md`:

```text
pre_health: 200
post_health: 200
register_status: 302
login_status: 302
lesson_status: 200
marker: WG_XSS_RUNTIME_webgoat_browser_runtime_xss_20260523T105506Z
runtime_marker: yes
```

Primary browser evidence from `xss/browser_result.json`:

```json
{
  "attrs": {
    "xss": "WG_XSS_RUNTIME_webgoat_browser_runtime_xss_20260523T105506Z",
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

Interpretation: the positive browser run mutated DOM state with the expected marker on the WebGoat origin/path, while the control request did not set `data-xss`. This supports `verified local-lab browser-runtime reflected XSS safe-marker proof`, not merely text reflection.

## Evidence files

Primary evidence:

- `<artifact-output-dir>/webgoat_browser_runtime_xss_20260523T105506Z/summary.md`
- `<artifact-output-dir>/webgoat_browser_runtime_xss_20260523T105506Z/observations.jsonl`
- `<artifact-output-dir>/webgoat_browser_runtime_xss_20260523T105506Z/xss/browser_result.json`
- `<artifact-output-dir>/webgoat_browser_runtime_xss_20260523T105506Z/xss/dom.html`
- `<artifact-output-dir>/webgoat_browser_runtime_xss_20260523T105506Z/xss/control_dom.html`
- `<artifact-output-dir>/webgoat_browser_runtime_xss_20260523T105506Z/browser/xss_page.png`

Supporting session artifacts:

- `http/registration.html`
- `http/register_post.html`
- `http/start.html`
- `http/CrossSiteScripting.lesson.html`
- `http/cookies.txt` (lab-only throwaway session artifact; do not publish)

## Controls / false-positive boundary

- Control request reflected marker-like text but did not set `document.body[data-xss]`.
- The proof checks browser runtime state, not only raw response reflection.
- Origin and path are preserved so future review can detect wrong-context execution.
- Payload avoids `alert(document.cookie)`, cookie reads, credential prompts, token exfiltration, redirects, persistence, and external callbacks.
- Limitation: the endpoint path is a WebGoat training route and this remains lab-only. Do not claim cross-user, persistent, credential-exfiltration, account-takeover, or production impact.

## Evidence review

Reviewer identity:

- Reviewer route/tool: Hermes `delegate_task` read-only artifact review
- Visible runtime model: `gpt-5.5` as reported by delegate tool
- Review focus: evidence quality and overclaim risk
- Limitation: artifact files do not expose the exact Chromium version or runner commit

Reviewer conclusion:

- Classification may remain `verified local-lab runtime proof` because runtime DOM mutation, origin/path binding, and a negative control are present.
- Do not downgrade to candidate-only.
- Keep classification strictly limited to authorized local WebGoat, single route, single throwaway session, safe DOM marker, no exfiltration/no persistence/no public target.

## Validation

```text
python -m py_compile scripts/labs/cdp_runtime_xss.py
bash -n scripts/labs/webgoat_browser_runtime_xss_wave1.sh
powershell.exe -NoProfile -ExecutionPolicy Bypass -File ./scripts/kali-run.ps1 -Command 'cd /mnt/hacking && bash scripts/labs/webgoat_browser_runtime_xss_wave1.sh'
MSYS2_ARG_CONV_EXCL='*' powershell.exe -NoProfile -ExecutionPolicy Bypass -File ./scripts/kali-pull.ps1 -RemotePath '/home/kali/<artifact-output-dir>/webgoat_browser_runtime_xss_20260523T105506Z'
python -m pytest -q scripts/test_lab_juice_shop_search_sqli_boolean_probe.py scripts/test_phase4b_three_exposure_bundles.py scripts/test_service_baseline_targets.py scripts/test_owasp_tool_wrapper_modules.py scripts/test_owasp_single_vuln_modules.py scripts/test_program_policy_boundary.py
```

Validation result:

```text
26 passed, 30 subtests passed in 8.89s
```

## Report-readiness

Decision: `local_learning` / `reusable_methodology`.

This is useful as a local proof-pattern and evidence-packet building block. It is not report-ready for any real program until scope/rules, rate limits, manual browser proof on the actual in-scope application, safe payload policy, redaction, and report-readiness gates are satisfied.

## 對專案有什麼幫助

- 驗證 `<attacker-vm>` 的預設攻擊路線仍可重跑 target-touching browser proof，且 NAT/Internet 維持關閉。
- 把 WebGoat XSS 從「之前做過」重新確認成可重跑的 browser-runtime evidence pattern：pre/post health、throwaway auth、DOM marker、origin/path、control、artifact pullback 都存在。
- 強化專案目前最需要的 local proof packet 能力：不是只看反射字串，而是能保存瀏覽器執行結果與 false-positive control。
- 支援下一步把 XSS proof packet hardening 做到 SSRF/DVWA evidence packet 同等標準。

## 新增/更新了什麼

- Added pulled rerun artifacts under `<artifact-output-dir>/webgoat_browser_runtime_xss_20260523T105506Z/`.
- Added this handoff: `handoff/webgoat_browser_runtime_xss_rerun_20260523.md`.
- Updated `handoff/accepted_changes.md` with the rerun result.
- Updated Obsidian Cybersec Lab note with the rerun result.
- Added temporary local health helper `setting/local/hermes_health_probe_20260523.sh` for this session's route checks.

## Next lanes

1. Promote this rerun into a compact XSS evidence packet if the next slice is documentation/report-readiness hardening.
2. If continuing target-touching tests, choose a different capability rather than rerunning this same route again: auth/session role separation, file-read packet rehearsal, or a second XSS target whose vulnerable endpoint directly renders HTML in-app.
3. Keep public/real bug bounty activation parked until local proof packets and report-readiness gates are stable.
