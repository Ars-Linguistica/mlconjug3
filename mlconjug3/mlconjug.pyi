# Stubs for mlconjug3.mlconjug (Python 3)

from .__init__ import Pipeline, SelectFromModel, CountVectorizer, LinearSVC, SGDClassifier
from .constants import *
from .PyVerbiste import Verbiste
from .conjug_manager import ConjugManager
from .verbs import *
from .utils import logger
from .feature_extractor import VerbFeatures

from random import Random
from collections import defaultdict
import joblib
import pkg_resources
import re
from zipfile import ZipFile
from functools import partial

from typing import List, Union

class Conjugator:
    def __init__(self, language:str='fr', model=None, feature_extractor=None):
        pass
    
    def __repr__(self) -> str:
        pass
    
    def _load_default_model(self, feature_extractor=None, classifier=None) -> Pipeline:
        pass

    def set_model(self, model:Pipeline):
        pass
    
    def conjugate(self, verb:str, subject:str='abbrev') -> Verb:
        pass
    
    def conjugate_multi(self, verbs:List[str], subject='abbrev'):
        pass


class Model:
    def init(self, pipeline:Pipeline, feature_extractor=None, classifier=None, verb_data:List[str], verb_classes:List[str], verb_mapping:List[str], language:str):
        pass
 
    def save(self, output:str) -> None:
        pass

    def train(self, verb_data:List[str], verb_classes:List[str], verb_mapping:List[str]) -> None:
        pass

    def evaluate(self, verb_data:List[str], verb_classes:List[str]) -> dict:
        pass

    def predict(self, verb:str) -> str:
        pass

    def predict_multiple(self, verbs:List[str]) -> List[str]:
        pass

    def test(self, verb_data:List[str], verb_classes:List[str]) -> Union[str, dict]:
        pass

    
class DataSet:
    def init(self, language: str, data: Union[str, List[str]]):
        pass
  
    def load_data(self, data: Union[str, List[str]]):
        pass

    def save_data(self, file_path: str):
        pass
    
    def preprocess_data(self):
        pass
    
    def get_data(self) -> List[str]:
        pass
    
    def get_language(self) -> str:
        pass
    
    def __len__(self) -> int:
        pass
    
    def __getitem__(self, index: int) -> str:
        pass
    
    def __iter__(self):
        pass
