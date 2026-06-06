#!/usr/bin/env python3
"""Small, safety-bounded Chromium CDP click helper for Kali/noVNC workflows.

This helper performs one reviewed browser action on the currently open Chromium
page via the local remote-debugging port. It intentionally avoids cookies,
storage, network bodies, request headers, input values, and screenshots. Output
is compact JSON with URL query/fragment removed.
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import socket
import struct
import sys
import time
import urllib.parse
import urllib.request
from typing import Any


class CdpActionError(RuntimeError):
    pass


def _json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False)


def sanitize_url(url: str) -> str:
    parsed = urllib.parse.urlsplit(url or "")
    if not parsed.scheme or not parsed.netloc:
        return url[:300]
    return urllib.parse.urlunsplit((parsed.scheme, parsed.netloc, parsed.path, "", ""))[:500]


def build_click_expression(*, selector: str | None = None, text: str | None = None, contains: bool = False) -> str:
    if not selector and not text:
        raise ValueError("selector or text is required")
    selector_js = _json(selector)
    text_js = _json(text)
    contains_js = "true" if contains else "false"
    return f"""
(() => {{
  const selector = {selector_js};
  const wantedText = {text_js};
  const contains = {contains_js};
  const norm = (s) => (s || '').replace(/\\s+/g, ' ').trim();
  const labelFor = (el) => norm(el.getAttribute('aria-label') || el.innerText || el.textContent || el.getAttribute('title') || '');
  let matches = [];
  if (selector) {{
    try {{ matches = Array.from(document.querySelectorAll(selector)); }}
    catch (err) {{ return {{ok:false, reason:'bad_selector', message:String(err).slice(0,160), selector}}; }}
  }} else {{
    const candidates = Array.from(document.querySelectorAll('a,button,[role="button"],input[type="button"],input[type="submit"]'));
    matches = candidates.filter((el) => {{
      const label = labelFor(el) || norm(el.getAttribute('value'));
      return contains ? label.includes(wantedText) : label === wantedText;
    }});
  }}
  if (matches.length !== 1) {{
    return {{
      ok:false,
      reason: matches.length === 0 ? 'not_found' : 'ambiguous',
      count: matches.length,
      query: selector ? {{selector}} : {{text:wantedText, contains}},
      candidates: matches.slice(0, 10).map((el) => ({{tag:el.tagName, label:labelFor(el)}}))
    }};
  }}
  const el = matches[0];
  const label = labelFor(el);
  el.scrollIntoView({{block:'center', inline:'center'}});
  el.focus({{preventScroll:true}});
  el.click();
  return {{ok:true, action:'click', tag:el.tagName, label, href:el.href || null, title:document.title || '', url:location.href}};
}})()
""".strip()


def build_fill_expression(*, selector: str, value: str) -> str:
    if not selector:
        raise ValueError("selector is required")
    selector_js = _json(selector)
    value_js = _json(value)
    return f"""
(() => {{
  const selector = {selector_js};
  const fillValue = {value_js};
  let matches = [];
  try {{ matches = Array.from(document.querySelectorAll(selector)); }}
  catch (err) {{ return {{ok:false, reason:'bad_selector', message:String(err).slice(0,160), selector}}; }}
  matches = matches.filter((el) => el instanceof HTMLInputElement || el instanceof HTMLTextAreaElement);
  if (matches.length !== 1) {{
    return {{ok:false, reason: matches.length === 0 ? 'not_found' : 'ambiguous', count:matches.length, selector}};
  }}
  const el = matches[0];
  el.scrollIntoView({{block:'center', inline:'center'}});
  el.focus({{preventScroll:true}});
  const proto = el instanceof HTMLTextAreaElement ? HTMLTextAreaElement.prototype : HTMLInputElement.prototype;
  const desc = Object.getOwnPropertyDescriptor(proto, 'value');
  if (desc && desc.set) desc.set.call(el, fillValue); else el.value = fillValue;
  el.dispatchEvent(new Event('input', {{bubbles:true}}));
  el.dispatchEvent(new Event('change', {{bubbles:true}}));
  return {{ok:true, action:'fill', tag:el.tagName, type:el.type || null, name:el.name || null, value_length:fillValue.length, title:document.title || '', url:location.href}};
}})()
""".strip()


def websocket_send_frame(sock: socket.socket, payload: bytes) -> None:
    # Client frames must be masked. Support small/medium CDP JSON payloads.
    header = bytearray([0x81])
    length = len(payload)
    if length < 126:
        header.append(0x80 | length)
    elif length < 65536:
        header.append(0x80 | 126)
        header.extend(struct.pack("!H", length))
    else:
        header.append(0x80 | 127)
        header.extend(struct.pack("!Q", length))
    mask = os.urandom(4)
    masked = bytes(b ^ mask[i % 4] for i, b in enumerate(payload))
    sock.sendall(bytes(header) + mask + masked)


def websocket_recv_frame(sock: socket.socket) -> bytes:
    first = sock.recv(2)
    if len(first) < 2:
        raise CdpActionError("websocket closed")
    b1, b2 = first
    opcode = b1 & 0x0F
    masked = bool(b2 & 0x80)
    length = b2 & 0x7F
    if length == 126:
        length = struct.unpack("!H", _recv_exact(sock, 2))[0]
    elif length == 127:
        length = struct.unpack("!Q", _recv_exact(sock, 8))[0]
    mask = _recv_exact(sock, 4) if masked else b""
    data = _recv_exact(sock, length)
    if masked:
        data = bytes(b ^ mask[i % 4] for i, b in enumerate(data))
    if opcode == 0x8:
        raise CdpActionError("websocket close frame")
    if opcode not in (0x1, 0x2):
        return b""
    return data


def _recv_exact(sock: socket.socket, n: int) -> bytes:
    chunks: list[bytes] = []
    remaining = n
    while remaining:
        chunk = sock.recv(remaining)
        if not chunk:
            raise CdpActionError("short websocket read")
        chunks.append(chunk)
        remaining -= len(chunk)
    return b"".join(chunks)


def websocket_request(ws_url: str, payload: dict[str, Any], timeout: float = 5.0) -> dict[str, Any]:
    parsed = urllib.parse.urlsplit(ws_url)
    if parsed.scheme not in {"ws", "wss"}:
        raise CdpActionError(f"unsupported websocket scheme: {parsed.scheme}")
    if parsed.scheme == "wss":
        raise CdpActionError("wss is not supported for local CDP helper")
    host = parsed.hostname or "127.0.0.1"
    port = parsed.port or 80
    path = urllib.parse.urlunsplit(("", "", parsed.path or "/", parsed.query, ""))
    key = base64.b64encode(os.urandom(16)).decode("ascii")
    with socket.create_connection((host, port), timeout=timeout) as sock:
        sock.settimeout(timeout)
        request = (
            f"GET {path} HTTP/1.1\r\n"
            f"Host: {host}:{port}\r\n"
            "Upgrade: websocket\r\n"
            "Connection: Upgrade\r\n"
            f"Sec-WebSocket-Key: {key}\r\n"
            "Sec-WebSocket-Version: 13\r\n\r\n"
        )
        sock.sendall(request.encode("ascii"))
        handshake = b""
        while b"\r\n\r\n" not in handshake:
            chunk = sock.recv(4096)
            if not chunk:
                raise CdpActionError("websocket handshake failed")
            handshake += chunk
            if len(handshake) > 8192:
                raise CdpActionError("websocket handshake too large")
        if b" 101 " not in handshake.split(b"\r\n", 1)[0]:
            raise CdpActionError("websocket upgrade rejected")
        websocket_send_frame(sock, json.dumps(payload).encode("utf-8"))
        deadline = time.time() + timeout
        while time.time() < deadline:
            data = websocket_recv_frame(sock)
            if not data:
                continue
            message = json.loads(data.decode("utf-8"))
            if message.get("id") == payload.get("id"):
                return message
    raise CdpActionError("timed out waiting for CDP response")


def choose_page(cdp_url: str) -> dict[str, Any]:
    pages = json.loads(urllib.request.urlopen(cdp_url.rstrip("/") + "/json/list", timeout=5).read().decode("utf-8"))
    candidates = [p for p in pages if p.get("type") == "page" and p.get("webSocketDebuggerUrl")]
    if not candidates:
        raise CdpActionError("no CDP page target with websocket URL found")
    return candidates[0]


def evaluate_expression(expression: str, *, cdp_url: str = "http://127.0.0.1:9222") -> dict[str, Any]:
    page = choose_page(cdp_url)
    payload = {
        "id": 1,
        "method": "Runtime.evaluate",
        "params": {"expression": expression, "returnByValue": True, "awaitPromise": True},
    }
    return websocket_request(page["webSocketDebuggerUrl"], payload)


def extract_action_result(message: dict[str, Any]) -> dict[str, Any]:
    value = message.get("result", {}).get("result", {}).get("value")
    if not isinstance(value, dict):
        raise CdpActionError("CDP response did not contain a JSON object result")
    allowed = {"ok", "action", "tag", "type", "name", "label", "href", "title", "url", "reason", "count", "query", "candidates", "selector", "message", "value_length"}
    out = {k: v for k, v in value.items() if k in allowed}
    for key in ("url", "href"):
        if isinstance(out.get(key), str):
            out[key] = sanitize_url(out[key])
    return out


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Safety-bounded local Chromium CDP click helper.")
    parser.add_argument("--text", help="Exact visible text/label to click")
    parser.add_argument("--text-b64", help="Base64-encoded exact visible text/label to click")
    parser.add_argument("--selector", help="CSS selector to click or fill")
    parser.add_argument("--selector-b64", help="Base64-encoded CSS selector to click or fill")
    parser.add_argument("--fill-text", help="Non-secret text to fill into selector")
    parser.add_argument("--fill-text-b64", help="Base64-encoded non-secret text to fill into selector")
    parser.add_argument("--contains", action="store_true", help="Allow text substring match instead of exact match")
    parser.add_argument("--cdp-url", default="http://127.0.0.1:9222")
    # Explicitly reject common live-target/scanner-shaped args so this helper is not mistaken for a fetch/probe tool.
    parser.add_argument("--target", action="store_true", help=argparse.SUPPRESS)
    parser.add_argument("--url", action="store_true", help=argparse.SUPPRESS)
    parser.add_argument("--host", action="store_true", help=argparse.SUPPRESS)
    parser.add_argument("--live", action="store_true", help=argparse.SUPPRESS)
    args = parser.parse_args(argv)
    if getattr(args, "target", False) or getattr(args, "url", False) or getattr(args, "host", False) or getattr(args, "live", False):
        raise SystemExit("refusing live-target arguments; open pages with kali-browser-ops.ps1 -Action open after policy approval")
    if args.text_b64:
        args.text = base64.b64decode(args.text_b64.encode("ascii"), validate=True).decode("utf-8")
    if args.selector_b64:
        args.selector = base64.b64decode(args.selector_b64.encode("ascii"), validate=True).decode("utf-8")
    if args.fill_text_b64:
        args.fill_text = base64.b64decode(args.fill_text_b64.encode("ascii"), validate=True).decode("utf-8")
    if args.fill_text is not None:
        if not args.selector or args.text:
            raise SystemExit("fill requires --selector/--selector-b64 and forbids --text")
    elif bool(args.text) == bool(args.selector):
        raise SystemExit("exactly one of --text/--text-b64 or --selector/--selector-b64 is required")
    return args


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    if args.fill_text is not None:
        expression = build_fill_expression(selector=args.selector, value=args.fill_text)
    else:
        expression = build_click_expression(selector=args.selector, text=args.text, contains=args.contains)
    message = evaluate_expression(expression, cdp_url=args.cdp_url)
    result = extract_action_result(message)
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0 if result.get("ok") else 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
