import re
from collections import defaultdict
from functools import partial
from typing import Tuple
from joblib import Memory
import hashlib
import os
import json
import re
import copy

from .mlconjug import *
from .constants import *
from .verbs import *
from .utils import logger


class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        # else:
            # json_file = "conjugation_data/{}_verbs.json".format(cls._instances[cls].language)
            # json_hash = hashlib.sha256(open(json_file, "rb").read()).hexdigest()
            # if json_hash != cls._instances[cls].cache.get(json_file)["hash"]:
                # cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
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
    def __init__(self, language='fr', extract_verb_features=None, pre_trained_models=None):
        if language not in SUPPORTED_LANGUAGES:
            raise ValueError(('Unsupported language.\nThe allowed languages are fr, en, es, it, pt, ro.'))
        self.language = language
        self.verbs = {}
        verbs_file = pkg_resources.resource_filename(RESOURCE_PACKAGE, VERBS_RESOURCE_PATH[self.language])
        conjugations_file = pkg_resources.resource_filename(RESOURCE_PACKAGE,
                                                            CONJUGATIONS_RESOURCE_PATH[self.language])
        self.conjugations = OrderedDict()
        self.pre_trained_models = pre_trained_models
        self.extract_verb_features = extract_verb_features
        self.cache = Memory(location= './cachedir', verbose=0)
        self._load_verbs(verbs_file)
        self._allowed_endings = self._detect_allowed_endings()
        self._load_conjugations(conjugations_file)
        self.templates = sorted(self.conjugations.keys())

    def __repr__(self):
        return '{0}.{1}(language={2})'.format(__name__, self.__class__.__name__, self.language)
    
    def _load_verbs(self, verbs_file):
        """
        Load and parses the verbs from the json file.
        :param verbs_file: string or path object.
            Path to the verbs json file.
        """
        with open(verbs_file, 'r', encoding='utf-8') as file:
            self.verbs = json.load(file)
        return

    def _load_conjugations(self, conjugations_file):
        """
        Load and parses the conjugations from the json file.
        :param conjugations_file: string or path object.
            Path to the conjugation json file.
        """
        with open(conjugations_file, 'r', encoding='utf-8') as file:
            self.conjugations = json.load(file)
        return
    
    def _detect_allowed_endings(self):
        """
        | Detects the allowed endings for verbs in the supported languages.
        | All the supported languages except for English restrict the form a verb can take.
        | As English is much more productive and varied in the morphology of its verbs, any word is allowed as a verb.
        :return: set.
            A set containing the allowed endings of verbs in the target language.
        """
        if self.language == 'en':
            return True
        return {verb.split(' ')[0][-2:] for verb in self.verbs if len(verb) >= 2}
    
    def is_valid_verb(self, verb):
        """
        | Checks if the verb is a valid verb in the given language.
        | English words are always treated as possible verbs.
        | Verbs in other languages are filtered by their endings.
        :param verb: string.
            The verb to conjugate.
        :return: bool.
            True if the verb is a valid verb in the language. False otherwise.
        """
        if self.language == 'en':
            return True  # LOL!
        return verb[-2:] in self._allowed_endings
    
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
    
    def get_verb_info(self, verb):
        """
        Gets verb information and returns a VerbInfo instance.
        :param verb: string.
            Verb to conjugate.
        :return: VerbInfo object or None.
        """
        if verb not in self.verbs.keys():
            return None
        infinitive = verb
        root = self.verbs[verb]['root']
        template = self.verbs[verb]['template']
        return VerbInfo(infinitive, root, template)

    def get_conjug_info(self, template):
        """
        Gets conjugation information corresponding to the given template.
        :param template: string.
            Name of the verb ending pattern.
        :return: OrderedDict or None.
            OrderedDict containing the conjugated suffixes of the template.
        """
        if template not in self.conjugations.keys():
            return None
        return copy.deepcopy(self.conjugations[template])

    
