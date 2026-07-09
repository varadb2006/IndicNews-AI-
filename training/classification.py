"""
classification.py
-------------------
Multi-label news category classification (Module 6). Builds on:
  - TF-IDF vectorizer/matrix (models/saved_models/tfidf_*)
  - `core_categories` multi-label column (data_utils.py)

Why multi-label, and why Logistic Regression specifically:

  established that a row can genuinely belong to more than one
  category at once (e.g. `sports` AND `national`), so this is a
  multi-label problem — `MultiLabelBinarizer` + `OneVsRestClassifier`,
  not a plain single-label classifier.

  Logistic Regression is used here because the target `/analyze`
  API response needs a genuine confidence score per predicted category
  Logistic Regression's `predict_proba` gives calibrated-ish probabilities
  natively; LinearSVC's `decision_function` is not a probability and
  would need extra calibration (CalibratedClassifierCV) to produce one
  
IMPORTANT — feature/label alignment: the saved TF-IDF matrix
(`tfidf_matrix.npz`) does NOT have labels saved alongside it. Row
alignment depends on re-running the *exact* same pipeline
(`load_dataset` -> `drop_duplicates` -> `reset_index` -> same order) that
built the matrix. `load_features_and_labels()` does this and
asserts the row counts match, specifically to catch silent misalignment
early rather than training a classifier against shuffled labels.
"""

import joblib
import numpy as np
import scipy.sparse as sp
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    classification_report,
    f1_score,
    hamming_loss,
    multilabel_confusion_matrix,
)
from sklearn.model_selection import train_test_split
from sklearn.multiclass import OneVsRestClassifier
from sklearn.preprocessing import MultiLabelBinarizer

SAVED_MODELS_DIR = "../../models/saved_models"


def load_features_and_labels(clean_df):
  
    X = sp.load_npz(f"{SAVED_MODELS_DIR}/tfidf_matrix.npz")

    if X.shape[0] != len(clean_df):
        raise ValueError(
            f"Row count mismatch: tfidf_matrix.npz has {X.shape[0]} rows but "
            f"clean_df has {len(clean_df)} rows. This means clean_df wasn't "
            f"built with the exact same load_dataset -> drop_duplicates -> "
            f"preprocess_pipeline sequence used  labels would "
            f"silently misalign with features if we proceeded. Rebuild "
            f"clean_df using that exact sequence (see this function's docstring)."
        )

    mlb = MultiLabelBinarizer()
    Y = mlb.fit_transform(clean_df["core_categories"])
    return X, Y, mlb


def train_classifier(X_train, Y_train, **logreg_overrides):
   
    params = dict(max_iter=1000, class_weight="balanced", random_state=42)
    params.update(logreg_overrides)
    model = OneVsRestClassifier(LogisticRegression(**params))
    model.fit(X_train, Y_train)
    return model


def evaluate_classifier(model, X_test, Y_test, class_names):
    
    Y_pred = model.predict(X_test)

    report = classification_report(
        Y_test, Y_pred, target_names=class_names, zero_division=0
    )
    micro_f1 = f1_score(Y_test, Y_pred, average="micro", zero_division=0)
    macro_f1 = f1_score(Y_test, Y_pred, average="macro", zero_division=0)
    weighted_f1 = f1_score(Y_test, Y_pred, average="weighted", zero_division=0)
    h_loss = hamming_loss(Y_test, Y_pred)
    subset_acc = np.mean(np.all(Y_test == Y_pred, axis=1))
    conf_matrices = multilabel_confusion_matrix(Y_test, Y_pred)

    return {
        "report": report,
        "micro_f1": micro_f1,
        "macro_f1": macro_f1,
        "weighted_f1": weighted_f1,
        "hamming_loss": h_loss,
        "subset_accuracy": subset_acc,
        "confusion_matrices": conf_matrices,
        "Y_pred": Y_pred,
    }


def save_classifier_bundle(model, mlb, path=f"{SAVED_MODELS_DIR}/classifier.joblib"):
   
    joblib.dump({"model": model, "mlb": mlb}, path)


def predict_categories(text, tfidf_vectorizer, model, mlb, preprocess_fn, finalize_fn=None, threshold=0.5):
    
    tokens = preprocess_fn(text)
    if finalize_fn is not None:
        tokens = finalize_fn(tokens)

    X = tfidf_vectorizer.transform([tokens])
    probs = model.predict_proba(X)[0]

    results = [
        (mlb.classes_[i], round(float(p) * 100, 1))
        for i, p in enumerate(probs)
        if p >= threshold
    ]
    return sorted(results, key=lambda x: -x[1])
