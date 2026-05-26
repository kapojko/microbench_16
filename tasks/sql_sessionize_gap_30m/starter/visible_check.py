from __future__ import annotations

import sqlite3
from pathlib import Path


SCHEMA = """
CREATE TABLE events (
  user_id INTEGER NOT NULL,
  event_ts TEXT NOT NULL
);
"""


def main() -> None:
    query = (Path(__file__).resolve().parent / "answer.sql").read_text(encoding="utf-8")
    events = [
        (1, "2025-03-01 09:00:00"),
        (1, "2025-03-01 09:10:00"),
        (1, "2025-03-01 09:50:00"),
        (1, "2025-03-01 10:25:00"),
        (2, "2025-03-01 12:00:00"),
        (2, "2025-03-01 12:30:00"),
        (2, "2025-03-01 13:01:00"),
    ]
    expected = [
        (1, 1, "2025-03-01 09:00:00", "2025-03-01 09:10:00", 2),
        (1, 2, "2025-03-01 09:50:00", "2025-03-01 09:50:00", 1),
        (1, 3, "2025-03-01 10:25:00", "2025-03-01 10:25:00", 1),
        (2, 1, "2025-03-01 12:00:00", "2025-03-01 12:30:00", 2),
        (2, 2, "2025-03-01 13:01:00", "2025-03-01 13:01:00", 1),
    ]

    conn = sqlite3.connect(":memory:")
    conn.executescript(SCHEMA)
    conn.executemany("INSERT INTO events VALUES (?, ?)", events)
    cursor = conn.execute(query)
    columns = [item[0] for item in cursor.description]
    rows = cursor.fetchall()

    expected_columns = [
        "user_id",
        "session_index",
        "session_start_ts",
        "session_end_ts",
        "event_count",
    ]
    if columns != expected_columns:
        raise SystemExit(f"Visible check failed.\nExpected columns: {expected_columns}\nActual columns:   {columns}")
    if rows != expected:
        raise SystemExit(f"Visible check failed.\nExpected rows: {expected}\nActual rows:   {rows}")
    print("visible_check: ok")


if __name__ == "__main__":
    main()
