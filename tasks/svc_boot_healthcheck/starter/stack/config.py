from __future__ import annotations

import os
from pathlib import Path


def get_settings() -> dict[str, object]:
    state_dir = Path(os.environ.get("STACK_STATE_DIR", "var/run"))
    return {
        "host": "127.0.0.1",
        "port": int(os.environ.get("STACK_PORT", "8123")),
        "state_dir": state_dir,
        "heartbeat_ttl": float(os.environ.get("STACK_HEARTBEAT_TTL", "2.0")),
    }
