
import numpy as np
from sklearn.metrics.pairwise import linear_kernel


def get_similar_for_corpus_article(article_index, X_corpus, top_n=5):
    
    query_vector = X_corpus[article_index]
    scores = linear_kernel(query_vector, X_corpus).ravel()
    scores[article_index] = -1  

    top_indices = scores.argsort()[::-1][:top_n]
    return [(int(i), float(scores[i])) for i in top_indices]


def get_similar_for_new_text(text, tfidf_vectorizer, X_corpus, preprocess_fn, finalize_fn=None, top_n=5):
    
    tokens = preprocess_fn(text)
    if finalize_fn is not None:
        tokens = finalize_fn(tokens)

    query_vector = tfidf_vectorizer.transform([tokens])
    scores = linear_kernel(query_vector, X_corpus).ravel()

    top_indices = scores.argsort()[::-1][:top_n]
    return [(int(i), float(scores[i])) for i in top_indices]


def format_results(results, clean_df, headline_col="Headline"):
    
    formatted = []
    for idx, score in results:
        row = clean_df.iloc[idx]
        formatted.append({
            "headline": row[headline_col],
            "similarity_percent": round(score * 100, 1),
            "categories": row["core_categories"],
        })
    return formatted
