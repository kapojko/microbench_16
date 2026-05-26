WITH RECURSIVE descendants(employee_id, manager_id, depth, path) AS (
  SELECT
    e.id,
    e.manager_id,
    1,
    printf('%d/%d', ?1, e.id)
  FROM employees e
  WHERE e.manager_id = ?1
    AND e.active = 1

  UNION ALL

  SELECT
    e.id,
    e.manager_id,
    d.depth + 1,
    printf('%s/%d', d.path, e.id)
  FROM employees e
  JOIN descendants d ON e.manager_id = d.employee_id
  WHERE e.active = 1
    AND INSTR('/' || d.path || '/', '/' || CAST(e.id AS TEXT) || '/') = 0
)
SELECT DISTINCT employee_id, manager_id, depth, path
FROM descendants
ORDER BY depth, employee_id;
