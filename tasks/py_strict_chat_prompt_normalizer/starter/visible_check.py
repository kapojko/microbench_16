from __future__ import annotations

from prompt_normalizer import normalize_messages


def main() -> None:
    original = [
        {"role": "system", "content": "Be concise."},
        {"role": "developer", "content": "Prefer bullet points.", "cache_hint": True},
        {"role": "user", "content": "Summarize the diff."},
    ]
    expected = [
        {
            "role": "system",
            "content": "Be concise.\n\nPrefer bullet points.",
            "cache_hint": True,
        },
        {"role": "user", "content": "Summarize the diff."},
    ]
    snapshot = [dict(item) for item in original]
    actual = normalize_messages(original)
    if actual != expected:
        raise SystemExit(f"Visible check failed.\nExpected: {expected}\nActual:   {actual}")
    if original != snapshot:
        raise SystemExit("Visible check failed: input messages were mutated.")
    print("visible_check: ok")


if __name__ == "__main__":
    main()
