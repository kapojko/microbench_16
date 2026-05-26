from __future__ import annotations

import subprocess
from pathlib import Path


VISIBLE_MAIN = r"""
#include <iostream>
#include <vector>

#include "csv_groupby.h"

int main(void) {
    const std::string csv =
        "team,city,points\n"
        "alpha,Berlin,4\n"
        "beta,\"New York, NY\",7\n"
        "alpha,Paris,3\n"
        "beta,Boston,1\n";

    const auto rows = summarize_csv(csv);
    if (rows.size() != 2) return 10;
    if (rows[0].team != "beta" || rows[0].total_points != 8 || rows[0].row_count != 2) return 11;
    if (rows[1].team != "alpha" || rows[1].total_points != 7 || rows[1].row_count != 2) return 12;
    return 0;
}
"""


def main() -> None:
    workspace = Path(__file__).resolve().parent
    temp_cpp = workspace / "mb12_visible.cpp"
    binary = workspace / "mb12_visible"
    temp_cpp.write_text(VISIBLE_MAIN, encoding="utf-8")
    try:
        compile_result = subprocess.run(
            [
                "g++",
                "-std=c++17",
                "-Wall",
                "-Wextra",
                "-Werror",
                "csv_groupby.cpp",
                "mb12_visible.cpp",
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
            raise SystemExit(f"visible_check failed with code {run_result.returncode}")
    finally:
        if temp_cpp.exists():
            temp_cpp.unlink()
        if binary.exists():
            binary.unlink()
    print("visible_check: ok")


if __name__ == "__main__":
    main()
