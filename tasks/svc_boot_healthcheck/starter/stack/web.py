from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, HTTPServer

from stack.config import get_settings


class Handler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:  # noqa: N802
        if self.path != "/health":
            self.send_response(404)
            self.end_headers()
            return
        payload = {"ok": True, "component": "web"}
        body = json.dumps(payload).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *_args) -> None:
        return


def main() -> None:
    settings = get_settings()
    server = HTTPServer((settings["host"], settings["port"]), Handler)
    server.serve_forever()


if __name__ == "__main__":
    main()
