
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
