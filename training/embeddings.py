"""
embeddings.py
--------------
Word2Vec and FastText training for the IndicNews AI project (Module 5).
The brief says "implement Word2Vec or FastText, whichever suits best" —
this module trains BOTH on the same corpus with matching hyperparameters
so 04_WordEmbeddings.ipynb can make that comparison with real numbers
instead of asserting it. Short version, confirmed in the notebook:
FastText wins for this dataset because Hindi is morphologically rich
(heavy inflection, frequent OOV/rare word forms even after stemming),
and FastText's subword n-grams handle that where Word2Vec just fails
with a KeyError.

Input corpus choice: trained on `Content_tokens` (IndicNLP-tokenized,
Hindi-stopword-removed, light-stemmed — the output of
`preprocessing.py`), NOT the further `EXTENDED_STOPWORDS_HI`-filtered
tokens from `feature_engineering.py`. Reasoning: Word2Vec/FastText learn
from local co-occurrence windows, so aggressively stripping additional
"reporting verb" tokens would shrink and distort context windows for
little benefit — that extra stopword layer was motivated by TF-IDF
feature *sparsity*, which doesn't apply here. The base
`preprocessing.py` stopword removal is kept since those are true
function words that add little distributional signal either way.


"""

import os

from gensim.models import Word2Vec, FastText
from gensim.models.fasttext import FastTextKeyedVectors


DEFAULT_PARAMS = dict(
    vector_size=100,
    window=5,
    min_count=5,
    sg=1,          
    epochs=10,
    workers=max(1, os.cpu_count() - 1),
    seed=42,
)


def train_word2vec(token_lists, **overrides):
    
    params = {**DEFAULT_PARAMS, **overrides}
    sentences = list(token_lists)
    return Word2Vec(sentences=sentences, **params)


def train_fasttext(token_lists, min_n=3, max_n=6, **overrides):
   
    params = {**DEFAULT_PARAMS, **overrides}
    sentences = list(token_lists)
    return FastText(sentences=sentences, min_n=min_n, max_n=max_n, **params)


def most_similar(model, word, topn=10):
    
    wv = model.wv if hasattr(model, "wv") else model
    is_fasttext = isinstance(wv, FastTextKeyedVectors)

    if not is_fasttext and word not in wv.key_to_index:
        return f"'{word}' not in vocabulary (min_count={DEFAULT_PARAMS['min_count']} excluded it; plain Word2Vec has no subword fallback for OOV words)"

    try:
        return wv.most_similar(word, topn=topn)
    except KeyError as e:
        return f"'{word}' could not be resolved even via subwords: {e}"
