# Task: `cpp_csv_groupby_quoted_fields`

Repair `csv_groupby.cpp`.

The file exposes:

```cpp
std::vector<SummaryRow> summarize_csv(const std::string& csv);
```

`csv` is a UTF-8 text blob with this header:

```text
team,city,points
```

Each subsequent row contains:

- `team`: string key
- `city`: arbitrary CSV field that may contain commas or escaped quotes
- `points`: signed integer

## Contract

- Parse CSV rows correctly when fields are quoted with `"..."`.
- Inside quoted fields, doubled quotes `""` mean a literal `"`.
- Ignore `\r` from CRLF input.
- Aggregate by exact `team` string.
- Return one `SummaryRow` per team.
- `total_points` is the sum of the `points` column.
- `row_count` is the number of rows for that team.
- Sort the result by:
  1. `total_points` descending
  2. `team` ascending

## Visible Check

Run:

```bash
python3 visible_check.py
```
