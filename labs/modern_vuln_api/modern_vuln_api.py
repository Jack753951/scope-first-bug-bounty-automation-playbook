#!/usr/bin/env python3
"""Disposable modern vulnerable API lab target.

Authorized local-lab use only. This intentionally exposes:
- IDOR / broken object ownership
- upload acceptance + retrieval
- SSRF-style server-side fetch to demonstrate isolated callback proof

No real credentials, no production use.
"""
from __future__ import annotations

import argparse
import base64
import html
import json
import os
import pickle
import re
import tempfile
import threading
import time
import urllib.request
import uuid
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

USERS = {
    "alice": {"id": 1, "password": "alicepass", "role": "user"},
    "bob": {"id": 2, "password": "bobpass", "role": "user"},
    "admin": {"id": 99, "password": "adminpass", "role": "admin"},
}
TOKENS: dict[str, str] = {}
INVOICES = {
    "1001": {"owner": "alice", "amount": 120, "secret_note": "ALICE_PRIVATE_INVOICE_MARKER"},
    "2001": {"owner": "bob", "amount": 220, "secret_note": "BOB_PRIVATE_INVOICE_MARKER"},
}
ADMIN_AUDIT_LOG = [
    {"id": "audit-001", "event": "role_change", "actor": "admin", "target": "alice", "marker": "ADMIN_AUDIT_MARKER_HERMES_LOCAL_LAB"},
    {"id": "audit-002", "event": "billing_export", "actor": "admin", "target": "org-1", "marker": "ADMIN_AUDIT_MARKER_HERMES_LOCAL_LAB"},
]
CALLBACKS: list[dict] = []
DESER_EVENTS: list[dict] = []
UPLOADS: dict[str, dict] = {}
UPLOAD_DIR = Path(tempfile.gettempdir()) / "hermes_modern_api_uploads"
UPLOAD_DIR.mkdir(exist_ok=True)
XXE_MARKER_FILE = Path(tempfile.gettempdir()) / "hermes_modern_api_xxe_marker.txt"
XXE_MARKER_FILE.write_text("XXE_SAFE_MARKER_HERMES_LOCAL_LAB\n", encoding="utf-8")
FILE_READ_PUBLIC_DIR = Path(tempfile.gettempdir()) / "hermes_modern_api_public_files"
FILE_READ_PUBLIC_DIR.mkdir(exist_ok=True)
FILE_READ_PUBLIC_FILE = FILE_READ_PUBLIC_DIR / "public.txt"
FILE_READ_PUBLIC_FILE.write_text("PUBLIC_FILE_CONTROL_HERMES_LOCAL_LAB\n", encoding="utf-8")
FILE_READ_MARKER_FILE = Path(tempfile.gettempdir()) / "hermes_modern_api_file_read_marker.txt"
FILE_READ_MARKER_FILE.write_text("FILE_READ_SAFE_MARKER_HERMES_LOCAL_LAB\n", encoding="utf-8")


def record_deser_marker(marker: str) -> dict:
    """Bounded pickle gadget sink used only for local lab proof.

    This intentionally proves code-path execution without shelling out, touching
    external systems, creating persistence, or reading secrets.
    """
    event = {"ts": time.time(), "marker": str(marker), "type": "bounded_pickle_gadget"}
    DESER_EVENTS.append(event)
    return {"recorded": True, "marker": str(marker)}


def record_deser_impact(marker: str, callback_url: str = "") -> dict:
    """Lab-only impact sink for unsafe-deserialization max-impact drills.

    The sink proves server-side control by writing a marker file and optionally
    calling an isolated host-only callback listener. It deliberately avoids a
    shell, arbitrary commands, persistence, credential access, and system-file
    damage. Callback destinations are restricted to host-only/local lab IPs.
    """
    safe_marker = re.sub(r"[^A-Za-z0-9_.:-]", "_", str(marker))[:80]
    marker_dir = Path(tempfile.gettempdir()) / "hermes_modern_api_impact"
    marker_dir.mkdir(exist_ok=True)
    marker_file = marker_dir / f"{safe_marker}.txt"
    marker_body = {
        "marker": safe_marker,
        "pid": os.getpid(),
        "uid": getattr(os, "getuid", lambda: "windows-na")(),
        "cwd": os.getcwd(),
        "ts": time.time(),
        "type": "lab_only_deser_impact",
    }
    marker_file.write_text(json.dumps(marker_body, indent=2), encoding="utf-8")
    callback = {"attempted": False, "allowed": False, "url": callback_url, "status": None, "error": None}
    if callback_url:
        parsed = urlparse(callback_url)
        allowed_hosts = {"127.0.0.1", "localhost", "<lab-ip>", "<lab-ip>", "<lab-ip>"}
        if parsed.scheme == "http" and parsed.hostname in allowed_hosts:
            callback["allowed"] = True
            callback["attempted"] = True
            try:
                req = urllib.request.Request(callback_url, headers={"User-Agent": "HermesModernVulnAPI-DeserImpact-Lab"})
                with urllib.request.urlopen(req, timeout=4) as resp:
                    callback["status"] = getattr(resp, "status", 200)
                    resp.read(200)
            except Exception as exc:  # pragma: no cover - lab evidence path
                callback["error"] = repr(exc)
    event = {"ts": time.time(), "marker": safe_marker, "type": "lab_only_deser_impact", "marker_file": str(marker_file), "callback": callback, "identity": marker_body}
    DESER_EVENTS.append(event)
    return {"recorded": True, "marker": safe_marker, "marker_file": str(marker_file), "callback": callback, "identity": marker_body}


def token_for(username: str) -> str:
    raw = f"{username}:{time.time()}:{uuid.uuid4()}".encode()
    tok = base64.urlsafe_b64encode(raw).decode().rstrip("=")
    TOKENS[tok] = username
    return tok


def read_json(handler: BaseHTTPRequestHandler) -> dict:
    n = int(handler.headers.get("Content-Length", "0") or 0)
    if not n:
        return {}
    try:
        return json.loads(handler.rfile.read(n).decode("utf-8", "replace"))
    except Exception:
        return {}


def auth_user(handler: BaseHTTPRequestHandler) -> str | None:
    h = handler.headers.get("Authorization", "")
    if h.startswith("Bearer "):
        return TOKENS.get(h.split(" ", 1)[1].strip())
    return None


class Handler(BaseHTTPRequestHandler):
    server_version = "HermesModernVulnAPI/0.1"

    def log_message(self, fmt: str, *args) -> None:
        print(f"{self.client_address[0]} - {fmt % args}", flush=True)

    def send_obj(self, code: int, obj: object, ctype: str = "application/json") -> None:
        data = json.dumps(obj, indent=2).encode() if ctype == "application/json" else obj  # type: ignore[assignment]
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        path = parsed.path
        qs = parse_qs(parsed.query)
        if path == "/health":
            self.send_obj(200, {"ok": True, "service": "modern-vuln-api", "purpose": "authorized-local-lab"})
            return
        if path == "/api/me":
            u = auth_user(self)
            if not u:
                self.send_obj(401, {"error": "missing bearer token"})
                return
            self.send_obj(200, {"username": u, "id": USERS[u]["id"], "role": USERS[u]["role"]})
            return
        m = re.fullmatch(r"/api/users/(\d+)", path)
        if m:
            # Intentional IDOR: any authenticated user can fetch another user's profile by id.
            u = auth_user(self)
            if not u:
                self.send_obj(401, {"error": "missing bearer token"})
                return
            uid = int(m.group(1))
            for name, info in USERS.items():
                if info["id"] == uid:
                    self.send_obj(200, {"id": uid, "username": name, "role": info["role"], "private_marker": f"PROFILE_MARKER_{name.upper()}"})
                    return
            self.send_obj(404, {"error": "not found"})
            return
        m = re.fullmatch(r"/api/invoices/(\d+)", path)
        if m:
            # Intentional IDOR: no owner check.
            u = auth_user(self)
            if not u:
                self.send_obj(401, {"error": "missing bearer token"})
                return
            inv = INVOICES.get(m.group(1))
            if not inv:
                self.send_obj(404, {"error": "not found"})
                return
            self.send_obj(200, {"id": m.group(1), **inv, "requested_by": u})
            return
        if path == "/api/admin/audit-log":
            # Intentional role-separation flaw: any authenticated user can read
            # admin-only audit metadata. This is a lab-owned marker surface for
            # multi-role proof practice, not a production pattern.
            u = auth_user(self)
            if not u:
                self.send_obj(401, {"error": "missing bearer token"})
                return
            self.send_obj(200, {"requested_by": u, "requested_role": USERS[u]["role"], "events": ADMIN_AUDIT_LOG})
            return
        if path == "/api/admin/settings":
            # Secure role-control endpoint for false-positive boundary: normal
            # users must not be able to access every admin route.
            u = auth_user(self)
            if not u:
                self.send_obj(401, {"error": "missing bearer token"})
                return
            if USERS[u]["role"] != "admin":
                self.send_obj(403, {"error": "admin role required"})
                return
            self.send_obj(200, {"requested_by": u, "requested_role": "admin", "setting_marker": "ADMIN_SETTINGS_CONTROL_HERMES_LOCAL_LAB"})
            return
        m = re.fullmatch(r"/uploads/([A-Za-z0-9_-]+)", path)
        if m:
            meta = UPLOADS.get(m.group(1))
            if not meta:
                self.send_obj(404, {"error": "upload not found"})
                return
            data = Path(meta["path"]).read_bytes()
            self.send_response(200)
            self.send_header("Content-Type", meta.get("content_type", "application/octet-stream"))
            self.send_header("X-Upload-Name", meta.get("name", "upload.bin"))
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)
            return
        if path == "/fetch":
            # Intentional SSRF-style server-side fetch. Use only against isolated local callback in lab.
            url = qs.get("url", [""])[0]
            if not url:
                self.send_obj(400, {"error": "missing url"})
                return
            try:
                req = urllib.request.Request(url, headers={"User-Agent": "HermesModernVulnAPI-SSRF-Lab"})
                with urllib.request.urlopen(req, timeout=4) as r:
                    data = r.read(300)
                    code = getattr(r, "status", 200)
                self.send_obj(200, {"fetched": url, "status": code, "bytes": len(data), "preview_b64": base64.b64encode(data).decode()})
            except Exception as e:
                self.send_obj(502, {"fetched": url, "error": repr(e)})
            return
        if path == "/callback":
            CALLBACKS.append({"ts": time.time(), "method": "GET", "client": self.client_address[0], "headers": dict(self.headers), "query": parsed.query})
            self.send_obj(200, {"callback": "recorded", "count": len(CALLBACKS), "method": "GET"})
            return
        if path == "/callback-log":
            self.send_obj(200, {"callbacks": CALLBACKS[-20:]})
            return
        if path == "/file-read":
            # Intentional bounded path traversal lab. Reads only the requested
            # path under a lab-owned temp fixture root, but naively joins the
            # user-supplied name so ../ can reach the lab-owned marker file.
            # Do not use against real files or production targets.
            name = qs.get("name", [""])[0]
            if not name:
                self.send_obj(400, {"error": "missing name"})
                return
            candidate = FILE_READ_PUBLIC_DIR / name
            try:
                data = candidate.read_text(encoding="utf-8")
                self.send_obj(200, {"name": name, "resolved": str(candidate), "content": data[:200], "bytes": len(data)})
            except Exception as e:
                self.send_obj(404, {"name": name, "resolved": str(candidate), "error": repr(e)})
            return
        if path == "/deser-log":
            self.send_obj(200, {"events": DESER_EVENTS[-20:]})
            return
        if path == "/xss-reflect":
            # Intentional reflected XSS lab page. Use only with local browser runtime proof.
            value = qs.get("q", [""])[0]
            body = f"""<!doctype html>
<html><head><meta charset='utf-8'><title>XSS Lab</title></head>
<body><h1>Reflected XSS Lab</h1><div id='sink'>{value}</div></body></html>""".encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        self.send_obj(404, {"error": "not found", "path": path})

    def do_POST(self) -> None:
        parsed = urlparse(self.path)
        path = parsed.path
        if path == "/api/login":
            body = read_json(self)
            u = body.get("username", "")
            p = body.get("password", "")
            if u in USERS and USERS[u]["password"] == p:
                self.send_obj(200, {"token": token_for(u), "username": u, "id": USERS[u]["id"]})
            else:
                self.send_obj(403, {"error": "bad credentials"})
            return
        if path == "/upload":
            u = auth_user(self)
            if not u:
                self.send_obj(401, {"error": "missing bearer token"})
                return
            n = int(self.headers.get("Content-Length", "0") or 0)
            data = self.rfile.read(n) if n else b""
            upload_id = uuid.uuid4().hex[:12]
            name = self.headers.get("X-Filename", "upload.bin")
            ctype = self.headers.get("Content-Type", "application/octet-stream")
            out = UPLOAD_DIR / upload_id
            out.write_bytes(data)
            UPLOADS[upload_id] = {"path": str(out), "name": name, "content_type": ctype, "owner": u, "bytes": len(data)}
            self.send_obj(201, {"upload_id": upload_id, "owner": u, "bytes": len(data), "retrieve": f"/uploads/{upload_id}"})
            return
        if path == "/callback":
            CALLBACKS.append({"ts": time.time(), "client": self.client_address[0], "headers": dict(self.headers)})
            self.send_obj(200, {"callback": "recorded", "count": len(CALLBACKS)})
            return
        if path == "/xxe":
            # Bounded XXE-style lab: intentionally expands only the known safe marker file.
            n = int(self.headers.get("Content-Length", "0") or 0)
            raw = self.rfile.read(n).decode("utf-8", "replace") if n else ""
            marker = ""
            if "<!ENTITY" in raw and f"file://{XXE_MARKER_FILE}" in raw:
                marker = XXE_MARKER_FILE.read_text(encoding="utf-8").strip()
            self.send_obj(200, {"parsed": True, "xxe_marker": marker, "marker_file": str(XXE_MARKER_FILE)})
            return
        if path == "/deserialize":
            # Intentional unsafe pickle lab, bounded by local-only test payloads.
            body = read_json(self)
            payload_b64 = body.get("payload_b64", "")
            try:
                obj = pickle.loads(base64.b64decode(payload_b64))
                self.send_obj(200, {"deserialized_type": type(obj).__name__, "result": repr(obj), "events": DESER_EVENTS[-5:]})
            except Exception as e:
                self.send_obj(400, {"error": repr(e), "events": DESER_EVENTS[-5:]})
            return
        self.send_obj(404, {"error": "not found", "path": path})


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--host", default="0.0.0.0")
    ap.add_argument("--port", type=int, default=18080)
    args = ap.parse_args()
    srv = ThreadingHTTPServer((args.host, args.port), Handler)
    print(f"Hermes Modern Vuln API listening on http://{args.host}:{args.port}", flush=True)
    srv.serve_forever()


if __name__ == "__main__":
    main()
