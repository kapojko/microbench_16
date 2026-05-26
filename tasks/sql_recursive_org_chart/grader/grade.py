from __future__ import annotations

import sqlite3
from pathlib import Path


SCHEMA = """
CREATE TABLE employees (
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
  manager_id INTEGER NULL,
  active INTEGER NOT NULL CHECK (active IN (0, 1))
);
"""

VISIBLE_ROWS = [
    (1, "CEO", None, 1),
    (2, "CTO", 1, 1),
    (3, "CFO", 1, 1),
    (4, "Eng Manager", 2, 1),
    (5, "Engineer", 4, 1),
    (6, "Intern", 4, 0),
    (7, "Analyst", 3, 1),
]

HIDDEN_CYCLE_ROWS = [
    (2, "A", 4, 1),
    (3, "B", 2, 1),
    (4, "C", 3, 1),
    (8, "D", 4, 1),
    (9, "E", 8, 0),
]


def _run_case(query: str, rows: list[tuple], root_id: int) -> tuple[list[str], list[tuple]]:
    conn = sqlite3.connect(":memory:")
    conn.executescript(SCHEMA)
    conn.executemany("INSERT INTO employees VALUES (?, ?, ?, ?)", rows)
    cursor = conn.execute(query, (root_id,))
    column_names = [item[0] for item in cursor.description]
    payload = cursor.fetchall()
    return column_names, payload


def grade_workspace(workspace_path: Path, task) -> dict:
    query = (workspace_path / "answer.sql").read_text(encoding="utf-8")
    checks = []

    columns, visible_rows = _run_case(query, VISIBLE_ROWS, 1)
    expected_visible = [
        (2, 1, 1, "1/2"),
        (3, 1, 1, "1/3"),
        (4, 2, 2, "1/2/4"),
        (7, 3, 2, "1/3/7"),
        (5, 4, 3, "1/2/4/5"),
    ]
    checks.append(
        {
            "name": "visible_dataset",
            "passed": visible_rows == expected_visible,
            "expected": expected_visible,
            "actual": visible_rows,
        }
    )

    expected_columns = ["employee_id", "manager_id", "depth", "path"]
    checks.append(
        {
            "name": "column_names",
            "passed": columns == expected_columns,
            "expected": expected_columns,
            "actual": columns,
        }
    )

    columns2, hidden_rows = _run_case(query, HIDDEN_CYCLE_ROWS, 2)
    expected_hidden = [
        (3, 2, 1, "2/3"),
        (4, 3, 2, "2/3/4"),
        (8, 4, 3, "2/3/4/8"),
    ]
    checks.append(
        {
            "name": "cycle_guard",
            "passed": hidden_rows == expected_hidden,
            "expected": expected_hidden,
            "actual": hidden_rows,
        }
    )
    checks.append(
        {
            "name": "column_names_hidden_case",
            "passed": columns2 == expected_columns,
            "expected": expected_columns,
            "actual": columns2,
        }
    )

    passed = all(item["passed"] for item in checks)
    return {
        "score": 1.0 if passed else 0.0,
        "passed": passed,
        "checks": checks,
        "summary": "Recursive org-chart query graded against visible and cycle-containing hidden datasets.",
    }
