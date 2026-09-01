"""Retrieval quality metrics: Hit@1, Precision@k, Recall@k, MRR, and
failure classification. Operates on a full [n_jds x n_resumes] score matrix
so recall@k and "correct resume never surfaces" failures can be measured
even when k is smaller than the resume count.
"""
from dataclasses import dataclass

CLOSE_SCORE_EPSILON = 0.02


@dataclass
class QueryResult:
    case_id: str
    ranked_resume_ids: list
    ranked_scores: list
    correct_resume_ids: list
    hit_at_1: int
    precision_at_k: float
    recall_at_k: float
    reciprocal_rank: float
    failure_type: str = None  # None if hit, else wrong_top1 | correct_missing_from_topk | close_score_ambiguous
    wrongness_gap: float = 0.0  # top1 score minus the best score among correct resumes; only set on a miss


def rank_resumes(scores_row, resume_ids):
    """Sort resume_ids by score descending; ties broken by resume id
    (lexicographic) for a deterministic, reproducible ranking. This is a
    tie-break rule for reproducibility, not a ranking signal."""
    order = sorted(
        range(len(resume_ids)),
        key=lambda i: (-scores_row[i], resume_ids[i]),
    )
    return [resume_ids[i] for i in order], [float(scores_row[i]) for i in order]


def classify_failure(ranked_resume_ids, ranked_scores, correct_set, k):
    top1 = ranked_resume_ids[0]
    if top1 in correct_set:
        return None

    if not any(rid in correct_set for rid in ranked_resume_ids[:k]):
        return "correct_missing_from_topk"

    if len(ranked_scores) > 1 and (ranked_scores[0] - ranked_scores[1]) <= CLOSE_SCORE_EPSILON:
        return "close_score_ambiguous"

    return "wrong_top1"


def evaluate_case(case_id, scores_row, resume_ids, correct_resume_ids, top_k):
    k = min(top_k, len(resume_ids))
    ranked_resume_ids, ranked_scores = rank_resumes(scores_row, resume_ids)
    correct_set = set(correct_resume_ids)

    hit_at_1 = 1 if ranked_resume_ids[0] in correct_set else 0

    top_k_ids = set(ranked_resume_ids[:k])
    precision_at_k = len(top_k_ids & correct_set) / k if k else 0.0
    recall_at_k = len(top_k_ids & correct_set) / len(correct_set) if correct_set else 0.0

    reciprocal_rank = 0.0
    for rank, rid in enumerate(ranked_resume_ids, start=1):
        if rid in correct_set:
            reciprocal_rank = 1.0 / rank
            break

    failure_type = classify_failure(ranked_resume_ids, ranked_scores, correct_set, k)

    wrongness_gap = 0.0
    if failure_type is not None:
        correct_scores = [s for rid, s in zip(ranked_resume_ids, ranked_scores) if rid in correct_set]
        best_correct_score = max(correct_scores) if correct_scores else min(ranked_scores)
        wrongness_gap = ranked_scores[0] - best_correct_score

    return QueryResult(
        case_id=case_id,
        ranked_resume_ids=ranked_resume_ids,
        ranked_scores=ranked_scores,
        correct_resume_ids=correct_resume_ids,
        hit_at_1=hit_at_1,
        precision_at_k=precision_at_k,
        recall_at_k=recall_at_k,
        reciprocal_rank=reciprocal_rank,
        failure_type=failure_type,
        wrongness_gap=wrongness_gap,
    )


def aggregate(results):
    """Average metrics across all query results for one method."""
    n = len(results)
    if n == 0:
        return {"hit_at_1": 0.0, "precision_at_k": 0.0, "recall_at_k": 0.0, "mrr": 0.0, "n": 0}

    return {
        "hit_at_1": sum(r.hit_at_1 for r in results) / n,
        "precision_at_k": sum(r.precision_at_k for r in results) / n,
        "recall_at_k": sum(r.recall_at_k for r in results) / n,
        "mrr": sum(r.reciprocal_rank for r in results) / n,
        "n": n,
    }


def failure_counts(results):
    """Aggregate counts by failure_type - safe to commit (no ids or text)."""
    counts = {}
    for r in results:
        if r.failure_type:
            counts[r.failure_type] = counts.get(r.failure_type, 0) + 1
    return counts
