"""
ner.py
-------
Named Entity Recognition via Stanza's Hindi pipeline 
Extracts Person / Location / Organization entities.

IMPORTANT — run NER on RAW text, not preprocessed text:
    `preprocessing.py`'s pipeline (stemming, stopword removal, special
    character stripping) is built for TF-IDF/classification, and it
    actively destroys what NER needs: word casing/inflection, sentence
    punctuation, and word order. Stanza's Hindi NER model expects
    natural, unmodified text. Always call `extract_entities()` on the
    original `Headline`/`Content` columns, never on `*_clean` /
    `*_tokens`.

"""

import re

import stanza
from indicnlp.tokenize import indic_tokenize

TAG_MAP = {
    "NEP": "Person",
    "NEL": "Location",
    "NEO": "Organization",
    "NEN": "Number",   
                       
    "NETI": "Time",    
}


_GAZETTEER_RAW = {
    
    "कांग्रेस": "Organization",
    "भाजपा": "Organization",
    "बीजेपी": "Organization",
    "टीएमसी": "Organization",
    "तृणमूल कांग्रेस": "Organization",
    "शिवसेना": "Organization",
    "एनसीपी": "Organization",
    "सपा": "Organization",
    "समाजवादी पार्टी": "Organization",
    "बसपा": "Organization",
    "बहुजन समाज पार्टी": "Organization",
    "जदयू": "Organization",
    "राजद": "Organization",
    "आम आदमी पार्टी": "Organization",
    "द्रमुक": "Organization",
    "अन्नाद्रमुक": "Organization",
    "अकाली दल": "Organization",
    "congress": "Organization",
    "bjp": "Organization",
    "tmc": "Organization",
    "aap": "Organization",
    "shiv sena": "Organization",
}


def _tokenize_for_gazetteer(text: str) -> list:
    
    tokens = indic_tokenize.trivial_tokenize(text, lang="hi")
    return [t.lower() if t.isascii() else t for t in tokens]


_GAZETTEER = {
    tuple(_tokenize_for_gazetteer(phrase)): entity_type
    for phrase, entity_type in _GAZETTEER_RAW.items()
}
_MAX_GAZETTEER_PHRASE_LEN = max(len(k) for k in _GAZETTEER)


def gazetteer_entities(text: str) -> list:
   
    original_tokens = indic_tokenize.trivial_tokenize(text, lang="hi")
    match_tokens = [t.lower() if t.isascii() else t for t in original_tokens]

    matches = []
    i, n = 0, len(match_tokens)
    while i < n:
        matched_len = 0
        for length in range(min(_MAX_GAZETTEER_PHRASE_LEN, n - i), 0, -1):
            window = tuple(match_tokens[i:i + length])
            if window in _GAZETTEER:
                display_text = " ".join(original_tokens[i:i + length])
                matches.append({
                    "text": display_text,
                    "type": _GAZETTEER[window],
                    "raw_type": "GAZETTEER",
                    "start_char": None,
                    "end_char": None,
                })
                matched_len = length
                break
        i += matched_len if matched_len else 1
    return matches

_PIPELINE = None  


def get_pipeline():
    
    global _PIPELINE
    if _PIPELINE is None:
        _PIPELINE = stanza.Pipeline(lang="hi", processors="tokenize,ner", verbose=False)
    return _PIPELINE


def map_entity_type(raw_tag: str) -> str:
    
    return TAG_MAP.get(raw_tag.upper(), raw_tag)


def extract_entities(text: str, nlp=None, use_gazetteer: bool = True) -> list:
    
    nlp = nlp or get_pipeline()
    doc = nlp(text)
    entities = []
    for ent in doc.ents:
        entities.append({
            "text": ent.text,
            "type": map_entity_type(ent.type),
            "raw_type": ent.type,
            "start_char": ent.start_char,
            "end_char": ent.end_char,
        })

    if use_gazetteer:
        seen = {e["text"] for e in entities}
        for g in gazetteer_entities(text):
            if g["text"] not in seen:
                entities.append(g)
                seen.add(g["text"])

    return entities


def group_entities_by_type(entities: list) -> dict:
    grouped = {}
    for ent in entities:
        bucket = grouped.setdefault(ent["type"], [])
        if ent["text"] not in bucket:
            bucket.append(ent["text"])
    return grouped


CORE_TYPES = {"Person", "Location", "Organization"}


def filter_core_entities(entities: list) -> list:
    
    return [ent for ent in entities if ent["type"] in CORE_TYPES]
