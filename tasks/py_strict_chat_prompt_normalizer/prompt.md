# Task: `py_strict_chat_prompt_normalizer`

Repair `prompt_normalizer.py`.

Implement:

```python
def normalize_messages(messages: list[dict]) -> list[dict]:
    ...
```

## Contract

Treat `system` and `developer` as instruction-bearing roles.

Return a **new** list of messages suitable for strict backends:

- Merge **all** instruction-bearing messages from the conversation into a single leading message.
- The merged instruction message must use role `system`.
- Concatenate merged instruction contents with `\n\n`.
- Preserve the original order of all non-instruction messages.
- If any merged instruction message has `cache_hint=True`, preserve `cache_hint=True` on the final leading system message.
- Do not mutate the input list or its dictionaries.

## Visible Check

Run:

```bash
python3 visible_check.py
```
