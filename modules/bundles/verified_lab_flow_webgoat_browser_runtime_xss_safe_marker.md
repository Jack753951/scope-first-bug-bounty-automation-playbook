> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Verified Lab Flow — WebGoat Browser Runtime XSS Safe Marker

Status: verified-impact / local-learning-lab only
Last verified: 2026-05-23
Primary handoff: `handoff/webgoat_browser_runtime_xss_wave1_20260523.md`
Latest artifacts: `<artifact-output-dir>/webgoat_browser_runtime_xss_20260523T030746Z/`
Primary scripts:
- `scripts/labs/webgoat_browser_runtime_xss_wave1.sh`
- `scripts/labs/cdp_runtime_xss.py`

## When to use

Use this bundle when the project needs a browser-runtime XSS proof pattern against the authorized local WebGoat lab:

- prove runtime JavaScript execution in a browser context, not just reflected text;
- preserve a safe marker in DOM state;
- label execution origin/path;
- include a negative/control request;
- avoid credential/token theft and external callback behavior.

Do not use it against public, client, or bug-bounty targets without a separate scope/rules/rate/report-readiness gate.

## Target and route

Default route:

```text
Windows Hermes control plane
-> <attacker-vm> / <lab-ip> / host-only attacker VM
-> <victim-vm> / <lab-ip> / Docker-backed WebGoat on 8080
```

Target:

```text
http://<lab-ip>:8080/WebGoat
```

Required route posture:

- attacker and victim NIC1 host-only;
- NIC2/NAT closed/off unless a separate temporary install window is explicitly open;
- attacker can reach victim ports `8080` and `9090`;
- attacker cannot reach Internet after the wave.

## What it runs

The runner:

1. checks `/WebGoat/login` health;
2. registers/logs in a short throwaway WebGoat user with lab password rules;
3. fetches the CrossSiteScripting lesson page;
4. creates a unique `WG_XSS_RUNTIME_<run_id>` marker;
5. launches Chromium through a minimal Chrome DevTools Protocol helper;
6. sets the lab `JSESSIONID` cookie;
7. navigates to `/WebGoat/CrossSiteScripting/attack5a` with a bounded `field1` payload;
8. renders the JSON `output` into a same-origin DOM sink to validate browser runtime behavior;
9. verifies `document.body[data-xss]` equals the marker;
10. runs a control request that must not set `data-xss`;
11. writes summary, JSONL observations, DOM artifacts, browser result JSON, and screenshot.

## Rerun command

From `<private-workspace>`:

```bash
powershell.exe -NoProfile -ExecutionPolicy Bypass -File ./scripts/kali-run.ps1 -Command 'cd /mnt/hacking && bash scripts/labs/webgoat_browser_runtime_xss_wave1.sh'
```

Pull artifacts back:

```bash
MSYS2_ARG_CONV_EXCL='*' powershell.exe -NoProfile -ExecutionPolicy Bypass -File ./scripts/kali-pull.ps1 -RemotePath '/home/kali/<artifact-output-dir>/<run_id>'
```

## Evidence to inspect

For a successful run, inspect:

```text
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

The key success condition is:

```json
{
  "attrs": {
    "xss": "WG_XSS_RUNTIME_<run_id>",
    "origin": "http://<lab-ip>:8080",
    "path": "/WebGoat/CrossSiteScripting/attack5a"
  },
  "control_attrs": {
    "xss": null
  }
}
```

## False-positive controls and limitations

Controls:

- positive marker must appear as runtime DOM state, not only in raw response text;
- control request must not set `data-xss`;
- origin/path must match the WebGoat target route;
- post-health must remain HTTP 200.

Limitations:

- Direct `/attack5a` returns JSON. The helper renders the endpoint `output` into a same-origin DOM sink for runtime validation. This is good for local proof-pattern training and evidence calibration, but it should not be described as a standalone public-target finding.
- The bundle deliberately avoids cookie/token reads, credential theft, redirects, persistence, and callbacks.
- A future improvement is full WebGoat lesson-page UI interaction through CDP or Selenium if needed.

## Boundary

Allowed:

- local WebGoat lab only;
- throwaway user;
- safe DOM marker mutation;
- artifact retention under `<artifact-output-dir>/`.

Disallowed:

- public/unknown targets;
- real credential or token access;
- exfiltration/callback/OAST;
- persistence/shell/destructive actions;
- automatic confirmed finding/report promotion.
