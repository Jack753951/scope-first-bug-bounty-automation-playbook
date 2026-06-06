> Public sanitized Hermes skill export. Private paths, targets, aliases, credentials, advisories, and run-specific evidence are redacted.

# VM-contained live-browser workflows

Use this pattern when the operator wants browser/login/proxy work moved out of the Windows host and into a Kali VM for cleaner isolation.

## Recommended split

- Windows host: Hermes control plane, handoff files, Obsidian/report writing, scope/safety decisions.
- Kali attacker VM: dedicated browser profiles, Burp/proxy tooling, screenshots, low-risk surface mapping, manual verification.
- Victim/lab VM: intentionally vulnerable local targets and recoverable exploit practice.

Avoid putting live-site login sessions or remote-debugging Chrome profiles on the Windows host unless the operator explicitly accepts that risk. For live websites, prefer a throwaway/test account in a dedicated VM browser profile.

## VirtualBox VM selection

- Use the regular Kali attacker VM for live-site browsing when possible.
- Do not use the victim VM for browsing/logins.
- Avoid mixing live website sessions with aggressive lab-only workflows unless the operator explicitly requests it and understands the isolation tradeoff.

## Browser launch pattern inside Kali

Via SSH wrapper or Kali terminal:

```bash
mkdir -p "$HOME/browser-profiles/<site>-hermes"
DISPLAY=:0 XAUTHORITY="$HOME/.Xauthority" nohup chromium \
  --user-data-dir="$HOME/browser-profiles/<site>-hermes" \
  --no-first-run \
  --new-window "https://example.com/" \
  > /tmp/<site>_chromium.log 2>&1 &
```

For CDP only when needed, bind locally inside the VM:

```bash
chromium \
  --remote-debugging-address=127.0.0.1 \
  --remote-debugging-port=9222 \
  --user-data-dir="$HOME/browser-profiles/<site>-hermes" \
  --no-first-run \
  --new-window "https://example.com/"
```

Do not bind CDP to `0.0.0.0` for live account sessions.

## Network mode for live browsing

A lab VM may intentionally be host-only. If a live website must be opened, prefer a temporary second adapter:

- `nic1=hostonly` for host/lab communication.
- `nic2=NAT` for temporary outbound web access.
- Disable `nic2` again after the task if isolation is the goal.

Confirm this is operator-approved before changing VM network state.

## Proxychains guidance

Proxychains is acceptable for authorized lab/CTF/client-scope CLI tools such as:

```bash
proxychains4 curl -I https://example.com/
```

Do not default to `proxychains4 chromium` for login/surface-map workflows. Chromium has multiple subprocesses and browser-level behaviors (DNS, QUIC, WebRTC, sandboxing) that can cause partial leaks or unstable results.

Prefer explicit browser proxy settings instead:

Burp/local HTTP proxy:

```bash
chromium \
  --user-data-dir="$HOME/browser-profiles/<site>-hermes" \
  --proxy-server="http://127.0.0.1:8080" \
  --no-first-run \
  --new-window "https://example.com/"
```

SOCKS proxy:

```bash
chromium \
  --user-data-dir="$HOME/browser-profiles/<site>-hermes" \
  --proxy-server="socks5://127.0.0.1:9050" \
  --host-resolver-rules="MAP * ~NOTFOUND , EXCLUDE 127.0.0.1" \
  --no-first-run \
  --new-window "https://example.com/"
```

## Safety notes

- Do not use proxying to hide identity, evade rate limits, bypass blocks, or violate bounty/client rules.
- Confirm live-target authorization and program rules before active scanning, fuzzing, exploitation, or automation.
- For account-owned browsing, keep the workflow manual/low-rate unless rules explicitly permit more.
