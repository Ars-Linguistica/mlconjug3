"""
MLConjug Main module.

| This module declares the main classes the user interacts with.

| The module defines the classes needed to interface with Machine Learning models.

"""

from .PyVerbiste import Verbiste

from .conjug_manager import ConjugManager

from .__init__ import Pipeline, SelectFromModel, CountVectorizer, LinearSVC, SGDClassifier

from .constants import *

from .verbs import *

from .feature_extractor import extract_verb_features

from .dataset import DataSet

from .models import Model

from .utils import logger

from functools import lru_cache
from concurrent.futures import ProcessPoolExecutor
from random import Random
from collections import defaultdict
import joblib
import pkg_resources
import re
from zipfile import ZipFile
from functools import partial


VERBS = {'fr': VerbFr,
          'en': VerbEn,
          'es': VerbEs,
          'it': VerbIt,
          'pt': VerbPt,
          'ro': VerbRo,
          }


class Conjugator:
    """
    | This is the main class of the project.
    | The class manages the Verbiste data set and provides an interface with the scikit-learn pipeline.
    | If no parameters are provided, the default language is set to french and the pre-trained french conjugation pipeline is used.
    | The class defines the method conjugate(verb, language) which is the main method of the module.

    :param language: string.
        Language of the conjugator. The default language is 'fr' for french.
    :param model: mlconjug3.Model or scikit-learn Pipeline or Classifier implementing the fit() and predict() methods.
        A user provided pipeline if the user has trained his own pipeline.
    :ivar language: string. Language of the conjugator.
    :ivar model: mlconjug3.Model or scikit-learn Pipeline or Classifier implementing the fit() and predict() methods.
    :ivar conjug_manager: Verbiste object.

    """

    def __init__(self, language='fr', model=None):
        self.language = language
        self.conjug_manager = Verbiste(language=language)
        if not model:
            with ZipFile(pkg_resources.resource_stream(
                    RESOURCE_PACKAGE, PRE_TRAINED_MODEL_PATH[language])) as content:
                with content.open('trained_model-{}-final.pickle'.format(self.language), 'r') as archive:
                    model = joblib.load(archive)
        if model:
            self.set_model(model)
        else:
            self.model = model
        return

    def __repr__(self):
        return '{}.{}(language={})'.format(__name__, self.__class__.__name__, self.language)

    def conjugate(self, verbs, subject='abbrev'):
        """
        Conjugate multiple verbs using multi-processing.
        :param verbs: list of strings or string.
            Verbs to conjugate.
        :param subject: string.
            Toggles abbreviated or full pronouns.
            The default value is 'abbrev'.
            Select 'pronoun' for full pronouns.
        :return: list of Verb objects or None.
        """
        if isinstance(verbs, str):
            # If only a single verb is passed, call the _conjugate method directly
            return self._conjugate(verbs, subject)
        else:
            with ProcessPoolExecutor() as executor:
                results = list(executor.map(self._conjugate, verbs, [subject]*len(verbs)))
            return results
    
    @lru_cache(maxsize=1024)
    def _conjugate(self, verb, subject='abbrev'):
        """
        | This is the main method of this class.
        | It first checks to see if the verb is in Verbiste.
        | If it is not, and a pre-trained scikit-learn pipeline has been supplied, the method then calls the pipeline
         to predict the conjugation class of the provided verb.

        | Returns a Verb object or None.

        :param verb: string.
            Verb to conjugate.
        :param subject: string.
            Toggles abbreviated or full pronouns.
            The default value is 'abbrev'.
            Select 'pronoun' for full pronouns.
        :return: Verb object or None.
        :raises: ValueError.

        """
        verb = verb.lower()
        prediction_score = 0
        if not self.conjug_manager.is_valid_verb(verb):
            raise ValueError(
                _('The supplied word: {0} is not a valid verb in {1}.').format(verb, LANGUAGE_FULL[self.language]))
        if verb not in self.conjug_manager.verbs.keys():
            if self.model is None:
                logger.warning(_('Please provide an instance of a mlconjug3.mlconjug3.Model'))
                raise ValueError(
                _('The supplied word: {0} is not in the conjugation {1} table and no Conjugation Model was provided.').format(
                    verb, LANGUAGE_FULL[self.language]))
            
            prediction = self.model.predict([verb])[0]
            prediction_score = self.model.pipeline.predict_proba([verb])[0][prediction]
            predicted = True
            template = self.conjug_manager.templates[prediction]
            index = - len(template[template.index(":") + 1:])
            root = verb if index == 0 else verb[:index]
            verb_info = VerbInfo(verb, root, template)
            conjug_info = self.conjug_manager.get_conjug_info(verb_info.template)
        else:
            predicted = False
            infinitive = verb
            verb_info = self.conjug_manager.get_verb_info(infinitive)
            if verb_info is None:
                return None
            conjug_info = self.conjug_manager.get_conjug_info(verb_info.template)
            if conjug_info is None:
                return None
        if predicted:
            verb_object = VERBS[self.language](verb_info, conjug_info, subject, predicted)
            verb_object.confidence_score = round(prediction_score, 3)
        else:
            verb_object = VERBS[self.language](verb_info, conjug_info, subject)

        return verb_object

    def set_model(self, model):
        """
        Assigns the provided pre-trained scikit-learn pipeline to be able to conjugate unknown verbs.

        :param model: scikit-learn Classifier or Pipeline.
        :raises: ValueError.

        """
        if not isinstance(model, Model):
            logger.warning(_('Please provide an instance of a mlconjug3.mlconjug3.Model'))
            raise ValueError
        else:
            self.model = model
        return


if __name__ == "__main__":
    pass
