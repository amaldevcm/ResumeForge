# Retrieval Evaluation Report

Generated: 2026-08-21T17:44:52.009052+00:00
Test cases evaluated: 3
Resume versions: 3
top_k requested: 3 (clamped to min(top_k, 3) per case)

## Disclosure

This test set is self-labeled by one user against their own resume versions. Results measure this specific retrieval approach on this specific person's data, and are not blindly generalizable to other users, resume corpora, or job markets.

## Retrieval quality

| Method | Hit@1 | Precision@k | Recall@k | MRR |
|---|---|---|---|---|
| embedding | 100.0% | 44.4% | 100.0% | 1.000 |
| tfidf | 100.0% | 44.4% | 100.0% | 1.000 |

## Latency (local computation only)

Measures embedding/vectorization + scoring time on this machine only - excludes the Pinecone network round-trip, Postgres hydration, and Supabase signed-URL generation the live app also pays for. Full production latency/cost instrumentation is a later phase.

Model load time: 3775.2 ms (one-time)

| Method | Embed p50 (ms) | Embed p95 (ms) | Score p50 (ms) | Score p95 (ms) |
|---|---|---|---|---|
| embedding | 33.32 | 33.72 | 1.06 | 1.76 |
| tfidf | 0.47 | 0.58 | 0.66 | 0.84 |

## Failure analysis

| Method | wrong_top1 | correct_missing_from_topk | close_score_ambiguous |
|---|---|---|---|
| embedding | 0 | 0 | 0 |
| tfidf | 0 | 0 | 0 |

## How to read this

- **Hit@1**: the top-ranked resume was one of the labeled correct resumes.
- **Precision@k / Recall@k**: k is clamped to `min(top_k, num_resumes)` so precision isn't artificially deflated when there are few resume versions - noted per-run above, not applied silently.
- **MRR**: mean reciprocal rank of the first correct resume in the ranking (1.0 = always ranked first).
- Ties are broken deterministically by resume id (lexicographic) for reproducibility - a tie-break rule, not a ranking signal.
- **wrong_top1**: a correct resume existed in the top-k but wasn't ranked first.
- **correct_missing_from_topk**: no correct resume appeared anywhere in the top-k.
- **close_score_ambiguous**: the top-1 and top-2 scores were within 0.02 of each other - a likely genuinely ambiguous JD rather than a confident wrong answer.
- **wrongness gap**: top-1 score minus the best score among the actually-correct resume(s) - how confidently wrong the miss was, not just whether it missed.

## Dataset growth

Current labeled test cases: 3. Target: 50-100 for a statistically meaningful sample.
