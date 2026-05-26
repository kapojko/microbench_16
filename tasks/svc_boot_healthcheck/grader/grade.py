from __future__ import annotations

import json
import os
import signal
import subprocess
import sys
import time
from pathlib import Path


def _run(
    workspace_path: Path,
    env: dict[str, str],
    *args: str,
    check: bool = True,
    timeout: float = 20,
) -> subprocess.CompletedProcess:
    cmd = [sys.executable, *args]
    try:
        return subprocess.run(
            cmd,
            cwd=workspace_path,
            env=env,
            check=check,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
    except subprocess.TimeoutExpired as exc:
        return subprocess.CompletedProcess(
            cmd,
            -signal.SIGKILL,
            exc.stdout or "",
            (exc.stderr or "") + f"\nTimed out after {timeout} seconds.",
        )


def _env_with_pythonpath(workspace_path: Path) -> dict[str, str]:
    env = os.environ.copy()
    env["PYTHONPATH"] = (
        str(workspace_path)
        if not env.get("PYTHONPATH")
        else f"{workspace_path}:{env['PYTHONPATH']}"
    )
    return env


def _load_pids(state_dir: Path) -> dict[str, int]:
    payload = json.loads((state_dir / "pids.json").read_text(encoding="utf-8"))
    return {name: int(pid) for name, pid in payload["pids"].items()}


def _terminate(pid: int) -> None:
    try:
        os.kill(pid, signal.SIGTERM)
    except ProcessLookupError:
        return


def grade_workspace(workspace_path: Path, task) -> dict:
    checks = []
    state_dir = workspace_path / "hidden_state"
    env = _env_with_pythonpath(workspace_path)
    env["STACK_PORT"] = "8137"
    env["STACK_STATE_DIR"] = str(state_dir)
    env["STACK_HEARTBEAT_TTL"] = "1.0"

    _run(workspace_path, env, "scripts/stop_stack.py", check=False)

    try:
        boot = _run(workspace_path, env, "scripts/boot_stack.py", check=False)
        checks.append(
            {
                "name": "boot_command_exits_cleanly",
                "passed": boot.returncode == 0,
                "expected": 0,
                "actual": boot.returncode,
                "stdout": boot.stdout[-4000:],
                "stderr": boot.stderr[-4000:],
            }
        )
        if boot.returncode != 0:
            return {
                "score": 0.0,
                "passed": False,
                "checks": checks,
                "summary": "Service stack failed before hidden health checks could run.",
            }
        time.sleep(1.2)

        healthy = _run(workspace_path, env, "tools/healthcheck.py", check=False)
        checks.append(
            {
                "name": "healthcheck_command_exits_cleanly",
                "passed": healthy.returncode == 0,
                "expected": 0,
                "actual": healthy.returncode,
                "stdout": healthy.stdout[-4000:],
                "stderr": healthy.stderr[-4000:],
            }
        )
        if healthy.returncode != 0:
            return {
                "score": 0.0,
                "passed": False,
                "checks": checks,
                "summary": "Service stack booted, but the healthcheck command itself failed.",
            }
        healthy_payload = json.loads(healthy.stdout)
        checks.append(
            {
                "name": "custom_env_boot_and_health",
                "passed": (
                    healthy_payload.get("ok") is True
                    and healthy_payload.get("port") == 8137
                    and healthy_payload.get("state_dir") == str(state_dir)
                ),
                "expected": {
                    "ok": True,
                    "port": 8137,
                    "state_dir": str(state_dir),
                },
                "actual": healthy_payload,
            }
        )

        pids_path = state_dir / "pids.json"
        checks.append(
            {
                "name": "boot_wrote_pid_file",
                "passed": pids_path.exists(),
                "expected": {"exists": True, "path": str(pids_path)},
                "actual": {"exists": pids_path.exists(), "path": str(pids_path)},
            }
        )
        if not pids_path.exists():
            return {
                "score": 0.0,
                "passed": False,
                "checks": checks,
                "summary": "Service stack booted, but did not emit the pid file required for stale-worker validation.",
            }

        pids = _load_pids(state_dir)
        _terminate(pids["worker"])
        time.sleep(1.3)

        stale = _run(workspace_path, env, "tools/healthcheck.py", check=False)
        checks.append(
            {
                "name": "stale_healthcheck_command_exits_cleanly",
                "passed": stale.returncode == 0,
                "expected": 0,
                "actual": stale.returncode,
                "stdout": stale.stdout[-4000:],
                "stderr": stale.stderr[-4000:],
            }
        )
        if stale.returncode != 0:
            return {
                "score": 0.0,
                "passed": False,
                "checks": checks,
                "summary": "Service stack booted, but stale-worker validation could not execute cleanly.",
            }
        stale_payload = json.loads(stale.stdout)
        checks.append(
            {
                "name": "stale_worker_detected",
                "passed": (
                    stale_payload.get("ok") is False
                    and stale_payload.get("worker", {}).get("ok") is False
                ),
                "expected": {"ok": False, "worker": {"ok": False}},
                "actual": stale_payload,
            }
        )
    finally:
        _run(workspace_path, env, "scripts/stop_stack.py", check=False)

    passed = all(item["passed"] for item in checks)
    return {
        "score": 1.0 if passed else 0.0,
        "passed": passed,
        "checks": checks,
        "summary": "Service stack graded on custom-env boot and stale-heartbeat detection.",
    }
