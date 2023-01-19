from sklearn.base import BaseEstimator, TransformerMixin
from .verbs import *
from .constants import *
from .utils import logger
import numpy as np
import re

class VerbFeatures(TransformerMixin, BaseEstimator):
    """
    Transformer to extract verb features using multiple techniques:
    - Character n-grams
    - Word2Vec embeddings
    - Morphological features
    """

    def __init__(self, char_ngrams=None, w2v_model=None, morph_features=None, language='fr'):
        self.char_ngrams = char_ngrams
        self.w2v_model = w2v_model
        self.morph_features = morph_features
        self.language = language

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        features = []
        for verb in X:
            feature_vector = []
            
            # Use custom vectorizer
            feature_vector.extend(VerbFeatures.extract_verb_features(verb, self.language, (2, 7)))

            # Extract character n-grams
            if self.char_ngrams:
                char_ngrams = [verb[i:i+n] for n in self.char_ngrams for i in range(len(verb)-n+1)]
                feature_vector.extend(char_ngrams)

            # Extract Word2Vec embeddings
            if self.w2v_model:
                try:
                    embeddings = self.w2v_model[verb]
                    feature_vector.extend(embeddings)
                except KeyError:
                    pass

            # Extract morphological features
            if self.morph_features:
                morph_extractor = {
                    'fr': VerbMorphologyFr(),
                    'en': VerbMorphologyEn(),
                    'es': VerbMorphologyEs(),
                    'it': VerbMorphologyIt(),
                    'pt': VerbMorphologyPt(),
                    'ro': VerbMorphologyRo(),
                }.get(self.language)
                feature_vector.extend(morph_extractor.transform([verb]))

            features.append(feature_vector)
        return np.array(features)
        
    @staticmethod   
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
        :return: list.
            List of the most salient features of the verb for the task of finding it's conjugation's class.
        """
        _white_spaces = re.compile(r"\s\s+")
        verb = _white_spaces.sub(" ", verb)
        verb = verb.lower()
        verb_len = len(verb)
        length_feature = 'LEN={0}'.format(str(verb_len))
        min_n, max_n = ngram_range
        final_ngrams = ['END={0}'.format(verb[-n:]) for n in range(min_n, min(max_n + 1, verb_len + 1))]
        initial_ngrams = ['START={0}'.format(verb[:n]) for n in range(min_n, min(max_n + 1, verb_len + 1))]
        if lang not in _ALPHABET:
            lang = 'en'  # We chose 'en' as the default alphabet because english is more standard, without accents or diactrics.
        vowels = sum(verb.count(c) for c in _ALPHABET[lang]['vowels'])
        vowels_number = 'VOW_NUM={0}'.format(vowels)
        consonants = sum(verb.count(c) for c in _ALPHABET[lang]['consonants'])
        consonants_number = 'CONS_NUM={0}'.format(consonants)
        if consonants == 0:
            vow_cons_ratio = 'V/C=N/A'
        else:
            vow_cons_ratio = 'V/C={0}'.format(round(vowels / consonants, 2))
        final_ngrams.extend(initial_ngrams)
        final_ngrams.extend((length_feature, vowels_number, consonants_number, vow_cons_ratio))
        return final_ngrams

