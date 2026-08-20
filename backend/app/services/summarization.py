"""
summarization.py
-------------------
Extractive summarization for longer articles. Scores each sentence by the sum of its words' TF-IDF weights
(reusing the same fitted vectorizer, no separate model needed) and
returns the top-N highest-scoring sentences, in their ORIGINAL order
(not sorted by score) so the summary still reads coherently.

Why not full TextRank: TextRank needs a sentence-similarity graph and a
PageRank pass (typically via networkx), which is a real dependency and
real complexity for a marginal quality gain at this scale. Sentence-
level TF-IDF scoring is simpler, needs nothing new (reuses Module 4's
vectorizer), and the brief explicitly names it as an acceptable
alternative.

Why this only matters for genuinely long input: Module 3's EDA found
Inshorts articles average ~59-60 words already (their whole editorial
format), so "summarizing" a typical dataset row would just be
paraphrasing something already summary-length. This only produces a
real summary for longer text a user pastes in directly — see
`Config.SUMMARIZATION_MIN_WORDS` in config.py, checked by the calling
route, not by this module (kept as a route-level policy decision, not
baked into the summarizer itself).
"""

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
    top_indices.sort()  # restore original reading order

    return " ".join(sentences[i] for i in top_indices)
