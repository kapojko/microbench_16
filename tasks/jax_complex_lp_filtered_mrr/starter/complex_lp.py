from __future__ import annotations


def complex_score(head_re, head_im, rel_re, rel_im, tail_re, tail_im):
    total = 0.0
    for h_re, h_im, r_re, r_im, t_re, t_im in zip(
        head_re, head_im, rel_re, rel_im, tail_re, tail_im
    ):
        total += h_re * r_re * t_re
        total += h_im * r_re * t_im
        total += h_re * r_im * t_im
        total += h_im * r_im * t_re  # BUG: the final term should be subtracted.
    return total


def filtered_mrr(
    triples,
    entity_re,
    entity_im,
    relation_re,
    relation_im,
    all_true_triples,
):
    reciprocal_ranks = []
    num_entities = len(entity_re)

    for head_id, rel_id, tail_id in triples:
        scored = []
        for candidate_tail in range(num_entities):
            if (head_id, rel_id, candidate_tail) in all_true_triples:
                continue  # BUG: this wrongly removes the target triple too.
            score = complex_score(
                entity_re[head_id],
                entity_im[head_id],
                relation_re[rel_id],
                relation_im[rel_id],
                entity_re[candidate_tail],
                entity_im[candidate_tail],
            )
            scored.append((score, candidate_tail))
        scored.sort(reverse=True)
        rank = 1
        for _, candidate_tail in scored:
            if candidate_tail == tail_id:
                break
            rank += 1
        reciprocal_ranks.append(1.0 / rank)
    return sum(reciprocal_ranks) / len(reciprocal_ranks)
