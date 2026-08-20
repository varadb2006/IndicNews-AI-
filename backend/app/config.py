"""
config.py
----------
Centralized configuration for the Flask backend — model artifact paths,
thresholds, and settings. Keeping this in one place means no file has a
hardcoded relative path buried in it; everything resolves from
BASE_DIR, so the app works the same whether it's run from
`backend/`, from the project root, or from inside a container.
"""

import os


CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.abspath(os.path.join(CURRENT_DIR, '..', '..'))
TRAINING_DIR = os.path.join(BASE_DIR, "training")
SAVED_MODELS_DIR = os.path.join(BASE_DIR, "models", "saved_models")


class Config:
    
    BASE_DIR = BASE_DIR
    TRAINING_DIR = TRAINING_DIR
    SAVED_MODELS_DIR = SAVED_MODELS_DIR

    
    TFIDF_VECTORIZER_PATH = os.path.join(SAVED_MODELS_DIR, "tfidf_vectorizer.joblib")
    CLASSIFIER_PATH = os.path.join(SAVED_MODELS_DIR, "classifier.joblib")
    TFIDF_MATRIX_PATH = os.path.join(SAVED_MODELS_DIR, "tfidf_matrix.npz")
    TOPIC_MODEL_NMF_PATH = os.path.join(SAVED_MODELS_DIR, "topic_model_nmf.joblib")
    FASTTEXT_MODEL_PATH = os.path.join(SAVED_MODELS_DIR, "fasttext.model")

   
    CLASSIFICATION_THRESHOLD = 0.3  
    SIMILARITY_TOP_N = 5            
    KEYWORD_TOP_N = 10               
    SIMILAR_WORDS_TOP_N = 10

    
    SUMMARIZATION_MIN_WORDS = 40
    SUMMARIZATION_SENTENCE_COUNT = 3

   
    CORS_ORIGINS = ["http://localhost:3000", "http://localhost:5173"]

    
    HOST = "0.0.0.0"
    PORT = 5000
    DEBUG = True  
