#!/usr/bin/env python
"""Run the offline retrieval evaluation harness.

Usage:
    python run_eval.py --example
    python run_eval.py
    python run_eval.py --testset path/to/testset.jsonl --resumes path/to/resumes.json --top-k 3

No dependency on Backend/, Flask, Pinecone, or a live Postgres connection -
see Evaluation/README.md for why.
"""
import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

EVAL_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(EVAL_ROOT))

from lib.schema import load_testset, load_resumes, validate_testset_against_resumes
from lib.retrieval import score_embedding, score_tfidf, load_model_timed
from lib.metrics import evaluate_case, aggregate, failure_counts
from lib.report import render_report


def parse_args():
    parser = argparse.ArgumentParser(description="Run the ResumeForge retrieval evaluation harness.")
    parser.add_argument("--testset", default=None,
                         help="Path to testset.jsonl (default: data/testset.jsonl, or the example set with --example)")
    parser.add_argument("--resumes", default=None,
                         help="Path to resumes.json (default: data/resumes/resumes.json, or the example set with --example)")
    parser.add_argument("--top-k", type=int, default=3, help="top_k to evaluate at (matches production default)")
    parser.add_argument("--example", action="store_true",
                         help="Run against the committed example fixtures instead of real data")
    parser.add_argument("--out-dir", default=None, help="Where to write results (default: Evaluation/results)")
    return parser.parse_args()


def resolve_paths(args):
    data_dir = EVAL_ROOT / "data"
    if args.example:
        testset_path = Path(args.testset) if args.testset else data_dir / "testset.example.jsonl"
        resumes_path = Path(args.resumes) if args.resumes else data_dir / "resumes" / "resumes.example.json"
    else:
        testset_path = Path(args.testset) if args.testset else data_dir / "testset.jsonl"
        resumes_path = Path(args.resumes) if args.resumes else data_dir / "resumes" / "resumes.json"
    out_dir = Path(args.out_dir) if args.out_dir else EVAL_ROOT / "results"
    return testset_path, resumes_path, out_dir


def run_method(score_fn, jd_texts, resume_texts, resume_ids, cases, top_k):
    scores, timings = score_fn(jd_texts, resume_texts)
    results = [
        evaluate_case(case.id, row, resume_ids, case.correct_resume_ids, top_k)
        for row, case in zip(scores, cases)
    ]
    return results, timings


def worst_n_failures(results, n=5):
    misses = [r for r in results if r.failure_type is not None]
    misses.sort(key=lambda r: -r.wrongness_gap)
    return [
        {"case_id": r.case_id, "failure_type": r.failure_type, "wrongness_gap": r.wrongness_gap}
        for r in misses[:n]
    ]


def write_failures(run_dir, method_results):
    failures_path = run_dir / "failures.jsonl"
    with open(failures_path, "w", encoding="utf-8") as f:
        for method, results in method_results.items():
            for r in results:
                if r.failure_type:
                    f.write(json.dumps({
                        "method": method,
                        "case_id": r.case_id,
                        "failure_type": r.failure_type,
                        "wrongness_gap": r.wrongness_gap,
                        "top1_score": r.ranked_scores[0] if r.ranked_scores else None,
                        "top2_score": r.ranked_scores[1] if len(r.ranked_scores) > 1 else None,
                    }) + "\n")
    return failures_path


def main():
    args = parse_args()
    testset_path, resumes_path, out_dir = resolve_paths(args)

    if not testset_path.exists():
        print(f"Test set not found: {testset_path}")
        print("Run with --example to verify the harness against the committed example fixtures,")
        print("or run scripts/export_resumes.py and label data/testset.jsonl for a real evaluation.")
        sys.exit(1)
    if not resumes_path.exists():
        print(f"Resume fixture not found: {resumes_path}")
        sys.exit(1)

    cases = load_testset(testset_path)
    resumes = load_resumes(resumes_path)
    cases, excluded_case_ids = validate_testset_against_resumes(cases, resumes)

    if not cases:
        print("No valid test cases remain after validation - nothing to evaluate.")
        sys.exit(1)

    resume_ids = [r.id for r in resumes]
    resume_texts = [r.resume_text for r in resumes]
    jd_texts = [c.jd_text for c in cases]

    model_load_s = load_model_timed()

    method_results = {}
    method_timings = {}
    for method_name, score_fn in [("embedding", score_embedding), ("tfidf", score_tfidf)]:
        results, timings = run_method(score_fn, jd_texts, resume_texts, resume_ids, cases, args.top_k)
        method_results[method_name] = results
        method_timings[method_name] = timings

    method_aggregates = {m: aggregate(r) for m, r in method_results.items()}
    method_failure_counts = {m: failure_counts(r) for m, r in method_results.items()}
    worst_failures_by_method = {m: worst_n_failures(r) for m, r in method_results.items()}

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    run_dir = out_dir / "runs" / timestamp
    run_dir.mkdir(parents=True, exist_ok=True)

    write_failures(run_dir, method_results)

    report_md = render_report(
        n_cases=len(cases),
        n_resumes=len(resumes),
        top_k=args.top_k,
        excluded_case_ids=excluded_case_ids,
        method_aggregates=method_aggregates,
        method_failure_counts=method_failure_counts,
        method_timings=method_timings,
        model_load_s=model_load_s,
        worst_failures_by_method=worst_failures_by_method,
    )

    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "latest_report.md").write_text(report_md, encoding="utf-8")
    (run_dir / "report.md").write_text(report_md, encoding="utf-8")

    print(f"Evaluated {len(cases)} test case(s) against {len(resumes)} resume(s).")
    print(f"Report written to {out_dir / 'latest_report.md'}")
    print(f"Run archive: {run_dir}")


if __name__ == "__main__":
    main()
