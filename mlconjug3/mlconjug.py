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

    def __init__(self, language='fr', model=None, feature_extractor=None):
        self.language = language
        self.conjug_manager = Verbiste(language=language)
        if model:
            self.model = model 
        elif feature_extractor:
            self.model = self._load_default_model(feature_extractor)
        else:
            self.model = self._load_default_model()
    
    def __repr__(self):
        return '{0}.{1}(language={2})'.format(__name__, self.__class__.__name__, self.language)
    
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
        prediction_score = 0
        if not self.conjug_manager.is_valid_verb(verb):
            raise ValueError(
                _('The supplied word: {0} is not a valid verb in {1}.').format(verb, _LANGUAGE_FULL[self.language]))
        if verb not in self.conjug_manager.verbs.keys():
            if self.model is None:
                logger.warning(_('Please provide an instance of a mlconjug3.mlconjug3.Model'))
                raise ValueError(
                _('The supplied word: {0} is not in the conjugation {1} table and no Conjugation Model was provided.').format(
                    verb, _LANGUAGE_FULL[self.language]))
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
            verb_object = _VERBS[self.language](verb_info, conjug_info, subject, predicted)
            verb_object.confidence_score = round(prediction_score, 3)
        else:
            verb_object = _VERBS[self.language](verb_info, conjug_info, subject)

        return verb_object
        
    def conjugate_multi(self, verbs, subject='abbrev'):
        """
        | This is the main method of this class.
        | It first checks to see if the verb is in Verbiste.
        | If it is not, and a pre-trained scikit-learn pipeline has been supplied, the method then calls the pipeline
         to predict the conjugation class of the provided verb.
        | Returns a list of Verb objects.
        :param verbs: list of strings.
            Verbs to conjugate.
        :param subject: string.
            Toggles abbreviated or full pronouns.
            The default value is 'abbrev'.
            Select 'pronoun' for full pronouns.
        """
        # Check if the verbs are valid
        base_forms = [self.conjug_manager.is_valid_verb(verb) for verb in verbs]
        if any(base_forms):
            base_forms = [base for base in base_forms if base]
        else:
            base_forms = verbs
        # Predict conjugation class
        conjugations = self.model.predict(base_forms)
        conjugations = [self.conjug_manager.conjugations[c] for c in conjugations]
        # Conjugate
        pool = multiprocessing.Pool()
        results = pool.map(partial(conjugate_verb, conjugations, subject), zip(verbs, base_forms, conjugations))
        pool.close()
        pool.join()
        return results
    

class DataSet:
    """
    | This class loads and prepares the dataset for training.
    | The class loads the dataset from a JSON file and prepares the data for training.
    :param language: string.
        Language of the dataset. The default language is 'fr' for french.
    :param split_ratio: float.
        Ratio of the dataset to be used for training. The remaining data is used for testing. Default value is 0.8.
    :param random_state: int.
        Seed for the random generator. Default value is 42.
    :param verb_class: string.
        The class of the verb to be used. Default value is 'verb'.
    :param verb_info_class: string.
        The class of the verb information to be used. Default value is 'verb_info'.
    :ivar data: list.
        List of tuples of verb information, conjugation class and conjugation information.
    :ivar X: list.
        List of verb information used as input for the model.
    :ivar y: list.
        List of conjugation classes used as output for the model.
    
    """
    
    def __init__(self, language='fr', split_ratio=0.8, random_state=42, verb_class='verb', verb_info_class='verb_info'):
        self.language = language
        self.split_ratio = split_ratio
        self.random_state = random_state
        self.verb_class = verb_class
        self.verb_info_class = verb_info_class
        self.data = self._load_data()
        self.X, self.y = self._prepare_data()
    
    def _load_data(self):
        """
        | Loads the dataset from a JSON file.
        | Returns a list of tuples of verb information, conjugation class and conjugation information.
    
        :return: list.
            List of tuples of verb information, conjugation class and conjugation information.
    
        """
        data = []
        with open(_DATASET_PATH[self.language], 'r') as f:
            dataset = json.load(f)
            for verb_info, conjugations in dataset.items():
                for conjugation_class, conjugation_info in conjugations.items():
                    data.append((verb_info, conjugation_class, conjugation_info))
        return data
    
    def _prepare_data(self):
        """
        | Prepares the data for training.
            | Returns X, the input data and y, the output data.
    
        :return: tuple.
            Tuple of X, the input data and y, the output data.
    
        """
        random = Random(self.random_state)
        random.shuffle(self.data)
        split_index = int(len(self.data) * self.split_ratio)
        X, y = [], []
        for verb_info, conjugation_class, conjugation_info in self.data:
            X.append(verb_info)
            y.append(conjugation_class)
        return X, y
    
    def get_train_test_data(self):
        """
        | Returns the training and testing data
        
        :return: tuple.
        A tuple of numpy arrays containing the train and test data respectively.
       """
        train_data = self.data.sample(frac=0.8, random_state=1)
        test_data = self.data.drop(train_data.index)
        return train_data[self.feature_cols], train_data[self.target_col], test_data[self.feature_cols], test_data[self.target_col]
    
    def get_data(self):
        """
        Retrieves the entire dataset.
        :return: pandas DataFrame.
            The entire dataset.
        """
        return self.data
        
    def get_feature_cols(self):
        """
        Retrieves the feature columns of the dataset.
        :return: list.
            List of feature column names.
        """
        return self.feature_cols
        
    def get_target_col(self):
        """
        Retrieves the target column of the dataset.
        :return: string.
            Name of the target column.
        """
        return self.target_col
        
    def get_class_labels(self):
        """
        Retrieves the class labels of the dataset.
        :return: list.
            List of class labels.
        """
        return self.class_labels


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
        """
        return extract_verb_features(verb, lang, ngram_range)


if __name__ == "__main__":
    pass
