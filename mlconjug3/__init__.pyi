from typing import Tuple
from joblib import Memory

class ConjugManager:

    def __init__(self, pre_trained_models: dict, extract_verb_features: dict, language: str = 'fr'):
        pass
    
    def _load_verbs(self, verbs_file: str):
        pass

    def _load_conjugations(self, conjugations_file: str):
        pass

    def _detect_allowed_endings(self):
        pass

    def is_valid_verb(self, verb: str):
        pass

class VerbFeatures(TransformerMixin, BaseEstimator):

    def __init__(self, char_ngrams: dict, w2v_model: dict, morph_features: dict, language: str = 'fr'):
        pass
        
    def fit(self, X, y=None):
        pass

    def transform(self, X, y=None):
        pass

    @staticmethod   
    def extract_verb_features(verb: str, lang: str, ngram_range: Tuple[int, int]):
        pass

def _get_user_locale():
    pass

def _getdoc(obj):
    pass
