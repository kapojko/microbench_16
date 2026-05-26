from __future__ import annotations

import json
import time
import urllib.error
import urllib.request
from pathlib import Path

from stack.config import get_settings


def _read_heartbeat(path: Path) -> tuple[bool, float | None]:
    if not path.exists():
        return False, None
    try:
        timestamp = float(path.read_text(encoding="utf-8").strip())
    except ValueError:
        return False, None
    return True, time.time() - timestamp


def main() -> None:
    settings = get_settings()

    # BUG: these should respect configured values and actual heartbeat freshness.
    state_dir = Path("var/run")
    url = "http://127.0.0.1:8123/ready"

    web_ok = False
    status_code = None
    try:
        with urllib.request.urlopen(url, timeout=1.0) as response:
            status_code = response.status
            web_ok = status_code == 200
    except (urllib.error.URLError, TimeoutError):
        web_ok = False

    worker_ok = (state_dir / "worker.ready").exists()
    mailer_ready = (state_dir / "mailer.ready").exists()
    mailer_ok = mailer_ready and (state_dir / "mailer.heartbeat").exists()

    payload = {
        "ok": web_ok and worker_ok and mailer_ok,
        "port": settings["port"],
        "state_dir": str(state_dir),
        "web": {"ok": web_ok, "status_code": status_code, "url": url},
        "worker": {"ok": worker_ok},
        "mailer": {"ok": mailer_ok, "ready_marker": mailer_ready},
    }
    print(json.dumps(payload))


if __name__ == "__main__":
    main()
