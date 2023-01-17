import re
from collections import defaultdict
from functools import partial
from typing import Tuple
from joblib import Memory
import hashlib
import os
import json
import re

from .mlconjug import *
from .constants import *
from .verbs import *

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        else:
            json_file = "conjugation_data/{}_verbs.json".format(cls._instances[cls].language)
            json_hash = hashlib.sha256(open(json_file, "rb").read()).hexdigest()
            if json_hash != cls._instances[cls].cache.get(json_file)["hash"]:
                cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class ConjugManager(metaclass=Singleton):
    """
    This is the class handling the mlconjug3 json files.
    :param language: string.
    | The language of the conjugator. The default value is fr for French.
    | The allowed values are: fr, en, es, it, pt, ro.
    :ivar language: Language of the conjugator.
    :ivar verbs: Dictionary where the keys are verbs and the values are conjugation patterns.
    :ivar conjugations: Dictionary where the keys are conjugation patterns and the values are inflected forms.
    """
    def init(self, language='fr', extract_verb_features=None, pre_trained_models=None):
        if language not in LANGUAGES:
            raise ValueError(('Unsupported language.\nThe allowed languages are fr, en, es, it, pt, ro.'))
        self.language = language
        self.verbs = {}
        self.conjugations = OrderedDict()
        self._allowed_endings = self._detect_allowed_endings()
        self.pre_trained_models = pre_trained_models
        self.extract_verb_features = extract_verb_features
        self.cache = Memory(location= './cachedir', verbose=0)
        self._load_verbs()
        self._load_conjugations()

    def __repr__(self):
        return '{0}.{1}(language={2})'.format(__name__, self.__class__.__name__, self.language)
    
    def _load_verbs(self):
        """
        Load and parses the verbs from the json file.
    
        :param verbs_file: string or path object.
            Path to the verbs json file.
    
        """
        json_file = "conjugation_data/{}_verbs.json".format(self.language)
        json_hash = hashlib.sha256(open(json_file, "rb").read()).hexdigest()
        
        if self.cache.get(json_file) and json_hash == self.cache.get(json_file)["hash"]:
            self.verbs = self.cache.get(json_file)["data"]
        else:
            with open(json_file, 'r', encoding='utf-8') as file:
                self.verbs = json.load(file)
                self.cache.set(json_file, {"hash":json_hash, "data":self.verbs})
        return
    
    def _load_conjugations(self):
        """
        Load and parses the conjugations from the json file.
        """
        json_file = "conjugation_data/{}_conjugations.json".format(self.language)
        json_hash = hashlib.sha256(open(json_file, "rb").read()).hexdigest()
        if self.cache.get(json_file) and json_hash == self.cache.get(json_file)["hash"]:
            self.conjugations = self.cache.get(json_file)["data"]
        else:
            with open(json_file, 'r', encoding='utf-8') as file:
                self.conjugations = json.load(file)
                self.cache.set(json_file, {"hash":json_hash, "data":self.conjugations})
        return
    
    def _detect_allowed_endings(self):
        """
        Detects the allowed verb endings from the conjugations json file.
        """
        allowed_endings = set()
        for conj in self.conjugations.values():
            for ending in conj['allowed_endings']:
                allowed_endings.add(ending)
        return allowed_endings
    
    def _get_verb_template(self, infinitive):
        """
        Returns the conjugation pattern of a verb.
        """
        infinitive = infinitive.lower()
        if infinitive in self.verbs:
            return self.verbs[infinitive]['template']
        else:
            for ending in self._allowed_endings:
                if infinitive.endswith(ending):
                    return self._detect_verb_template(infinitive)
        return None

    
