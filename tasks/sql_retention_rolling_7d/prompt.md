# Task: `sql_retention_rolling_7d`

Edit `answer.sql`.

You are given:

```sql
CREATE TABLE users (
  user_id INTEGER PRIMARY KEY,
  signup_date TEXT NOT NULL
);

CREATE TABLE events (
  user_id INTEGER NOT NULL,
  event_date TEXT NOT NULL
);
```

Dates are ISO strings in `YYYY-MM-DD` format.

## Metric Definition

For every calendar `anchor_date` from the earliest signup/event date through the latest event date inclusive, return:

- `anchor_date`
- `eligible_users`
- `retained_users`
- `retention_rate`

Rules:

- A user is **eligible** on `anchor_date = D` if `signup_date <= date(D, '-6 day')`.
- A user is **retained** on `D` if the user is eligible and has at least one event in the inclusive range `[date(D, '-6 day'), D]`.
- Multiple events for the same user inside the window count once.
- If `eligible_users = 0`, emit `retention_rate = 0.0`.
- Order by `anchor_date`.

## Visible Check

Run:

```bash
python3 visible_check.py
```
