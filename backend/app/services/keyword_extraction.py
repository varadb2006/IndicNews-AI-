"""
keyword_extraction.py
------------------------
Top keywords for a single piece of text (brief: "Display Top 10
keywords"), using the same fitted TF-IDF vectorizer as everything else
— no separate model needed. For one document, a word's TF-IDF weight
in its own (single-document) vector already reflects how much that
word stands out relative to the whole training corpus, which is
exactly what "keyword" should mean here.
"""


def extract_keywords(text, tfidf_vectorizer, preprocess_fn, finalize_fn, top_n=10):
    """
    Returns the top-N terms by TF-IDF weight for this specific text,
    highest first. Terms can be unigrams, bigrams, or trigrams, since
    the vectorizer was fit with ngram_range=(1, 3) — a multi-word
    keyword like "विश्व कप" is a valid, often more informative, result.
    """
    tokens = finalize_fn(preprocess_fn(text))
    vector = tfidf_vectorizer.transform([tokens])

    feature_names = tfidf_vectorizer.get_feature_names_out()
    row = vector.tocoo()

    scored = sorted(zip(row.col, row.data), key=lambda x: -x[1])[:top_n]
    return [feature_names[col] for col, _ in scored]
