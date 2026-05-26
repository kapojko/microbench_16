WITH ordered AS (
  SELECT
    user_id,
    event_ts,
    LAG(event_ts) OVER (PARTITION BY user_id ORDER BY event_ts) AS prev_event_ts
  FROM events
),
flagged AS (
  SELECT
    user_id,
    event_ts,
    CASE
      WHEN prev_event_ts IS NULL THEN 1
      WHEN CAST(strftime('%s', event_ts) AS INTEGER) - CAST(strftime('%s', prev_event_ts) AS INTEGER) >= 1800 THEN 1
      ELSE 0
    END AS is_new_session
  FROM ordered
),
sessioned AS (
  SELECT
    user_id,
    event_ts,
    SUM(is_new_session) OVER (
      PARTITION BY user_id
      ORDER BY event_ts
      ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS session_index
  FROM flagged
)
SELECT
  user_id,
  session_index,
  MIN(event_ts) AS session_start_ts,
  MAX(event_ts) AS session_end_ts,
  COUNT(*) AS event_count
FROM sessioned
GROUP BY user_id, session_index
ORDER BY user_id, session_index;
