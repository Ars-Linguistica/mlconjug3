"""
Feature extraction module for verb conjugation classification.

This version provides:
- Morphological signals (prefix/suffix structure)
- Length + phonetic statistics
- Language-aware vowel/consonant ratios
- Structural repetition patterns
- Light internal character patterns (bigram-like signals)
"""

import re
from mlconjug3.constants import ALPHABET


def extract_verb_features(verb, lang=None, ngram_range=None):
    """
    Extract handcrafted linguistic features from a verb.

    NOTE:
    - Character n-grams are handled separately in CountVectorizer.
    - This function only provides symbolic/linguistic features.
    """

    _white_spaces = re.compile(r"\s\s+")
    verb = _white_spaces.sub(" ", verb).lower()

    if not verb:
        return []

    verb_len = len(verb)
    features = []

    # ---------------------------
    # Basic morphology
    # ---------------------------
    features.append(f"END={verb[-2:]}")
    features.append(f"END3={verb[-3:]}" if verb_len >= 3 else f"END3={verb}")

    features.append(f"START={verb[:2]}")
    features.append(f"START3={verb[:3]}" if verb_len >= 3 else f"START3={verb}")

    features.append(f"LEN={verb_len}")

    # ---------------------------
    # Suffix patterns (strong signal)
    # ---------------------------
    for i in range(2, min(6, verb_len + 1)):
        features.append(f"SUF{i}={verb[-i:]}")

    # ---------------------------
    # Prefix patterns
    # ---------------------------
    for i in range(2, min(5, verb_len + 1)):
        features.append(f"PREF{i}={verb[:i]}")

    # ---------------------------
    # Language-specific phonetics
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

    # ---------------------------
    # Structural signal: double letters
    # ---------------------------
    has_double = any(verb[i] == verb[i + 1] for i in range(len(verb) - 1))
    features.append(f"HAS_DOUBLE={has_double}")

    # ---------------------------
    # Internal character patterns (light bigram signal)
    # ---------------------------
    for i in range(len(verb) - 1):
        features.append(f"BI_{verb[i:i+2]}")

    return features


if __name__ == "__main__":
    pass
