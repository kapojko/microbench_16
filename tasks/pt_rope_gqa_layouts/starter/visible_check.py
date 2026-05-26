from rope_gqa import apply_rope_gqa


def main() -> None:
    q = [[[[1.0, 2.0, 3.0, 4.0]]]]
    k = [[[[5.0, 6.0, 7.0, 8.0]]]]
    cos = [[0.0, 1.0]]
    sin = [[1.0, 0.0]]
    q_half, k_half = apply_rope_gqa(q, k, cos, sin, rope_layout="half_split")
    expected_q_half = [[[[ -3.0, 2.0, 1.0, 4.0 ]]]]
    expected_k_half = [[[[ -7.0, 6.0, 5.0, 8.0 ]]]]
    if q_half != expected_q_half or k_half != expected_k_half:
        raise SystemExit(
            f"Visible check failed.\nExpected q={expected_q_half}, k={expected_k_half}\nActual q={q_half}, k={k_half}"
        )

    q_interleaved, k_interleaved = apply_rope_gqa(q, k, cos, sin, rope_layout="interleaved")
    expected_q_interleaved = [[[[ -2.0, 1.0, 3.0, 4.0 ]]]]
    expected_k_interleaved = [[[[ -6.0, 5.0, 7.0, 8.0 ]]]]
    if q_interleaved != expected_q_interleaved or k_interleaved != expected_k_interleaved:
        raise SystemExit(
            "Visible check failed on interleaved layout.\n"
            f"Expected q={expected_q_interleaved}, k={expected_k_interleaved}\n"
            f"Actual q={q_interleaved}, k={k_interleaved}"
        )
    print("visible_check: ok")


if __name__ == "__main__":
    main()
