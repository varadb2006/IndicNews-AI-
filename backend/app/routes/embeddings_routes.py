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
                     "models/saved_models/"
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
