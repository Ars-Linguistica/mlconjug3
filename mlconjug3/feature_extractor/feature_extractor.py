"""
This module declares the feature extractors for verbs.

A custom tokenizer optimized for extracting verb features.
"""

import re
from mlconjug3.constants import ALPHABET


def extract_verb_features(verb, lang=None, ngram_range=None):
    """
    Extract base features from a verb.

    NOTE:
    - ngram_range is deprecated and ignored.
    - N-gram generation is now handled by sklearn's CountVectorizer.

    :param verb: str
    :param lang: str
    :param ngram_range: deprecated
    :return: list[str]
    """
    _white_spaces = re.compile(r"\s\s+")
    verb = _white_spaces.sub(" ", verb).lower()

    if not verb:
        return []

    verb_len = len(verb)

    # ---------------------------
    # Base features (NO n-grams)
    # ---------------------------
    features = []

    # Basic morphological signals
    features.append(f"END={verb[-2:]}")   # last 2 chars
    features.append(f"END3={verb[-3:]}" if verb_len >= 3 else f"END3={verb}")

    features.append(f"START={verb[:2]}")
    features.append(f"START3={verb[:3]}" if verb_len >= 3 else f"START3={verb}")

    # Length
    features.append(f"LEN={verb_len}")

    # ---------------------------
    # Language-specific features
    # ---------------------------
    if lang not in ALPHABET:
        lang = "en"

    vowels = sum(verb.count(c) for c in ALPHABET[lang]["vowels"])
    consonants = sum(verb.count(c) for c in ALPHABET[lang]["consonants"])

    features.append(f"VOW_NUM={vowels}")
    features.append(f"CONS_NUM={consonants}")

    if consonants == 0:
        features.append("V/C=N/A")
    else:
        features.append(f"V/C={round(vowels / consonants, 2)}")

    return features


if __name__ == "__main__":
    pass
