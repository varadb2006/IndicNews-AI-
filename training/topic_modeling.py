

import numpy as np
from sklearn.decomposition import NMF, LatentDirichletAllocation


def build_lda_model(X_counts, n_topics=7, **kwargs):
    
    params = dict(n_components=n_topics, random_state=42, max_iter=20, learning_method="online")
    params.update(kwargs)
    model = LatentDirichletAllocation(**params)
    model.fit(X_counts)
    return model


def build_nmf_model(X_tfidf, n_topics=7, **kwargs):
    params = dict(n_components=n_topics, random_state=42, max_iter=300, init="nndsvda")
    params.update(kwargs)
    model = NMF(**params)
    model.fit(X_tfidf)
    return model


def get_top_words_per_topic(model, feature_names, n_words=10) -> dict:
    
    topics = {}
    for topic_idx, component in enumerate(model.components_):
        top_indices = component.argsort()[::-1][:n_words]
        topics[topic_idx] = [feature_names[i] for i in top_indices]
    return topics


def get_dominant_topic(model, X) -> np.ndarray:
    doc_topic = model.transform(X)
    return doc_topic.argmax(axis=1)


def topic_category_crosstab(dominant_topics, core_categories, n_topics):
    
    from collections import Counter, defaultdict

    crosstab = defaultdict(Counter)
    for topic_idx, cats in zip(dominant_topics, core_categories):
        primary_cat = cats[0] if len(cats) > 0 else "other"
        crosstab[topic_idx][primary_cat] += 1
    return {t: dict(crosstab[t]) for t in range(n_topics)}
