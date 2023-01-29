"""
ConjugManager.

This module declares the code for the class ConjugManager.

More information about mlconjug3 at https://pypi.org/project/mlconjug3/
The conjugation data conforms to the JSon schema defined by mlconjug3.
"""

__author__ = 'Ars-Linguistica'
__author_email__ = 'diao.sekou.nlp@gmail.com'

import os
import joblib
import copy
import defusedxml.ElementTree as ET
import json
from collections import OrderedDict
import pkg_resources
from mlconjug3.constants import *
from mlconjug3.verbs import *


class ConjugManager:
    """
        This is the class handling the mlconjug3 json files.
        
        :param language: string.
            | The language of the conjugator. The default value is fr for French.
            | The allowed values are: fr, en, es, it, pt, ro.
        :ivar language: Language of the conjugator.
        :ivar verbs: Dictionary where the keys are verbs and the values are conjugation patterns.
        :ivar conjugations: Dictionary where the keys are conjugation patterns and the values are inflected forms.
        :ivar templates: list of string representing the conjugation templates.
        :ivar _allowed_endings: set containing the allowed endings of verbs in the target language.
    """

    def __init__(self, language='default'):
        if language not in LANGUAGES:
            raise ValueError(_('Unsupported language.\nThe allowed languages are fr, en, es, it, pt, ro.'))
        self.language = 'fr' if language == 'default' else language
        self.verbs = {}
        self.conjugations = OrderedDict()
        verbs_file = pkg_resources.resource_filename(RESOURCE_PACKAGE, VERBS_RESOURCE_PATH[self.language])
        self._load_verbs(verbs_file)
        self._allowed_endings = self._detect_allowed_endings()
        conjugations_file = pkg_resources.resource_filename(RESOURCE_PACKAGE,
                                                            CONJUGATIONS_RESOURCE_PATH[self.language])
        self._load_conjugations(conjugations_file)
        self.templates = sorted(self.conjugations.keys())
        return

    def __repr__(self):
        return '{}.{}(language={})'.format(__name__, self.__class__.__name__, self.language)

    def _load_cache(self, file):
        file_path = os.path.abspath(file)
        if not file_path.endswith('.json'):
            raise ValueError(f"Invalid file path, expected .json file, got {file_path}")
        pkl_file = file_path + '.pkl'
        
        if os.path.isfile(pkl_file):
            last_modified_time_file = os.path.getmtime(file_path)
            last_modified_time_pkl = os.path.getmtime(pkl_file)
            if last_modified_time_file <= last_modified_time_pkl:
                file_dic = joblib.load(pkl_file)
                return file_dic
        else:
            return None
    
    def _load_verbs(self, verbs_file):
        """
        Load and parses the verbs from the json file.
        
        :param verbs_file: string or path object.
            Path to the verbs json file.
        """
        cache = self._load_cache(verbs_file)
        if cache:
            self.verbs = cache
        else:
            with open(verbs_file, encoding='utf-8') as file:
                self.verbs = json.load(file)
        return

    def _load_conjugations(self, conjugations_file):
        """
        Load and parses the conjugations from the json file.
        
        :param conjugations_file: string or path object.
            Path to the conjugation json file.
        """
        cache = self._load_cache(conjugations_file)
        if cache:
            self.conjugations = cache
        else:
            with open(conjugations_file, encoding='utf-8') as file:
                self.conjugations = json.load(file)
        return

    def _detect_allowed_endings(self):
        """
        | Detects the allowed endings for verbs in the supported languages.
        | All the supported languages except for English restrict the form a verb can take.
        | As English is much more productive and varied in the morphology of its verbs, any word is allowed as a verb.
        
        :return allowed_endings: set.
            A set containing the allowed endings of verbs in the target language.
        """
        if self.language == 'en':
            return set()
        return {verb.split(' ')[0][-2:] for verb in self.verbs if len(verb) >= 2}

    def is_valid_verb(self, verb):
        """
        | Checks if the verb is a valid verb in the given language.
        | English words are always treated as possible verbs.
        | Verbs in other languages are filtered by their endings.
        :param verb: string.
            The verb to conjugate.
        :return is_allowed: bool.
        
            True if the verb is a valid verb in the language. False otherwise.
        """
        if self.language == 'en':
            return True  # LOL!
        return verb[-2:] in self._allowed_endings

    def get_verb_info(self, verb):
        """
        Gets verb information and returns a VerbInfo instance.
        
        :param verb: string.
            Verb to conjugate.
        :return VerbInfo: VerbInfo object or None.
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
        :return inflected_forms: OrderedDict or None.
            OrderedDict containing the conjugated suffixes of the template.
        """
        if template not in self.conjugations.keys():
            return None
        return copy.deepcopy(self.conjugations[template])
      
      
if __name__ == "__main__":
    pass
