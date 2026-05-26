from __future__ import annotations

import argparse
import json
from pathlib import Path

from microbench12.grader import grade_workspace, load_telemetry
from microbench12.scoring import collect_result_paths, load_results, summarize_results
from microbench12.tasks import list_task_ids, load_task, materialize_task
from microbench12.types import AttemptMetadata


def _cmd_list(_: argparse.Namespace) -> int:
    for task_id in list_task_ids():
        task = load_task(task_id)
        print(
            f"{task.id}\t{task.difficulty}\t{task.family}\t{task.task_type}\t{task.title}"
        )
    return 0


def _cmd_describe(args: argparse.Namespace) -> int:
    task = load_task(args.task)
    print(json.dumps(task.__dict__, indent=2, sort_keys=True))
    return 0


def _cmd_materialize(args: argparse.Namespace) -> int:
    out_dir = Path(args.out).resolve()
    materialize_task(args.task, out_dir, force=args.force)
    print(out_dir)
    return 0


def _cmd_grade(args: argparse.Namespace) -> int:
    telemetry = load_telemetry(Path(args.telemetry).resolve()) if args.telemetry else None
    metadata = AttemptMetadata(
        task_id=args.task,
        model=args.model,
        harness=args.harness,
        repeat=args.repeat,
        variant=args.variant,
        backend=args.backend,
        reasoning_mode=args.reasoning_mode,
        notes=args.notes,
    )
    payload = grade_workspace(
        task_id=args.task,
        workspace=Path(args.workspace).resolve(),
        metadata=metadata,
        telemetry=telemetry,
    )
    output_path = Path(args.out).resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(output_path)
    return 0


def _cmd_score(args: argparse.Namespace) -> int:
    result_paths = collect_result_paths(Path(args.results_dir).resolve())
    summary = summarize_results(load_results(result_paths))
    out_path = Path(args.out).resolve()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(out_path)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="mb12", description="MicroBench-12 CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    list_parser = subparsers.add_parser("list", help="List benchmark tasks")
    list_parser.set_defaults(func=_cmd_list)

    describe_parser = subparsers.add_parser("describe", help="Describe one task")
    describe_parser.add_argument("--task", required=True)
    describe_parser.set_defaults(func=_cmd_describe)

    materialize_parser = subparsers.add_parser("materialize", help="Materialize one task")
    materialize_parser.add_argument("--task", required=True)
    materialize_parser.add_argument("--out", required=True)
    materialize_parser.add_argument("--force", action="store_true")
    materialize_parser.set_defaults(func=_cmd_materialize)

    grade_parser = subparsers.add_parser("grade", help="Grade one completed workspace")
    grade_parser.add_argument("--task", required=True)
    grade_parser.add_argument("--workspace", required=True)
    grade_parser.add_argument("--model", required=True)
    grade_parser.add_argument("--harness", required=True)
    grade_parser.add_argument("--repeat", type=int, required=True)
    grade_parser.add_argument("--out", required=True)
    grade_parser.add_argument("--variant")
    grade_parser.add_argument("--backend")
    grade_parser.add_argument("--reasoning-mode")
    grade_parser.add_argument("--notes")
    grade_parser.add_argument("--telemetry")
    grade_parser.set_defaults(func=_cmd_grade)

    score_parser = subparsers.add_parser("score", help="Aggregate many graded attempts")
    score_parser.add_argument("--results-dir", required=True)
    score_parser.add_argument("--out", required=True)
    score_parser.set_defaults(func=_cmd_score)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)
