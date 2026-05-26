# Task: `pt_prompt_blend_prob_space`

Repair `prompt_blend.py`.

Implement:

```python
def blend_branch_log_probs(branch_log_probs, weights):
    ...
```

Inputs:

- `branch_log_probs`: list of branches, each a list of log-probabilities over the same vocabulary
- `weights`: positive branch weights

## Requirements

- Mix branches in **probability space**, not log space.
- Normalize weights internally.
- Return blended **log-probabilities**.
- Be numerically stable enough for very small probabilities.

## Visible Check

Run:

```bash
python3 visible_check.py
```
