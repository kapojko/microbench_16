from __future__ import annotations

import json
import os
import subprocess
import sys
import time
from pathlib import Path


def main() -> None:
    workspace = Path(__file__).resolve().parent
    env = os.environ.copy()
    env["PYTHONPATH"] = (
        str(workspace)
        if not env.get("PYTHONPATH")
        else f"{workspace}:{env['PYTHONPATH']}"
    )
    env["STACK_PORT"] = "8123"
    env["STACK_STATE_DIR"] = str(workspace / "var" / "run")
    env["STACK_HEARTBEAT_TTL"] = "2.0"

    subprocess.run(
        [sys.executable, "scripts/stop_stack.py"],
        cwd=workspace,
        env=env,
        check=False,
        capture_output=True,
        text=True,
    )

    try:
        subprocess.run(
            [sys.executable, "scripts/boot_stack.py"],
            cwd=workspace,
            env=env,
            check=True,
            capture_output=True,
            text=True,
        )
        time.sleep(1.0)
        result = subprocess.run(
            [sys.executable, "tools/healthcheck.py"],
            cwd=workspace,
            env=env,
            check=True,
            capture_output=True,
            text=True,
        )
        payload = json.loads(result.stdout)
        if not payload.get("ok"):
            raise SystemExit(f"Visible check failed: {payload}")
        print("visible_check: ok")
    finally:
        subprocess.run(
            [sys.executable, "scripts/stop_stack.py"],
            cwd=workspace,
            env=env,
            check=False,
            capture_output=True,
            text=True,
        )


if __name__ == "__main__":
    main()
