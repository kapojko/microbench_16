from __future__ import annotations


def argmax(values):
    best_index = 0
    best_value = values[0]
    for index, value in enumerate(values[1:], start=1):
        if value > best_value:
            best_index = index
            best_value = value
    return best_index


class ToyDecoder:
    def __init__(self, embedding_table, output_matrix, output_bias):
        self.embedding_table = embedding_table
        self.output_matrix = output_matrix
        self.output_bias = output_bias
        self.embedding_visits = 0

    @classmethod
    def demo(cls):
        return cls(
            embedding_table=[
                [1.0, 0.0, 0.0],
                [0.0, 1.0, 0.0],
                [0.0, 0.0, 1.0],
                [1.0, 1.0, 0.0],
                [0.0, 1.0, 1.0],
            ],
            output_matrix=[
                [0.1, 0.2, 0.3],
                [0.4, 0.1, 0.0],
                [0.0, 0.5, 0.2],
                [0.3, 0.3, 0.3],
                [0.2, 0.0, 0.6],
            ],
            output_bias=[0.0, 0.0, 0.0, 0.1, -0.1],
        )

    def reset_counters(self):
        self.embedding_visits = 0

    def _embed(self, token_id):
        self.embedding_visits += 1
        return self.embedding_table[token_id]

    def _advance(self, token_id, cache):
        embedding = self._embed(token_id)
        if cache is None:
            state = [0.0 for _ in embedding]
        else:
            state = list(cache["state"])
        for index, value in enumerate(embedding):
            state[index] += value
        return {"state": state, "last_token": token_id}

    def prefill(self, prompt_ids):
        cache = None
        for token_id in prompt_ids:
            cache = self._advance(token_id, cache)
        return cache

    def decode_next(self, token_id, cache):
        return self._advance(token_id, cache)

    def logits_from_cache(self, cache):
        logits = []
        for token_id, (weights, bias) in enumerate(zip(self.output_matrix, self.output_bias)):
            score = sum(weight * value for weight, value in zip(weights, cache["state"])) + bias
            if cache["last_token"] == token_id:
                score += 0.05
            logits.append(score)
        return logits


def generate_reference(model, prompt_ids, max_new_tokens):
    context = list(prompt_ids)
    generated = []
    for _ in range(max_new_tokens):
        cache = model.prefill(context)
        logits = model.logits_from_cache(cache)
        next_token = argmax(logits)
        generated.append(next_token)
        context.append(next_token)
    return generated


def generate_cached(model, prompt_ids, max_new_tokens):
    """Return only the newly generated token ids.

    BUG: this starter recomputes the entire prefix every step instead of
    carrying cache state forward.
    """

    context = list(prompt_ids)
    generated = []
    for _ in range(max_new_tokens):
        cache = model.prefill(context)
        logits = model.logits_from_cache(cache)
        next_token = argmax(logits)
        generated.append(next_token)
        context.append(next_token)
    return generated
