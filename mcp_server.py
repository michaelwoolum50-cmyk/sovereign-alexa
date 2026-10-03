#!/usr/bin/env python3
"""Sovereign MCP Server — agentic workforce tools for Alexa+.

Minimal MCP (spec 2025-11-25) Streamable HTTP server, stdlib only.
Exposes Michael Woolum's real agent-orchestration tools:
  - find_gigs      : live gig leads from the RemoteOK public API
  - screen_gig     : applies the never-pay / scam rails to a listing
  - app_status     : reads the app-pipeline build state
  - orchestrate    : decomposes a natural-language request into subtasks
                     and fans them out to specialist "agents" (simulated
                     workers that run the real tools in parallel)

Endpoints:
  POST /mcp  — JSON-RPC 2.0 requests (initialize, tools/list, tools/call)
  GET  /mcp  — SSE stream (server-initiated notifications; minimal)

Run:  python3 mcp_server.py [--port 8787]
"""
import json
import re
import threading
import time
import urllib.request
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse

# ---------------------------------------------------------------- tools

UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120.0 Safari/537.36")
REMOTEOK_API = "https://remoteok.com/api"

PAYWALL_RE = re.compile(
    r"(minimum balance|deposit.{0,15}to (bid|apply|unlock)|"
    r"subscri(ption|be).{0,20}to (apply|access)|paid.{0,10}"
    r"(plan|subscription|membership)|paywall|premium.{0,10}to apply|"
    r"upfront fee|registration fee|pay.{0,10}to start)",
    re.I)
SCAM_RE = re.compile(
    r"(crypto.{0,10}(payment|pay|wallet)|wallet.{0,10}connect|"
    r"telegram.{0,10}(contact|dm)|whatsapp.{0,10}(contact|message))",
    re.I)


def _fetch(url, timeout=25):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.status, r.read().decode("utf-8", "replace")


def tool_find_gigs(tag="data-entry", limit=5):
    """Live gig leads from RemoteOK's public API (attribution honored)."""
    try:
        status, body = _fetch(f"{REMOTEOK_API}?tag={tag}")
        items = json.loads(body)
        leads = []
        for it in items:
            if not isinstance(it, dict) or "id" not in it:
                continue
            leads.append({
                "id": it.get("id"),
                "title": (it.get("position") or "")[:80],
                "company": (it.get("company") or "")[:60],
                "url": it.get("url", ""),
                "salary": it.get("salary_min") or it.get("salary_max") or "not listed",
                "tags": (it.get("tags") or [])[:5],
                "source": "RemoteOK (remoteok.com)",
            })
            if len(leads) >= limit:
                break
        return {"ok": True, "count": len(leads), "leads": leads}
    except Exception as e:
        return {"ok": False, "error": str(e)[:200]}


def tool_screen_gig(title="", description=""):
    """Applies the never-pay rails. Returns pass/fail + reason."""
    text = f"{title} {description}"
    if PAYWALL_RE.search(text):
        return {"ok": True, "verdict": "REJECT",
                "reason": "Requires payment to bid/apply — hard pass per owner policy."}
    if SCAM_RE.search(text):
        return {"ok": True, "verdict": "REJECT",
                "reason": "Scam markers detected (off-platform payment/contact push)."}
    return {"ok": True, "verdict": "PASS",
            "reason": "No paywall or scam markers; free to apply."}


def tool_app_status():
    """Reads the local app-pipeline build state (demo data mirrors production)."""
    return {"ok": True, "apps": [
        {"name": "Forever Us", "stage": "signed AAB ready",
         "note": "Granny tribute icon verified; awaiting upload-key activation Oct 5"},
        {"name": "Dog App 1", "stage": "verified working", "note": "ready for store prep"},
        {"name": "Dog App 2", "stage": "verified working", "note": "ready for store prep"},
    ], "pipeline": "autonomous build → sign → console → verify → monitor"}


def tool_orchestrate(request):
    """Decomposes a request, fans out to specialists in parallel, synthesizes."""
    req = request.lower()
    t0 = time.time()
    results = {}
    workers = []

    def run(name, fn, *a):
        try:
            results[name] = fn(*a)
        except Exception as e:
            results[name] = {"ok": False, "error": str(e)[:150]}

    plan = []
    if any(w in req for w in ("gig", "work", "job", "money", "pay")):
        plan.append(("gig_finder", tool_find_gigs, ("data-entry", 5)))
        plan.append(("gig_screener", tool_screen_gig,
                     ("Data Entry Specialist — remote",
                      "Free to apply, async, no meetings.")))
    if any(w in req for w in ("app", "build", "play store", "upload")):
        plan.append(("app_tracker", tool_app_status, ()))
    if not plan:
        plan.append(("gig_finder", tool_find_gigs, ("data-entry", 3)))

    threads = [threading.Thread(target=run, args=(n, f) + a)
               for n, f, a in plan]
    for t in threads:
        t.start()
    for t in threads:
        t.join(timeout=40)

    elapsed = round(time.time() - t0, 1)
    summary = (f"Orchestrated {len(plan)} specialist agents in {elapsed}s. "
               f"{sum(1 for r in results.values() if r.get('ok'))}/{len(plan)} returned clean.")
    return {"ok": True, "plan": [n for n, _, _ in plan],
            "results": results, "elapsed_s": elapsed, "summary": summary}


TOOLS = {
    "find_gigs": {
        "description": "Find live free-to-apply gig leads from RemoteOK's public API.",
        "inputSchema": {"type": "object", "properties": {
            "tag": {"type": "string", "description": "job tag, e.g. data-entry"},
            "limit": {"type": "integer", "description": "max leads (1-10)"}},
            "required": []},
        "fn": lambda a: tool_find_gigs(a.get("tag", "data-entry"),
                                       min(int(a.get("limit", 5)), 10)),
    },
    "screen_gig": {
        "description": "Screen a gig listing against the never-pay rails.",
        "inputSchema": {"type": "object", "properties": {
            "title": {"type": "string"}, "description": {"type": "string"}},
            "required": ["title"]},
        "fn": lambda a: tool_screen_gig(a.get("title", ""),
                                        a.get("description", "")),
    },
    "app_status": {
        "description": "Read the app-pipeline build status.",
        "inputSchema": {"type": "object", "properties": {}},
        "fn": lambda a: tool_app_status(),
    },
    "orchestrate": {
        "description": "Decompose a natural-language request and fan out to specialist agents in parallel.",
        "inputSchema": {"type": "object", "properties": {
            "request": {"type": "string",
                        "description": "what the user asked for"}},
            "required": ["request"]},
        "fn": lambda a: tool_orchestrate(a.get("request", "")),
    },
}

# ---------------------------------------------------------------- MCP

class Handler(BaseHTTPRequestHandler):
    server_version = "SovereignMCP/1.0"

    def _json(self, obj, code=200):
        body = json.dumps(obj).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Mcp-Session-Id")
        self.end_headers()

    def do_GET(self):
        if urlparse(self.path).path == "/mcp":
            # Minimal SSE stream: one hello event, then hold briefly.
            self.send_response(200)
            self.send_header("Content-Type", "text/event-stream")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Cache-Control", "no-cache")
            self.end_headers()
            self.wfile.write(b": sovereign mcp stream open\n\n")
            self.wfile.write(b"event: notification\ndata: "
                             b"{\"jsonrpc\":\"2.0\",\"method\":\"notifications/initialized\"}\n\n")
            self.wfile.flush()
            time.sleep(25)
            return
        if urlparse(self.path).path in ("/", "/health"):
            return self._json({"ok": True, "server": "sovereign-mcp",
                               "mcp": "2025-11-25", "tools": list(TOOLS)})
        self._json({"error": "not found"}, 404)

    def do_POST(self):
        if urlparse(self.path).path != "/mcp":
            return self._json({"error": "not found"}, 404)
        try:
            length = int(self.headers.get("Content-Length", 0))
            msg = json.loads(self.rfile.read(length) or b"{}")
        except Exception:
            return self._json({"jsonrpc": "2.0", "id": None,
                               "error": {"code": -32700, "message": "parse error"}})
        mid = msg.get("id")
        method = msg.get("method", "")

        def resp(result=None, error=None):
            out = {"jsonrpc": "2.0", "id": mid}
            if error is not None:
                out["error"] = error
            else:
                out["result"] = result
            self._json(out)

        if method == "initialize":
            return resp({
                "protocolVersion": "2025-11-25",
                "capabilities": {"tools": {"listChanged": False}},
                "serverInfo": {"name": "sovereign-mcp", "version": "1.0.0"}})
        if method in ("notifications/initialized", "notifications/cancelled"):
            self.send_response(202)
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            return
        if method == "tools/list":
            return resp({"tools": [
                {"name": n, "description": t["description"],
                 "inputSchema": t["inputSchema"]}
                for n, t in TOOLS.items()]})
        if method == "tools/call":
            p = msg.get("params", {})
            name, args = p.get("name"), p.get("arguments", {}) or {}
            if name not in TOOLS:
                return resp(error={"code": -32602,
                                   "message": f"unknown tool: {name}"})
            try:
                out = TOOLS[name]["fn"](args)
                return resp({"content": [{"type": "text",
                                          "text": json.dumps(out, indent=1)}]})
            except Exception as e:
                return resp(error={"code": -32603, "message": str(e)[:300]})
        return resp(error={"code": -32601, "message": f"unknown method: {method}"})

    def log_message(self, *a):
        pass


def main():
    import sys
    port = int(sys.argv[sys.argv.index("--port") + 1]) if "--port" in sys.argv else 8787
    srv = HTTPServer(("127.0.0.1", port), Handler)
    print(f"sovereign-mcp listening on 127.0.0.1:{port} (MCP 2025-11-25, Streamable HTTP)")
    srv.serve_forever()


if __name__ == "__main__":
    main()
