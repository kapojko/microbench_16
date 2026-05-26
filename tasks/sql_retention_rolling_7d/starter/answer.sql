SELECT
  signup_date AS anchor_date,
  COUNT(*) AS eligible_users,
  0 AS retained_users,
  0.0 AS retention_rate
FROM users
GROUP BY signup_date
ORDER BY signup_date;
