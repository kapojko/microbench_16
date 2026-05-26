from __future__ import annotations

import subprocess
from pathlib import Path


HIDDEN_C = r"""
#include <stdio.h>
#include "ring_buffer.h"

int main(void) {
    int storage[3] = {0};
    ring_buffer_t rb;
    int value = 0;

    rb_init(&rb, storage, 3);
    rb_push(&rb, 1);
    rb_push(&rb, 2);
    rb_push(&rb, 3);
    rb_push(&rb, 4);  // overwrite 1

    if (rb_len(&rb) != 3) return 10;
    if (!rb_peek_oldest(&rb, &value) || value != 2) return 11;
    if (!rb_peek_newest(&rb, &value) || value != 4) return 12;
    if (!rb_pop_oldest(&rb, &value) || value != 2) return 13;
    if (!rb_pop_oldest(&rb, &value) || value != 3) return 14;
    rb_push(&rb, 5);
    if (!rb_peek_oldest(&rb, &value) || value != 4) return 15;
    if (!rb_peek_newest(&rb, &value) || value != 5) return 16;
    return 0;
}
"""


def grade_workspace(workspace_path: Path, task) -> dict:
    temp_c = workspace_path / "mb12_hidden_check.c"
    binary = workspace_path / "mb12_hidden_check"
    checks = []
    temp_c.write_text(HIDDEN_C, encoding="utf-8")
    try:
        compile_result = subprocess.run(
            [
                "gcc",
                "-std=c11",
                "-Wall",
                "-Wextra",
                "-Werror",
                "ring_buffer.c",
                "mb12_hidden_check.c",
                "-o",
                str(binary),
            ],
            cwd=workspace_path,
            capture_output=True,
            text=True,
            timeout=30,
        )
        checks.append(
            {
                "name": "compile",
                "passed": compile_result.returncode == 0,
                "expected": 0,
                "actual": compile_result.returncode,
                "stderr": compile_result.stderr[-4000:],
            }
        )
        if compile_result.returncode == 0:
            try:
                run_result = subprocess.run(
                    [str(binary)],
                    cwd=workspace_path,
                    capture_output=True,
                    text=True,
                    timeout=5,
                )
                run_check = {
                    "name": "runtime_semantics",
                    "passed": run_result.returncode == 0,
                    "expected": 0,
                    "actual": run_result.returncode,
                    "stdout": run_result.stdout[-4000:],
                    "stderr": run_result.stderr[-4000:],
                }
            except subprocess.TimeoutExpired as exc:
                run_check = {
                    "name": "runtime_semantics",
                    "passed": False,
                    "expected": 0,
                    "actual": "timeout",
                    "stdout": (exc.stdout or "")[-4000:],
                    "stderr": (exc.stderr or "")[-4000:],
                }
            checks.append(
                run_check
            )
    finally:
        if temp_c.exists():
            temp_c.unlink()
        if binary.exists():
            binary.unlink()

    passed = all(item["passed"] for item in checks)
    return {
        "score": 1.0 if passed else 0.0,
        "passed": passed,
        "checks": checks,
        "summary": "Ring buffer graded by compiling and executing a hidden C semantics check.",
    }
