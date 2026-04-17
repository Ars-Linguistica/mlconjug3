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
    - ngram_range is ignored (sklearn handles n-grams)
    """

    _white_spaces = re.compile(r"\s\s+")
    verb = _white_spaces.sub(" ", verb).lower()

    if not verb:
        return []

    verb_len = len(verb)
    features = []

    # ---------------------------
    # BASE MORPHOLOGY (GLOBAL)
    # ---------------------------
    features.append(f"END={verb[-2:]}")
    features.append(f"END3={verb[-3:]}" if verb_len >= 3 else f"END3={verb}")

    features.append(f"START={verb[:2]}")
    features.append(f"START3={verb[:3]}" if verb_len >= 3 else f"START3={verb}")

    features.append(f"LEN={verb_len}")

    # Strong suffix hierarchy
    for i in range(2, min(7, verb_len + 1)):
        features.append(f"SUF{i}={verb[-i:]}")

    # =========================================================
    # 🇮🇹 ITALIAN TARGETED FEATURES
    # =========================================================
    if lang == "it":

        ends_are = verb.endswith("are")
        ends_ere = verb.endswith("ere")
        ends_ire = verb.endswith("ire")

        features.append(f"IT_ARE={ends_are}")
        features.append(f"IT_ERE={ends_ere}")
        features.append(f"IT_IRE={ends_ire}")

        # -isc verbs (key signal)
        features.append(f"IT_ISC={'isc' in verb[-6:]}")

        # stem variability
        features.append(f"IT_STEM_VAR={len(set(verb[:3]))}")

        # vowel structure
        vowels_it = sum(verb.count(c) for c in "aeiou")
        features.append(f"IT_VOWELS={vowels_it}")
        features.append(f"IT_VOWEL_RATIO={round(vowels_it / max(1, verb_len), 3)}")

        # suffix tension (helps separate similar endings)
        features.append(f"IT_SUFFIX_TENSION={verb[-1] + verb[-2:]}")

    # =========================================================
    # 🇷🇴 ROMANIAN TARGETED FEATURES
    # =========================================================
    if lang == "ro":

        features.append(f"RO_IZA={verb.endswith('iza')}")
        features.append(f"RO_IFICA={verb.endswith('ifica')}")
        features.append(f"RO_UI={verb.endswith('ui')}")
        features.append(f"RO_A_VERB={verb.endswith('a')}")

        # derived verbs cluster (key for template 105)
        features.append(
            f"RO_DERIV_CHAIN={'iza' in verb or 'fica' in verb or 'ui' in verb}"
        )

        # complexity signal
        features.append(f"RO_COMPLEXITY={len(set(verb)) + verb_len}")

        # suffix entropy proxy
        features.append(f"RO_SUFFIX3={verb[-3:]}")

        # vowel duplication signal
        features.append(
            f"RO_DOUBLE_VOWEL={'aa' in verb or 'ee' in verb or 'ii' in verb}"
        )

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
    # STRUCTURE FEATURES
    # ---------------------------
    features.append(
        f"HAS_DOUBLE={any(verb[i] == verb[i + 1] for i in range(len(verb) - 1))}"
    )

    return features


if __name__ == "__main__":
    pass
