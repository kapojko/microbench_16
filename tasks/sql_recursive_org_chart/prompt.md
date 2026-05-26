# Task: `sql_recursive_org_chart`

You are working with SQLite.

Edit `answer.sql` so that it returns the **active descendants** of the root employee whose id is passed as parameter `?1`.

## Schema

```sql
CREATE TABLE employees (
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
  manager_id INTEGER NULL,
  active INTEGER NOT NULL CHECK (active IN (0, 1))
);
```

## Requirements

- Use a recursive CTE.
- Return exactly these columns:
  - `employee_id`
  - `manager_id`
  - `depth`
  - `path`
- Exclude the root employee itself.
- Traverse only rows where `active = 1`.
- Do not loop forever if the hidden data contains a cycle.
- Do not emit duplicate employees even if a cycle points back to the root.
- `depth` is the number of edges from the root to the employee.
- `path` is a slash-separated chain of ids such as `1/2/5`.
- Order rows by `depth`, then `employee_id`.

## Artifact

Your final query must live in `answer.sql`.

## Visible Check

Run:

```bash
python3 visible_check.py
```
