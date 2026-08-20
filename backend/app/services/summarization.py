import re

_SENTENCE_SPLIT_PATTERN = re.compile(r"(?<=[।॥.!?])\s+")


def split_sentences(text):
    
    sentences = _SENTENCE_SPLIT_PATTERN.split(text.strip())
    return [s.strip() for s in sentences if s.strip()]


def summarize(text, tfidf_vectorizer, preprocess_fn, finalize_fn, n_sentences=3):
    
    sentences = split_sentences(text)
    if len(sentences) <= n_sentences:
        return text.strip()

    sentence_scores = []
    for sentence in sentences:
        tokens = finalize_fn(preprocess_fn(sentence))
        if not tokens:
            sentence_scores.append(0.0)
            continue
        vector = tfidf_vectorizer.transform([tokens])
        sentence_scores.append(float(vector.sum()))

    top_indices = sorted(
        range(len(sentences)), key=lambda i: -sentence_scores[i]
    )[:n_sentences]
    top_indices.sort()  

    return " ".join(sentences[i] for i in top_indices)
