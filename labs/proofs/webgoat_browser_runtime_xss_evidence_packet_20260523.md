> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# WebGoat Browser-Runtime XSS Safe-Marker Evidence Packet

Status: completed / reusable_methodology / verified local-lab runtime proof
Source: Hermes synthesis of verified rerun artifacts + read-only artifact review
Date: 2026-05-23
Repo truth: `handoff/webgoat_browser_runtime_xss_rerun_20260523.md`, `modules/bundles/verified_lab_flow_webgoat_browser_runtime_xss_safe_marker.md`, `handoff/proof_library_index_20260523.md`
Run ID: `webgoat_browser_runtime_xss_20260523T105506Z`

## Reviewer identity

- Reviewer route/tool: Hermes local synthesis + Hermes `delegate_task` read-only artifact review
- Visible runtime model: local synthesis current session `gpt-5.5 / openai-codex`; delegate review reported `gpt-5.5`
- Provider / CLI version if visible: provider exposed as `openai-codex`; CLI wrapper version not exposed
- Review focus: evidence quality, false-positive boundary, reproducibility, report-readiness gate
- Limitation: browser artifact exposes CDP/Chromium behavior but not exact Chromium version; screenshot file exists but packet relies mainly on DOM/JSON artifacts, not image OCR.

## Target

- Target name: WebGoat browser-runtime XSS training route
- Target URL / service: `http://<lab-ip>:8080/WebGoat/CrossSiteScripting/attack5a`
- Victim route: `<victim-vm>` / Docker-backed WebGoat / `<lab-ip>:8080`
- Attacker/tool route: `<attacker-vm>` / Kali Chromium-CDP helper / `<lab-ip>`
- Artifact root: `<artifact-output-dir>/webgoat_browser_runtime_xss_20260523T105506Z/`

## Vulnerability class

- Class: Browser-runtime reflected XSS safe-marker proof
- OWASP / CWE mapping: OWASP A03:2021 Injection / Cross-Site Scripting; CWE-79; 2025 migration track: injection/XSS proof capability
- One-vulnerability boundary: one WebGoat CrossSiteScripting lesson route receives one bounded `field1` payload and is validated by browser DOM state plus a control request.
- Why this target demonstrates the class: the vulnerable training route reflects attacker-controlled HTML into a browser-rendered context; the payload executes in Chromium and mutates DOM attributes on the WebGoat origin/path.

## Authorized scope

- Scope basis: local intentionally vulnerable training lab only.
- Public/real target involved: no.
- Safety lane: `local-learning-lab`.
- Disallowed surfaces avoided: no public target, no credential theft, no token/cookie exfiltration, no external callback/OAST, no persistence, no shell/destructive write, no automatic finding/report promotion, and no production impact claim.

## Route/tool

- Control plane: Windows Hermes / repo `<private-workspace>`.
- Tool/attacker plane: `<attacker-vm>` using `scripts/labs/webgoat_browser_runtime_xss_wave1.sh` and `scripts/labs/cdp_runtime_xss.py`.
- Victim plane: `<victim-vm>` running Docker-backed WebGoat.
- Network posture: host-only local lab route.
- NAT status: attacker route checked before/after; Internet remained `internet_closed`.
- Tools/scripts used: curl for session/setup, Kali Chromium via CDP helper for browser runtime evidence, PowerShell SSH/SCP wrappers for run/pullback.

## Preconditions

- Attacker IP: `<lab-ip>`.
- Victim IP: `<lab-ip>`.
- Target service health: WebGoat login page returned HTTP 200 before and after the proof.
- Auth/session setup: runner registered/logged in a short throwaway WebGoat user; session cookie was used only for the local lab proof.
- Snapshot/recovery state: no snapshot restore required; target post-health stayed 200.

## Exploit/probe path

- Discovery path: WebGoat CrossSiteScripting lesson route and prior verified WebGoat browser-runtime proof pattern.
- Exact trigger path: `GET /WebGoat/CrossSiteScripting/attack5a?...&field1=<safe DOM marker payload>&field2=111&field3=webgoat`.
- Payload/command summary: an inert image error handler calls `document.body.setAttribute(...)` to set `data-xss`, `data-origin`, and `data-path`; it does not read cookies/tokens or call out.
- Request caps/timeouts/rate: one positive browser run plus one control browser run inside a single throwaway session.
- Why this is bounded: local training target, unique marker, safe DOM-only mutation, negative control, no exfiltration/callback/persistence, no public target.

## Evidence

Primary artifacts:

- Runner summary: `<artifact-output-dir>/webgoat_browser_runtime_xss_20260523T105506Z/summary.md`
- Observations: `<artifact-output-dir>/webgoat_browser_runtime_xss_20260523T105506Z/observations.jsonl`
- Browser result JSON: `<artifact-output-dir>/webgoat_browser_runtime_xss_20260523T105506Z/xss/browser_result.json`
- Positive DOM: `<artifact-output-dir>/webgoat_browser_runtime_xss_20260523T105506Z/xss/dom.html`
- Control DOM: `<artifact-output-dir>/webgoat_browser_runtime_xss_20260523T105506Z/xss/control_dom.html`
- Screenshot: `<artifact-output-dir>/webgoat_browser_runtime_xss_20260523T105506Z/browser/xss_page.png`
- Payload/URLs: `xss/payload.html`, `xss/xss_url.txt`, `xss/control_url.txt`

Verified summary values:

```text
pre_health: 200
post_health: 200
register_status: 302
login_status: 302
lesson_status: 200
marker: WG_XSS_RUNTIME_webgoat_browser_runtime_xss_20260523T105506Z
runtime_marker: yes
```

Primary browser evidence:

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

## Impact

- Verified impact: attacker-controlled safe marker JavaScript executed in a browser context and changed DOM state on the WebGoat origin/path.
- Maximum safe local-lab impact reached: browser-runtime proof with unique marker, origin/path label, authenticated lab session, positive DOM artifact, control DOM artifact, screenshot, and pre/post target health.
- Impact not claimed: credential theft, cookie/token access, account takeover, stored/persistent XSS, cross-user impact, production impact, public target finding, or report-ready bug bounty issue.
- Why this matters for future authorized assessment: it establishes the minimum evidence bar for XSS claims: runtime DOM/browser state plus negative control, not raw reflection alone.

## Controls / false-positive boundary

- Noisy possibility: raw reflected text can look like XSS without runtime execution.
- Exclusion: positive run produced `data-xss=<marker>` in browser result/DOM; control request reflected marker-like text but `control_attrs.xss` remained `null`.
- Context check: browser result records `origin=http://<lab-ip>:8080` and `path=/WebGoat/CrossSiteScripting/attack5a`.
- Remaining uncertainty: this is a WebGoat training route and a controlled lab session; a real target would require program scope, safe payload policy, manual browser validation, redaction, and report-readiness review.

## Cleanup

- Containers/processes removed: none created by this proof; WebGoat lab service remains a reusable local training target.
- Files/markers removed or intentionally left in disposable lab: no persistent marker file was written; artifacts retained under `<artifact-output-dir>/`.
- NAT/network restored: attacker route remained host-only; post-run Internet probe returned `internet_closed`.
- Snapshot/restore used: no snapshot restore required.
- Remaining cleanup debt: none recorded for this run.

## Rerun commands

Use only in the authorized local lab after confirming the active route and network posture.

```bash
cd <private-workspace>
python -m py_compile scripts/labs/cdp_runtime_xss.py
bash -n scripts/labs/webgoat_browser_runtime_xss_wave1.sh
powershell.exe -NoProfile -ExecutionPolicy Bypass -File ./scripts/kali-run.ps1 -Command 'cd /mnt/hacking && bash scripts/labs/webgoat_browser_runtime_xss_wave1.sh'
MSYS2_ARG_CONV_EXCL='*' powershell.exe -NoProfile -ExecutionPolicy Bypass -File ./scripts/kali-pull.ps1 -RemotePath '/home/kali/<artifact-output-dir>/<run_id>'
```

Rerun gate:

- Confirm `<attacker-vm>` is the attacker route and `<victim-vm>` is the victim route.
- Confirm WebGoat login health returns 200 before running.
- Use throwaway accounts only.
- Keep payload to safe DOM marker mutation only.
- Preserve positive and control artifacts.
- Do not use credential/cookie/token exfiltration payloads.

## Report-readiness

Decision: `reusable_methodology`

Reason: the local-lab proof is strong and evidence-complete for methodology reuse, but it is not a real bug bounty or pentest finding. It demonstrates the XSS evidence packet shape required before any public/authorized assessment lane.

Missing before real bug bounty / pentest use:

- explicit authorized target/program scope;
- written rules allowing XSS testing and safe payloads;
- target-specific safe request cap/rate/timeout plan;
- manual browser validation on the in-scope application;
- no credential/token/cookie exfiltration payloads unless explicitly allowed, and even then with strict minimization;
- redaction and evidence minimization policy;
- report-readiness review;
- no automatic submission.

## 對專案有什麼幫助

- Capability growth: closes the XSS evidence-packet hardening lane with a reusable browser-runtime proof shape.
- Evidence quality improvement: upgrades XSS evidence from reflection/candidate wording to DOM runtime marker + origin/path + control artifact.
- Automation/readiness impact: gives future XSS/adapted target waves a packet template and rerun gate without adding schema-first bureaucracy.
- False-positive/precondition lesson: XSS claims should require browser runtime proof and negative controls; reflected marker text alone is not enough.

## 新增/更新了什麼

- Scripts: no script changes; reused `scripts/labs/webgoat_browser_runtime_xss_wave1.sh` and `scripts/labs/cdp_runtime_xss.py`.
- Bundles: source bundle remains `modules/bundles/verified_lab_flow_webgoat_browser_runtime_xss_safe_marker.md`.
- Handoffs: added this evidence packet `handoff/webgoat_browser_runtime_xss_evidence_packet_20260523.md`.
- Obsidian notes: Cybersec Lab project note should point to this packet as completed XSS packet hardening.
- Artifacts: reused verified rerun artifacts under `<artifact-output-dir>/webgoat_browser_runtime_xss_20260523T105506Z/`.
- Blockers: no runtime blocker in this rerun; only limitation is lab-only/report-readiness boundary.
- Reusable workflow updates: future browser-runtime XSS packets should preserve marker, origin/path/session, positive/control DOM artifacts, screenshot when useful, pre/post health, and explicit no-exfiltration boundaries.
