from __future__ import annotations

import sqlite3
from pathlib import Path


SCHEMA = """
CREATE TABLE events (
  user_id INTEGER NOT NULL,
  event_ts TEXT NOT NULL
);
"""


def _run(query: str, events: list[tuple[int, str]]) -> tuple[list[str], list[tuple]]:
    conn = sqlite3.connect(":memory:")
    conn.executescript(SCHEMA)
    conn.executemany("INSERT INTO events VALUES (?, ?)", events)
    cursor = conn.execute(query)
    columns = [item[0] for item in cursor.description]
    rows = cursor.fetchall()
    return columns, rows


def grade_workspace(workspace_path: Path, task) -> dict:
    query = (workspace_path / "answer.sql").read_text(encoding="utf-8")
    checks = []
    expected_columns = [
        "user_id",
        "session_index",
        "session_start_ts",
        "session_end_ts",
        "event_count",
    ]

    events_1 = [
        (1, "2025-03-01 09:00:00"),
        (1, "2025-03-01 09:10:00"),
        (1, "2025-03-01 09:50:00"),
        (1, "2025-03-01 10:25:00"),
        (2, "2025-03-01 12:00:00"),
        (2, "2025-03-01 12:30:00"),
        (2, "2025-03-01 13:01:00"),
    ]
    rows_1_expected = [
        (1, 1, "2025-03-01 09:00:00", "2025-03-01 09:10:00", 2),
        (1, 2, "2025-03-01 09:50:00", "2025-03-01 09:50:00", 1),
        (1, 3, "2025-03-01 10:25:00", "2025-03-01 10:25:00", 1),
        (2, 1, "2025-03-01 12:00:00", "2025-03-01 12:30:00", 2),
        (2, 2, "2025-03-01 13:01:00", "2025-03-01 13:01:00", 1),
    ]
    columns_1, rows_1 = _run(query, events_1)
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

    events_2 = [
        (7, "2025-03-01 23:50:00"),
        (7, "2025-03-02 00:10:00"),
        (7, "2025-03-02 00:40:00"),
        (7, "2025-03-02 01:11:00"),
        (8, "2025-03-02 08:00:00"),
        (8, "2025-03-02 08:00:00"),
        (8, "2025-03-02 08:45:00"),
        (9, "2025-03-02 14:00:00"),
        (9, "2025-03-02 14:29:59"),
        (9, "2025-03-02 14:59:59")
    ]
    rows_2_expected = [
        (7, 1, "2025-03-01 23:50:00", "2025-03-02 00:40:00", 3),
        (7, 2, "2025-03-02 01:11:00", "2025-03-02 01:11:00", 1),
        (8, 1, "2025-03-02 08:00:00", "2025-03-02 08:00:00", 2),
        (8, 2, "2025-03-02 08:45:00", "2025-03-02 08:45:00", 1),
        (9, 1, "2025-03-02 14:00:00", "2025-03-02 14:59:59", 3)
    ]
    _, rows_2 = _run(query, events_2)
    checks.append(
        {
            "name": "hidden_dataset_with_boundaries_duplicates_and_cross_midnight",
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
        "summary": "Sessionization query graded on exact 30-minute boundaries, duplicates, and cross-midnight timestamp handling.",
    }
