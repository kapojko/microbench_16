from __future__ import annotations


def logit_lens_topk(hidden_states, ln_weight, ln_bias, lm_head, k):
    """Return top-k token ids per layer.

    This starter is intentionally wrong:
    - it uses the first token instead of the final token
    - it skips layer normalization
    - it does not define deterministic tie-breaking explicitly
    """

    results = []
    for layer_states in hidden_states:
        token = layer_states[0]
        scored = []
        for token_id, row in enumerate(lm_head):
            logit = sum(value * weight for value, weight in zip(token, row))
            scored.append((logit, token_id))
        scored.sort(reverse=True)
        results.append([token_id for _, token_id in scored[:k]])
    return results
