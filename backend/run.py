"""
run.py
-------
Entrypoint. 

The app factory (app/__init__.py) loads all models eagerly at startup,
so there will be a noticeable pause (Stanza's pipeline load is the slow
part) before you see "Running on http://0.0.0.0:5000"  that's expected,
not a hang.
"""

from app import create_app
from app.config import Config

app = create_app()

if __name__ == "__main__":
    app.run(host=Config.HOST, port=Config.PORT, debug=Config.DEBUG)
