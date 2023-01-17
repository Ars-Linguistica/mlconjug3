import abc
import json
import re
from collections import defaultdict
from functools import partial
from typing import Tuple
from joblib import Memory
import hashlib
import os
import pickle

class VerbFeaturesBase(abc.ABC):
    """
    Base class for verb feature extractors.
    """
    @abc.abstractmethod
    def extract_verb_features(self, verb, lang, ngram_range):
        pass

class VerbFeatures(VerbFeaturesBase):
    """
    Transformer to extract verb features using multiple techniques:
    - Character n-grams
    - Word2Vec embeddings
    - Morphological features
    """

    def __init__(self, char_ngrams=None, w2v_model=None, morph_features=None, language='fr', feature_extractors=[]):
        self.char_ngrams = char_ngrams
        self.w2v_model = w2v_model
        self.morph_features = morph_features
        self.language = language
        self.feature_extractors = feature_extractors

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
                # char_ngrams = [verb[i:i+n] for n in self.char_ngrams for i in range(len
