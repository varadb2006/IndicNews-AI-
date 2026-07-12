"""
similarity.py
--------------
Similar News Recommendation (Module 9) — TF-IDF + cosine similarity,
reusing  already-fitted vectorizer/matrix directly (no
refitting). Two entry points:

  - `get_similar_for_corpus_article()` — "find articles like row i" for
    exploring the training corpus (notebook demo, potential "you might
    also like" feature browsing existing articles).
  - `get_similar_for_new_text()` — the one  `/analyze`
    endpoint actually needs: arbitrary new user text in, top-5 most
    similar EXISTING corpus articles out. Mirrors
    `classification.predict_categories()`'s pattern (same preprocess ->
    finalize_tokens -> transform pipeline), so training-time and
    serving-time logic can't drift apart here either.

IMPLEMENTATION NOTE — linear_kernel, not cosine_similarity:
    scikit-learn's `TfidfVectorizer` L2-normalizes every vector by
    default (`norm="l2"`). For already-L2-normalized vectors, cosine
    similarity IS the dot product — `cosine_similarity()` computes that
    same dot product but re-derives/re-checks norms it doesn't need to.
    `linear_kernel()` skips that redundant work. Since saved
    vectorizer uses the default norm, `linear_kernel` here gives
    identical results to `cosine_similarity` for less computation —
    worth using at this matrix size (34,826 x 60,359).
"""

import numpy as np
from sklearn.metrics.pairwise import linear_kernel


def get_similar_for_corpus_article(article_index, X_corpus, top_n=5):
    """
    Find the top-N most similar articles to an existing corpus row,
    using its already-computed TF-IDF vector directly (no
    preprocessing/transform needed — it's already in X_corpus).

    Returns a list of (index, similarity_score) tuples, EXCLUDING the
    query article itself, sorted by similarity descending.
    """
    query_vector = X_corpus[article_index]
    scores = linear_kernel(query_vector, X_corpus).ravel()
    scores[article_index] = -1  

    top_indices = scores.argsort()[::-1][:top_n]
    return [(int(i), float(scores[i])) for i in top_indices]


def get_similar_for_new_text(text, tfidf_vectorizer, X_corpus, preprocess_fn, finalize_fn=None, top_n=5):
    """
    Find the top-N corpus articles most similar to arbitrary new text 
    the function `/analyze` endpoint calls directly.

    Args:
        text: raw Hindi headline or article string (NOT preprocessed —
            preprocess_fn handles that, matching classification.py's
            predict_categories() pattern)
        tfidf_vectorizer: Module 4's fitted vectorizer
        X_corpus: Module 4's fitted TF-IDF matrix (or any matrix built
            with the same vectorizer)
        preprocess_fn: callable(text) -> tokens,
            e.g. lambda t: preprocess_text(t)[1]
        finalize_fn: optional callable(tokens) -> tokens, e.g.
            feature_engineering.finalize_tokens_for_features — apply the
            SAME extended-stopword filtering used when X_corpus was
            built, for methodological consistency (see classification.py
            for the same design note)
        top_n: how many results to return

    Returns a list of (index, similarity_score) tuples, sorted by
    similarity descending. No self-exclusion needed here — the query
    text is new, not already a row in X_corpus.
    """
    tokens = preprocess_fn(text)
    if finalize_fn is not None:
        tokens = finalize_fn(tokens)

    query_vector = tfidf_vectorizer.transform([tokens])
    scores = linear_kernel(query_vector, X_corpus).ravel()

    top_indices = scores.argsort()[::-1][:top_n]
    return [(int(i), float(scores[i])) for i in top_indices]


def format_results(results, clean_df, headline_col="Headline"):
    """
    Turn (index, score) tuples into display-ready dicts: headline,
    similarity score (rounded %), and category — the shape Module 10's
    API response and the React "Similar News Cards" will want.
    """
    formatted = []
    for idx, score in results:
        row = clean_df.iloc[idx]
        formatted.append({
            "headline": row[headline_col],
            "similarity_percent": round(score * 100, 1),
            "categories": row["core_categories"],
        })
    return formatted
