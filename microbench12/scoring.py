from __future__ import annotations

import json
import math
from collections import defaultdict
from pathlib import Path
from typing import Any


def _mean(values: list[float]) -> float:
    return sum(values) / len(values) if values else 0.0


def _stdev(values: list[float]) -> float:
    if len(values) < 2:
        return 0.0
    mean_value = _mean(values)
    variance = sum((value - mean_value) ** 2 for value in values) / len(values)
    return math.sqrt(variance)


def load_results(paths: list[Path]) -> list[dict[str, Any]]:
    payloads: list[dict[str, Any]] = []
    for path in paths:
        with path.open("r", encoding="utf-8") as handle:
            payload = json.load(handle)
        if _is_grade_result(payload):
            payloads.append(payload)
    return payloads


def _is_grade_result(payload: Any) -> bool:
    return (
        isinstance(payload, dict)
        and isinstance(payload.get("task"), dict)
        and isinstance(payload.get("attempt"), dict)
        and isinstance(payload.get("result"), dict)
    )


def collect_result_paths(results_dir: Path) -> list[Path]:
    return sorted(path for path in results_dir.rglob("*.json") if path.is_file())


def summarize_results(results: list[dict[str, Any]]) -> dict[str, Any]:
    by_variant: dict[str, list[dict[str, Any]]] = defaultdict(list)

    for payload in results:
        attempt = payload["attempt"]
        variant = attempt.get("variant") or f'{attempt["harness"]}__{attempt["model"]}'
        by_variant[variant].append(payload)

    summary_variants: list[dict[str, Any]] = []
    for variant, payloads in sorted(by_variant.items()):
        task_scores: dict[str, list[float]] = defaultdict(list)
        family_scores: dict[str, list[float]] = defaultdict(list)
        difficulty_scores: dict[str, list[float]] = defaultdict(list)
        wall_times: list[float] = []
        token_usage: list[float] = []

        for payload in payloads:
            task_id = payload["task"]["id"]
            family = payload["task"]["family"]
            difficulty = payload["task"]["difficulty"]
            score = float(payload["result"]["score"])
            task_scores[task_id].append(score)
            family_scores[family].append(score)
            difficulty_scores[difficulty].append(score)
            telemetry = payload.get("telemetry", {})
            if "wall_time_sec" in telemetry:
                wall_times.append(float(telemetry["wall_time_sec"]))
            if "total_tokens" in telemetry:
                token_usage.append(float(telemetry["total_tokens"]))

        per_task = {
            task_id: {
                "mean_score": round(_mean(values), 6),
                "stdev": round(_stdev(values), 6),
                "repeats": len(values),
                "min_score": round(min(values), 6),
                "max_score": round(max(values), 6),
            }
            for task_id, values in sorted(task_scores.items())
        }

        summary_variants.append(
            {
                "variant": variant,
                "attempt_count": len(payloads),
                "overall_mean_score": round(
                    _mean([task["mean_score"] for task in per_task.values()]), 6
                ),
                "difficulty_means": {
                    key: round(_mean(values), 6)
                    for key, values in sorted(difficulty_scores.items())
                },
                "family_means": {
                    key: round(_mean(values), 6)
                    for key, values in sorted(family_scores.items())
                },
                "per_task": per_task,
                "telemetry_means": {
                    "wall_time_sec": round(_mean(wall_times), 6) if wall_times else None,
                    "total_tokens": round(_mean(token_usage), 6) if token_usage else None,
                },
            }
        )

    return {
        "variant_count": len(summary_variants),
        "variants": summary_variants,
    }
