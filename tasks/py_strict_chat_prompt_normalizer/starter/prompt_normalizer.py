from __future__ import annotations


def normalize_messages(messages: list[dict]) -> list[dict]:
    """Normalize messages for a strict backend.

    This starter is intentionally incomplete:
    - it only merges leading system messages
    - it ignores developer messages
    - it mutates the original dictionaries
    """

    if not messages:
        return []

    merged = []
    system_chunks: list[str] = []
    saw_non_system = False

    for message in messages:
        if message.get("role") == "system" and not saw_non_system:
            system_chunks.append(message.get("content", ""))
            continue
        saw_non_system = True
        merged.append(message)

    if system_chunks:
        merged.insert(0, {"role": "system", "content": "\n\n".join(system_chunks)})

    return merged
