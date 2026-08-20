"""
topic_service.py
-------------------
Dominant-topic prediction for a single piece of text, using the saved
NMF model. NMF topics are just numbered clusters of
words anf not human-readable on their own, so this also carries
hand-assigned labels for the 7 topics discovered training run.

IMPORTANT — where these labels came from, and when to double-check them:
    `TOPIC_LABELS` below was assigned by directly reading the actual
    top-10-words-per-topic output from real run (not
    guessed). `build_nmf_model()` in topic_modeling.py fixes
    `random_state=42` and `init="nndsvda"` (deterministic), so re-fitting
    NMF on the same corpus should reproduce the same 7 topics in the
    same order. BUT if the training corpus changes (more data, different
    preprocessing, a different EXTENDED_STOPWORDS_HI list) before
    `topic_model_nmf.joblib` is regenerated, topic order or content
    could shift the label mapping is by topic INDEX, not by content
    matching, so a stale mapping would silently mislabel topics rather
    than erroring. If you retrain the topic model, re-run
    07_TopicModeling.ipynb's §1-2 output and check these labels still
    match before trusting this file again.
"""

TOPIC_LABELS = {
    0: "Crime & Law and Order",
    1: "Sports (Cricket)",
    2: "Elections & Politics",
    3: "Viral & Social Media / Entertainment",
    4: "Numbers & Finance",
    5: "PM Modi / National Leadership",
    6: "Delhi Politics (Kejriwal)",
}


def predict_topic(text, tfidf_vectorizer, topic_model, feature_names, preprocess_fn, finalize_fn, top_words_n=10):
   
    tokens = finalize_fn(preprocess_fn(text))
    vector = tfidf_vectorizer.transform([tokens])

    topic_distribution = topic_model.transform(vector)[0]
    topic_id = int(topic_distribution.argmax())

    component = topic_model.components_[topic_id]
    top_indices = component.argsort()[::-1][:top_words_n]
    top_words = [feature_names[i] for i in top_indices]

    return {
        "topic_id": topic_id,
        "label": TOPIC_LABELS.get(topic_id, f"Topic {topic_id}"),
        "top_words": top_words,
    }
