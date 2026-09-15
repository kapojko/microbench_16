#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DIFFICULTY_ORDER = {"easy": 0, "medium": 1, "hard": 2}

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from microbench12.scoring import collect_result_paths, load_results, summarize_results  # noqa: E402
from microbench12.tasks import list_task_ids, load_task  # noqa: E402


def _utc_stamp() -> str:
    return time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime())


def _fmt(value: Any, digits: int = 3) -> str:
    if value is None:
        return "—"
    return f"{float(value):.{digits}f}"


def _cell(value: Any) -> str:
    return str(value).replace("|", "\\|")


def _md_table(headers: list[str], rows: list[list[Any]]) -> list[str]:
    lines = [
        "| " + " | ".join(_cell(header) for header in headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(_cell(cell) for cell in row) + " |")
    return lines


def _load_task_meta() -> dict[str, dict[str, str]]:
    meta: dict[str, dict[str, str]] = {}
    try:
        task_ids = list_task_ids()
    except (OSError, ValueError, KeyError):
        return meta
    for task_id in task_ids:
        try:
            task = load_task(task_id)
        except (OSError, ValueError, KeyError):
            continue
        meta[task.id] = {
            "title": task.title,
            "family": task.family,
            "difficulty": task.difficulty,
        }
    return meta


def _sort_difficulties(values: set[str]) -> list[str]:
    return sorted(values, key=lambda value: (DIFFICULTY_ORDER.get(value, 99), value))


def _task_label(task_id: str, meta: dict[str, str] | None) -> str:
    if meta:
        return f"{task_id} — {meta['title']} ({meta['family']}, {meta['difficulty']})"
    return task_id


def _build_report(
    *,
    title: str,
    results_dir: str,
    summary: dict[str, Any],
    task_meta: dict[str, dict[str, str]],
) -> str:
    variants = sorted(
        summary["variants"],
        key=lambda item: (-float(item["overall_mean_score"]), str(item["variant"])),
    )
    variant_names = [str(item["variant"]) for item in variants]
    manifest_order = {task_id: index for index, task_id in enumerate(task_meta)}
    all_task_ids = sorted(
        {task_id for item in variants for task_id in item["per_task"]},
        key=lambda task_id: (manifest_order.get(task_id, len(manifest_order)), task_id),
    )
    difficulties = _sort_difficulties(
        {key for item in variants for key in item["difficulty_means"]}
    )
    families = sorted({key for item in variants for key in item["family_means"]})
    attempt_count = sum(item["attempt_count"] for item in variants)

    leader_headers = [
        "Rank",
        "Variant",
        "Attempts",
        "Overall",
        *difficulties,
        "Wall time (s)",
        "Tokens",
    ]
    leader_rows = []
    for rank, item in enumerate(variants, start=1):
        telemetry = item["telemetry_means"]
        row = [
            rank,
            item["variant"],
            item["attempt_count"],
            _fmt(item["overall_mean_score"]),
        ]
        row.extend(_fmt(item["difficulty_means"].get(difficulty)) for difficulty in difficulties)
        row.append(_fmt(telemetry.get("wall_time_sec"), 1))
        row.append(_fmt(telemetry.get("total_tokens"), 0))
        leader_rows.append(row)

    task_headers = ["Task", *variant_names]
    task_rows = []
    for task_id in all_task_ids:
        row = [_task_label(task_id, task_meta.get(task_id))]
        for item in variants:
            entry = item["per_task"].get(task_id)
            if entry is None:
                row.append("—")
            elif entry["repeats"] > 1:
                row.append(f"{entry['mean_score']:.3f} ± {entry['stdev']:.3f}")
            else:
                row.append(f"{entry['mean_score']:.3f}")
        task_rows.append(row)

    family_headers = ["Family", *variant_names]
    family_rows = [
        [family, *(_fmt(item["family_means"].get(family)) for item in variants)]
        for family in families
    ]

    lines: list[str] = [
        f"# {title}",
        "",
        f"_Generated: {_utc_stamp()} · Results: `{results_dir}`_",
        "",
        f"- Variants: {len(variants)}",
        f"- Graded attempts: {attempt_count}",
        f"- Tasks covered: {len(all_task_ids)}",
        "",
        "## Leaderboard",
        "",
        *_md_table(leader_headers, leader_rows),
        "",
        "## Per-task scores",
        "",
        "Mean score per task and variant; `mean ± stdev` when a task has repeats, `—` when a variant has no attempts for that task.",
        "",
        *_md_table(task_headers, task_rows),
        "",
        "## Family means",
        "",
        *_md_table(family_headers, family_rows),
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate a markdown report from MicroBench-12 grade result JSON files."
    )
    parser.add_argument(
        "--results-dir",
        default=str(PROJECT_ROOT / "results"),
        help="Directory scanned recursively for grade result JSON files.",
    )
    parser.add_argument(
        "--out",
        default=str(PROJECT_ROOT / "results" / "report.md"),
        help="Path of the markdown report to write.",
    )
    parser.add_argument(
        "--title",
        default="MicroBench-12 Report",
        help="Report title.",
    )
    args = parser.parse_args()

    results_dir = Path(args.results_dir).resolve()
    if not results_dir.is_dir():
        print(f"error: results directory not found: {args.results_dir}", file=sys.stderr)
        return 1

    results = load_results(collect_result_paths(results_dir))
    if not results:
        print(f"error: no graded results found under {results_dir}", file=sys.stderr)
        return 1

    summary = summarize_results(results)
    report = _build_report(
        title=args.title,
        results_dir=str(Path(args.results_dir)),
        summary=summary,
        task_meta=_load_task_meta(),
    )

    out_path = Path(args.out).resolve()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(report, encoding="utf-8")
    print(out_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
