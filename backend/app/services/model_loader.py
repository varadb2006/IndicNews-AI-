import os
import sys

import joblib
import pandas as pd
import scipy.sparse as sp

from app.config import Config


sys.path.insert(0, Config.TRAINING_DIR)

from preprocessing import preprocess_text  
from feature_engineering import finalize_tokens_for_features  
from classification import predict_categories  
from ner import get_pipeline as get_ner_pipeline, extract_entities, group_entities_by_type
from topic_modeling import get_top_words_per_topic
from similarity import get_similar_for_new_text, format_results 


class ModelBundle:
    _instance = None

    def __init__(self):
        print("[model_loader] Loading TF-IDF vectorizer...")
        self.tfidf_vectorizer = joblib.load(Config.TFIDF_VECTORIZER_PATH)

        print("[model_loader] Loading classifier bundle...")
        clf_bundle = joblib.load(Config.CLASSIFIER_PATH)
        self.classifier = clf_bundle["model"]
        self.mlb = clf_bundle["mlb"]

        print("[model_loader] Loading TF-IDF corpus matrix + index...")
        self.X_corpus = sp.load_npz(Config.TFIDF_MATRIX_PATH)
        self.corpus_index = pd.read_pickle(
            os.path.join(Config.SAVED_MODELS_DIR, "corpus_index.pkl")
        )
        if self.X_corpus.shape[0] != len(self.corpus_index):
            raise ValueError(
                f"Row count mismatch: tfidf_matrix.npz has {self.X_corpus.shape[0]} rows "
                f"but corpus_index.pkl has {len(self.corpus_index)} rows. Re-run "
                f"training/build_corpus_index.py against the same deduplicated dataset "
                f"used to build the TF-IDF matrix."
            )

        print("[model_loader] Loading topic model...")
        self.topic_model = joblib.load(Config.TOPIC_MODEL_NMF_PATH)
        self.topic_feature_names = self.tfidf_vectorizer.get_feature_names_out()

        print("[model_loader] Loading Stanza NER pipeline (this is the slow one)...")
        self.ner_pipeline = get_ner_pipeline()

        self.fasttext_model = None
        if os.path.exists(Config.FASTTEXT_MODEL_PATH):
            print("[model_loader] Loading FastText model...")
            from gensim.models import FastText
            self.fasttext_model = FastText.load(Config.FASTTEXT_MODEL_PATH)

        print("[model_loader] All models loaded.")

    @classmethod
    def get(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance


    @staticmethod
    def preprocess_fn(text):
        return preprocess_text(text)[1]

    @staticmethod
    def finalize_fn(tokens):
        return finalize_tokens_for_features(tokens)

    def tokens_for(self, text):
        return self.finalize_fn(self.preprocess_fn(text))
