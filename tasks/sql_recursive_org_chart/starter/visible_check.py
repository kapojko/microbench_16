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

ROWS = [
    (1, "CEO", None, 1),
    (2, "CTO", 1, 1),
    (3, "CFO", 1, 1),
    (4, "Eng Manager", 2, 1),
    (5, "Engineer", 4, 1),
    (6, "Intern", 4, 0),
    (7, "Analyst", 3, 1),
]

EXPECTED = [
    (2, 1, 1, "1/2"),
    (3, 1, 1, "1/3"),
    (4, 2, 2, "1/2/4"),
    (7, 3, 2, "1/3/7"),
    (5, 4, 3, "1/2/4/5"),
]


def main() -> None:
    query = Path("answer.sql").read_text(encoding="utf-8")
    conn = sqlite3.connect(":memory:")
    conn.executescript(SCHEMA)
    conn.executemany("INSERT INTO employees VALUES (?, ?, ?, ?)", ROWS)
    rows = conn.execute(query, (1,)).fetchall()
    if rows != EXPECTED:
        raise SystemExit(f"Visible check failed.\nExpected: {EXPECTED}\nActual:   {rows}")
    print("visible_check: ok")


if __name__ == "__main__":
    main()
