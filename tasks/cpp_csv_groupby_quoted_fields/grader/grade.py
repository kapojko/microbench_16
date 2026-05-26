from __future__ import annotations

import subprocess
from pathlib import Path


HIDDEN_MAIN = r"""
#include <iostream>
#include <string>
#include <vector>

#include "csv_groupby.h"

namespace {

bool expect_row(
    const SummaryRow& row,
    const std::string& team,
    long long total_points,
    int row_count
) {
    return row.team == team && row.total_points == total_points && row.row_count == row_count;
}

}  // namespace

int main(void) {
    {
        const std::string csv =
            "team,city,points\r\n"
            "core,\"San \"\"Fran\"\", CA\",5\r\n"
            "edge,Tokyo,5\r\n"
            "core,Seoul,2\r\n";
        const auto rows = summarize_csv(csv);
        if (rows.size() != 2) return 20;
        if (!expect_row(rows[0], "core", 7, 2)) return 21;
        if (!expect_row(rows[1], "edge", 5, 1)) return 22;
    }

    {
        const std::string csv =
            "team,city,points\n"
            "blue,Rome,3\n"
            "amber,\"A, B\",3\n"
            "amber,Oslo,1\n"
            "blue,Paris,1\n";
        const auto rows = summarize_csv(csv);
        if (rows.size() != 2) return 30;
        if (!expect_row(rows[0], "amber", 4, 2)) return 31;
        if (!expect_row(rows[1], "blue", 4, 2)) return 32;
    }

    return 0;
}
"""


def grade_workspace(workspace_path: Path, task) -> dict:
    temp_cpp = workspace_path / "mb12_hidden_check.cpp"
    binary = workspace_path / "mb12_hidden_check"
    temp_cpp.write_text(HIDDEN_MAIN, encoding="utf-8")
    checks: list[dict] = []
    try:
        compile_result = subprocess.run(
            [
                "g++",
                "-std=c++17",
                "-Wall",
                "-Wextra",
                "-Werror",
                "csv_groupby.cpp",
                "mb12_hidden_check.cpp",
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
                    "name": "quoted_fields_and_sort_semantics",
                    "passed": run_result.returncode == 0,
                    "expected": 0,
                    "actual": run_result.returncode,
                    "stdout": run_result.stdout[-4000:],
                    "stderr": run_result.stderr[-4000:],
                }
            except subprocess.TimeoutExpired as exc:
                run_check = {
                    "name": "quoted_fields_and_sort_semantics",
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
        if temp_cpp.exists():
            temp_cpp.unlink()
        if binary.exists():
            binary.unlink()

    passed = all(item["passed"] for item in checks)
    return {
        "score": 1.0 if passed else 0.0,
        "passed": passed,
        "checks": checks,
        "summary": "C++ CSV task graded on quoted-field parsing, escaped quotes, CRLF handling, and deterministic sort semantics.",
    }
