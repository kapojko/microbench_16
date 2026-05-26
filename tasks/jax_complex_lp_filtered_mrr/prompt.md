# Task: `jax_complex_lp_filtered_mrr`

Repair `complex_lp.py`.

The task is written in pure Python lists, but the semantics are the usual ComplEx link-prediction equations.

## Requirements

- `complex_score(...)` must compute the real part of `<h ⊙ r, conj(t)>`.
- `filtered_mrr(...)` performs **tail prediction** for each triple.
- When ranking candidate tails for `(h, r, ?)`:
  - filter out other known true tails for the same `(h, r)`
  - keep the target tail itself in the candidate set
- Rank higher scores first.
- Return the mean reciprocal rank as a float.

## Visible Check

Run:

```bash
python3 visible_check.py
```
