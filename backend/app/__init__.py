"""
app/__init__.py
------------------
Flask application factory. Models are loaded EAGERLY here (not lazily
on first request) — `ModelBundle.get()` is called once at startup, so
the slow Stanza pipeline load and joblib deserialization happen before
the server starts accepting requests, not on whichever unlucky first
request triggers it.
"""

from flask import Flask
from flask_cors import CORS

from app.config import Config


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app, origins=Config.CORS_ORIGINS)

    from app.routes.analyze import analyze_bp
    from app.routes.health import health_bp
    from app.routes.embeddings_routes import embeddings_bp

    app.register_blueprint(analyze_bp)
    app.register_blueprint(health_bp)
    app.register_blueprint(embeddings_bp)

    # Force model loading now, not on first request — see module docstring.
    with app.app_context():
        from app.services.model_loader import ModelBundle
        ModelBundle.get()

    return app
