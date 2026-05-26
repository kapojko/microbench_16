# Task: `pt_kv_cache_generate`

Repair `kv_cache_generate.py`.

The toy decoder exposes:

- `prefill(prompt_ids)` -> cache after consuming the prompt
- `decode_next(token_id, cache)` -> updated cache after appending one token
- `logits_from_cache(cache)` -> logits for the next token

Implement:

```python
def generate_cached(model, prompt_ids, max_new_tokens):
    ...
```

## Requirements

- Return the list of newly generated token ids.
- Use greedy decoding with `argmax`.
- Match the reference generation behavior exactly.
- Do not recompute the full prompt on every step.

The hidden grader inspects `model.embedding_visits`, so this is a semantic cache task, not just a functional task.

## Visible Check

Run:

```bash
python3 visible_check.py
```
