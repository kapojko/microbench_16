from __future__ import annotations

import importlib.util
from pathlib import Path


def _load_module(workspace_path: Path):
    module_path = workspace_path / "complex_lp.py"
    spec = importlib.util.spec_from_file_location("student_complex_lp", module_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Unable to import {module_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _reference_score(head_re, head_im, rel_re, rel_im, tail_re, tail_im):
    total = 0.0
    for h_re, h_im, r_re, r_im, t_re, t_im in zip(
        head_re, head_im, rel_re, rel_im, tail_re, tail_im
    ):
        total += h_re * r_re * t_re
        total += h_im * r_re * t_im
        total += h_re * r_im * t_im
        total -= h_im * r_im * t_re
    return total


def _reference_filtered_mrr(
    triples, entity_re, entity_im, relation_re, relation_im, all_true_triples
):
    reciprocal_ranks = []
    num_entities = len(entity_re)
    for head_id, rel_id, tail_id in triples:
        scored = []
        for candidate_tail in range(num_entities):
            if candidate_tail != tail_id and (head_id, rel_id, candidate_tail) in all_true_triples:
                continue
            score = _reference_score(
                entity_re[head_id],
                entity_im[head_id],
                relation_re[rel_id],
                relation_im[rel_id],
                entity_re[candidate_tail],
                entity_im[candidate_tail],
            )
            scored.append((score, candidate_tail))
        scored.sort(key=lambda item: (-item[0], item[1]))
        for rank, (_, candidate_tail) in enumerate(scored, start=1):
            if candidate_tail == tail_id:
                reciprocal_ranks.append(1.0 / rank)
                break
    return sum(reciprocal_ranks) / len(reciprocal_ranks)


def grade_workspace(workspace_path: Path, task) -> dict:
    module = _load_module(workspace_path)
    checks = []

    checks.append(
        {
            "name": "complex_score_sign",
            "passed": abs(
                module.complex_score([1.0], [2.0], [3.0], [4.0], [5.0], [6.0]) - 35.0
            )
            <= 1e-9,
            "expected": 35.0,
            "actual": module.complex_score([1.0], [2.0], [3.0], [4.0], [5.0], [6.0]),
        }
    )

    entity_re = [[1.0, 0.0], [0.5, 1.0], [1.5, -0.5]]
    entity_im = [[0.0, 1.0], [1.0, 0.0], [0.5, 0.5]]
    relation_re = [[1.0, 0.5]]
    relation_im = [[0.25, 1.0]]
    triples = [(0, 0, 1), (0, 0, 2)]
    all_true = {(0, 0, 1), (0, 0, 2)}

    expected_mrr = _reference_filtered_mrr(
        triples, entity_re, entity_im, relation_re, relation_im, all_true
    )
    actual_mrr = module.filtered_mrr(
        triples, entity_re, entity_im, relation_re, relation_im, all_true
    )
    checks.append(
        {
            "name": "filtered_mrr_tail_prediction",
            "passed": abs(actual_mrr - expected_mrr) <= 1e-9,
            "expected": expected_mrr,
            "actual": actual_mrr,
        }
    )

    passed = all(item["passed"] for item in checks)
    return {
        "score": 1.0 if passed else 0.0,
        "passed": passed,
        "checks": checks,
        "summary": "ComplEx evaluation graded on score sign and filtered-MRR tail-ranking semantics.",
    }
