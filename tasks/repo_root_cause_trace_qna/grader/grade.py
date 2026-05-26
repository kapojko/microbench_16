from __future__ import annotations

import re
from pathlib import Path


def _contains_all(text: str, needles: list[str]) -> bool:
    return all(needle in text for needle in needles)


def _has_fix_direction(text: str) -> bool:
    if "last_seen_at" not in text:
        return False
    if (
        "use last_seen_at" in text
        or "switch the cleanup check" in text
        or "change cleanup to use last_seen_at" in text
        or "change cleanup" in text
        or "cleanup freshness" in text
    ):
        return True
    return bool(
        re.search(
            r"\b(change|switch|replace|base|compute|calculate)\b"
            r"[\s\S]{0,120}\bissued_at\b[\s\S]{0,120}\blast_seen_at\b",
            text,
        )
    )


def grade_workspace(workspace_path: Path, task) -> dict:
    answer_path = workspace_path / "answer.md"
    answer = answer_path.read_text(encoding="utf-8").lower()
    normalized_answer = answer.replace("`", "")
    checks = []

    checks.append(
        {
            "name": "cleanup_path_identified",
            "passed": ("session_cleanup.py" in answer)
            or ("drop_expired_pending_sessions" in answer),
            "expected": "Mention the cleanup path in app/jobs/session_cleanup.py.",
            "actual": answer,
        }
    )
    checks.append(
        {
            "name": "timestamp_field_mismatch",
            "passed": _contains_all(answer, ["issued_at", "last_seen_at"]),
            "expected": "Explain that cleanup uses issued_at when it should use last_seen_at.",
            "actual": answer,
        }
    )
    checks.append(
        {
            "name": "restart_fallback_identified",
            "passed": (
                ("resume_or_restart" in answer or "onboarding.py" in answer)
                and ("welcome" in answer or "restart" in answer)
            ),
            "expected": "Explain the fallback path that restarts onboarding at welcome when the session is missing.",
            "actual": answer,
        }
    )
    checks.append(
        {
            "name": "fix_outline_present",
            "passed": _has_fix_direction(normalized_answer),
            "expected": "Provide a minimal fix outline that changes cleanup semantics.",
            "actual": answer,
        }
    )

    score = sum(1.0 for item in checks if item["passed"]) / len(checks)
    passed = all(item["passed"] for item in checks)
    return {
        "score": score,
        "passed": passed,
        "checks": checks,
        "summary": "Repository QnA graded with a four-item deterministic rubric.",
    }
