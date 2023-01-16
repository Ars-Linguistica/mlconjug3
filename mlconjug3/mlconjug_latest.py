# -*- coding: utf-8 -*-

"""
MLConjug Main module.

| This module declares the main classes the user interacts with.

| The module defines the classes needed to interface with Machine Learning models.

"""

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

# Added for backward compatibility.
extract_verb_features = VerbFeatures.extract_verb_features


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
    :param feature_extractor: Feature extractor class implementing the fit() and transform() methods.
        A user provided feature extractor class.
    :param classifier: Classifier class implementing the fit() and predict() methods.
        A user provided classifier class.
    :ivar language: string. Language of the conjugator.
    :ivar model: mlconjug3.Model or scikit-learn Pipeline or Classifier implementing the fit() and predict() methods.
    :ivar conjug_manager: Verbiste object.

    """

    def __init__(self, language='fr', model=None, feature_extractor=None, classifier=None):
        self.language = language
        self.conjug_manager = Verbiste(language=language)
        if model:
            self.model = model 
        else:
            self.model = self._load_default_model(feature_extractor, classifier)

    def _load_default_model(self, feature_extractor=None, classifier=None):
        if self.model:
            return self.model
        else:
            with ZipFile(pkg_resources.resource_stream(
                _RESOURCE_PACKAGE, _PRE_TRAINED_MODEL_PATH[self.language])) as content:
                    with content.open('trained_model-{0}-final.pickle'.format(self.language), 'r') as archive:
                        model = joblib.load(archive)
        if feature_extractor:
            model.steps[0][1] = feature_extractor
        if classifier:
        model.steps[-1][1] = classifier
        return model
        
    def __repr__(self):
        return '{0}.{1}(language={2})'.format(__name__, self.__class__.__name__, self.language)
    
    def set_model(self, model):
        self.model = model
    
    def conjugate(self, verb, subject='abbrev'):
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
        prediction_score = self.model.predict_proba([verb])
        prediction = self.model.predict([verb])
        prediction = int(prediction[0])
        prediction_score = prediction_score[0][prediction]
        try:
            return self.conjug_manager.get_conjug(verb, prediction, subject=subject, score=prediction_score)
        except ValueError:
            return None
