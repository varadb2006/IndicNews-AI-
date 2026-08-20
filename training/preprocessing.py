
import json
import os
import re
import unicodedata

from indicnlp.normalize.indic_normalize import IndicNormalizerFactory
from indicnlp.tokenize import indic_tokenize



_NORMALIZER = IndicNormalizerFactory().get_normalizer("hi")

_STOPWORDS_PATH = os.path.join(os.path.dirname(__file__), "resources", "hindi_stopwords.json")
with open(_STOPWORDS_PATH, encoding="utf-8") as f:
    HINDI_STOPWORDS = set(json.load(f))


_ALLOWED_CHARS_PATTERN = re.compile(
    r"[^\u0900-\u097F\sA-Za-z0-9।॥]"
)
_URL_PATTERN = re.compile(r"(https?://\S+|www\.\S+)")
_EXTRA_SPACE_PATTERN = re.compile(r"\s+")

_PUNCTUATION_ONLY_TOKENS = {"।", "॥"}
_HAS_WORD_CHAR_PATTERN = re.compile(r"[\u0900-\u097FA-Za-z0-9]")


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
_MIN_STEM_LENGTH = 2  



def normalize_unicode(text: str) -> str:
    
    if not isinstance(text, str):
        return ""
    text = unicodedata.normalize("NFC", text)
    return _NORMALIZER.normalize(text)


def remove_urls(text: str) -> str:
    
    return _URL_PATTERN.sub(" ", text)


def remove_special_characters(text: str) -> str:
    
    return _ALLOWED_CHARS_PATTERN.sub(" ", text)


def remove_extra_spaces(text: str) -> str:
    return _EXTRA_SPACE_PATTERN.sub(" ", text).strip()


def tokenize(text: str) -> list:
    
    return indic_tokenize.trivial_tokenize(text, lang="hi")


def remove_stopwords(tokens: list) -> list:
    return [t for t in tokens if t not in HINDI_STOPWORDS]


def light_stem(token: str) -> str:
    
    for length in (5, 4, 3, 2, 1):
        if len(token) - length < _MIN_STEM_LENGTH:
            continue
        for suffix in _SUFFIXES_BY_LENGTH[length]:
            if token.endswith(suffix):
                return token[: -length]
    return token



def preprocess_text(
    text: str,
    remove_stopwords_flag: bool = True,
    apply_stemming: bool = True,
) -> tuple:
    
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