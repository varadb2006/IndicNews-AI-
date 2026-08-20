def extract_keywords(text, tfidf_vectorizer, preprocess_fn, finalize_fn, top_n=10):
    tokens = finalize_fn(preprocess_fn(text))
    vector = tfidf_vectorizer.transform([tokens])

    feature_names = tfidf_vectorizer.get_feature_names_out()
    row = vector.tocoo()

    scored = sorted(zip(row.col, row.data), key=lambda x: -x[1])[:top_n]
    return [feature_names[col] for col, _ in scored]
