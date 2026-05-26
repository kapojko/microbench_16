from __future__ import annotations


def _copy_4d(tensor):
    return [
        [
            [list(head_values) for head_values in seq_item]
            for seq_item in batch_item
        ]
        for batch_item in tensor
    ]


def _rotate_half_split(vector, cos_row, sin_row):
    half = len(cos_row)
    first = vector[:half]
    second = vector[half : half * 2]
    rotated = []
    for index in range(half):
        rotated.append(first[index] * cos_row[index] - second[index] * sin_row[index])
    for index in range(half):
        rotated.append(first[index] * sin_row[index] + second[index] * cos_row[index])
    return rotated


def _rotate_interleaved(vector, cos_row, sin_row):
    rotated = []
    for index, (cos_value, sin_value) in enumerate(zip(cos_row, sin_row)):
        even = vector[index * 2]
        odd = vector[index * 2 + 1]
        rotated.append(even * cos_value - odd * sin_value)
        rotated.append(even * sin_value + odd * cos_value)
    return rotated


def apply_rope_gqa(q, k, cos, sin, rope_layout="half_split"):
    q_out = _copy_4d(q)
    k_out = _copy_4d(k)
    rotary_dim = len(cos[0]) * 2

    # BUG: this starter always applies half-split rotation, even for interleaved layout.
    rotate = _rotate_half_split
    if rope_layout not in {"half_split", "interleaved"}:
        raise ValueError(f"unsupported rope_layout: {rope_layout}")

    for batch_index in range(len(q_out)):
        for seq_index in range(len(q_out[batch_index])):
            for head_index in range(len(q_out[batch_index][seq_index])):
                vector = q_out[batch_index][seq_index][head_index]
                rotated = rotate(vector[:rotary_dim], cos[seq_index], sin[seq_index])
                q_out[batch_index][seq_index][head_index] = rotated + vector[rotary_dim:]

    for batch_index in range(len(k_out)):
        for seq_index in range(len(k_out[batch_index])):
            for head_index in range(len(k_out[batch_index][seq_index])):
                vector = k_out[batch_index][seq_index][head_index]
                rotated = rotate(vector[:rotary_dim], cos[seq_index], sin[seq_index])
                k_out[batch_index][seq_index][head_index] = rotated + vector[rotary_dim:]

    return q_out, k_out
