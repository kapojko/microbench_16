# Task: `sql_sessionize_gap_30m`

Write the final query in `answer.sql`.

The input table is:

```sql
CREATE TABLE events (
  user_id INTEGER NOT NULL,
  event_ts TEXT NOT NULL
);
```

`event_ts` uses the format `YYYY-MM-DD HH:MM:SS`.

## Contract

For each user, order events by timestamp and split them into sessions.

- A new session starts when the gap from the previous event for the same user is **strictly greater than 30 minutes**.
- A gap of exactly 30 minutes stays in the same session.
- Session numbering starts at `1` for each user.

Return these exact columns:

1. `user_id`
2. `session_index`
3. `session_start_ts`
4. `session_end_ts`
5. `event_count`

Sort the final rows by:

1. `user_id` ascending
2. `session_index` ascending

## Visible Check

Run:

```bash
python3 visible_check.py
```
