from kv_cache_generate import ToyDecoder, generate_cached


def main() -> None:
    model = ToyDecoder.demo()
    generated = generate_cached(model, [2, 1, 0], 3)
    expected = [1, 1, 1]
    if generated != expected:
        raise SystemExit(f"Visible check failed.\nExpected: {expected}\nActual:   {generated}")
    max_embedding_visits = 6
    if model.embedding_visits > max_embedding_visits:
        raise SystemExit(
            "Visible check failed.\n"
            f"Expected embedding_visits <= {max_embedding_visits}\n"
            f"Actual embedding_visits = {model.embedding_visits}"
        )
    print("visible_check: ok")


if __name__ == "__main__":
    main()
