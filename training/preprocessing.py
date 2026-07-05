"""
preprocessing.py
------------------
Reusable Hindi text preprocessing pipeline, shared by every training
notebook from 02_Preprocessing.ipynb onward (and later ported into the
Flask backend in Module 10, so the exact same cleaning happens at
inference time as at training time).

Pipeline stages (each usable standalone, or chained via
`preprocess_text` / `preprocess_pipeline`):

    1. remove_urls          - strips http(s)/www links
    2. remove_special_characters
                             - drops punctuation/symbols/emoji, keeps
                               Devanagari text, Latin letters, and digits
    3. normalize_unicode    - Unicode NFC + Indic-aware normalization
                              (fixes nukta/matra variants, e.g. multiple
                              ways of encoding "क़" or "ी")
    4. remove_extra_spaces  - collapses repeated whitespace, strips ends
    5. tokenize             - Devanagari-aware tokenization via IndicNLP
                              (NOT nltk.word_tokenize — see note below)
    6. remove_stopwords     - drops ~225 common Hindi function words
    7. light_stem           - rule-based Hindi suffix stripping

IMPORTANT — why punctuation is stripped *before* normalization, not
after: IndicNLP's Devanagari normalizer has a hardcoded legacy-encoding
rule that silently rewrites a plain ASCII colon into the Devanagari
**visarga** character (ः, U+0903) whenever it directly follows a
Devanagari letter — e.g. "देखें:" becomes "देखेंः" (a real Devanagari
letter appended, not punctuation anymore). That corrupted word then
survives special-character stripping because visarga is a legitimate
character inside the Devanagari Unicode block. Running punctuation/URL
removal *first* means the normalizer never sees a bare colon to
"correct" in the first place. (Found this by testing on real headlines
— see 02_Preprocessing.ipynb §2 for the before/after.)

Why IndicNLP instead of NLTK for tokenization/stopwords:
    NLTK's tokenizers (Punkt) are trained on English/European sentence
    conventions and its `stopwords` corpus does not include Hindi at all
    (verified directly: `nltk.corpus.stopwords.fileids()` lists 33
    languages, no 'hindi'). IndicNLP's tokenizer understands Devanagari
    punctuation/structure, so it's the correct tool here. NLTK is not
    used in this module for that reason — see project README for the
    fuller explanation.

Usage (from a notebook):
    import sys
    sys.path.append("..")
    from preprocessing import preprocess_text, preprocess_pipeline

    clean, tokens = preprocess_text(raw_headline)
"""

import json
import os
import re
import unicodedata

from indicnlp.normalize.indic_normalize import IndicNormalizerFactory
from indicnlp.tokenize import indic_tokenize

# ---------------------------------------------------------------------
# Setup: normalizer + stopwords (loaded once at import time)
# ---------------------------------------------------------------------

_NORMALIZER = IndicNormalizerFactory().get_normalizer("hi")

_STOPWORDS_PATH = os.path.join(os.path.dirname(__file__), "resources", "hindi_stopwords.json")
with open(_STOPWORDS_PATH, encoding="utf-8") as f:
    HINDI_STOPWORDS = set(json.load(f))

# Devanagari block (U+0900–U+097F) + Vedic extensions some texts use,
# plus common Devanagari punctuation (danda ।, double-danda ॥).
_ALLOWED_CHARS_PATTERN = re.compile(
    r"[^\u0900-\u097F\sA-Za-z0-9।॥]"
)
_URL_PATTERN = re.compile(r"(https?://\S+|www\.\S+)")
_EXTRA_SPACE_PATTERN = re.compile(r"\s+")
# A token that contains no Devanagari letter, Latin letter, or digit is
# pure punctuation (e.g. a lone danda '।' or '॥' surviving tokenization)
# and adds nothing but noise to BoW/TF-IDF/embeddings — drop it at the
# token stage. NOTE: `clean_text` is built by joining this same filtered
# token list, so danda is excluded from `clean_text` too, not just from
# `tokens` — if a later module needs sentence-boundary detection, split
# on danda in the *raw* `Content`/`Headline` column, before this pipeline
# runs, not on its output.
_PUNCTUATION_ONLY_TOKENS = {"।", "॥"}
_HAS_WORD_CHAR_PATTERN = re.compile(r"[\u0900-\u097FA-Za-z0-9]")

# Rule-based Hindi suffix list for light stemming, ordered longest-first
# so e.g. "ाएंगी" is stripped whole rather than leaving "ाएंगी" partially
# un-stripped by a shorter suffix matching first. This is the standard
# suffix set used in Hindi light-stemming literature (Ramanathan & Rao
# style rules) — Hindi has no single dominant lemmatizer the way English
# has WordNet, so rule-based suffix stripping is the practical choice
# for a fast, dependency-light pass over 185k+ rows. (A statistical
# lemmatizer via Stanza is introduced later in Module 7/NER, and can be
# swapped in for higher accuracy on smaller batches if needed.)
_SUFFIXES_BY_LENGTH = {
    5: ["ाएंगी", "ाएंगे", "ाऊंगी", "ाऊंगा", "ाइयाँ", "ाइयों", "ाइयां"],
    4: ["ाएगी", "ाएगा", "ाओगी", "ाओगे", "एंगी", "ेंगी", "एंगे", "ेंगे",
        "ूंगी", "ूंगा", "ियाँ", "ियों", "ियां"],
    3: ["ाकर", "ाइए", "ाईं", "ाया", "ेगी", "ेगा", "ोगी", "ोगे", "ाने",
        "ाना", "ाते", "ाती", "ाता", "तीं", "ाओं", "ाएं", "ुओं", "ुएं"],
    2: ["कर", "ाओ", "िए", "ाई", "ाए", "ने", "नी", "ना", "ते", "ीं",
        "ती", "ता", "ाँ", "ां", "ों", "ें"],
    1: ["ो", "े", "ू", "ु", "ी", "ि", "ा"],
}
_MIN_STEM_LENGTH = 2  # never strip a suffix if it would leave < 2 chars


# ---------------------------------------------------------------------
# Individual pipeline stages
# ---------------------------------------------------------------------

def normalize_unicode(text: str) -> str:
    """
    Apply standard Unicode NFC normalization, then IndicNLP's Hindi-aware
    normalizer (handles nukta variants, multiple matra encodings, and
    other Devanagari quirks that plain `unicodedata.normalize` misses).
    """
    if not isinstance(text, str):
        return ""
    text = unicodedata.normalize("NFC", text)
    return _NORMALIZER.normalize(text)


def remove_urls(text: str) -> str:
    """Strip http(s):// and www. links."""
    return _URL_PATTERN.sub(" ", text)


def remove_special_characters(text: str) -> str:
    """
    Remove punctuation, symbols, and emoji while keeping Devanagari
    script, Latin letters (some headlines mix in English acronyms/
    brand names), digits, and Devanagari sentence punctuation (danda).
    """
    return _ALLOWED_CHARS_PATTERN.sub(" ", text)


def remove_extra_spaces(text: str) -> str:
    """Collapse repeated whitespace/newlines/tabs into single spaces."""
    return _EXTRA_SPACE_PATTERN.sub(" ", text).strip()


def tokenize(text: str) -> list:
    """
    Devanagari-aware word tokenization via IndicNLP (not NLTK — see
    module docstring for why NLTK's tokenizer is the wrong tool here).
    """
    return indic_tokenize.trivial_tokenize(text, lang="hi")


def remove_stopwords(tokens: list) -> list:
    """Drop tokens that are in the ~225-word Hindi stopword list."""
    return [t for t in tokens if t not in HINDI_STOPWORDS]


def light_stem(token: str) -> str:
    """
    Rule-based Hindi suffix stripping. Tries suffixes longest-first so a
    5-character ending like 'ाएंगी' is matched whole instead of a
    shorter suffix cutting it awkwardly. Refuses to strip if doing so
    would leave a stem shorter than `_MIN_STEM_LENGTH`, to avoid
    destroying short/already-base-form words.
    """
    for length in (5, 4, 3, 2, 1):
        if len(token) - length < _MIN_STEM_LENGTH:
            continue
        for suffix in _SUFFIXES_BY_LENGTH[length]:
            if token.endswith(suffix):
                return token[: -length]
    return token


# ---------------------------------------------------------------------
# Full pipeline
# ---------------------------------------------------------------------

def preprocess_text(
    text: str,
    remove_stopwords_flag: bool = True,
    apply_stemming: bool = True,
) -> tuple:
    """
    Run the full cleaning pipeline on one string.

    Returns:
        (clean_text, tokens) where `clean_text` is the cleaned, joined
        string (useful for TF-IDF/vectorizers that expect raw text) and
        `tokens` is the final token list (useful for Word2Vec/FastText
        training, which expect pre-tokenized input).
    """
    text = remove_urls(text)
    text = remove_special_characters(text)
    text = normalize_unicode(text)
    text = remove_extra_spaces(text)

    tokens = tokenize(text)
    tokens = [
        t for t in tokens
        if t.strip() and t not in _PUNCTUATION_ONLY_TOKENS and _HAS_WORD_CHAR_PATTERN.search(t)
    ]

    if remove_stopwords_flag:
        tokens = remove_stopwords(tokens)
    if apply_stemming:
        tokens = [light_stem(t) for t in tokens]

    clean_text = " ".join(tokens)
    return clean_text, tokens


def preprocess_pipeline(
    df,
    columns=("Headline", "Content"),
    remove_stopwords_flag: bool = True,
    apply_stemming: bool = True,
):
    """
    Apply `preprocess_text` across one or more DataFrame columns,
    producing `<column>_clean` (string) and `<column>_tokens` (list)
    columns for each. Used on both Headline and Content per the project
    brief ("use both ... during preprocessing wherever appropriate").
    """
    df = df.copy()
    for col in columns:
        results = df[col].apply(
            lambda t: preprocess_text(t, remove_stopwords_flag, apply_stemming)
        )
        df[f"{col}_clean"] = results.apply(lambda r: r[0])
        df[f"{col}_tokens"] = results.apply(lambda r: r[1])
    return df