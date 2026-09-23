"""Minimal HTTP service for the Prismatic multi-repo deploy pilot.

GET /health   -> 200 {"ok": true, "version": "<__version__>"}
GET /version  -> 200 <__version__> (plain text)

Port: argv[1] or $PILOT_PORT or 9461. Stdlib only.
"""

from __future__ import annotations

import json
import os
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from pilot_service import __version__


class Handler(BaseHTTPRequestHandler):
    server_version = "PilotService/1.0"

    def _send_json(self, code: int, payload: dict) -> None:
        body = json.dumps(payload).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:  # noqa: N802 - http.server convention
        if self.path == "/health":
            self._send_json(200, {"ok": True, "version": __version__})
        elif self.path == "/version":
            body = __version__.encode()
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        else:
            self._send_json(404, {"ok": False, "error": "not found"})

    def log_message(self, fmt: str, *args: object) -> None:
        sys.stderr.write("pilot: " + fmt % args + "\n")


def main() -> None:
    port = int(sys.argv[1] if len(sys.argv) > 1 else os.environ.get("PILOT_PORT", "9461"))
    server = ThreadingHTTPServer(("0.0.0.0", port), Handler)
    print(f"pilot_service {__version__} listening on :{port}", flush=True)
    server.serve_forever()


if __name__ == "__main__":
    main()
