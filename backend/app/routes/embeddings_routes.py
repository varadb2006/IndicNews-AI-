"""
routes/embeddings_routes.py
------------------------------
GET /similar-words?word=... — bonus endpoint. The brief's "Semantic
Representation" feature says to train Word2Vec/FastText and "show
similar words." Module 5 already demonstrated this in the training
notebook, but exposing it through the live app too means it's not just
a one-off Colab result. Uses FastText specifically (not Word2Vec) —
Module 5's real comparison found FastText handles typos/rare word forms
via subwords where Word2Vec fails outright, which matters for
arbitrary user-typed queries here.
"""

from flask import Blueprint, jsonify, request

from app.config import Config
from app.services.model_loader import ModelBundle

embeddings_bp = Blueprint("embeddings", __name__)


@embeddings_bp.route("/similar-words", methods=["GET"])
def similar_words():
    word = request.args.get("word", "").strip()
    if not word:
        return jsonify({"error": "Query parameter 'word' is required."}), 400

    bundle = ModelBundle.get()
    if bundle.fasttext_model is None:
        return jsonify({
            "error": "FastText model not loaded. Ensure fasttext.model exists in "
                     "models/saved_models/ (see Module 5's 04_WordEmbeddings.ipynb)."
        }), 503

    wv = bundle.fasttext_model.wv
    try:
        results = wv.most_similar(word, topn=Config.SIMILAR_WORDS_TOP_N)
    except KeyError as e:
        return jsonify({"error": f"Could not resolve '{word}': {e}"}), 404

    return jsonify({
        "word": word,
        "similar_words": [{"word": w, "similarity": round(float(s), 4)} for w, s in results],
    })
