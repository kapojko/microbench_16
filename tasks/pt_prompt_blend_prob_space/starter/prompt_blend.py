from __future__ import annotations

import math


def blend_branch_log_probs(branch_log_probs, weights):
    """Blend branch predictions and return log-probabilities.

    BUG: this starter averages log-probabilities directly instead of blending
    in probability space.
    """

    if not branch_log_probs:
        return []
    total_weight = sum(weights)
    normalized = [weight / total_weight for weight in weights]
    vocab_size = len(branch_log_probs[0])
    blended = []
    for token_index in range(vocab_size):
        value = 0.0
        for branch_index, branch in enumerate(branch_log_probs):
            value += normalized[branch_index] * branch[token_index]
        blended.append(value)
    return blended
