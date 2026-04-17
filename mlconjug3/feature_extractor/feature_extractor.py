"""
Feature extraction module for verb conjugation classification.

Now optimized for:
- Romanian (morphological complexity)
- Italian (stem variation)
- Stable performance for Romance languages
"""

import re
from mlconjug3.constants import ALPHABET


def extract_verb_features(verb, lang=None, ngram_range=None):
    _white_spaces = re.compile(r"\s\s+")
    verb = _white_spaces.sub(" ", verb).lower()

    if not verb:
        return []

    verb_len = len(verb)
    features = []

    weak_lang = lang in {"ro", "it"}

    # ---------------------------
    # CORE MORPHOLOGY
    # ---------------------------
    features.append(f"END={verb[-2:]}")
    features.append(f"END3={verb[-3:]}" if verb_len >= 3 else f"END3={verb}")

    features.append(f"START={verb[:2]}")
    features.append(f"START3={verb[:3]}" if verb_len >= 3 else f"START3={verb}")

    features.append(f"LEN={verb_len}")

    # ---------------------------
    # SUFFIX FEATURES (BOOSTED FOR WEAK LANGUAGES)
    # ---------------------------
    max_suf = 7 if weak_lang else 5

    for i in range(2, min(max_suf, verb_len + 1)):
        features.append(f"SUF{i}={verb[-i:]}")

    # extra suffix emphasis for RO/IT
    if weak_lang:
        features.append(f"SUF_LONG={verb[-6:] if verb_len >= 6 else verb}")

    # ---------------------------
    # PREFIX FEATURES
    # ---------------------------
    for i in range(2, min(5, verb_len + 1)):
        features.append(f"PREF{i}={verb[:i]}")

    # ---------------------------
    # PHONETIC FEATURES
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
    # STRUCTURE SIGNAL (LIGHTWEIGHT ONLY)
    # ---------------------------
    has_double = any(verb[i] == verb[i + 1] for i in range(len(verb) - 1))
    features.append(f"HAS_DOUBLE={has_double}")

    # ---------------------------
    # INTERNAL PATTERN (REDUCED NOISE VERSION)
    # ---------------------------
    # Only for weak languages to avoid hurting FR/ES/PT
    if weak_lang:
        for i in range(0, len(verb) - 2, 2):  # sparse sampling instead of full bigrams
            features.append(f"BI_{verb[i:i+2]}")

    return features


if __name__ == "__main__":
    pass
