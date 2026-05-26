from __future__ import annotations

import math

from logit_lens import logit_lens_topk


def _reference(hidden_states, ln_weight, ln_bias, lm_head, k):
    def normalize(vector):
        mean = sum(vector) / len(vector)
        var = sum((value - mean) ** 2 for value in vector) / len(vector)
        scale = math.sqrt(var + 1e-5)
        return [
            ((value - mean) / scale) * weight + bias
            for value, weight, bias in zip(vector, ln_weight, ln_bias)
        ]

    output = []
    for layer_states in hidden_states:
        token = layer_states[-1]
        normalized = normalize(token)
        logits = []
        for token_id, row in enumerate(lm_head):
            logits.append((sum(value * weight for value, weight in zip(normalized, row)), token_id))
        logits.sort(key=lambda item: (-item[0], item[1]))
        output.append([token_id for _, token_id in logits[:k]])
    return output


def main() -> None:
    hidden_states = [
        [[1.0, 0.0, -1.0], [0.5, 1.5, -0.5]],
        [[0.0, 2.0, -1.0], [1.0, 0.0, 1.0]],
    ]
    ln_weight = [1.0, 1.0, 1.0]
    ln_bias = [0.0, 0.0, 0.0]
    lm_head = [
        [1.0, 0.0, 0.5],
        [0.0, 1.0, 0.0],
        [-0.5, 0.5, 1.0],
        [0.5, -1.0, 0.0],
    ]
    expected = _reference(hidden_states, ln_weight, ln_bias, lm_head, 2)
    actual = logit_lens_topk(hidden_states, ln_weight, ln_bias, lm_head, 2)
    if actual != expected:
        raise SystemExit(f"Visible check failed.\nExpected: {expected}\nActual:   {actual}")
    print("visible_check: ok")


if __name__ == "__main__":
    main()
