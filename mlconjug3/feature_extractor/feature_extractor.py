"""
This module declares the feature extractors for verbs.

A custom vectorizer optimized for extracting verb features,
including n-grams of verb endings and beginnings, verb length,
number of vowels and consonants, and ratio of vowels to consonants.
"""

import re
from mlconjug3.constants import ALPHABET


def extract_verb_features(verb, lang, ngram_range):
    """
    | Custom Vectorizer optimized for extracting verbs features.
    | As in Indo-European languages verbs are inflected by adding a morphological suffix,
     the vectorizer extracts verb endings and produces a vector representation of the verb with binary features.
    | To enhance the results of the feature extration, several other features have been included:
    | The features are the verb's ending n-grams, starting n-grams, length of the verb, number of vowels,
     number of consonants and the ratio of vowels over consonants.
     
    :param verb: string.
        Verb to vectorize.
    :param lang: string.
        Language to analyze.
    :param ngram_range: tuple.
        The range of the ngram sliding window.
    :return features: list.
        List of the most salient features of the verb for the task of finding it's conjugation's class.
    """
    _white_spaces = re.compile(r"\s\s+")
    verb = _white_spaces.sub(" ", verb)
    verb = verb.lower()
    verb_len = len(verb)
    length_feature = 'LEN={}'.format(str(verb_len))
    min_n, max_n = ngram_range
    final_ngrams = ['END={}'.format(verb[-n:]) for n in range(min_n, min(max_n + 1, verb_len + 1))]
    initial_ngrams = ['START={}'.format(verb[:n]) for n in range(min_n, min(max_n + 1, verb_len + 1))]
    if lang not in ALPHABET:
        lang = 'en'  # We chose 'en' as the default alphabet because english is more standard, without accents or diactrics.
    vowels = sum(verb.count(c) for c in ALPHABET[lang]['vowels'])
    vowels_number = 'VOW_NUM={}'.format(vowels)
    consonants = sum(verb.count(c) for c in ALPHABET[lang]['consonants'])
    consonants_number = 'CONS_NUM={}'.format(consonants)
    if consonants == 0:
        vow_cons_ratio = 'V/C=N/A'
    else:
        vow_cons_ratio = 'V/C={}'.format(round(vowels / consonants, 2))
    final_ngrams.extend(initial_ngrams)
    final_ngrams.extend((length_feature, vowels_number, consonants_number, vow_cons_ratio))
    return final_ngrams
  
if __name__ == "__main__":
    pass
