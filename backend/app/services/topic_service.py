
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
