"""Render eval harness results into a human-readable markdown report."""
from datetime import datetime, timezone


def _pct(x):
    return f"{x * 100:.1f}%"


def _latency_stats(values_ms):
    if not values_ms:
        return {"median": 0.0, "p95": 0.0}
    sorted_vals = sorted(values_ms)
    n = len(sorted_vals)
    median = sorted_vals[n // 2]
    p95_idx = min(n - 1, int(round(0.95 * (n - 1))))
    p95 = sorted_vals[p95_idx]
    return {"median": median, "p95": p95}


def render_report(*, n_cases, n_resumes, top_k, excluded_case_ids,
                   method_aggregates, method_failure_counts, method_timings,
                   model_load_s, worst_failures_by_method):
    total_cases = n_cases + len(excluded_case_ids)
    lines = []
    lines.append("# Retrieval Evaluation Report")
    lines.append("")
    lines.append(f"Generated: {datetime.now(timezone.utc).isoformat()}")
    lines.append(
        f"Test cases evaluated: {n_cases}"
        + (f" ({len(excluded_case_ids)} excluded, see below)" if excluded_case_ids else "")
    )
    lines.append(f"Resume versions: {n_resumes}")
    lines.append(f"top_k requested: {top_k} (clamped to min(top_k, {n_resumes}) per case)")
    lines.append("")

    lines.append("## Disclosure")
    lines.append("")
    lines.append(
        "This test set is self-labeled by one user against their own resume versions. "
        "Results measure this specific retrieval approach on this specific person's data, "
        "and are not blindly generalizable to other users, resume corpora, or job markets."
    )
    lines.append("")

    if excluded_case_ids:
        lines.append("## Data integrity warning")
        lines.append("")
        lines.append(
            f"{len(excluded_case_ids)} test case(s) referenced a `correct_resume_id` not present "
            "in the resume fixture and were excluded from scoring rather than silently counted "
            "as failures: " + ", ".join(excluded_case_ids)
        )
        lines.append("")

    lines.append("## Retrieval quality")
    lines.append("")
    lines.append("| Method | Hit@1 | Precision@k | Recall@k | MRR |")
    lines.append("|---|---|---|---|---|")
    for method, agg in method_aggregates.items():
        lines.append(
            f"| {method} | {_pct(agg['hit_at_1'])} | {_pct(agg['precision_at_k'])} "
            f"| {_pct(agg['recall_at_k'])} | {agg['mrr']:.3f} |"
        )
    lines.append("")

    lines.append("## Latency (local computation only)")
    lines.append("")
    lines.append(
        "Measures embedding/vectorization + scoring time on this machine only - excludes "
        "the Pinecone network round-trip, Postgres hydration, and Supabase signed-URL "
        "generation the live app also pays for. Full production latency/cost instrumentation "
        "is a later phase."
    )
    lines.append("")
    lines.append(f"Model load time: {model_load_s * 1000:.1f} ms (one-time)")
    lines.append("")
    lines.append("| Method | Embed p50 (ms) | Embed p95 (ms) | Score p50 (ms) | Score p95 (ms) |")
    lines.append("|---|---|---|---|---|")
    for method, timings in method_timings.items():
        e = _latency_stats(timings["embed_query_ms"])
        s = _latency_stats(timings["score_ms"])
        lines.append(
            f"| {method} | {e['median']:.2f} | {e['p95']:.2f} | {s['median']:.2f} | {s['p95']:.2f} |"
        )
    lines.append("")

    lines.append("## Failure analysis")
    lines.append("")
    lines.append("| Method | wrong_top1 | correct_missing_from_topk | close_score_ambiguous |")
    lines.append("|---|---|---|---|")
    for method, counts in method_failure_counts.items():
        lines.append(
            f"| {method} | {counts.get('wrong_top1', 0)} | {counts.get('correct_missing_from_topk', 0)} "
            f"| {counts.get('close_score_ambiguous', 0)} |"
        )
    lines.append("")

    for method, worst in worst_failures_by_method.items():
        if not worst:
            continue
        lines.append(f"**Worst misses - {method}** (largest wrongness gap first):")
        lines.append("")
        for w in worst:
            lines.append(f"- `{w['case_id']}`: {w['failure_type']}, wrongness gap {w['wrongness_gap']:.3f}")
        lines.append("")

    lines.append("## How to read this")
    lines.append("")
    lines.append("- **Hit@1**: the top-ranked resume was one of the labeled correct resumes.")
    lines.append(
        "- **Precision@k / Recall@k**: k is clamped to `min(top_k, num_resumes)` so precision "
        "isn't artificially deflated when there are few resume versions - noted per-run above, "
        "not applied silently."
    )
    lines.append(
        "- **MRR**: mean reciprocal rank of the first correct resume in the ranking "
        "(1.0 = always ranked first)."
    )
    lines.append(
        "- Ties are broken deterministically by resume id (lexicographic) for reproducibility - "
        "a tie-break rule, not a ranking signal."
    )
    lines.append("- **wrong_top1**: a correct resume existed in the top-k but wasn't ranked first.")
    lines.append("- **correct_missing_from_topk**: no correct resume appeared anywhere in the top-k.")
    lines.append(
        "- **close_score_ambiguous**: the top-1 and top-2 scores were within 0.02 of each other - "
        "a likely genuinely ambiguous JD rather than a confident wrong answer."
    )
    lines.append(
        "- **wrongness gap**: top-1 score minus the best score among the actually-correct "
        "resume(s) - how confidently wrong the miss was, not just whether it missed."
    )
    lines.append("")

    lines.append("## Dataset growth")
    lines.append("")
    lines.append(f"Current labeled test cases: {total_cases}. Target: 50-100 for a statistically meaningful sample.")
    lines.append("")

    return "\n".join(lines)
