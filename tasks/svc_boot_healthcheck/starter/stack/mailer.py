from __future__ import annotations

import time

from stack.config import get_settings


def main() -> None:
    settings = get_settings()
    state_dir = settings["state_dir"]
    state_dir.mkdir(parents=True, exist_ok=True)
    (state_dir / "mailer.ready").write_text("ready\n", encoding="utf-8")
    heartbeat = state_dir / "mailer.heartbeat"
    while True:
        heartbeat.write_text(f"{time.time():.6f}\n", encoding="utf-8")
        time.sleep(0.3)


if __name__ == "__main__":
    main()
