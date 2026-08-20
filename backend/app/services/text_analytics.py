"""
text_analytics.py
--------------------
Basic text statistics.
"""

from app.services.summarization import split_sentences

WORDS_PER_MINUTE = 200


def compute_statistics(text):
    words = text.split()
    sentences = split_sentences(text)

    word_count = len(words)
    char_count = len(text)
    sentence_count = len(sentences)
    reading_time_seconds = max(1, round(word_count / WORDS_PER_MINUTE * 60))

    return {
        "word_count": word_count,
        "character_count": char_count,
        "sentence_count": sentence_count,
        "estimated_reading_time_seconds": reading_time_seconds,
    }
