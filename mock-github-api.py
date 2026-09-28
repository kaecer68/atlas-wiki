#!/usr/bin/env python3
"""mock-github-api.py — 供護欄自測使用的極簡 GitHub API mock（2026-09-28）

用法: python3 mock-github-api.py <port> <label_actor> [approver]
  GET /repos/*/issues/<n>/timeline → 一筆 labeled 事件（actor=<label_actor>）
  GET /repos/*/pulls/<n>/reviews  → 若有 approver ⇒ 一筆 APPROVED（user.login=<approver>）
"""
import json, sys
from http.server import BaseHTTPRequestHandler, HTTPServer

PORT = int(sys.argv[1]); LABEL_ACTOR = sys.argv[2]
APPROVER = sys.argv[3] if len(sys.argv) > 3 else ""


class H(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def do_GET(self):
        if "/timeline" in self.path:
            body = [{"event": "labeled", "label": {"name": "kaecer-reviewed"},
                     "actor": {"login": LABEL_ACTOR}}] if LABEL_ACTOR else []
        elif "/reviews" in self.path:
            body = [{"state": "APPROVED", "user": {"login": APPROVER}}] if APPROVER else []
        else:
            body = []
        raw = json.dumps(body).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)


HTTPServer(("127.0.0.1", PORT), H).serve_forever()
