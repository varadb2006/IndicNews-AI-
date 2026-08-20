from flask import Blueprint, jsonify, request

from app.config import Config
from app.services.model_loader import (
    ModelBundle, predict_categories, extract_entities, group_entities_by_type,
    get_similar_for_new_text, format_results,
)
from app.services.keyword_extraction import extract_keywords
from app.services.topic_service import predict_topic
from app.services.summarization import summarize
from app.services.text_analytics import compute_statistics

analyze_bp = Blueprint("analyze", __name__)


@analyze_bp.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json(silent=True)
    if not data or "text" not in data:
        return jsonify({"error": "Request body must be JSON with a 'text' field."}), 400

    text = data["text"].strip()
    if not text:
        return jsonify({"error": "'text' cannot be empty."}), 400

    bundle = ModelBundle.get()

   
    category_predictions = predict_categories(
        text, bundle.tfidf_vectorizer, bundle.classifier, bundle.mlb,
        preprocess_fn=bundle.preprocess_fn, finalize_fn=bundle.finalize_fn,
        threshold=Config.CLASSIFICATION_THRESHOLD,
    )
    categories = [{"label": label, "confidence": conf} for label, conf in category_predictions]

    
    entities = extract_entities(text, bundle.ner_pipeline)
    grouped_entities = group_entities_by_type(entities)

    
    keywords = extract_keywords(
        text, bundle.tfidf_vectorizer,
        preprocess_fn=bundle.preprocess_fn, finalize_fn=bundle.finalize_fn,
        top_n=Config.KEYWORD_TOP_N,
    )

    
    topic = predict_topic(
        text, bundle.tfidf_vectorizer, bundle.topic_model, bundle.topic_feature_names,
        preprocess_fn=bundle.preprocess_fn, finalize_fn=bundle.finalize_fn,
    )

    similar_results = get_similar_for_new_text(
        text, bundle.tfidf_vectorizer, bundle.X_corpus,
        preprocess_fn=bundle.preprocess_fn, finalize_fn=bundle.finalize_fn,
        top_n=Config.SIMILARITY_TOP_N,
    )
    similar_articles = format_results(similar_results, bundle.corpus_index)

    statistics = compute_statistics(text)

    summary = None
    if statistics["word_count"] >= Config.SUMMARIZATION_MIN_WORDS:
        summary = summarize(
            text, bundle.tfidf_vectorizer,
            preprocess_fn=bundle.preprocess_fn, finalize_fn=bundle.finalize_fn,
            n_sentences=Config.SUMMARIZATION_SENTENCE_COUNT,
        )

    return jsonify({
        "categories": categories,
        "keywords": keywords,
        "entities": grouped_entities,
        "topic": topic,
        "summary": summary,
        "statistics": statistics,
        "similar_articles": similar_articles,
    })
