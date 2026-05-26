from __future__ import annotations

import sqlite3
from pathlib import Path


SCHEMA = """
CREATE TABLE users (
  user_id INTEGER PRIMARY KEY,
  signup_date TEXT NOT NULL
);
CREATE TABLE events (
  user_id INTEGER NOT NULL,
  event_date TEXT NOT NULL
);
"""


def _run(query: str, users: list[tuple], events: list[tuple]) -> tuple[list[str], list[tuple]]:
    conn = sqlite3.connect(":memory:")
    conn.executescript(SCHEMA)
    conn.executemany("INSERT INTO users VALUES (?, ?)", users)
    conn.executemany("INSERT INTO events VALUES (?, ?)", events)
    cursor = conn.execute(query)
    columns = [item[0] for item in cursor.description]
    rows = cursor.fetchall()
    return columns, rows


def grade_workspace(workspace_path: Path, task) -> dict:
    query = (workspace_path / "answer.sql").read_text(encoding="utf-8")
    checks = []
    expected_columns = [
        "anchor_date",
        "eligible_users",
        "retained_users",
        "retention_rate",
    ]

    users_1 = [
        (1, "2025-01-01"),
        (2, "2025-01-02"),
        (3, "2025-01-04"),
    ]
    events_1 = [
        (1, "2025-01-07"),
        (2, "2025-01-07"),
        (2, "2025-01-07"),
        (3, "2025-01-09"),
    ]
    rows_1_expected = [
        ("2025-01-01", 0, 0, 0.0),
        ("2025-01-02", 0, 0, 0.0),
        ("2025-01-03", 0, 0, 0.0),
        ("2025-01-04", 0, 0, 0.0),
        ("2025-01-05", 0, 0, 0.0),
        ("2025-01-06", 0, 0, 0.0),
        ("2025-01-07", 1, 1, 1.0),
        ("2025-01-08", 2, 2, 1.0),
        ("2025-01-09", 2, 2, 1.0),
    ]
    columns_1, rows_1 = _run(query, users_1, events_1)
    checks.append(
        {
            "name": "columns",
            "passed": columns_1 == expected_columns,
            "expected": expected_columns,
            "actual": columns_1,
        }
    )
    checks.append(
        {
            "name": "visible_like_dataset",
            "passed": rows_1 == rows_1_expected,
            "expected": rows_1_expected,
            "actual": rows_1,
        }
    )

    users_2 = [
        (10, "2025-02-01"),
        (11, "2025-02-01"),
        (12, "2025-02-03"),
        (13, "2025-02-05"),
    ]
    events_2 = [
        (10, "2025-02-07"),
        (10, "2025-02-08"),
        (11, "2025-02-08"),
        (11, "2025-02-08"),
        (13, "2025-02-12"),
    ]
    rows_2_expected = [
        ("2025-02-01", 0, 0, 0.0),
        ("2025-02-02", 0, 0, 0.0),
        ("2025-02-03", 0, 0, 0.0),
        ("2025-02-04", 0, 0, 0.0),
        ("2025-02-05", 0, 0, 0.0),
        ("2025-02-06", 0, 0, 0.0),
        ("2025-02-07", 2, 1, 0.5),
        ("2025-02-08", 2, 2, 1.0),
        ("2025-02-09", 3, 2, 0.6666666666666666),
        ("2025-02-10", 3, 2, 0.6666666666666666),
        ("2025-02-11", 4, 2, 0.5),
        ("2025-02-12", 4, 3, 0.75)
    ]
    _, rows_2 = _run(query, users_2, events_2)
    checks.append(
        {
            "name": "hidden_dataset_with_gaps_and_duplicates",
            "passed": rows_2 == rows_2_expected,
            "expected": rows_2_expected,
            "actual": rows_2,
        }
    )

    passed = all(item["passed"] for item in checks)
    return {
        "score": 1.0 if passed else 0.0,
        "passed": passed,
        "checks": checks,
        "summary": "Rolling retention query graded on visible and hidden datasets with duplicates and date gaps.",
    }
