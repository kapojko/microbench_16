from __future__ import annotations

import subprocess
import textwrap
from pathlib import Path


VISIBLE_C = r"""
#include <stdio.h>
#include <stdlib.h>
#include "ring_buffer.h"

int main(void) {
    int storage[3] = {0};
    ring_buffer_t rb;
    int value = 0;

    rb_init(&rb, storage, 3);
    rb_push(&rb, 10);
    rb_push(&rb, 20);
    rb_push(&rb, 30);
    if (!rb_peek_oldest(&rb, &value) || value != 10) return 1;
    if (!rb_peek_newest(&rb, &value) || value != 30) return 2;
    return 0;
}
"""


def main() -> None:
    workspace = Path(__file__).resolve().parent
    temp_c = workspace / "visible_main.c"
    binary = workspace / "visible_main"
    temp_c.write_text(textwrap.dedent(VISIBLE_C), encoding="utf-8")
    try:
        compile_result = subprocess.run(
            [
                "gcc",
                "-std=c11",
                "-Wall",
                "-Wextra",
                "-Werror",
                "ring_buffer.c",
                "visible_main.c",
                "-o",
                str(binary),
            ],
            cwd=workspace,
            capture_output=True,
            text=True,
        )
        if compile_result.returncode != 0:
            raise SystemExit(compile_result.stderr)
        run_result = subprocess.run([str(binary)], cwd=workspace, capture_output=True, text=True)
        if run_result.returncode != 0:
            raise SystemExit(f"Visible check failed with exit code {run_result.returncode}")
        print("visible_check: ok")
    finally:
        if temp_c.exists():
            temp_c.unlink()
        if binary.exists():
            binary.unlink()


if __name__ == "__main__":
    main()
