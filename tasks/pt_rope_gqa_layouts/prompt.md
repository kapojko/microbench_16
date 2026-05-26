# Task: `pt_rope_gqa_layouts`

Repair `rope_gqa.py`.

The file uses pure Python nested lists to mimic tensor shapes:

- `q`: `[batch][seq][q_heads][dim]`
- `k`: `[batch][seq][kv_heads][dim]`
- `cos`: `[seq][rotary_dim / 2]`
- `sin`: `[seq][rotary_dim / 2]`

Implement:

```python
def apply_rope_gqa(q, k, cos, sin, rope_layout="half_split"):
    ...
```

## Requirements

- Support `rope_layout="half_split"` and `rope_layout="interleaved"`.
- Rotate only the first `rotary_dim` dimensions.
- Leave the remaining tail dimensions unchanged.
- Apply the same per-position rotation to all heads.
- Preserve input shapes.

## Visible Check

Run:

```bash
python3 visible_check.py
```
