"""routes/health.py -- simple liveness check, and confirms models loaded."""

from flask import Blueprint, jsonify

from app.services.model_loader import ModelBundle

health_bp = Blueprint("health", __name__)


@health_bp.route("/health", methods=["GET"])
def health():
    try:
        bundle = ModelBundle.get()
        return jsonify({
            "status": "ok",
            "models_loaded": True,
            "corpus_size": int(bundle.X_corpus.shape[0]),
        })
    except Exception as e:
        return jsonify({"status": "error", "models_loaded": False, "detail": str(e)}), 500
