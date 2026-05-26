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

USERS = [
    (1, "2025-01-01"),
    (2, "2025-01-02"),
    (3, "2025-01-04"),
]

EVENTS = [
    (1, "2025-01-07"),
    (2, "2025-01-07"),
    (2, "2025-01-07"),
    (3, "2025-01-09"),
]

EXPECTED = [
    ("2025-01-01", 0, 0, 0.0),
    ("2025-01-02", 0, 0, 0.0),
    ("2025-01-03", 0, 0, 0.0),
    ("2025-01-04", 0, 0, 0.0),
    ("2025-01-05", 0, 0, 0.0),
    ("2025-01-06", 0, 0, 0.0),
    ("2025-01-07", 1, 1, 1.0),
    ("2025-01-08", 2, 2, 1.0),
    ("2025-01-09", 3, 3, 1.0),
]


def main() -> None:
    query = Path("answer.sql").read_text(encoding="utf-8")
    conn = sqlite3.connect(":memory:")
    conn.executescript(SCHEMA)
    conn.executemany("INSERT INTO users VALUES (?, ?)", USERS)
    conn.executemany("INSERT INTO events VALUES (?, ?)", EVENTS)
    rows = conn.execute(query).fetchall()
    if rows != EXPECTED:
        raise SystemExit(f"Visible check failed.\nExpected: {EXPECTED}\nActual:   {rows}")
    print("visible_check: ok")


if __name__ == "__main__":
    main()
