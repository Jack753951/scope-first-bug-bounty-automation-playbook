> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# WebGoat browser-runtime XSS safe-marker proof pattern

Session source: 2026-05-23 Cybersec Lab proof wave.
Use this reference when the next OWASP single-vulnerability wave is browser-runtime XSS on a local WebGoat/lesson-style target.

## Durable lesson

A browser-runtime XSS proof should prove execution in the correct browser/origin/session context, not only raw text reflection. Preserve:

- a unique safe marker;
- browser DOM state or console evidence;
- origin and path labels;
- positive and negative/control artifacts;
- pre/post health;
- route/NAT posture;
- clear limitation language.

## Tested local-lab shape

Route used:

```text
Windows Hermes control plane
-> <lab-vm> / host-only attacker VM
-> <lab-vm> / Docker-backed WebGoat on <lab-ip>:8080
```

Target class:

```text
WebGoat CrossSiteScripting lesson / browser runtime safe-marker proof
```

Artifact shape:

```text
kali-output/webgoat_browser_runtime_xss_<timestamp>/
  summary.md
  observations.jsonl
  xss/browser_result.json
  xss/dom.html
  xss/control_dom.html
  xss/payload.html
  xss/xss_url.txt
  xss/control_url.txt
  browser/xss_page.png
```

Successful `browser_result.json` should show the marker in runtime DOM state and no marker in the control, for example:

```json
{
  "attrs": {
    "xss": "WG_XSS_RUNTIME_<run_id>",
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

## CDP helper workaround pattern

If a high-level browser driver is unavailable or unreliable in the isolated lab, do not stop the XSS lane automatically. A small Chrome DevTools Protocol helper can be a better local-lab proof primitive:

1. Start Chromium/headless with a local debug port and isolated profile.
2. Use `/json/list` to get the page WebSocket, not only `/json/version` browser WebSocket.
3. Set the lab session cookie explicitly.
4. Navigate to the target URL.
5. Capture runtime DOM state, HTML, screenshot, and a control run.
6. Keep the helper narrow: it is a local-lab proof helper, not a scanner.

Do not record transient driver/setup failures as durable tool limitations. Capture the workaround and rerun path instead.

## WebGoat JSON-output limitation

Some WebGoat XSS lesson endpoints return JSON containing an `output` field instead of directly rendering HTML. If validating that endpoint with CDP, it is acceptable for local proof-pattern calibration to render the JSON `output` into a same-origin DOM sink and then verify DOM mutation, but the handoff must say this explicitly.

Use wording like:

```text
Because direct /attack5a returns JSON, the CDP helper renders the JSON output into a same-origin browser DOM sink for runtime validation. Treat this as a verified local-lab runtime-sink proof and reusable browser-proof pattern, not as a standalone public-target report by itself.
```

## Safe payload rules

Allowed for this lab pattern:

- inert DOM marker mutation, e.g. `document.body.setAttribute(...)`;
- origin/path labeling;
- local screenshot/DOM capture.

Avoid:

- `alert(document.cookie)`;
- cookie/token reads;
- credential prompts;
- external callbacks/OAST;
- redirects or persistence;
- public-target finding language.

## Closeout wording for this user

The final summary/handoff should include the user's preferred project-value sections:

- `對專案有什麼幫助` — how the proof improves capability, evidence quality, automation/readiness, and false-positive/precondition learning.
- `新增/更新了什麼` — changed scripts, bundles, handoffs, Obsidian notes, artifacts, blockers, and reusable workflow updates.

Keep route/tool, visible model/runtime when available, artifact paths, boundaries, validation, and next-lane recommendation next to these sections.
