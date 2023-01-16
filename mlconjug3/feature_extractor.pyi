# Stub files for mlconjug3.feature_extractor

from sklearn.base import BaseEstimator, TransformerMixin

class VerbFeatures(TransformerMixin, BaseEstimator):
    def __init__(self, char_ngrams=None, w2v_model=None, morph_features=None, language:str='fr'):
        pass
      
    def fit(self, X, y=None):
        pass

    def transform(self, X, y=None):
        pass
    
    @staticmethod   
    def extract_verb_features(verb:str, lang:str, ngram_range:Tuple):
        pass

      
class VerbMorphology:
    def __init__(self, language:str):
        pass
  
    def transform(self, X):
        pass
      
      
class VerbMorphologyFr(VerbMorphology):
    def extract_verb_prefix(self, verb:str) -> str:
        pass
      
    def extract_verb_suffix(self, verb:str) -> str:
        pass


class VerbMorphologyEn(VerbMorphology):
    def extract_verb_prefix(self, verb:str) -> str:
        pass
      
    def extract_verb_suffix(self, verb:str) -> str:
        pass

      
class VerbMorphologyEs(VerbMorphology):
    def extract_verb_prefix(self, verb:str) -> str:
        pass
      
    def extract_verb_suffix(self, verb:str) -> str:
        pass
      
      
class VerbMorphologyIt(VerbMorphology):
    def extract_verb_prefix(self, verb:str) -> str:
        pass
      
    def extract_verb_suffix(self, verb:str) -> str:
        pass
      
      
      
class VerbMorphologyPt(VerbMorphology):
    def extract_verb_prefix(self, verb:str) -> str:
        pass
      
    def extract_verb_suffix(self, verb:str) -> str:
        pass
      
         
class VerbMorphologyRoVerbMorphology):
    def extract_verb_prefix(self, verb:str) -> str:
        pass
      
    def extract_verb_suffix(self, verb:str) -> str:
        pass
