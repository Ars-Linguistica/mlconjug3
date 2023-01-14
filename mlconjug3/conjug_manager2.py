import json
import re
from collections import defaultdict
from functools import partial
from typing import Tuple
from joblib import Memory

class ConjugManager:
    """
    This is the class handling the mlconjug3 json files.
        :param language: string.
            | The language of the conjugator. The default value is fr for French.
            | The allowed values are: fr, en, es, it, pt, ro.
        :ivar language: Language of the conjugator.
        :ivar verbs: Dictionary where the keys are verbs and the values are conjugation patterns.
        :ivar conjugations: Dictionary where the keys are conjugation patterns and the values are inflected forms.
    """

    def __init__(self, language='fr', pre_trained_models, extract_verb_features):
        if language not in _LANGUAGES:
            raise ValueError(_('Unsupported language.\nThe allowed languages are fr, en, es, it, pt, ro.'))
        self.language = language
        self.verbs = {}
        self.conjugations = OrderedDict()
        self._allowed_endings = self._detect_allowed_endings()
        self.pre_trained_models = pre_trained_models
        self.extract_verb_features = extract_verb_features
        self.cache = Memory(cachedir='/path/to/cache', verbose=0)

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
        | If the verb is invalid, returns alse, otherwise returns the base form of the verb.
            :param verb: string.
        The verb to be checked.
    :return: string or bool.
        Returns the base form of the verb if valid, False otherwise.

    """
    if self.language == 'en':
        return verb
    base_form = self.verbs.get(verb, None)
    if not base_form:
        logger.warning("The verb '{}' is not a valid verb in the {} language.".format(verb, _LANGUAGE_FULL[self.language]))
        return False
    return base_form

def conjugate(self, verb, subject='abbrev'):
    """
    | Conjugates a given verb in the target language.
    | The conjugation is done using a pre-trained machine learning model, based on the verb's base form.
    | The result is a ConjugationInfo object, containing the conjugated forms of the verb.

    :param verb: string.
        The verb to be conjugated.
    :param subject: string.
        The subject format type for the conjugated forms.
        The values can be 'abbrev' or 'pronoun'. The default value is 'abbrev'.
    :return: ConjugationInfo.
        A ConjugationInfo object, containing the conjugated forms of the verb.

    """
    base_form = self.cache.cache(is_valid_verb)(self, verb)
    if not base_form:
        return False
    conjug_pattern = self.verbs[base_form]
    conjug_info = self.conjugations.get(conjug_pattern, None)
    if not conjug_info:
        logger.warning("The conjugation pattern '{}' is not supported by the {} language.".format(conjug_pattern, _LANGUAGE_FULL[self.language]))
        return False
    conjug_info = ConjugationInfo(base_form, conjug_info, subject)
    return conjug_info
    
    def conjugate(self, verb, subject='abbrev'):
        """
        | Conjugates a given verb in the target language.
        | The conjugation is done using a pre-trained machine learning model, based on the verb's base form.
        | The result is a ConjugationInfo object, containing the conjugated forms of the verb.

        :param verb: string.
            The verb to be conjugated.
        :param subject: string.
            The subject format type for the conjugated forms.
            The values can be 'abbrev' or 'pronoun'. The default value is 'abbrev'.
        :return: ConjugationInfo.
            A ConjugationInfo object, containing the conjugated forms of the verb.

        """
        base_form = self.cache.cache(is_valid_verb)(self, verb)
        if not base_form:
            return False
        conjug_pattern = self.verbs[base_form]
        conjug_info = self.conjugations.get(conjug_pattern, None)
        if not conjug_info:
            logger.warning("The conjugation pattern '{}' is not supported by the {} language.".format(conjug_pattern, _LANGUAGE_FULL[self.language]))
            return False
        conjug_info = ConjugationInfo(base_form, conjug_info, subject)
        return conjug_info

    def conjugate_multiple(self, verbs, subject='abbrev'):
        """
        | Conjugates multiple verbs at once.
        :param verbs: list of strings.
            The verbs to be conjugated.
        :param subject: string.
            The subject format type for the conjugated forms.
            The values can be 'abbrev' or 'pronoun'. The default value is 'abbrev'.
        :return: dict of ConjugationInfo objects.
            A dictionary where the keys are the base forms of the verbs, and the values are ConjugationInfo objects.

        """
        conjugations = self.cache.cache(map, ignore=['subject'])(self.conjugate, verbs, [subject]*len(verbs))
        return {base_form: conjug_info for base_form, conjug_info in zip(verbs, conjugations) if conjug_info}

    def conjugate_random(self, subject='abbrev', sample_size=10):
        """
        | Conjugates a random set of verbs.
        :param subject: string.
            The subject format type for the conjugated forms.
            The values can be 'abbrev' or 'pronoun'. The default value is 'abbrev'.
        :param sample_size: int.
            The number of verbs to be conjugated.
        :return: dict.
            A dictionary where the keys are the infinitive forms of the verbs and the values are the conjugated forms.
        """
        rnd = Random()
        verbs = rnd.sample(self.verbs.keys(), sample_size)
        return self.conjugate_batch(verbs, subject)

