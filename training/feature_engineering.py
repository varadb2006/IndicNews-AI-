"""
feature_engineering.py
------------------------
Feature engineering for the cleaned/tokenized corpus produced by
`preprocessing.py`. Builds the TF-IDF representation used by Module 6
(Classification), Module 7 (Keyword Extraction), and Module 9
(Similarity Search) — one fitted vectorizer, reused everywhere, so
"similar keywords" always means the same feature space.

"""

import re

from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer


_REPORTING_VERB_STEMS = {
    "उन्हों", "ले", "बत", "गई", "रह", "बन", "जा", "लग",
    "गए", "मिल", "दे", "दी", "कर", "लिख", "चल",
}


_ATTRIBUTION_CONNECTORS = {"मुताबिक", "बकौल", "दौरान", "साम"}

EXTENDED_STOPWORDS_HI = _REPORTING_VERB_STEMS | _ATTRIBUTION_CONNECTORS



_PURE_NUMERIC_PATTERN = re.compile(r"^[0-9०-९]+$")


def _identity(tokens):
    
    return tokens


def remove_extended_stopwords(tokens: list) -> list:
    return [t for t in tokens if t not in EXTENDED_STOPWORDS_HI]


def remove_numeric_tokens(tokens: list) -> list:
   
    return [t for t in tokens if not _PURE_NUMERIC_PATTERN.match(t)]


def finalize_tokens_for_features(tokens: list, drop_numeric: bool = False) -> list:
    
    tokens = remove_extended_stopwords(tokens)
    if drop_numeric:
        tokens = remove_numeric_tokens(tokens)
    return tokens




def build_tfidf_vectorizer(ngram_range=(1, 3), min_df=5, max_df=0.85, **kwargs):
    
    return TfidfVectorizer(
        tokenizer=_identity,
        preprocessor=_identity,
        token_pattern=None,
        lowercase=False,
        ngram_range=ngram_range,
        min_df=min_df,
        max_df=max_df,
        sublinear_tf=True,
        **kwargs,
    )


def build_count_vectorizer(ngram_range=(1, 1), min_df=5, max_df=0.85, **kwargs):
    
    return CountVectorizer(
        tokenizer=_identity,
        preprocessor=_identity,
        token_pattern=None,
        lowercase=False,
        ngram_range=ngram_range,
        min_df=min_df,
        max_df=max_df,
        **kwargs,
    )


def build_combined_token_field(df, headline_col="Headline_tokens", content_col="Content_tokens", drop_numeric=False):
    
    combined = df[headline_col] + df[content_col]
    return combined.apply(lambda toks: finalize_tokens_for_features(toks, drop_numeric=drop_numeric))