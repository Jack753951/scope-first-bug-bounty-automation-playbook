#!/usr/bin/env python3
"""Minimal Chrome DevTools Protocol runtime-XSS verifier.

Local lab helper only. Sets a provided session cookie, navigates to one XSS URL
and one control URL, then records DOM/body attributes/screenshot artifacts.
"""
from __future__ import annotations

import argparse
import base64
import json
import os
import shutil
import subprocess
import tempfile
import time
import urllib.parse
import urllib.request
from pathlib import Path

import websocket
from websocket import WebSocketTimeoutException


def wait_json(url: str, timeout: float = 10.0):
    deadline = time.time() + timeout
    last = None
    while time.time() < deadline:
        try:
            with urllib.request.urlopen(url, timeout=1) as r:
                return json.loads(r.read().decode())
        except Exception as e:
            last = e
            time.sleep(0.2)
    raise RuntimeError(f"timed out waiting for {url}: {last!r}")


class CDP:
    def __init__(self, ws_url: str):
        self.ws = websocket.create_connection(ws_url, timeout=5)
        self.next_id = 0

    def call(self, method: str, params: dict | None = None, timeout: float = 30.0):
        self.next_id += 1
        msg_id = self.next_id
        self.ws.settimeout(1)
        self.ws.send(json.dumps({"id": msg_id, "method": method, "params": params or {}}))
        deadline = time.time() + timeout
        while time.time() < deadline:
            try:
                raw = self.ws.recv()
            except WebSocketTimeoutException:
                continue
            msg = json.loads(raw)
            if msg.get("id") == msg_id:
                if "error" in msg:
                    raise RuntimeError(f"CDP {method} error: {msg['error']}")
                return msg.get("result", {})
        raise TimeoutError(method)

    def close(self):
        self.ws.close()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--chromium", default=shutil.which("chromium") or shutil.which("chromium-browser") or "chromium")
    ap.add_argument("--cookie-name", default="JSESSIONID")
    ap.add_argument("--cookie-value", required=True)
    ap.add_argument("--cookie-url", required=True)
    ap.add_argument("--xss-url", required=True)
    ap.add_argument("--control-url", required=True)
    ap.add_argument("--marker", required=True)
    ap.add_argument("--out", required=True)
    ns = ap.parse_args()

    out = Path(ns.out)
    out.mkdir(parents=True, exist_ok=True)
    profile = Path(tempfile.mkdtemp(prefix="hermes-cdp-xss-"))
    port = 9222 + (os.getpid() % 1000)
    proc = subprocess.Popen([
        ns.chromium,
        "--headless=new",
        "--disable-gpu",
        "--no-sandbox",
        f"--remote-debugging-port={port}",
        "--remote-allow-origins=*",
        f"--user-data-dir={profile}",
        "about:blank",
    ], stdout=subprocess.DEVNULL, stderr=(out / "chromium.stderr").open("wb"))
    try:
        wait_json(f"http://127.0.0.1:{port}/json/version")
        pages = wait_json(f"http://127.0.0.1:{port}/json/list")
        page_ws = next((p.get("webSocketDebuggerUrl") for p in pages if p.get("type") == "page" and p.get("webSocketDebuggerUrl")), None)
        if not page_ws:
            raise RuntimeError(f"no page websocket in {pages!r}")
        cdp = CDP(page_ws)
        try:
            cdp.call("Network.enable")
            cdp.call("Runtime.enable")
            cdp.call("Page.enable")
            cookie_res = cdp.call("Network.setCookie", {
                "name": ns.cookie_name,
                "value": ns.cookie_value,
                "url": ns.cookie_url,
                "path": "/WebGoat",
                "httpOnly": True,
            })
            cdp.call("Page.navigate", {"url": ns.xss_url})
            time.sleep(2)
            cdp.call("Runtime.evaluate", {"expression": """
(() => {
  const raw = document.body ? document.body.innerText : '';
  try {
    const data = JSON.parse(raw);
    if (data && data.output) document.body.innerHTML = String(data.output).replaceAll('\\\\&quot;', '"').replaceAll('&quot;', '"');
  } catch (e) {}
})()
""", "returnByValue": True})
            time.sleep(2)
            attrs = cdp.call("Runtime.evaluate", {"expression": "({xss: document.body && document.body.getAttribute('data-xss'), origin: location.origin, path: location.pathname, url: location.href, title: document.title})", "returnByValue": True})
            dom = cdp.call("Runtime.evaluate", {"expression": "document.documentElement.outerHTML", "returnByValue": True})
            shot = cdp.call("Page.captureScreenshot", {"format": "png", "captureBeyondViewport": True}, timeout=12)
            (out / "dom.html").write_text(dom.get("result", {}).get("value", ""), encoding="utf-8")
            (out / "xss_page.png").write_bytes(base64.b64decode(shot.get("data", "")))
            cdp.call("Page.navigate", {"url": ns.control_url})
            time.sleep(2)
            cdp.call("Runtime.evaluate", {"expression": """
(() => {
  const raw = document.body ? document.body.innerText : '';
  try {
    const data = JSON.parse(raw);
    if (data && data.output) document.body.innerHTML = String(data.output).replaceAll('\\\\&quot;', '"').replaceAll('&quot;', '"');
  } catch (e) {}
})()
""", "returnByValue": True})
            time.sleep(1)
            control_attrs = cdp.call("Runtime.evaluate", {"expression": "({xss: document.body && document.body.getAttribute('data-xss'), origin: location.origin, path: location.pathname, url: location.href, title: document.title})", "returnByValue": True})
            control_dom = cdp.call("Runtime.evaluate", {"expression": "document.documentElement.outerHTML", "returnByValue": True})
            (out / "control_dom.html").write_text(control_dom.get("result", {}).get("value", ""), encoding="utf-8")
            result = {
                "cookie_set": cookie_res,
                "attrs": attrs.get("result", {}).get("value", {}),
                "control_attrs": control_attrs.get("result", {}).get("value", {}),
                "xss_url": ns.xss_url,
                "control_url": ns.control_url,
                "marker": ns.marker,
            }
            (out / "browser_result.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
            ok = result["attrs"].get("xss") == ns.marker and not result["control_attrs"].get("xss")
            print(json.dumps({"ok": ok, **result}, indent=2))
            return 0 if ok else 4
        finally:
            cdp.close()
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=3)
        except subprocess.TimeoutExpired:
            proc.kill()


if __name__ == "__main__":
    raise SystemExit(main())
