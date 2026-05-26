from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

from stack.config import get_settings


def _spawn(module: str, cwd: Path, env: dict[str, str], log_path: Path) -> subprocess.Popen:
    log_path.parent.mkdir(parents=True, exist_ok=True)
    handle = log_path.open("a", encoding="utf-8")
    return subprocess.Popen(
        [sys.executable, "-m", module],
        cwd=cwd,
        env=env,
        stdout=handle,
        stderr=subprocess.STDOUT,
    )


def main() -> None:
    settings = get_settings()
    repo_root = Path(__file__).resolve().parents[1]
    env = os.environ.copy()
    env["PYTHONUNBUFFERED"] = "1"

    # BUG: this should use the configured state directory, not a hard-coded path.
    state_dir = repo_root / "var" / "run"
    state_dir.mkdir(parents=True, exist_ok=True)

    processes = {
        "web": _spawn("stack.web", repo_root, env, state_dir / "web.log"),
        "worker": _spawn("stack.worker", repo_root, env, state_dir / "worker.log"),
        "mailer": _spawn("stack.mailer", repo_root, env, state_dir / "mailer.log"),
    }
    payload = {
        "port": settings["port"],
        "state_dir": str(state_dir),
        "pids": {name: process.pid for name, process in processes.items()},
    }
    (state_dir / "pids.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
