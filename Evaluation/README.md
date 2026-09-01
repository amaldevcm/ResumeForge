# Retrieval Evaluation Harness

Phase 1 of evaluating ResumeForge's resume-to-job-description matching: a
ground-truth test set plus an offline harness that scores the production
embedding approach against a TF-IDF baseline, with failure analysis and
latency numbers.

## Why this exists

ResumeForge's retrieval (`Backend/Services/PineconeService.findBestResumes`)
had never been measured against ground truth — it returned Pinecone cosine
scores with no way to know if the "best match" was actually correct. This
harness fixes that for the retrieval step specifically. Faithfulness
evaluation of the LLM-generated resume customization/cover letter
(`Backend/Prompts/customResume.py`), full production latency/cost
instrumentation, and a CI regression gate are later phases, not covered here.

## Why it doesn't call the production code directly

`PineconeService.findBestResumes()` calls `get_current_user()`, which reads
Flask's request-scoped session and raises outside an active Flask request —
it can't be called from a standalone script. Rather than fake a Flask
request context, this harness reimplements the scoring (same
`sentence-transformers` model + cosine similarity) directly against locally
exported resume text. That also means it scores *every* resume per query
(not just Pinecone's `top_k`), which is required for recall@k and for
catching "the correct resume never surfaces at all" failures. It has zero
dependency on Flask, Pinecone, or a live Postgres connection — which is
also what will make a future CI gate cheap to add.

Note: local brute-force cosine similarity and Pinecone's ANN cosine aren't
guaranteed bit-identical (floating point, approximate nearest-neighbor vs.
exact) — at 4-6 resume vectors this is a non-issue (brute-force here is
exact), but it's worth being precise about rather than implying this is a
perfect mirror of the live index.

## Setup

No separate dependencies — this reuses `Backend/.venv` (`sentence-transformers`
and `scikit-learn` are already pinned in `Backend/requirements.txt`).

```bash
cd Backend
.venv\Scripts\activate   # Windows; source .venv/bin/activate on macOS/Linux
```

## Quick start (verify the harness works, no real data needed)

```bash
python ../Evaluation/scripts/run_eval.py --example
```

This runs against the committed example fixtures (`data/testset.example.jsonl`,
`data/resumes/resumes.example.json` — clearly fake, `[EXAMPLE]`-prefixed
data) and writes `Evaluation/results/latest_report.md`.

## Building a real evaluation

1. **Export your real resume fixture** (run where your `Backend/.env` DB is reachable):
   ```bash
   python ../Evaluation/scripts/export_resumes.py --user-id <your-user-id> --out ../Evaluation/data/resumes/resumes.json
   ```
2. **Label real job descriptions.** Create `Evaluation/data/testset.jsonl`
   (gitignored — this is your personal data) with one JSON object per line:
   ```json
   {"id": "jd-0001", "job_title": "...", "company": "...", "jd_text": "...", "correct_resume_ids": ["<resume id from resumes.json>"], "notes": "", "labeled_date": "2026-08-21"}
   ```
   `correct_resume_ids` is always a list — a job description can reasonably
   fit more than one resume version. See `data/testset.example.jsonl` for
   the full format, including a multi-label example.
3. **Run the eval:**
   ```bash
   python ../Evaluation/scripts/run_eval.py
   ```
4. Read `Evaluation/results/latest_report.md`. Keep labeling toward 50-100
   entries for a statistically meaningful sample — the harness works
   correctly at any size in the meantime.

## What's measured

- **Hit@1, Precision@k, Recall@k, MRR** for two methods: `embedding`
  (production's approach) and `tfidf` (a lexical baseline, via
  `scikit-learn`'s `TfidfVectorizer`) — this is the baseline-vs-alternative
  comparison a "real" RAG project needs, not just one untested method.
  `k` is `min(top_k, num_resumes)`.
- **Failure analysis**: every miss classified as `wrong_top1`,
  `correct_missing_from_topk`, or `close_score_ambiguous` (top-1/top-2
  scores within 0.02), plus a "wrongness gap" (how confidently wrong the
  miss was).
- **Latency**: local embed/vectorize + score time per query, mean/median/p95
  — local computation only, excludes the network/DB calls the live app
  also pays for.

## Privacy

Raw personal data (`data/testset.jsonl`, `data/resumes/resumes.json`, and
per-run `results/runs/*/failures.jsonl`) is gitignored. Only
`results/latest_report.md` is committed, and it references test cases by
`id` only — never raw job description text, job title, company name, or
resume text (company name would reveal which employers you applied to).
