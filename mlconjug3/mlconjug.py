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
    :ivar language: string. Language of the conjugator.
    :ivar model: mlconjug3.Model or scikit-learn Pipeline or Classifier implementing the fit() and predict() methods.
    :ivar conjug_manager: Verbiste object.

    """

    def __init__(self, language='fr', model=None):
        self.language = language
        self.conjug_manager = Verbiste(language=language)
        self.model = model if model else self._load_default_model()

    def _load_default_model(self):
        with ZipFile(pkg_resources.resource_stream(
                _RESOURCE_PACKAGE, _PRE_TRAINED_MODEL_PATH[self.language])) as content:
            with content.open('trained_model-{0}-final.pickle'.format(self.language), 'r') as archive:
                return joblib.load(archive)

    def __repr__(self):
        return '{0}.{1}(language={2})'.format(__name__, self.__class__.__name__, self.language)

    def set_model(self, model):
        self.model = model
    
    def conjugate(self, verb, subject='abbrev'):
        verb = verb.lower()
        verb_info = self.conjug_manager.get_verb(verb)
        if not verb_info:
            return None
        
        if self.model:
            verb_features = extract_verb_features(verb_info)
            conjug_class = self.model.predict([verb_features])[0]
            conjug_info = self.conjug_manager.get_conjug(verb_info.infinitive, conjug_class)
            predicted = True
        else:
            conjug_info = self.conjug_manager.get_conjug(verb_info.infinitive)
            predicted = False

        if self.language == 'fr':
            verb_obj = VerbFr(verb_info, conjug_info, subject, predicted)
        else:
            verb_obj = Verb(verb_info, conjug_info, subject, predicted)
        return verb_obj

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


class DataSet:
    """
    | This class holds and manages the data set.
    | Defines helper methodss for managing Machine Learning tasks like constructing a training and testing set.

    :param verbs_dict:
        A dictionary of verbs and their corresponding conjugation class.

    """

    def __init__(self, verbs_dict):
        self.verbs_dict = verbs_dict
        self.verbs = self.verbs_dict.keys()
        self.templates = sorted(
            {verb['template'] for verb in self.verbs_dict.values()}
        )

        self.verbs_list = []
        self.templates_list = []
        self.dict_conjug = None
        self.min_threshold = 8
        self.split_proportion = 0.5
        self.train_input = []
        self.train_labels = []
        self.test_input = []
        self.test_labels = []
        self.construct_dict_conjug()
        return

    def __repr__(self):
        return '{0}.{1}()'.format(__name__, self.__class__.__name__)

    def construct_dict_conjug(self):
        """
        | Populates the dictionary containing the conjugation templates.
        | Populates the lists containing the verbs and their templates.

        """
        conjug = defaultdict(list)
        verb_items = list(self.verbs_dict.items())
        Random(42).shuffle(verb_items)
        for verb, info_verb in verb_items:
            self.verbs_list.append(verb)
            self.templates_list.append(self.templates.index(info_verb["template"]))
            conjug[info_verb["template"]].append(verb)
        self.dict_conjug = conjug
        return

    def split_data(self, threshold=8, proportion=0.5):
        """
        Splits the data into a training and a testing set.

        :param threshold: int.
            Minimum size of conjugation class to be split.
        :param proportion: float.
            Proportion of samples in the training set.
            Must be between 0 and 1.
        :raises: ValueError.

        """
        if proportion <= 0 or proportion > 1:
            raise ValueError(_('The split proportion must be between 0 and 1.'))
        self.min_threshold = threshold
        self.split_proportion = proportion
        train_set = []
        test_set = []
        for template, lverbs in self.dict_conjug.items():
            if len(lverbs) <= threshold:
                for verbe in lverbs:
                    train_set.append((verbe, template))
            else:
                index = round(len(lverbs) * proportion)
                for verbe in lverbs[:index]:
                    train_set.append((verbe, template))
                for verbe in lverbs[index:]:
                    test_set.append((verbe, template))
        Random(42).shuffle(train_set)
        Random(42).shuffle(test_set)
        self.train_input = [elmt[0] for elmt in train_set]
        self.train_labels = [self.templates.index(elmt[1]) for elmt in train_set]
        self.test_input = [elmt[0] for elmt in test_set]
        self.test_labels = [self.templates.index(elmt[1]) for elmt in test_set]
        return


class Model:
    """
    | This class wraps the scikit-learn pipeline.
    | The pipeline is used to train the model and predict the conjugation class of a verb.
    | The pipeline is composed of:
    |   - a feature extractor,
    |   - a feature selector using Linear Support Vector Classification,
    |   - a classifier using Stochastic Gradient Descent.
    :param feature_extractor: a class that implements the fit and transform methods.
    Instance of a class that implements the fit and transform methods.
    :param pipeline: scikit-learn pipeline.
        Pipeline containing the feature extraction and the classification steps.
    :param feature_extractor_params: dict.
        Parameters for the feature extractor.
    :param pipeline_params: dict.
        Parameters for the pipeline.
    :param lang: string.
        Language of the conjugator. The default language is 'fr' for french.
    :param ngram_range: tuple.
        The range of the ngram sliding window.
    
    """
    def __init__(self, feature_extractor=None, pipeline=None, feature_extractor_params=None, pipeline_params=None, lang='fr', ngram_range=(1, 2)):
        self.feature_extractor = feature_extractor if feature_extractor else VerbFeatures
        self.feature_extractor_params = feature_extractor_params if feature_extractor_params else {'char_ngrams': (3, 4, 5), 'w2v_model': None, 'morph_features': None, 'language': lang}
        self.pipeline = pipeline if pipeline else Pipeline([
            ('feature_extractor', self.feature_extractor(**self.feature_extractor_params)),
            ('classifier', LinearSVC())
        ])
        self.pipeline_params = pipeline_params if pipeline_params else {'classifier__C': 1.0}
        self.ngram_range = ngram_range
        self.lang = lang
    
    def fit(self, X, y):
        self.pipeline.fit(X, y)
    
    def predict(self, X):
        return self.pipeline.predict(X)
    
    def evaluate(self, X, y):
        return self.pipeline.score(X, y)
    
    def save(self, filepath):
        joblib.dump(self, filepath)
    
    def load(self, filepath):
        return joblib.load(filepath)
    
    @staticmethod
    def extract_verb_features(verb, lang, ngram_range):
        """
        | Custom Vectorizer optimized for extracting verbs features.
        | As in Indo-European languages verbs are inflected by adding a morphological suffix,
        the vector


    


if __name__ == "__main__":
    pass
