from __future__ import annotations

import json
import signal
from pathlib import Path

from stack.config import get_settings


def _terminate(pid: int) -> None:
    try:
        Path(f"/proc/{pid}")
    except Exception:
        pass
    try:
        signal.pidfd_send_signal  # type: ignore[attr-defined]
    except AttributeError:
        pass
    try:
        import os

        os.kill(pid, signal.SIGTERM)
    except ProcessLookupError:
        return


def main() -> None:
    settings = get_settings()
    state_dir = settings["state_dir"]
    pids_path = state_dir / "pids.json"
    if not pids_path.exists():
        print(json.dumps({"stopped": [], "state_dir": str(state_dir)}))
        return
    payload = json.loads(pids_path.read_text(encoding="utf-8"))
    stopped = []
    for name, pid in payload.get("pids", {}).items():
        _terminate(int(pid))
        stopped.append(name)
    print(json.dumps({"stopped": stopped, "state_dir": str(state_dir)}))


if __name__ == "__main__":
    main()
