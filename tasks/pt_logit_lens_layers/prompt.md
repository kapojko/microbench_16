# Task: `pt_logit_lens_layers`

Repair `logit_lens.py`.

Implement:

```python
def logit_lens_topk(hidden_states, ln_weight, ln_bias, lm_head, k):
    ...
```

## Inputs

- `hidden_states`: `list[num_layers][num_tokens][d_model]`
- `ln_weight`: `list[d_model]`
- `ln_bias`: `list[d_model]`
- `lm_head`: `list[vocab_size][d_model]`
- `k`: number of token ids to return per layer

## Contract

For each layer:

1. take the **final token** hidden state from that layer
2. apply layer norm with:

```python
mean = sum(x) / d_model
var = sum((x - mean) ** 2) / d_model
normalized_i = ((x_i - mean) / sqrt(var + eps)) * ln_weight_i + ln_bias_i
```

Use `eps = 1e-5`.

3. compute logits by dotting the normalized vector with each row in `lm_head`
4. return the top-`k` token ids for that layer

Top-k order must be:

- descending logit
- ascending token id to break ties

Return shape:

```python
list[num_layers][k]
```

## Visible Check

Run:

```bash
python3 visible_check.py
```
