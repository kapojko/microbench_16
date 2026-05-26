# Task: `c_ring_buffer_overwrite_semantics`

Repair `ring_buffer.c`.

## Contract

`rb_push` appends a new value.

- If the buffer is not full, length increases by one.
- If the buffer is full, the **oldest** item is overwritten.

`rb_peek_oldest` returns the oldest item without removing it.

`rb_peek_newest` returns the newest item without removing it.

`rb_pop_oldest` removes and returns the oldest item.

## Visible Check

Run:

```bash
python3 visible_check.py
```
