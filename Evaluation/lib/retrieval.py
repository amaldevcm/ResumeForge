"""Pure retrieval scoring: embedding cosine similarity + TF-IDF baseline.

No I/O beyond loading the embedding model, and no dependency on Backend/
or Flask - this keeps the eval harness fast, deterministic, and runnable
without a live Pinecone/Postgres connection. See Evaluation/README.md for
why this reimplements scoring instead of calling PineconeService directly.
"""
import time

import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"  # matches PineconeService.findBestResumes

_model = None


def _get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer(EMBEDDING_MODEL_NAME)
    return _model


def load_model_timed():
    """Load (or reuse the already-loaded) embedding model, returning the
    one-time load time in seconds."""
    start = time.perf_counter()
    _get_model()
    return time.perf_counter() - start


def score_embedding(jd_texts, resume_texts):
    """Cosine similarity between each JD and each resume, using the same
    embedding model as production (PineconeService.findBestResumes).

    Returns (scores, timings): scores is an [n_jds x n_resumes] array;
    timings is {"embed_query_ms": [...], "score_ms": [...]}, one entry per
    JD, for latency reporting.
    """
    model = _get_model()
    resume_vecs = model.encode(resume_texts, convert_to_numpy=True)

    scores_rows = []
    embed_times_ms = []
    score_times_ms = []
    for jd_text in jd_texts:
        t0 = time.perf_counter()
        jd_vec = model.encode(jd_text, convert_to_numpy=True)
        t1 = time.perf_counter()
        row = cosine_similarity(jd_vec.reshape(1, -1), resume_vecs)[0]
        t2 = time.perf_counter()

        embed_times_ms.append((t1 - t0) * 1000)
        score_times_ms.append((t2 - t1) * 1000)
        scores_rows.append(row)

    scores = np.array(scores_rows) if scores_rows else np.zeros((0, len(resume_texts)))
    return scores, {"embed_query_ms": embed_times_ms, "score_ms": score_times_ms}


def score_tfidf(jd_texts, resume_texts):
    """TF-IDF lexical-similarity baseline - the alternative-method
    comparison against the embedding approach above.

    Returns (scores, timings) with the same shape/contract as score_embedding.
    """
    vectorizer = TfidfVectorizer()
    resume_matrix = vectorizer.fit_transform(resume_texts)

    scores_rows = []
    embed_times_ms = []
    score_times_ms = []
    for jd_text in jd_texts:
        t0 = time.perf_counter()
        jd_vec = vectorizer.transform([jd_text])
        t1 = time.perf_counter()
        row = cosine_similarity(jd_vec, resume_matrix)[0]
        t2 = time.perf_counter()

        embed_times_ms.append((t1 - t0) * 1000)
        score_times_ms.append((t2 - t1) * 1000)
        scores_rows.append(row)

    scores = np.array(scores_rows) if scores_rows else np.zeros((0, len(resume_texts)))
    return scores, {"embed_query_ms": embed_times_ms, "score_ms": score_times_ms}
