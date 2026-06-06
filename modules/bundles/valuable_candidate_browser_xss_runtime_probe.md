> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# valuable_candidate_browser_xss_runtime_probe

Status: valuable-candidate / attempted-not-verified runtime proof
Date: 2026-05-22
Route/tool: Windows Hermes control plane -> SSH/SCP -> `<attacker-vm>` -> Chromium headless -> authorized Juice Shop victim
Artifact root: `<artifact-output-dir>/kali_intel_wave3_20260522T005554Z/`
Sources mapped: NVD/Exploit-DB/GitHub/HTB XSS patterns, OWASP A03/A05, CWE-79

## Why keep this bundle

This is worth retaining because modern XSS validation often fails when a scanner only sees reflected payload text. The useful part here is the browser-backed proof workflow and the decision not to overclaim execution.

## Payload families attempted

```text
/#/search?q=<img src=x onerror="document.body.setAttribute('data-vf3-alert','VF3_XSS')">
/#/search?q=<script>document.body.setAttribute("data-vf3-alert","VF3_XSS")</script>
/redirect?to=javascript:document.body.setAttribute("data-vf3-alert","VF3_XSS")
```

The runner used Kali Chromium headless with DOM dump and marker search.

## Observed result

Wave 3 produced browser DOM artifacts and candidate markers:

```text
search_img     status=0 hit=candidate bytes=205271
search_script  status=0 hit=candidate bytes=204085
redirect_js    status=0 hit=candidate bytes=3332
```

## Verification decision

Do not mark as verified XSS yet.

Reason:

- Current hit detection is too broad and may match reflected or encoded payload text.
- We did not yet preserve a conclusive runtime signal such as:
  - alert override invocation count;
  - DOM attribute set by executed JavaScript rather than payload text;
  - console log emitted by payload;
  - challenge completion state tied to XSS execution.

## Value retained

- A Kali-side browser validation route exists.
- Payload families and artifact locations are recorded.
- False-positive rule is explicit: reflected payload text is not runtime proof.

## Next steps

- Replace broad regex marker search with a Playwright/Puppeteer or Chrome DevTools Protocol script that checks actual JavaScript-side state.
- Save DOM/console/network artifacts inside the run directory, not `/tmp`.
- Prefer known Juice Shop challenge routes or PortSwigger-style XSS lab fixture if current target does not provide stable runtime proof.
